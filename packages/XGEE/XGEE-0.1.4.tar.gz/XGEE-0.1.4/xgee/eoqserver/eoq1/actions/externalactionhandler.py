#check for all actions in folder

from .. import CommandParser,ResultParser,ValueParser
from ..model import *
from ..error import EoqActionError
from ..domains import LocalDomain
from ..domains import MultiprocessingQueueDomainHost
from ..domains import MultiprocessingQueueDomainClient
from . import ActionUtils

import sys
import os
import glob
import imp
import time
import traceback

import io
from contextlib import redirect_stdout
import datetime

from multiprocessing import Process
import threading
from .actionutils import ActionUtils
from ..domains import LocalDomain
from paramiko import channel
from sys import stderr

class WriteRedirector:
    def __init__(self,callId,channelName,domain,legacyWriteFcn=None,bufferTime=1.0):
        self.callId = callId
        self.domain = domain
        self.channelName = channelName
        self.legacyWriteFcn = legacyWriteFcn
        self.bufferTime = bufferTime
        
        self.lastWriteTime = time.perf_counter()
        self.buffer = b''

    def write(self,data, *args):
            currentWriteTime = time.perf_counter()
            try:
                if(self.legacyWriteFcn):
                    self.legacyWriteFcn(data)
                if(isinstance(data, str) and 0<len(data)):
                    data = data.encode('utf-8')
                    self.buffer+=data
                    if(currentWriteTime-self.lastWriteTime>self.bufferTime):
                        ActionUtils.OutputToChannel(self.callId,self.channelName,self.buffer,self.domain)
                        self.buffer = b''
                        self.lastWriteTime = currentWriteTime
            except:
                pass
    def flush(self):
            try:
                if(0<len(self.buffer)):
                    ActionUtils.OutputToChannel(self.callId,self.channelName,self.buffer,self.domain)
                    self.buffer = b''
            except:
                pass
        
    def getStdStreamCompatibleWriteRedirector(self):
        return (lambda data, *args: self.write(data, *args))


def AsyncCallProcessMain(actiondir,callId,actionName,argStr,cmdQueue,resQueue):
    #connect to domain
    domain = MultiprocessingQueueDomainClient(cmdQueue,resQueue)
    stdoutRedirector = WriteRedirector(callId,'STDOUT',domain,legacyWriteFcn=sys.stdout.write)
    stderrRedirector = WriteRedirector(callId,'STDERR',domain,legacyWriteFcn=sys.stderr.write)
    #redirect std outputs
    sys.stdout.write = stdoutRedirector.getStdStreamCompatibleWriteRedirector()  
    sys.stderr.write = stderrRedirector.getStdStreamCompatibleWriteRedirector()
    #load action function
    searchString = os.path.join(actiondir+'/*.py')
    pythonfiles = glob.glob(searchString)
    actionFunction = None
    for pythonfile in pythonfiles:
        pathname, filename = os.path.split(pythonfile)
        actionname = filename[:-3]; #without .py
        if(actionName == actionname):
            packagename = pathname.replace('/','.')
            modulename = packagename+'.'+actionname
            file, modulepath, description = imp.find_module(actionname, [pathname])
            actionmodule = imp.load_module(modulename, file, modulepath, description)
            actionFunction = getattr(actionmodule,actionname)
            break
    #convert input values
    if(actionFunction):
        args = ValueParser.StringToValue(argStr)
        pArguments = ValueParser.ValueToPython(args)
        ActionUtils.SetCallStatus(callId,CallStatusE.RUNNING,domain)
        pResult = actionFunction(domain,*pArguments)
        returnValues = ValueParser.PythonToValue(pResult)
        #make sure all output was printed to the domain
        stdoutRedirector.flush()
        stderrRedirector.flush()
        #finaly change the call status to FINISHED
        ActionUtils.SetCallStatus(callId,CallStatusE.FINISHED,domain)

#PRIVATE CLASS DEFINITIONS
class EoqExternalActionError(EoqActionError):
    def __init__(self, code, message):
        EoqActionError.__init__(self, code, "EXTERNALACTIONHANDLER: "+message)
        
class ActionInfo:
    def __init__(self,name,details,actionFunction,args,results,description):
        self.name = name
        self.details = details
        self.actionFunction = actionFunction
        self.args = args
        self.results = results
        self.description = description
        
class ArgumentInfo:
    def __init__(self,name,type,min,max,description,default,choices):
        self.name = name
        self.type = type
        self.min = min
        self.max = max
        self.description = description
        self.default = default
        self.choices = choices
        
class RunningAction:
    def __init__(self,actionCall,process,domainWrapper):
        self.actionCall = actionCall
        self.process = process
        self.domainWrapper = domainWrapper
        
class RunAsCurrentTransactionLocalDomainWrapper(LocalDomainA):
    def __init__(self,localdomain : LocalDomain, transaction : Transaction):
        self._domain = localdomain
        self.transaction = transaction
        
    def Do(self, command : CommandA) -> ResultA:
        historyOffset = len(self.transaction.history)
        self.__AdoptHistoryRefsCommand(command,historyOffset)
        result = self._domain.DoAsTransaction(command,self.transaction)
        return result
            
    def Call(self, name : str, args : ListValue, transaction : Transaction) -> CallResult:
        return LocalDomainA.Call(self, name, args, transaction)
    
    def __AdoptHistoryRefsCommand(self,command,offset):
        if(command.type == CommandTypesE.COMPOUND):
            for command in command.commands: 
                self.__AdoptHistoryRefsCommand(command,offset)
        elif(command.type == CommandTypesE.RETRIEVE):
            self.__AdoptHistoryRefsValue(command.target,offset)
        elif(command.type == CommandTypesE.UPDATE):
            self.__AdoptHistoryRefsValue(command.target,offset)
            self.__AdoptHistoryRefsValue(command.value,offset)
        elif(command.type == CommandTypesE.CALL):
            self.__AdoptHistoryRefsValue(command.args,offset)
        elif(command.type == CommandTypesE.ASYNCCALL):
            self.__AdoptHistoryRefsValue(command.args,offset)
        return command

    def __AdoptHistoryRefsValue(self,value,offset):
        if(value.type == ValueTypesE.LIST):
            for v in value.v:
                self.__AdoptHistoryRefsValue(v,offset)
        elif(value.type == ValueTypesE.HISTORYREF):
            value.v += offset
        return value
        
'''
    The external action handler
'''
class ExternalActionHandler(ActionHandlerA):
    
    def __init__(self,domain : LocalDomainA, basedir='actions'):
        self._domain = domain
        self._basedir = basedir
        self._actions = {}
        self._runningActions = {}
        #register default action for reloading action files        
        self.__ReloadActions(domain)
        return
    
    def __ScanForActions(self):
        #find all actions within files
        searchString = os.path.join(self._basedir+'/*.py')
        pythonfiles = glob.glob(searchString)
        sys.path.append(self._basedir) #add this to make libraries of actions accessible
        for pythonfile in pythonfiles:
            pathname, filename = os.path.split(pythonfile)
            actionname = filename[:-3]; #without .py
            packagename = pathname.replace('/','.')
            modulename = packagename+'.'+actionname
            try: #prevent server crash by broken action scripts
                file, modulepath, description = imp.find_module(actionname, [pathname])
                actionmodule = imp.load_module(modulename, file, modulepath, description)
                #check for a unique name
                if(actionname in self._actions):
                    print("WARNING: Found external action %s in file %s, but an action with the same name is already registered from file %s. Action names must be unique!"%(actionname,pythonfile,self._actions[actionname].filepath))
                    continue
                #check if the module contains a function with the same name
                if(actionname not in dir(actionmodule)):
                    print("WARNING: Found no function called %s in %s. This action can not be used."%(actionname,pythonfile))
                    continue
                print("INFO: Found external action %s in file %s"%(actionname,pythonfile))
                #register the new action 
                
                actionFunction = getattr(actionmodule,actionname)
                actionArguments = self.__ParseActionArguments(actionname,actionFunction)
                actionResults = self.__ParseActionResults(actionname,actionFunction)
                actionDescription = actionmodule.__doc__
                self._actions[actionname] = ActionInfo(actionname,pythonfile,actionFunction,actionArguments,actionResults,actionDescription)
            except Exception as e:
                print("Error loading external action '%s':"%(pythonfile))
                traceback.print_exc(file=sys.stdout)
            
    def __ParseActionArguments(self,actionName,actionFunction):
            args = []
            nArguments = actionFunction.__code__.co_argcount
            functionVariables = actionFunction.__code__.co_varnames
            actionArguments = functionVariables[0:nArguments]
            actionArgumentTypeInfos = actionFunction.__annotations__
            
            if(nArguments==0):
                print('WARNING: Action %s has no argument. Actions must have at least one argument of type EoqDomainA.'%(actionName))
            else:
                #look for the first argument. This must always be a domain
                argumentName = actionArguments[0]
                argument = None
                if(argumentName not in actionArgumentTypeInfos):
                    print('WARNING: Argument 1 of action %s is not annotated assuming EoqDomainA as type.'%(actionName))
                else:
                    argumentAnnotation = actionArgumentTypeInfos[argumentName]
                    if(DomainA.__name__!=argumentAnnotation):
                        print('WARNING: Argument 1 of action %s has type %s but expected is %s. This will probably not work.'%(actionName,argumentAnnotation,DomainA.__name__))
                #add all args after the first 
                for i in range(1,nArguments):
                    argumentName = actionArguments[i]
                    argument = None
                    if(argumentName not in actionArgumentTypeInfos):
                        print('WARNING: Argument %s of action %s has no annotation. Assuming * as type'%(argumentName,actionName))
                        argument = ArgumentInfo(argumentName,'*',1,1,'','',[])
                    else:
                        argumentAnnotation = actionArgumentTypeInfos[argumentName]
                        [argumentType, argumentMin, argumentMax, description, default, choices] = self.__ParseArgumentAnnotation(argumentAnnotation)
                        argument = ArgumentInfo(argumentName,argumentType, argumentMin, argumentMax, description, default, choices)
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
                print('WARNING: Action %s has no return annotation. Assuming no return value'%(actionName))
            else:
                argumentAnnotation = actionArgumentTypeInfos[argumentName]
                if('' != argumentAnnotation):
                    [argumentType, argumentMin, argumentMax, description, default, choices] = self.__ParseArgumentAnnotation(argumentAnnotation)
                    args.append(ArgumentInfo(argumentName,argumentType, argumentMin, argumentMax, description, default, choices))
            return args
        
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
        multiplicityStart = argumentAnnotation.find('[')
        choiceStart = argumentAnnotation.find('{')
        defaultStart = argumentAnnotation.find('=')
        descriptionStart = argumentAnnotation.find(':')
        
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
                print('WARNING: Malformed multiplicity in argument annotation %s'%(argumentAnnotation))

        #choice
        if(choiceStart > 0):
            choiceEnd = choiceStart+argumentAnnotation[choiceStart:].find('}')
            if(choiceEnd>0 and choiceEnd-1>choiceStart+1): #skip { and }
                choiceStr = argumentAnnotation[choiceStart+1:choiceEnd]
                choices = choiceStr.split(',')
            else:
                print('WARNING: Malformed choice in argument annotation %s'%(argumentAnnotation))
        #default
        if(defaultStart > 0):
            defaultEnd = min([nArgumentAnnotation,
                              descriptionStart%nArgumentAnnotation])
            if(defaultEnd>0 and defaultEnd-1>defaultStart+1):
                default = argumentAnnotation[defaultStart+1:defaultEnd] #skip :' and '
            else:
                print('WARNING: Malformed default in argument annotation %s'%(argumentAnnotation))

        #description
        if(descriptionStart > 0):
            descriptionEnd = nArgumentAnnotation 
            if(descriptionEnd>0 and descriptionEnd>descriptionStart+1): #skip :
                description = argumentAnnotation[descriptionStart+1:descriptionEnd] #skip :
            else:
                print('WARNING: Malformed description in argument annotation %s'%(argumentAnnotation))


        #type
        typeStart = 0
        typeEnd = min([nArgumentAnnotation,
                       multiplicityStart%nArgumentAnnotation,
                       choiceStart%nArgumentAnnotation,
                       defaultStart%nArgumentAnnotation,
                       descriptionStart%nArgumentAnnotation])
        argumentType = argumentAnnotation[typeStart:typeEnd]                 
        return [argumentType, argumentMin, argumentMax, description, default, choices] 
        
        
    def __AddActionToDomain(self,action,domain):
        actionDescriptor = None
        #check if an action with that name already exists
        command = CommandParser.RetrieveCommandStr(ObjectRefValue(v=0),"/actions{name='%s'}"%(action.name))
        result = domain.Do(command)
        if(ResultParser.IsResultNok(result)):
            raise EoqExternalActionError(1,'Could not read actions from domain')
        if(result.value.type == ValueTypesE.LIST and len(result.value.v) == 1 and result.value.v[0].type == ValueTypesE.OBJECTREF):
            actionDescriptor = result.value.v[0]
            
        #update or add an action
        if(actionDescriptor):
            command = CompoundCommand()
            command.commands.add(self.__ActionUpdateCommand(action,actionDescriptor))                   
            domain.Do(command)
        else:
            command = CompoundCommand()
            command.commands.add(CommandParser.CreateCommand('http://www.eoq.de/model/v1.0', 'ActionInfo',1))
            command.commands.add(self.__ActionUpdateCommand(action,HistoryRefValue(v=0)))        
            command.commands.add(CommandParser.UpdateCommandStr(ObjectRefValue(v=0), '/actions[+]', HistoryRefValue(v=0)))                          
            result = domain.Do(command)
            if(ResultParser.IsResultNok(result)):
                raise EoqExternalActionError(2,'Could not add action %s to domain because: %s(%d)%s'%(action.name,result.type,result.code,result.message))
            actionDescriptor = result.results[0].value
        parameterDescriptors = []
        for parameter in action.args:
            parameterDescriptors.append(self.__AddParameterToAction(actionDescriptor, parameter, 'parameters',domain))
        #delete existing parameters
        command = CommandParser.RetrieveCommandStr(actionDescriptor,"/parameters")
        result = domain.Do(command)
        actualParameters = result.value
        for actualParameter in actualParameters.v:
            if(actualParameter.v not in [x.v for x in parameterDescriptors]):
                command = CommandParser.UpdateCommandStr(actionDescriptor, '/parameters[-]', actualParameter)                          
                result = domain.Do(command)
        
        actionDescriptors = []
        for parameter in action.results:
            actionDescriptors.append(self.__AddParameterToAction(actionDescriptor, parameter, 'results',domain))
            
        #delete existing results
        command = CommandParser.RetrieveCommandStr(actionDescriptor,"/results")
        result = domain.Do(command)
        actualParameters = result.value
        for actualParameter in actualParameters.v:
            if(actualParameter.v not in [x.v for x in actionDescriptors]):
                command = CommandParser.UpdateCommandStr(actionDescriptor, '/results[-]', actualParameter)                          
                result = domain.Do(command)
                
        return actionDescriptor
    
    def __AddParameterToAction(self,actionDescriptor,parameter,target,domain):
        parameterDescriptor = None
        #check if an parameter with that name already exists
        command = CommandParser.RetrieveCommandStr(actionDescriptor,"/%s{name='%s'}"%(target,parameter.name))
        result = domain.Do(command)
        if(ResultParser.IsResultNok(result)):
            raise EoqExternalActionError(1,'Could not read %s for action'%(target))
        if(result.value.type == ValueTypesE.LIST and len(result.value.v) == 1 and result.value.v[0].type == ValueTypesE.OBJECTREF):
            parameterDescriptor = result.value.v[0]
        if(parameterDescriptor):
            command = CompoundCommand()
            command.commands.add(self.__ActionParameterUpdateCommand(parameter,parameterDescriptor))                   
            domain.Do(command)
        else:
            command = CompoundCommand()
            command.commands.add(CommandParser.CreateCommand('http://www.eoq.de/model/v1.0', 'ActionParameter',1))
            command.commands.add(self.__ActionParameterUpdateCommand(parameter,HistoryRefValue(v=0))) 
            command.commands.add(CommandParser.UpdateCommandStr(actionDescriptor, '/%s[+]'%(target), HistoryRefValue(v=0)))                          
            result = domain.Do(command)
            if(ResultParser.IsResultNok(result)):
                raise EoqExternalActionError(2,'Could not add %s %s to domain because: %s(%d)%s'%(target,parameterDescriptor.name,result.type,result.code,result.message))
            parameterDescriptor = result.results[0].value
        choiceDescriptors = []
        for choice in parameter.choices:
            choiceDescriptors.append(self.__AddChoiceToParameter(parameterDescriptor, choice,domain))
        #delete existing ones
        command = CommandParser.RetrieveCommandStr(parameterDescriptor,"/choices")
        result = domain.Do(command)
        actualChoices = result.value
        for actualChoice in actualChoices.v:
            if(actualChoice.v not in [x.v for x in choiceDescriptors]):
                command = CommandParser.UpdateCommandStr(parameterDescriptor, '/choices[-]', actualChoice)                          
                result = domain.Do(command)
                
        return parameterDescriptor
    
    def __AddChoiceToParameter(self,parameterDescriptor,choice,domain):
        choiceDescriptor = None
        #check if an parameter with that name already exists
        command = CommandParser.RetrieveCommandStr(parameterDescriptor,"/choices{value='%s'}"%(choice))
        result = domain.Do(command)
        if(ResultParser.IsResultNok(result)):
            raise EoqExternalActionError(1,'Could not read parameters for action')
        if(result.value.type == ValueTypesE.LIST and len(result.value.v) == 1 and result.value.v[0].type == ValueTypesE.OBJECTREF):
            choiceDescriptor = result.value.v[0]
        if(choiceDescriptor):
            pass
        else:
            command = CompoundCommand()
            command.commands.add(CommandParser.CreateCommand('http://www.eoq.de/model/v1.0', 'Choice',1))
            command.commands.add(CommandParser.UpdateCommandStr(HistoryRefValue(v=0), '/value', StringValue(v=choice))) 
            command.commands.add(CommandParser.UpdateCommandStr(parameterDescriptor, '/choices[+]', HistoryRefValue(v=0)))                         
            result = domain.Do(command)
            if(ResultParser.IsResultNok(result)):
                raise EoqExternalActionError(2,'Could not add choice %s to parameter because: %s(%d)%s'%(choice,result.type,result.code,result.message))
            choiceDescriptor = result.results[0].value
        return choiceDescriptor
    
    def __ActionUpdateCommand(self,action,actionDescriptor):
        command = CompoundCommand()
        command.commands.add(CommandParser.UpdateCommandStr(actionDescriptor, '/name', StringValue(v=action.name)))
        command.commands.add(CommandParser.UpdateCommandStr(actionDescriptor, '/details', StringValue(v=action.details)))
        command.commands.add(CommandParser.UpdateCommandStr(actionDescriptor, '/description', StringValue(v=action.description)))
        command.commands.add(CommandParser.UpdateCommandStr(actionDescriptor, '/handler', ObjectValue(v=self)))
        return command
    
    def __ActionParameterUpdateCommand(self,parameter,parameterDescriptor):
        command = CompoundCommand()
        command.commands.add(CommandParser.UpdateCommandStr(parameterDescriptor, '/name', StringValue(v=parameter.name)))
        command.commands.add(CommandParser.UpdateCommandStr(parameterDescriptor, '/type', StringValue(v=parameter.type)))
        command.commands.add(CommandParser.UpdateCommandStr(parameterDescriptor, '/lowerBound', IntValue(v=parameter.min)))
        command.commands.add(CommandParser.UpdateCommandStr(parameterDescriptor, '/upperBound', IntValue(v=parameter.max)))
        command.commands.add(CommandParser.UpdateCommandStr(parameterDescriptor, '/default', StringValue(v=parameter.default)))
        command.commands.add(CommandParser.UpdateCommandStr(parameterDescriptor, '/description', StringValue(v=parameter.description)))
        return command
    
    def __RemoveActionFromDomain(self,actionname,domain):
        actionDescriptor = self._actions[actionname]

        #update or add an action
        command = CommandParser.UpdateCommandStr(ObjectRefValue(v=0), '/actions[-]', actionDescriptor)                       
        result = domain.Do(command)
        if(ResultParser.IsResultNok(result)):
            raise EoqExternalActionError(3,'Could not remove action %s from domain because: %s(%d)%s'%(actionname,result.type,result.code,result.message))
        return
    
    def __ReloadActions(self,domain):
        #empty the list of actions
        currentlyRegisteredActions = dict(self._actions) #make a copy to delete them later
        self._actions.clear()
        #add an internal action to reload all actions
        actionname = 'reload-actions'
        actionFunction = lambda d: self.__ReloadActions(d)
        self._actions[actionname] = ActionInfo(actionname,'',actionFunction,[],[],'Reloads the action files and their descriptions from the file system')
        
        self.__ScanForActions()
        #register actions in the model
        for newActionname in self._actions:
            action = self._actions[newActionname]
            actionObject = self.__AddActionToDomain(action,domain)
                     
        #delete non existing actions from the model
        for oldActionname in currentlyRegisteredActions:
            if(oldActionname not in self._actions):
                self.__RemoveActionFromDomain(oldActionname,domain)
        return
        
    def Call(self, actionCall : ActionCall, transaction : Transaction):
        if(actionCall.action not in self._actions):
            raise EoqExternalActionError(1,'Action with name %s is unknown.'%(actionCall.action))
        action = self._actions[actionCall.action]
        #print("Called external action %s(%s)"%(name,ValueParser.ValueToString(args)))
        domain = RunAsCurrentTransactionLocalDomainWrapper(self._domain,transaction)
        pArguments = ValueParser.ValueToPython(actionCall.args)
        
        stdoutOutput = io.StringIO()
        ActionFunction = action.actionFunction
        with redirect_stdout(stdoutOutput):
            ActionUtils.SetCallStatus(actionCall.callId,CallStatusE.RUNNING,domain)
            pResult = ActionFunction(domain,*pArguments)
        returnValues = ValueParser.PythonToValue(pResult)
        if(stdoutOutput.getvalue()):
            ActionUtils.OutputToChannel(actionCall.callId,'STDOUT',stdoutOutput.getvalue(),domain)
        actionCall.returnValues = returnValues
        ActionUtils.SetCallStatus(actionCall.callId,CallStatusE.FINISHED,domain)
        return 
    
    def AsyncCall(self, actionCall : ActionCall, transaction : Transaction):
        if(actionCall.action not in self._actions):
            raise EoqExternalActionError(1,'Action with name %s is unknown.'%(actionCall.action))
        observerThread = threading.Thread(target=self.__AsyncCallObserverThread, args=(actionCall,))
        observerThread.start()
        return 
    
    def CallStatus(self, actionCall : ActionCall, transaction : Transaction):
        raise EoqExternalActionError(45,'CallStatus: Not implemented for ExternalActionHandler.')

    def AbortCall(self, actionCall : ActionCall, transaction : Transaction):
        if(actionCall.callId not in self._runningActions):
            raise EoqExternalActionError(46,'ExternalActionHandler: CallId %d is unknown'%(actionCall.callId))
        #remove from the list of running processes
        runningAction = self._runningActions.pop(actionCall.callId)
        #kill the process
        runningAction.process.terminate() 
        #set an aborted status
        domain = RunAsCurrentTransactionLocalDomainWrapper(self._domain,transaction)
        ActionUtils.SetCallStatus(actionCall.callId,CallStatusE.ABORTED,domain)
        return
    
    def __AsyncCallObserverThread(self,actionCall : ActionCall):
        argsStr = ValueParser.ValueToString(actionCall.args)
        domainWrapper = MultiprocessingQueueDomainHost(self._domain)
        proc = Process(target=AsyncCallProcessMain, args=(self._basedir,actionCall.callId,actionCall.action,argsStr,domainWrapper.cmdQueue,domainWrapper.resQueue))
        runningAction = RunningAction(actionCall,proc,domainWrapper)
        self._runningActions[actionCall.callId] = runningAction
        
        domainWrapper.Start()
        proc.start()
        
        while(proc.is_alive()): #wait until the thread has finished
            time.sleep(0.1)
        domainWrapper.Join()