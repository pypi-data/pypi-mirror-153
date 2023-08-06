'''
 Bjoern Annighoefer 2019
 '''

from .framehandler import FrameHandler
from .frame import FrameTypes
from ..event import ALL_EVENT_TYPES

class HandlerInfo:
    def __init__(self,handler,version):
        self.version = version
        self.handler = handler
    
class MultiVersionFrameHandler(FrameHandler):
    def __init__(self,handlerInfos=[]):
        super().__init__()
        self.handlers = []
        for handlerInfo in handlerInfos:
            self.AddHandler(handlerInfo[0], handlerInfo[1]) #handler infos must be list of tuples
        
    def Handle(self,frames,sessionId=None):
        for i in range(len(frames)):
            wasHandled = False
            for handlerInfo in self.handlers:
                if(frames[i].ver >= handlerInfo.version):
                    frames[i] = handlerInfo.handler.Handle([frames[i]],sessionId)[0]
                    wasHandled = True
                    break
            if(not wasHandled):
                errorMsg = "Could not find a frame handler for version %d"%(frames[i].ver)
                print("WARNING: %s"%(errorMsg))
                frames[i].eoq = FrameTypes.ERR
                frames[i].dat = errorMsg
        return frames   
    
    #@Override 
    def Gby(self,sessionId):
        for handlerInfo in self.handlers:
            handler = handlerInfo.handler
            handler.Gby(sessionId)
        
    def AddHandler(self,version,handler):
        self.handlers.append(HandlerInfo(handler,version))
        self.handlers = sorted(self.handlers, key=lambda a: a.version,reverse=True)
        #handler.ObserveEvents(self.OnHandlerEvent)
        
    #@Override 
    def Observe(self,callback,eventTypes=ALL_EVENT_TYPES,context=None,sessionId=None): #by default register for all events
        for handlerInfo in self.handlers:
            handler = handlerInfo.handler
            handler.Observe(callback,eventTypes,context,sessionId)
    
    #@Override    
    def Unobserve(self,callback,context=None):
        for handlerInfo in self.handlers:
            handler = handlerInfo.handler
            handler.Unobserve(callback,context)
        