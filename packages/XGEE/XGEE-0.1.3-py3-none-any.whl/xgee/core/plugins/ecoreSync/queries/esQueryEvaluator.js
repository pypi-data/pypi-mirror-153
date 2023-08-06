/* ecoreSync EOQ2 queryEvaluator */
/* This ecoreSync queryEvaluator enables local EOQ2 queries on ecoreSync */

/* The ecoreSync queryEvaluator is based on the pyeoq2 queryEvaluator. The original python code was written by Björn Annighöfer */
/* ecoreSync provides a mdbAccessor to enable hybrid (local/remote) query evaluation */
/* (C) 2020 Instiute of Aircraft Systems, Matthias Brunner */

var QryMetaSegTypes={
    CLS : 'CLASS',  //class
    CLN : 'CLASSNAME',  //class name
    CON : 'CONTAINER',  //parent (container)
    PAR : 'PARENT',  //parent (container)
    ALP : 'ALLPARENTS',  //parent (container)
    ASO : 'ASSOCIATES',  //ASSOCIATES(start:root) all elements refering to this one beginning at start. default is root
    IDX : 'INDEX',  //index within its containment
    CFT : 'CONTAININGFEATURE',  //the feature that contains the element
    FEA : 'FEATURES',  //all features
    FEV : 'FEATUREVALUES',  //all feature values
    FEN : 'FEATURENAMES',  //all feature names
    ATT : 'ATTRIBUTES',  //all attribute features
    ATN : 'ATTRIBUTENAMES',  //all attribute feature names
    ATV : 'ATTRIBUTEVALUES',  //all attribute feature values
    REF : 'REFERENCES',  //all reference features
    REN : 'REFERENCENAMES',  //all reference feature names
    REV : 'REFERENCEVALUES',  //all reference feature values
    CNT : 'CONTAINMENTS',  //all containment features
    CNV : 'CONTAINMENTVALUES',  //all containment feature values
    CNN : 'CONTAINMENTNAMES',  //all containment feature names
    
    //class operators
    PAC : 'PACKAGE',  //class
    STY : 'SUPERTYPES',  //directly inherited classes
    ALS : 'ALLSUPERTYPES',  //all and also indirectly inherited classes
    IMP : 'IMPLEMENTERS',  //all direct implementers of a class
    ALI : 'ALLIMPLEMENTERS',  //all and also indirect implementers of a class  
    MMO : 'METAMODELS',  //retrieve all metamodels
    
     //Control flow operators 
    IFF : 'IF',  //if(condition,then,else); ,  //DEPRICATED
    TRY : 'TRY',  //catch errors and return a default,  //NOT IMPLEMENTED        
    
    //list operators
    LEN : 'SIZE',  //size of a list,  //DEPRICATED
    
    //recursive operators
    REC : 'REPEAT',  //REPEAT(<query>,depth) repeat a given query until no more results are found,  //NOT IMPLEMENTED    
}

export default class EsQueryEvaluator{
    constructor(mdbAccessor)
    {
        this.mdbAccessor=mdbAccessor

        //Terminator operation
        var oprTrm=(a,b) => a //do nothing


        //equals Operations
        var equBol= (a,b) => a==b            
        var equInt= (a,b) => a==b
        var equStr= (a,b) => a==b
        var equFlo= (a,b) => a==b
        var equObj= (a,b) => { if(a && b){ return a.v==b.v }else { return !a && !b} }
        this.equEvaluators = {bool: equBol, int: equInt, str: equStr, float: equFlo, ObjSeg: equObj,Terminator: oprTrm} //TODO: does probably not work for queries decoded from JSON

        //not equals Operations
        var neqBol= (a,b) => a!=b            
        var neqInt= (a,b) => a!=b
        var neqStr= (a,b) => a!=b
        var neqFlo= (a,b) => a!=b
        var neqObj= (a,b) => { if(a && b){ return a.v!=b.v }else { return !(!a && !b)}}
        this.neqEvaluators = {bool: neqBol, int: neqInt, str: neqStr, float: neqFlo, ObjSeg: neqObj,Terminator: oprTrm} //TODO: does probably not work for queries decoded from JSON

        //greater Operations
        var greBol= (a,b) => a>b            
        var greInt= (a,b) => a>b
        var greStr= (a,b) => a>b
        var greFlo= (a,b) => a>b
        var greObj= (a,b) => a.v>b.v
        this.greEvaluators = {bool: greBol, int: greInt, str: greStr, float: greFlo, ObjSeg: greObj,Terminator: oprTrm} //TODO: does probably not work for queries decoded from JSON

        //less Operations
        var lesBol= (a,b) => a<b            
        var lesInt= (a,b) => a<b
        var lesStr= (a,b) => a<b
        var lesFlo= (a,b) => a<b
        var lesObj= (a,b) => a.v<b.v
        this.lesEvaluators = {bool: lesBol, int: lesInt, str: lesStr, float: lesFlo, ObjSeg: lesObj,Terminator: oprTrm} //TODO: does probably not work for queries decoded from JSON

        //add Operations
        var addBol= (a,b) => a||b            
        var addInt= (a,b) => a+b
        var addStr= (a,b) => a+b
        var addFlo= (a,b) => a+b
        var addObj= (a,b) => [a,b]
        this.addEvaluators = {bool: addBol, int: addInt, str: addStr, float: addFlo, ObjSeg: addObj,Terminator: oprTrm} //TODO: does probably not work for queries decoded from JSON

        //sub Operations
        var subBol= (a,b) => (!a&&b)||(a&&!b)            
        var subInt= (a,b) => a-b
        var subStr= (a,b) => a-b
        var subFlo= (a,b) => a-b
        var subObj= (a,b) => [a,b]
        this.subEvaluators = {bool: subBol, int: subInt, str: subStr, float: subFlo, ObjSeg: subObj,Terminator: oprTrm} //TODO: does probably not work for queries decoded from JSON

        //mul Operations
        var mulBol= (a,b) => (a&&b)            
        var mulInt= (a,b) => a*b
        var mulStr= (a,b) => a+b
        var mulFlo= (a,b) => a*b
        var mulObj= (a,b) => [a,b]
        this.mulEvaluators = {bool: mulBol, int: mulInt, str: mulStr, float: mulFlo, ObjSeg: mulObj,Terminator: oprTrm} //TODO: does probably not work for queries decoded from JSON

        //div Operations
        var divBol= (a,b) => !(a&&b)            
        var divInt= (a,b) => parseInt(a/b)
        var divStr= (a,b) => a+b
        var divFlo= (a,b) => a/b
        var divObj= (a,b) => [a,b]
        this.divEvaluators = {bool: divBol, int: divInt, str: divStr, float: divFlo, ObjSeg: divObj,Terminator: oprTrm} //TODO: does probably not work for queries decoded from JSON

        /* Operator and Evaluator Registration */
        /* Segment Operators */

        this.segmentEvaluators={};      
        this.segmentEvaluators['OBJ'] = this.EvalObj.bind(this)
        this.segmentEvaluators['HIS'] = this.EvalHis.bind(this)
        this.segmentEvaluators['PTH'] = this.EvalPth.bind(this)
        this.segmentEvaluators['CLS'] = this.EvalCls.bind(this)
        this.segmentEvaluators['INO'] = this.EvalIno.bind(this)
        this.segmentEvaluators['MET'] = this.EvalMet.bind(this)
        this.segmentEvaluators['TRM'] = this.EvalTrm.bind(this)

        this.segmentEvaluators['IDX'] = this.EvalIdx.bind(this)
        this.segmentEvaluators['SEL'] = this.EvalSel.bind(this)
        this.segmentEvaluators['ARR'] = this.EvalArr.bind(this)
        this.segmentEvaluators['QRY'] = this.EvalQry.bind(this);

        this.segmentEvaluators['ANY'] = this.EvalAny.bind(this)
        this.segmentEvaluators['ALL'] = this.EvalAll.bind(this)
        
        this.segmentEvaluators['EQU'] = this.EvalEqu.bind(this)
        this.segmentEvaluators['NEQ'] = this.EvalNeq.bind(this)
        this.segmentEvaluators['GRE'] = this.EvalGre.bind(this)
        this.segmentEvaluators['LES'] = this.EvalLes.bind(this)
        

        //synonyms for boolean operations
        this.segmentEvaluators['ORR'] = this.EvalAdd.bind(this)
        this.segmentEvaluators['XOR'] = this.EvalSub.bind(this)
        this.segmentEvaluators['AND'] = this.EvalMul.bind(this)
        this.segmentEvaluators['NAD'] = this.EvalDiv.bind(this)


        this.segmentEvaluators['ADD'] = this.EvalAdd.bind(this)
        this.segmentEvaluators['SUB'] = this.EvalSub.bind(this)
        this.segmentEvaluators['MUL'] = this.EvalMul.bind(this)
        this.segmentEvaluators['DIV'] = this.EvalDiv.bind(this)
        
        this.segmentEvaluators['CSP'] = this.EvalCsp.bind(this)
        this.segmentEvaluators['ITS'] = this.EvalIts.bind(this)
        this.segmentEvaluators['UNI'] = this.EvalUni.bind(this)
        this.segmentEvaluators['CON'] = this.EvalCon.bind(this)


        /* Meta Operators */
        this.metEvaluators = {} 
        this.metEvaluators[QryMetaSegTypes.CLS] = this.EvalMetCls.bind(this)
        this.metEvaluators[QryMetaSegTypes.CLN] = this.EvalMetCln.bind(this)
        this.metEvaluators[QryMetaSegTypes.LEN] = this.EvalMetLen.bind(this)
        this.metEvaluators[QryMetaSegTypes.PAR] = this.EvalMetPar.bind(this)
        this.metEvaluators[QryMetaSegTypes.CON] = this.EvalMetPar.bind(this) //container is the same as parent
        this.metEvaluators[QryMetaSegTypes.ALP] = this.EvalMetAlp.bind(this)
        this.metEvaluators[QryMetaSegTypes.IDX] = this.EvalMetIdx.bind(this)
        this.metEvaluators[QryMetaSegTypes.ASO] = this.EvalMetAso.bind(this)
        this.metEvaluators[QryMetaSegTypes.CFT] = this.EvalMetCft.bind(this)
        this.metEvaluators[QryMetaSegTypes.FEA] = this.EvalMetFea.bind(this)
        this.metEvaluators[QryMetaSegTypes.FEN] = this.EvalMetFen.bind(this)
        this.metEvaluators[QryMetaSegTypes.FEV] = this.EvalMetFev.bind(this)
        this.metEvaluators[QryMetaSegTypes.ATT] = this.EvalMetAtt.bind(this)
        this.metEvaluators[QryMetaSegTypes.ATN] = this.EvalMetAtn.bind(this)
        this.metEvaluators[QryMetaSegTypes.ATV] = this.EvalMetAtv.bind(this)
        this.metEvaluators[QryMetaSegTypes.REF] = this.EvalMetRef.bind(this)
        this.metEvaluators[QryMetaSegTypes.REN] = this.EvalMetRen.bind(this)
        this.metEvaluators[QryMetaSegTypes.REV] = this.EvalMetRev.bind(this)
        this.metEvaluators[QryMetaSegTypes.CNT] = this.EvalMetCnt.bind(this)
        this.metEvaluators[QryMetaSegTypes.CNN] = this.EvalMetCnn.bind(this)
        this.metEvaluators[QryMetaSegTypes.CNV] = this.EvalMetCnv.bind(this)

        /* Class meta Operators */
        this.metEvaluators[QryMetaSegTypes.PAC] = this.EvalMetPac.bind(this)
        this.metEvaluators[QryMetaSegTypes.STY] = this.EvalMetSty.bind(this)
        this.metEvaluators[QryMetaSegTypes.ALS] = this.EvalMetAls.bind(this)
        this.metEvaluators[QryMetaSegTypes.IMP] = this.EvalMetImp.bind(this)
        this.metEvaluators[QryMetaSegTypes.ALI] = this.EvalMetAli.bind(this)

        /* Control flow Operators */
        this.metEvaluators[QryMetaSegTypes.IFF] = this.EvalMetIff.bind(this)   
    }

    cspUni(a,b){
        var res = []
        for(e1 in a){
            for(e2 in b){            
                res.push([e1,e2])
            }
        }
        return res
    }

    itsUni(a,b){
        var res = []
        //add common elements
        for(e1 in a)
        {
            notFoundInRes = true //uniquenes
            foundInB = false //commons
            for(r in res)
            {
                if(this.equEvaluators[self._type(e1)](e1,r)){
                    notFoundInRes = false
                    break
                }
            }
            for(e2 in b)
            {
                if(this.equEvaluators[self._type(e1)](e1,e2)){
                    foundInB = true
                    break
                }
            }
            if(notFoundInRes && foundInB) res.push(e1)      
        }
        return res
    }

    uniUni(a,b){
        res = []
        //add all unique elments of a
        for(e in a){
            notFound = true
            for(r in res){
                if(this.equEvaluators[this._type(e)](e,r)){
                    notFound = false
                    break
                }              
            }   
            if(notFound) res.push(e)        
        }
        //add all unique elments of b
        for(e in b){
            notFound = true
            for(r in res){
                if(this.equEvaluators[this._type(e)](e,r)){
                    notFound = false
                    break
                }                    
                if(notFound) res.push(e)
            }
        }
        return res
    }

    conUni(a,b){
        res = []
        res.concat(a)
        res.concat(b)
        return res
    }

    async Eval(qry,eoqHistory=[]){
        var res=null
        var modelroot = await this.mdbAccessor.GetRoot()
        var context = modelroot
        try{
             res=await this.EvalOnContextAndScope(context,qry,context,eoqHistory)
        }catch(e){
            throw 'Could not evaluate query:'+e
        }
        return res
    }

    async EvalOnContextAndScope(context,seg,scope,eoqHistory){
  
        var res = null
        var t=null
        if(seg) t = seg.qry      
        if(!t)  return seg 
 
        try{        
            var evalFunction = this.segmentEvaluators[t]  
            if(!evalFunction)
            {
                throw('FATAL ERROR: eval function not found for segment type:'+t)
            }      

            var v=null;    
            if(seg){      
                 v = seg.v    
            }  

            try{
                res = await evalFunction(context,v,scope,eoqHistory)    
            }
            catch(e)
            {
                console.error('Failed to evaluate segment. An error occured in the evaluation function '+evalFunction.name+': '+e)
                console.error(context);
                console.error(seg);
                console.error(scope);
                console.error(eoqHistory);
                throw e
            }
        }
        catch(e){
             throw 'Evaluation failed:'+e
         }           
        
        return res   
    }

    /* Segment evaluators */

    async EvalQry(context,args,scope,eoqHistory){
        var res = null
        var currentContext = scope //each subquery restarts from the current scope
        //var newScope = context
        for(let seg in args){      
            if(currentContext instanceof Terminator){ break; }
            try{           
                currentContext = await this.EvalOnContextAndScope(currentContext,args[seg],scope,eoqHistory)
            }
            catch(e)
            {
                throw 'Query failed: '+e
            }
        }
        res = Determinate(currentContext)
        return res
    }

    EvalObj(context,v,scope,eoqHistory){
        if(!Number.isInteger(v)) throw 'FATAL ERROR: Invalid object id, expected Integer got:'+v
        return {qry:"OBJ",v:v} //because the argument is unpacked before, hard coded?
    }

    EvalHis(context,n,scope,eoqHistory){
        var res = null
        var idx=n;
        if(n<0){ idx=eoqHistory.length+n};
        if(idx>=0)
        {
            res = eoqHistory[idx]
        }
        else
        {
            throw "Error evaluating eoqHistory "+n+". Current eoqHistory has a length of "+eoqHistory.length
        }
        return res
    }

    async EvalPth(context,name,scope,eoqHistory){
        var self=this;
        var res = null
        var pathFunctor = async function(o){ 
            if(o==null) throw 'FATAL ERROR: path functor evaluation failure ('+name+'). Argument is null'
            var res=await self.mdbAccessor.Get(o,name)
            return res
        }
        try{               
            res= await ApplyToAllElements(context, pathFunctor)  
        }
        catch(e){ 
            throw 'Path failure:'+e
        }
        return res
    }
 
    async EvalCls(context,name,scope,eoqHistory){
        var res = null
        var self=this;
        var clsFunctor = function(o){ return self.mdbAccessor.GetAllChildrenOfType(o,name) } 
        
        try{
            res = await ApplyToAllElements(context, clsFunctor)
        }
        catch(e){
            console.error("Error evaluating class segment "+name+": "+e)
            throw e
        }
        return res
    }
  
    async EvalIno(context,name,scope,eoqHistory){
        var res = null
        var self=this;
        var inoFunctor = function(o){ return self.mdbAccessor.GetAllChildrenInstanceOfClass(o,name) } 
        
        try{
            res = await ApplyToAllElements(context, inoFunctor)
        }
        catch(e){
             console.error("Error evaluating instance of segment "+name+": "+e)
             throw e
        }
        return res
    }

    async EvalSel(context,args,scope,eoqHistory){ 
        
        var res = []
        var SelListVsListFunc=function(a,b){  
            return a.filter(function(e,i){
                return b[i]
            })
        }
        var SelListVsStructFunc=function(a,b){
            console.error("Error applying selector: Argument of selector must be of lower depth than the context, but got "+a+";"+b);
        }
        var SelStructVsListFunc=function(a,b){
            return a.filter(function(e,i){
                return b[i]
            })
        }

        //Start Select evaluation        
        //selector changes the context
        var select=null
        try{
            if(IsNoList(context)) throw 'FATAL ERROR: expected list-typed context in selector segment'
             select = await this.EvalOnContextAndScope(context,args,context,eoqHistory)
             
        }
        catch(e)
        {
            throw 'Selection failed:'+e
        }

        try{
            res = ApplyToSimilarListsOfObjects(context,select,SelListVsListFunc,SelListVsStructFunc,SelStructVsListFunc)
        }catch(e){           
            throw 'Selection failed: '+e
        }
        
        return res
    }

    async EvalTrm(context,args,scope,eoqHistory){
        var res = null
        //Define select functors
        var TrmOperator=function(a,b,c){
            var res = null;
            if(a instanceof Terminator){
                res = a
            }else if(b){
                res = new Terminator(c)
            }else{
                res = a
            }
            return res
        }
        var TrmElemVsElemFunc=function(a,b,c){            
            var res=b.map((e,i) => TrmOperator(a[i],b[i],c));           
            return res
        }
        var TrmElemVsStructFunc=function(a,b,c){
            throw "Error applying termination: Argument of termination condition must be of lower depth than the context, but got "+a+","+b+","+c
        }
        var TrmStructVsElemFunc=function(a,b,c){
            var res=b.map((e,i) => TrmOperator(a[i],e,c));            
            return res
        }
        //Begin of function
        var condquery = args[0]
        if(!condquery){ //special default case
            condquery = new eoq2.Qry().Equ(null)
        }
        var condition = await this.EvalOnContextAndScope(context,condquery,context,eoqHistory)
        var defaultVal = await this.EvalOnContextAndScope(context,args[1],context,eoqHistory)  
        try{
            res = ApplyToSimilarListsOfObjects([context],[condition],TrmElemVsElemFunc,TrmElemVsStructFunc,TrmStructVsElemFunc,defaultVal)
        }
        catch(e){
            throw "Failed evaluating terminator "+args+". Terminator condition context and argument must be arrays of similar structure. Argument must be either be an array of Bool, but got "+condition+": "+e
        }        

        return res[0] //return the first element because context and condition were listified above
    }



    async EvalArr(context,args,scope,eoqHistory){
        var self=this;
        var res = []
        for(let arg of args)
        {
            res.push(self.EvalOnContextAndScope(context,arg,context,eoqHistory) )
        }      
        return await Promise.all(res)
    }
 
    async EvalMet(context,args,scope,eoqHistory){
        var res = null
        try{
            var name = args[0]
            var metEvaluator = this.metEvaluators[name]
            var res = await metEvaluator(context,args,scope,eoqHistory)
        }
        catch(e){
            throw "Failed to evaluate meta segment "+name+": "+e;
        }

        return res
    }

    async EvalAll(context,args,scope,eoqHistory){
        throw 'Not implemented'
    }

    async EvalAny(context,args,scope,eoqHistory){
        var res=null;
        var self=this;
           var anyFunctor=async function(a,b){
                if(IsList(b)){
                    for(let j in b){
                        for(let i in a){               
                            if(await self.EvalEqu(a[i],b[j],scope,eoqHistory)) return true 
                        } 
                    }
                }else{                    
                        for(let i in a){
                            //let res=await self.EvalEqu(a[i],b,scope,eoqHistory)
                            if(await self.EvalEqu(a[i],b,scope,eoqHistory)) return true 
                        } 
                }        
                return false
            }
    
        if(!IsList(context)){
            console.error("ANY(1): Select argument must be a single element or a list of elements but got: "+context);
        }
        var select = await this.EvalOnContextAndScope(context,args,context,eoqHistory)
        if(IsList(select) && !IsListOfObjects(select)){
           console.error("ANY(2): Select argument must be a single element or a list of elements but got: "+select);
        }
        res = ApplyToAllListsOfElementsInA(context,select,anyFunctor)
        return res
    }

    /* Meta evaluators */

    async EvalMetCls(context,args,scope,eoqHistory){
        var self=this;
        if(args.length==1)
        {
            var clsFunctor = (a,b) => self.mdbAccessor.Class(a)
            var res = ApplyToAllElementsInA(context,null,clsFunctor)
        }
        else
        {
            var packageName=await self.EvalOnContextAndScope(context,args[1],context,eoqHistory)
            var className=await self.EvalOnContextAndScope(context,args[2],context,eoqHistory)       

            if(typeof packageName == 'string' && typeof className == 'string'  )
            {        
                res=self.mdbAccessor.GetClassByName(packageName,className)
            }
          
        }
        return awaitAll(res);
    }
 
    async EvalMetCln(context,args,scope,eoqHistory){
        var self=this;
        var clnFunctor = (a,b) => self.mdbAccessor.ClassName(a)
        var res = ApplyToAllElementsInA(context,null,clnFunctor)         
        return awaitAll(res);
    }

    EvalMetLen(context,args,scope,eoqHistory){
        var lenFunctor = (a,b) => a.length
        var res = ApplyToAllListsOfElementsInA(context,null,lenFunctor)
        return res
    }

    EvalMetPar(context,args,scope,eoqHistory){
        var self=this;
        var parFunctor = (a,b) => self.mdbAccessor.GetParent(a)
        var res = ApplyToAllElementsInA(context,null,parFunctor)
        return res
    }
 
    EvalMetAlp(context,args,scope,eoqHistory){
        var self=this;
        var alpFunctor = (a,b) => self.mdbAccessor.GetAllParents(a)
        var res = ApplyToAllElementsInA(context,null,alpFunctor)
        return res
    }

    EvalMetAso(context,args,scope,eoqHistory){
        var self=this; 
        let root = null
        if(args && args.length>1){
            root = self.EvalOnContextAndScope(context,args[1],context,eoqHistory)
        }
        else{
            root = self.mdbAccessor.GetRoot()
        }
        var asoFunctor = (a,b) => self.mdbAccessor.GetAssociates(a,b)
        var res = ApplyToAllElementsInA(context,root,asoFunctor)
        return awaitAll(res);
    }

    EvalMetIdx(context,args,scope,eoqHistory){
        var self=this;
        var idxFunctor = (a,b) => self.mdbAccessor.GetIndex(a)
        var res = ApplyToAllElementsInA(context,null,idxFunctor)
        return res
    }

    EvalMetCft=function(context,args,scope,eoqHistory){
        var self=this;
        var cftFunctor = (a,b) => self.mdbAccessor.GetContainingFeature(a)
        var res = ApplyToAllElementsInA(context,null,cftFunctor)
        return res
    }
    
    EvalMetFea(context,args,scope,eoqHistory){
        var self=this;
        var feaFunctor = (a,b) => self.mdbAccessor.GetAllFeatures(a)
        var res = ApplyToAllElementsInA(context,null,feaFunctor)
        return res
    }

    EvalMetFen(context,args,scope,eoqHistory){
        var self=this;
        var fenFunctor = (a,b) => self.mdbAccessor.GetAllFeatureNames(a)
        var res = ApplyToAllElementsInA(context,null,fenFunctor)
        return res
    }
  
    EvalMetFev(context,args,scope,eoqHistory){
        var self=this;
        var fevFunctor = (a,b) => self.mdbAccessor.GetAllFeatureValues(a)
        var res = ApplyToAllElementsInA(context,null,fevFunctor)
        return res
    }
    
    EvalMetAtt(context,args,scope,eoqHistory){
        var self=this;
        var attFunctor = (a,b) => self.mdbAccessor.GetAllFeatures(a)
        var res = ApplyToAllElementsInA(context,null,attFunctor)
        return res
    }
    
    EvalMetAtn(context,args,scope,eoqHistory){
        var self=this;
        var atnFunctor = (a,b) => self.mdbAccessor.GetAllAttributeNames(a)
        var res = ApplyToAllElementsInA(context,null,atnFunctor)
        return res
    }
 
    EvalMetAtv(context,args,scope,eoqHistory){
        var self=this;
        var atvFunctor = (a,b) => self.mdbAccessor.GetAllFeatureValues(a)
        var res = ApplyToAllElementsInA(context,null,atvFunctor)
        return res
    }
 
    EvalMetRef(context,args,scope,eoqHistory){
        var self=this;
        var refFunctor = (a,b) => self.mdbAccessor.GetAllReferences(a)
        var res = ApplyToAllElementsInA(context,null,refFunctor)
        return res
    }

    async EvalMetRen(context,args,scope,eoqHistory){
        var self=this;
        var renFunctor = (a,b) => self.mdbAccessor.GetAllReferenceNames(a)
        var res = ApplyToAllElementsInA(context,null,renFunctor)
        return awaitAll(res);
    }
    
    EvalMetRev(context,args,scope,eoqHistory){
        var self=this;
        var revFunctor = (a,b) => self.mdbAccessor.GetAllReferenceValues(a)
        var res = ApplyToAllElementsInA(context,null,revFunctor)
        return res
    }   
    
    EvalMetCnt(context,args,scope,eoqHistory){
        var self=this;
        var cntFunctor = (a,b) => self.mdbAccessor.GetAllContainments(a)
        var res = ApplyToAllElementsInA(context,null,cntFunctor)
        return res
    }
    
    EvalMetCnn(context,args,scope,eoqHistory){
        var self=this;
        var cnnFunctor = (a,b) => self.mdbAccessor.GetAllContainmentNames(a)
        var res = ApplyToAllElementsInA(context,null,cnnFunctor)
        return res
    }  
    
    EvalMetCnv(context,args,scope,eoqHistory){
        var self=this;
        var cnvFunctor = (a,b) => self.mdbAccessor.GetAllContainmentValues(a)
        var res = ApplyToAllElementsInA(context,null,cnvFunctor)
        return res
    }

    EvalMetPac(context,args,scope,eoqHistory){
        var self=this;
        var pacFunctor = (a,b) => self.mdbAccessor.Package(a)
        var res = ApplyToAllElementsInA(context,null,pacFunctor)
        return res
    }
    
    EvalMetSty(context,args,scope,eoqHistory){
        var self=this;
        var styFunctor = (a,b) => self.mdbAccessor.Supertypes(a)
        var res = ApplyToAllElementsInA(context,null,styFunctor)
        return res
    }
    
    EvalMetAls(context,args,scope,eoqHistory){
        var self=this;
        var alsFunctor = (a,b) => self.mdbAccessor.AllSupertypes(a)
        var res = ApplyToAllElementsInA(context,null,alsFunctor)
        return awaitAll(res)
    }
    
    async EvalMetImp(context,args,scope,eoqHistory){
        var self=this;
        var impFunctor = (a,b) => self.mdbAccessor.Implementers(a)
        var res = ApplyToAllElementsInA(context,null,impFunctor)
        return res
    }

    async EvalMetAli(context,args,scope,eoqHistory){
        var self=this;
        var aliFunctor = (a,b) => self.mdbAccessor.AllImplementers(a)
        var res = ApplyToAllElementsInA(context,null,aliFunctor)
        return await res
    }
    
    async EvalMetIff(context,args,scope,eoqHistory){ 
        window["DEBUG_EVAL_EMT_IFF_CONTEXT"]=context
        try{        
            var condition = await this.EvalOnContextAndScope(context,args[1],context,eoqHistory)
        }
        catch(e){
            throw 'condition evaluation failed: '+e
        }
        var res = null;
        if(condition){
            try{
            res = await this.EvalOnContextAndScope(context,args[2],context,eoqHistory)
            }
            catch(e)
            {
                console.error(context)
                console.error(args[2])
                throw 'failed to evaluate when condition is true: '+e
            }
        }else{
            try{
            res = await this.EvalOnContextAndScope(context,args[3],context,eoqHistory)
            }
            catch(e)
            {
                throw 'failed to evaluate when condition is true: '+e
            }
        }
        return res
    }

    async EvalIdx(context,args,scope,eoqHistory){
        var self=this;
        var res = null
        if(!IsList(context)){
            throw 'IDX: Can only select from lists but got: '+context
        }
        var n = await this.EvalOnContextAndScope(context,args,context,eoqHistory)
        if(this._type(n)=='int'){
            var idxFunctor = (a,b) => a[b]
            res = ApplyToAllListsOfElementsInA(context,n,idxFunctor)
        }
        else if (this._type(n)=='str'){
            if("SORTASC"==n){
                var ascFunctor = (a,b) => a.sort()
                res = ApplyToAllListsOfElementsInA(context,null,ascFunctor)
            }
            else if("SORTDSC"==n){
                var dscFunctor = (a,b) => a.sort().reverse()
                res = ApplyToAllListsOfElementsInA(context,null,dscFunctor)
            }
            else if("FLATTEN"==n){
                if(IsList(context)){   
                    var _flatten=function(e){
                        if(Array.isArray(e))
                        {
                            return e.flatMap(_flatten)
                        }
                        else
                        {
                            return e
                        }
                    }                 
                    res=context.flatMap(_flatten)
                }
                else{
                    res = context
                }
            }
            else if("SIZE"==n){
                var lenFunctor = (a,b) => a.length
                res = ApplyToAllListsOfElementsInA(context,null,lenFunctor)
            }
            else{
                throw 'unkown index keyword: '+n
            }
        }else if(IsList(n) && n.length==3 && n[0]!=null && self._type(n[0])=="int")
        {
            var rngFunctor = (a,b) => self._range(a,b[0],b[1],b[2])
            res = ApplyToAllListsOfElementsInA(context,n,rngFunctor)
        }
        else{
            throw 'Invalid index argument, got: '+n+'('+self._type(n)+')'
        }
        return res
    }
 
    /* LOGICAL AND MATH OPERATORS */
    async EvalEqu(context,args,scope,eoqHistory){
        var res = await this.EvalElementOperation(context, args, scope, 'EQU', this.equEvaluators,eoqHistory)
        return res
    }
    
    async EvalNeq(context,args,scope,eoqHistory){
        var res = await this.EvalElementOperation(context, args, scope,'NEQ', this.neqEvaluators,eoqHistory)
        return res
    }
    
    EvalGre(context,args,scope,eoqHistory){
        var res = this.EvalElementOperation(context, args, scope, 'GRE', this.greEvaluators,eoqHistory)
        return res
    }
    
    EvalLes(context,args,scope,eoqHistory){
        var res = this.EvalElementOperation(context, args, scope, 'LES', this.lesEvaluators,eoqHistory)
        return res
    }

    EvalAdd(context,args,scope,eoqHistory){
        var res = this.EvalElementOperation(context, args, scope, 'ADD', this.addEvaluators,eoqHistory)
        return res
    }
    
    EvalSub(context,args,scope,eoqHistory){
        var res = this.EvalElementOperation(context, args, scope, 'SUB', this.subEvaluators,eoqHistory)
        return res
    }
    
    EvalMul(context,args,scope,eoqHistory){
        var res = this.EvalElementOperation(context, args, scope, 'MUL', this.mulEvaluators,eoqHistory)
        return res
    }
    
    EvalDiv(context,args,scope,eoqHistory){
        var res = this.EvalElementOperation(context, args, scope, 'DIV', this.divEvaluators,eoqHistory)
        return res
    }
    
    EvalCsp(context,args,scope,eoqHistory){
        var res = this.EvalListOfElementsOperation(context, args, scope, 'CSP', this.cspEvaluator,eoqHistory)
        return res
    }
    
    EvalIts(context,args,scope,eoqHistory){
        var res = this.EvalListOfElementsOperation(context, args, scope, 'ITS', this.itsEvaluator,eoqHistory)
        return res
    }
    
    EvalDif(context,args,scope,eoqHistory){
        var res = this.EvalListOfElementsOperation(context, args, scope, 'DIF', this.difEvaluator,eoqHistory)
        return res
    }

    EvalUni(context,args,scope,eoqHistory){
        var res = this.EvalListOfElementsOperation(context, args, scope, 'UNI', this.uniEvaluator,eoqHistory)
        return res
    }
    
    EvalCon(context,args,scope,eoqHistory){
        var res = this.EvalListOfElementsOperation(context, args, scope, 'CON', this.conEvaluator,eoqHistory)
        return res
    }

    /* Private methods */

    async EvalElementOperation(context,args,scope,operator,opEvaluators,eoqHistory){
        var self=this;
        var res = null
        //varine operators
            var opEqualListsFunc=(a,b) => opEvaluators[self._type(a)](a,b)
            var opOnlyOp1ListFunc=function(a,b){
                    op1Functor = (o1,o2) => opEvaluators[self._type(o1)](o1,o2)
                    return ApplyToAllElementsInB(a,b,op1Functor)
            }
            var opOnlyOp2ListFunc=function(a,b){ // Is this the same as above?
                    var op2Functor = (o1,o2) => opEvaluators[self._type(o1)](o1,o2)
                    return ApplyToAllElementsInA(a,b,op2Functor)
            }
            var op1 = context
            var op2 = await this.EvalOnContextAndScope(context,args,scope,eoqHistory)
            try{
                res = ApplyToSimilarElementStrutures(op1, op2, opEqualListsFunc, opOnlyOp1ListFunc, opOnlyOp2ListFunc)
            }
            catch(e){
                console.error("Failed to evaluate "+operator+". Context and arguments must be single elements or arrays of same type and size, but got "+op1+" "+op2+" "+ operator +" :"+e)
            }
            return res
    }   

    EvalListOfElementsOperation(context,args,scope,operator,opEvaluator,eoqHistory){
        var res = null
        //varine operators
        var opEqualListsFunc=(a,b) => opEvaluator(a,b)
        var opOnlyOp1ListFunc=(a,b) => ApplyToAllElementsInB(a,b,opEvaluator)
        var opOnlyOp2ListFunc=(a,b) => ApplyToAllElementsInA(a,b,opEvaluator)
        var op1 = context
        var op2 = this.EvalOnContextAndScope(context,args,scope,eoqHistory)    
        try{
            res = ApplyToSimilarListsOfObjects(op1, op2, opEqualListsFunc, opOnlyOp1ListFunc, opOnlyOp2ListFunc)
        }
        catch(e)
        {
            console.error("Failed to evaluate %s. Context and arguments must be single elements or arrays of same type and size, but got "+operator+" "+op1+" "+operator+" "+op2+" : "+e)
        }
        return res
    }
    

    _Flatten(src,target){
        for(x in src){
            if(Array.isArray(x)){
                this._Flatten(x, target)
            }
            else{
                target.push(x)
            }
        }
    }

    _type=function(v)
    {
        var res=null
        switch(typeof v)
        {
            case "boolean":
                res="bool"
                break;
            case "number":
                if(Number.isSafeInteger(v)){
                    res="int"
                } 
                else
                {
                    res="float"
                }          
                break;
            case "string":            
                res="str"
                break;
            default:
                res="ObjSeg"
                break
        }  
        return res;
    }

    _range=function(arr,start,stop,step){
        var res=[];
        arr.forEach(function(e,i){
        if(i>=start && i< stop)
        {
            if(i==start) 
            {
                res.push(e)
            }
            else
            {               
                if((i%step-start%step)==0) res.push(e);
            }
        } 
        })
        return res
    }



}
