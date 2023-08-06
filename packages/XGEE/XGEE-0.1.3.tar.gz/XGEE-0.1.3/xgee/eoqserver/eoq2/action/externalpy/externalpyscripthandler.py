'''
 2019 Bjoern Annighoefer
'''

#check for all actions in folder


from ..action import Action,ActionArg,ActionArgOption
from ..call import CallStatus,CallOptions
from ..callhandler import CallHandler
from ...serialization import JsonSerializer
from ...domain.multiprocessing import MultiprocessingQueueDomainClient,MultiprocessingQueueDomainHost
from ...command.command import Abc
from ...util import EoqError,NoLogging,DATE_TIME_STR_FORMAT

import sys
import os
import imp
import time
import traceback
from datetime import datetime

from multiprocessing import Process
import threading

from timeit import default_timer as timer 


class SyncWriteRedirector:
    def __init__(self,stream,callId,channelName,callManager,silent=False,eventsonly=False,bufferTime=0.0):
        self.stream = stream
        self.callId = callId
        self.callManager = callManager
        self.channelName = channelName
        self.silent = silent
        self.eventsonly = eventsonly
        self.bufferTime = bufferTime
        
        self.lastWriteTime = time.perf_counter()
        self.buffer = ''
        
    def Redirect(self):
        self.legacyWriteFcn = self.stream.write
        self.stream.write = self.write

    def Restore(self):
        self.flush()
        self.stream.write = self.legacyWriteFcn
     
    # with handlers   
    def __enter__(self):
        self.Redirect()
        
    def __exit__(self,exc_type,exc_val,exc_tb):
        self.Restore()
         
    # overwrite stream functions        
    def write(self,data,*args):
            currentWriteTime = time.perf_counter()
            try:
                if(self.legacyWriteFcn and not self.silent and not self.eventsonly):
                    self.legacyWriteFcn(data)
                if(isinstance(data, str) and 0<len(data) and not self.silent):
                    #data = data.encode('utf-8')
                    self.buffer+=data
                    if(currentWriteTime-self.lastWriteTime>self.bufferTime):
                        self.callManager.AddCallOutputRaw(self.callId,self.channelName,self.buffer)
                        self.buffer = ''
                        self.lastWriteTime = currentWriteTime
            except Exception as e:
                sys.stderr.write(str(e))
    def flush(self):
            try:
                if(0<len(self.buffer) and not self.silent):
                    self.callManager.AddCallOutputRaw(self.callId,self.channelName,self.buffer)
                    self.buffer = ''
            except:
                pass
        
# 
# class WriteRedirector:
#     def __init__(self,callId,channelName,callManager,legacyWriteFcn=None,bufferTime=0.0):
#         self.callId = callId
#         self.callManager = callManager
#         self.channelName = channelName
#         self.legacyWriteFcn = legacyWriteFcn
#         self.bufferTime = bufferTime
#         
#         self.lastWriteTime = time.perf_counter()
#         self.buffer = ''
# 
#     def write(self,data, *args):
#             currentWriteTime = time.perf_counter()
#             try:
#                 if(self.legacyWriteFcn):
#                     self.legacyWriteFcn(data)
#                 if(isinstance(data, str) and 0<len(data)):
#                     #data = data.encode('utf-8')
#                     self.buffer+=data
#                     if(currentWriteTime-self.lastWriteTime>self.bufferTime):
#                         self.callManager.AddCallOutput(self.callId,self.channelName,self.buffer)
#                         self.buffer = ''
#                         self.lastWriteTime = currentWriteTime
#             except Exception as e:
#                 print(str(e))
#     def flush(self):
#             try:
#                 if(0<len(self.buffer)):
#                     self.callManager.AddCallOutput(self.callId,self.channelName,self.buffer)
#                     self.buffer = ''
#             except:
#                 pass
#         
#     def getStdStreamCompatibleWriteRedirector(self):
#         return (lambda data, *args: self.write(data, *args))

def AsyncCallProcessMain(actiondir,actionname,callId,argStr,optsStr,cmdQueue,resQueue,evtQueue):
    serializer = JsonSerializer()
    #restore args
    args = serializer.Des(argStr)
    #restore opts
    opts = CallOptions()
    opts.FromArray(serializer.Des(optsStr))
    #connect to domain
    domain = MultiprocessingQueueDomainClient(cmdQueue,resQueue,evtQueue,callId)
    stdoutRedirector = SyncWriteRedirector(sys.stdout,callId,'STDOUT',domain.callManager,silent=opts.silent,eventsonly=opts.eventsonly)
    stdoutRedirector.Redirect()
    relpathname = actionname+".py"
    pythonfile = os.path.join(actiondir,relpathname)
    pathname, filename = os.path.split(pythonfile)
    actionfunctionname = filename[:-3]
    modulename = actionname
    file, modulepath, description = imp.find_module(actionfunctionname, [pathname])
    sys.path.append(pathname)
    actionmodule = imp.load_module(modulename, file, modulepath, description)
    actionFunction = getattr(actionmodule,actionfunctionname)
    #convert input values
    if(actionFunction):
        stime = timer()
        callStatusInfo = "Python action %s started %s "%(relpathname,datetime.now().strftime(DATE_TIME_STR_FORMAT)) #is extended later
        domain.callManager.ChangeCallStatus(callId,CallStatus.RUN,callStatusInfo)
        finalCallStatus = CallStatus.RUN #is changed later
        try:
            value = actionFunction(domain,*args)
            domain.callManager.SetCallValue(callId, value)
            etime = timer()
            finalCallStatus = CallStatus.FIN
            callStatusInfo += " and ended %s (elapsed time: %f s) "%(datetime.now().strftime(DATE_TIME_STR_FORMAT),etime-stime)
        except Exception as e:
            traceback.print_exc()#
            etime = timer()
            finalCallStatus = CallStatus.ERR
            callStatusInfo += " and failed %s (elapsed time: %f s): %s"%(datetime.now().strftime(DATE_TIME_STR_FORMAT),etime-stime,str(e))
        #make sure all output was printed to the domain
        stdoutRedirector.flush()
        stdoutRedirector.Restore()
        #finally change the call status to FINISHED
        domain.callManager.ChangeCallStatus(callId,finalCallStatus,callStatusInfo)
    domain.Stop() #stop the event listener thread of the domain
    
            
        
class RunningAction:
    #def __init__(self,actionCall,process,domainWrapper):
    def __init__(self,callId):
        self.started = False
        self.aborted = False
        self.callId = callId
        self.process = None
        self.domainWrapper = None
        
    def SetStarted(self,process,domainWrapper):
        self.started = True
        self.process = process
        self.domainWrapper = domainWrapper
        
    def HasStarted(self):
        return self.started;
    
    def IsAborted(self):
        return self.aborted;
    
    def Abort(self):
        self.aborted = True;
        
'''
    The external action handler
'''
class ExternalPyScriptHandler(CallHandler):
    
    def __init__(self,callManager,basedir='actions',logger=NoLogging()):
        #constants
        self.ANNOTATION_ESCAPE_SYMBOLS = [r'\:',r'\[',r'\]',r'\{',r'\}',r"\'",r'\"',r'\\']
        #parameters
        self.callManager = callManager
        self._basedir = basedir
        self.logger = logger
        
        self._actions = {} #name -> (action,handlerfunction)
        self._runningActions = {}
        #register default action for reloading action files        
        self.__ReloadActions()
        return
    
    def __ScanForActions(self):
    
        #find all python files in the action directory
        pythonfiles = []
        for root, dirs, files in os.walk(self._basedir, topdown=True):
            for file in files:
                if(file.endswith('.%s'%('py'))):
                    #relativeRoot = os.path.relpath(root, self._basedir)
                    #pythonfiles += [os.path.join(relativeRoot,file)] #2: omits the ./ at the beginning
                    pythonfiles += [os.path.join(root,file)] #2: omits the ./ at the beginning
        
        
        for pythonfile in pythonfiles:
            pathname, filename = os.path.split(pythonfile)
            if(os.path.isfile(os.path.join(pathname,'__init__.py'))):
                continue #skip any submodules from beeing loaded as an action
            actionfunctionname = filename[:-3] #without .py
            relpathname = os.path.relpath(pathname, self._basedir)
            modulename = None
            if(relpathname=="."): #it is the root folder
                modulename = actionfunctionname
            else: #any subfolder
                prefixfreepath = relpathname.replace('./','')
                packagename = prefixfreepath.replace('/','.')
                modulename = packagename+'.'+actionfunctionname
            actionname = modulename.replace('.','/')
            try: #prevent server crash by broken action scripts
                file, modulepath, description = imp.find_module(actionfunctionname, [pathname])
                sys.path.append(pathname)
                actionmodule = imp.load_module(modulename, file, modulepath, description)
                #check for a unique name
                if(actionfunctionname in self._actions):
                    self.logger.Warn("Found external action %s in file %s, but an action with the same name is already registered from file %s. Action names must be unique!"%(actionname,pythonfile,self._actions[actionname].filepath))
                    continue
                #check if the module contains a function with the same name
                if(actionfunctionname not in dir(actionmodule)):
                    self.logger.Warn("Skipped no-action %s in %s."%(actionname,pythonfile))
                    continue
                self.logger.Info("Found external action %s in file %s"%(actionname,pythonfile))
                #register the new action 
                
                actionFunction = getattr(actionmodule,actionfunctionname)
                actionArguments = self.__ParseActionArguments(actionname,actionFunction)
                actionResults = self.__ParseActionResults(actionname,actionFunction)
                actionDescription = actionmodule.__doc__
                actionTags = getattr(actionmodule, '__tags__', [])
                if actionTags:
                    self.logger.Info("Action has tags: %s"%(actionTags))
                actionCategory = ""
                action = Action(actionname,actionArguments,actionResults,actionDescription,actionCategory,actionTags)

                self._actions[actionname] = (action,actionFunction)
                #Action(actionname,pythonfile,actionFunction,actionArguments,actionResults,actionDescription)
            except Exception as e:
                self.logger.Error("Error loading external action %s from %s: %s"%(actionname,pythonfile,str(e)))
                traceback.print_exc(file=sys.stdout)
            
    def __ParseActionArguments(self,actionName,actionFunction):
        args = []
        nArguments = actionFunction.__code__.co_argcount
        functionVariables = actionFunction.__code__.co_varnames
        actionArguments = functionVariables[0:nArguments]
        actionArgumentTypeInfos = actionFunction.__annotations__
        
        if(nArguments==0):
            self.logger.Warn("Action %s has no argument. Actions must have at least one argument of type Domain."%(actionName))
        else:
            #look for the first argument. This must always be a domain
            argumentName = actionArguments[0]
            argument = None
            if(argumentName not in actionArgumentTypeInfos):
                self.logger.Warn("Argument 1 of action %s is not annotated assuming Domain as type."%(actionName))
            else:
                argumentAnnotation = actionArgumentTypeInfos[argumentName]
                if("Domain"!=argumentAnnotation):
                    self.logger.Warn("Argument 1 of action %s has type %s but expected is %s. This will probably not work."%(actionName,argumentAnnotation,"Domain"))
            #add all args after the first 
            for i in range(1,nArguments):
                argumentName = actionArguments[i]
                argument = None
                if(argumentName not in actionArgumentTypeInfos):
                    self.logger.Warn("Argument %s of action %s has no annotation. Assuming * as type"%(argumentName,actionName))
                    argument = ActionArg(argumentName,'*',1,1,'','',[])
                else:
                    argumentAnnotation = actionArgumentTypeInfos[argumentName]
                    [argumentType, argumentMin, argumentMax, description, default, choices] = self.__ParseArgumentAnnotation(argumentAnnotation)
                    argument = ActionArg(argumentName,argumentType, argumentMin, argumentMax, description, default, choices)
                args.append(argument)
        return args
        
    def __ParseActionResults(self,actionName,actionFunction):
        args = []
        nArguments = actionFunction.__code__.co_argcount
        functionVariables = actionFunction.__code__.co_varnames
        actionArguments = functionVariables[0:nArguments]
        actionArgumentTypeInfos = actionFunction.__annotations__
        
        argumentName = 'return' #'return' is the default key for return annotations in python
        argument = None
        if(argumentName not in actionArgumentTypeInfos):
            self.logger.Warn("Action %s has no return annotation. Assuming no return value"%(actionName))
        else:
            argumentAnnotation = actionArgumentTypeInfos[argumentName]
            if('' != argumentAnnotation):
                [argumentType, argumentMin, argumentMax, description, default, choices] = self.__ParseArgumentAnnotation(argumentAnnotation)
                args.append(ActionArg(argumentName,argumentType, argumentMin, argumentMax, description, default, choices))
        return args
    
    def __MaskEscapeArgumentAnnotation(self,annotation):
        maskedAnnotation = annotation
        for s in self.ANNOTATION_ESCAPE_SYMBOLS:
            maskedAnnotation = maskedAnnotation.replace(s,'x')
        return maskedAnnotation
        
    def __UnescapeArgumentAnnotation(self,annotation):
        
        maskedAnnotation = annotation
        for s in self.ANNOTATION_ESCAPE_SYMBOLS:
            maskedAnnotation = maskedAnnotation.replace(s,s[1])
        return maskedAnnotation
        
        
    def __ParseArgumentAnnotation(self,argumentAnnotation):
        #a annotation should look like this: <Type>[<multiplicity=0..1|*>]{<choice1>',<choice2>,...}=<default>:<Description>
        #all parameters except type are optional
        argumentType = ''
        argumentMin = 1
        argumentMax = 1
        description = ''
        default = ''
        choices = []
        
        #parse string
        nArgumentAnnotation = len(argumentAnnotation)+1
        maskedAnnotation = self.__MaskEscapeArgumentAnnotation(argumentAnnotation) #neglect all escaped symbols
        multiplicityStart = maskedAnnotation.find('[')
        choiceStart = maskedAnnotation.find('{')
        defaultStart = maskedAnnotation.find('=')
        descriptionStart = maskedAnnotation.find(':')
        # remove all escape sequences
        argumentAnnotation = self.__UnescapeArgumentAnnotation(argumentAnnotation)
        
        #multiplicity
        if(multiplicityStart > 0):
            multiplicityEnd = multiplicityStart+argumentAnnotation[multiplicityStart:].find(']')
            if(multiplicityEnd>0 and multiplicityEnd>multiplicityStart):
                multiplicityStr = argumentAnnotation[multiplicityStart+1:multiplicityEnd]
                if('..' in multiplicityStr):
                    multiplicity = multiplicityStr.split('..')
                    if(len(multiplicity)==2):
                        argumentMin = int(multiplicity[0])
                        if('*' == multiplicity[1]):
                            argumentMax = -1
                        else:
                            argumentMax = int(multiplicity[1])
                else:
                    if('*' == multiplicityStr):
                        argumentMin = 0
                        argumentMax = -1
                    else:
                        argumentMin = int(multiplicityStr)
                        argumentMax = int(multiplicityStr)
            else:
                self.logger.Warn("Malformed multiplicity in argument annotation %s"%(argumentAnnotation))

        #choice
        if(choiceStart > 0):
            choiceEnd = choiceStart+argumentAnnotation[choiceStart:].find('}')
            if(choiceEnd>0 and choiceEnd>choiceStart+1): #skip { and }
                choiceStr = argumentAnnotation[choiceStart+1:choiceEnd]
                choices = [ActionArgOption(v,'') for v in choiceStr.split(',')]
            else:
                self.logger.Warn("Malformed choice in argument annotation %s"%(argumentAnnotation))
        #default
        if(defaultStart > 0):
            defaultEnd = min([nArgumentAnnotation,
                              descriptionStart%nArgumentAnnotation])
            if(defaultEnd>0 and defaultEnd>defaultStart+1):
                default = argumentAnnotation[defaultStart+1:defaultEnd] #skip :' and '
            else:
                self.logger.Warn("Malformed default in argument annotation %s"%(argumentAnnotation))

        #description
        if(descriptionStart > 0):
            descriptionEnd = nArgumentAnnotation 
            if(descriptionEnd>0 and descriptionEnd>descriptionStart+1): #skip :
                description = argumentAnnotation[descriptionStart+1:descriptionEnd] #skip :
            else:
                self.logger.Warn("Malformed description in argument annotation %s"%(argumentAnnotation))


        #type
        typeStart = 0
        typeEnd = min([nArgumentAnnotation,
                       multiplicityStart%nArgumentAnnotation,
                       choiceStart%nArgumentAnnotation,
                       defaultStart%nArgumentAnnotation,
                       descriptionStart%nArgumentAnnotation])
        argumentType = argumentAnnotation[typeStart:typeEnd]                 
        return [argumentType, argumentMin, argumentMax, description, default, choices] 
        
    
    def __ReloadActions(self):
        #empty the list of actions
        for key in self._actions:
            self.callManager.UnregisterAction(key)
        self._actions.clear()
            
#         #register actions
#         actionname = 'reload-actions'
#         actionFunction = lambda d: self.__ReloadActions(d)
#         self._actions[actionname] = (Action(actionname,'',[],[],'Reloads the action files and their descriptions from the file system'),actionFunction)
#         #scan for file based actions
        self.__ScanForActions()
        #register all actions
        for item in self._actions.items():
            name = item[0]
            action = item[1][0] #action is the first element of the touble (action,handler)
            self.callManager.RegisterAction(name,action,self)
        return
        
    def HandleSync(self,name,callId,domain,args,opts,callManager):
        if(opts.timeout>0.0):
            self.logger.Warn('timeout=%f is not supported for CAL'%(opts.timeout))
        
        if(name not in self._actions):
            raise EoqError(0,'Action with name %s is unknown.'%(name))
        (action,actionFunction) = self._actions[name]
        
        callStatusInfo = "Python action %s started %s"%(name,datetime.now().strftime(DATE_TIME_STR_FORMAT))
        callManager.ChangeCallStatus(callId,CallStatus.RUN,callStatusInfo)
        finalCallStatus = CallStatus.RUN #is changed later
        value = None
        with SyncWriteRedirector(sys.stdout,callId,'STDOUT',callManager,silent=opts.silent,eventsonly=opts.eventsonly,bufferTime=0.0):
            stime = timer()
            try:
                value = actionFunction(domain,*args)
                finalCallStatus = CallStatus.FIN
                etime = timer()
                callStatusInfo += " and ended %s (elapsed time: %f s)"%(datetime.now().strftime(DATE_TIME_STR_FORMAT),etime-stime)
            except Exception as e: 
                traceback.print_exc()
                finalCallStatus = CallStatus.ERR
                etime = timer()
                callStatusInfo += " and failed %s (elapsed time: %f s): %s"%(datetime.now().strftime(DATE_TIME_STR_FORMAT),etime-stime,str(e))
                raise e #make sure the exception goes to the call manager
        callManager.ChangeCallStatus(callId,finalCallStatus,callStatusInfo)
        return value
    
    def HandleAsync(self,name,callId,domain,args,opts,callManager,sessionId=None):
        # AsyncCall(self, actionCall : ActionCall, transaction : Transaction):
        if(name not in self._actions):
            raise EoqError(0,'Action with name %s is unknown.'%(name))
        
        runningAction = RunningAction(callId)
        self._runningActions[callId] = runningAction
        
        observerThread = threading.Thread(target=self.__AsyncCallObserverThread, args=(name,runningAction,domain,args,opts,callManager,sessionId,callId,))
        observerThread.start()
        return

    def AbortCall(self, callId):
        #(self, actionCall : ActionCall, transaction : Transaction):
        if(callId not in self._runningActions):
            raise EoqError(0,'ExternalActionHandler: CallId %d is unknown'%(callId))
        #remove from the list of running processes
        runningAction = self._runningActions.pop(callId)
        #set an aborted status
        runningAction.Abort()
        
        if(runningAction.HasStarted()):
            #kill the process
            runningAction.process.terminate() 
        return True
    
    def __AsyncCallObserverThread(self,name,runningAction,domain,args,opts,callManager,sessionId,callId):
        #runningAction = self._runningActions[callId]
        serializer = JsonSerializer()
        argsStr = serializer.Ser(args)
        optsStr = serializer.Ser(opts.ToArray())
        hasTimout = (opts.timeout > 0.0)
        wasAborted = False
        domainWrapper = MultiprocessingQueueDomainHost(domain,callManager,sessionId=sessionId,callId=callId)
        proc = Process(target=AsyncCallProcessMain, args=(self._basedir,name,runningAction.callId,argsStr,optsStr,domainWrapper.cmdQueue,domainWrapper.resQueue,domainWrapper.evtQueue,))
#         runningAction = RunningAction(callId,proc,domainWrapper)
#         self._runningActions[callId] = runningAction
        sTime = timer()
    
        if(not runningAction.IsAborted()): #check if the call was aborted before the process was created
            domainWrapper.Start()
            proc.start()
            runningAction.SetStarted(proc,domainWrapper)
          
            while(proc.is_alive()): #wait until the thread has finished
                time.sleep(0.1)
                if(hasTimout):
                    cTime = timer()
                    pTime = cTime-sTime
                    if(not wasAborted and pTime > opts.timeout): 
                        #abort the process if it took to long
                        self.logger.Warn('Timeout of %f s reached for call %d. Aborting.'%(opts.timeout,callId))
                        domain.Do(Abc(callId))
                        wasAborted = True
                
            domainWrapper.Join()