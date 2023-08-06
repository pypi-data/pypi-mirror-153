/* ecoreSync EOQ2 Comm&&Runner */
/* This ecoreSync Comm&&Runner enables local EOQ2 comm&&s on ecoreSync */

/* The ecoreSync Comm&&Runner is based on the pyeoq2 Comm&&Runner. The original python code was written by Björn Annighöfer */
/* ecoreSync provides a mdbAccessor to enable hybrid (local/remote) comm&& && query evaluation */

/* (C) 2020 Instiute of Aircraft Systems, Matthias Brunner */

import EsQueryEvaluator from './esQueryEvaluator.js'

const CmdTypes={
    //data related commm&&s
    GET : 'GET', //get cmd
    SET : 'SET', //set cmd value
    ADD : 'ADD', //add cmd value
    REM : 'REM', //remove cmd value
    MOV : 'MOV', //move cmd cmd
    DEL : 'DEL', //delete cmd
    CLO : 'CLO', //clone source target mode
    CRT : 'CRT', //create by class
    CRN : 'CRN', //create by name
    
    //meta model related comm&&s
    GMM : 'GMM', //get meta models
    RMM : 'RMM', //register meta model
    UMM : 'UMM', //unregister meta model
    
    //maintenance related comm&&s
    HEL : 'HEL', //hello
    GBY : 'GBY', //goodbye
    SES : 'SES', //session
    STS : 'STS', //status
    CHG : 'CHG', //changes
    
    //Action related comm&&s
    GAA : 'GAA', //get all actions
    CAL : 'CAL', //call
    ASC : 'ASC', //async Call
    ABC : 'ABC', //abort call
    CST : 'CST', //call status
    
    CMP : 'CMP' //compound
}


export default class EsCmdRunner{
    constructor(esDomain,maxChanges=100){
        this.esDomain=esDomain;
        this.mdbAccessor=esDomain.mdbAccessor;

        this.qryEvaluator=new EsQueryEvaluator(esDomain.mdbAccessor);
        this.maxChanges=maxChanges;

        this.tempChangesForTransaction={}
        this.tempHistoryForTransaction={}

        this.latestTransactionId=0
        this.transactions=[]
        
        this.earliestChangeId=0
        this.latestChangeId=0
        this.changes=[]
        this.currenteoqHistoryId=0
        this.eoqHistory=[]

        this.cmdEvaluators={};
        this.cmdEvaluators[CmdTypes.CMP]=this.ExecCmp.bind(this); 
        this.cmdEvaluators[CmdTypes.GET]=this.ExecGet.bind(this); 
        this.cmdEvaluators[CmdTypes.CRN]=this.ExecCrn.bind(this); 
        this.cmdEvaluators[CmdTypes.CLO]=this.ExecClo.bind(this); 
        this.cmdEvaluators[CmdTypes.ADD]=this.ExecAdd.bind(this); 
        this.cmdEvaluators[CmdTypes.REM]=this.ExecRem.bind(this); 
        this.cmdEvaluators[CmdTypes.SET]=this.ExecSet.bind(this); 
    }


    async Exec(cmd){
        var tid=await this.StartTransaction()
        var res= await this.ExecOnTransaction(cmd,tid)
        res=await ApplyToAllElements(res,this.esDomain.utils.decode.bind(this.esDomain.utils));
        await this.EndTransaction(res,tid)
        return res
    }

    //Transaction H&&ling
    ExecOnTransaction(cmd,tid){
        var res = null;        
        try{
            let evaluator = this.cmdEvaluators[cmd.cmd]
            res = evaluator(cmd.a,tid)
        }
        catch(e)
        {         
            let errorMsg = "Error evaluating comm&& "+cmd.cmd+" :"+e
            console.error(errorMsg)     
            console.error(cmd);
        }
       
        return res
    }

    async StartTransaction()
    {
        await this.mdbAccessor.Lock() 
        if($DEBUG) console.debug("Local transaction id="+tid+" started")   
        this.latestTransactionId+=1
        var tid = this.latestTransactionId
        this.tempHistoryForTransaction[tid]=[]
        return tid
    }

    async EndTransaction(res,tid)
    {       
        await this.mdbAccessor.Release()    
        if($DEBUG) console.debug("Local transaction id="+tid+" complete")   
    }

    AddToHistory(value,tid){
        this.tempHistoryForTransaction[tid].push(value)
    }
    
    //Evaluators
    async ExecGet(args,tid){
        var status = 'OK'
        var res = null  
        try{
            var target = args
            var eoqHistory = this.tempHistoryForTransaction[tid]
            res = await this.qryEvaluator.Eval(target,eoqHistory)
            this.AddToHistory(res,tid)
        }
        catch(e){
            let errorMsg = e.toString()
            console.error('Get CMD failed:'+errorMsg)
            status = 'ERR'
            res = errorMsg
        }
        return res
    }

    async ExecCmp(args,tid){
        var subresults = []
        var n = 0;
        for(let c in args){
            n+=1
            try{
                let subresult = this.ExecOnTransaction(args[c], tid) 
                subresult=await ApplyToAllElements(subresult,this.esDomain.utils.decode.bind(this.esDomain.utils));
                subresults.push(subresult)
            }
            catch(e){       
            console.error("Sub comm&& "+n+" failed: "+e)
            }
        }
        return subresults
    }

    async ExecCrn(args,tid){
        var status = 'OK'
        var res = null  
        try{ 
            var eoqHistory = this.tempHistoryForTransaction[tid]
            var packageName = await this.qryEvaluator.Eval(args[0],eoqHistory)
            var className = await this.qryEvaluator.Eval(args[1],eoqHistory)
            var n = await this.qryEvaluator.Eval(args[2],eoqHistory)
            var constructorArgs = args[3].map(function(a){ return this.qryEvaluator.Eval(a,eoqHistory)})
            var constructorArgs= await Promise.all(constructorArgs);
            if(IsNoList(packageName) && IsNoList(className)){
                if(IsNoList(n)){
                    res = await this.mdbAccessor.CreateByName(packageName,className,n,constructorArgs)
                }
                else{
                   throw 'Error in create: n must be a positive integer, but got: '+n
                }
            }
            else{
                throw 'Error in create: packageName && className must be strings, but got: '+packageName +', '+className 
            }
            this.AddToHistory(res,tid)
        }
        catch(e){
            status = 'ERR'           
            throw e
        }

        return res; 
    }


    async ExecClo(args,tid){
        var status = 'OK'
        var res = null  
        try{ 
            var eoqHistory = this.tempHistoryForTransaction[tid]
            var target = await this.qryEvaluator.Eval(args[0],eoqHistory)
            var mode = await this.qryEvaluator.Eval(args[1],eoqHistory)
            if(IsNoList(target)){
                if(IsNoList(mode))
                {
                     res = await this.mdbAccessor.Clone(target,mode)
                }
                else
                {
                    throw 'error in clone: mode is invalid'
                }
            }else if(IsListOfObjects(target)){
                if(IsNoList(mode))
                {
                    var clones=[];
                    for(let t of target){
                        clones.push(this.mdbAccessor.Clone(t,mode));
                    }
                    res=this.esDomain.utils.awaitAll(clones);
                }
                else
                {
                    if(target.length==mode.length)
                    {
                        var clones=[];
                        for(let i=0; i<target.length; i++){
                            clones.push(this.mdbAccessor.Clone(target[i],mode[i]));
                        }
                        res=this.esDomain.utils.awaitAll(clones);
                    }
                    else
                    {
                        throw 'error in clone: targets/mode dim mismatch'
                    }
                }
            }            
            this.AddToHistory(res,tid)
        }
        catch(e){
            status = 'ERR'           
            throw e
        }
        return res; 
    }


    async ExecSet(args,tid){
        var status = 'OK'
        var res=null;
        var eoqHistory = this.tempHistoryForTransaction[tid] //hack to make history work for the SET comm&&, because transactions are not implemented yet for the comm&&runner           
        let tgt =  this.qryEvaluator.Eval(args[0],eoqHistory)
        let ft =  this.qryEvaluator.Eval(args[1],eoqHistory)
        let val =  this.qryEvaluator.Eval(args[2],eoqHistory)
     
      
        //parellelizes the query evaluation
        var target=await tgt
        var feature=await ft
        var value=await val

        if(IsNoList(target))
        {
            if(IsNoList(feature))
            {
                if(IsNoList(value))
                {
                    //default case: one target, one feature
                    await this.mdbAccessor.Set(target,feature,value);
                }
                else
                {                      
                    var operations=[];
                    for(let v in value){
                        operations.push(this.mdbAccessor.Set(target,feature,value[v]));
                    }
                    await Promise.all(operations)
                }
                
                
            }
        }else if(IsListOfObjects(target)){ //e.g. [#20,#22,#23]
            //all multiple targets
            if(IsNoList(feature))
            {
                //multiple targets, all single feature
                if(IsNoList(value))
                {
                    //case: multiple target, single feature, single value
                    var operations=[];
                    for(let t in target)
                    {
                        operations.push(this.mdbAccessor.Set(target[t],feature,value));
                    }
                    await Promise.all(operations)
                }
                else if(value.length && target.length)
                {
                    //case: multiple target, single feature, multiple value, with equal list lengths
                    var operations=[];                       
                    for(let t in target)
                    {
                        operations.push(this.mdbAccessor.Set(target[t],feature,value[t]));
                    }
                    await Promise.all(operations)
                }
            }
        }

        res = [target,feature,value]
        this.AddToHistory(res,tid)
        return res;
    }

    async ExecAdd(args,tid)
    {
        var status='OK'
        var res=null;
        var eoqHistory = this.tempHistoryForTransaction[tid] //hack to make history work for the SET comm&&, because transactions are not implemented yet for the comm&&runner    
        let tgt =  this.qryEvaluator.Eval(args[0],eoqHistory)
        let ft =  this.qryEvaluator.Eval(args[1],eoqHistory)
        let val =  this.qryEvaluator.Eval(args[2],eoqHistory)     

        //parellelizes the query evaluation
        let target=await tgt
        let feature=await ft
        let value=await val

        if(IsNoList(target)) // e.g. #20
        {      
            if(IsNoList(feature))
            {           
                if(IsNoList(value))
                {                   
                        //default case: one target, one feature, single value
                        await this.mdbAccessor.Add(target,feature,value);
                }
                else
                {    
                    var operations=[];
                    for(let v in value){
                        operations.push(this.mdbAccessor.Add(target,feature,value[v]) );
                    }
                    await Promise.all(operations)
                }
            }
      
        }else if(IsListOfObjects(target)){ //e.g. [#20,#22,#23]
            //all multiple targets
            if(IsNoList(feature))
            {
                //multiple targets, all single feature
                if(IsNoList(value))
                {
                    //case: multiple target, single feature, single value
                    var operations=[];
                    for(let t of target)
                    {
                        operations.push(this.mdbAccessor.Add(target[t],feature,value));
                    }
                    await Promise.all(operations)
                }
                else if(value.length && target.length)
                {
                    //case: multiple target, single feature, multiple value, with equal list lengths
                    var operations=[];
                    for(let t of target)
                    {
                        operations.push(this.mdbAccessor.Add(target[t],feature,value[t]));
                    }
                    await Promise.all(operations)
                }
            }

        }   

        res = [target,feature,value]
        this.AddToHistory(res,tid)
        return res;
    }

    async ExecRem(args,tid)
    {
        var self=this
        let status = 'OK'
        let res = null  
        var eoqHistory = this.tempHistoryForTransaction[tid] //hack to make history work for the SET comm&&, because transactions are not implemented yet for the comm&&runner  

        let tgt =  this.qryEvaluator.Eval(args[0],eoqHistory)
        let ft =  this.qryEvaluator.Eval(args[1],eoqHistory)
        let val =  this.qryEvaluator.Eval(args[2],eoqHistory)    


        
        //parellelizes the query evaluation
        let target=await tgt
        let feature=await ft
        let value=await val
 
        //set the value(s) depending on the multiplicity of the arguments
        if(IsNoList(target)){ // e.g. #20
            if(IsNoList(feature)){
                if(IsNoList(value)){
                    self.mdbAccessor.Remove(target,feature,value)  
                }
                else if(IsList(value)){                    
                        self.mdbAccessor.RemoveMany(target,feature,value)                    
                }
                else{
                    throw 'Error in remove: value must be single value or list of values'
                }
            }
            else if(IsListOfObjects(feature)){
                if(IsNoList(value)){
                    for(let f of feature){
                        self.mdbAccessor.Remove(target,f,value)
                    }
                }
                else if (IsList(value) && value.length == feature.length){
                    for(let i=0;i<feature.length;i++){
                        if(IsListOfObjects(value[i])){
                            for(let v of value[i]){
                                self.mdbAccessor.Remove(target,feature[i],v)
                            }
                        }
                        else{
                            throw 'Error in remove: for multiple features the value must be a list of list of objects for each feature'
                        }        
                    }        
                }
                else
                {
                    throw 'Error in remove: value must be single value or list of list of values with outer list having a length equal to the number of features'
                }
            }
            else{
                throw 'Error in remove: feature must be single object or list of objects'
            }
        }
        else if(IsListOfObjects(target)){ // e.g. [#20,#22,#23]
            if(IsNoList(feature)){
                if(IsNoList(value)){
                    for(let t of target){
                        self.mdbAccessor.Remove(t,feature,value)
                    }
                }
                else if(IsList(value) && value.length == target.length){
                    for(let j=0;j<len(target);j++){
                        if(IsListOfObjects(value[j])){
                            for(let i=0;i<len(value[j]);i++){
                                self.mdbAccessor.Remove(target[j],feature,value[j][i])
                            }
                        }
                        else{
                            throw 'Error in add: for multiple targets the value must be a list of list of objects for each target'
                        }
                    }
                }
                else{
                    throw 'Error in remove: value must be single value or list of list of values with the outer list having a length equal to the number of targets'
                }
            }
            else if(IsListOfObjects(feature)){
                if(IsNoList(value)){
                    for(let t of target){
                        for(let f of feature){
                            self.mdbAccessor.Remove(t,f,value)    
                        }     
                    }    
                }              
                else if(IsListOfObjects(value) && value.length == feature.length){
                    for(let t of target){
                        for(let i=0;i<feature.length;i++){
                            self.mdbAccessor.Remove(t,feature[i],value[i])   
                        }
                    }       
                }                 
                else if(IsList(value) && value.length == len(target)){
                    for(let j=0;j<len(target);j++){
                        if(IsListOfObjects(value[j]) && len(value[j]) == feature.length){
                            for(let i=0;i<feature.length;i++){
                                self.mdbAccessor.Remove(target[j],feature[i],value[j][i])    
                            }    
                        }                        
                        else if(IsList(value[j]) && len(value[j]) == feature.length){
                            for(let i=0;i<feature.length;i++){
                                if(IsList(value[j][i])){
                                    for(v in value[j][i]){
                                        self.mdbAccessor.Remove(target[j],feature[i],v) 
                                    }                                      
                                }
                                else{
                                    throw 'Error in remove: for multiple targets, multiple features && multiple values value must list equal to targets containing a list equal to features containing a list of values'
                                }
                            }
                        }
                        else{
                            throw 'Error in remove: for multiple targets && multiple features the value for each entry must have the same length as the number of features.'
                        }
                    }
                }   
                else{
                    throw 'Error in remove: value must be single value or list of list of list of values with outer list having a lenght equal to the number of targets && the middle list with a length equal to the number of features'
                }
            }
            else{
                throw 'Error in remove: feature must be single object or list of objects'
            }
        }
        else{
            throw 'Error in remove: target must be single object or list of objects'
        }

        res = [target,feature,value]
        this.AddToHistory(res,tid)
        return res;
    }

}




