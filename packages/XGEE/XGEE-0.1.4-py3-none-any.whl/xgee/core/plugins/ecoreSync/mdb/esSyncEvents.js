import UUID from '../util/uuid.js'

const _watchEvent =(atoken) => {
    var resolveAnnouncement=() => {};
    var rejectAnnouncement=() => {};
    const promise=new Promise(function(resolve,reject){
        resolveAnnouncement=(eObject) => { resolve(eObject) };
        rejectAnnouncement=() => { reject() };
    })
    return {
        promise: promise,
        token: atoken,
        check: (token) => {return atoken==token},
        resolve: (eObject) => { resolveAnnouncement(eObject) },
        reject: () => { rejectAnnouncement(); }
    }
};


export default class EsSyncLock{
    constructor(){
        this.events=new Map();
        this.history=new Set();
    }

    reserve(syncEventId){
        let uuid=new UUID.v4
        let token=null;
        if(!this.events.has(syncEventId)){
            token=uuid.toString();;
            this.events.set(syncEventId,_watchEvent(token));
        }
        return token;
    }

    fire(syncEventId,token,value,success=true){
        var res=false;
        if(this.canFire(syncEventId,token) && this.events.has(syncEventId)){
            if(success){
                this.events.get(syncEventId).resolve(value);
            }
            else
            {
                this.events.get(syncEventId).reject(value);
            }
            this.history.add(syncEventId);
            this.events.delete(syncEventId);
            res=true;
        }
        return res;
    }

    isReserved(syncEventId){
        var res=false;
        if(this.events.has(syncEventId)){
            res=true;
        }
        return res;
    }

    canFire(syncEventId,token)
    {
        var res=false;
        if(!this.events.has(syncEventId)){
            res=true;
        }
        else
        {
            if(this.events.get(syncEventId).check(token))
            {
                res=true;
            }
        }
        return res;
    }

    async waitFor(syncEventId){
        var event=this.events.get(syncEventId);
        if(event)
        {
            var res=await event.promise
            return res;
        }
        else
        {
            throw 'no event with id='+syncEventId+' is present'
        }
    }
    
}