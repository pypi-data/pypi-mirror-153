'''
 2019 Bjoern Annighoefer
'''

from .multiprocessingcallmanager import MutliprocessingQueueCallManager
from ..domain import Domain
from ...serialization import JsonSerializer
from ...command.result import ResTypes,Res
from ...frame import Frame,FrameTypes
from ...util.error import EoqError

import queue # imported for using queue.Empty exception
import threading #used for the event observer



'''
 CLIENT
 
'''

class MultiprocessingQueueDomainClient(Domain):
    def __init__(self,cmdQueue,resQueue,evtQueue,callId=-1,serializer=JsonSerializer(),timeout=1000000):
        super().__init__()
        self.cmdQueue = cmdQueue
        self.resQueue = resQueue
        self.evtQueue = evtQueue
        self.timeout = timeout
        self.serializer = serializer
        self.callManager = MutliprocessingQueueCallManager(cmdQueue,serializer,callId)
        self.cmdId = 0
        
        ##create an event observing thread
        self.shallRun = True
        self.eventThread = threading.Thread(target=self.__EventObserverThread)
        self.eventThread.start()
        
        
    def Stop(self):
        self.shallRun = False
        
    def RawDo(self,cmd,sessionId=None):
        # TODO: fix sessionID
        currentCmdId = self.cmdId;
        self.cmdId += 1
        frame = Frame(FrameTypes.CMD,currentCmdId,cmd)
        framesStr = self.serializer.Ser([frame])
        self.cmdQueue.put(framesStr)
        try:
            resFramesStr = self.resQueue.get(timeout=self.timeout)
            resFrames = self.serializer.Des(resFramesStr)
            if(1 != len(resFrames) or resFrames[0].uid != currentCmdId):
                raise EoqError("MultiProcessingClientDomain: Received invalid response to cmd %d: len: %d, resId: %d"%(currentCmdId,len(resFrames),resFrames[0].uid))
            result = resFrames[0].dat
        except queue.Empty:
            result = Res(cmd.cmd,ResTypes.ERR,"Internal multiprocessing queue receive timeout after %s s."%(self.timeout))
        return result
    
    def __EventObserverThread(self):
        while(self.shallRun):
            try:
                evts = []
                framesStr = self.evtQueue.get(timeout=0.1)
                frames = self.serializer.Des(framesStr)
                for frame in frames:
                    if(frame.eoq==FrameTypes.EVT):
                        evts.append(frame.dat)
                if(0<len(evts)):
                    self.NotifyObservers(evts)
            except queue.Empty:
                continue
            except:
                break
        #thread terminates here
            
