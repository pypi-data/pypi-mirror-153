from .. import ValueParser,QueryParser,CommandParser
from ..model import *
from ..error import EoqError,EoqRetrieveError,EoqCreateError,EoqUpdateError,EoqContextError,EoqTransactionError,EoqIdError,EoqGeneralError,EoqActionError

from pyecore.resources import Resource,ResourceSet,URI
from pyecore.ecore import EOrderedSet,EObject,EPackage,EEnumLiteral,EClass,EAttribute,EReference,EProxy,MetaEClass
import pyecore.behavior as behavior # We need to import the 'behavior' package

import types
import os
import time
import glob
import sys,traceback
from datetime import datetime
import shutil
import logging


import threading #make local domain threadsafe
from pyeoq.error.error import EoqValueError
from pip._vendor.colorama.ansi import Back
from pyeoq.resultparser import ResultParser

#Implement methods
@PathElementA.behavior
def actualPath(self):
	path = self.name
	parent = self.eContainer()
	while(isinstance(parent,Directory)):
		path = os.path.join(parent.name,path)
		parent = parent.eContainer()
	return path #2: omits the ./ at the beginning

@PathElementA.behavior
def actualPathAbs(self):
	path = self.name
	parent = self.eContainer()
	while(isinstance(parent,Directory)):
		path = os.path.join(parent.name,path)
		if(isinstance(parent, LocalDomainA)):
			path = os.path.join(parent.baseDirAbs,path)
		parent = parent.eContainer()
	return path #2: omits the ./ at the beginning

@PathElementA.behavior
def actualPathCwd(self):
	path = self.name
	parent = self.eContainer()
	while(isinstance(parent,Directory)):
		path = os.path.join(parent.name,path)
		if(isinstance(parent, LocalDomainA)):
			path = os.path.join(parent.baseDir,path)
		parent = parent.eContainer()
	return path #2: omits the ./ at the beginning
		

'''

'''

DEFAULT_TIMEOUT = 1.0

class LocalDomain(LocalDomainA):
	
	def __init__(self,baseDir,timeout=DEFAULT_TIMEOUT,metaDir=['./.meta'],enableBackup=True,logPath='./log',logLimit=10):
		self.baseDir = baseDir
		self.baseDirAbs = os.path.join(os.getcwd(),baseDir)
		self.baseDirUri = URI(baseDir) 
		self.resourceSet = ResourceSet()
		self.resourceObjectLUT = {} #a look-up table between eResources and ModelResource objects
		self.defaultTimeout = timeout
		self.metaDir = metaDir #the directory that contains model definitions
		#logging
		self.logPath = logPath
		self.logLimit = logLimit #the number of backups stored concurrently
		self.currentLogDir = None #is set later
		self.errorsLogger = None
		self.commandsLogger = None # is set later
		self.changesLogger = None # is set later
		#backup
		self.enableBackup = enableBackup
		self.currentBackupDir = None #is set later
		
		
		self.version = "v0.7"
		
		self.objectToIdLUT = {}
		self.idToObjectLUT = {}
		self.lastId = 0
		self.knownModelExtensions = ['ecore'] #this is used to identify the model files to be loaded. ecore files are known as model files by default.
		
		self.commandLUT = [
			self.__HelloCommand,
			self.__GoodbyeCommand,
			self.__SessionCommand,
			self.__StatusCommand,
			self.__ChangesCommand,
			self.__RetrieveCommand,
			self.__CreateCommand,
			self.__UpdateCommand,
			self.__CloneCommand,
			self.__UndoCommand,
			self.__CallCommand,
			self.__AsyncCallCommand,
			self.__CallStatusCommand,
			self.__AbortCallCommand,
			self.__CompoundCommand]
		
		#initialization
		self.id = self.__EncodeObjects(self)
		
		#initialize local EResource content method in order to support dynamic loading
		#EResource.python_class.isLoaded = lambda this: (this.uri in this.domain.resourceSet.resources)
		
		self.name = '.' #this is the root directories name
		
		self.__InitLogging()
		
		if(self.enableBackup):
			self.__Backup()
		
		self.__InitCommands()
		
		self.__LoadMetaModels()
		
		self.__LoadResourceTree()
				
		self.__InitActions()
		
		self.threadLock = threading.Lock()
		
					
	'''
	Must be called before any actions on the model
	default timeout is 1s
	'''	
		
	def Do(self,command : CommandA) -> ResultA:
		with self.threadLock: #if multiple threads enter, all but the first must wait here
			try:
				transaction = self.__BeginTransaction()
				result = self.DoAsTransaction(command,transaction)
			except Exception as e: #catch things going wrong in transaction closing and ending
				traceback.print_exc(file=sys.stdout)
				self.errorsLogger.error(e, exc_info=True)
				result = ErrorResult()
				result.commandType = command.type
				result.code = 9999
				result.message = '%s'%(str(e))
			finally:
				self.__EndTransaction(transaction)
		
		return result
	
	def DoAsTransaction(self,command : CommandA, transaction : int) -> ResultA:
		self.commandsLogger.info(CommandParser.CommandToString(command))
		result = self.__ExecuteCommand(command,transaction)
		self.commandsLogger.info(ResultParser.ResultToString(result))
		return result
	
	def Call(self,actionCall : ActionCall, transaction : Transaction) -> ListValue:
		#returnValues = ListValue()
		args = self.__ResolveHistory(actionCall.args, transaction)	
		if('load-resource' == actionCall.action):
			if(len(args.v)!=1 or args.v[0].type!=ValueTypesE.OBJECTREF):
				raise EoqActionError(10,'The number of args for action load-resource must be 1 and the type must be FileResource.')
			fileResource = self.__DecodeSingleObject(args.v[0])
			self.__LoadResource(fileResource,transaction)
			returnValues = self.__EncodeSingleObject(fileResource)
		elif('save-resource' == actionCall.action):
			if(len(args.v)!=1 or args.v[0].type!=ValueTypesE.OBJECTREF):
				raise EoqActionError(10,'The number of args for action save-resource must be 1 and the type must be FileResource.')
			fileResource = self.__DecodeSingleObject(args.v[0])
			self.__SaveResource(fileResource,transaction)
			returnValues = self.__EncodeSingleObject(fileResource)
		else:
			raise EoqActionError(99,'Action with name %s is unknown for the handler localDomain'%(actionCall.action))
		actionCall.returnValues = returnValues
		return

	def AsyncCall(self, actionCall : ActionCall, transaction : Transaction):
		raise EoqGeneralError(44,'AyncCall: LocalDomain does not support asynchronous actions.')

	def CallStatus(self, actionCall : ActionCall, transaction : Transaction):
		raise EoqGeneralError(45,'CallStatus: LocalDomain does not support asynchronous actions.')

	def AbortCall(self, actionCall : ActionCall, transaction : Transaction):
		raise EoqGeneralError(46,'AbortCall: LocalDomain does not support asynchronous actions.')
	
	#PRIVATE METHODS
		
	def __ExecuteCommand(self,command : CommandA, transaction : int):
		result = None
		#resolve any history already here?
		try:
			if(0 <= command.type.value and command.type.value < len(self.commandLUT)):
				result = self.commandLUT[command.type.value](command,transaction)
			else:
				raise EoqGeneralError(99,'Unknown command type: %d'%(command.type.value))

		#Error handling
		except EoqError as e:
			cmdStr = CommandParser.CommandToString(command)
			print('ERROR EXECUTING COMMAND:%s'%(cmdStr))
			traceback.print_exc(file=sys.stdout)
			self.errorsLogger.exception('ERROR EXECUTING COMMAND:%s'%(cmdStr))
			#self.errorsLogger.error(e, exc_info=True)
			result = ErrorResult()
			result.code = e.type + e.code
			result.message = '%s (in "%s")'%(e.message,cmdStr)
		except Exception as e:
			cmdStr = CommandParser.CommandToString(command)
			print('ERROR EXECUTING COMMAND:%s'%(cmdStr))
			traceback.print_exc(file=sys.stdout)
			self.errorsLogger.exception('ERROR EXECUTING COMMAND:%s'%(cmdStr))
			#self.errorsLogger.error(e, exc_info=True)
			result = ErrorResult()
			result.code = 9800
			result.message = '%s (in "%s")'%(str(e),cmdStr)
			
		result.commandType = command.type
		result.transactionId = transaction.id
		return result
	
	def __HelloCommand(self,command : HelloCommand,transaction : Transaction)->ResultA:
		result = HelloResult()
		#TODO: add return types
		return result
	
	def __GoodbyeCommand(self,command : GoodbyeCommand,transaction : Transaction)->ResultA:
		result = GoodbyeResult()
		return result
	
	def __SessionCommand(self,command : SessionCommand,transaction : Transaction)->ResultA:
		result = SessionResult()
		#TODO: add return types
		return result
	
	def __StatusCommand(self,command : StatusCommand,transaction : Transaction)->ResultA:
		result = StatusResult()
		#TODO: add return types
		return result
	
	def __ChangesCommand(self,command : ChangesCommand,transaction : Transaction)->ResultA:
		result = ChangesResult()
		earliestChangeId = self.__Resolve(command.earliestChangeId, IntValue, 'earliestChangeId', transaction).v
		requestedChanges = self.changes[earliestChangeId:]
		result.changes = ListValue()
		for requestedChange in requestedChanges:
			changeRecord = ListValue()
			changeRecord.v.add(IntValue(v=requestedChange.changeId))
			changeRecord.v.add(IntValue(v=requestedChange.sourceTransactionId))
			changeRecord.v.add(ValueParser.CloneValue(requestedChange.target))
			changeRecord.v.add(StringValue(v=QueryParser.QueryToString(requestedChange.query)))
			changeRecord.v.add(ValueParser.CloneValue(requestedChange.newValue))
			changeRecord.v.add(ValueParser.CloneValue(requestedChange.oldValue))
			result.changes.v.add(changeRecord)		
		return result
	
	def __RetrieveCommand(self,command : RetrieveCommand,transaction : Transaction)->ResultA:
		returnValue = self.__Retrieve(command.target, command.query,transaction)
		result = RetrieveResult()
		result.value = returnValue
		return result
	
	def __CreateCommand(self,command : CreateCommand,transaction : Transaction)->ResultA:
		
		packageNsUri = self.__Resolve(command.packageNsUri, StringValue, 'packageNsUri', transaction).v
		className = self.__Resolve(command.className, StringValue, 'className', transaction).v
		n = self.__Resolve(command.n, IntValue, 'n', transaction).v
		
		returnValue = self.__Create(packageNsUri, className, n,transaction)
		result = CreateResult()
		result.value = returnValue
		return result
	
	def __UpdateCommand(self,command : UpdateCommand,transaction : Transaction)->ResultA:
		returnValue = self.__Update(command.target, command.query, command.value, transaction)
		result = UpdateResult()
		result.target = returnValue
		return result
	
	def __CloneCommand(self,command : CloneCommand,transaction : Transaction)->ResultA:
		returnValue = self.__Clone(command.target, command.mode, transaction)
		result = CloneResult()
		result.value = returnValue
		return result
	
	def __UndoCommand(self,command,transaction : Transaction):
		pass
			
	def __CallCommand(self,command : CallCommand,transaction : Transaction)->ResultA:
		#initialize action call
		actionCall = self.__NewActionCall(command,transaction)
		self.actionCalls.add(actionCall)
		#execute action
		actionCall.handler.Call(actionCall,transaction)
		#build return value
		result = CallResult(callId=actionCall.callId,returnValues=actionCall.returnValues)
		return result
	
	def __AsyncCallCommand(self,command : AsyncCallCommand,transaction : Transaction)->ResultA:
		#initialize action call
		actionCall = self.__NewActionCall(command,transaction)
		#execute action
		actionCall.handler.AsyncCall(actionCall,transaction)
		#build return value
		result = AsyncCallResult(callId=actionCall.callId)
		return result
	
	def __CallStatusCommand(self,command : CallStatusCommand,transaction : Transaction)->ResultA:
		result = CallStatusResult()
		result.result = EmptyValue()
		#TODO: add return types
		return result
	
	def __AbortCallCommand(self,command : AbortCallCommand,transaction : Transaction)->ResultA:
		callId = self.__Resolve(command.callId, IntValue, 'callId', transaction).v
		if(callId<0 or len(self.actionCalls)<=callId):
			raise EoqGeneralError(23,'CallId %d is unknown'%(callId))
		actionCall = self.actionCalls[callId]
		actionCall.handler.AbortCall(actionCall,transaction)
		result = AbortCallResult()
		#TODO: add return types
		return result
	
	def __CompoundCommand(self,command : CompoundCommand,transaction : Transaction)->ResultA:
		result = CompoundResult()
		result.transactionId = transaction.id
		for subcommand in command.commands:
			subresult = self.__ExecuteCommand(subcommand,transaction)
			result.results.add(subresult)
			if(subresult.type == ResultTypesE.ERROR):
				result.type = ResultTypesE.COMPOUND_ERROR
				break #stop if one command fails
		return result
	
	def __NewActionCall(self,command,transaction : Transaction):
		action = self.__Resolve(command.action, StringValue, 'action', transaction).v
		actionHandler = self.__GetActionHandler(action)
		callId = self.callCount
		#resolve history arguments
		args = ValueParser.CloneValue(command.args)
		args = self.__ResolveHistory(args, transaction)	
		self.callCount +=1
		actionCall = ActionCall(callId=callId,action=action,args=args,handler=actionHandler)
		self.actionCalls.add(actionCall)
		return actionCall
		
	def __BeginTransaction(self,timeout=DEFAULT_TIMEOUT):
		if(timeout==DEFAULT_TIMEOUT):
			timeout = self.defaultTimeout #inherit the timeout from the class definition
		currentTime = time.perf_counter()
		if(self.currentTransaction):
			#check if the ongoing transaction is still in time
			if self.currentTransaction.deadline < currentTime:
				self.currentTransaction.wasTimedout = True
				self.currentTransaction.deadline = currentTime
			else:
				raise EoqTransactionError(1,'Cannot start transactionRecord another transaction is ongoing')
		#create a new transaction
		transactionId = self.transactionCount
		transaction = Transaction(id=transactionId,starttime=currentTime,maxDuration=timeout,deadline=(currentTime+timeout))
		self.transactions.add(transaction)
		self.transactionCount += 1
		
		self.currentTransaction = transaction
		return transaction
		
	def __EndTransaction(self,transaction):
		currentTime = time.perf_counter()
		transaction.wasEnded = True
		transaction.endtime = currentTime
		self.currentTransaction = None
		
	def __ValidateTransaction(self,transaction):
		currentTime = time.perf_counter()
		if self.currentTransaction == transaction:
			#check if the transaction has still time
			if transaction.deadline > currentTime:
				return transaction #everything seems ok, the transaction can go on
			else:
				#transaction.Timeout(currentTime)
				transaction.wasTimedout = True
				transaction.deadline = currentTime
				self.currentTransaction = None
				raise EoqTransactionError(2,'Transaction timeout. The requested transaction time of %f s is over since it is now %f s after begin. Quit here.'%(transaction.maxDuration,currentTime-transaction.starttime))
		else:
			if(transaction.wasEnded):
				raise EoqTransactionError(3,'Your transaction is not active any more. It was closed %f s ago.'%(currentTime-transaction.endtime))
			if(transaction.wasTimedout):
				raise EoqTransactionError(4,'Your transaction is not active any more. It timed out %f s ago.'%(currentTime-transaction.deadline))
			else:
				raise EoqTransactionError(5,'Serious error. Your transaction is not active any more. But reason is not clear.')
		return transaction
		
	def __Resolve(self,value : Value, expectedType : object, name : str, transaction : Transaction):
		resolvedValue = self.__ResolveHistory(value, transaction)
		if(not isinstance(resolvedValue,expectedType)):
			raise EoqValueError(33,'Wrong value type. Got value type %s for parameter %s, but expected type %s'%(type(resolvedValue).__name__,name,expectedType.__name__),value)
		return resolvedValue
		
	'''
	examples:
	- Retrieve(None,':architecture.ecore') #returns the root of resource 'architecture.ecore
	'''
	def __Retrieve(self,targetIds,query,transaction):
		transaction = self.__ValidateTransaction(transaction)
		
		hTargetIds = self.__ResolveHistory(targetIds,transaction)
		pTargetIds = ValueParser.ValueToPython(hTargetIds)
		targetObjs = self.__DecodeObjects(pTargetIds)
		#check the input type
		if(query.sourceClass):
			self.__ValidateSourceClass(targetObjs,query.sourceClass)
			
		
		#resultObjs = self.__RetrieveSegments(targetObjs,query.segments,transaction)
		resultObjs = self.__ResolveSegmentsRecursive(targetObjs,query.segments,0,1,transaction)
		
		
		#consider multiplicity
		if(query.returnMultiplicity):
			resultObjs = self.__ApplyReturnMultiplicity(resultObjs,query.returnMultiplicity)
		

		resultIds = self.__EncodeObjects(resultObjs)
		values = ValueParser.PythonToValue(resultIds)
		
		#store result in history	
		historyEntry = ValueParser.CloneValue(values) #must be cloned since it can be modified from outside otherwise
		self.__AddToHistory(historyEntry,transaction)
		
		return values
	
	def __Update(self,targetIds,query,value,transaction):
		transaction = self.__ValidateTransaction(transaction)
		hTargetIds = self.__ResolveHistory(targetIds,transaction)
		pTargetIds = ValueParser.ValueToPython(hTargetIds)
		targetObjs = self.__DecodeObjects(pTargetIds)
		hvalue = self.__ResolveHistory(value,transaction)
		pvalue = ValueParser.ValueToPython(hvalue)
		pvalue = self.__DecodeObjects(pvalue)

		nSegments = len(query.segments)
		lastSegment = None
		if(1==nSegments):
			updateObjs = targetObjs
			lastSegment = query.segments[0]
		elif(1<nSegments):
			lastSegment = query.segments[-1]
			#updateObjs = self.__RetrieveSegments(targetObjs, query.segments[:-1],transaction)
			updateObjs = self.__ResolveSegmentsRecursive(targetObjs, query.segments[:-1],0,1,transaction)
		
		#retrieve the actual values for the purpose of logging this transaction
		pOldValue = None
		if(isinstance(updateObjs,Resource)):
			pOldValue = []
		else:
			#pOldValue = self.__RetrieveSegments(updateObjs,[lastSegment],transaction)
			pOldValue = self.__ResolveSegmentsRecursive(updateObjs,[lastSegment],0,1,transaction)
		pOldValueNoObjects = self.__EncodeObjects(pOldValue)
		oldValue = ValueParser.PythonToValue(pOldValueNoObjects)
		
		#Carry out actual update
		self.__UpdateSegments(updateObjs,lastSegment,pvalue,transaction)	
		
		#get the new value in the new encoding (History values must be eliminated by real objects
		pNewValueNoObjects = self.__EncodeObjects(pvalue)
		newValue = ValueParser.PythonToValue(pNewValueNoObjects)
				
		#return the changed elements
		changedObjs = updateObjs
		changedObjsNoObject = self.__EncodeObjects(changedObjs)
		
		effectedObjects = ValueParser.PythonToValue(changedObjsNoObject)
		
		#store the changes in the record
		changedTargets = ValueParser.CloneValue(effectedObjects) #objects must be cloned, because they become alread member of the returned results
		lastSegmentOnlyQuery = Query()
		lastSegmentOnlyQuery.segments.append(lastSegment) #this line might change the initial query object.
		self.__AddToChangeRecord(changedTargets, lastSegmentOnlyQuery, newValue, oldValue, transaction)
		
		return effectedObjects
	
	def __Create(self,packageNsUri,className,numberOfInstances,transaction):
		transaction = self.__ValidateTransaction(transaction)
		#Create the new EObject
		obj = None
		try:
			pack = self.resourceSet.metamodel_registry[packageNsUri]
		except KeyError:
			raise EoqCreateError(5,'ERROR(NS): No package with namespace %s is known.'%(packageNsUri),packageNsUri,className)
		clazz = pack.getEClassifier(className)
		if(None is clazz): 
			raise EoqCreateError(6,'ERROR(class): No class named %s in package %s.'%(className,packageNsUri),packageNsUri,className)
		try:
			if(1==numberOfInstances):
				obj = clazz()
			elif(1<numberOfInstances):
				obj = []
				for i in range(numberOfInstances):
					obj.append(clazz())
		except TypeError as e:
			raise EoqCreateError(7,'ERROR(instantiation): %s.'%(e),packageNsUri,className)
		
		
		
		objectId = self.__EncodeObjects(obj)
		
		value = ValueParser.PythonToValue(objectId)
		#store result in history	
		historyEntry = ValueParser.CloneValue(value) #must be cloned since it can be modified from outside otherwise
		self.__AddToHistory(historyEntry,transaction)
		
		return value
	
	def __Clone(self,targetIds,mode,transaction):
		transaction = self.__ValidateTransaction(transaction)
		
		hTargetIds = self.__ResolveHistory(targetIds,transaction)
		pTargetIds = ValueParser.ValueToPython(hTargetIds)
		targetObjs = self.__DecodeObjects(pTargetIds)
		
		
		#resultObjs = self.__RetrieveSegments(targetObjs,query.segments,transaction)
		resultObjs = self.__CloneRecursive(targetObjs,mode,transaction)
		
		resultIds = self.__EncodeObjects(resultObjs)
		values = ValueParser.PythonToValue(resultIds)
		
		#store result in history	
		historyEntry = ValueParser.CloneValue(values) #must be cloned since it can be modified from outside otherwise
		self.__AddToHistory(historyEntry,transaction)
		
		return values
	
	def __CloneRecursive(self,targetObjs,mode,transaction):
		value = None
		if(isinstance(targetObjs, list)):
			value = []
			for targetObj in targetObjs:
				value.append(self.__CloneRecursive(targetObj, mode, transaction))
		else:
			if(CloneModesE.CLASS==mode):
				value = self.__ECloneClass(targetObjs)
			elif(CloneModesE.ATTRIBUTES==mode):
				value = self.__ECloneAttributes(targetObjs)
			elif(CloneModesE.FULL==mode):
				value = self.__ECloneFull(targetObjs)
			elif(CloneModesE.DEEP==mode):
				value = self.__ECloneDeep(targetObjs)
		return value
	
	def __AddToHistory(self,value,transaction):
		transaction.history.add(value) 
		
	def __ResolveHistory(self,value,transaction):
		#resolvedValue = value
		if(value.type == ValueTypesE.HISTORYREF):
			slot = value.v
			nHistory = len(transaction.history)
			if(slot<nHistory):
				if(slot<0):
					slot = nHistory+slot #slot is negative
				historyValue = transaction.history[slot]
				value = ValueParser.CloneValue(historyValue)
			else:
				raise EoqIdError(9,'Error history $%s does not exist. The current history length for this transaction is %d'%(slot,len(transaction.history)),slot)
		elif(value.type == ValueTypesE.LIST):
			nSubvalues = len(value.v)
			for i in range(nSubvalues):
				value.v[i] = self.__ResolveHistory(value.v[i], transaction)
		return value
		
	def __EncodeObjects(self,objs):
		if(isinstance(objs,list)):
			n = len(objs)
			for i in range(n):
				objs[i] = self.__EncodeObjects(objs[i])
		elif(isinstance(objs,EEnumLiteral)):
			objs = str(objs)
		elif(isinstance(objs,(EObject,type))):
			objs = self.__EncodeSingleObject(objs)
		return objs
	
	def __EncodeSingleObject(self,obj):
		idNb = 0
		try:
		##if obj in self.objectToIdLUT:
			idNb = self.objectToIdLUT[obj]
		except:
		#else:
			idNb = self.lastId
			self.objectToIdLUT[obj] = idNb
			self.idToObjectLUT[idNb] = obj
			self.lastId += 1 #root id starts now at 0 like all other indexes
		return ObjectRefValue(v=idNb)
	
	def __DecodeObjects(self,objIds):
		if(isinstance(objIds,list)):
			n = len(objIds)
			for i in range(n):
				objIds[i] = self.__DecodeObjects(objIds[i])
		elif(isinstance(objIds,ObjectRefValue)):
			objIds = self.__DecodeSingleObject(objIds)
		return objIds
	
	def __DecodeSingleObject(self,objId):
		obj = None
		idNb = objId.v
		try:
		#if idNb in self.idToObjectLUT:
			obj = self.idToObjectLUT[idNb]
		except:
		#else:
			raise EoqIdError(8,'Error id #%s is not a known object'%(idNb),idNb)
		return obj
		
	'''
	PRIVATE METHODS
	'''

	def __UpdateSegments(self,targetObjs,segment,value,transaction):
		if(isinstance(targetObjs,list)):
			nTargetObjs = len(targetObjs)
			isOneToOneAssignment = False
			if(isinstance(value,list)):
				nValues = len(value)
				if(nValues==nTargetObjs):
					isOneToOneAssignment = True #in this case each of the entries in values is assigned to exactly on target obj
			for i in range(nTargetObjs):
				targetObj = targetObjs[i]
				v = value[i] if isOneToOneAssignment else value		
				if(None == v):
					pass	
				if(isinstance(targetObj,list)):
					self.__UpdateSegments(targetObj,segment,v,transaction) #recursion
				else:
					self.__UpdateSegment(targetObj,segment,v,transaction)
		else:
			self.__UpdateSegment(targetObjs,segment,value,transaction)
		return
	
	def __UpdateSegment(self,targetObj,segment,value,transaction):
		if(segment.selector):
			raise EoqUpdateError(10,"ERROR: Set operation can not have a selector",value)
			return []
		if(segment.depth):
			raise EoqUpdateError(10,"ERROR: Set operation can not have a depth",value)
			return []
		if(isinstance(segment,PathSegment)):
			#for o in objs:
			self.__SetReferenceOrAttribute(targetObj,segment,value,transaction)
			#resource = targetObj.eResource
			#if(None != resource):
				#self.resourceDirty[resource] = True
		elif(isinstance(segment,ResourceSegment)):
			destination = self.__RetrieveResourceSegment(segment.identifier)
			#get the resource, or load it and clear existing elements if required.
			resource = None
			resourceContents = None
			
			if(isinstance(destination,Resource)): #resource is empty
				resource = destination
				resourceContents = []
			elif(isinstance(destination,list)): #resource has already a obj element, which is now replaced
				resource = destination[0].eResource
				resourceContents = destination
				
			#check for index
			if(segment.index):
				nResourceContents = len(resourceContents)
				if(segment.index.type == IndexTypesE.NUMBER):
					if(isinstance(value,list)):
						raise EoqUpdateError(11,"When setting a specific resource %d index, must be an EObject, not a list."%(segment.index.value),value)
					if(segment.index.value > nResourceContents):
						raise EoqUpdateError(12,"Resource has only %d elements. Cannot set index %"%(nResourceContents,segment.index.value),value)
					#because the resource array can not be edited directly, the elements that shall persist must be collected and later readded
					removedResources = [] 
					for i in range(nResourceContents):
						if(i>=segment.index.value):
							resource.remove(resourceContents[i])
						if(i>segment.index.value):
							removedResources.append(resourceContents[i])
					#add the new entry and all old ones
					if(isinstance(value,EObject)):
						resource.append(value)
					elif(None==value):
						pass # do nothing, which means the element is removed
					for c in removedResources:
						resource.append(c)
				if(segment.index.type == IndexTypesE.ADD):
					if(isinstance(value,list)):
						raise EoqUpdateError(13,"When setting a specific resource %d index, must be an EObject, not a list."%(segment.index.value),value)
					resource.append(value)	
				if(segment.index.type == IndexTypesE.REMOVE):
					if(isinstance(value,list)):
						raise EoqUpdateError(14,"When setting a specific resource %d index, must be an EObject, not a list."%(segment.index.value),value)
					resource.remove(value)
			else: #without index
				#delete all existing
				for c in resourceContents:
					resource.remove(c)
				#add new ones
				if(isinstance(value,list)):
					for v in value:
						if(not isinstance(v,EObject)):
							raise EoqUpdateError(15,"Could not set resource because value must be EObject or list of EObjects, but got %s"%(type(v)),value)
						resource.append(v)
				elif(isinstance(value,EObject)):
					resource.append(value)
				elif(value==None):
					pass #do nothing resource stays empty and can be deleted		
				else:
					raise EoqUpdateError(16,"Could not set resource because value must be EObject or list of EObjects, but got %s"%(type(value)),value)
			#self.resourceDirty[resource] = True
			return

	def __SetReferenceOrAttribute(self,targetObj,segment,value,transaction):
		identifier = segment.identifier
		
		feature = targetObj.eClass.findEStructuralFeature(identifier)
		if(None==feature):
			raise EoqUpdateError(30,"ERROR: Object of class %s has no feature named %s"%(targetObj.eClass,identifier),value)
		
		if(feature.many):
			if(segment.index):
				index = segment.index
				if(index.type == IndexTypesE.NUMBER):
					i = index.value; 
					if(i<0 or (feature.upperBound > 0 and i>= feature.upperBound)):
						raise EoqUpdateError(31,"Maximum number of elements is %d. Index %d is iligeal"%(feature.upperBound,i),value)
					if(None == value):
						valueAtIndex = targetObj.eGet(feature)[i] 
						targetObj.eGet(feature).remove(valueAtIndex)
					else:
						targetObj.eGet(feature)[i] = value 
				elif(index.type == IndexTypesE.RANGE):
					#TODO implement
					raise EoqUpdateError(32,"WARNING: Range indexing is currently not implemented",value)
				elif(index.type == IndexTypesE.ADD):
					if(isinstance(value,list)):
						for v in value:
							targetObj.eGet(feature).add(v)
					else:
						targetObj.eGet(feature).add(value)
				elif(index.type == IndexTypesE.REMOVE):
					if(isinstance(value,list)):
						for v in value:
							targetObj.eGet(feature).remove(v)
					else:
						targetObj.eGet(feature).remove(value)
				else:
					#Should never go here
					raise EoqUpdateError(33,"ERROR: Unsupported index type %s."%(type(index)),value)
			else: #no index
				targetObj.eGet(feature).clear()
				if(None != value):
					targetObj.eGet(feature).add(value)
		else: #not many
			if(segment.index):
				index = segment.index
				if(index.type == IndexTypesE.NUMBER):
					i = index.value-1; #because Python indexes beginning at 0
					# the only accepted index is 0
					if(i!=0):
						raise EoqUpdateError(40,"Maximum number of elements is %d. Index %d is iligeal"%(feature.upperBound,i),value)
					else:
						targetObj.eSet(feature,value) 
				elif(index.type == IndexTypesE.RANGE):
					raise EoqUpdateError(41,"Range indexing is not applicable for single element references",value)
				elif(index.type == IndexTypesE.ADD):
					if(None == targetObj.eGet(feature)):
						targetObj.eSet(feature,value)
					else:
						raise EoqUpdateError(42,"Maximum number of elements is %d. Cannot attach a further element by [+]"%(feature.upperBound),value)
				elif(index.type == IndexTypesE.REMOVE):
					targetObj.eSet(feature,None)
			else: #no index
				targetObj.eSet(feature,value)
	
		modelResource = self.__GetContainingResourceObject(targetObj)
		if(modelResource):
			self.__SetResourceDirty(modelResource, transaction)
	
	def __ResolveSegmentsLinear(self,targetObjs,segments,currentSegment,currentDepth,transaction):
		resultObjs = None
		nSegments = len(segments)
		if(currentSegment < nSegments and targetObjs):
			childObjs = None
			segment = segments[currentSegment]
			if(segment.identifierType == ListOpSegmentTypesE.from_string('SIZE')):
				if(isinstance(targetObjs,list)):
					childObjs = len(targetObjs)
				else:
					childObjs = 1;
			elif(segment.identifierType == ListOpSegmentTypesE.from_string('FLATTEN')):
				pass
			#continue recursion
			resultObjs = self.__ResolveSegmentsRecursive(childObjs,segments,currentSegment+1,1,transaction) #start path recursion	
		else: #recursion is over
			resultObjs = targetObjs
		return resultObjs
		
	def __ResolveSegmentsRecursive(self,targetObjs,segments,currentSegment,currentDepth,transaction):
		resultObjs = None
		#parentObjs = targetObjs
		nSegments = len(segments)
		if(currentSegment < nSegments and targetObjs): #non exiting objects are as null):
			segment = segments[currentSegment]
			
			#evaluate the current segment
			if(SegmentProcessingTypesE.LINEAR == segment.processingType):
				resultObjs = self.__ResolveSegmentsLinear(targetObjs,segments,currentSegment,1,transaction)
			else:
				if(isinstance(targetObjs,list)):
					resultObjs = []
					for targetObj in targetObjs:
						
						resultObj = self.__ResolveSegmentsRecursive(targetObj,segments,currentSegment,1,transaction)
						resultObjs.append(resultObj)
				else: #Could check for none here, but prefere that the user gets and error if the following is an unset object
					resultObj = self.__ResolveSegment(targetObjs,segment,transaction)
					#apply index
					if(segment.index):
						resultObj = self.__ApplyIndex(resultObj, segment.index)
					
					childObjs = self.__ResolveSegmentsRecursive(resultObj,segments,currentSegment+1,1,transaction) #start path recursion
					
					#apply depth (Seems realy complex think about disabling depth for deterministic applications
					if(segment.depth and segment.depth.value != currentDepth):
						if(isinstance(resultObj,list)):
							for i in range(len(resultObj)):
								recursiveChildObj = self.__ResolveSegmentsRecursive(resultObj[i],segments,currentSegment,currentDepth+1,transaction) #start depth recursion
								if(recursiveChildObj):
									if(not isinstance(childObjs,list)):
										childObjs[i] = [childObjs[i]]
									if(isinstance(recursiveChildObj,list)):
										childObjs[i].extend(recursiveChildObj)
									else:
										childObjs[i].append(recursiveChildObj)
						#merge results
						elif(resultObj):
							recursiveChildObj = self.__ResolveSegmentsRecursive(resultObj,segments,currentSegment,currentDepth+1,transaction) #start depth recursion
							if(recursiveChildObj):
								if(not isinstance(childObjs,list)):
									childObjs = [childObjs]
								if(isinstance(recursiveChildObj,list)):
									childObjs.extend(recursiveChildObj)
								else:
									childObjs.append(recursiveChildObj)
						
					resultObjs = childObjs	
		else: #recursion is over
			resultObjs = targetObjs
		return resultObjs
		
	def __ResolveSegment(self,targetObj,segment,transaction):
		resultObjs = None
		
		#selector
		selectorFunctor = self.__CreateSelectorFunctor(segment,transaction)
		
		#Eval individual segment types
		if(segment.type == SegmentTypesE.PATH):
			resultObjs = self.__RetrievePathSegment(targetObj,segment.identifier,selectorFunctor)
		elif(segment.type == SegmentTypesE.CLAZZ):
			resultObjs = self.__RetrieveClassSegment(targetObj,segment.identifier,selectorFunctor)
		elif(segment.type == SegmentTypesE.INSTANCE):
			resultObjs = self.__RetrieveInstanceOfSegment(targetObj,segment.identifier,selectorFunctor)
# 		elif(segment.type == SegmentTypesE.ID):
# 			childs = self.__RetrieveIdSegment(targetObj,segment.identifier)
		elif(segment.type == SegmentTypesE.META):
			resultObjs = self.__RetrieveMetaSegment(targetObj,segment,selectorFunctor)
		elif(segment.type == SegmentTypesE.RESOURCE):
			resultObjs = self.__RetrieveResourceSegment(segment.identifier)
		return resultObjs
	
	def __CreateSelectorFunctor(self,segment,transaction):
		
		#consider the selector
		selectorFunctor = lambda o: True
		
		if(segment.selector):
			#initialization
			comperatorFunctor = lambda a,b:False
			selectFunctor = lambda o:False
			
			#handle selector
			selector = segment.selector
			selectFunctor  = lambda o: o.eGet(selector.name)
			
			#handle operation
			operator = selector.operator
			if(operator.type == OperatorTypesE.EQUAL):
				comperatorFunctor = lambda a,b: a==b
			elif(operator.type == OperatorTypesE.NOTEQUAL):
				comperatorFunctor = lambda a,b: a!=b
			elif(operator.type == OperatorTypesE.GREATER):
				comperatorFunctor = lambda a,b: a>b
			elif(operator.type == OperatorTypesE.LESS):
				comperatorFunctor = lambda a,b: a<b
			
			#handle value type
			valueObj = selector.value
			if(valueObj.type == ValueTypesE.INT):
				value = valueObj.v
			elif(valueObj.type == ValueTypesE.FLOAT):
				value = valueObj.v
			elif(valueObj.type == ValueTypesE.BOOL):
				value = valueObj.v
			elif(valueObj.type == ValueTypesE.STRING):
				value = valueObj.v
			elif(valueObj.type == ValueTypesE.OBJECTREF):
				value = self.__DecodeSingleObject(valueObj)
			elif(valueObj.type == ValueTypesE.HISTORYREF):
				value = self.__ResolveHistory(valueObj,transaction)
			elif(valueObj.type == ValueTypesE.EMPTY):
				value = None
			
			selectorFunctor  = lambda o: self.__DoesObjectMatchSelector(o,comperatorFunctor,selectFunctor,value)
		
		return selectorFunctor
	
	def __DoesObjectMatchSelector(self,obj,comperatorFunctor,selectFunctor,value):
		a = selectFunctor(obj)
		if(isinstance(a,EOrderedSet)):
			for memberOfA in a:
				if(comperatorFunctor(memberOfA,value)):
					return True
			return False #if no comparison was successful the result is false
		else:
			return comperatorFunctor(a,value)

	
	def __RetrievePathSegment(self,targetObj,refname,selectorFunctor):
		resultObjs = None
		#children = targetObj.eGet(refname)
		children = targetObj.__getattribute__(refname); #hack for more speed
		if(isinstance(children,types.MethodType)):
			#children = targetObj.eGet(refname)() #imitate a method call
			children = targetObj.__getattribute__(refname)() #imitate a method call
		if(isinstance(children,(EOrderedSet,list,set))):
			resultObjs = []
			for child in children:
				if(selectorFunctor(child)):
					resultObjs.append(self.__ResolveProxyAndBuildInClasses(child))
		elif(selectorFunctor(children)):
			resultObjs = self.__ResolveProxyAndBuildInClasses(children)
		return resultObjs
	
	def __ResolveProxyAndBuildInClasses(self,obj): 
		if(isinstance(obj, EProxy)):
			obj.force_resolve()
			obj = obj._wrapped #remove the outer proxy
		if(isinstance(obj, (MetaEClass,type,types.ModuleType))): #this is necessary to mask compiled model instances
			obj = obj.eClass
		return obj
	
	def __ApplyIndex(self,objs,segmentIndex):
		if(segmentIndex.type in [IndexTypesE.NUMBER,IndexTypesE.RANGE] and isinstance(objs,list)):
			nObjs = len(objs)
			if(segmentIndex.type == IndexTypesE.NUMBER):
				if(segmentIndex.value >= nObjs):
					raise EoqRetrieveError(10,'Index value %d is greater than result size of %d'%(segmentIndex.value,nObjs))
				return objs[segmentIndex.value]
			elif(segmentIndex.type == IndexTypesE.RANGE):
				if(segmentIndex.upper >= nObjs) :
					raise EoqRetrieveError(11,'Upper range index %d is greater than the result size of %d'%(segmentIndex.upper,nObjs))
				return objs[segmentIndex.lower:segmentIndex.upper]
		else:
			return objs
	
	def __RetrieveClassSegment(self,targetObj,clsname,selectorFunctor):
		resultObjs = []

		if(self.__IsType(targetObj,clsname) and selectorFunctor(targetObj)):
			resultObjs.append(targetObj)
		contents = targetObj.eAllContents()
		if(contents):
			for c in contents:
				if(self.__IsType(c,clsname) and selectorFunctor(c)):
					resultObjs.append(c)		
		return resultObjs
	
	def __RetrieveInstanceOfSegment(self,targetObj,clsname,selectorFunctor):
		resultObjs = []
		if(self.__IsInstanceOf(targetObj,clsname) and selectorFunctor(targetObj)):
			resultObjs.append(targetObj)
		contents = targetObj.eAllContents()
		if(contents):
			for c in contents:
				if(self.__IsInstanceOf(c,clsname) and selectorFunctor(c)):
					resultObjs.append(c)		
		return resultObjs
	
# 	def __RetrieveIdSegment(self,objs,idstr):
# 		results = []
# 		for o in objs:
# 			r = []	
# 			results += r
# 		return r
	
	def __RetrieveMetaSegment(self,targetObj,segment,selectorFunctor):
		resultObjs = []
		if(segment.identifierType == MetaSegmentIdentifiersE.from_string('CONTAINER')):
			resultObjs = targetObj.eContainer()
		elif(segment.identifierType == MetaSegmentIdentifiersE.from_string('INDEX')):
			f = targetObj.eContainmentFeature()
			if(None==f or f.upperBound == 1):
				resultObjs = 0 ##-1 denotes the index makes no sense for single object references
			else: #index must be determined by backwards search
				#this backward search seems not optimal
				containingIndex = 0 #Eoq indicies start at 1
				container = targetObj.eContainer()
				for sibling in container.eGet(f):
					containingIndex = containingIndex+1
					if(sibling==targetObj):
						resultObjs = containingIndex
						break;
		elif(segment.identifierType == MetaSegmentIdentifiersE.from_string('TYPE')):
			resultObjs = targetObj.eClass.findEStructuralFeature(segment.identifier) #does not make sence since it only works for 
		elif(segment.identifierType == MetaSegmentIdentifiersE.from_string('CLASS')):
			resultObjs = self.__ResolveProxyAndBuildInClasses(targetObj.eClass)
		elif(segment.identifierType == MetaSegmentIdentifiersE.from_string('CONTENTS')):
			resultObjs = [x for x in targetObj.eContents if selectorFunctor(x)]
		elif(segment.identifierType == MetaSegmentIdentifiersE.from_string('CLASSNAME')):
			resultObjs = targetObj.eClass.name
		elif(segment.identifierType == MetaSegmentIdentifiersE.from_string('PACKAGE')):
			resultObjs = self.__ResolveProxyAndBuildInClasses(targetObj.eClass.eContainer())
		elif(segment.identifierType == MetaSegmentIdentifiersE.from_string('PACKAGENAME')):
			resultObjs = targetObj.eClass.eContainer().name
		elif(segment.identifierType == MetaSegmentIdentifiersE.from_string('RESOURCE')):
			resultObjs = self.__GetContainingResourceObject(targetObj)
		elif(segment.identifierType == MetaSegmentIdentifiersE.from_string('RESOURCENAME')):
			resultObjs = ''
			for key,value in self.resourceSet.resources.items():
				if value==targetObj.eResource:
					resultObjs = self.__ResourcePathOnly(key)
					break;
		elif(segment.identifierType == MetaSegmentIdentifiersE.from_string('CONTAININGFEATURE')):
			f = self.__ResolveProxyAndBuildInClasses(targetObj.eContainmentFeature())
			if(f):
				resultObjs = f
			else:
				resultObjs = None
		elif(segment.identifierType == MetaSegmentIdentifiersE.from_string('CONTAININGFEATURENAME')):
			f = targetObj.eContainmentFeature()
			if(f):
				resultObjs = f.name
			else:
				resultObjs = ''
		elif(segment.identifierType == MetaSegmentIdentifiersE.from_string('FEATURES')):
			resultObjs = [self.__ResolveProxyAndBuildInClasses(x) for x in targetObj.eClass.eAllStructuralFeatures() if selectorFunctor(x)]
		elif(segment.identifierType == MetaSegmentIdentifiersE.from_string('FEATURENAMES')):
			resultObjs = [x.name for x in targetObj.eClass.eAllStructuralFeatures() if selectorFunctor(x)]
		elif(segment.identifierType == MetaSegmentIdentifiersE.from_string('FEATUREVALUES')):
			features = [x.name for x in targetObj.eClass.eAllStructuralFeatures() if selectorFunctor(x)]
			resultObjs = [self.__OrderedSetEliminator(targetObj.eGet(a)) for a in features]
			for i in range(len(resultObjs)):
				if(isinstance(resultObjs[i], list)):
					for j in range(len(resultObjs[i])):
						resultObjs[i][j] = self.__ResolveProxyAndBuildInClasses(resultObjs[i][j])
				else:
					resultObjs[i] = self.__ResolveProxyAndBuildInClasses(resultObjs[i])
			#resultObjs = [[ self.__ResolveProxyAndBuildInClasses(x) for x in self.__OrderedSetEliminator(targetObj.eGet(a))] for a in features]
		elif(segment.identifierType == MetaSegmentIdentifiersE.from_string('ATTRIBUTES')):
			resultObjs = [self.__ResolveProxyAndBuildInClasses(x) for x in targetObj.eClass.eAllAttributes() if selectorFunctor(x)]
		elif(segment.identifierType == MetaSegmentIdentifiersE.from_string('ATTRIBUTENAMES')):
			resultObjs = [x.name for x in targetObj.eClass.eAllAttributes() if selectorFunctor(x)]
		elif(segment.identifierType == MetaSegmentIdentifiersE.from_string('ATTRIBUTEVALUES')):
			attributes = [x for x in targetObj.eClass.eAllAttributes() if selectorFunctor(x) ]
			resultObjs = [targetObj.eGet(a) for a in attributes]
		elif(segment.identifierType == MetaSegmentIdentifiersE.from_string('EALLREFERENCES')):
			resultObjs = [self.__ResolveProxyAndBuildInClasses(x) for x in targetObj.eAllReferences() if selectorFunctor(x)] 
		elif(segment.identifierType == MetaSegmentIdentifiersE.from_string('REFERENCES')):
			resultObjs = [self.__ResolveProxyAndBuildInClasses(x) for x in targetObj.eClass.eAllReferences() if selectorFunctor(x)] 
		elif(segment.identifierType == MetaSegmentIdentifiersE.from_string('REFERENCENAMES')):
			resultObjs = [x.name for x in targetObj.eClass.eAllReferences() if selectorFunctor(x)]
		elif(segment.identifierType == MetaSegmentIdentifiersE.from_string('REFERENCEVALUES')):
			references = [x.name for x in targetObj.eClass.eAllReferences() if selectorFunctor(x)]
			resultObjs = [self.__OrderedSetEliminator(targetObj.eGet(a)) for a in references]
			for i in range(len(resultObjs)):
				if(isinstance(resultObjs[i], list)):
					for j in range(len(resultObjs[i])):
						resultObjs[i][j] = self.__ResolveProxyAndBuildInClasses(resultObjs[i][j])
				else:
					resultObjs[i] = self.__ResolveProxyAndBuildInClasses(resultObjs[i])
		elif(segment.identifierType == MetaSegmentIdentifiersE.from_string('CONTAINMENTS')):
			resultObjs = [self.__ResolveProxyAndBuildInClasses(x) for x in targetObj.eClass.eAllReferences() if x.containment and selectorFunctor(x)] 
		elif(segment.identifierType == MetaSegmentIdentifiersE.from_string('CONTAINMENTNAMES')):
			resultObjs = [x.name for x in targetObj.eClass.eAllReferences() if x.containment and selectorFunctor(x)] 
		elif(segment.identifierType == MetaSegmentIdentifiersE.from_string('CONTAINMENTVALUES')):
			containments = [x.name for x in targetObj.eClass.eAllReferences() if x.containment and selectorFunctor(x)]
			resultObjs = [self.__OrderedSetEliminator(targetObj.eGet(a)) for a in containments] 
		else:
			raise EoqRetrieveError(51,'Illegal meta segment %s for object'%(segment.identifier))
		return resultObjs
	
	def __SetResourceDirty(self,modelResource,transaction):
		if(not modelResource.isDirty):
			modelResource.isDirty = True
			self.__AddToChangeRecord(self.__EncodeSingleObject(modelResource), QueryParser.StringToQuery('/isDirty'), BoolValue(v=True), BoolValue(v=False), transaction)
	
	def __SetResourceClean(self,modelResource,transaction):
		if(modelResource.isDirty):
			modelResource.isDirty = False
			self.__AddToChangeRecord(self.__EncodeSingleObject(modelResource), QueryParser.StringToQuery('/isDirty'), BoolValue(v=False), BoolValue(v=True), transaction)
	
	def __SetResourceLoaded(self,modelResource,transaction):
		if(not modelResource.isLoaded):
			modelResource.isLoaded = True
			self.__AddToChangeRecord(self.__EncodeSingleObject(modelResource), QueryParser.StringToQuery('/isLoaded'), BoolValue(v=True), BoolValue(v=False), transaction)
	
	def __SetResourcePersistentPath(self,modelResource,newPath,transaction):
		if(modelResource.lastPersistentPath != newPath):
			oldPath = modelResource.lastPersistentPath
			modelResource.lastPersistentPath = newPath
			self.__AddToChangeRecord(self.__EncodeSingleObject(modelResource), QueryParser.StringToQuery('/lastPersistentPath'), StringValue(v=newPath), StringValue(v=oldPath) if oldPath else EmptyValue(), transaction)

	
	def __GetContainingResourceObject(self,obj):
		resourceObj = None
		eResource = obj.eResource
		if(eResource in self.resourceObjectLUT):
			resourceObj = self.resourceObjectLUT[eResource]
		else:
			resourceObj = self.__RecursiveResourceObjSearch(obj)
		return resourceObj
	
	def __RecursiveResourceObjSearch(self,obj):
		resourceObj = None
		if(isinstance(obj,FileResourceA)):
			resourceObj = obj
		else:
			container = obj.eContainer()
			if(container):
				resourceObj = self.__RecursiveResourceObjSearch(container)
		return resourceObj
	
	def __RetrieveResourceSegment(self,resourceName):
		resultObjs = None
		resourcePath = os.path.join(self.baseDir,resourceName)
		resourceUri = URI(resourcePath)
		if resourceUri.normalize() not in self.resourceSet.resources:
			if(os.path.isfile(resourcePath)):
				if('.ecore' in resourceName and 'Ecore.ecore' not in resourceName): #register a meta model automatically. 
					#Prevent that the Ecore definition is registered as a new meta-model. Since the Ecore meta model is implemented in 
					#pyecore already, this will create a mess or name ambiguities.
					gcmRoot = self.__LoadMetaModelResource(resourcePath)
				else: 
					gcmRoot = self.__LoadModelResource(resourcePath)
				resultObjs = gcmRoot
			else:
				resource = self.resourceSet.create_resource(resourcePath)
				resultObjs = resource
		else:
			resource = self.resourceSet.resources[resourceUri.normalize()]
			if(len(resource.contents)>0):
				resultObjs = list(resource.contents) #resource list is an object, so if it is modified later this makes problems. Therefore a copy must be created.
			else:
				resultObjs = resource
		return resultObjs
	
	'''
	UTILITY FUNCTIONS
	'''
	
	def __IsType(self,obj,classname):
		return (obj.eClass.name==classname)
	
	def __IsInstanceOf(self,obj,classname):
		result = self.__IsType(obj,classname)
		if(not result):
			for superType in obj.eClass.eAllSuperTypes():
				if(superType.name==classname):
					result = True
					break
			if('EObject'==classname):
				result = isinstance(obj,EObject)
		return result
	
	def __ResourcePathOnly(self,absoluteResourcePath):
		absoluteBaseDirPath = self.baseDirUri.normalize();
		#absoluteResourcePath = resourceUri.normalize() 
		
		if(absoluteBaseDirPath in absoluteResourcePath):
			resourcePath = absoluteResourcePath[len(absoluteBaseDirPath)+1:]
		else:
			resourcePath = absoluteResourcePath
		return resourcePath
	
	def __ScanForModelFiles(self):
		modelFiles = []
		for root, dirs, files in os.walk(self.baseDir, topdown=True):
			for file in files:
				for extension in self.knownModelExtensions:
					if(file.endswith('.%s'%(extension))):
						relativeRoot = os.path.relpath(root, self.baseDir)
						modelFiles += [os.path.join(relativeRoot,file)] #2: omits the ./ at the beginning
		return modelFiles
	
	def __ValidateSourceClass(self,root,sourceClass):
		isContextValid = False
		className = sourceClass.name
		if(isinstance(root,list)):
			for obj in root:
				self.__ValidateSourceClass(obj, sourceClass)
		else:
			if(root.eClass.name==className):
				isContextValid = True
			elif('EObject'==className):
				isContextValid = isinstance(root,EObject)
			else:
				for superType in root.eClass.eAllSuperTypes():
					if(superType.name==className):
						isContextValid = True
						break
			if(not isContextValid):
				raise EoqContextError(60,"Context should be instance of class %s, but got object of class %s"%(className,root.eClass.name))
		#return isContextValid
	
	def __ApplyReturnMultiplicity(self,r,returnMultiplicity):
		if(returnMultiplicity.type == ReturnMultiplicityTypeE.FLATTENED):
			r = self.__FlattenList(r)
		elif(returnMultiplicity.type == ReturnMultiplicityTypeE.FORCESINGLE):
			if(isinstance(r, list)):
				if(1==len(r)):
					r = r[0]
				elif(0==len(r)):
					r = None
				else:
					raise EoqContextError((70,"Expected multiplicity is %d but got list of %d elements")%(1,len(r)))
		elif(returnMultiplicity.type == ReturnMultiplicityTypeE.UNCHANGED):
			pass #needs no action
		return r
	
	def __LoadModelResource(self,resourceFile):
		resource = self.resourceSet.get_resource(resourceFile)
		return list(resource.contents) #make a copy of the list contents
	
	def __LoadMetaModelResource(self,resourceFile):
		modelContents = self.__LoadModelResource(resourceFile)
		gcmRoot = modelContents[0]
		self.resourceSet.metamodel_registry[gcmRoot.nsURI] = gcmRoot
		# register all possible subpackages
		for child in gcmRoot.eAllContents():
			if(isinstance(child,EPackage)):
				self.resourceSet.metamodel_registry[child.nsURI] = child
		#remember the file extension, which is the file name (without extension) of the model file
		metaModelFileName = os.path.basename(resourceFile)
		modelExtension = os.path.splitext(metaModelFileName)[0]
		self.knownModelExtensions += [modelExtension]
		#return the root
		return modelContents
	
	def __OrderedSetEliminator(self,obj):
		if(isinstance(obj,EOrderedSet)):
			return list(obj)
		else:
			return obj
		
	def __FlattenList(self,nestedList):
		flatList = None
		if(isinstance(nestedList,list)):
			flatList = []
			for l1 in nestedList:
				if(isinstance(l1,list)):
					flatList.extend(self.__FlattenList(l1))
				else:
					flatList.append(l1)
		else:
			flatList = nestedList
		return flatList
	
	def __AddToChangeRecord(self,target,query,newValue,oldValue,transaction):
		changeRecord = Change()
		changeRecord.target = target
		changeRecord.query = query
		changeRecord.newValue = newValue
		changeRecord.oldValue = oldValue
		changeRecord.sourceTransactionId = transaction.id
		changeRecord.changeId = self.changeCount
		self.changes.add(changeRecord)
		self.changeCount += 1
		self.changesLogger.info("%d: %s %s %s %s %d"%(self.changeCount,
													ValueParser.ValueToString(target),
													QueryParser.QueryToString(query),
													ValueParser.ValueToString(newValue),
													ValueParser.ValueToString(oldValue),
													transaction.id))
	
	def __CloneList(self,inList):
		clonedList = None
		if(isinstance(inList,list)):
			clonedList = list(inList)
			for i in range(len(clonedList)):
				clonedList[i] = self.__CloneList(clonedList[i])
		else:
			clonedList = inList
		return clonedList
	
	def __InitLogging(self):
		#create the log dir if it does not exist
		if(not os.path.isdir(self.logPath)):
			os.makedirs(self.logPath)
		#build log folder name from current date
		now = datetime.now() # current date and time
		logBasename = now.strftime("%Y-%m-%d_%H_%M_%S")
		n = 0
		#check if there is already a backup for that second
		while(os.path.isdir(os.path.join(self.logPath,"%s_%05d"%(logBasename,n)))):
			n+=1
		self.currentLogDir = os.path.join(self.logPath,"%s_%05d"%(logBasename,n))
		
		#remove old backups, if limit is exceeded
		existingLogDirs = []
		for name in os.listdir(self.logPath): 
			existingLogDir = os.path.join (self.logPath, name)   
			if os.path.isdir(existingLogDir):
				existingLogDirs.append(existingLogDir)
				
		nExistingLogDirs = len(existingLogDirs)
		nEntriesToDelete = max([nExistingLogDirs-self.logLimit+1,0]) #+1 for the newly created one
		if 0 < nEntriesToDelete:
			existingLogDirs = sorted(existingLogDirs)
			for i in range(nEntriesToDelete):
				shutil.rmtree(existingLogDirs[i])
			nExistingLogDirs -= nEntriesToDelete
		
		#on for the current log
		os.makedirs(self.currentLogDir)
		nExistingLogDirs += 1;
		
		#init error logger
		self.errorsLogger = logging.getLogger('error')
		fh = logging.FileHandler(os.path.join(self.currentLogDir,"errors.log"))
		fh.setLevel(logging.INFO)
		formatter = logging.Formatter('%(asctime)s - %(message)s')
		fh.setFormatter(formatter)
		self.errorsLogger.addHandler(fh)
		self.errorsLogger.setLevel(logging.INFO)
		
		#init command logger
		self.commandsLogger = logging.getLogger('commands')
		fh = logging.FileHandler(os.path.join(self.currentLogDir,"commands.log"))
		fh.setLevel(logging.INFO)
		formatter = logging.Formatter('%(asctime)s - %(message)s')
		fh.setFormatter(formatter)
		self.commandsLogger.addHandler(fh)
		self.commandsLogger.setLevel(logging.INFO)
		
		#init changes logger
		self.changesLogger = logging.getLogger('changes')
		fh = logging.FileHandler(os.path.join(self.currentLogDir,"changes.log"))
		fh.setLevel(logging.INFO)
		formatter = logging.Formatter('%(asctime)s - %(message)s')
		fh.setFormatter(formatter)
		self.changesLogger.addHandler(fh)
		self.changesLogger.setLevel(logging.INFO)
		
		print('Logging enabled! (path: %s, existing: %d, removed: %d, limit: %d)'%(self.currentLogDir,nExistingLogDirs,nEntriesToDelete,self.logLimit))
	
	
	def __Backup(self):
		self.currentBackupDir = os.path.join(self.currentLogDir,"backup")
		
		#os.makedirs(backupName)
		shutil.copytree(self.baseDir,self.currentBackupDir)
		
		print('Backup created! (path: %s)'%(self.currentBackupDir))
	
	
	def __InitCommands(self):
		#load all commands from the meta model and initialize the commands data objects within the domain, such that the information is accessible by queries
		#model.eClass.eClassifiers
		#dummyCommand = RetrieveCommand() #use this to get access to the meta model
		#for commandClass in CommandA.eClass.allInstances(None):
		for classifier in CommandA.eClass.ePackage.eClassifiers:
			if(isinstance(classifier,EClass) and (CommandA.eClass in classifier.eAllSuperTypes())):
				commandClass = classifier
				commandFeatures = commandClass.eStructuralFeatures
				commandName = commandFeatures[0].get_default_value().name #the first feature of each command should always be the type
				commandDescription = self.__GetEAnnotationValue(commandClass,'documentation')
				command = CommandInfo(name=commandName,description=commandDescription)		
				for i in range(1,len(commandFeatures)):
					commandFeature = commandFeatures[i]
					paramName = commandFeature.name 
					paramType = commandFeature.eType.eClass.name
					paramDescription = self.__GetEAnnotationValue(commandFeature,'documentation')
					paramExample = 'exampleParameter'
					if(isinstance(commandFeature, EAttribute) and commandFeature.get_default_value()):
						paramExample = str(commandFeature.get_default_value()) #could be also an integer
					commandParameter = CommandParameter(name=paramName,type=paramType,description=paramDescription,example=paramExample)
					
					command.parameters.add(commandParameter)
				
				#find matching command results
				for resultClassifier in CommandA.eClass.ePackage.eClassifiers:
					if(isinstance(resultClassifier,EClass) and (ResultA.eClass in resultClassifier.eAllSuperTypes())):
						commandResultClass = resultClassifier
						commandResultFeatures = commandResultClass.eStructuralFeatures
						commandResultCommandType = commandResultFeatures[1].get_default_value().name #the second feature of each command should always be the command type
						if(commandResultCommandType == commandName):
							for j in range(1,len(commandResultFeatures)):
								commandResultFeature = commandResultFeatures[j]
								commandResultParamName = commandResultFeature.name
								commandResultParamType = commandResultFeature.eType.eClass.name
								commandResultParamDescription = self.__GetEAnnotationValue(commandResultFeature,'documentation')
								commandResultParamExample = 'exampleResult';
								if(isinstance(commandResultFeature, EAttribute) and commandResultFeature.get_default_value()):
									commandResultParamExample = str(commandResultFeature.get_default_value()) #could be also an integer
								commandResultParameter = CommandParameter(name=commandResultParamName,type=commandResultParamType,description=commandResultParamDescription,example=commandResultParamExample)
								command.results.add(commandResultParameter)
				#finally add the command definition to the domain such that it can be queried
				self.commands.add(command)
		return
				
				
	def __GetEAnnotationValue(self,annotatedElement,key):
		for annotation in annotatedElement.eAnnotations:
			for entry in annotation.entries:
				if(entry.key == key):
					return entry.value
				
		return ''
		
			
	def __LoadMetaModels(self):
		#look for existing meta models and load them on them
		for mp in self.metaDir:
			metadir = mp
			if(not os.path.isabs(mp)):
				metadir = os.path.join(self.baseDir,mp)
			searchString = os.path.join(metadir+'/*.ecore')
			modeldefinitions = glob.glob(searchString)
			for md in modeldefinitions:
				self.__LoadMetaModelResource(md)
					
		#transfer the complete meta registry to the domain model
		for uri in self.resourceSet.metamodel_registry.keys():
			package = self.resourceSet.metamodel_registry[uri]
			if(isinstance(package,types.ModuleType)):
				#this happens for metamodels loaded by generated python code
				#in this case we must create a copy as a psydo EPackge
				package = package.eClass #this is how pyecore generates the models. It is not clear, why the class of this module is a package, but it seems to work
				metamodel = Metamodel(name=package.name,source=MetaModelSourcesE.BUILDIN,package=package)
				self.metamodels.add(metamodel)
			else:
				metamodel = Metamodel(name=package.name,source=MetaModelSourcesE.DYNAMIC,package=package)
				self.metamodels.add(metamodel)
		return
						
			
	def __LoadResourceTree(self):
		modelfiles = self.__ScanForModelFiles()
		
		for modelfile in modelfiles:
			head,tail = os.path.split(modelfile)
			directory = self.__GetOrCreateDir(head)
			modelResource = ModelResource(name=tail,lastPersistentPath=modelfile)
			#do not load the resource now, do it later on demand
			directory.resources.add(modelResource)
		return
			
	def __InitActions(self):
		#register resource related actions 
		action = ActionInfo(name='load-resource',handler=self,description='Loads model elements from file based resources.')
		action.parameters.add(ActionParameter(name='resource',type='EResource',description='EResource object which contains the file path of the resource to be loaded and which will contain the data afterwards.'))
		action.results.add(ActionParameter(name='resource',type='EResource',description='The resource object that was loaded.'))
		self.actions.add(action)
		
		action = ActionInfo(name='save-resource',handler=self,description='Saves model elements to file based resources.')
		action.parameters.add(ActionParameter(name='resource',type='EResource',description='EResource object which contains the file path of the resource to be saved and which contains the data to be saved.'))
		action.results.add(ActionParameter(name='resource',type='EResource',description='The resource object that was saved.'))
		self.actions.add(action)	
		return
	
	def __GetOrCreateDir(self,path):
		directory = self
		if(path and path != '.'): #only procced for non empty strings
			segments = path.split(os.path.sep)
			for segment in segments: 
				subdirexists = False
				for subdir in directory.subdirectories:
					if(subdir.name == segment):
						directory = subdir
						subdirexists = True
						break
				if(not subdirexists):
					newsubdir = Directory(name=segment)
					directory.subdirectories.add(newsubdir)
					directory = newsubdir
		return directory
	
	def __GetActionHandler(self,actionName):
		for action in self.actions:
			if(action.name == actionName):
				return action.handler
		raise EoqActionError(1,'Action with name %s is unknown.'%(actionName))
		return
	
	#ACTIONS
	def __LoadResource(self,modelResource,transaction):
		if(modelResource.isLoaded):
			return modelResource
		if(modelResource.type == FileResourceTypesE.MODEL):
			resource = self.resourceSet.get_resource(os.path.join(self.baseDir,modelResource.lastPersistentPath)) #neglegt any path changes here, since they manifest on safe
			#self.DoAsTransaction(CommandParser.UpdateCommandStr(self.__EncodeSingleObject(modelResource), '/contents', EmptyValue()), transaction);
			#modelResource.contents.clear()
			contents = list(resource.contents)
			pContents = self.__EncodeObjects(contents)
			vContents = ValueParser.PythonToValue(pContents)
			self.DoAsTransaction(CommandParser.UpdateCommandStr(self.__EncodeSingleObject(modelResource), '/contents', EmptyValue() ), transaction);
			self.DoAsTransaction(CommandParser.UpdateCommandStr(self.__EncodeSingleObject(modelResource), '/contents[+]', vContents ), transaction);
			#for content in resource.contents:
			#	modelResource.contents.add(content)
				
			self.resourceObjectLUT[resource] = modelResource
			#read the contents to the resource object because the containment removes it
			for content in modelResource.contents:
				resource.append(content)
		elif(modelResource.type == FileResourceTypesE.TEXT):
			pass
		elif(modelResource.type == FileResourceTypesE.RAW):
			pass
		
		self.__SetResourceLoaded(modelResource, transaction)
		self.__SetResourceClean(modelResource, transaction)
		#self.DoAsTransaction(CommandParser.UpdateCommandStr(self.__EncodeSingleObject(modelResource), '/isDirty', BoolValue(v=False)), transaction);
		#self.DoAsTransaction(CommandParser.UpdateCommandStr(self.__EncodeSingleObject(modelResource), '/isLoaded', BoolValue(v=True)), transaction);
		
	def __SaveResource(self,modelResource,transaction):
		pathHasChanged = False
		if(modelResource.lastPersistentPath and os.path.normpath(modelResource.lastPersistentPath) != os.path.normpath(modelResource.actualPath())):
			pathHasChanged = True
		if(modelResource.type == FileResourceTypesE.MODEL): 
			resource = self.__GetResourceForModelResource(modelResource)
			if(resource and pathHasChanged): #resource was renamed or moved
				resource.uri = URI(os.path.join(self.baseDir,modelResource.actualPath()))
			if(None == resource): #new resource 
				resource = self.resourceSet.create_resource(os.path.join(self.baseDir,modelResource.actualPath()))
				self.resourceObjectLUT[resource] = modelResource
			#update the content
			self.__ConnectAllResources()
			resource.save()
			self.__DisconnectAllResources()
		elif(modelResource.type == FileResourceTypesE.TEXT):
			pass
		elif(modelResource.type == FileResourceTypesE.RAW):
			pass
		self.__SetResourceLoaded(modelResource, transaction)
		self.__SetResourceClean(modelResource, transaction)
		#self.DoAsTransaction(CommandParser.UpdateCommandStr(self.__EncodeSingleObject(modelResource), '/isDirty', BoolValue(v=False)), transaction);
		#self.DoAsTransaction(CommandParser.UpdateCommandStr(self.__EncodeSingleObject(modelResource), '/isLoaded', BoolValue(v=True)), transaction);
		if(pathHasChanged):
			os.remove(os.path.join(self.baseDir,modelResource.lastPersistentPath))
		#modelResource.lastPersistentPath = modelResource.actualPath()
		newPath = modelResource.actualPath()
		self.__SetResourcePersistentPath(modelResource,newPath,transaction)
		
		#self.DoAsTransaction(CommandParser.UpdateCommandStr(self.__EncodeSingleObject(modelResource), '/lastPersistentPath', StringValue(v=modelResource.actualPath())), transaction);
		
	def __GetResourceForModelResource(self,modelResource):
		resource = None
		if(modelResource.lastPersistentPath):
			resourceUri = URI(os.path.join(self.baseDir,modelResource.lastPersistentPath))
			if(resourceUri.normalize() in self.resourceSet.resources): #existing resource
				resource = self.resourceSet.resources[resourceUri.normalize()]
		return resource
	
	def __GetModelResourceForResource(self,resource):
		try:
			return self.resourceObjectLUT[resource]
		except:
			return None
		
	def __ConnectAllResources(self):
		for resourceUri in self.resourceSet.resources:
			resource = self.resourceSet.resources[resourceUri]
			modelResource = self.__GetModelResourceForResource(resource)
			if(modelResource):
				for content in resource.contents:
					resource.remove(content)
				for content in modelResource.contents:
					resource.append(content)
					#modelResource.contents.discard(content)
				#HACK1: elements must be removed from the Resource in order to make save work
				modelResource.contents.clear()
		
	def __DisconnectAllResources(self):
		for resourceUri in self.resourceSet.resources:
			resource = self.resourceSet.resources[resourceUri]
			modelResource = self.__GetModelResourceForResource(resource)
			if(modelResource):
				#HACK2: now read the content
				for content in resource.contents:
					modelResource.contents.add(content)
				#HACK3: content must be re-added to the resource because eResource() wont work otherwise
				for content in modelResource.contents:
					resource.append(content)
				
	
	def __ResourceObjOfEResource(self,eResource):
		resource = None
		resourceUri = URI(eResource.lastPersistentPath)
		if(resourceUri.normalize() in self.resourceSet.resources):
			resource = self.resourceSet.resources(resourceUri.normalize())
		return resource
	
	def __ECloneClass(self,eObject):
		clazz = eObject.eClass
		clone = clazz()
			
		return clone
	
	def __ECloneAttributes(self,eObject):
		clone = self.__ECloneClass(eObject)
		clazz = eObject.eClass
		attributes = clazz.eAllAttributes()
		for attribute in attributes:
			if(attribute.many):
				for attributeValue in eObject.eGet(attribute):
					clone.eGet(attribute).add(attributeValue)
			else:
				clone.eSet(attribute,eObject.eGet(attribute))	
		return clone
	
	def __ECloneDeep(self,eObject,copyReferences=True):
		clone = self.__ECloneAttributes(eObject)
		clazz = eObject.eClass
		references = clazz.eAllReferences()
		for reference in references:
			if(reference.containment):
				if(reference.many):
					for child in eObject.eGet(reference):
						clonedChild = self.__ECloneDeep(child,copyReferences)
						clone.eGet(reference).add(clonedChild)
				else:
					child = eObject.eGet(reference)
					if(child): #only clone non empty single containments
						clonedChild = self.__ECloneDeep(child,copyReferences)
						clone.eSet(reference,clonedChild)
			elif(copyReferences): #non containments
				if(reference.many):
					for refObj in eObject.eGet(reference):
						clone.eGet(reference).add(refObj)
				else:
					clone.eSet(reference,eObject.eGet(reference))
			
		return clone
	
	def __ECloneFull(self,eObject):
		clone = self.__ECloneDeep(eObject,False)
		clazz = eObject.eClass
		self.__ECloneFullReferenceUpdater(eObject,clone,eObject,clone)			
		return clone
	
	def __ECloneFullReferenceUpdater(self,eObject,clonedEObject,root,clone):
		clazz = eObject.eClass
		references = clazz.eAllReferences()
		for reference in references:
			if(reference.containment):
				if(reference.many):
					nChilds = len(eObject.eGet(reference))
					for i in range(nChilds):
						child = eObject.eGet(reference)[i]
						clonedChild = clonedEObject.eGet(reference)[i]
						self.__ECloneFullReferenceUpdater(child, clonedChild, root, clone)
				else:
					child = eObject.eGet(reference)
					if(child): #only clone non empty single containments
						clonedChild = clonedEObject.eGet(reference)
						self.__ECloneFullReferenceUpdater(child, clonedChild, root, clone)
			else: #non containments
				if(reference.many):
					for oldRef in eObject.eGet(reference):
						newRef = self.__ECloneFullFindCorrespondingReference(oldRef,root,clone)
						clonedEObject.eGet(reference).add(newRef)
				else:
					oldRef = eObject.eGet(reference)
					if(oldRef): #null references need no cloning
						newRef = self.__ECloneFullFindCorrespondingReference(oldRef,root,clone)
						clonedEObject.eSet(reference,newRef)
		return clone
	
	def __ECloneFullFindCorrespondingReference(self,oldRef,root,clone):
		newRef = oldRef
		if(self.__ECloneFullIsParentOf(oldRef,root)): #we only need an new reference if the root contains the referred object
			featurePath = self.__ECloneFullGetPathFromTo(root,oldRef)
			newRef = clone
			for p in featurePath: #p is a tuple (featureName, many, index)
				feature = p[0]
				if(p[1]): #many
					index = p[2]
					newRef = newRef.eGet(feature)[index]
				else: #single
					newRef = newRef.eGet(feature)
		return newRef
	
	def __ECloneFullIsParentOf(self,child,possibleParent):
		if(child == possibleParent) :
			return True
		parent = child.eContainer()
		if(parent and isinstance(parent, EObject)):
			return self.__ECloneFullIsParentOf(parent, possibleParent)
		return False #has no parent any more, return false
	
	def __ECloneFullGetPathFromTo(self,anchestor,child):
		featurePath = []
		if(anchestor!=child):
			parent = child.eContainer()
			if(parent and isinstance(parent, EObject)):
				feature = child.eContainmentFeature()
				featureName = feature.name
				many = feature.many
				index = 0
				if(many):
					index = parent.eGet(featureName).index(child)
				featurePath = [(featureName,many,index)]
				featurePath = self.__ECloneFullGetPathFromTo(anchestor,parent) + featurePath
		return featurePath #has no parent any more, return false
			
				
				