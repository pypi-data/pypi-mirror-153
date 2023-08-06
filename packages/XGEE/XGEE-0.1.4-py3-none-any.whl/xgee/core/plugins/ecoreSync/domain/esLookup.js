//Lookup and retrieval functions for ecoreSync
//(C) 2020 Matthias Brunner / University of Stuttgart, Institute of Aircraft Systems

 export default class EsLookup{
    initializer(){

    }

    async getObject(oid){
        if(!Number.isInteger(oid)) throw 'oid is not an Integer='+oid
        var self=this;
        var eObject=this.lookup(oid)
                
        if(!eObject)
        {

            let cmd = CMD.Cmp();
            cmd.Get(QRY.Obj(oid).Met('CLASS')); 
            cmd.Get(QRY.Obj(oid).Met('CLASSNAME'));
            var res=await self.eoq2domain.Do(cmd)

           
            switch(res[1])
            {
                case 'EClass':                            
                    eObject=await this.initEClass(oid,false);
                    break;
                case 'EPackage':               
                    eObject=await this.initEPackage(oid,token);
                    break;
                default:
                    let token=this.mdb.lockObjectId(oid);
                    if(token!=null)
                    {                         
                        if(res[0]){                                             
                            var eClass=await self.initEClass(res[0].v,true);
                            if(eClass){
                                eObject=eClass.create();
                                self.mdb.add(oid,eObject,token);                 
                            }
                            else
                            {
                                throw 'failed to create local eObject (#'+oid+')'
                            }                   
                        }
                        else
                        {
                            throw 'failed to get object #'+oid
                        }

                    }
                    else
                    {                        
                        eObject=await self.mdb.waitForObject(oid);               
                    }            
            }            
              
        }
        return eObject
    }

    lookup(oids){
        var self=this;   
        var res=null;
        if(!Array.isArray(oids)) { 
            res=self.mdb.getObjectById(oids);
        }
        else
        {
            if(oids.length){  
                res=oids.map(function(oid){
                    return self.mdb.getObjectById(oid)
                })      
            }
            else
            {
                res=[];
            }
        }  
        return res;     
    }

    rlookup(...eObjects)
    {       
        var self=this;
        if(eObjects.length){        
            if(Array.isArray(eObjects[0])) eObjects=eObjects[0]
            if(eObjects.length>1)
            {
                return eObjects.map(function(eObject){
                    return self.mdb.getId(eObject)
                })
            }
            else
            {
                return this.mdb.getId(eObjects[0])
            } 
        }      
    }

    getEClass(nsURI,name){
        return this._esDomain.getEClass(nsURI,name);
    }
}