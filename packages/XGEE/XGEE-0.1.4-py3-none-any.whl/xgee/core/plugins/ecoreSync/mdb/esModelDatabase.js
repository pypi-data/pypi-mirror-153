import EsSyncStatus from './esSyncStatus.js'
import EsSyncEvents from './esSyncEvents.js'
import UUID from '../util/uuid.js'

export default class EsModelDatabase{

    constructor(esInstance,eventBroker){
        this.objDb=new Map(); //used for lookups id->eObject
        this.robjDb=new Map(); //used for reverse lookups eObject->id
        this.statDb=new Map(); //used for status lookups eObject -> status
        this.packDb=new Map(); //used for package lookups by nsURI and class lookups by nsURI and name
        this.objLockDb=new Map(); //used for reserved object ids for deconflicting operations 
        this.featureLockDb=new Map(); //used for reserved object ids / feature combinations for deconflicting operations 
        this.esInstance=esInstance;
        this.instanceId=esInstance.getInstanceId();
        this.eventBroker=eventBroker;
        this.syncEvents=new EsSyncEvents();

    }

    containsObjectId(objectId){
        return this.objDb.has(objectId)
    }
    
    contains(eObject){
        return this.robjDb.has(eObject)
    }

    isIndexed(eObject,feature=null){
        if(Number.isInteger(eObject))
        {
            eObject=this.getObjectById(eObject);
        }
        if(eObject && this.contains(eObject))
        {
            if(!feature)
            {
                return true;
            }
            else
            {

            }
        }
        return false;
    }

    getObjectById(objectId){
        return this.objDb.get(objectId);
    }

    getId(eObject){
        return this.robjDb.get(eObject);
    }

    getStatus(eObject){
        let status=this.statDb.get(eObject);
        return status?status:null
    }

    getStatusById(objectId){
        var res=null;
        var obj=this.getObjectById(objectId);
        if(obj)
        {
            res=this.getStatus(obj);
        }
        return res;
    }

    getEClass(nsURI,name)
    {
        var res=null;
        if(this.packDb.has(nsURI))
        {
            let ePackageIdx=this.packDb.get(nsURI);
            if(ePackageIdx.eClassifiers.has(name))
            {
                return ePackageIdx.eClassifiers.get(name)
            }
        }
        return res;
    }

    add(OID,eObject,token=null){ 

        let syncEventId='#'+OID;
        if(!Number.isInteger(OID))
        {
            throw('ecoreSync: Cannot add eObject to the index, because the object id='+OID+' is invalid')
        }  

        //guard mdb access
        if(!this.syncEvents.canFire(syncEventId,token)){
            throw 'locked OIDs can only be added with the valid token'
        }

        if(!this.containsObjectId(OID))
        {
            if(eObject.eClass.get('name')=='EPackage') this.packDb.set(eObject.get("nsURI"),{ePackage: eObject, eClassifiers: new Map()});
            if(eObject.eClass.get('name')=='EClass'){
                  if(eObject.eContainer){         
                    this.packDb.get(eObject.eContainer.get("nsURI")).eClassifiers.set(eObject.get('name'),eObject);
                  }
                  else
                  {
                    console.error(new Error().stack);
                    console.error(eObject);
                    throw 'error: eClass is not contained in an ePackage, OID='+OID
                  }
            }

            this.objDb.set(OID,eObject);
            this.robjDb.set(eObject,OID);
            this.statDb.set(eObject,new EsSyncStatus(this.esInstance,eObject));
      

            //attribute listeners
            var self=this;
            eObject.on('change',function(change){
                self.eventBroker.publish('ecore/'+self.instanceId+'/'+OID+'/change/'+change,eObject.get(change));    
            })

            //reference listeners
            var eAllReferences=eObject.eClass.get('eAllReferences');
            eAllReferences=eAllReferences.concat(eObject.eClass.get('eAllContainments'));
            eAllReferences.forEach(function(feature){
                eObject.on('add:'+feature.get('name'),function(){
                    self.eventBroker.publish('ecore/'+self.instanceId+'/'+OID+'/add/'+feature.get('name'),eObject.get(feature.get('name')));    
                });
                eObject.on('remove:'+feature.get('name'),function(){
                    self.eventBroker.publish('ecore/'+self.instanceId+'/'+OID+'/remove/'+feature.get('name'),eObject.get(feature.get('name')));    
                });
            });    

            //automatic listener installation upon eClass update
            eObject.eClass.on('add:eStructuralFeatures',function(feature){
                eObject.on('add:'+feature.get('name'),function(){
                    self.eventBroker.publish('ecore/'+self.instanceId+'/'+OID+'/add/'+feature.get('name'),eObject.get(feature.get('name')));    
                });
                eObject.on('remove:'+feature.get('name'),function(){
                    self.eventBroker.publish('ecore/'+self.instanceId+'/'+OID+'/remove/'+feature.get('name'),eObject.get(feature.get('name')));    
                });
            })

            //release lock
            this.syncEvents.fire(syncEventId,token,eObject);
        }
    }

    remove(eObject)
    {
        if(this.contains(eObject))
        {
            let oid=this.getObjectId(eObject);
            this.objDb.delete(oid);
            this.robjDb.delete(eObject);
        }
    }

    removeById(objectId)
    {
        if(this.containsObjectId(objectId))
        {
            let eObject=this.objDb.get(objectId);
            this.objDb.delete(objectId);
            this.robjDb.delete(eObject);
        }
    }


    setFeatureInitialized(oid,featureName,token)
    {
        let syncEventId='#'+oid+'/'+featureName;
        if(!this.containsObjectId(oid)) throw 'the supplied object id is unknown to ecoreSync'
        let eObject=this.getObjectById(oid);
        let value=eObject.get(featureName);
        let feature=eObject.eClass.getEStructuralFeature(featureName);
        if(feature.get('upperBound')!=1)
        {       
            value=value.array()
        }    
        //guard mdb access
        if(!this.syncEvents.canFire(syncEventId,token)){
            throw 'locked OIDs can only be added with the valid token'
        }        
        let status=this.getStatusById(oid);
        status.setInitialized(featureName);
        this.syncEvents.fire(syncEventId,token,value);
    }

    find(func){
        for (const entry of objDb) {
            if(func(entry[1]))
            {
                return entry[1];
            }
        }
    }

    filter(func){
        var matches=[];
        for (const entry of objDb) {
            if(func(entry[1]))
            {
                matches.push(entry[1]);
            }
        }
        return matches;
    }


    //Model-database sync events
    //These events are used to manage concurrent synchronization requests

    lockObjectId(oid,modifier=null)
    {
        //Locks the OID to the model database.
        //If the oid has not been locked previously a token is returned. Otherwise null is returned.
        //The token must be used when adding the eObject to the model database.
       var res=null;
       let syncEventId='#'+oid
       if(!this.containsObjectId(oid))
       {
            res=this.syncEvents.reserve(syncEventId);
       }
       return res;
    }

    unlockObjectId(oid,token)
    {
        let syncEventId='#'+oid;
        return this.syncEvents.fire(syncEventId,token,null,false);
    }

    lockFeature(oid,feature)
    {
        var res=null;
        let syncEventId='#'+oid+'/'+feature;
        if(!this.containsObjectId(oid))
        {
             throw 'cannot lock feature for unknown oid'
        }

        let status=this.getStatusById(oid);
        if(!status.isInitialized(feature))
        {
            res=this.syncEvents.reserve(syncEventId);
        }               
        return res;
    }

    unlockFeature(oid,feature,token)
    {
        let syncEventId='#'+oid+'/'+feature;
        return this.syncEvents.fire(syncEventId,token,null,false);
    }

    async waitForObject(oid){
        //waits for an sync event. Returns the corresponding results once added to the model database
        var res=null;
        let syncEventId='#'+oid;
        if(this.containsObjectId(oid))
        {
            res=this.getObjectById(oid);
        }
        else
        {
            res=this.syncEvents.waitFor(syncEventId);
        }
        return res;
    }

    async waitForFeature(oid,featureName){
        //waits for an sync event. Returns the corresponding results once added to the model database
        var res=null;
        let syncEventId='#'+oid+'/'+featureName;
        if(this.containsObjectId(oid))
        {
            let status=this.getStatusById(oid);
            if(status.isInitialized(featureName))
            {
                let value=eObject.get(featureName);
                let feature=eObject.eClass.getEStructuralFeature(featureName);
                if(feature.get('upperBound')!=1)
                {       
                    value=value.array()
                }   
                res=value;
            }
            else
            {
                res=await this.syncEvents.waitFor(syncEventId);
            }
        }
        else
        {
            throw 'cannot wait for feeture of unknown oid'
        }
        return res;        
    }

}

