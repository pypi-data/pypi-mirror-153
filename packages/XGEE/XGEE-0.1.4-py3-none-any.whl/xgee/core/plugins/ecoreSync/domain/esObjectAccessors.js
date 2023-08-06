import {UnknownObject, NoSuchFeature} from './esErrors.js'

export default class EsObjectAccessors{
    initializer(){

    }
	//Object interaction
    async get(eObject,featureName){
        var res=null;
        var self=this;
        var oid=self.rlookup(eObject);
        if(!Number.isInteger(oid)) throw new UnknownObject('cannot get a feature of an unknown eObject')

        if(!self.utils.isBuiltInClass(eObject.eClass))
        {
            var classOid=self.rlookup(eObject.eClass);
            if(!Number.isInteger(classOid)){
                throw new UnknownObject('the eClass of the supplied eObject is unknown in this ecoreSync domain')
            }
            await this.initEClass(classOid,true) //ensures that the eClass is fully initialized
        }

        var feature=eObject.eClass.getEStructuralFeature(featureName);
        var ft=eObject.get(featureName);        
        if(!feature) throw new NoSuchFeature('no feature '+featureName+' exists for the supplied eObject (#'+oid+') of type '+eObject.eClass.get('name'))
        var status=this.mdb.getStatus(eObject);
        if(!status.isInitialized(featureName))
        {  
            var token=this.mdb.lockFeature(oid,featureName);
            if(token!=null)
            {
                let cmd=CMD.Cmp();
                cmd.Get(QRY.Obj(oid).Pth(featureName));
                if(feature.eClass.get('name')=='EReference')
                {
                    cmd.Get(QRY.His(-1).Trm().Met('CLASS'))
                } 
                let results=await self.eoq2domain.Do(cmd);


                if(feature.eClass.get('name')=='EReference')
                {                  
                    if(feature.get('upperBound')!=1)
                    {         

                        let resObjs=self.lookup(results[0].map(function(e){ return e.v; }));
                
                        let unsyncedObjects=[];

                        for(let i=0;i<resObjs.length;i++)
                        {
                            if(resObjs[i])
                            {
                                if(!self.utils.isContained(eObject,featureName,resObjs[i]))
                                {
                                    ft.add(resObjs[i]);                        
                                } 
                            }
                            else
                            {         
                                
                                let token=self.mdb.lockObjectId(results[0][i].v);
                                if(token!=null)
                                {    
                                    unsyncedObjects.push(self.initEClass(results[1][i].v).then(function(eClass){
                                        let eObject=eClass.create();
                                        self.mdb.add(results[0][i].v,eObject,token);
                                        ft.add(eObject);     
                                        return eObject;
                                    }));     
                                }
                                else
                                {            
                                    unsyncedObjects.push((async () => {
                                        let eObject=await self.mdb.waitForObject(results[0][i].v)
                                        ft.add(eObject); 
                                        return eObject;
                                    })());
                                }    
                                    
                                    
                            }
                        }

                        await Promise.all(unsyncedObjects);  
                        res=ft.array();                          
                                
                    }
                    else
                    {                     
                        if(results[0]!=null)
                        {                           
                            let resObj=self.lookup(results[0].v);
                            if(!resObj)
                            {   
                                let token=self.mdb.lockObjectId(results[0].v);
                                if(token!=null)
                                {
                                    let resEClass=await self.initEClass(results[1].v,true);
                                    resObj=resEClass.create();
                                    self.mdb.add(results[0].v,resObj,token);
                                }
                                else
                                {
                                    resObj=await self.mdb.waitForObject(results[0].v)
                                }
                            }
                            eObject.set(featureName,resObj);
                            res=resObj;               

                        }
                        else
                        {
                            eObject.unset(featureName);
                        }
                    }
        
                } else if( feature.eClass.get('name')=='EAttribute' ){

                    if(results[0]!=null)
                    {
                        eObject.set(featureName,results[0]);
                    }
                    else
                    {
                        eObject.unset(featureName);
                    }
                    res=results[0];
                }        
                
                this.mdb.setFeatureInitialized(oid,featureName,token);
            }
            else
            {
                res=await this.mdb.waitForFeature(oid,featureName)
            }
        }
        else
        {
            res=ft;
            if(feature.get('upperBound')!=1)
            {
                res=res.array();
            }
        }    
        

        return res;     
    }

    async set(eObject,featureName,newValue){
        var res=false;
        var self=this;
        var oid=self.rlookup(eObject);
        if(!Number.isInteger(oid)) throw new UnknownObject('cannot set a feature of an unknown eObject')
        var classOid=self.rlookup(eObject.eClass);
        if(!Number.isInteger(classOid)) throw new UnknownObject('the eClass of the supplied eObject is unknown in this ecoreSync domain')
        
        //Esnure initialization of eClass
        await this.initEClass(classOid,true) 

        var feature=eObject.eClass.getEStructuralFeature(featureName);     
        if(!feature) throw new NoSuchFeature('no feature '+featureName+' exists for the supplied eObject (#'+oid+') of type '+eObject.eClass.get('name'))

        if(this.utils.checkType(feature.get('eType'),newValue))
        {

            let cmd=CMD.Set(QRY.Obj(oid),featureName,this.utils.valueToQuery(feature.get('eType'),newValue));
            var status=this.mdb.getStatus(eObject);   
            
            try{               
                await this.eoq2domain.Do(cmd);
                eObject.set(featureName,newValue); //TODO: could be set beforehand and reverted back on failure for speed
                if(!status.isInitialized(featureName)) status.setInitialized(featureName);        
            }
            catch(e)
            {
                throw 'could not set feature '+featureName+' for #'+oid+' to value='+newValue+': error='+e;
            }
        }
        else
        {
            throw 'the supplied value is not of type '+feature.get('eType').get('name')
        }
        return res;
    }

    async unset(eObject,featureName){
        var res=false;
        var self=this;
        var oid=self.rlookup(eObject);
        if(!Number.isInteger(oid)) throw new UnknownObject('cannot unset a feature of an unknown eObject')
        if( typeof featureName != 'string' ) throw new TypeError('feature name must be a string')
        var classOid=self.rlookup(eObject.eClass);
        if(!Number.isInteger(classOid)) throw new UnknownObject('the eClass of the supplied eObject is unknown in this ecoreSync domain')
        await this.initEClass(classOid,true) //ensures that the eClass is fully initialized
        var feature=eObject.eClass.getEStructuralFeature(featureName);     
        if(!feature) throw new NoSuchFeature('no feature '+featureName+' exists for the supplied eObject (#'+oid+') of type '+eObject.eClass.get('name'))
        try{

            if(feature.get('upperBound')!=1){
                eObject.get(featureName).clear();  
                await this.eoq2domain.Do(CMD.Set(QRY.Obj(oid),featureName,new eoq2.Arr()));
            }
            else
            {
                eObject.unset(featureName);
                await this.eoq2domain.Do(CMD.Set(QRY.Obj(oid),featureName,null));
            }                 
            res=true;
        }
        catch(e){
            res=false;
            console.error('failed to unset feature '+featureName+' : '+e);  
        }
        return res;
    }

    async add(eContainer,featureName,eObject){
        var res=false;
        var self=this;
        var containerOid=self.rlookup(eContainer);
        if(!Number.isInteger(containerOid)) throw new UnknownObject('the supplied eContainer is unknown in this ecoreSync domain')
        var oid=self.rlookup(eObject);
        if(!Number.isInteger(oid)) throw new UnknownObject('the supplied eObject is unknown in this ecoreSync domain')
        if( typeof featureName != 'string' ) throw new TypeError('feature name must be a string')

        //Satisfy pre-conditions
        //Ensure full initialization of eClass of the eContainer
        var containerClassOid=self.rlookup(eContainer.eClass);
        if(!Number.isInteger(containerClassOid)) throw new UnknownObject('the eClass of the supplied eContainer is unknown in this ecoreSync domain')
        await this.initEClass(containerClassOid,true) //ensures that the eClass is fully initialized

        //Ensure full initialization of eClass of the eObject
        var eObjectClassOid=self.rlookup(eObject.eClass);
        if(!Number.isInteger(eObjectClassOid)) throw new UnknownObject('the eClass of the supplied eObject is unknown in this ecoreSync domain')
        await this.initEClass(eObjectClassOid,true) //ensures that the eClass is fully initialized

        var feature=eContainer.eClass.getEStructuralFeature(featureName);     
        if(!feature) throw 'ADD FAILED: no feature '+featureName+' exists for the supplied eObject (#'+oid+') of type '+eContainer.eClass.get('name')
        var status=this.mdb.getStatus(eObject);
        if(!status.isInitialized(featureName)) await this.get(eContainer,featureName) //ensures correct order, could be later replaced by more sophisticated code
  
        try{
            let cmd=CMD.Add(QRY.Obj(containerOid),featureName,QRY.Obj(oid));
            await this.eoq2domain.Do(cmd);
            if(!self.utils.isContained(eContainer,featureName,eObject))
            {
                eContainer.get(featureName).add(eObject); //TODO: could be set beforehand and reverted back on failure for speed
            }
            res=true;
        }
        catch(e)
        {
            res=false;
            console.error('failed to add #'+oid+' to '+featureName+' in #'+containerOid+' : '+e);  
        }

        return res;
    }

    async remove(eContainer,featureName,eObject){
        var res=false;
        var self=this;
    
        //Check input values
        var containerOid=self.rlookup(eContainer);
        if(!Number.isInteger(containerOid)) throw new UnknownObject('the supplied eContainer is unknown in this ecoreSync domain')
        var oid=self.rlookup(eObject);
        if(!Number.isInteger(oid)) throw new UnknownObject('the supplied eObject is unknown in this ecoreSync domain')
        if( typeof featureName != 'string' ) throw new TypeError('feature name must be a string')

        //Class initialization and check for feature presence
        var classOid=self.rlookup(eContainer.eClass);
        if(!Number.isInteger(classOid)) throw new UnknownObject('the eClass of the supplied eObject is unknown in this ecoreSync domain')
        await this.initEClass(classOid,true) //ensures that the eClass of the eContainer is fully initialized
        var feature=eContainer.eClass.getEStructuralFeature(featureName);     
        if(!feature){    
            throw 'REMOVE FAILED: no feature '+featureName+' exists for the supplied eObject (#'+containerOid+') of type '+eContainer.eClass.get('name')
        } 

        //Enforce feature initialization (ensures correct order)
        var status=this.mdb.getStatus(eContainer);
        if(!status.isInitialized(featureName)) await this.get(eContainer,featureName)
  
        try{
            let cmd=CMD.Rem(QRY.Obj(containerOid),featureName,QRY.Obj(oid));
            await this.eoq2domain.Do(cmd);
            if(self.utils.isContained(eContainer,featureName,eObject))
            {
                eContainer.get(featureName).remove(eObject); //TODO: could be set beforehand and reverted back on failure for speed
            }
            res=true;
        }
        catch(e)
        {
            res=false;
            console.error('failed to remove #'+oid+' from '+featureName+' in #'+containerOid+' : '+e);  
        }

        return res;
    }
    
    async removeMany(eContainer,featureName,eObjects)
    {
        var res=false;
        var self=this;
    
        var containerOid=self.rlookup(eContainer);
        if(!Number.isInteger(containerOid)) throw new UnknownObject('the supplied eContainer is unknown in this ecoreSync domain')
        if( typeof featureName != 'string' ) throw new TypeError('feature name must be a string')

        var checkEObject=async (eObject) => {
            //Check input values
            var oid=self.rlookup(eObject);
            if(!Number.isInteger(oid)) throw new UnknownObject('the supplied eObject is unknown in this ecoreSync domain')        
        }

        for(let eObject of eObjects)
        {
            await checkEObject(eObject)
        }

  
        //Class initialization and check for feature presence
        var classOid=self.rlookup(eContainer.eClass);
        if(!Number.isInteger(classOid)) throw new UnknownObject('the eClass of the supplied eObject is unknown in this ecoreSync domain')
        await this.initEClass(classOid,true) //ensures that the eClass of the eContainer is fully initialized
        var feature=eContainer.eClass.getEStructuralFeature(featureName);     
        if(!feature){    
            throw 'REMOVE FAILED: no feature '+featureName+' exists for the supplied eObject (#'+containerOid+') of type '+eContainer.eClass.get('name')
        } 

        //Enforce feature initialization (ensures correct order)
        var status=this.mdb.getStatus(eContainer);
        if(!status.isInitialized(featureName)) await this.get(eContainer,featureName)
  
        try{
            let cmd=CMD.Rem(QRY.Obj(containerOid),featureName,this.utils.encode(eObjects));
            await this.eoq2domain.Do(cmd);
            for(let eObject of eObjects)
            {
                if(self.utils.isContained(eContainer,featureName,eObject))
                {
                    eContainer.get(featureName).remove(eObject); //TODO: could be set beforehand and reverted back on failure for speed
                }       
            }
            res=true;
        }
        catch(e)
        {
            res=false;
            console.error('failed to remove multiple objects from '+featureName+' in #'+containerOid+' : '+e);  
        }

        return res;
    }

    async clear(eContainer,featureName)
    {
        var res=false
        var self=this
        var containerOid=self.rlookup(eContainer);
        if(!Number.isInteger(containerOid)) throw new UnknownObject('the supplied eContainer is unknown in this ecoreSync domain')
        if( typeof featureName != 'string' ) throw new TypeError('feature name must be a string')
        try{
            let cmd=CMD.Rem(QRY.Obj(containerOid),featureName,QRY.Obj(containerOid).Pth(featureName));
            await this.eoq2domain.Do(cmd);                
            eContainer.get(featureName).clear()           
            res=true;
        }
        catch(e)
        {
            res=false;
            console.error('failed to remove multiple objects from '+featureName+' in #'+containerOid+' : '+e);  
        }
    }

    //Object creation and replication
    async create(eClass,n=1){
        var results=null;
        var classOid=this.rlookup(eClass);
        if(!Number.isInteger(classOid)) throw new UnknownObject('the eClass of the supplied eObject is unknown in this ecoreSync domain')
        if(!Number.isInteger(n) || n<0) throw 'cannot create n='+n+' objects, n must be a positive integer'

        if(n>0)
        {
            let cmd= new eoq2.Crt(QRY.Obj(classOid),n);
            var res=await this.eoq2domain.Do(cmd);
            if(n>1)
            {
                results=[];
                for(let i=0; i<res.length; i++){
                    let eObject=eClass.create();
                    this.mdb.add(res[i].v,eObject);
                    results.push(eObject);
                }       
            }
            else
            {
                let eObject=eClass.create();
                this.mdb.add(res.v,eObject);
                results=eObject;
            } 
        }
        return results;
    }

    async createByName(nsURI,name,n=1)
    {
       
        var res=null;
        if(!Number.isInteger(n) || n<0) throw 'cannot create n='+n+' objects, n must be a positive integer'

        if(n>0)
        {
            let cmd=new eoq2.Cmp();
                cmd.Gmm()
                cmd.Get(new eoq2.Qry().His(-1).Sel(new eoq2.Qry().Pth('nsURI').Equ(nsURI)).Cls('EClass').Sel(new eoq2.Qry().Pth('name').Equ(name)).Idx('FLATTEN').Trm(new eoq2.Met('SIZE').Equ(0),[]).Idx(0));
                cmd.Crt(new eoq2.Qry().His(-1),n);
            try{            
                let results=await this.remoteExec(cmd);
                let eClass=await this.initEClass(results[1].v,false); 

                var oids=[];
                if(n>1){
                    oids=results[2].map(function(e){ return e.v; });
                }
                else
                {
                    oids=[results[2].v];
                }
                
                if(n>1)
                {
                    res=[];
                    for(let i=0;i<results[2].length;i++)
                    {
                        let eObject=eClass.create();
                        this.mdb.add(results[2][i].v,eObject);
                        res.push(eObject);
                    }   
                }
                else
                {
                    let eObject=eClass.create();
                    this.mdb.add(oids[0],eObject);
                    res=eObject;
                }         
            }
            catch(e)
            {
                throw 'failed to create object(s): '+e;
            }
        }

        return res;
    }

    async clone(eObject,n=1,mode='deep'){
        var res=null;
        var cloneModes=new Map([['class','CLS'],['deep','DEP'],['attributes','ATT'],['full','FUL']]);       
        if(!cloneModes.has(mode)) throw 'the supplied clone mode is invalid'
        var oid=this.rlookup(eObject);
        if(!Number.isInteger(oid)) throw new UnknownObject('the supplied eObject is unknown in this ecoreSync domain')
        if(!Number.isInteger(n) || n<=0) throw 'cannot create n='+n+' objects, n must be a positive integer'
        var eClass=eObject.eClass;
        let eoqCloneMode=cloneModes.get(mode);
        let cmd=CMD.Cmp();

        for(let i=0;i<n;i++)
        {
            cmd.Clo(QRY.Obj(oid),eoqCloneMode);
        }

        try{            
            let results=await this.eoq2domain.Do(cmd);           
            if(n>1)
            {
                res=[];
                for(let i=0;i<n;i++)
                {
                    let eObject=eClass.create();
                    this.mdb.add(results[i].v,eObject);
                    res.push(eObject);
                }   
            }
            else
            {
                let eObject=eClass.create();
                this.mdb.add(results[0].v,eObject);
                res=eObject;
            }                   
        }
        catch(e)
        {
            throw 'failed to create object(s): '+e;
        }

        return res;
    }

} 
