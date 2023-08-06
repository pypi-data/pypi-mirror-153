from .query import QrySegTypes,QryMetaSegTypes,QryIdxTypes,ObjSeg,Qry,Seg,Try
from ..util.error import EoqError
from ..util.util import ApplyToAllElements,ApplyToAllElementsInA,ApplyToAllElementsInB,ApplyToAllListsOfElementsInA,ApplyToSimilarElementStrutures,ApplyToSimilarListsOfObjects,IsList,IsListOfObjects,Terminator,Determinate,IsNoList
from ..util.benchmark import Benchmark

import re

'''
    QueryRunner
    
    Evaluates a essential object query using a mdb accessor and value codec. Only the EvalOnContextAndScope function should be called
    
'''

class QryRunner:
    def __init__(self,mdbAccessor,validationManager,enableBenchmark=False):
        #self.mdb = mdb
        self.mdbAccessor = mdbAccessor
        self.enableBenchmark = enableBenchmark
        self.segmentEvaluators = {}
        #constraints
        self.validationManager = validationManager
        
        #benchmark
        if self.enableBenchmark:
            self.benchmark = Benchmark()
            allQryTypes = [getattr(QrySegTypes,k) for k in QrySegTypes.__dict__ if not k.startswith('_')]
            for t in allQryTypes:
                self.benchmark.InitMessure(t)
        
        
        #Segment oparators
        self.segmentEvaluators[QrySegTypes.OBJ] = self.EvalObj
        self.segmentEvaluators[QrySegTypes.HIS] = self.EvalHis
        
        self.segmentEvaluators[QrySegTypes.PTH] = self.EvalPth
        self.segmentEvaluators[QrySegTypes.CLS] = self.EvalCls
        self.segmentEvaluators[QrySegTypes.INO] = self.EvalIno
        self.segmentEvaluators[QrySegTypes.MET] = self.EvalMet
        self.segmentEvaluators[QrySegTypes.NOT] = self.EvalNot
        self.segmentEvaluators[QrySegTypes.TRM] = self.EvalTrm
        self.segmentEvaluators[QrySegTypes.CNS] = self.EvalCns
        self.segmentEvaluators[QrySegTypes.TRY] = self.EvalTry
        
        self.segmentEvaluators[QrySegTypes.IDX] = self.EvalIdx
        self.segmentEvaluators[QrySegTypes.SEL] = self.EvalSel
        self.segmentEvaluators[QrySegTypes.ARR] = self.EvalArr
        self.segmentEvaluators[QrySegTypes.ZIP] = self.EvalZip
        self.segmentEvaluators[QrySegTypes.QRY] = self.EvalQry
        
        self.segmentEvaluators[QrySegTypes.ANY] = self.EvalAny
        self.segmentEvaluators[QrySegTypes.ALL] = self.EvalAll
        
        self.segmentEvaluators[QrySegTypes.EQU] = self.EvalEqu
        self.segmentEvaluators[QrySegTypes.EQA] = self.EvalEqa
        self.segmentEvaluators[QrySegTypes.NEQ] = self.EvalNeq
        self.segmentEvaluators[QrySegTypes.LES] = self.EvalLes
        self.segmentEvaluators[QrySegTypes.GRE] = self.EvalGre
        self.segmentEvaluators[QrySegTypes.RGX] = self.EvalRgx
        
        self.segmentEvaluators[QrySegTypes.ADD] = self.EvalAdd
        self.segmentEvaluators[QrySegTypes.SUB] = self.EvalSub
        self.segmentEvaluators[QrySegTypes.MUL] = self.EvalMul
        self.segmentEvaluators[QrySegTypes.DIV] = self.EvalDiv
        
        #synonyms for boolean operations
        self.segmentEvaluators[QrySegTypes.ORR] = self.EvalAdd
        self.segmentEvaluators[QrySegTypes.XOR] = self.EvalSub
        self.segmentEvaluators[QrySegTypes.AND] = self.EvalMul
        self.segmentEvaluators[QrySegTypes.NAD] = self.EvalDiv
        
        self.segmentEvaluators[QrySegTypes.CSP] = self.EvalCsp
        self.segmentEvaluators[QrySegTypes.ITS] = self.EvalIts
        self.segmentEvaluators[QrySegTypes.DIF] = self.EvalDif
        self.segmentEvaluators[QrySegTypes.UNI] = self.EvalUni
        self.segmentEvaluators[QrySegTypes.CON] = self.EvalCon
        
        #META oparators
        self.metEvaluators = {}
        self.metEvaluators[QryMetaSegTypes.CLS] = self.EvalMetCls
        self.metEvaluators[QryMetaSegTypes.CLN] = self.EvalMetCln
        self.metEvaluators[QryMetaSegTypes.LEN] = self.EvalMetLen
        self.metEvaluators[QryMetaSegTypes.PAR] = self.EvalMetPar
        self.metEvaluators[QryMetaSegTypes.CON] = self.EvalMetPar #container is the same as parent
        self.metEvaluators[QryMetaSegTypes.ALP] = self.EvalMetAlp
        self.metEvaluators[QryMetaSegTypes.ASO] = self.EvalMetAso
        self.metEvaluators[QryMetaSegTypes.IDX] = self.EvalMetIdx
        self.metEvaluators[QryMetaSegTypes.CFT] = self.EvalMetCft
        self.metEvaluators[QryMetaSegTypes.FEA] = self.EvalMetFea
        self.metEvaluators[QryMetaSegTypes.FEN] = self.EvalMetFen
        self.metEvaluators[QryMetaSegTypes.FEV] = self.EvalMetFev
        self.metEvaluators[QryMetaSegTypes.ATT] = self.EvalMetAtt
        self.metEvaluators[QryMetaSegTypes.ATN] = self.EvalMetAtn
        self.metEvaluators[QryMetaSegTypes.ATV] = self.EvalMetAtv
        self.metEvaluators[QryMetaSegTypes.REF] = self.EvalMetRef
        self.metEvaluators[QryMetaSegTypes.REN] = self.EvalMetRen
        self.metEvaluators[QryMetaSegTypes.REV] = self.EvalMetRev
        self.metEvaluators[QryMetaSegTypes.CNT] = self.EvalMetCnt
        self.metEvaluators[QryMetaSegTypes.CNN] = self.EvalMetCnn
        self.metEvaluators[QryMetaSegTypes.CNV] = self.EvalMetCnv
        #class meta operators
        self.metEvaluators[QryMetaSegTypes.PAC] = self.EvalMetPac
        self.metEvaluators[QryMetaSegTypes.STY] = self.EvalMetSty
        self.metEvaluators[QryMetaSegTypes.ALS] = self.EvalMetAls
        self.metEvaluators[QryMetaSegTypes.IMP] = self.EvalMetImp
        self.metEvaluators[QryMetaSegTypes.ALI] = self.EvalMetAli
        self.metEvaluators[QryMetaSegTypes.MMO] = self.EvalMetMmo
        #control flow operators
        self.metEvaluators[QryMetaSegTypes.IFF] = self.EvalMetIff
        
        #terminate operation
        def oprTrm(a,b):
            return a #do nothing
         
        #equals Operations
        def equBol(a,b):
            return a==b
        def equInt(a,b):
            return a==b
        def equStr(a,b):
            return a==b
        def equFlo(a,b):
            return a==b
        def equObj(a,b):
            return a==b
        def equNon(a,b):
            return a==b
        self.equEvaluators = {bool: equBol, int: equInt, str: equStr, float: equFlo, ObjSeg: equObj, type(None): equNon, Terminator: oprTrm} #TODO: does probably not work for queries decoded from JSON
        
        #not not equal Operations
        def neqBol(a,b):
            return a!=b
        def neqInt(a,b):
            return a!=b
        def neqStr(a,b):
            return a!=b
        def neqFlo(a,b):
            return a!=b
        def neqObj(a,b):
            return a!=b
        def neqNon(a,b):
            return a!=b
        self.neqEvaluators = {bool: neqBol, int: neqInt, str: neqStr, float: neqFlo, ObjSeg: neqObj, type(None): neqNon, Terminator: oprTrm} #TODO: does probably not work for queries decoded from JSON
        
        #not greater Operations
        def greBol(a,b):
            return a>b
        def greInt(a,b):
            return a>b
        def greStr(a,b):
            return a>b
        def greFlo(a,b):
            return a>b
        def greObj(a,b):
            return a.v>b.v
        self.greEvaluators = {bool: greBol, int: greInt, str: greStr, float: greFlo, ObjSeg: greObj, Terminator: oprTrm} #TODO: does probably not work for queries decoded from JSON
        
        #not less Operations
        def lesBol(a,b):
            return a<b
        def lesInt(a,b):
            return a<b
        def lesStr(a,b):
            return a<b
        def lesFlo(a,b):
            return a<b
        def lesObj(a,b):
            return a.v<b.v
        self.lesEvaluators = {bool: lesBol, int: lesInt, str: lesStr, float: lesFlo, ObjSeg: lesObj, Terminator: oprTrm} #TODO: does probably not work for queries decoded from JSON
        
        #regex Operations
        def rgxStr(a,b):
            return True if(b.search(a)) else False
        self.rgxEvaluators = {str: rgxStr} #TODO: does probably not work for queries decoded from JSON

        #add Operations
        def addBol(a,b):
            return (a or b)
        def addInt(a,b):
            return a+b
        def addStr(a,b):
            return a+b
        def addFlo(a,b):
            return a+b
        def addObj(a,b):
            return [a,b]
        self.addEvaluators = {bool: addBol, int: addInt, str: addStr, float: addFlo, ObjSeg: addObj, Terminator: oprTrm} 
        
        #substraction perations
        def subBol(a,b):
            return ((not a and b) or (a and not b))
        def subInt(a,b):
            return a-b
        def subStr(a,b):
            return a-b
        def subFlo(a,b):
            return a-b
        def subObj(a,b):
            return [a,b]
        self.subEvaluators = {bool: subBol, int: subInt, str: subStr, float: subFlo, ObjSeg: subObj, Terminator: oprTrm} 
        
        # Init multiplication operators
        def mulBol(a,b):
            return (a and b)
        def mulInt(a,b):
            return a*b
        def mulStr(a,b):
            return a+b
        def mulFlo(a,b):
            return a*b
        def mulObj(a,b):
            return [a,b]
        self.mulEvaluators = {bool: mulBol, int: mulInt, str: mulStr, float: mulFlo, ObjSeg: mulObj, Terminator: oprTrm} #TODO: does probably not work for queries decoded from JSON
                
        #division operators
        def divBol(a,b):
            return (not (a and b))
        def divInt(a,b):
            return int(a/b)
        def divStr(a,b):
            return a+b
        def divFlo(a,b):
            return a/b
        def divObj(a,b):
            return [a,b]
        self.divEvaluators = {bool: divBol, int: divInt, str: divStr, float: divFlo, ObjSeg: divObj, Terminator: oprTrm} 
        
        
       
        
        #cross product operation
        def cspUni(a,b):
            res = []
            for e1 in a:
                for e2 in b:
                    res.append([e1,e2])
            return res
        self.cspEvaluator = cspUni
        
        #intersection operation
        def itsUni(a,b):
            res = []
            #add common elements
            for e1 in a:
                if(e1 in b):
                    res.append(e1)
            return res
        self.itsEvaluator = itsUni
        
        #set difference operation
        def difUni(a,b):
            res = []
            #add common elements
            for e1 in a:
                if(e1 not in b):
                    res.append(e1)
            return res
        self.difEvaluator = difUni
        
        #union operations
        def uniUni(a,b):
            res = []
            #add all unique elements of a
            for e in a:
                if(e in res):
                    continue
                res.append(e)
            #add all unique elements of b
            for e in b:
                if(e in res):
                    continue
                res.append(e)
            return res
        self.uniEvaluator = uniUni
        
        #concatenate operation
        def conUni(a,b):
            res = []
            res.extend(a)
            res.extend(b)
            return res
        self.conEvaluator = conUni
        
        
    def Eval(self,qry,history=[]):
        modelroot = self.mdbAccessor.GetRoot()
        context = modelroot
        return self.EvalOnContextAndScope(context,qry,context,history)
        
    def EvalOnContextAndScope(self,context,seg,scope,history):
        res = None
        
        if(isinstance(seg,Seg)):
            qryType = seg.qry
            try:
                evalFunction = self.segmentEvaluators[qryType] 
            except KeyError as e:
                raise EoqError(0,"Unknown segment type: %s: %s"%(qryType,str(e)))
            if self.enableBenchmark: self.benchmark.Start()
            try:
                v = seg.v 
                res = evalFunction(context,v,scope,history)
            except Exception as e:
                if self.enableBenchmark: self.benchmark.Stop(qryType)
                raise e         
            if self.enableBenchmark: self.benchmark.Stop(qryType)
        elif(IsList(seg)):
            res = self.EvalArr(context,seg,scope,history)
        else:
            res = seg #its a primitive value, do nothing
        return res   
    
    '''
        SEGMENT EVALUATORS
    '''
        
    def EvalQry(self,context,args,scope,history):
        currentContext = scope #each subquery restarts from the current scope
        #newScope = context
        for seg in args:
            if(isinstance(currentContext,Terminator)):
                break;
            currentContext = self.EvalOnContextAndScope(currentContext,seg,scope,history)
        res = Determinate(currentContext)
        return res
    
    def EvalObj(self,context,v,scope,history):
        return ObjSeg(v) # because the argument is unpacked before
    
    def EvalHis(self,context,n,scope,history):
        res = None
        try:
            res = self.EvalOnContextAndScope(context,history[n],context,history)
        except Exception as e:
            raise EoqError(0,"Error evaluating history %s. Current history has a length of %d: %s"%(n,len(history),str(e)))
        return res
        
    def EvalPth(self,context,name,scope,history):
        res = None
        
        pathFunctor = lambda o: self.mdbAccessor.Get(o,name)
        
        try:
            res = ApplyToAllElements(context, pathFunctor)
        except Exception as e:
            raise EoqError(0,"Error evaluating path segment %s: %s"%(name,str(e)))
        return res
    
    def EvalCls(self,context,args,scope,history):
        res = None
        
        clsFunctor = lambda a,b: self.mdbAccessor.GetAllChildrenOfType(a,b)
        
        name = self.EvalOnContextAndScope(context,args,context,history)
        try:
            res = ApplyToAllElementsInA(context,name,clsFunctor)
        except Exception as e:
            raise EoqError(0,"Error evaluating class segment %s: %s"%(name,str(e)))
        return res

    def EvalIno(self,context,args,scope,history):
        res = None
        
        inoFunctor = lambda a,b: self.mdbAccessor.GetAllChildrenInstanceOfClass(a,b)
        
        name = self.EvalOnContextAndScope(context,args,context,history)
        try:
            res = ApplyToAllElementsInA(context,name,inoFunctor)
        except Exception as e:
            raise EoqError(0,"Error evaluating instance of segment %s: %s"%(name,str(e)))
        return res
    
    def EvalNot(self,context,name,scope,history):
        res = None
        
        notFunctor = lambda o: False if o else True
        
        try:
            res = ApplyToAllElements(context, notFunctor)
        except Exception as e:
            raise EoqError(0,"Error evaluating not segment %s: %s"%(name,str(e)))
        return res
    
    def EvalTrm(self,context,args,scope,history):
        res = None
        #Define select functors
        def TrmOperator(a,b,c):
            res = None
            if(isinstance(a,Terminator)):
                res = a
            elif(b):
                res = Terminator(c)
            else:
                res = a
            return res
        def TrmElemVsElemFunc(a,b,c):
            return [TrmOperator(a[i],b[i],c) for i in range(len(b))]
            #return TrmOperator(a,b,c)
        def TrmElemVsStructFunc(a,b,c):
            raise EoqError(0,"Error applying termination: Argument of termination condition must be of lower depth than the context, but got %s{%s,%s}="%(a,b,c))
        def TrmStructVsElemFunc(a,b,c): 
            return [TrmOperator(a[i],b[i],c) for i in range(len(b))]
        #Begin of function
        condquery = args[0]
        if(None==condquery): #special default case
            condquery = Qry().Equ(None)
        condition = self.EvalOnContextAndScope(context,condquery,context,history)
        default = self.EvalOnContextAndScope(context,args[1],context,history)
        try:
            res = ApplyToSimilarListsOfObjects([context],[condition],TrmElemVsElemFunc,TrmElemVsStructFunc,TrmStructVsElemFunc,default)
        except Exception as e:
            raise EoqError(0,"Failed evaluating terminator %s. Terminator condition context and argument must be arrays of similar structure. Argument must be either be an array of Bool, but got %s: %s"%(args,condition,str(e)))
        return res[0] #return the first element because context and condition were listified above

    def EvalCns(self,context,name,scope,history):
        if not(isinstance(context,list)):
            context = [context]
        res = None
        tid = self.mdbAccessor.latestTransactionId
        try:
            res = self.validationManager.GetConstraintsTargeting(context, tid)
        except Exception as e:
            raise EoqError(0,"Error evaluating CNS segment %s: %s"%(name,str(e)))
        return res
    
    def EvalTry(self,context,args,scope,history):
        def tryFunctor(a,b):
            res = None
            query = b[0]
            default = b[1]
            history = b[2]
            try:
                res = self.EvalOnContextAndScope(a,query,a,history)
            except:
                res = self.EvalOnContextAndScope(a,default,a,history)
            return res
        
        query = args[0] #do not evaluate here but element-wise inside try
        default = args[1]
        #default = self.EvalOnContextAndScope(context,args[1],context,history)
        
        res = ApplyToAllElementsInA(context,(query,default,history),tryFunctor)
        
        return res
    
    def EvalIdx(self,context,args,scope,history):
        res = None
        if(not IsList(context)):
            raise EoqError(0,"IDX: Can only select from lists but got: %s"%(context))
        n = self.EvalOnContextAndScope(context,args,context,history)
        if(isinstance(n, int)):
            idxFunctor = lambda a,b: a[b]
            res = ApplyToAllListsOfElementsInA(context,n,idxFunctor)
        elif(isinstance(n, str)):
            if(QryIdxTypes.ASC==n): #sort ascending
                ascFunctor = lambda a,b: sorted(a)
                res = ApplyToAllListsOfElementsInA(context,None,ascFunctor)
            elif(QryIdxTypes.DSC==n): #sort descending
                dscFunctor = lambda a,b: sorted(a,reverse=True)
                res = ApplyToAllListsOfElementsInA(context,None,dscFunctor)
            elif(QryIdxTypes.FLT==n): #flatten
                if(IsList(context)):
                    res = []
                    self._Flatten(context,res)
                else:
                    res = context
            elif(QryIdxTypes.LEN==n): #calc size
                lenFunctor = lambda a,b: len(a)
                res = ApplyToAllListsOfElementsInA(context,None,lenFunctor)
            else:
                raise EoqError(0,"IDX: Unknown index keyword: %s"%(n))
        elif(IsList(n) and len(n)==3 and isinstance(n[0], int)):
            rngFunctor = lambda a,b: a[b[0]:b[1]:b[2]]
            res = ApplyToAllListsOfElementsInA(context,n,rngFunctor)
        else:
            raise EoqError(0,"IDX: argument bust be index:int, %s or [lb:int,ub:int,step:int] but got: %s"%([QryIdxTypes.ASC,QryIdxTypes.DSC,QryIdxTypes.FLT,QryIdxTypes.LEN],n))
        return res
    
    def EvalSel(self,context,args,scope,history):
        res = []
        #Define select functors
        def SelListVsListFunc(a,b,c):
            if(len(a) == len(b)):
                return [a[i] for i in range(len(b)) if b[i]]
            else: 
                raise EoqError(0,"Error applying selector: context and selector list must have the same number of elements, but got %s{%s}"%(a,b))
        def SelListVsStructFunc(a,b,c):
            if(IsList(b)):
                raise EoqError(0,"Error applying selector: Argument of selector must be of lower depth than the context, but got %s{%s}"%(a,b))
            else: 
                return [a[i] for i in range(len(a)) if b]
        def SelStructVsListFunc(a,b,c): 
            return [a[i] for i in range(len(b)) if b[i]] # is the same since 
        # Input check 
        if(IsNoList(context)): 
            raise EoqError(0,"Select only works on lists or lists of list, but got %s"%(str(context)))
        #Start Select evaluation        
        # selector changes the context
        if(0==len(context)):
            res = [] #The result of an empty array is always an empty array. This saves time and prevents wrong interpretations of select queries that reduce the array length, e.g. any
        else:
            select = self.EvalOnContextAndScope(context,args,context,history)
            try:
                res = ApplyToSimilarListsOfObjects(context,select,SelListVsListFunc,SelListVsStructFunc,SelStructVsListFunc)
            except Exception as e:
                raise EoqError(0,"Failed evaluating selector %s. Selectors context and argument must be arrays of similar structure. Argument must be either be an array of Bool, but got %s: %s"%(args,select,str(e)))
        return res
    
    def EvalArr(self,context,args,scope,history): 
        res = [self.EvalOnContextAndScope(context,a,context,history) for a in args]
        return res
    
    def EvalZip(self,context,args,scope,history):
        class ZipBlocker:
            def __init__(self,v):
                self.v = v
        
        def ZipListVsListFunc(a,b,c):
            return a+[ZipBlocker(b)]
        def ZipListVsStructFunc(a,b,c):
            return a+[ZipBlocker(b)]
        def ZipStructVsListFunc(a,b,c):
            #return a+[b]
            return [ApplyToAllListsOfElementsInA(a[i],b[i],lambda a,b: a+[ZipBlocker(b)]) for i in range(len(b))]
        
        #prepare the results structure according to the context
        res = ApplyToAllElementsInA(context,None,lambda a,b: [])
        #get the individual results
        for a in args:
            ar = self.EvalOnContextAndScope(context,a,context,history)
            #merge the individual result in the result structure derived from the context
            res = ApplyToSimilarListsOfObjects(res,ar,ZipListVsListFunc,ZipListVsStructFunc,ZipStructVsListFunc)
        
        #remove ZipBlocker
        def RemoveZipBlockers(l):
            if(IsList(l)):
                return [RemoveZipBlockers(i) for i in l]
            else:
                if(ZipBlocker == type(l)):
                    return l.v
                else:
                    return l
                
        res = RemoveZipBlockers(res)

        return res
    
    
    def EvalAny(self,context,args,scope,history):
        #local functor
        def anyFunctor(a,b):
            if(IsList(b)):
                for e in b:
                    if(e in a):
                        return True
            else:
                return (b in a)
            return False
        
        #method start
        if(not IsList(context)):
            raise EoqError(0,"ANY: Can only select from lists but got: %s"%(context))
        select = self.EvalOnContextAndScope(context,args,context,history)
        if(IsList(select) and not IsListOfObjects(select)):
            raise EoqError(0,"ANY: Select argument must be a single element or a list of elements but got: %s"%(select))
        res = ApplyToAllListsOfElementsInA(context,select,anyFunctor)
        return res
    
    def EvalAll(self,context,args,scope,history):
        #local functor
        def allFunctor(a,b):
            foundMembers = 0
            if(IsList(b)):
                for e in b:
                    if(e in a):
                        foundMembers +=1
                return (len(b)==foundMembers)
            else:
                return (b in a)
            return False
        
        #method start
        if(not IsList(context)):
            raise EoqError(0,"ALL: Can only select from lists but got: %s"%(context))
        select = self.EvalOnContextAndScope(context,args,context,history)
        if(IsList(select) and not IsListOfObjects(select)):
            raise EoqError(0,"ALL: Select argument must be a single element or a list of elements but got: %s"%(select))
        res = ApplyToAllListsOfElementsInA(context,select,allFunctor)
        return res
    
    def EvalMet(self,context,args,scope,history):
        res = None
        try: 
            name = args[0]
            metEvaluator = self.metEvaluators[name]
            res = metEvaluator(context,args,scope,history)
        except KeyError as e:
            raise EoqError(0,"Unknown META segment type: %s: %s"%(name,str(e)))
        except Exception as e:
            raise EoqError(0,"Failed to evaluate meta segment %s: %s"%(name,str(e)))
        return res
    
    '''
        META EVALATORS
    '''
   
    def EvalMetCls(self,context,args,scope,history):
        res = None
        nArgs = len(args)
        if(1==nArgs):
            clsFunctor = lambda a,b: self.mdbAccessor.Class(a)
            res = ApplyToAllElementsInA(context,None,clsFunctor)
        elif(3==nArgs):
            packageName = self.EvalOnContextAndScope(context,args[1],context,history)
            className = self.EvalOnContextAndScope(context,args[2],context,history)
            if(isinstance(packageName,str) and isinstance(className,str)):
                res = self.mdbAccessor.GetClassByName(packageName,className)
            else:
                raise EoqError(0,"CLASS if giving two args, both must be string, but got: package %s and class %s"%(str(packageName,className)))
        else:
            raise EoqError(0,"CLASS expects either no argument or two of type string, but got: %s."%(str(args)))
        return res
    
    def EvalMetCln(self,context,args,scope,history):
        clnFunctor = lambda a,b: self.mdbAccessor.ClassName(a)
        
        res = ApplyToAllElementsInA(context,None,clnFunctor)
        return res
    
    def EvalMetLen(self,context,args,scope,history):
        lenFunctor = lambda a,b: len(a)
        
        res = ApplyToAllListsOfElementsInA(context,None,lenFunctor)
        return res
    
    def EvalMetPar(self,context,args,scope,history):
        parFunctor = lambda a,b: self.mdbAccessor.GetParent(a)
        
        res = ApplyToAllElementsInA(context,None,parFunctor)
        return res
    
    def EvalMetAlp(self,context,args,scope,history):
        alpFunctor = lambda a,b: self.mdbAccessor.GetAllParents(a)
        
        res = ApplyToAllElementsInA(context,None,alpFunctor)
        return res
    
    def EvalMetAso(self,context,args,scope,history):
        
        root = None
        if(1<len(args)):
            root = self.EvalOnContextAndScope(context,args[1],context,history)
        else:
            root = self.mdbAccessor.GetRoot()
        
        asoFunctor = lambda a,b: self.mdbAccessor.GetAssociates(a,b)
        
        res = ApplyToAllElementsInA(context,root,asoFunctor)
        return res
    
    def EvalMetIdx(self,context,args,scope,history):
        idxFunctor = lambda a,b: self.mdbAccessor.GetIndex(a)
        
        res = ApplyToAllElementsInA(context,None,idxFunctor)
        return res
    
    def EvalMetCft(self,context,args,scope,history):
        cftFunctor = lambda a,b: self.mdbAccessor.GetContainingFeature(a)
        
        res = ApplyToAllElementsInA(context,None,cftFunctor)
        return res
    
    def EvalMetFea(self,context,args,scope,history):
        feaFunctor = lambda a,b: self.mdbAccessor.GetAllFeatures(a)
        
        res = ApplyToAllElementsInA(context,None,feaFunctor)
        return res
    
    def EvalMetFen(self,context,args,scope,history):
        fenFunctor = lambda a,b: self.mdbAccessor.GetAllFeatureNames(a)
        
        res = ApplyToAllElementsInA(context,None,fenFunctor)
        return res
    
    def EvalMetFev(self,context,args,scope,history):
        fevFunctor = lambda a,b: self.mdbAccessor.GetAllFeatureValues(a)
        
        res = ApplyToAllElementsInA(context,None,fevFunctor)
        return res
    
    def EvalMetAtt(self,context,args,scope,history):
        attFunctor = lambda a,b: self.mdbAccessor.GetAllAttributes(a)
        
        res = ApplyToAllElementsInA(context,None,attFunctor)
        return res
    
    def EvalMetAtn(self,context,args,scope,history):
        atnFunctor = lambda a,b: self.mdbAccessor.GetAllAttributeNames(a)
        
        res = ApplyToAllElementsInA(context,None,atnFunctor)
        return res
    
    def EvalMetAtv(self,context,args,scope,history):
        atvFunctor = lambda a,b: self.mdbAccessor.GetAllAttributeValues(a)
        
        res = ApplyToAllElementsInA(context,None,atvFunctor)
        return res
    
    def EvalMetRef(self,context,args,scope,history):
        refFunctor = lambda a,b: self.mdbAccessor.GetAllReferences(a)
        
        res = ApplyToAllElementsInA(context,None,refFunctor)
        return res
    
    def EvalMetRen(self,context,args,scope,history):
        renFunctor = lambda a,b: self.mdbAccessor.GetAllReferenceNames(a)
        
        res = ApplyToAllElementsInA(context,None,renFunctor)
        return res
    
    def EvalMetRev(self,context,args,scope,history):
        revFunctor = lambda a,b: self.mdbAccessor.GetAllReferenceValues(a)
        
        res = ApplyToAllElementsInA(context,None,revFunctor)
        return res
    
    def EvalMetCnt(self,context,args,scope,history):
        cntFunctor = lambda a,b: self.mdbAccessor.GetAllContainments(a)
        
        res = ApplyToAllElementsInA(context,None,cntFunctor)
        return res
    
    def EvalMetCnn(self,context,args,scope,history):
        cnnFunctor = lambda a,b: self.mdbAccessor.GetAllContainmentNames(a)
        
        res = ApplyToAllElementsInA(context,None,cnnFunctor)
        return res
    
    def EvalMetCnv(self,context,args,scope,history):
        cnvFunctor = lambda a,b: self.mdbAccessor.GetAllContainmentValues(a)
        
        res = ApplyToAllElementsInA(context,None,cnvFunctor)
        return res
    
    def EvalMetPac(self,context,args,scope,history):
        pacFunctor = lambda a,b: self.mdbAccessor.Package(a)
        
        res = ApplyToAllElementsInA(context,None,pacFunctor)
        return res
    
    def EvalMetSty(self,context,args,scope,history):
        
        styFunctor = lambda a,b: self.mdbAccessor.Supertypes(a)
        
        res = ApplyToAllElementsInA(context,None,styFunctor)
        return res
    
    def EvalMetAls(self,context,args,scope,history):
        alsFunctor = lambda a,b: self.mdbAccessor.AllSupertypes(a)
        
        res = ApplyToAllElementsInA(context,None,alsFunctor)
        return res
    
    def EvalMetImp(self,context,args,scope,history):
        impFunctor = lambda a,b: self.mdbAccessor.Implementers(a)
        
        res = ApplyToAllElementsInA(context,None,impFunctor)
        return res
    
    def EvalMetAli(self,context,args,scope,history):
        aliFunctor = lambda a,b: self.mdbAccessor.AllImplementers(a)
        
        res = ApplyToAllElementsInA(context,None,aliFunctor)
        return res
    
    def EvalMetMmo(self,context,args,scope,history):
        res = self.mdbAccessor.GetAllMetamodels()
        return res
    
    
    def EvalMetIff(self,context,args,scope,history):
        
        condition = self.EvalOnContextAndScope(context,args[1],context,history)
        
        res = None
        if(condition):
            res = self.EvalOnContextAndScope(context,args[2],context,history)
        else:
            res = self.EvalOnContextAndScope(context,args[3],context,history)
        return res
    
    '''
        LOGICAL AND MATH OPERATORS
    '''
    
    def EvalEqu(self,context,args,scope,history):
        res = self.EvalElementOperation(context, args, scope, QrySegTypes.EQU, self.equEvaluators,history)
        return res
    
    def EvalEqa(self,context,args,scope,history):
        #local functor
        def eqaFunctor(a,b):
            return (a in b)
        
        #method start
        select = self.EvalOnContextAndScope(context,args,context,history)
        if(not IsListOfObjects(select)):
            raise EoqError(0,"EQA: Argument must be a list of elements but got: %s"%(select))
        res = ApplyToAllElementsInA(context,select,eqaFunctor)
        return res
    
    def EvalNeq(self,context,args,scope,history):
        res = self.EvalElementOperation(context, args, scope, QrySegTypes.NEQ, self.neqEvaluators,history)
        return res
    
    def EvalLes(self,context,args,scope,history):
        res = self.EvalElementOperation(context, args, scope, QrySegTypes.LES, self.lesEvaluators,history)
        return res
    
    def EvalGre(self,context,args,scope,history):
        res = self.EvalElementOperation(context, args, scope, QrySegTypes.GRE, self.greEvaluators,history)
        return res
    
    def EvalRgx(self,context,args,scope,history):
        if(not isinstance(args,str)):
            raise EoqError(0,"Regex argument must be string, but got %s."%(args))
        pattern = None
        try:
            pattern = re.compile(args)
        except Exception as e:
            raise EoqError(0,"%s is no valid regular expression: %s"%(args,str(e)))
        res = self.EvalElementOperation(context, pattern, scope, QrySegTypes.RGX, self.rgxEvaluators,history)
        return res

    def EvalRgx(self,context,args,scope,history):
        if(not isinstance(args,str)):
            raise EoqError(0,"Regex argument must be string, but got %s."%(args))
        pattern = None
        try:
            pattern = re.compile(args)
        except Exception as e:
            raise EoqError(0,"%s is no valid regular expresion: %s"%(args,str(e)))
        res = self.EvalElementOperation(context, pattern, scope, QrySegTypes.RGX, self.rgxEvaluators, history)
        return res
    
    def EvalAdd(self,context,args,scope,history):
        res = self.EvalElementOperation(context, args, scope, QrySegTypes.ADD, self.addEvaluators,history)
        return res
    
    def EvalSub(self,context,args,scope,history):
        res = self.EvalElementOperation(context, args, scope, QrySegTypes.SUB, self.subEvaluators,history)
        return res
    
    def EvalMul(self,context,args,scope,history):
        res = self.EvalElementOperation(context, args, scope, QrySegTypes.MUL, self.mulEvaluators,history)
        return res
    
    def EvalDiv(self,context,args,scope,history):
        res = self.EvalElementOperation(context, args, scope, QrySegTypes.DIV, self.divEvaluators,history)
        return res
    
    
    def EvalCsp(self,context,args,scope,history):
        res = self.EvalListOfElementsOperation(context, args, scope, QrySegTypes.CSP, self.cspEvaluator,history)
        return res
    
    def EvalIts(self,context,args,scope,history):
        res = self.EvalListOfElementsOperation(context, args, scope, QrySegTypes.ITS, self.itsEvaluator,history)
        return res
    
    def EvalDif(self,context,args,scope,history):
        res = self.EvalListOfElementsOperation(context, args, scope, QrySegTypes.ITS, self.difEvaluator,history)
        return res
    
    def EvalUni(self,context,args,scope,history):
        res = self.EvalListOfElementsOperation(context, args, scope, QrySegTypes.UNI, self.uniEvaluator,history)
        return res
    
    def EvalCon(self,context,args,scope,history):
        res = self.EvalListOfElementsOperation(context, args, scope, QrySegTypes.CON, self.conEvaluator,history)
        return res
    
    '''
        PRIVATE METHODS
    '''
   
    def EvalElementOperation(self,context,args,scope,operator,opEvaluators,history):  
        res = None
        #Define operators
        def opEqualListsFunc(a,b,c):
            return opEvaluators[type(a)](a,b)
        def opOnlyOp1ListFunc(a,b,c):
            op1Functor = lambda o1,o2: opEvaluators[type(o1)](o1,o2)
            return ApplyToAllElementsInB(a,b,op1Functor)
        def opOnlyOp2ListFunc(a,b,c):
            op2Functor = lambda o1,o2: opEvaluators[type(o1)](o1,o2)
            return ApplyToAllElementsInA(a,b,op2Functor)
    
        op1 = context
        op2 = self.EvalOnContextAndScope(context,args,scope,history)
        
        try:
            res = ApplyToSimilarElementStrutures(op1, op2, opEqualListsFunc, opOnlyOp1ListFunc, opOnlyOp2ListFunc)
        except Exception as e:
            raise EoqError(0,"Failed to evaluate %s. Context and arguments must be single elements or arrays of same type and size, but got %s %s %s: %s"%(operator,op1,operator,op2,str(e)))
        return res

    def EvalListOfElementsOperation(self,context,args,scope,operator,opEvaluator,history):  
        res = None
        #Define operators
        def opEqualListsFunc(a,b,c):
            return opEvaluator(a,b)
        def opOnlyOp1ListFunc(a,b,c):
            return ApplyToAllElementsInB(a,b,opEvaluator)
        def opOnlyOp2ListFunc(a,b,c):
            return ApplyToAllElementsInA(a,b,opEvaluator)
    
        op1 = context
        op2 = self.EvalOnContextAndScope(context,args,scope,history)
        
        try:
            res = ApplyToSimilarListsOfObjects(op1, op2, opEqualListsFunc, opOnlyOp1ListFunc, opOnlyOp2ListFunc)
        except Exception as e:
            raise EoqError(0,"Failed to evaluate %s. Context and arguments must be single elements or arrays of same type and size, but got %s %s %s: %s"%(operator,op1,operator,op2,str(e)))
        return res
    
    def _Flatten(self,src,target):
        for x in src:
            if(IsList(x)):
                self._Flatten(x, target)
            else: 
                target.append(x)
                