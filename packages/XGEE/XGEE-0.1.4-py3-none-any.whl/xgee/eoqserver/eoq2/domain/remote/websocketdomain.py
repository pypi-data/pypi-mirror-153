'''
    A remote WebSocket domain for EOQ2
    based on the jseoq web socket domain by Bjoern Annighoefer (https://gitlab.com/eoq/js/eoq2)
    (C) 2021 Matthias Brunner
'''

import websocket
import threading
import time
import uuid
import traceback

from eoq2 import Hel,Gby
from eoq2.domain import Domain
from eoq2 import __version__ as eoqVersion
from eoq2.frame import Frame,FrameTypes


class Timeout(Exception):
    def __init__(self):
        super().__init__(self)
    
class WebSocketDomainNotConnected(Exception):
    def __init__(self):
        super().__init__()


class PendingCommand():
    def __init__(self,sessionId,cmd,timeout):
        #Session
        self.sessionId=sessionId

        # Command
        self.cmd=cmd
        self.timeout=timeout
        self.sent=time.time()

        # Results
        self.__rxEvent=threading.Event()
        self.ready=True
        self.received=None
        self.res=None

    def wait(self,timeout=None):
        return self.__rxEvent.wait(timeout)

    def setResults(self,res):
        self.read=True
        self.received=time.time()
        self.res=res
        self.__rxEvent.set()


class WebSocketDomain(Domain):
    def __init__(self,url,timeout,serializer,retries=50,retryTimeout=5,retryWait=1):
        super().__init__()

        # Retry configuration
        self.__retries=retries
        self.__retryWait=retryWait # in seconds
        self.__retryTimeout=retryTimeout # in seconds

        self.__url=url # user selected url
        self.__timeout=timeout # timeout of the connection
        self.__serializer=serializer
        self.__pendingCmds=dict()

        self.__numericVersion=int(eoqVersion.replace(".", ""))

        # To be initialized later
        self.__webSocketReady=None
        self.__webSocket=None
        self.__webSocketUrl=None
        self.__webSocketThread=None
        self.__sessionId=None

        # Open web-socket to target url
        self.__Open(self.__url)

    def __IsOpened(self):
        res=False
        if not self.__webSocket is None:
            res=True
        return res

    def __thread(self):
        try:
            self.__webSocket.run_forever()
        except KeyboardInterrupt:
            print('Websocket thread is stopping')

    def __TryOpen(self,url):
        self.__webSocketReady=threading.Event()
        self.__webSocketUrl=url      
        self.__webSocket = websocket.WebSocketApp(self.__webSocketUrl,    
                            on_open=lambda ws: self.__OnOpen(ws),                           
                            on_message=lambda ws,msg: self.__OnMessage(ws,msg),
                            on_error=lambda ws,error: self.__OnError(ws,error),
                            on_ping=lambda ws: self.__OnPing(ws),
                            on_close=lambda ws,close_code,close_reason: self.__OnClose(ws,close_code,close_reason))
        self.__webSocketThread=threading.Thread(target=self.__thread)
        self.__webSocketThread.daemon = True
        self.__webSocketThread.start()

    def __Open(self,url):
        if not self.__IsOpened():
 
            self.__TryOpen(url) # Initial try      
            ready=False
            retry=0      
                  
            while not ready and self.__retries>0:
                 self.__retries-=1                 
                 self.__TryOpen(url)
                 ready=self.__webSocketReady.wait(self.__retryTimeout)    # wait for websocket to become ready
                 retry+=1

            if ready:   # Succeeded to connect       
                self.__InitSession()
                print('Connected to EOQ remote domain at '+str(url))
            else:       # Failed to connect
                print('Failed to connect to EOQ remote domain at '+str(url))     
                raise WebSocketDomainNotConnected()    
        
        else:
            raise ValueError('Could not open WebSocket to domain: already open')
        return True
   
    def __Abort(self,reason='unknown'):
        print('Aborted, reason='+str(reason))
        self.__Close()


    def __InitSession(self):
        res=self.RawDo(Hel('user','password'))     
        self.__sessionId=res.v
        print('Session ID is : '+str(self.__sessionId))

    def __terminateSession(self):
        if self.__sessionId is not None:
            res=self.RawDo(Gby(self.__sessionId))
            print('Session with ID '+str(self.__sessionId)+' terminated')

    def __getCmdId(self):        
        return str(uuid.uuid4())       

    def RawDo(self,cmd,sessionId=None,wait=True):
        res=None
        if self.__IsOpened():
            cmdId=self.__getCmdId()
            # Register as pending command
            self.__pendingCmds[cmdId]=PendingCommand(sessionId,cmd,self.__timeout)
            frame=Frame(FrameTypes.CMD,cmdId,cmd,self.__numericVersion)
            frames=[frame]
            serializedFrames = self.__serializer.serialize(frames)
            self.__webSocket.send(serializedFrames)
        else:
            raise ValueError('Cannot process command on web-socket domain. The web-socket connection is not open.')

        response=self.__WaitForResponse(self.__timeout,cmdId)  
        if response[0]:
            res=response[1]
        else:
            raise Timeout()

        return res

    def __WaitForResponse(self,timeout,cmdId):
        res=False,None
        if cmdId in self.__pendingCmds:
            pendingCmd=self.__pendingCmds[cmdId]        
            received=pendingCmd.wait()              
            if received:
                res=True,pendingCmd.res    
        else:
            raise ValueError('Command with '+str(cmdId)+' is unknown')
        return res        

    def __OnOpen(self,ws,a=None,b=None):
        self.__webSocketReady.set()

    def __OnPing(self,ws,a=None,b=None):
        pass

    def __OnMessage(self,ws=None,serializedFrames=[]):  
        frames=self.__serializer.deserialize(serializedFrames)
        for frame in frames:            
            if frame.uid in self.__pendingCmds:
                self.__pendingCmds[frame.uid].setResults(frame.dat)
                del self.__pendingCmds[frame.uid]

    def __OnError(self,ws,error):

        ws.keep_running=False
        errorHandlers={
             'ConnectionRefusedError':lambda error: print(error)
        }

        # Shutting down WebSocket Thread
        self.__webSocket.keep_running=False       

        if error.__class__.__name__ in errorHandlers:
            errorHandlers[error.__class__.__name__](error)
        else:  
            self.__Abort('Unhandled '+error.__class__.__name__)

       

    def __OnClose(self,ws,close_code,close_reason):
        self.__sessionId=None
    
    def __Close(self):
        self.__terminateSession()
        self.__webSocket.close()
        self.__webSocket=None

    def Close(self):
        self.__Close()


