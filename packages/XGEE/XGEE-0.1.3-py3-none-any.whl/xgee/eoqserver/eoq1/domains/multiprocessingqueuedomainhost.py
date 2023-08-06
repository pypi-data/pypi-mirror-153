'''
Created on 24.06.2019

@author: Annighoefer
'''

from ..model import DomainA
from .. import CommandParser
from .. import ResultParser

import threading
from multiprocessing import Queue
import queue # imported for using queue.Empty exception

class MultiprocessingQueueDomainHost(DomainA):
    def __init__(self,domain,timeout=0.1):
        self.domain = domain
        self.cmdQueue = Queue()
        self.resQueue = Queue()
        self.timeout = timeout
        self.shallRun = True
        
    def Start(self):
        self.listenerThread = threading.Thread(target=self.__RemoteCommandHandler, args=())
        self.listenerThread.start()
        
    def Join(self):
        self.shallRun = False
        self.listenerThread.join()
        
    def __RemoteCommandHandler(self):
        while self.shallRun:
            try:
                cmdStr = self.cmdQueue.get(timeout=self.timeout)
                cmd = CommandParser.StringToCommand(cmdStr)
                res = self.domain.Do(cmd)
                resStr = ResultParser.ResultToString(res)
                self.resQueue.put(resStr) 
            except queue.Empty:
                continue
            except:
                break