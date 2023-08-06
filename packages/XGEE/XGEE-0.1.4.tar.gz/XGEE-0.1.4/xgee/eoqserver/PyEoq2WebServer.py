import asyncio
import threading
import tornado.ioloop
import tornado.web
import tornado.websocket
import signal
import time

from uuid import uuid4

import traceback

import argparse

from eoq2 import __version__ as eoqVersion

from eoq2.mdb.pyecore import PyEcoreWorkspaceMdbProvider,PyEcoreMdbAccessor,PyEcoreIdCodec
from eoq2.domain.local import LocalMdbDomain

from eoq2.action.externalpy import ExternalPyScriptHandler
from eoq2.serialization import JsonSerializer,JsSerializer
from eoq2.util import ConsoleAndFileLogger,Backupper,LogLevels

from timeit import default_timer as timer

from eoq2.frame import DomainFrameHandler,MultiVersionFrameHandler,Frame,FrameTypes
from eoq2.legacy import LegacyDomain,LegacyTextFrameHandler

sessions = {} #store all sessions to prevent to create a dublicated session id

def CreateNewUniqueSessionId():
    global sessions
    sessionId = str(uuid4())
    while(sessionId in sessions):
        sessionId = str(uuid4())
    sessions[sessionId] = sessionId
    return sessionId

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Sorry, this is the wrong way to access the PyEoq-Web-Server.\nClone https://gitlab.com/mbrunner/ecoreeditor and start the index.html.")
        
class EoqHandler(tornado.web.RequestHandler):
    def initialize(self,eoq,serializer):
        self.start = timer()
        self.eoq = eoq
        self.serializer = serializer
        
    def post(self):
        cmdJson = self.get_body_argument("command")
        cmd = self.serializer.deserialize(cmdJson)
        result = self.eoq.Do(cmd)
        response = self.serializer.serialize(result)
        #output the response
        self.set_header("Content-Type", "text/plain")
        self.set_header('Access-Control-Allow-Origin','*') #Necessary to allow local requests
        self.write(response)
        self.end = timer()
        print("Request completed in %s s."%(self.end-self.start))
        
class PyEoq2WebSocket(tornado.websocket.WebSocketHandler):
    def initialize(self,frameHandler,serializer,logger):
        self.sessionId = CreateNewUniqueSessionId()
        self.frameHandler = frameHandler
        self.serializer = serializer
        self.logger = logger 
        #listen to events
        self.frameHandler.Observe(self.OnEvents,context=self,sessionId=self.sessionId) #only observe events specific to this session
        self.eventQueue = [] #the list of events to be send when it is next possible
        self.eventQueueMutex = asyncio.Lock()
        self.eventQueueMutex2 = threading.Lock();
        self.ioLoop = tornado.ioloop.IOLoop.current()
        
    #the check_origin override allows request from the local server
    def check_origin(self, origin):
        return True
    
    def open(self):
        pass

    def on_message(self, message):
        #print("WebSocket received: "+ message)
        start = timer()
        self.logger.PassivatableLog(LogLevels.DEBUG,lambda : "Web socket message received: %s"%(message))
        try:
            frames = self.serializer.Des(message)
            frames= self.frameHandler.Handle(frames,sessionId=self.sessionId)
            response = self.serializer.Ser(frames)
            self.write_message(response)
            end = timer()
            self.logger.PassivatableLog(LogLevels.DEBUG,lambda : "Web socket response (after %d s): %s"%(end-start,response))
        except Exception as e:
            self.logger.Error("Invalid message received: %s (error: %s)"%(message,str(e)))
            self.logger.Error(traceback.format_exc())
            #raise Exception()

    def on_close(self):
        #quit listening to events
        self.frameHandler.Unobserve(self.OnEvents,context=self)
        #force closing the session
        self.frameHandler.Gby(self.sessionId)
        
    def SendEvents(self):
        # !! This must be called in the main thread of tornado !!
        self.eventQueueMutex2.acquire()
        try:
        #with self.eventQueueMutex:
            # pack events in frames    
            frames = []
            for evt in self.eventQueue:
                frame = Frame(FrameTypes.EVT,0,evt)
                frames.append(frame)
            # clear the event queue
            self.eventQueue.clear()
            # send events 
            response = self.serializer.Ser(frames)
            if(isinstance(response, str)):
                self.write_message(response) 
            else:
                self.logger.Warn("Got non-string response of type %s: %s"%(type(response).__name__,str(response)))
        finally:
            self.eventQueueMutex2.release();
    
    def OnEvents(self,evts,src):
        #!! Attention this is called from the outside (from any thread) and is, therefore, 
        # not in the tornado IO loop and can not safely call write!!!
        self.eventQueueMutex2.acquire();
        try:
        #with self.eventQueueMutex:
            for evt in evts:
                self.eventQueue.append(evt)
            # make sure the events are processed in the main thread
            self.ioLoop.add_callback(self.SendEvents)
        finally:
            self.eventQueueMutex2.release();
        

class PyeoqWebSocketServer:
    def __init__(self):
        self.ioLoop = None
        self.backupper = None
        self.logger = None
        self.mdbProvider = None
        self.valueCodec = None
        self.mdbAccessor = None
        self.domain = None
        self.frameHandler = None
        self.externalActionHandler = None
        self.app = None
        self.httpServerApi = None
        self.args = None
        self.isRunning = False
        

    def Start(self,args):
        self.args = args
        self.isRunning = True
        #start local ioloop
        self.ioLoop = tornado.ioloop.IOLoop()
        self.ioLoop.make_current()
        
        
        #Do backup if required
        if(args.backup):
            self.backupper = Backupper([args.workspaceDir,args.logDir])
            self.backupper.CreateBackup()
        
        #initialize logger. For the file based logger this must happen after the backup
        #logger = ConsoleLogger()
        self.logger = ConsoleAndFileLogger(logDir=args.logDir,toConsole=args.logToConsole,toFile=args.logToFile,activeLevels=[LogLevels.INFO,LogLevels.WARN,LogLevels.ERROR,"change","event"])
        #define a global serializer for outputs
        self.debugSerializer = JsSerializer()
              
        #initialize EOQ
        self.mdbProvider = PyEcoreWorkspaceMdbProvider(args.workspaceDir,metaDir=[args.metaDir],saveTimeout=args.autosave,logger=self.logger,trackFileChanges=args.trackFileChanges)
        self.valueCodec = PyEcoreIdCodec()
        self.mdbAccessor = PyEcoreMdbAccessor(self.mdbProvider.GetMdb(),self.valueCodec)
        self.domain = LocalMdbDomain(self.mdbAccessor,maxChanges=args.maxChanges,logger=self.logger,serializer=self.debugSerializer, enableBenchmark=args.enableBenchmark)
        self.mdbProvider.CoupleWithDomain(self.domain, self.valueCodec)
        
        #register external actions if required
        if(args.actions):
            self.externalActionHandler = ExternalPyScriptHandler(self.domain.cmdRunner.callManager,args.actionsDir,logger=self.logger)
        
        
        
        #initialize frame handlers in order to support legacy frames
        self.frameHandler = MultiVersionFrameHandler([
            (100,LegacyTextFrameHandler(LegacyDomain(self.domain,serializer=self.debugSerializer,logger=self.logger),logger=self.logger)),
            (200,DomainFrameHandler(self.domain))
            ])
        
        #define serializer for all client communication
        self.serializer = JsonSerializer()
        
        #start webserver
        print("Initiating tornado application... ",end='')
        self.app = tornado.web.Application([
            (r"/", MainHandler),
            (args.ws, PyEoq2WebSocket, dict(frameHandler=self.frameHandler,serializer=self.serializer,logger=self.logger))
        ])
        self.httpServerApi = tornado.httpserver.HTTPServer(self.app)
        print("ok")
        
        port = args.port
        print("Opening port %d... "%(port),end='')
        self.httpServerApi.listen(port)
        print("ok")
        
        print("Server is running...")
        tornado.ioloop.IOLoop.current().start()
        
    def Stop(self,sig,frame):
        print('Shutting down...')
        print('Stopping tornado... ',end='')
        asyncio.run(self.httpServerApi.close_all_connections()) # Is this necessary? Seems not possible to wait here
        self.httpServerApi.stop()
        self.ioLoop.stop()
        time.sleep(3) #wait for tornado to close
        print('ok')
        print('Closing the domain... ',end='')
        self.domain.Close()
        print('ok')
        print('Closing the mdb... ',end='')
        self.mdbProvider.Close()
        print('ok')
        self.isRunning = False



if __name__ == "__main__":
    version = "2.2.1" #to be changed manually in accordance to EOQ version
    #get commandline arguments
    parser = argparse.ArgumentParser(description='An eoq2 server listening for commands on a web socket.')
    parser.add_argument('--ws', metavar='ws', type=str, default='/ws/eoq.do', help='the websocket url', dest='ws')
    parser.add_argument('--port', metavar='port', type=int, default=8000, help='the port name the EOQ server shall listen to', dest='port')
    parser.add_argument('--workspaceDir', metavar='workspaceDir', type=str, default='./workspace', help='the root directory including the model files to work with', dest='workspaceDir')
    parser.add_argument('--metaDir', metavar='metaDir', type=str, default='./.meta', help='The directory including the meta models of known model formats. This is relative to the workspace', dest='metaDir')
    parser.add_argument('--actions', metavar='actions', type=int, default=1, help='Whether external actions shall be available or not. (0=no, 1=yes)', dest='actions')
    parser.add_argument('--actionsDir', metavar='actionsDir', type=str, default='./workspace/actions', help='The directory containing action files', dest='actionsDir')
    parser.add_argument('--timeout', metavar='timeout', type=float, default=10.0, help='The maximum timeout for a transaction', dest='timeout')  
    parser.add_argument('--backup', metavar='backup', type=int, default=1, help='Shall a backup of the workspace and logs be created? (0=no, 1=yes)', dest='backup')   
    parser.add_argument('--backupDir', metavar='backupDir', type=str, default='./backup', help='Destination folder for the backup', dest='backupDir')   
    parser.add_argument('--logDir', metavar='logDir', type=str, default='./log', help='Destination folder for log files', dest='logDir')  
    parser.add_argument('--logToConsole', metavar='logToConsole', type=int, default=0, help='Print log messages in the console? (0=no, 1=yes)', dest='logToConsole')   
    parser.add_argument('--logToFile', metavar='logToFile', type=int, default=1, help='Print log messages in log files? (0=no, 1=yes)', dest='logToFile')   
    parser.add_argument('--autosave', metavar='autosave', type=float, default=5.0, help='The timeout after that autosave is triggered', dest='autosave')   
    parser.add_argument('--trackFileChanges', metavar='trackFileChanges', type=int, default=1, help='Update models if files in the workspace dir change? (0=no, 1=yes)', dest='trackFileChanges')
    parser.add_argument('--maxChanges', metavar='maxChanges', type=int, default=10000, help='How many changes shall be remembered until the oldest change is forgotten (1 to 1000000)', dest='maxChanges') 
    parser.add_argument('--enableBenchmark', metavar='enableBenchmark', type=int, default=0, help='Messure the time for queries and commands and write log when closed? (0=no, 1=yes)', dest='enableBenchmark')     
    args = parser.parse_args()

    print("*******************************************")
    print("*           EOQ2  Web Server              *")
    print("*******************************************")
    print("Version:      %s"%(version))
    print("EOQ Version:  %s"%(eoqVersion))
    print("Workspace:    %s"%(args.workspaceDir))
    print("Web Socket:   %s"%(args.ws))
    print("Port:         %s"%(args.port))
    print("Max Changes:  %d"%(args.maxChanges))
    print("Track files:  %d"%(args.trackFileChanges))
    print("Benchmark:    %d"%(args.enableBenchmark))
    print("*******************************************")
    
    server = PyeoqWebSocketServer()
    serverThread = threading.Thread(target=server.Start, args=(args,))
        
    print("Registering signal listeners ... ",end='')
    signal.signal(signal.SIGTERM, server.Stop)
    signal.signal(signal.SIGINT,  server.Stop)
    print("ok")
    
    serverThread.start()
    time.sleep(1) #wait for the server thread to start
    
    #keep the main thread alive until the server is closed. This is mandatory to receive CTRL + C signals
    while server.isRunning:
        time.sleep(3)
        
    print('Goodbye!')
    