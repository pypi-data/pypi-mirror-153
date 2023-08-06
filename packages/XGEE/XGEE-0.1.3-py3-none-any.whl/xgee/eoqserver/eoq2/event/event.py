'''
 2019 Bjoern Annighoefer
'''

class EvtTypes:
    CHG = "CHG" # change
    WAT = "WAT" # watch event (not implemented)
    OUP = "OUP" # output of a call
    INP = "INP" # input for a call
    CST = "CST" # call status change
    CVA = "CVA" # call value change event
    MSG = "MSG" # message
    CUS = "CUS" # custom event with user defined structure
    VCA = "VCA" # validation constraint added
    VCR = "VCR" # validation constraint removed
    VCS = "VCS" # validation constraint status
    
class ChgTypes:
    SET = 'SET'
    ADD = 'ADD'
    REM = 'REM'
    MOV = 'MOV'
    ADC = 'ADC'
    RMC = 'RMC'
    
    
ALL_EVENT_TYPES = [EvtTypes.CHG,EvtTypes.OUP,EvtTypes.INP,EvtTypes.CST,EvtTypes.CVA,EvtTypes.MSG,EvtTypes.VCA,EvtTypes.VCR,EvtTypes.VCS]
    
        
class Evt:
    def __init__(self,ctype,key,args):
        self.evt = ctype
        self.k = key
        self.a = args  
  
class ChgEvt(Evt):
    def __init__(self,cid,ctype,target,feature,newVal=None,oldVal=None,oldOwner=None,oldFeature=None,oldIndex=None,tid=0,user='',sessionNumber=0):
        key = '%s:%s:%s'%(target,ctype,feature)
        super().__init__(EvtTypes.CHG,key,[cid,ctype,target,feature,newVal,oldVal,oldOwner,oldFeature,oldIndex,tid,user,sessionNumber])
        
class OupEvt(Evt):
    def __init__(self,callId,channelName,data):
        key = str(callId)
        super().__init__(EvtTypes.OUP,key,[callId,channelName,data])
        
class InpEvt(Evt):
    def __init__(self,callId,channelName,data):
        key = str(callId)
        super().__init__(EvtTypes.INP,key,[callId,channelName,data])
        
class CstEvt(Evt):
    def __init__(self,callId,status,info=''):
        key = str(callId)
        super().__init__(EvtTypes.CST,key,[callId,status,info])
        
class CvaEvt(Evt):
    def __init__(self,callId,value):
        key = str(callId)
        super().__init__(EvtTypes.CVA,key,[callId,value])
        
class MsgEvt(Evt):
    def __init__(self,key,msg):
        super().__init__(EvtTypes.MSG,key,msg)
        
class CusEvt(Evt):
    def __init__(self,key,data):
        super().__init__(EvtTypes.CUS,key,data)

class VcaEvt(Evt):
    def __init__(self,cid,ctype,target,feature,constraint):
        key = '%s:%s:%s'%(target,ctype,feature)
        super().__init__(EvtTypes.VCA,key,[cid,ctype,target,feature,constraint])

class VcrEvt(Evt):
    def __init__(self,cid,ctype,target,feature,constraint):
        key = '%s:%s:%s'%(target,ctype,feature)
        super().__init__(EvtTypes.VCA,key,[cid,ctype,target,feature,constraint])

class VcsEvt(Evt):
    def __init__(self,cid,ctype,target,feature,constraint):
        key = '%s:%s:%s'%(target,ctype,feature)
        super().__init__(EvtTypes.VCA,key,[cid,ctype,target,feature,constraint])
        
        
import traceback
import threading

class ObserverInfo:
    def __init__(self,callback,eventTypes,context,sessionId):
        self.callback = callback #the callback function of the event listener
        self.eventTypes = eventTypes #the events that are desired
        self.context = context #a unique identifier or None
        self.sessionId = sessionId #set if this observer is linked to a session
        
'''
    EventProvider
'''
class EvtProvider:
    def __init__(self):
        self.observers = {} # callback -> event
        self.eventQueu = [] #events reserved for the next notification
        #self.eventQueueMutex = threading.Lock()
        self.observerQueuMutex = threading.Lock()
        
    def Observe(self,callback,eventTypes=ALL_EVENT_TYPES,context=None,sessionId=None): #by default register for all events
        observerInfo = ObserverInfo(callback,eventTypes,context,sessionId)
        self.observerQueuMutex.acquire()
        try:
            self.observers[(callback,context)] = observerInfo
        finally:
            self.observerQueuMutex.release()
        
    def Unobserve(self,callback,context=None):
        self.observerQueuMutex.acquire()
        try:
            self.observers.pop((callback,context))
        finally:
            self.observerQueuMutex.release()
            
#     '''
#         EVENT FORWARDING
#     '''
#         
#     def ObserveExternalProvider(self,eventProvider,eventTypes=ALL_EVENT_TYPES,context=None):
#         eventProvider.Observe(self._OnExternalEvent,eventTypes,context)
#         
#     def UnobserveExternalProvider(self,eventProvider,context=None):
#         eventProvider.Unobserve(self._OnExternalEvent,context)
#     
#     def _OnExternalEvent(self,evts,src):
#         self.NotifyObservers(evts,src)
        
#     def QueuEvent(self,evt,src):
#         self.eventQueu.append(evt)

    '''
        INTERNAL EVENT PROCESSING
    '''

    def IsEventDesired(self,evt,callback,eventTypes,context,sessionId):
        return evt.evt in eventTypes
        
    def NotifyObservers(self,evts,excludedCallback=None,excludedContext=None): #sends multiple events 
        
        #copy the events from the internal list and release it
#         self.eventQueueMutex.acquire()
#         try:
#             newEvts = self.eventQueu + evts
#             self.eventQueu.clear()
#         finally:
#             self.eventQueueMutex.release()

        newEvts = evts.copy() #make a copy to ensure that the list is not changed outside when the event notification loop runs.
            
        
        self.observerQueuMutex.acquire()
        try:
            for observer in self.observers.items():
                observerInfo = observer[1]
                if(excludedCallback==observerInfo.callback and excludedContext==observerInfo.context):
                    continue
                filterdEvts = [e for e in newEvts if self.IsEventDesired(e,observerInfo.callback,observerInfo.eventTypes,observerInfo.context,observerInfo.sessionId)]
                #if(evt.evt in item[1] and excludedObserver!=item[0]):
                try:
                    if(0<len(filterdEvts)):
                        observerInfo.callback(filterdEvts,self)
                except:
                    print("EvtProvider: Warning observer callback failed:")
                    traceback.print_exc()
        finally:
            self.observerQueuMutex.release()
        