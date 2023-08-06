'''
 Bjoern Annighoefer 2019
'''

from ..event import EvtProvider,ALL_EVENT_TYPES

class FrameHandler(EvtProvider):
    def __init__(self):
        self.observers = {}
    
    def Handle(self,frames,sessionId=None):
        pass
    
    def Gby(self,sessionId):
        pass
    
    #Override the event provid methods since the sole event provider shall be the cmd runner
    #@Override
    def Observe(self,callback,eventTypes=ALL_EVENT_TYPES,context=None,sessionId=None): #by default register for all events
        pass #needs to be overwritten in frame handler implementation
    
    #@Override    
    def Unobserve(self,callback,context=None):
        pass #needs to be overwritten in frame handler implementation