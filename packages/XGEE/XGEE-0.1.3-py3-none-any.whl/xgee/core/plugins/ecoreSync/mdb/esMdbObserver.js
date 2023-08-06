/* ecoreSync ModelDB observer interface (MOI) */
/* The ecoreSync mdbObserver API is used to create model listeners. It enables the queryObserver to observer queries on the ecoreSync mdb. It provides the ecoreSync
   functionalities in a EOQ2 compatibile manner. */

/* (C) 2020 Instiute of Aircraft Systems, Matthias Brunner */

import UUID from "../util/uuid.js"

const EVENT_HANDLER_INTERVAL=10 //ms
const delay = interval => new Promise(resolve => setTimeout(resolve,interval));



class EsChangeObserver{
    constructor(esDomain,changeTypes,filter=()=>true)
    {
        var self=this
        this.changeTypes=changeTypes
        this.eventBroker=esDomain.eventBroker;
        this.isObserving=false;
        this.eventPending=false;
        this.subscriptions=[]
        this.filter=filter
        changeTypes.forEach((changeType) => {
            self.subscriptions.push('ecoreSync/_internal/changes/'+changeType)
        })
        this.subscribedEventHandler=null
        this.esDomain=esDomain
    }

    async start(callback){

        var self=this;
        if(!this.isObserving)
        {
            if(callback==null) {  throw 'callback must not be null' }
            this.callback=callback;
            this.subscribedEventHandler=this.eventHandler.bind(this);
            this.subscriptions.forEach(subscription => {
                self.eventBroker.subscribe(subscription,self.subscribedEventHandler);
            });          

            this.isObserving=true;
            return true;
        }
        else
        {
            console.warn('cannot start observer multiple times')
            return true;
        }

    }

    async eventHandler(change){
        if(!this.eventPending)
        {
            this.eventPending=true;
            await delay(EVENT_HANDLER_INTERVAL)   
            if(this.isObserving && this.filter(change)){
                 this.callback()
            }
            this.eventPending=false;
        }   
    }

    async stop(){
        var self=this
        this.subscriptions.forEach(subscription => {
            self.eventBroker.unsubscribe(subscription,self.subscribedEventHandler);
        });      
        this.isObserving=false;
    }

    setToken(token){
        this.token=token;
    }

    getToken(){
        return this.token;
    }
}

class EsFeatureObserver{

    constructor(esDomain){
        this.esDomain=esDomain;
        this.eventBroker=esDomain.eventBroker;
        this.isObserving=false;
        this.subscription='';
        this.eventPending=false;
        this.callback=null;
        this.observedObject=null;
        this.observedFeature=null;
        this.subscribedEventHandler=null;
        this.token=null;
    }
    
    async createSubscription(eObject,featureName){       
        let oid=this.esDomain.rlookup(eObject);
        if(oid==null) throw 'eObject is unknown to this ecoreSync instance'

        if(!this.esDomain.utils.isBuiltInClass(eObject.eClass)){
            let classOid=this.esDomain.rlookup(eObject.eClass);
            if(classOid==null) throw 'eClass is unknown to this ecoreSync instance'
            await this.esDomain.initEClass(classOid,true)
        }
        
        let instanceId=this.esDomain.esInstance.getInstanceId();
        let subscription='ecore/'+instanceId+'/'+oid;
        var feature=eObject.eClass.getEStructuralFeature(featureName);
        if(!feature) throw 'the eClass of the eObject has no such feature'

        switch(feature.eClass.get('name'))
        {
            case 'EReference':
                subscription+='/*/'+featureName
            break;
            case 'EAttribute':
                subscription+='/change/'+featureName
            break;
            default:
                throw 'unexpected feature class: '+feature.get('name')                 
        }

        return subscription;
    }

    async start(eObject,feature,callback){

        if(!this.isObserving)
        {
            if(!eObject) {  throw 'an eObject must be provided' }
            this.observedObject=eObject;

            if(callback==null) {  throw 'callback must not be null' }
            this.callback=callback;

            if(feature==null) {  throw 'feature must not be null' }
            this.observedFeature=feature;

            this.subscription=await this.createSubscription(eObject,feature);
            this.subscribedEventHandler=this.eventHandler.bind(this);
            this.eventBroker.subscribe(this.subscription,this.subscribedEventHandler);
            this.isObserving=true;
            return true;
        }
        else
        {
            console.warn('cannot start observer multiple times')
            return true;
        }
    }

    stop(){
        var res=false;
        console.info('stopping internal observer: '+this.token+', subscription: '+this.subscription)   
        if(!this.eventBroker.unsubscribe(this.subscribedEventHandler,this.subscription))
        {
            console.error('unsubscription failed: '+this.token)
        }
        else
        {
            console.info('subscription successfully terminated')
            res=true;
        }
        this.isObserving=false;
        return res;
    }

    async getFeature(){
        if(!this.observedObject) throw 'internal error: observed object is invalid'
        if(!this.observedFeature) throw 'internal error: observed feature is invalid'
        var feature=this.observedObject.eClass.getEStructuralFeature(this.observedFeature);
        if(!feature) throw 'internal error: eClass feature is invalid'
        var res=null;
        switch(feature.eClass.get('name'))
        {
            case 'EReference':
                if(feature.get("upperBound")>1)
                {
                    res=this.observedObject.get(this.observedFeature).array();
                    results=results.map(function(e){ 
                        return self.esDomain.utils.encode(e);
                    })
                }
                else
                {           
                    res=this.esDomain.utils.encode(this.observedObject.get(this.observedFeature))
                }
                break;
            case 'EAttribute':
                    res=this.observedObject.get(this.observedFeature);
                break;
            default:
                throw 'unexpected feature class: '+feature.get('name') 
        }
        return res;
    }

    async eventHandler(){
        if(!this.eventPending)
        {
            this.eventPending=true;
            await delay(EVENT_HANDLER_INTERVAL)   
            if(this.isObserving) this.callback(await this.getFeature())
            this.eventPending=false;
        }   
    }

    setToken(token){
        this.token=token;
    }

    getToken(){
        return this.token;
    }

}


export default class EsMdbObserver{
    constructor(esDomain)
    {
        this.esDomain=esDomain;
        this.eventBroker=esDomain.eventBroker;
        this.observers=new Map();
    } 


    async Observe(obj,feature,callback){
        //Observes a feature of an object 
        // calls the callback function with the new feature value
        let observer=new EsFeatureObserver(this.esDomain);
        let uuid=new UUID.v4();
        var observerToken=uuid.toString();
        while(this.observers.has(observerToken))
        {
            let uuid=new UUID.v4();
            observerToken=uuid.toString();
        }
        observer.setToken(observerToken);

        this.observers.set(observerToken,observer);            
        var obj=await this.esDomain.utils.decode(obj);  
        await observer.start(obj,feature,callback);
        return observerToken;
    }


    async ObserveAllChanges(changeTypes,callback,filter=()=>true){
        //Generic change observer
        //Observes all changes of the supplied types
        let observer=new EsChangeObserver(this.esDomain,changeTypes,filter);
        let uuid=new UUID.v4();
        var observerToken=uuid.toString();
        while(this.observers.has(observerToken))
        {
            let uuid=new UUID.v4();
            observerToken=uuid.toString();
        }
        observer.setToken(observerToken);

        this.observers.set(observerToken,observer);            
        await observer.start(callback);
        return observerToken;
    }

    Unobserve(observerToken){
        // Stops the observer associated with the observing token from observing 
        // removes the observertoken and the observer from the list of observers 
        var res=false;
        if(this.observers.has(observerToken))
        {
            let observer=this.observers.get(observerToken);
            res=observer.stop();
            this.observers.delete(observerToken);
        }
        else
        {
            console.warn('could not find internal observer: '+observerToken)   
        }
        return res;
    }

    UnobserveAll(){
        this.observers.forEach(function(observer,observerToken){
            if(observer.stop())
            {
                console.info('observer '+observerToken+' stopped')
            }
        });
        this.observers.clear();
        return true;
    }

}



