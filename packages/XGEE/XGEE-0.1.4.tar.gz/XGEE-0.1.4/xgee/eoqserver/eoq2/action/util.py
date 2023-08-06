'''
 2019 Bjoern Annighoefer
'''

from .call import CallStatus
from ..command.command import Cmp,Ubs
from ..query.query import His
from ..event.event import EvtTypes
from ..util.error import EoqCallError,EoqCallAborted

import time

def ShowProgress(progress):
    print('Total progress: %d%%'%(int(progress)))
    return


class CallObserver:
    def __init__(self,domain,forwardOutput=False):
        self.domain = domain
        self.callId = 0  
        self.forwardOutput = forwardOutput
        self.callFinished = False
        self.gotReturnValue = False
        self.callReturnValue = None
        self.callStatus = None
        self.statusMessage = ''
        
        #observe the domain
        self.domain.Observe(self.OnCallEvent,context=self)
        
    def __del__(self):
        self.domain.Unobserve(self.OnCallEvent,context=self)
        
    def WaitOnCall(self,action,args,opts):
        cmd = Cmp().Asc(action,args,opts).Obs('*',His(0))
        res = self.domain.Do(cmd)
        self.callId = res[0]
        
    def CleanUp(self):
        self.domain.Do(Ubs('*',str(self.callId)))
        
    def IsCallFinished(self):
        return self.callFinished
    
    def CallIsRunning(self):
        return not self.callFinished
    
    def GetCallResult(self):
        return self.callReturnValue
        
    def OnCallEvent(self,evts,source):
        for evt in evts: #the event handler always gets a list of events.
            if(evt.evt == EvtTypes.CST and evt.a[0]==self.callId):
                if(CallStatus.FIN == evt.a[1]):
                    self.callStatus = evt.a[1]
                    if(self.gotReturnValue):
                        self.callFinished = True #set only finished if return value was also received
                elif(CallStatus.ABO == evt.a[1] or CallStatus.ERR == evt.a[1]):
                    self.callStatus = evt.a[1]
                    self.statusMessage = evt.a[2]
                    self.callFinished = True
            elif(evt.evt == EvtTypes.CVA and evt.a[0]==self.callId):
                self.callReturnValue = evt.a[1]
                self.gotReturnValue = True
                if(CallStatus.FIN == self.callStatus):
                    self.callFinished = True
            elif(self.forwardOutput and evt.evt == EvtTypes.OUP and evt.a[0]==self.callId):
                self.domain.callManager.AddCallOutput(evt.a[1],evt.a[2])
                  

def AscAndWait(domain,action,args=[],opts=[],forwardOutput=False):
    observer = CallObserver(domain,forwardOutput=forwardOutput)
    observer.WaitOnCall(action,args,opts)
    #main wait loop
    while(observer.CallIsRunning()):
        time.sleep(0.1) #waste time until call is ready
    
    observer.CleanUp()
    
    if(CallStatus.ERR == observer.callStatus):
        raise EoqCallError(observer.statusMessage)
    elif(CallStatus.ABO == observer.callStatus):
        raise EoqCallAborted(observer.statusMessage)
    
    return observer.GetCallResult()



def UiMessageGeneric(state,*args):
    """ prints generalized messages that can be parsed by the UI """
    print('[{state}]'.format(state=state),*args)


def UiShowProgress(progress):
    """ Displays current progress """
    UiMessageGeneric('progress','{progress}%'.format(progress=round(progress)))


def ShowCalculatedProgress(index,target,startPercentage=0,targetPercentage=100,incrementer=1):
    """ Displays calculated process """
    return UiShowProgress(startPercentage + (index + incrementer) / target * (targetPercentage - startPercentage))


def UiStartTask(taskName):
    """ Indicates task start """
    UiMessageGeneric('Started Task',taskName)


def UiEndTask(taskName):
    """ Indicated task end """
    UiMessageGeneric('Ended Task',taskName)


def UiAnnounceTasks(taskNum):
    """ Indicated how many tasks are to be expected """
    UiMessageGeneric('Announced Tasks',taskNum)


def UiMessageInfo(*args):
    """ Indicates an info message """
    UiMessageGeneric('INFO',*args)


def UiMessageError(*args):
    """ Indicates an error message """
    UiMessageGeneric('ERROR',*args)


def UiMessageWarning(*args):
    """ Indicates a warning message """
    UiMessageGeneric('WARNING',*args)


def UiMessageSuccess(*args):
    """ Indicates a success message """
    UiMessageGeneric('SUCCESS',*args)


def UiItemSaved(*args):
    """ Indicates a saved-event """
    UiMessageGeneric('SAVED',*args)


def UiItemDeleted(*args):
    """ Indicates a deleted-event """
    UiMessageGeneric('DELETED',*args)


def UiItemChanged(*args):
    """ Indicates a changed-event """
    UiMessageGeneric('CHANGED',*args)


def UiItemCreated(*args):
    """ Indicates a created-event """
    UiMessageGeneric('CREATED',*args)


def UiItemLoaded(*args):
    """ Indicates a loaded-event """
    UiMessageGeneric('LOADED',*args)


def UiItemFound(*args):
    """ Indicates a found-event """
    UiMessageGeneric('FOUND',*args)
