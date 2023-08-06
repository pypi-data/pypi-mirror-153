'''
 2019 Bjoern Annighoefer
'''

from ..event import EvtProvider

'''
  CALL MANAGER
'''

class CallManager(EvtProvider):
    def __init__(self,callId=-1):
        super().__init__()
        self.callId = callId
        
    def RegisterAction(self,name,action,handler):
        pass
        
    def UnregisterAction(self,name):
        pass
        
    def GetAllActions(self):
        pass
       
    def ChangeCallStatus(self,callId,status,info=''):
        pass
            
    def SetCallValue(self,callId,value):
        pass
            
    def AddCallOutputRaw(self,callId,channelName,data):
        pass
            
    def AddCallOutput(self,channelName,data):
        self.AddCallOutputRaw(self.callId,channelName,data)
            
    def RunCallSync(self,name,args,opts,tid,sessionId=None):
        pass

    def RunCallAsnyc(self,name,args,opts,tid,sessionId=None,parentSessionId=None):
        pass
    
    def AbortCall(self,callId,tid):
        pass
        
