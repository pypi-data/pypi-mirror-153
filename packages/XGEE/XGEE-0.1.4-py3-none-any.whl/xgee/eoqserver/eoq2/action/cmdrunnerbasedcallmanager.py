'''
 2019 Bjoern Annighoefer
'''
from ..action.callmanager import CallManager
from ..action.call import CallOptions

from .call import CallTypes,CallStatus,Call,CALL_STATUS_FINAL_TYPES
from ..event import CstEvt,CvaEvt,OupEvt,ALL_EVENT_TYPES
from ..util import EoqError,DATE_TIME_STR_FORMAT

from datetime import datetime


'''
  CmdRunnerBaseCallManager
'''

class CmdRunnerBasedCallManager(CallManager):
    def __init__(self,cmdRunner,callId=-1):
        super().__init__(callId)
        self.cmdRunner = cmdRunner
        self.actionInfos = {} #'action name' -> (action,handler)
        self.currentCallId = 0 #only for async calls
        self.runningCalls = {} #callid -> (callback handler, abort handler, call status,)
    
    def RegisterAction(self,name,action,handler):
        self.actionInfos[name] = (action,handler)
        
    def UnregisterAction(self,name):
        self.actionInfos.pop(name)
        
    def GetAllActions(self):
        return [value[0] for key, value in sorted(self.actionInfos.items())]
    
    def FinalizeAsyncCall(self,call):
        #check if the action is terminated in case of an async action
        if(CallTypes.ASY == call.ctype and call.status in CALL_STATUS_FINAL_TYPES and call.hasValue):
            if(call.opts.autoobserve and call.parentSessionId):
                self.cmdRunner.Ubs(call.parentSessionId,'*',str(call.callId))
            self.cmdRunner.CloseTempSession(call.sessionId) #free the actions session
       
    def ChangeCallStatus(self,callId,status,info=''):
        if(callId in self.runningCalls):
            call = self.runningCalls[callId]
            if(call.status != status): #make sure this is really an update
                call.status = status
                self.NotifyObservers([CstEvt(callId,status,info)])
                self.FinalizeAsyncCall(call)
            
    def SetCallValue(self,callId,value):
        if(callId in self.runningCalls):
            call = self.runningCalls[callId]
            call.value = value
            call.hasValue = True
            self.NotifyObservers([CvaEvt(callId,value)],self)
            self.FinalizeAsyncCall(call)
            
    def AddCallOutputRaw(self,callId,channelName,data):
        if(callId in self.runningCalls):
            callInfo = self.runningCalls[callId]
            if(channelName in callInfo.outputs):
                callInfo.outputs[channelName] += data
            else:
                callInfo.outputs[channelName] = data
            self.NotifyObservers([OupEvt(callId,channelName,data)],self)
            
    def AddCallOutput(self,channelName,data):
        self.AddCallOutputRaw(self.callId,channelName,data)
            
    def RunCallSync(self,name,args,optsArr,tid,sessionId=None):
        #name = args[0]
        #obtain the handler
        info = self.actionInfos[name]
        action = info[0]
        handler = info[1]
        #check if the arguments are appropriate
        nActionArgs = len(args)
        nExpectedArgs = len(action.args)
        if(nActionArgs!=nExpectedArgs):
            raise EoqError(0,"Action %s requires %s arguments, but got %d."%(name,nExpectedArgs,nActionArgs))
        #parse options
        opts = CallOptions()
        opts.FromArray(optsArr)
        #call the handler
        domain = CallDomain(self.cmdRunner,tid) #create a private domain to be used within the action
        callInfo = self.CreateNewCall(domain,name,args,opts,handler,CallTypes.SYN,sessionId)
        
        if(opts.autoobserve and sessionId):
            self.cmdRunner.Obs(sessionId,'*',str(callInfo.callId))
        value = handler.HandleSync(name,callInfo.callId,domain,args,opts,self)
        if(opts.autoobserve and sessionId):
            self.cmdRunner.Ubs(sessionId,'*',str(callInfo.callId))
        callOutputs = [[i[0],i[1]] for i in callInfo.outputs.items()] #dict needs to be removed
        result = [callInfo.callId,value,callInfo.status,callOutputs]
        return result
    
    def RunCallAsync(self,name,args,optsArr,tid,sessionId=None,parentSessionId=None):
        info = self.actionInfos[name]
        action = info[0]
        handler = info[1]
        #check if the arguments are appropriate
        nActionArgs = len(args)
        nExpectedArgs = len(action.args)
        if(nActionArgs!=nExpectedArgs):
            raise EoqError(0,"Action %s requires %s arguments, but got %d."%(name,nExpectedArgs,nActionArgs))
        #parse options
        opts = CallOptions()
        opts.FromArray(optsArr)
        #call the handler
        domain = AsyncCallDomain(self.cmdRunner) #create a private domain to be used within the action
        callInfo = self.CreateNewCall(domain,name,args,opts,handler,CallTypes.ASY,sessionId,parentSessionId)
        
        if(opts.autoobserve and parentSessionId):
            self.cmdRunner.Obs(parentSessionId,'*',str(callInfo.callId))
        handler.HandleAsync(name,callInfo.callId,domain,args,opts,self,sessionId=sessionId)
        result = callInfo.callId
        return result
    
    
    def AbortCall(self,callId,tid):
        try:
            callInfo = self.runningCalls[callId]
            if(callInfo.ctype == CallTypes.SYN):
                raise EoqError(0,"Call %d is synchronous. Only asynchronous calls can be aborted."%(callId))
            if(callInfo.status in CALL_STATUS_FINAL_TYPES):
                raise EoqError(0,"Call %d is not running any more."%(callId))
            result = callInfo.handler.AbortCall(callId)
            if(result):
                callInfo.endTime = datetime.now()
                callStatusInfo = "Action %s started %s was aborted at %s (elapsed time: %d s) "%(
                    callInfo.name,
                    callInfo.startTime.strftime(DATE_TIME_STR_FORMAT),
                    callInfo.endTime.strftime(DATE_TIME_STR_FORMAT),
                    (callInfo.endTime-callInfo.startTime).total_seconds()
                    )
                self.ChangeCallStatus(callId, CallStatus.ABO,callStatusInfo)
        except KeyError:
            raise EoqError(0,"Call id %d is unknown."%(callId))
        return result
    
    '''
     PRIVATE METHODS
    '''
   
    def CreateNewCall(self,domain,name,args,opts,handler,ctype,sessionId=None,parentSessionId=None):
        callId = self.currentCallId
        self.currentCallId+=1
        callInfo = Call(callId,domain,name,args,opts,handler,ctype,sessionId,parentSessionId=parentSessionId)
        callInfo.startTime = datetime.now()
        self.runningCalls[callId] = callInfo
        return callInfo
    
'''
    A domain that wraps a specific transaction id
    Is used internally in the command runner for executing actions
'''   
        
from ..domain.domain import Domain
        
class CallDomain(Domain):
    def __init__(self,cmdRunner,tid):
        self.cmdRunner = cmdRunner
        self.tid = tid
       
    #@override 
    def RawDo(self,cmd,sessionId=None):
        # TODO: fix sessionId to do something
        res = self.cmdRunner.ExecOnTransaction(cmd,self.tid)
        return res
    
class AsyncCallDomain(Domain):
    def __init__(self,cmdRunner):
        super().__init__()
        self.cmdRunner = cmdRunner
       
    #@override 
    def RawDo(self,cmd,sessionId=None):
        res = self.cmdRunner.Exec(cmd,sessionId=sessionId)
        return res
    
    #Override the event provid methods since the sole event provider shall be the cmd runner
    #@Override
    def Observe(self,callback,eventTypes=ALL_EVENT_TYPES,context=None,sessionId=None): #by default register for all events
        self.cmdRunner.Observe(callback,eventTypes,context,sessionId)
    
    #@Override    
    def Unobserve(self,callback,context=None):
        self.cmdRunner.Unobserve(callback,context)
        
    #@Override
    def NotifyObservers(self,evts,excludedCallback=None,excludedContext=None):
        self.cmdRunner.NotifyObservers(evts,excludedCallback,excludedContext)
