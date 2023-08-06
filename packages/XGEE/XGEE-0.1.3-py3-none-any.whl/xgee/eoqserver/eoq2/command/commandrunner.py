from .command import CmdTypes, MrgModes
from .result import Res,ResTypes
from .diff import DifferenceFinder
from ..query.query import Qry,Obj,ObjSeg
from ..query.queryrunner import QryRunner
from ..util.error import EoqError
from ..action import CmdRunnerBasedCallManager
from ..event.event import EvtProvider,ChgEvt,ChgTypes,ALL_EVENT_TYPES
from ..util.util import IsListOfObjects,IsNoList,IsList,ApplyToAllElements
from ..util.logger import NoLogging
from ..util.benchmark import Benchmark
from ..serialization.jsonserializer import JsonSerializer
from ..serialization.textserializer import TextSerializer
from ..validation.validation import ValidationManager

from datetime import time
from uuid import uuid4

import traceback


class Session:
    def __init__(self,sessionId,sessionNumber):
        self.sessionId = sessionId
        self.sessionNumber = sessionNumber
        self.user = None
        self.begin = time
        self.isTemp = False
        #initialize event table
        self.events = {} #lists the events this session is observing as 
        for e in ALL_EVENT_TYPES:
            self.events[e] = {} #indicates to listen to no key at all
            
class Transaction:
    def __init__(self,tid):
        self.tid = tid
        self.session = None
        self.changes = [] #dictionary which collects changes until the transaction is finished
        self.history = []
        self.isMuted = False
        
'''
 Cmd Runner
'''   
class CmdRunner(EvtProvider):
    def __init__(self,mdbAccessor,maxChanges=10000,logger=NoLogging(),enableBenchmark=False):
        super().__init__()
        self.mdbAccessor = mdbAccessor
        self.maxChanges = maxChanges #the number of changes that are preserved
        #logging
        self.logger = logger
        self.enableBenchmark = enableBenchmark
        self.logSerializer = JsonSerializer()
        #validation
        self.validationManager = ValidationManager(self)
        self.textSerializer = TextSerializer()
        #initialize internals
        self.latestTransactionId = 0
        self.sessionCount = 0
        self.transactions = {}
        #sessions
        self.sessions = {} #dict containing sessions keys and related session informations
        #changes
        self.earliestChangeId = 0
        self.latestChangeId = 0
        self.changes = {}
        #query runner
        self.qryEvaluator = QryRunner(self.mdbAccessor,self.validationManager,enableBenchmark=enableBenchmark)
        self.callManager = CmdRunnerBasedCallManager(self)        
        #init command evaluators functor table
        self.cmdEvaluators = {}
        self.cmdEvaluators[CmdTypes.GET] = self.ExecGet
        self.cmdEvaluators[CmdTypes.SET] = self.ExecSet
        self.cmdEvaluators[CmdTypes.ADD] = self.ExecAdd
        self.cmdEvaluators[CmdTypes.REM] = self.ExecRem
        self.cmdEvaluators[CmdTypes.MOV] = self.ExecMov
        self.cmdEvaluators[CmdTypes.CLO] = self.ExecClo
        self.cmdEvaluators[CmdTypes.CRT] = self.ExecCrt
        self.cmdEvaluators[CmdTypes.CRN] = self.ExecCrn
        self.cmdEvaluators[CmdTypes.QRF] = self.ExecQrf
        self.cmdEvaluators[CmdTypes.CPR] = self.ExecCpr
        self.cmdEvaluators[CmdTypes.MRG] = self.ExecMrg
        self.cmdEvaluators[CmdTypes.STS] = self.ExecSts
        self.cmdEvaluators[CmdTypes.GMM] = self.ExecGmm
        self.cmdEvaluators[CmdTypes.RMM] = self.ExecRmm
        self.cmdEvaluators[CmdTypes.UMM] = self.ExecUmm
        self.cmdEvaluators[CmdTypes.GAA] = self.ExecGaa
        self.cmdEvaluators[CmdTypes.HEL] = self.ExecHel
        self.cmdEvaluators[CmdTypes.SES] = self.ExecSes
        self.cmdEvaluators[CmdTypes.GBY] = self.ExecGby
        self.cmdEvaluators[CmdTypes.CHG] = self.ExecChg
        self.cmdEvaluators[CmdTypes.OBS] = self.ExecObs
        self.cmdEvaluators[CmdTypes.UBS] = self.ExecUbs
        self.cmdEvaluators[CmdTypes.CAL] = self.ExecCal
        self.cmdEvaluators[CmdTypes.ASC] = self.ExecAsc
        self.cmdEvaluators[CmdTypes.ABC] = self.ExecAbc
        self.cmdEvaluators[CmdTypes.ADC] = self.ExecAdc
        self.cmdEvaluators[CmdTypes.RMC] = self.ExecRmc
        self.cmdEvaluators[CmdTypes.VAL] = self.ExecVal
        self.cmdEvaluators[CmdTypes.GAC] = self.ExecGac
        self.cmdEvaluators[CmdTypes.CMP] = self.ExecCmp
        self.cmdEvaluators[CmdTypes.MUT] = self.ExecMut
        self.cmdEvaluators[CmdTypes.UMT] = self.ExecUmt
        
        #start listening to external events
        if(self.mdbAccessor):
            self.mdbAccessor.Observe(self.OnCallMdbAccessorEvent)
        if(self.callManager):
            self.callManager.Observe(self.OnCallManagerEvent)
            
        #benchmark
        if(self.enableBenchmark):
            self.benchmark = Benchmark()
            allCmdTypes = [getattr(CmdTypes,k) for k in CmdTypes.__dict__ if not k.startswith('_')]
            for t in allCmdTypes:
                self.benchmark.InitMessure(t)


        # merge / diff
        self.oldRoot = None
        self.newRoot = None
        self.postponedMergeReferences = []
        self.diffcommands = []
        self.mDummies = 1
        
    '''
    COMMAND EXECUTION
    '''
    
    def Exec(self,cmd,sessionId=None):
        res = None
        try:
            tid = self.StartTransaction(sessionId)
            res = self.ExecOnTransaction(cmd,tid)
        except Exception as e: 
            errorMsg = "Command %s failed: %s"%(self.logSerializer.Ser(cmd),str(e))
            self.logger.Error(errorMsg)
            traceback.print_exc()
            res = Res(cmd.cmd,ResTypes.ERR,str(e),tid,self.latestChangeId)     
        self.EndTransaction(res,tid)
        return res
    
    def ExecOnTransaction(self,cmd,tid):
        self.logger.PassivatableLog('transaction',lambda : self.logSerializer.Ser(cmd))
        cmdType = cmd.cmd
        try:
            evaluator = self.cmdEvaluators[cmdType]
        except KeyError:
            raise EoqError(0,"Error evaluating command: Unknown command type: %s."%(cmd.cmd))
        if self.enableBenchmark: self.benchmark.Start()
        try:
            res = evaluator(cmd.a,tid)
        except Exception as e: 
            if self.enableBenchmark: self.benchmark.Stop(cmdType)
            raise e #forward exception
        if self.enableBenchmark: self.benchmark.Stop(cmdType)
        self.logger.PassivatableLog('transaction',lambda: self.logSerializer.Ser(res))
        return res
    
    def ExecCmp(self,args,tid):
        transaction = self.GetTransaction(tid)
        status = ResTypes.OKY
        subresults = []
        n = 0;
        for cmd in args:
            n = n+1;
            try:
                subresult = self.ExecOnTransaction(cmd, tid) 
                if(transaction.isMuted):
                    subresult.v = None #cut of the output, but it is still in the history
                subresults.append(subresult)
            except Exception as e:
                raise EoqError(0,"Sub command %d failed: %s"%(n,str(e)))
        return Res(CmdTypes.CMP,status,subresults,tid,self.latestChangeId)
    
    def ExecMut(self,args,tid):
        transaction = self.GetTransaction(tid)
        transaction.isMuted = True
        res = True
        self.AddToHistory(res,tid)
        return Res(CmdTypes.MUT,ResTypes.OKY,res,tid,self.latestChangeId)
    
    def ExecUmt(self,args,tid):
        transaction = self.GetTransaction(tid)
        transaction.isMuted = False
        res = True
        self.AddToHistory(res,tid)
        return Res(CmdTypes.MUT,ResTypes.OKY,res,tid,self.latestChangeId)
            
    def ExecGet(self,args,tid):
        status = ResTypes.OKY
        target = args
        history = self.GetHistory(tid)
        res = self.qryEvaluator.Eval(target,history)
        self.AddToHistory(res,tid)
        #result = []
        #if not(isinstance(res, list)):
            #res = [res]
        #for constraint in res:
            #try:
                #result.append([constraint.constraintType, constraint.target, constraint.feature, constraint.law, constraint.name, constraint.annotation])
            #except:
                #result.append(constraint)
        if isinstance(res,list):
            res = self.ChangeConstrainttoList(res)
        return Res(CmdTypes.GET,status,res,tid,self.latestChangeId)
    
    def ExecSet(self,args,tid):
        status = ResTypes.OKY
        #res = None  #[target,feature,oldVal]
        cid = self.latestChangeId
        #eval all arguments
        history = self.GetHistory(tid)
        target = self.qryEvaluator.Eval(args[0],history)
        feature = self.qryEvaluator.Eval(args[1],history)
        value = self.qryEvaluator.Eval(args[2],history)
        
        #set the value(s) depending on the multiplicity of the arguments
        if(IsNoList(target)): # e.g. #20
            if(IsNoList(feature)):
                (oldVal,oldOwner,oldFeature,oldIndex) = self.mdbAccessor.Set(target,feature,value)
                cid = self.AddLocalChange(tid,ChgTypes.SET,target,feature,value,oldVal,oldOwner,oldFeature,oldIndex)
                self.Val(target, tid)
            elif(IsListOfObjects(feature)):
                if(IsNoList(value)):
                    for f in feature:
                        (oldVal,oldOwner,oldFeature,oldIndex) = self.mdbAccessor.Set(target,f,value)
                        cid = self.AddLocalChange(tid,ChgTypes.SET,target,f,value,oldVal,oldOwner,oldFeature,oldIndex)
                        self.Val(target, tid)
                elif(IsListOfObjects(value) and len(value) == len(feature)):
                    for i in range(len(feature)):
                        (oldVal,oldOwner,oldFeature,oldIndex) = self.mdbAccessor.Set(target,feature[i],value[i])
                        cid = self.AddLocalChange(tid,ChgTypes.SET,target,feature[i],value[i],oldVal,oldOwner,oldFeature,oldIndex)
                        self.Val(target, tid)
                else:
                    raise EoqError(0,'Error in set: value must be single value or list of values with equal length of the number of features, but got: %s:'%(value)) 
            else:
                raise EoqError(0,'Error in set: feature must be single object or list of objects but got: %s:'%(feature)) 
        elif(IsListOfObjects(target)): # e.g. [#20,#22,#23]
            if(IsNoList(feature)):
                if(IsNoList(value)):
                    for t in target:
                        (oldVal,oldOwner,oldFeature,oldIndex) = self.mdbAccessor.Set(t,feature,value)
                        cid = self.AddLocalChange(tid,ChgTypes.SET,t,feature,value,oldVal,oldOwner,oldFeature,oldIndex)
                        self.Val(t, tid)
                elif(IsListOfObjects(value) and len(value) == len(target)):
                    for i in range(len(target)):
                        (oldVal,oldOwner,oldFeature,oldIndex) = self.mdbAccessor.Set(target[i],feature,value[i])
                        cid = self.AddLocalChange(tid,ChgTypes.SET,target[i],feature,value[i],oldVal,oldOwner,oldFeature,oldIndex)
                        self.Val(target[i], tid)
                else:
                    raise EoqError(0,'Error in set: value must be single value or list of values with equal length of the number of targets, but got: %s:'%(value)) 
            elif(IsListOfObjects(feature)):
                if(IsNoList(value)):
                    for t in target:
                        for f in feature:
                            (oldVal,oldOwner,oldFeature,oldIndex) = self.mdbAccessor.Set(t,f,value)
                            cid = self.AddLocalChange(tid,ChgTypes.SET,t,f,value,oldVal,oldOwner,oldFeature,oldIndex)
                            self.Val(t, tid)
                elif(IsListOfObjects(value) and len(value) == len(feature)):
                    for t in target:
                        for i in range(len(feature)):
                            (oldVal,oldOwner,oldFeature,oldIndex) = self.mdbAccessor.Set(t,feature[i],value[i])
                            cid = self.AddLocalChange(tid,ChgTypes.SET,t,feature[i],value[i],oldVal,oldOwner,oldFeature,oldIndex)
                            self.Val(t, tid)
                elif(IsList(value) and len(value) == len(target)):
                    for j in range(len(target)):
                        if(IsListOfObjects(value[j]) and len(value[j]) == len(feature)):
                            for i in range(len(feature)):
                                (oldVal,oldOwner,oldFeature,oldIndex) = self.mdbAccessor.Set(target[j],feature[i],value[j][i])
                                cid = self.AddLocalChange(tid,ChgTypes.SET,target[j],feature[i],value[j][i],oldVal,oldOwner,oldFeature,oldIndex)
                                self.Val(target[j], tid)
                        else:
                            raise EoqError(0,'Error in set: for multiple targets and multiple features the value for each entry must have the same length as the number of features. Expected %d entries for target %d, but got %d.'%(len(feature),j,len(value[j])))
                else:
                    raise EoqError(0,'Error in set: value must be single value or list of values with equal length of the number of targets, but got: %s:'%(value)) 
            else:
                raise EoqError(0,'Error in set: feature must be single object or list of objects but got: %s:'%(feature)) 
        else: 
            raise EoqError(0,'Error in set: target must be single object or list of objects but got: %s:'%(target))
        
        res = [target,feature,value]
        self.AddToHistory(res,tid)
        return Res(CmdTypes.SET,status,res,tid,cid)
    
    def ExecAdd(self,args,tid):
        status = ResTypes.OKY
        #res = None  
        cid = self.latestChangeId
        #eval all arguments
        history = self.GetHistory(tid)
        target = self.qryEvaluator.Eval(args[0],history)
        feature = self.qryEvaluator.Eval(args[1],history)
        value = self.qryEvaluator.Eval(args[2],history)
        # reset the validation cache since the model is changed
        self.validationManager.ClearCache()
        
        #set the value(s) depending on the multiplicity of the arguments
        if(IsNoList(target)): # e.g. #20
            if(IsNoList(feature)):
                if(IsNoList(value)):
                    (oldVal,oldOwner,oldFeature,oldIndex) = self.mdbAccessor.Add(target,feature,value)
                    cid = self.AddLocalChange(tid,ChgTypes.ADD,target,feature,value,oldVal,oldOwner,oldFeature,oldIndex)
                    self.Val(target, tid)
                elif(IsList(value)):
                    for v in value:
                        (oldVal,oldOwner,oldFeature,oldIndex) = self.mdbAccessor.Add(target,feature,v)
                        cid = self.AddLocalChange(tid,ChgTypes.ADD,target,feature,v,oldVal,oldOwner,oldFeature,oldIndex)
                        self.Val(target, tid)
                else:
                    raise EoqError(0,'Error in add: value must be single value or list of values, but got: %s:'%(value)) 
            elif(IsListOfObjects(feature)):
                if(IsNoList(value)):
                    for f in feature:
                        (oldVal,oldOwner,oldFeature,oldIndex) = self.mdbAccessor.Add(target,f,value)
                        cid = self.AddLocalChange(tid,ChgTypes.ADD,target,f,value,oldVal,oldOwner,oldFeature,oldIndex)
                        self.Val(target, tid)
                elif(IsList(value) and len(value) == len(feature)):
                    for i in range(len(feature)):
                        if(IsListOfObjects(value[i])):
                            for v in value[i]:
                                (oldVal,oldOwner,oldFeature,oldIndex) = self.mdbAccessor.Add(target,feature[i],v)
                                cid = self.AddLocalChange(tid,ChgTypes.ADD,target,feature[i],v,oldVal,oldOwner,oldFeature,oldIndex)
                                self.Val(target, tid)
                        else:
                            raise EoqError(0,'Error in add: for multiple features the value must be a list of list of objects for each feature, but entry %d is %s.'%(i,value[i]))
                else:
                    raise EoqError(0,'Error in add: value must be single value or list of list of values with outer list having a length equal to the number of features, but got: %s:'%(value)) 
            else:
                raise EoqError(0,'Error in add: feature must be single object or list of objects but got: %s:'%(feature)) 
        elif(IsListOfObjects(target)): # e.g. [#20,#22,#23]
            if(IsNoList(feature)):
                if(IsNoList(value)):
                    for t in target:
                        (oldVal,oldOwner,oldFeature,oldIndex) = self.mdbAccessor.Add(t,feature,value)
                        cid = self.AddLocalChange(tid,ChgTypes.ADD,t,feature,value,oldVal,oldOwner,oldFeature,oldIndex)
                        self.Val(t, tid)
                elif(IsList(value) and len(value) == len(target)):
                    for j in range(len(target)):
                        if(IsListOfObjects(value[j])):
                            for i in range(len(value[j])):
                                (oldVal,oldOwner,oldFeature,oldIndex) = self.mdbAccessor.Add(target[j],feature,value[j][i])
                                cid = self.AddLocalChange(tid,ChgTypes.ADD,target[j],feature,value[j][i],oldVal,oldOwner,oldFeature,oldIndex)
                                self.Val(target[j], tid)
                        else:
                            raise EoqError(0,'Error in add: for multiple targets the value must be a list of list of objects for each target, but entry %d is %s.'%(j,value[j]))
                else:
                    raise EoqError(0,'Error in add: value must be single value or list of list of values with the outer list having a length equal to the number of targets, but got: %s:'%(value)) 
            elif(IsListOfObjects(feature)):
                if(IsNoList(value)):
                    for t in target:
                        for f in feature:
                            (oldVal,oldOwner,oldFeature,oldIndex) = self.mdbAccessor.Add(t,f,value)
                            cid = self.AddLocalChange(tid,ChgTypes.ADD,t,f,value,oldVal,oldOwner,oldFeature,oldIndex)
                            self.Val(t, tid)
                elif(IsListOfObjects(value) and len(value) == len(feature)):
                    for t in target:
                        for i in range(len(feature)):
                            (oldVal,oldOwner,oldFeature,oldIndex) = self.mdbAccessor.Add(t,feature[i],value[i])
                            cid = self.AddLocalChange(tid,ChgTypes.ADD,t,feature[i],value[i],oldVal,oldOwner,oldFeature,oldIndex)
                            self.Val(t, tid)
                elif(IsList(value) and len(value) == len(target)):
                    for j in range(len(target)):
                        if(IsListOfObjects(value[j]) and len(value[j]) == len(feature)):
                            for i in range(len(feature)):
                                (oldVal,oldOwner,oldFeature,oldIndex) = self.mdbAccessor.Add(target[j],feature[i],value[j][i])
                                cid = self.AddLocalChange(tid,ChgTypes.ADD,target[j],feature[i],value[j][i],oldVal,oldOwner,oldFeature,oldIndex)
                                self.Val(target[j], tid)
                        elif(IsList(value[j]) and len(value[j]) == len(feature)):
                            for i in range(len(feature)):
                                if(IsList(value[j][i])):
                                    for v in value[j][i]:
                                        (oldVal,oldOwner,oldFeature,oldIndex) = self.mdbAccessor.Add(target[j],feature[i],v)
                                        cid = self.AddLocalChange(tid,ChgTypes.ADD,target[j],feature[i],v,oldVal,oldOwner,oldFeature,oldIndex)
                                        self.Val(target[j], tid)
                                else:
                                    raise EoqError(0,'Error in add: for multiple targets, multiple features and multiple values value must list equal to targets containing a list equal to features containing a list of values, but got %s for target %d and feature %d.'%(value[j][i],j,i)) 
                        else:
                            raise EoqError(0,'Error in add: for multiple targets and multiple features the value for each entry must have the same length as the number of features. Expected %d entries for target %d, but got %s.'%(len(feature),j,value[j]))
                else:
                    raise EoqError(0,'Error in add: value must be single value or list of list of list of values with outer list having a length equal to the number of targets and the middle list with a length equal to the number of features, but got: %s:'%(value)) 
            else:
                raise EoqError(0,'Error in add: feature must be single object or list of objects but got: %s:'%(feature)) 
        else: 
            raise EoqError(0,'Error in add: target must be single object or list of objects but got: %s:'%(target))
        
        res = [target,feature,value]
        self.AddToHistory(res,tid)
        return Res(CmdTypes.ADD,status,res,tid,cid)
    
    def ExecRem(self,args,tid):
        status = ResTypes.OKY
        #res = None  
        cid = self.latestChangeId
        #eval all arguments
        history = self.GetHistory(tid)
        target = self.qryEvaluator.Eval(args[0],history)
        feature = self.qryEvaluator.Eval(args[1],history)
        value = self.qryEvaluator.Eval(args[2],history)
        # reset the validation cache since the model is changed
        self.validationManager.ClearCache()
        
        #set the value(s) depending on the multiplicity of the arguments
        if(IsNoList(target)): # e.g. #20
            if(IsNoList(feature)):
                if(IsNoList(value)):
                    (oldVal,oldOwner,oldFeature,oldIndex) = self.mdbAccessor.Remove(target,feature,value)
                    cid = self.AddLocalChange(tid,ChgTypes.REM,target,feature,value,oldVal,oldOwner,oldFeature,oldIndex)
                    self.Val(target, tid)
                elif(IsList(value)):
                    for v in value:
                        (oldVal,oldOwner,oldFeature,oldIndex) = self.mdbAccessor.Remove(target,feature,v)
                        cid = self.AddLocalChange(tid,ChgTypes.REM,target,feature,v,oldVal,oldOwner,oldFeature,oldIndex)
                        self.Val(target, tid)
                else:
                    raise EoqError(0,'Error in remove: value must be single value or list of values, but got: %s:'%(value)) 
            elif(IsListOfObjects(feature)):
                if(IsNoList(value)):
                    for f in feature:
                        (oldVal,oldOwner,oldFeature,oldIndex) = self.mdbAccessor.Remove(target,f,value)
                        cid = self.AddLocalChange(tid,ChgTypes.REM,target,f,value,oldVal,oldOwner,oldFeature,oldIndex)
                        self.Val(target, tid)
                elif(IsList(value) and len(value) == len(feature)):
                    for i in range(len(feature)):
                        if(IsListOfObjects(value[i])):
                            for v in value[i]:
                                (oldVal,oldOwner,oldFeature,oldIndex) = self.mdbAccessor.Remove(target,feature[i],v)
                                cid = self.AddLocalChange(tid,ChgTypes.REM,target,feature[i],v,oldVal,oldOwner,oldFeature,oldIndex)
                                self.Val(target, tid)
                        else:
                            raise EoqError(0,'Error in remove: for multiple features the value must be a list of list of objects for each feature, but entry %d is %s.'%(i,value[i]))
                else:
                    raise EoqError(0,'Error in remove: value must be single value or list of list of values with outer list having a length equal to the number of features, but got: %s:'%(value)) 
            else:
                raise EoqError(0,'Error in remove: feature must be single object or list of objects but got: %s:'%(feature)) 
        elif(IsListOfObjects(target)): # e.g. [#20,#22,#23]
            if(IsNoList(feature)):
                if(IsNoList(value)):
                    for t in target:
                        (oldVal,oldOwner,oldFeature,oldIndex) = self.mdbAccessor.Remove(t,feature,value)
                        cid = self.AddLocalChange(tid,ChgTypes.REM,t,feature,value,oldVal,oldOwner,oldFeature,oldIndex)
                        self.Val(t, tid)
                elif(IsList(value) and len(value) == len(target)):
                    for j in range(len(target)):
                        if(IsListOfObjects(value[j])):
                            for i in range(len(value[j])):
                                (oldVal,oldOwner,oldFeature,oldIndex) = self.mdbAccessor.Remove(target[j],feature,value[j][i])
                                cid = self.AddLocalChange(tid,ChgTypes.REM,target[j],feature,value[j][i],oldVal,oldOwner,oldFeature,oldIndex)
                                self.Val(target[j], tid)
                        else:
                            raise EoqError(0,'Error in add: for multiple targets the value must be a list of list of objects for each target, but entry %d is %s.'%(j,value[j]))
                else:
                    raise EoqError(0,'Error in remove: value must be single value or list of list of values with the outer list having a length equal to the number of targets, but got: %s:'%(value)) 
            elif(IsListOfObjects(feature)):
                if(IsNoList(value)):
                    for t in target:
                        for f in feature:
                            (oldVal,oldOwner,oldFeature,oldIndex) = self.mdbAccessor.Remove(t,f,value)
                            cid = self.AddLocalChange(tid,ChgTypes.REM,t,f,value,oldVal,oldOwner,oldFeature,oldIndex)
                            self.Val(t, tid)
                elif(IsListOfObjects(value) and len(value) == len(feature)):
                    for t in target:
                        for i in range(len(feature)):
                            (oldVal,oldOwner,oldFeature,oldIndex) = self.mdbAccessor.Remove(t,feature[i],value[i])
                            cid = self.AddLocalChange(tid,ChgTypes.REM,t,feature[i],value[i],oldVal,oldOwner,oldFeature,oldIndex)
                            self.Val(t, tid)
                elif(IsList(value) and len(value) == len(target)):
                    for j in range(len(target)):
                        if(IsListOfObjects(value[j]) and len(value[j]) == len(feature)):
                            for i in range(len(feature)):
                                (oldVal,oldOwner,oldFeature,oldIndex) = self.mdbAccessor.Remove(target[j],feature[i],value[j][i])
                                cid = self.AddLocalChange(tid,ChgTypes.REM,target[j],feature[i],value[j][i],oldVal,oldOwner,oldFeature,oldIndex)
                                self.Val(target[j], tid)
                        elif(IsList(value[j]) and len(value[j]) == len(feature)):
                            for i in range(len(feature)):
                                if(IsList(value[j][i])):
                                    for v in value[j][i]:
                                        (oldVal,oldOwner,oldFeature,oldIndex) = self.mdbAccessor.Remove(target[j],feature[i],v)
                                        cid = self.AddLocalChange(tid,ChgTypes.REM,target[j],feature[i],v,oldVal,oldOwner,oldFeature,oldIndex)
                                        self.Val(target[j], tid)
                                else:
                                    raise EoqError(0,'Error in remove: for multiple targets, multiple features and multiple values value must list equal to targets containing a list equal to features containing a list of values, but got %s for target %d and feature %d.'%(value[j][i],j,i))
                        else:
                            raise EoqError(0,'Error in remove: for multiple targets and multiple features the value for each entry must have the same length as the number of features. Expected %d entries for target %d, but got %d.'%(len(feature),j,value[j]))
                else:
                    raise EoqError(0,'Error in remove: value must be single value or list of list of list of values with outer list having a lenght equal to the number of targets and the middle list with a length equal to the number of features, but got: %s:'%(value)) 
            else:
                raise EoqError(0,'Error in remove: feature must be single object or list of objects but got: %s:'%(feature)) 
        else: 
            raise EoqError(0,'Error in remove: target must be single object or list of objects but got: %s:'%(target))
        
        res = [target,feature,value]
        self.AddToHistory(res,tid)
        return Res(CmdTypes.REM,status,res,tid,cid)
    
    
    def ExecMov(self,args,tid):
        status = ResTypes.OKY
        #res = None  #[target,feature,oldVal]
        cid = self.latestChangeId
        #eval all arguments
        history = self.GetHistory(tid)
        target = self.qryEvaluator.Eval(args[0],history)
        newIndex = self.qryEvaluator.Eval(args[1],history)
        
        #set the value(s) depending on the multiplicity of the arguments
        if(IsNoList(target)): # e.g. #20
            if(IsNoList(newIndex)):
                (oldVal,oldOwner,oldFeature,oldIndex) = self.mdbAccessor.Move(target,newIndex)
                cid = self.AddLocalChange(tid,ChgTypes.MOV,target,oldFeature,newIndex,oldVal,oldOwner,oldFeature,oldIndex)
                self.Val(target, tid)
            else:
                raise EoqError(0,'Error in move: new index must be an integer, but got: %s:'%(newIndex)) 
        elif(IsListOfObjects(target)): # e.g. [#20,#22,#23]
            if(IsNoList(newIndex)):
                for t in target:
                    (oldVal,oldOwner,oldFeature,oldIndex) = self.mdbAccessor.Move(t,newIndex)
                    cid = self.AddLocalChange(tid,ChgTypes.MOV,t,oldFeature,newIndex,oldVal,oldOwner,oldFeature,oldIndex)
                    self.Val(t, tid)
            elif(IsListOfObjects(newIndex) and len(newIndex) == len(target)):
                for i in range(len(target)):
                    (oldVal,oldOwner,oldFeature,oldIndex) = self.mdbAccessor.Move(target[i],newIndex[i])
                    cid = self.AddLocalChange(tid,ChgTypes.MOV,target[i],oldFeature,newIndex[i],oldVal,oldOwner,oldFeature,oldIndex)
                    self.Val(target[i], tid)
            else:
                raise EoqError(0,'Error in move: new index must be single value or list of values with equal length of the number of targets, but got: %s:'%(newIndex)) 
        else: 
            raise EoqError(0,'Error in move: target must be single object or list of objects but got: %s:'%(target))
        
        res = [target,newIndex]
        self.AddToHistory(res,tid)
        return Res(CmdTypes.MOV,status,res,tid,cid)
    
    
    def ExecClo(self,args,tid):
        status = ResTypes.OKY
        #res = None  
        history = self.GetHistory(tid)
        target = self.qryEvaluator.Eval(args[0],history)
        mode = self.qryEvaluator.Eval(args[1],history)
        if(IsNoList(target)): # e.g. #20
            if(IsNoList(mode)):
                res = self.mdbAccessor.Clone(target,mode)
            else:
                raise EoqError(0,'Error in clone: mode must be a string, but got: %s:'%(mode)) 
        elif(IsListOfObjects(target)): # e.g. [#20,#22,#23]
            if(IsNoList(mode)):
                res = [self.mdbAccessor.Clone(t,mode) for t in target]
            elif(IsListOfObjects(mode) and len(mode) == len(target)):
                res = [self.mdbAccessor.Clone(target[i],mode[i]) for i in range(len(target))]
            else:
                raise EoqError(0,'Error in clone: mode must be a string or a list of strings, but got: %s:'%(mode)) 
        else:
            raise EoqError(0,'Error in clone: target must be an object or a list of objects, but got: %s:'%(target)) 
        self.AddToHistory(res,tid)
        return Res(CmdTypes.CLO,status,res,tid,self.latestChangeId)

    def ExecMrg(self, args, tid):
        '''
        Merges all changes from file 'new' onto file 'old'.
        '''
        status = ResTypes.OKY
        res = self.ExecCpr(args, tid)
        cmds = res.GetValue()
        # execute commands
        for cmd in cmds:
            self.ExecOnTransaction(cmd, tid)
        return Res(CmdTypes.MRG, status, res, tid, self.latestChangeId)

    def ExecCpr(self, args, tid):
        '''
        Creates a list with all the necessary commands to adapt 
        the old object to the new one.
        '''
        status = ResTypes.OKY
        res = None
        history = self.GetHistory(tid)
        old     = self.qryEvaluator.Eval(args[0], history) # old file
        new     = self.qryEvaluator.Eval(args[1], history) # new file
        mrgMode = self.qryEvaluator.Eval(args[2], history) # new file
        if IsList(old) or IsList(new):
            raise EoqError(0,'Error in Diff/Merge: No Lists allowed.')
        # init diff.py
        differenceFinder = DifferenceFinder(self, self.mdbAccessor, 
            old, new, tid, mrgMode, logger = self.logger)
        if mrgMode == MrgModes.DET:
            differenceFinder.CreateObjectOverviewFile()
        # start diff.py
        differenceFinder.Run()
        # obtain commands
        res = differenceFinder.GetCommands()
        # serialize commands
        if mrgMode in [MrgModes.LST, MrgModes.LOG, MrgModes.DET]:
            path = 'log/cmdList_{}_{}.txt'.format(old, new)
            with open(path, 'w') as file:
                file.write('### Commands to merge {} onto {} ###\n'.format(new, old))
                for cmd in res:
                    file.write(self.logSerializer.Ser(cmd))
                    file.write('\n')
        return Res(CmdTypes.CPR, status, res, tid, self.latestChangeId)
    
    def ExecCrt(self,args,tid):
        status = ResTypes.OKY
        #res = None  
        history = self.GetHistory(tid)
        clazz = self.qryEvaluator.Eval(args[0],history)
        n = self.qryEvaluator.Eval(args[1],history)
        constructorArgs = self.qryEvaluator.Eval(args[2],history)
        #constructorArgs = [self.qryEvaluator.Eval(a,history) for a in args[2]]
        if(IsNoList(clazz)): # e.g. #20
            if(IsNoList(n)):
                res = self.mdbAccessor.Create(clazz,n,constructorArgs)
            else:
                raise EoqError(0,'Error in create: n must be a positive integer, but got: %s:'%(n)) 
        else:
            raise EoqError(0,'Error in create: clazz must be an object of type class, but got: %s:'%(clazz)) 
        self.AddToHistory(res,tid)
        return Res(CmdTypes.CRT,status,res,tid,self.latestChangeId)
    
    def ExecCrn(self,args,tid):
        status = ResTypes.OKY
        #res = None  
        history = self.GetHistory(tid)
        packageName = self.qryEvaluator.Eval(args[0],history)
        className = self.qryEvaluator.Eval(args[1],history)
        n = self.qryEvaluator.Eval(args[2],history)
        constructorArgs = self.qryEvaluator.Eval(args[3],history)
        #constructorArgs = [self.qryEvaluator.Eval(a,history) for a in args[3]]
        if(IsNoList(packageName) and IsNoList(className)): # e.g. #20
            if(IsNoList(n)):
                res = self.mdbAccessor.CreateByName(packageName,className,n,constructorArgs)
            else:
                raise EoqError(0,'Error in create: n must be a positive integer, but got: %s:'%(n)) 
        else:
            raise EoqError(0,'Error in create: packageName and className must be strings, but got: %s, %s:'%(packageName,className)) 
        self.AddToHistory(res,tid)
        return Res(CmdTypes.CRN,status,res,tid,self.latestChangeId)
    
    def ExecQrf(self,args,tid):
        def qrfFunctor(a):
            res = None
            if(isinstance(a,ObjSeg)):
                #traverse the path backwards from the object to the root
                pathFromParent = []
                c = a
                p = self.mdbAccessor.GetParent(c)
                while(p):
                    f = self.mdbAccessor.GetContainingFeature(c)
                    n = self.mdbAccessor.Get(f,'name')
                    i = self.mdbAccessor.GetIndex(c)
                    pathFromParent.append((n,i))
                    #go one level back, i.e. the new parent is the parent of the old
                    c = p
                    p = self.mdbAccessor.GetParent(c)
                #build a query that leads to the object
                res = Qry()
                for segment in reversed(pathFromParent):
                    n = segment[0]
                    i = segment[1]
                    if(None==i):
                        res.Pth(n)
                    else:
                        res.Pth(n).Idx(i)
            else:
                res = a 
            return res
        
        status = ResTypes.OKY
        target = args
        history = self.GetHistory(tid)
        elements = self.qryEvaluator.Eval(target,history)
        
        res = ApplyToAllElements(elements, qrfFunctor)
        
        self.AddToHistory(res,tid)
        return Res(CmdTypes.GET,status,res,tid,self.latestChangeId)
    
    def ExecGmm(self,args,tid):
        status = ResTypes.OKY
        #res = None  
        res = self.mdbAccessor.GetAllMetamodels()
        self.AddToHistory(res,tid)
        return Res(CmdTypes.GMM,status,res,tid,self.latestChangeId)
    
    def ExecRmm(self,args,tid):
        status = ResTypes.OKY
        #res = None  
        history = self.GetHistory(tid)
        package = self.qryEvaluator.Eval(args,history) 
        res = self.mdbAccessor.RegisterMetamodel(package)
        self.AddToHistory(res,tid)
        return Res(CmdTypes.RMM,status,res,tid,self.latestChangeId)
    
    def ExecUmm(self,args,tid):
        status = ResTypes.OKY
        #res = None  
        history = self.GetHistory(tid)
        package = self.qryEvaluator.Eval(args,history) 
        res = self.mdbAccessor.UnregisterMetamodel(package)
        self.AddToHistory(res,tid)
        return Res(CmdTypes.UMM,status,res,tid,self.latestChangeId)
    
    def ExecHel(self,args,tid):
        status = ResTypes.OKY
        #res = None  
        transaction = self.GetTransaction(tid)
        history = transaction.history
        user = self.qryEvaluator.Eval(args[0],history) 
        password = self.qryEvaluator.Eval(args[1],history) 
        
        #prepare a new session
        sessionId = None
        #check identification
        if(1): #TODO: validate user and password
            session = None
            if(transaction.session):
                session = transaction.session
            else: #new session is needed
                session = self.InitSession(transaction, sessionId)
            sessionId = session.sessionId #retrieve the existing session id
            session.user = user
        else:
            raise EoqError(0,'Identification failed.')
        res = sessionId
        self.AddToHistory(res,tid)
        return Res(CmdTypes.HEL,status,res,tid,self.latestChangeId)
    
    def ExecSes(self,args,tid):
        status = ResTypes.OKY
        #res = None  
        transaction = self.GetTransaction(tid)
        history = transaction.history
        sessionId = self.qryEvaluator.Eval(args,history) 
        try:
            session = self.sessions[sessionId]
            transaction.session = session
        except KeyError:
            raise EoqError(0,'Unknown session %s'%(sessionId))
        res = True
        self.AddToHistory(res,tid)
        return Res(CmdTypes.SES,status,res,tid,self.latestChangeId)
    
    def ExecGby(self,args,tid):
        status = ResTypes.OKY
        #res = None  
        transaction = self.GetTransaction(tid)
        history = transaction.history
        sessionId = self.qryEvaluator.Eval(args,history) 
        try:
            self.sessions.pop(sessionId) #delete the session
            transaction.session = None #remove any eventual remaining reference to the session
        except KeyError:
            raise EoqError(0,'Unknown session %s'%(sessionId))
        res = True
        self.AddToHistory(res,tid)
        return Res(CmdTypes.SES,status,res,tid,self.latestChangeId)
    
    def ExecSts(self,args,tid):
        status = ResTypes.OKY
        #res = None   
        res = self.latestChangeId-1 #latest the latest change is one below the indication
        self.AddToHistory(res,tid)
        return Res(CmdTypes.STS,status,res,tid,self.latestChangeId)
    
    def ExecChg(self,args,tid):
        status = ResTypes.OKY
        #res = None  
        history = self.GetHistory(tid)
        changeId = self.qryEvaluator.Eval(args[0],history)
        n = self.qryEvaluator.Eval(args[1],history)
        #sanity check
        if(n<0):
            raise EoqError(0,"Index must be greater or equal zero, but got: %d"%(n))
        
        if(changeId<self.earliestChangeId):
            if(n==0 or changeId+n >= self.latestChangeId): 
                res = [self.changes[i].a for i in range(self.earliestChangeId,self.latestChangeId)]
            elif(changeId+n >= self.earliestChangeId):
                res = [self.changes[i].a for i in range(self.earliestChangeId,changeId+n)]
            else: 
                res = []
        elif(changeId >= self.latestChangeId):
            res = []
        else: #is a valid change id
            if(n==0 or changeId+n >= self.latestChangeId):
                res = [self.changes[i].a for i in range(changeId,self.latestChangeId)]
            else:
                res = [self.changes[i].a for i in range(changeId,changeId+n)]    
        self.AddToHistory(res,tid)
        return Res(CmdTypes.CHG,status,res,tid,self.latestChangeId)
    
    def ExecObs(self,args,tid):
        status = ResTypes.OKY
        #res = None  
        transaction = self.GetTransaction(tid)
        history = transaction.history
        eventType = str(self.qryEvaluator.Eval(args[0],history)) #everything must be string
        eventKey = str(self.qryEvaluator.Eval(args[1],history)) #everything must be string
        #check is session is known
        if(not transaction.session):
            raise EoqError(0,'Must specify session before observing events.')
        #add the desired events to the observation list
        sessionId = transaction.session.sessionId
        self.Obs(sessionId,eventType,eventKey)
        res = True
        self.AddToHistory(res,tid)
        return Res(CmdTypes.OBS,status,res,tid,self.latestChangeId)
    
    def ExecUbs(self,args,tid):
        status = ResTypes.OKY
        #res = None  
        transaction = self.GetTransaction(tid)
        history = transaction.history
        eventType = str(self.qryEvaluator.Eval(args[0],history)) #everything must be string
        eventKey = str(self.qryEvaluator.Eval(args[1],history)) #everything must be string
        #check is session is known
        if(not transaction.session):
            raise EoqError(0,'Must specify session before observing events.')
        #remove the desired events to the observation list
        sessionId = transaction.session.sessionId
        self.Ubs(sessionId,eventType,eventKey)
        res = True
        self.AddToHistory(res,tid)
        return Res(CmdTypes.UBS,status,res,tid,self.latestChangeId)
    
    def ExecGaa(self,args,tid):
        status = ResTypes.OKY
        #res = None  
        #history = self.GetHistory(tid)
        res = [[a.name,[[p.name,p.type,p.min,p.max,p.default,p.description,[[o.value,o.description] for o in p.options]] for p in a.args],[[r.name,r.type,r.min,r.max,r.default,r.description,[[o.value,o.description] for o in r.options]] for r in a.results],a.description,a.tags] for a in self.callManager.GetAllActions()]
        self.AddToHistory(res,tid)
        return Res(CmdTypes.CAL,status,res,tid,self.latestChangeId)
    
    def ExecCal(self,args,tid):
        status = ResTypes.OKY  
        #evaluate any query within the arguments of the call
        transaction = self.GetTransaction(tid)
        history = transaction.history 
        name = self.qryEvaluator.Eval(args[0],history)
        actionArgs = []
        for qry in args[1]:
            aa = self.qryEvaluator.Eval(qry,history)
            actionArgs.append(aa)
            
        optsArr = args[2]
        
        session = transaction.session
        sessionId = session.sessionId if session else None
            
        #call the handler
        res = self.callManager.RunCallSync(name,actionArgs,optsArr,tid,sessionId)
        self.AddToHistory(res,tid)
        return Res(CmdTypes.CAL,status,res,tid,self.latestChangeId)
    
    def ExecAsc(self,args,tid):
        status = ResTypes.OKY
        transaction = self.GetTransaction(tid)
        history = transaction.history 
        
        name = self.qryEvaluator.Eval(args[0],history)
        actionArgs = []
        for qry in args[1]:
            aa = self.qryEvaluator.Eval(qry,history)
            actionArgs.append(aa)
            
        optsArr = args[2]
            
        # Create a temporary session for the action call. This is necessary,
        # to prevent the original session ID from being exposed to the call
        # and for enabling a self-controlled event listening within the action.
        inheritSession = transaction.session
        callSession = self.CreateNewSession(inheritSession=inheritSession,isTemp=True)  
        
        callSessionId =   callSession.sessionId
        inheritSessionId = inheritSession.sessionId if inheritSession else None
        
        res = self.callManager.RunCallAsync(name,actionArgs,optsArr,tid,callSessionId,inheritSessionId)
        self.AddToHistory(res,tid)
        return Res(CmdTypes.ASC,status,res,tid,self.latestChangeId)
    
    
    def ExecAbc(self,args,tid):
        status = ResTypes.OKY
        #res = False  
        history = self.GetHistory(tid)
        callId = self.qryEvaluator.Eval(args,history)
        res = self.callManager.AbortCall(callId, tid)
        self.AddToHistory(res,tid)
        return Res(CmdTypes.CAL,status,res,tid,self.latestChangeId)

    def ExecAdc(self,args,tid):
        status = ResTypes.OKY
        transaction = self.GetTransaction(tid)
        history = transaction.history
        res = self.Adc(*args)
        self.Val(res,tid) # direct evaluation after creation of constraint
        self.AddToHistory(res, tid)
        cid = self.AddLocalChange(tid,ChgTypes.ADC,args[1],args[2],args[4],None)
        res = [res.constraintType, res.target, res.feature, res.law, res.name, res.annotation]
        return Res(CmdTypes.ADC, status, res, tid, self.latestChangeId)

    def ExecRmc(self,args,tid):
        status = ResTypes.OKY
        transaction = self.GetTransaction(tid)
        history = transaction.history
        if args is None:
            self.logger.Info("validation: removing all constraints")
            constraint_target, constraint_feature, constraint_name = self.validationManager.RemoveAllConstraints()
            res = [constraint_target, constraint_feature, constraint_name]
        else:
            res = self.Rmc(args,tid)
            print("res: ",res)
            constraint_target = []
            constraint_feature = []
            constraint_name = []
            if not(isinstance(res,list)):
                res = [res]
            elif isinstance(res[0],list):
                res = res[0]
            for constraint in res:
                constraint_target.append(constraint.target)
                constraint_feature.append(constraint.feature)
                constraint_name.append(constraint.name)
        cid = self.AddLocalChange(tid,ChgTypes.RMC,constraint_target,constraint_feature,constraint_name,None)
        result = []
        if not(isinstance(res, list)):
            res = [res]
        for constraint in res:
            try:
                result.append([constraint.constraintType, constraint.target, constraint.feature, constraint.law, constraint.name, constraint.annotation])
            except:
                result.append(constraint)
        return Res(CmdTypes.RMC, status, result, tid, self.latestChangeId)

    def ExecVal(self,args,tid):
        obj1_new = []
        status = ResTypes.OKY
        transaction = self.GetTransaction(tid)
        history = transaction.history
        if args is None:
            res, obj1, obj2 = self.validationManager.ValidateAll(tid)
            for obj in obj1:
                obj1_new.append(obj.v)
        else:
            res, obj1, obj2 = self.Val(args, tid)
        self.AddToHistory(res, tid)
        return Res(CmdTypes.VAL, status, res, tid, self.latestChangeId)

    def ExecGac(self,args,tid):
        status = ResTypes.OKY
        transaction = self.GetTransaction(tid)
        history = transaction.history
        res = self.Gac()
        self.AddToHistory(res, tid)
        result = []
        for constraint in res:
            try:
                result.append([constraint.constraintType, constraint.target, constraint.feature, constraint.law, constraint.name, constraint.annotation])
            except:
                result.append(constraint)
        return Res(CmdTypes.GAC, status, result, tid, self.latestChangeId)
    
    #@Override
    def IsEventDesired(self,evt,callback,eventTypes,context,sessionId):
        #extend decision based on the session
        if(sessionId):
            if(sessionId in self.sessions):
                eventType = evt.evt
                typeKeys = self.sessions[sessionId].events[eventType]
                eventKey = evt.k
                isEventOk = (eventKey in typeKeys) or ('*' in typeKeys)
                return isEventOk and (evt.evt in eventTypes)
        else:
            return super().IsEventDesired(evt,callback,eventTypes,context,sessionId)
        
    
    '''
    MAINTENANCE METHODS
    '''     
   
    def OnCallManagerEvent(self,evts,source):
        self.NotifyObservers(evts,self) #forward all events of the call manager to the the own listeners
        
    def OnCallMdbAccessorEvent(self,evts,source):
        self.NotifyObservers(evts,self) #forward all events of the call manager to the the own listeners
        
    '''
    PRIVATE METHODS
    '''
    
    def StartTransaction(self,sessionId=None):
        self.mdbAccessor.Lock() #lock the db for this transaction
        self.latestTransactionId+=1
        tid = self.latestTransactionId
        self.mdbAccessor.latestTransactionId = self.latestTransactionId
        self.logger.Log('transaction','Transaction %d started.'%(tid))
        transaction = Transaction(tid)
        self.transactions[tid] = transaction
        #init session if required
        if(sessionId):
            self.InitSession(transaction, sessionId)
        return tid
    
    def EndTransaction(self,res,tid):
        #obtain the changes done during the transaction
        #transactionChanges = self.tempChangesForTransaction.pop(tid)
        
        transaction = self.transactions.pop(tid)
        transactionChanges = transaction.changes
        
        if(res.s == ResTypes.ERR):
            reason = res.v
            self.logger.Warn('Transaction %d failed: %s'%(tid,reason))
            nChanges = len(transactionChanges)
            if(0<nChanges):
                self.logger.Warn('Transaction %d: Rolling back %d changes.'%(tid,nChanges))
                self.RollbackChanges(transactionChanges)
        else:
            if(0<len(transactionChanges)):
                self.PersistChanges(transactionChanges)
        
        #delete the history
        self.mdbAccessor.Release()
        #self.tempHistoryForTransaction.pop(tid)
        self.logger.Log('transaction','Transaction %d ended.'%(tid))
        
    def GetTransaction(self,tid):
        transaction = None
        try:
            transaction = self.transactions[tid]
        except KeyError:
            raise EoqError(0,"Invalid transaction id %d"%tid)
        return transaction
    
    def InitSession(self,transaction,sessionId):
        session = None
        try:
            session = self.sessions[sessionId]
        except KeyError:
            #if not existing, create a new one
            session = self.CreateNewSession(sessionId=sessionId)
        #set the current transaction to the session
        transaction.session = session
        return session
    
    def CreateNewSession(self,sessionId=None,inheritSession=None,isTemp=False):
        if(None==sessionId):
            sessionId = str(uuid4())
            while(sessionId in self.sessions):
                sessionId = str(uuid4())
        elif(sessionId in self.sessions):
            raise EoqError('Session with id %s does already exist.'%(sessionId))
        self.sessionCount += 1
        sessionNumber = self.sessionCount
        session = Session(sessionId,sessionNumber)
        session.isTemp = isTemp
        if(inheritSession):
            session.user = inheritSession.user #inherit the user and access rights
        self.sessions[sessionId] = session
        return session
    
    def CloseTempSession(self,sessionId):
        if(sessionId in self.sessions):
            session = self.sessions[sessionId]
            if(session.isTemp):
                self.sessions.pop(sessionId) #delete the session
            else:
                raise EoqError(0,'Session %s is not a temp session.'%(sessionId))
        else:
            raise EoqError(0,'Unknown session %s'%(sessionId))
        return
        
    def GetHistory(self,tid):
        return self.GetTransaction(tid).history
        
    def AddToHistory(self,value,tid):
        self.GetTransaction(tid).history.append(value)
        
    def AddLocalChange(self,tid,ctype,target,feature,newVal,oldVal,oldOwner=None,oldFeature=None,oldIndex=None):
        transaction = self.GetTransaction(tid)
        cid = self.latestChangeId + len(transaction.changes)#+1
        user = ''
        sessionNumber = 0
        if transaction.session:
            user = transaction.session.user
            sessionNumber = transaction.session.sessionNumber
        chg = ChgEvt(cid,ctype,target,feature,newVal,oldVal,oldOwner,oldFeature,oldIndex,tid,user,sessionNumber) #change id is defined later if the command is done
        self.GetTransaction(tid).changes.append(chg)
        return cid
        
    def PersistChanges(self,changes):
        #notify observers on changes
        for chg in changes:
            #if the maximum of saved changes is exceeded begin deleting entries
            if(self.latestChangeId - self.earliestChangeId > self.maxChanges):
                self.changes.pop(self.earliestChangeId)
                self.earliestChangeId +=1
            #add each change of the current transaction to the change list
            self.changes[self.latestChangeId] = chg
            if(self.latestChangeId!=chg.a[0]):
                raise EoqError(0,'Inconsistency in change detected list.')
            self.latestChangeId+=1
            #log the changes if logging is enabled
            self.logger.Log('change',"Change (%d): %s t: %s, f: %s, n: %s, [was: v:%s, o: %s, f:%s, i:%s] (tid:%d, u:%s, sn:%d)"%(chg.a[0],chg.a[1],chg.a[2],chg.a[3],chg.a[4],chg.a[5],chg.a[6],chg.a[7],chg.a[8],chg.a[9],chg.a[10],chg.a[11]))
        self.NotifyObservers(changes,self)
        
    
        
    def RollbackChanges(self,changes):
        #revert local changes for multicommand transactions
        try:
            for chg in reversed(changes):
                self.logger.Warn("ROLLBACK: %s t: %s, f: %s, n: %s, o:%s"%(chg.a[1],chg.a[2],chg.a[3],chg.a[4],chg.a[5]))
                ctype = chg.a[1]
                if(ctype == ChgTypes.SET):
                    self.RollbackSet(chg)
                elif(ctype == ChgTypes.ADD):
                    self.RollbackAdd(chg)
                elif(ctype == ChgTypes.REM):
                    self.RollbackRem(chg)
                elif(ctype == ChgTypes.MOV):
                    self.RollbackMov(chg)
        except Exception as e:
            self.logger.Error("Error during rollback: %s"%(str(e)))  
            traceback.print_exc()
            
    def RollbackSet(self,chg):
        target = chg.a[2]
        feature = chg.a[3]
        newValue = chg.a[4]
        oldValue = chg.a[5]
        oldOwner = chg.a[6]
        oldFeature = chg.a[7]
        oldIndex = chg.a[8]
        #reset the old value
        self.mdbAccessor.Set(target,feature,oldValue)
        #rebuild the old values containment if it was existing before
        if(oldOwner):
            if(None==oldIndex):
                self.mdbAccessor.Set(oldOwner,oldFeature,newValue)
            else:
                self.mdbAccessor.Add(oldOwner,oldFeature,newValue)
                self.mdbAccessor.Move(newValue,oldIndex)
               
    def RollbackAdd(self,chg):
        target = chg.a[2]
        feature = chg.a[3]
        newValue = chg.a[4]
        #oldValue = chg.a[5]
        oldOwner = chg.a[6]
        oldFeature = chg.a[7]
        oldIndex = chg.a[8]
        #reset the old 
        #rebuild the old values containment if it was existing before
        if(oldOwner):
            if(None==oldIndex):
                self.mdbAccessor.Set(oldOwner,oldFeature,newValue)
            else:
                self.mdbAccessor.Add(oldOwner,oldFeature,newValue)
                self.mdbAccessor.Move(newValue,oldIndex)
        else: #was a new or free object
            self.mdbAccessor.Remove(target,feature,newValue)
            
    def RollbackRem(self,chg):
        target = chg.a[2]
        feature = chg.a[3]
        newValue = chg.a[4]
        #oldValue = chg.a[5]
        #oldOwner = chg.a[6]
        #oldFeature = chg.a[7]
        oldIndex = chg.a[8]
        #reset the old 
        #rebuild the old values containment if it was existing before
        self.mdbAccessor.Add(target,feature,newValue)
        self.mdbAccessor.Move(newValue,oldIndex)
            
    def RollbackMov(self,chg):
        target = chg.a[2]
        #feature = chg.a[3]
        #newValue = chg.a[4]
        #oldValue = chg.a[5]
        #oldOwner = chg.a[6]
        #oldFeature = chg.a[7]
        oldIndex = chg.a[8]
        #reset the old 
        #rebuild the old values containment if it was existing before
        self.mdbAccessor.Move(target,oldIndex)
        
    def Obs(self,sessionId,eventType,eventKey):
        session = self.sessions[sessionId]
        if((eventType not in ALL_EVENT_TYPES) and not(eventType == '*')):
            raise EoqError(0,'Unknown event type: %s'%(eventType))
        if('*' == eventType): #wildcard event
            for e in session.events:
                session.events[e][eventKey] = True
        else: #no wildcard event
            session.events[eventType][eventKey] = True
              
    def Ubs(self,sessionId,eventType,eventKey):
        session = self.sessions[sessionId]
        if((eventType not in ALL_EVENT_TYPES) and not(eventType == '*')):
            raise EoqError(0,'Unknown event type: %s'%(eventType))
        if('*' == eventType): #wildcard event
            if('*' == eventKey): #if key is a wildcard, all events are removed
                for e in session.events:
                    session.events[e].clear()
            else: #else remove the specific key
                for e in session.events:
                    session.events[e].pop(eventKey)
        else: #no wildcard event
            if('*' == eventKey):
                session.events[eventType].clear()
            else:
                session.events[eventType].pop(eventKey)

    def Adc(self,constraintType,target,feature,law,name,annotation):
        return self.validationManager.AddConstraint(constraintType,target,feature,law,name,annotation)

    def Rmc(self,constraint,tid):
        try:
            # TODO redo after constraints are properly integrated into model
            # hacky: convert history object to possible constraint
            history = self.GetHistory(tid)
            constraint2 = self.qryEvaluator.Eval(constraint,history)
        except:
            constraint2 = None
        if not(isinstance(constraint2,list)):
            constraint2 = [constraint2]
        elif isinstance(constraint2[0],list):
            constraint2 = constraint2[0]
        for con in constraint2:
            if self.validationManager.IsConstraint(constraint):
                # this only works if constraint is a native Constraint instance
                self.validationManager.RemoveConstraint(constraint)
            elif self.validationManager.IsConstraint(con):
                # therefore we try to convert a EOQ His object to its "value" above
                self.validationManager.RemoveConstraint(con)
        return constraint2

    def Val(self, obj, tid):
        """
            can evaluate either obj that are constraints (case 1 and 2) or obj that are targets (case 3)
        """
        result = []
        try:
            # TODO redo after constraints are properly integrated into model
            # hacky: convert history object to possible constraint
            #cmd = self.textSerializer.Des("GET "+self.textSerializer.Ser(obj))
            #obj2 = self.validationManager._RunCmd(cmd, tid).v
            history = self.GetHistory(tid)
            obj2 = self.qryEvaluator.Eval(obj,history)
        except:
            obj2 = None
        if not(isinstance(obj2,list)):
            obj2 = [obj2]
        elif isinstance(obj2[0],list):
            obj2 = obj2[0]
        for obj3 in obj2:
            if self.validationManager.IsConstraint(obj):
                # this only works if obj is a native Constraint instance
                res = self.validationManager.ValidateConstraint(obj, tid)
            elif self.validationManager.IsConstraint(obj3):
                # therefore we try to convert a EOQ His object to its "value" above
                res = self.validationManager.ValidateConstraint(obj3, tid)[0]
            else:
                # otherwise it is not a constraint but a valid target
                res = self.validationManager.ValidateTarget(obj, tid)
            result.append(res)
        return result, obj, obj2

    def Gac(self):
        return self.validationManager.GetConstraints()
        
    def ChangeConstrainttoList(self, res):
        for index in range(len(res)):
            if isinstance(res[index],list):
                self.ChangeConstrainttoList(res[index])
            elif self.validationManager.IsConstraint(res[index]):
                res[index] = [res[index].constraintType, res[index].target, res[index].feature, res[index].law, res[index].name, res[index].annotation]
            else:
                res[index] = res[index]
        return res

