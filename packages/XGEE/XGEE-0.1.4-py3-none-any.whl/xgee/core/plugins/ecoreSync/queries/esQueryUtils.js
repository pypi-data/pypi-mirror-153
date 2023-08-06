class Terminator{
    constructor(v){
        this.v=v;
    }
    isEqual(other){
        if(other instanceof Terminator)
        {
            return this.v==other.v
        }
        return this.v == other;
    }    
}

function Determinate(res){
    if(IsList(res)){
        res =  res.map(function(r){ return Determinate(r) }) 
    }
    else if(res instanceof Terminator){
        res = res.v
    }
    return res
}

function ApplyToAllElements(context, functor){
    var res=null
    if(Array.isArray(context))
    {
        res=Promise.all(context.map(function(c){
            return ApplyToAllElements(c,functor)
        }))
    }
    else if(context instanceof Terminator){
            res=res
    }
    else
    {
        res=Promise.resolve(functor(context))
    }
    return res
}

function ApplyToAllCorrespondingElements(a,b,functor){
    var res = null
    if(IsList(a)){
        res = a.map(function(c,i){
            return ApplyToAllCorrespondingElements(a[i],b[i],functor)
        })
        
    }else{
        res = functor(a,b) 
    }
    return res
}


function ApplyToAllElementsInA(a,b,functor){
    var res = null
    if(IsList(a)){
        res = a.map(function(c){
            return ApplyToAllElementsInA(c,b,functor)
        })
    }else{
         res = functor(a,b) 
    } 
    return res
}

function ApplyToAllElementsInB(a,b,functor){
    var res = null
    if(IsList(b)){
        res = b.map(function(c){
            return ApplyToAllElementsInB(a,c,functor)
        })
    }else{
        res = functor(a,b) 
    }
    return res
}

async function ApplyToAllListsOfElementsInA(a,b,functor){
    var res = null
    if(IsListOfObjects(a)){
        res = functor(a,b) 
    }else{   
        res = Promise.all(a.map(function(c){
            return ApplyToAllListsOfElementsInA(c,b,functor)
        }))
    }
    return await res
}


function ApplyToAllListsOfElementsInB(a,b,functor){
    var res = null
    if(IsListOfObjects(b)){
        res = functor(a,b) 
    }else{
        res = b.map(function(c){
            return ApplyToAllListsOfElementsInB(a,c,functor)
        })
    }
    return res
}

function ApplyToSimilarListsOfObjects(op1,op2,listVsListFunc,listVsStructFunc,structVsListOp,param=null){
    var res = null
    if(IsListOfObjects(op1) && IsListOfObjects(op2)){
        res = listVsListFunc(op1,op2,param) 
    } else if(IsListOfObjects(op1)){
        res = listVsStructFunc(op1,op2,param) 
    } else if(IsListOfObjects(op2)){
        res = structVsListOp(op1,op2,param) 
    }else{
        res = op1.map(function(e,i){
            return ApplyToSimilarListsOfObjects(op1[i],op2[i],listVsListFunc,listVsStructFunc,structVsListOp,param)
        });
    }
    return res    
}

function ApplyToSimilarElementStrutures(op1,op2,elemVsElemFunc,elemVsStruct,structVsElemOp,param=null){
    var res = null
    if(IsNoList(op1) && IsNoList(op2)){
        res = elemVsElemFunc(op1,op2,param) 
    }else if (IsNoList(op1)){
        res = elemVsStruct(op1,op2,param) 
    }else if(IsNoList(op2)){
        res = structVsElemOp(op1,op2,param) 
    }else{
        res = op1.map(function(e,i){
            return ApplyToSimilarElementStrutures(op1[i],op2[i],elemVsElemFunc,elemVsStruct,structVsElemOp,param)
        });
    }
    return res
}

function IsListOfObjects(obj)
{
    if(IsList(obj))
    {
        if(obj.length==0) return true
        var nonNullContents=obj.filter(function(e){ return e!=null; });
        if(nonNullContents.length>0 && nonNullContents[0].constructor !== Array) return  true
        return false
    }
    else
    {
        return false
    }
}

function IsNoList(obj)
{
    return !Array.isArray(obj);
}

function IsList(obj)
{
    return Array.isArray(obj);
}

async function awaitAll(obj)
{
    var res=null;
    if(Array.isArray(obj))
    {
        var pending=[];
        for(let i=0;i<obj.length;i++)
        {
            pending.push(awaitAll(obj[i]));
        }
        res=await Promise.all(pending);
    }
    else
    {
        res=await obj;
    }
    return res;
}


