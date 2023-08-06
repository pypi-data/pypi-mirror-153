import UUID from  './uuid.js'

export function castToFloat(num){

    if(Number.isNaN(num))
    {
        num=0;
    }
    var floatNum=Number.parseFloat(num)
    if(Number.isInteger(floatNum))
    {
        floatNum+=1e-5;
    }
    return floatNum;

}

export function replaceTemplates(valueSet,string)
{
    var res=string;
    if(typeof res == 'string')
    {
        for (const [key, value] of Object.entries(valueSet)) {
            let repValue=value;
            if(value && typeof value == "object") repValue=ecoreSync.rlookup(value)
            if(repValue==null){ repValue=''}
            res=res.replace(new RegExp('{'+key+'}', 'g'),repValue)  
        }
    }
    return res
}


export function mergeValueSets(valueSetA,valueSetB,immutableValues=[])
{                    
    var valueSet=Object.assign({},valueSetA);
    for(let value in valueSetB)
    {
        if(!immutableValues.includes(value))
        {
            valueSet[value]=valueSetB[value]
        }
    }

    return valueSet;
}

function copyValueSet(valueSet){
    return Object.assign({},valueSet);
}

export var multipleClasses = (baseClass, ...mixins) => {
    //class aggregation taken from http://es6-features.org/#ClassInheritanceFromExpressions
    let base = class _XtdClass extends baseClass {
        constructor (...args) {
            super(...args)
            mixins.forEach((mixin) => {
                mixin.prototype.initializer.call(this)
            })
        }
    }
    let copyProps = (target, source) => {
        Object.getOwnPropertyNames(source)
            .concat(Object.getOwnPropertySymbols(source))
            .forEach((prop) => {
            if (prop.match(/^(?:constructor|prototype|arguments|caller|name|bind|call|apply|toString|length)$/))
                return
            Object.defineProperty(target, prop, Object.getOwnPropertyDescriptor(source, prop))
        })
    }
    mixins.forEach((mixin) => {
        copyProps(base.prototype, mixin.prototype)
        copyProps(base, mixin)
    })
    return base
}


class _Event{
    constructor(enabled=true){
        this.listeners=[];
        this.enabled=enabled;
    }

    raise(eventData){
        if(this.enabled){
            this.listeners.forEach(function(callback){
                callback(eventData);
            });
        }
    }

    enable(){
        this.enabled=true;
    }

    disable(){
        this.enabled=false;
    }

    addListener(callbackFunction){
        this.listeners.push(callbackFunction)
        let listenerId=this.listeners.length-1
        return listenerId
    }

    removeListener(listenerId){
        this.listeners=this.listeners.splice(listenerId,1)
        return true
    }

    removeListenerByFunction(callbackFunction){
        var found=false;
        this.listeners=this.listeners.filter(function(e){
            if(e!=callbackFunction)
            {
                return true
            }
            else
            {
                found=true;
            }
        })
        return found
    }
}


class Observable{
    constructor(){
        this.events={};
    }
    initializer(){
        this.events={};        
    }
    addListener(eventName,callback){
        if(this.events[eventName])
        {
            this.events.addListener(callback);
        }
    }
    removeListener(eventName,callback)
    {
        if(this.events[eventName])
        {
            this.events.removeListener(callback);
        }
    }
    _addEvent(eventName,enabled=true){
        if(this.events[eventName])
        {
            this.events[eventName]=new _Event(enabled);
        }
    }
    _removeEvent(eventName)
    {
        if(this.events[eventName])
        {
            delete this.events[eventName]
        }
    }
}


function rateLimitedFunctionCall(func,interval)
{
	this.action=func;
	this.interval=interval;
	this.timeout=null;
	this.t0=performance.now();
	var self=this;
	this.runRateLimited=function(){ 
					clearTimeout(self.timeout);
					self.timeout=setTimeout(self.runNow,interval);

					};
	this.runNow=function(){ if(self.timeout!=null){clearTimeout(self.timeout);} func.apply();};	
}


export function serialPromise(objects,fn)
{
    return objects.reduce((p, v) => p.then((a) => fn(v).then(r => r != undefined ? a.concat([r]) : a)),Promise.resolve([]));
}


/* Move to ecoreSync once BA's work with ecoreSync is finished */
export function ecoreLocalClone(original)
{
    var clone=original.eClass.create();
    var attributes=original.eClass.get("eAllAttributes")
    var references=original.eClass.get("eAllReferences")
    var containments=original.eClass.get("eAllContainments")

    for(let i in attributes)
    {
        var contents=original.get(attributes[i].get("name"))
        clone.set(attributes[i].get("name"),contents);
    }

    for(let i in references)
    {
        console.debug("Processing reference: "+references[i].get("name"));
        var contents=original.get(references[i].get("name"));
        if(original.eClass.getEStructuralFeature(references[i].get("name")).get("upperBound")==1)
        {
            clone.set(references[i].get("name"),contents);
        }
        else
        {     
            clone.get(references[i].get("name")).add(contents.array());
        }
    }

    
    for(let i in containments)
    {
        var contents=original.get(containments[i].get("name"));
        if(original.eClass.getEStructuralFeature(containments[i].get("name")).get("upperBound")==1)
        {
            if(contents)
            {
            clone.set(containments[i].get("name"),ecoreLocalClone(contents));
            }
        }
        else
        {
            var clonedContents=contents.map(function(e){
                if(e)
                {
                    return ecoreLocalClone(e);
                }
                else
                {
                    return null
                }
            });
            clonedContents.forEach(function(e){
                clone.get(containments[i].get("name")).add(e);
            })
        }
    }
    

    return clone;
}


//Mutex implementation
export class Mutex{
    constructor(){
        this.inUse=false
        this.owner=null

        this.queue=[]
        this.tokens=new Map();
    }


    async lock(){
        this.pending+=1  
              
        
        //Acquire individual lock for token
        let uuid=new UUID.v4
        let token=uuid.toString();

        if(this.inUse){
            var releaseLock=() => {};
            var rejectLock=() => {};

            let tokenLock=new Promise(function(release,reject){
                releaseLock=()=> { release(); };
                rejectLock=()=> { reject(); };
            })

            this.tokens.set(token,{
                lock:tokenLock,
                releaseLock:releaseLock,
                rejectLock: rejectLock 
            });

            this.queue.push(token)  
            await tokenLock
        }
        else
        {
            this.tokens.set(token,{})
        }
      
            this._acquireMutex(token)         

        return token;
    }

    _acquireMutex(token){
 
   
        this.inUse=true
        this.owner=token

        var releaseMutex=() => {};
        var rejectMutex=() => {};

        this.mutex=new Promise(function(release,reject){
            releaseMutex=()=> { release(); };
            rejectMutex=()=> { reject(); };
        })

        //Mutex has been acquired, let's update the token object
        let tokenObject=this.tokens.get(token)
        tokenObject.hasMutex=true
        tokenObject.releaseMutex=releaseMutex
        tokenObject.rejectMutex=rejectMutex     
    }


    release(token)
    {
        if(this.tokens.has(token))
        {
            let tokenObject=this.tokens.get(token);
            this.tokens.delete(token);
            tokenObject.releaseMutex(); 

            if(!this.tokens.size)
            {
                this.mutex=Promise.resolve();
                this.inUse=false
                this.owner=null
            }                               

            if(this.queue.length){
                let nextToken=this.queue[0]
                this.queue.shift()
                let nextTokenObject=this.tokens.get(nextToken)  
                  
                nextTokenObject.releaseLock()      
            }

        }
 
    }

}