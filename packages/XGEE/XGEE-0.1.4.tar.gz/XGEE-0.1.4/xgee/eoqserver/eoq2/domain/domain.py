'''
 2019 Bjoern Annighoefer
'''

from ..event.event import EvtProvider
from ..util.logger import NoLogging
from ..command.command import Gby

class Domain(EvtProvider):
    def __init__(self,logger=NoLogging()):
        super().__init__()
        self.logger = logger
        
    def RawDo(self,cmd,sessionId=None):
        pass
    
    def Do(self,cmd,sessionId=None):
        res = self.RawDo(cmd,sessionId)
        value = res.GetValue()
        return value
    
    def Gby(self,sessionId):
        return self.Do(Gby(sessionId))
    
    def Close(self):
        pass #is to be called if the domain closes down
    
                    
    
        
        