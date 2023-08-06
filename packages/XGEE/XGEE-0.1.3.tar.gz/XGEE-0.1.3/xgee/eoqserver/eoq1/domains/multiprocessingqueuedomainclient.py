from ..model import DomainA, CommandA, ResultA, ErrorResult
from .. import CommandParser
from .. import ResultParser

from multiprocessing import Queue
import queue # imported for using queue.Empty exception

class MultiprocessingQueueDomainClient(DomainA):
    def __init__(self,cmdQueue : Queue,resQueue : Queue,timeout=1000000):
        self.cmdQueue = cmdQueue
        self.resQueue = resQueue
        self.timeout = timeout
        
    def Do(self, command : CommandA) -> ResultA:
        cmdStr = CommandParser.CommandToString(command)
        self.cmdQueue.put(cmdStr)
        try:
            resultStr = self.resQueue.get(timeout=self.timeout)
            result = ResultParser.StringToResult(resultStr)
        except queue.Empty:
            result = ErrorResult()
            result.code = 9880
            result.message = "Internal multiprocessing queue receive timout after %s s."%(self.timout)
        
        return result
        

