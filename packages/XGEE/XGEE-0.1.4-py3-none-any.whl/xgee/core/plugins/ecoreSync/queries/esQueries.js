//ecoreSync EOQ support
//(C) 2020 Matthias Brunner / University of Stuttgart, Institute of Aircraft Systems

import UUID from "../util/uuid.js"
import EsQueryObserver from "../queries/esQueryObserver.js"


 export default class EsQueries{
    initializer(){
        this.qryObservers=new Map();
    }  

    async exec(cmd,encode=false){
        var res=null;
        try{
            res=this.cmdRunner.Exec(cmd)
        }catch(e){          
            throw 'ecoreSync: Failed to execute local command: '+e
        }
        if(encode) res=this.utils.encode(res);   
        return res;
    }

    async remoteExec(cmd,decode=false){
        try{
            var res=await this.eoq2domain.Do(cmd);
        }
        catch(e)
        {
            throw('ecoreSync: Failed to execute remote command: '+e)
        } 
        try{        
            if(decode) res=this.utils.decode(res);  
        }
        catch(e)
        {
            throw('ecoreSync: Failed to decode command results: '+e)  
        }
        return res;
    }

    async observe(qry,callback,decode=true){
        if(!callback) throw 'no callback function supplied for observe operation '
        var uuid=new UUID.v4
        var observerToken=uuid.toString();
        var observer=new EsQueryObserver(this);
        this.qryObservers.set(observerToken,observer);
        await observer.Eval(qry,callback,decode);
        return observerToken;
    }

    unobserve(observerToken){
        var res=false;
        if(this.qryObservers.has(observerToken))
        {
            var observer=this.qryObservers.get(observerToken);
            this.qryObservers.delete(observerToken);
            observer.Stop();
            res=true;
        }
        else
        {
            console.warn(observerToken+' is not a known observer token.')
        }
        return res;
    }
}