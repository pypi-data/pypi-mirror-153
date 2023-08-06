'''
2019 Bjoern Annighoefer
'''

class LogLevels:
    DEBUG = "debug"
    INFO = "info"
    WARN = "warn"
    ERROR = "error"
    
DEFAULT_LOG_LEVELS = [LogLevels.INFO,LogLevels.WARN,LogLevels.ERROR]

class Logger:
    def __init__(self,activeLevels=DEFAULT_LOG_LEVELS):
        self.activeLevels = activeLevels
        
    def ShallLog(self):
        return True
    
    def Log(self,level,msg):
        if(level in self.activeLevels and self.ShallLog()):
            self._Log(level,msg)
            
    def PassivatableLog(self,level,func):
        if(level in self.activeLevels and self.ShallLog()):
            self._Log(level,func())
    
    def Debug(self,msg):
        self.Log(LogLevels.DEBUG, msg)
    
    def Info(self,msg):
        self.Log(LogLevels.INFO,msg)
        
    def Warn(self,msg):
        self.Log(LogLevels.WARN,msg)
        
    def Error(self,msg):
        self.Log(LogLevels.ERROR,msg)

    #the following must be overwritten to produce the output
    def _Log(self,level,msg):
        pass
        
        
'''
A default logger which does nothing
'''

class NoLogging(Logger):
    def __init__(self):
        super().__init__()
        
    #@Override
    def ShallLog(self):
        return False
    
    
'''
A default logger which does nothing
'''

class ConsoleLogger(Logger):
    def __init__(self,activeLevels=DEFAULT_LOG_LEVELS):
        super().__init__(activeLevels)

        
    #@Override         
    def _Log(self,level,msg):
        print("%s: %s"%(level,msg))

'''
A default logger that outputs every thing to the console and dedicated files for each active log level
'''

import os
import logging

class ConsoleAndFileLogger(Logger):
    def __init__(self,toConsole=True,toFile=True,logDir='./log',activeLevels=DEFAULT_LOG_LEVELS):
        super().__init__(activeLevels)
        self.toConsole = toConsole
        self.toFile = toFile
        self.logDir = logDir
        
        self.loggers = {}
        
        if(self.toFile):
            #make sure the
            if(not os.path.isdir(self.logDir)):
                os.makedirs(self.logDir)
            #create native python loggers for each level
            for level in self.activeLevels:
                #init error logger
                logger = logging.getLogger(level)
                logFile = os.path.join(self.logDir,"%s.log"%(level))
                fh = logging.FileHandler(logFile,'w')
                fh.setLevel(logging.INFO)
                formatter = logging.Formatter('%(asctime)s - %(message)s')
                fh.setFormatter(formatter)
                logger.addHandler(fh)
                logger.setLevel(logging.INFO)
                self.loggers[level] = logger
                
    #@Override
    def ShallLog(self):
        return (self.toConsole or self.toFile)
                
    #@Override         
    def _Log(self,level,msg):
        if(self.toConsole):
            print("%s: %s"%(level,msg))
        if(self.toFile):
            self.loggers[level].info(msg)

class FileLogger(Logger):
    def __init__(self,toConsole=False,toFile=True,logDir='./log',activeLevels=DEFAULT_LOG_LEVELS):
        super().__init__(activeLevels)
        self.toConsole = toConsole
        self.toFile = toFile
        self.logDir = logDir
        
        self.loggers = {}
        
        if(self.toFile):
            #make sure the
            if(not os.path.isdir(self.logDir)):
                os.makedirs(self.logDir)
            #create native python loggers for each level
            for level in self.activeLevels:
                #init error logger
                logger = logging.getLogger(level)
                logFile = os.path.join(self.logDir,"%s.log"%(level))
                fh = logging.FileHandler(logFile,'w')
                fh.setLevel(logging.INFO)
                formatter = logging.Formatter('%(asctime)s - %(message)s')
                fh.setFormatter(formatter)
                logger.addHandler(fh)
                logger.setLevel(logging.INFO)
                self.loggers[level] = logger
                
    #@Override
    def ShallLog(self):
        return (self.toConsole or self.toFile)
                
    #@Override         
    def _Log(self,level,msg):
        if(self.toConsole):
            print("%s: %s"%(level,msg))
        if(self.toFile):
            self.loggers[level].info(msg)

