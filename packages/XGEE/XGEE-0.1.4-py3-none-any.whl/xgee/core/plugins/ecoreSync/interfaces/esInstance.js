import UUID from "../util/uuid.js"

export default class EsInstance{
    constructor(eventBroker,id=null){
        this._eventBroker=eventBroker;
        this._UUID=new UUID.v4();
        this._esDomain=null;
        if(id==null)
        {
            this._id=this._UUID.toString();
        }
        else
        {
            this._id=id;
        }
    }

    //Instance identification
    getUUID(){
        return this._UUID.toString();
    }

    getInstanceId(){
        return this._id;
    }

    //Basic object manipulation
    async get(eObject,featureName){
        return this._esDomain.get(eObject,featureName);
    }

    async set(eObject,featureName,value){
        return this._esDomain.set(eObject,featureName,value);
    }

    async unset(eObject,featureName){
        return this._esDomain.unset(eObject,featureName);
    }

    async add(eObject,featureName,value){
        return this._esDomain.add(eObject,featureName,value);
    }

    async remove(eObject,featureName,value){
        return this._esDomain.remove(eObject,featureName,value);
    }    

    //Object creation and replication
    async create(eClass,n){
        return await this._esDomain.create(eClass,n);
    }

    async createByName(nsURI,name,n){
        return await this._esDomain.createByName(nsURI,name,n);
    }

    async clone(eObject,n=1){
        return await this._esDomain.clone(eObject,n);
    }

    //Lookup and retrieval functions
    lookup(...oids){
        if(oids.length){
           var res=this._esDomain.lookup(oids);
           if(res.length==1)
           {
               return res[0]
           }
           else
           {
               return res;
           }
        }
    }

    rlookup(...objects){
        if(objects.length){
            return this._esDomain.rlookup(objects)
        }
    }

    status(oid){
        return this._esDomain.mdb.getStatusById(oid)
    }
    
    async obj(oid){
        //shorthand alias
        return await this._esDomain.getObject(oid);
    }

    async getObject(OID)
    {
        return await this._esDomain.getObject(OID);
    }

    //Query execution
    async exec(cmd,encode=false){
        return this._esDomain.exec(cmd,encode)
    }

    async remoteExec(cmd,decode=false){
        return this._esDomain.remoteExec(cmd,decode)
    }

    //Query observers
    observe(cmd,callback,decoded=true){
        return this._esDomain.observe(cmd,callback,decoded);
    }

    unobserve(observerToken){
        return this._esDomain.unobserve(observerToken);
    }


    //DEBUGGING AND COMPATIBILITY
    getObjectById(id)
    {
        console.warn('ecoreSync: deprecated call to getObjectById(), please use getObject() instead')
        return this.getObject(id);
    }
} 
