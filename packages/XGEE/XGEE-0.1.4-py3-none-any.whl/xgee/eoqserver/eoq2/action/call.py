'''
 2019 Bjoern Annighoefer
'''
from ..util.error import EoqError

class CallTypes:
    SYN = 'SYN'
    ASY = 'ASY'
    
class CallStatus: 
    INI = 'INI' #initiated
    RUN = 'RUN' #running
    WAI = 'WAI' #waiting (e.g. for user input)
    ABO = 'ABO' #aborted
    ERR = 'ERR' #error
    FIN = 'FIN' #finished (successfully)
 
CALL_STATUS_FINAL_TYPES = [CallStatus.ABO,CallStatus.ERR,CallStatus.FIN] 

class CallOptions:
    def __init__(self):
        self.silent = False
        self.eventsonly = False
        self.timeout = 0.0 #0.0 = no timeout
        self.autoobserve = False
        
    def ToArray(self):
        return [
                'silent',self.silent,
                'eventsonly',self.eventsonly,
                'timeout',self.timeout,
                'autoobserve',self.autoobserve
                ]
        
    def FromArray(self,optionsArr):
        n = len(optionsArr)
        if(n % 2 == 1):
            raise EoqError(0,'Call options array must have an even length, but got length %d.'%(n))
        for i in range(0,n,2):
            name = optionsArr[i]
            val = optionsArr[i+1]
            if('silent' == name):
                if(isinstance(val,bool)):
                    self.silent = val
                else:
                    raise EoqError(0,'Wrong data type for call option %s. Expected bool, but got %s'%(name,val))
            elif('eventsonly' == name):
                if(isinstance(val,bool)):
                    self.eventsonly = val
                else:
                    raise EoqError(0,'Wrong data type for call option %s. Expected bool, but got %s'%(name,val))
            elif('timeout' == name):
                if(isinstance(val,float)):
                    self.timeout = val
                else:
                    raise EoqError(0,'Wrong data type for call option %s. Expected float, but got %s'%(name,val))
            elif('autoobserve' == name):
                if(isinstance(val,bool)):
                    self.autoobserve = val
                else:
                    raise EoqError(0,'Wrong data type for call option %s. Expected bool, but got %s'%(name,val))
            else:
                raise EoqError(0,'Unknown call option %s.'%(name))
                
                

'''
 CALL 
''' 
class Call: 
    def __init__(self,callId,domain,name,args,opts,handler,ctype,sessionId,status=CallStatus.INI,parentSessionId=None):
        self.callId = callId
        self.domain = domain
        self.name = name
        self.args = args
        self.opts = opts
        self.handler = handler
        self.ctype = ctype
        self.status = status
        self.sessionId = sessionId
        self.parentSessionId = parentSessionId
        self.outputs= {}
        self.hasValue = False
        self.value = None
        self.startTime = None
        self.endTime = None
        
        