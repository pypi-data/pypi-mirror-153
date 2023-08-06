/* ecoreSync EOQ2 QueryObserver */
/* This ecoreSync queryObserver enables local EOQ2 query observance */

/* The ecoreSync queryObserver is based on the pyeoq2 queryRunner. The original python code was written by Björn Annighöfer */
/* ecoreSync provides a mdbAccessor and mdbObserver to enable hybrid (local/remote) query evaluation */
/* (C) 2020 Instiute of Aircraft Systems, Matthias Brunner */

import EsQueryEvaluator from '../queries/esQueryEvaluator.js'
import EsMdbObserver from '../mdb/esMdbObserver.js'
import EsQueryObserverState from './esQueryObserverState.js'

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

export default class EsQueryObserver extends EsQueryEvaluator{
    constructor(esDomain){
        super(esDomain.mdbAccessor);
        this.esDomain=esDomain;
        this.mdbAccessor=this.esDomain.mdbAccessor;
        this.mdbObserver=new EsMdbObserver(this.esDomain);
        this.observerState=new EsQueryObserverState(); 

        /* Evaluator function, that the Query observer specifies itself */
        this.segmentEvaluators['MET'] = this.EvalMet.bind(this)
        this.metEvaluators[QryMetaSegTypes.IFF] = this.EvalMetIff.bind(this)  
        this.segmentEvaluators['ADD'] = this.EvalAdd.bind(this)
    }

    async Eval(qry,callback,decode=true)
    {
        var self=this;
        if(!callback) { console.trace();  throw 'callback undefined (EVAL)'}
        var res=null
        var modelroot = await this.mdbAccessor.GetRoot()
        var context = modelroot
        var res=await this.EvalOnContextAndScope(context,qry,context,history,async function(results){             
            var decodedRes=await ApplyToAllElements(results,self.esDomain.utils.decode.bind(self.esDomain.utils));
            if(self.observerState.update(decodedRes))
            {
                if(decode){
                    callback(self.observerState.getResults(),self.observerState.getDeltaPlus(),self.observerState.getDeltaMinus())
                }
                else
                {
                    let results=ApplyToAllElements(self.observerState.getResults(),self.esDomain.utils.encode.bind(self.esDomain.utils));
                    let deltaPlus=ApplyToAllElements(self.observerState.getDeltaPlus(),self.esDomain.utils.encode.bind(self.esDomain.utils));
                    let deltaMinus=ApplyToAllElements(self.observerState.getDeltaMinus(),self.esDomain.utils.encode.bind(self.esDomain.utils));
                    callback(results,deltaPlus,deltaMinus);
                }
            }                   
        });        
        var decodedRes=await ApplyToAllElements(res,self.esDomain.utils.decode.bind(self.esDomain.utils));   
        this.observerState.update(decodedRes); 
    }

    Stop(){
        this.mdbObserver.UnobserveAll();
    }

    async EvalOnContextAndScope(context,seg,scope,eoqHistory,callback)
    {
        var res = null
        if(!callback) { 
            var EvalOnContextAndScope=super.EvalOnContextAndScope.bind(this); //evaluator function
            res=EvalOnContextAndScope(context,seg,scope,eoqHistory);
        }
        else
        {    
            var t=null
            if(seg) t = seg.qry      
            if(!t)  return seg 
    
            try{        
                var evalFunction = this.segmentEvaluators[t]  
                if(!evalFunction)
                {
                    throw('eval function not found for segment type:'+t)
                }      

                var v=null;    
                if(seg){      
                    v = seg.v    
                }  

                try{
                    res = await evalFunction(context,v,scope,eoqHistory,callback)    
                }
                catch(e)
                {
                    console.error('Failed to evaluate segment. An error occured in the evaluation function '+evalFunction.name+': '+e)
                    throw e
                }
            }
            catch(e){
                console.error("Segment type error type:"+t+" "+e);
                throw e
            }           
        }

        return res  
   

    }

    async EvalPth(context,name,scope,history,callback)
    {

        var self=this;
        var superEvalPth=super.EvalPth.bind(this);
        var res = null
        if(!callback) { //console.warn('callback undefined, no observer installed');
            res=superEvalPth(context,name,scope,history);
        }
        else
        {
            var pathFunctor = async function(o){     
                var res=null;
                if(!o){ 
                    throw 'pathFunctor: object undefined, feature='+name
                }
                else
                {        
                    
                    res=await self.mdbAccessor.Get(o,name)  
                    await self.mdbObserver.Observe(o,name,async function(results){ var result=await superEvalPth(context,name,scope);  callback(result); })  
                    
                       
                }
                return res
            }        
            try{          
                res= await ApplyToAllElements(context, pathFunctor)         
            }
            catch(e){
                console.error("Error evaluating path segment "+name+": "+e)
                throw e
            }
        }
        return res   
    }

    async EvalAny(context,args,scope,eoqHistory,callback){
        var res=null;
        var self=this;
           var anyFunctor=async function(a,b){
                if(IsList(b)){
                    for(let j in b){
                        for(let i in a){               
                            if(await self.EvalEqu(a[i],b[j],scope,eoqHistory,callback)) return true 
                        } 
                    }
                }else{                    
                        for(let i in a){                           
                            if(await self.EvalEqu(a[i],b,scope,eoqHistory,callback)) return true 
                        } 
                }        
                return false
            }
    
        if(!IsList(context)){
            console.error("ANY(1): Select argument must be a single element or a list of elements but got: "+context);
        }
        var select = await this.EvalOnContextAndScope(context,args,context,eoqHistory,callback)
        if(IsList(select) && !IsListOfObjects(select)){
           console.error("ANY(2): Select argument must be a single element or a list of elements but got: "+select);
        }
        res = ApplyToAllListsOfElementsInA(context,select,anyFunctor)       

        return res
    }

    async EvalCls(context,name,scope,eoqHistory,callback){
        var res = null
        var self=this;
        
        var clsFunctor = function(o){ 
            var res=null; 
            res=self.mdbAccessor.GetAllChildrenOfType(o,name)
            return res;
        } 
        var clsFilterFunctor= async (o) => {
            return await ecoreSync.remoteExec(new eoq2.Get(new eoq2.Obj(o.v).Met('CONTAINMENTS').Sel(QRY.Pth('eType').Pth('name').Equ(name)).Idx('FLATTEN').Pth('name')))
        }


        if(context!=null)
        {
            let relevantReferenceNames=await ApplyToAllElements(context, clsFilterFunctor)

            //Brute-Force observing changes in CLS. Re-run query on every add/rem change
            await self.mdbObserver.ObserveAllChanges([eoq2.event.ChgTypes.ADD,eoq2.event.ChgTypes.REM],async function(){
                let tempRes=await ApplyToAllElements(context, clsFunctor)
                let changeDetected=false
                let resObjIds=res.map(obj => obj.v);
                let tempResObjIds=tempRes.map(obj => obj.v);            
                resObjIds.forEach(objId => {
                    if(!tempResObjIds.includes(objId)){
                        changeDetected=true
                    }
                })
                tempResObjIds.forEach(objId => {
                    if(!resObjIds.includes(objId)){
                        changeDetected=true
                    }
                })
                if(changeDetected){
                    res=tempRes
                    callback(res)                
                }
            },(change)=>{return relevantReferenceNames.includes(change.data[3])})
            
            try{
                res = await ApplyToAllElements(context, clsFunctor)
            }
            catch(e){
                console.error("Error evaluating class segment "+name+": "+e)
                throw e
            }
        }
        return res
    }

    async EvalIno(context,name,scope,eoqHistory,callback){
        var res = null
        var self=this;
        var inoFunctor = function(o){ return self.mdbAccessor.GetAllChildrenInstanceOfClass(o,name) } 
        var inoFilterFunctor= async (o) => {
            return await ecoreSync.remoteExec(new eoq2.Get(new eoq2.Obj(o.v).Met('CONTAINMENTS').Sel(QRY.Pth('eType').Met('IMPLEMENTERS').Pth('name').Any(name).Orr(QRY.Pth('eType').Pth('name').Equ(name))).Idx('FLATTEN').Pth('name')))
        }

        let relevantReferenceNames=await ApplyToAllElements(context, inoFilterFunctor)

        //Brute-Force observing changes in INO. Re-run query on every add/rem change
        await self.mdbObserver.ObserveAllChanges([eoq2.event.ChgTypes.ADD,eoq2.event.ChgTypes.REM],async function(){
            let tempRes=await ApplyToAllElements(context, inoFunctor)
            let changeDetected=false
            let resObjIds=res.map(obj => obj.v);
            let tempResObjIds=tempRes.map(obj => obj.v);            
            resObjIds.forEach(objId => {
                if(!tempResObjIds.includes(objId)){
                    changeDetected=true
                }
            })
            tempResObjIds.forEach(objId => {
                if(!resObjIds.includes(objId)){
                    changeDetected=true
                }
            })
            if(changeDetected){
                res=tempRes
                callback(res)                
            }
        },(change)=>{ return relevantReferenceNames.includes(change.data[3]) })
        
        try{
            res = await ApplyToAllElements(context, inoFunctor)
        }
        catch(e){
            console.error("Error evaluating INO segment "+name+": "+e)
            throw e
        }
        return res
    }
    

    async EvalTrm(context,args,scope,eoqHistory,callback){
        var res = null
        var superEvalTrm=super.EvalTrm.bind(this);

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
            var res=[];
            b.forEach(function(e,i){
                res.push(TrmOperator(a[i],e,c));
            })
            return res
        }
        var TrmElemVsStructFunc=function(a,b,c){
            throw "Error applying termination: Argument of termination condition must be of lower depth than the context, but got "+a+","+b+","+c
        }
        var TrmStructVsElemFunc=function(a,b,c){
            var res=[];
            b.forEach(function(e,i){
                res.push(TrmOperator(a[i],e,c));
            })
            return res
        }
        //Begin of function
        var condquery = args[0]
        if(!condquery){ //special default case
            condquery = new eoq2.Qry().Equ(null)
        }

        var onChange=async function(results){
            var res=await superEvalTrm(context,args,eoqHistory);
            callback(res);
        }

        var defaultVal = await this.EvalOnContextAndScope(context,args[1],context,eoqHistory,onChange)  
        var condition = await this.EvalOnContextAndScope(context,condquery,context,eoqHistory,onChange)
        


        try{
            res = ApplyToSimilarListsOfObjects([context],[condition],TrmElemVsElemFunc,TrmElemVsStructFunc,TrmStructVsElemFunc,defaultVal)
        }
        catch(e){
            throw "Failed evaluating terminator "+args+". Terminator condition context and argument must be arrays of similar structure. Argument must be either be an array of Bool, but got "+condition+": "+e
        }
        
        return res[0] //return the first element because context and condition were listified above
    }

    async EvalQry(context,args,scope,history,callback)
    {
        var EvalQry=super.EvalQry.bind(this)  //evaluator function
        var self=this;
        var res = null
        if(!callback) { 
            //console.warn('callback undefined, no observer installed');
            res=EvalQry(context,args,scope,history);
        }
        else
        {
            var currentContext = scope //each subquery restarts from the current scope
            
        
            var segmentCallback=function(seg){  

                //This is the segment callback of segment #seg indexed in args
                //The segment returns its new results and the successor should be evaluated using this new result
                //if the segment is the end of the query, we directly call the callback

                var evalStartSeg=seg+1; //therefore we start evaluation after his segment

                if(evalStartSeg<args.length)
                {
                    //there are successors
                    return async function(results){
                        //evaluate all successors (there should be a way to prevent multiple cb registration during this evaluation)
                        //e.g. the first time there should be a registration, but not afterwards

                        var currentContext=results;            
                        var res=null;
                        if(!args[evalStartSeg])
                        {       
                            throw('Segment evaluation error: no such segment')
                        }  

                        for(let i=evalStartSeg; i<args.length; i++)
                        {                
                            if(currentContext instanceof Terminator){ break; }
                            currentContext = await self.EvalOnContextAndScope(currentContext,args[i],scope,history,segmentCallback(i))
                        }

                        res = Determinate(currentContext) //not sure if this is working in this context
                        
                        callback(res); 
                    }
                }
                else
                {
                    //there are no successors, then then we can return the Query results directly
                    return async function(results){
                        callback(results);
                    }
                }
            }

            var currentContext = scope //each subquery restarts from the current scope
            //var newScope = context
            for(let i=0; i<args.length; i++){       
                if(currentContext instanceof Terminator){ break; }        
                currentContext = await this.EvalOnContextAndScope(currentContext,args[i],scope,history,segmentCallback(i))           
            }

            res = Determinate(currentContext)
        }
        return res      
    }

    async EvalSel(context,args,scope,eoqHistory,callback)
    {
        if(!callback) { console.trace();  throw 'callback undefined'}
        var res = []
        var SelListVsListFunc=function(a,b){  
            return a.filter(function(e,i){
                return b[i]
            })
        }
        var SelListVsStructFunc=function(a,b){
            console.error("Error applying selector: Argument of selector must be of lower depth than the context, but got:");
            console.error('a=');
            console.error(a);
            console.error('b=');
            console.error(b);
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
             select = await this.EvalOnContextAndScope(context,args,context,eoqHistory,function(select){
                var res=[];
                try{
                    res = ApplyToSimilarListsOfObjects(context,select,SelListVsListFunc,SelListVsStructFunc,SelStructVsListFunc)
                }catch(e){
                    console.error("Failed evaluating selector during callback: "+args+". Selectors context and argument must be arrays of similar structure. Argument must be either be an array of Bool, but got "+select+": "+e)
                    throw e
                }     
                callback(res) //callback toward parent           
            })             
        }
        catch(e)
        {
            console.error('Select evaluation failed: '+e)
        }

        try{ 
            res = ApplyToSimilarListsOfObjects(context,select,SelListVsListFunc,SelListVsStructFunc,SelStructVsListFunc)
        }catch(e){
            console.error("Failed evaluating selector "+args+". Selectors context and argument must be arrays of similar structure. Argument must be either be an array of Bool, but got "+select+": "+e)
            throw e
        }        
   
        return res
    }

    async EvalEqu(context,args,scope,eoqHistory,callback){
        var res = await this.EvalElementOperation(context, args, scope, 'EQU', this.equEvaluators,eoqHistory,callback)
        return res
    }
    
    async EvalNeq(context,args,scope,eoqHistory,callback){
        var res = await this.EvalElementOperation(context, args, scope,'NEQ', this.neqEvaluators,eoqHistory,callback)
        return res
    }

    async EvalMul(context,args,scope,eoqHistory,callback){
        var res = this.EvalElementOperation(context, args, scope, 'MUL', this.mulEvaluators,eoqHistory,callback)
        return res
    }

    async EvalIdx(context,args,scope,eoqHistory,callback){
        var self=this;
        var res = null
        if(!IsList(context)){
            throw 'IDX: Can only select from lists but got: '+context
        }
        var n = await this.EvalOnContextAndScope(context,args,context,eoqHistory,function(){ console.warn('no callback implemented for EvalIdx'); })
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

    async EvalMet(context,args,scope,eoqHistory,callback){
        var res = null
        try{
            var name = args[0]
            var metEvaluator = this.metEvaluators[name]
            var res = await metEvaluator(context,args,scope,eoqHistory,callback)
        }
        catch(e){
            throw "Failed to evaluate meta segment "+name+": "+e;
        }

        return res
    }

    async EvalMetIff(context,args,scope,eoqHistory,callback){ 

        var self=this
        var EvalOnContextAndScope=super.EvalOnContextAndScope.bind(self); //evaluator function

        var condition = await this.EvalOnContextAndScope(context,args[1],context,eoqHistory,async (condition) => {
            var res = null;
            if(condition){
                res = await EvalOnContextAndScope(context,args[2],context,eoqHistory)
            }else{
                res = await EvalOnContextAndScope(context,args[3],context,eoqHistory)
            }
            callback(res);
        })
        
        var res = null;
        if(condition){
            res = await this.EvalOnContextAndScope(context,args[2],context,eoqHistory,(res) => {
                let condition=EvalOnContextAndScope(context,args[1],context,eoqHistory);
                if(condition) callback(res);
            })
        }else{
            res = await this.EvalOnContextAndScope(context,args[3],context,eoqHistory,(res) => {
                let condition=EvalOnContextAndScope(context,args[1],context,eoqHistory);
                if(!condition) callback(res);
            })
        }
        return res
    }

    EvalAdd(context,args,scope,eoqHistory,callback){
        var res = this.EvalElementOperation(context, args, scope, 'ADD', this.addEvaluators,eoqHistory,callback)
        return res
    }
    /* Private Methods */

    async EvalElementOperation(context,args,scope,operator,opEvaluators,eoqHistory,callback){
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
            
            var elementOperationCallback=function(op2){
                let res=null
                try{
                    res=ApplyToSimilarElementStrutures(op1, op2, opEqualListsFunc, opOnlyOp1ListFunc, opOnlyOp2ListFunc)
                }
                catch(e)
                {
                    console.error("Failed to evaluate "+operator+" in callback. Context and arguments must be single elements or arrays of same type and size, but got "+op1+" "+op2+" "+ operator +" :"+e)  
                }
                callback(res)
            }

            var op2 = await this.EvalOnContextAndScope(context,args,scope,eoqHistory,elementOperationCallback)
            try{
                res = ApplyToSimilarElementStrutures(op1, op2, opEqualListsFunc, opOnlyOp1ListFunc, opOnlyOp2ListFunc)
            }
            catch(e){
                console.error("Failed to evaluate "+operator+". Context and arguments must be single elements or arrays of same type and size, but got "+op1+" "+op2+" "+ operator +" :"+e)
            }
            return res
    }  

}