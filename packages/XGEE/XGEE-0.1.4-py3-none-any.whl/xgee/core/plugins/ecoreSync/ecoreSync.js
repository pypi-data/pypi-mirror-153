
import EsInstance from "./interfaces/esInstance.js"
import EsDomain from "./domain/esDomain.js"

//EcoreSync interface

export default class EcoreSync{
    constructor(eventBroker){
        this._instances=new Map();
        this._idInstances=new Map();
        this._version="2.0.0"
        this._eventBroker=eventBroker;
    }

    getInstance(eoq2domain,id=null)
    {
        var instance=null;

        if(id != null && typeof id != 'string') throw 'id is not a valid string'       
                
        if(this._instances.has(eoq2domain))
        {
            instance=this._instances.get(eoq2domain);
            if(id != null && instance.getId() != id )  throw 'cannot redefine id to id='+id+' for existing instance with id='+instance.getid() 
        }
        else
        {
            if(this._idInstances.has(id))   throw 'id must be a unique string, id='+id+' is already taken'   

            instance=new EsInstance(this._eventBroker,id);            
            instance._esDomain=new EsDomain(eoq2domain,this._eventBroker,instance);    
            instance.utils=instance._esDomain.utils; //add utils available to the instance interface     

            if(instance==null) throw 'Fatal Error: Failed to create ecoreSync instance'

            this._idInstances.set(id,instance);
            this._instances.set(eoq2domain,instance);
        }

        if(instance==null) throw 'Fatal Error: Invalid result while getting ecoreSync instance'       
        return instance
    }

    getInstanceById(id)
    {
        var res=null;
        if(this._idInstances.has(id))
        {
            res=this._idInstances.get(id);
        }
        return res;
    }

    getVersion(){
        return this.version;
    }

}

