'''
 2019 Bjoern Annighoefer
'''


from ...action import CallManager
from ...frame import FrameTypes,Frame
from ...event.event import CstEvt,OupEvt,CvaEvt

class MutliprocessingQueueCallManager(CallManager):
    def __init__(self,cmdQueue,serializer,callId=-1):
        super().__init__(callId)
        self.cmdQueue = cmdQueue
        self.serializer = serializer
    
    def ChangeCallStatus(self,callId,status,info=''):
        evt = CstEvt(callId,status,info)
        frame = Frame(FrameTypes.EVT,0,evt)
        frameStr = self.serializer.Ser([frame])
        self.cmdQueue.put(frameStr)
            
    def SetCallValue(self,callId,value):
        evt = CvaEvt(callId,value)
        frame = Frame(FrameTypes.EVT,0,evt)
        frameStr = self.serializer.Ser([frame])
        self.cmdQueue.put(frameStr)
            
    def AddCallOutputRaw(self,callId,channelName,data):
        evt = OupEvt(callId,channelName,data)
        frame = Frame(FrameTypes.EVT,0,evt)
        frameStr = self.serializer.Ser([frame])
        self.cmdQueue.put(frameStr)


