
import UUID from '../util/uuid.js'

class Mutex{
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


export default class EsChanges{
    
    constructor(esDomain,listen=true){
        this.esDomain=esDomain;
        this.changeId=0;
        this.listening=false;
        this.mutex=new Mutex();
        this.localChanges=new Set();
        if(listen) this.startListening();
    }

    async domainChangeHandler(evts,src){
        var dchid=Math.random();

        let token=await this.lock();

        for(let i=0;i<evts.length;i++) {
            let evt = evts[i];
            try{
                await this.process(evt.a)           
            }
            catch(e)
            {
                console.error("Failed to process change. error="+e)        
            }
        }
        //releases exactly one of the pending queue

        this.release(token);

    }

    async lock(){
        let release= await this.mutex.lock();
        return release;
    }

    release(token){
        this.mutex.release(token);
    }

    async process(change){
        var self=this;
        let changeId = change[0];
        let changeType = change[1];
        let oid = change[2].v;
     
            if(this.changeId<changeId)
            {
             //change is only processed if it is recent

                this.esDomain.eventBroker.publish('ecoreSync/_internal/changes/'+changeType,change)
                var eObject=this.esDomain.lookup(oid);
                //change is only relevant to us if it is part of the local ecoreSync cache

                if(eObject)
                {
                    //the object this change relates to is locally available
                    //currently ecoreSync only supports direct changes to objects, however future releases might also regard changes that alter local queries such as Cls(...)

                    let status=this.esDomain.mdb.getStatusById(oid);
                    var featureName = change[3];
                    var newValue=change[4];

                    if(status && status.isInitialized(featureName)){
                        //only changes that affect locally initialized features are regarded 

                        if(!this.localChanges.has(changeId))
                        {
                            //this change originates from somewhere else than our local instance

                            switch(changeType) {
                                case eoq2.event.ChgTypes.SET:
                                    {
                                        var currentValue= await this.esDomain.get(eObject,featureName);                                                    
                                        //look if the change is an object and if the change changes anything locally
                                        if(newValue != null && newValue.v) {
                                            if(this.esDomain.rlookup(currentValue)!=newValue.v)
                                            {
                                                var object=await this.esDomain.getObject(newValue.v);
                                                eObject.set(featureName,object);
                                            }
                                        } else {
                                            if(currentValue!=newValue) eObject.set(featureName,newValue);                                            
                                        }           
                                    } 
                                    break;
                                case eoq2.event.ChgTypes.ADD:
                                    {         
                                        var currentValue=await this.esDomain.get(eObject,featureName); 
                                        var inReference=false;
                                        if(Array.isArray(currentValue))
                                        {
                                            if(currentValue.find(function(e){ return self.esDomain.rlookup(e)==newValue.v  })){
                                                inReference=true;
                                            }                                    
                                        }
                                        else
                                        {
                                            throw 'CHG result is not an array.'
                                        }
                                                                
                                        if(!inReference) {        
                                            
                                            var object=await this.esDomain.getObject(newValue.v);
                                            eObject.get(featureName).add(object);   
                                            var postValue=await this.esDomain.get(eObject,featureName);                             
                                        }   
                                                     
                                    }                   
                                    break;
                                case eoq2.event.ChgTypes.REM:
                                    {
                                        var currentValue= await this.esDomain.get(eObject,featureName); 
                                        var inReference=false;
            
                                        if(Array.isArray(currentValue))
                                        {
                                            if(currentValue.find(function(e){    return self.esDomain.rlookup(e)==newValue.v  })){
                                                inReference=true;
                                            }                                    
                                        }
                                        else
                                        {
                                            throw 'CHG result is not an array.'
                                        }
                                                                
                                        if(inReference) 
                                        {                                 
                                            var object=await self.esDomain.getObject(newValue.v);
                                            eObject.get(featureName).remove(object);         
                                        }                               
                                    }
                                    break;
                                case eoq2.event.ChgTypes.MOV:
                                        console.warn('ChgType MOV not processed in this release')
                                        break;
                                default:
                                    throw "ecoreSync got change of unknown type: "+changeType;
                            }

                        }
                        else
                        {
                            this.setChangeId(changeId);
                            this.localChanges.delete(changeId); //tidy up a bit
                        }
                    }
                }
            }
        
           
        return true
    }

    async startListening(){
        if(!this.listening)
        {
            await this.setChangeIdToLatest();
            await this.esDomain.eoq2domain.Do(new eoq2.command.Obs('CHG','*'));
            this.esDomain.eoq2domain.Observe(this.domainChangeHandler.bind(this),[eoq2.event.EvtTypes.CHG]);
            this.listening=true;
        }
    }

    stopListening(){
        if(this.listening)
        {
            this.esDomain.eoq2domain.Unobserve(this.domainChangeHandler.bind(this));
            this.listening=true;
        }
    }

    async getRemoteChangeId()
    {
        let cmd = new eoq2.Sts();
        return await this.esDomain.remoteExec(cmd);
    }

    setChangeId(changeId)
    {
        this.changeId=changeId;
    }

    async setChangeIdToLatest()
    {
        let changeId=await this.getRemoteChangeId();
        this.setChangeId(changeId);
    }

    getChangeId()
    {
        return this.changeId;
    }

    markChangeIdAsLocal(changeId)
    {
        this.localChanges.add(changeId);
    }

    syncToChangeId(changeId)
    {
        return Promise.reject('placeholder for future use');
    }


}
