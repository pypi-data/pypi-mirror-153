'''
 Bjoern Annighoefer 2019
 '''

from .frame import FrameTypes,Frame
from .framehandler import FrameHandler
from ..util import EoqError
from ..util.logger import NoLogging,LogLevels
from ..event import ALL_EVENT_TYPES

import traceback

class DomainFrameHandler(FrameHandler):
    def __init__(self,domain,logger=NoLogging()):
        super().__init__()
        self.domain = domain
        self.logger = logger
        #self.domain.Observe(self.OnDomainEvent)
    
    def Handle(self,frames,sessionId=None):
        for i in range(len(frames)):
            try:   
                if(FrameTypes.CMD == frames[i].eoq):
                    cmd = frames[i].dat
                    res = self.domain.RawDo(cmd,sessionId)
                    frames[i].dat = res
                    frames[i].eoq = FrameTypes.RES
                else: 
                    raise EoqError(0,"Can not handle frame type: %s"%(frames[i].eoq))
            except Exception as e:
                errorMsg = "Got invalid frame: %s"%(str(e))
                self.logger.Error(errorMsg)
                traceback.print_exc();
                frames[i].eoq = FrameTypes.ERR
                frames[i].dat = errorMsg
        return frames
    
    #@Override 
    def Gby(self,sessionId):
        self.domain.Gby(sessionId)
    
    #@Override 
    def Observe(self,callback,eventTypes=ALL_EVENT_TYPES,context=None,sessionId=None): #by default register for all events
        self.domain.Observe(callback,eventTypes,context,sessionId)
    
    #@Override    
    def Unobserve(self,callback,context=None):
        self.domain.Unobserve(callback,context)