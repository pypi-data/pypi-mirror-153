//ecoreSync meta-model synchronization
//(C) 2020 Matthias Brunner / University of Stuttgart, Institute of Aircraft Systems



 export default class EsMetaSync{
    initializer(){

    }
  
    isTypeOf(eObject,typeName)
    {
        return eObject.eClass.get('name')==typeName
    }

    async initEClass(oid, featureInit=false){
        //initializes locally an eClass object
        var self=this;
   
    

        if(!Number.isInteger(oid)) throw 'supplied object id is not an Integer: '

        var eClass=this.lookup(oid);        
        if(eClass && !this.isTypeOf(eClass,'EClass')) throw 'object associated to supplied oid (#'+oid+') is not of type EClass'
        let eClassIsLocallyPresent=eClass?true:false 

        var status=null;
        let statusPresent=false
        
        var basicInitState=false;
        var featureInitState=false;

        if(eClassIsLocallyPresent)
        {
            status=this.mdb.getStatus(eClass);      
            if(status)
            {
                statusPresent=true
                basicInitState=!status.isDangling() && status.isInitialized('name','abstract');
                featureInitState=basicInitState && status.isInitialized('eStructuralFeatures');
            }
        }
    
   


            

        if( !basicInitState || featureInit && !featureInitState )
        {
            let operation={name:'initEClass',args:arguments}

            //sends the operation to the operation handler     
            let res=await this.opHandler.run(operation,async function(){                

                    let cmd=new eoq2.Cmp();

                        //cmds 0-2
                        cmd.Get(new eoq2.Qry().Obj(oid).Pth("name"))
                        cmd.Get(new eoq2.Qry().Obj(oid).Pth("abstract"))
                        cmd.Get(new eoq2.Qry().Obj(oid).Met("PACKAGE"))

                    if(featureInit)
                    {
                        //cmds 3-11
                        cmd.Get(new eoq2.Qry().Obj(oid).Pth("eAllReferences"))
                        cmd.Get(new eoq2.Qry().His(3).Pth("name"))
                        cmd.Get(new eoq2.Qry().His(3).Pth("eType"))
                        cmd.Get(new eoq2.Qry().His(3).Pth("containment"))
                        cmd.Get(new eoq2.Qry().His(3).Pth("lowerBound"))
                        cmd.Get(new eoq2.Qry().His(3).Pth("upperBound"))
                        cmd.Get(new eoq2.Qry().His(5).Pth('name'))
                        cmd.Get(new eoq2.Qry().His(5).Pth('abstract'))
                        cmd.Get(new eoq2.Qry().His(5).Met('PACKAGE'))
               
                        //cmds 12-17
                        cmd.Get(new eoq2.Qry().Obj(oid).Pth("eAllAttributes"))
                        cmd.Get(new eoq2.Qry().His(12).Pth("name"))
                        cmd.Get(new eoq2.Qry().His(12).Pth("eType"))
                        cmd.Get(new eoq2.Qry().His(14).Pth('name'))
                        cmd.Get(new eoq2.Qry().His(14).Met('CLASS').Pth('name'))
                        cmd.Get(new eoq2.Qry().His(14).Pth('instanceClassName'))
                    }

                    var results=await self.eoq2domain.Do(cmd)
                    var ePackage=await self.initEPackage(results[2].v);            
        
                    if(!eClassIsLocallyPresent)
                    {
                        eClass=Ecore.EClass.create();                      
                        ePackage.get('eClassifiers').add(eClass);
                        self.mdb.add(oid,eClass);                        
                    }
                    
                    status=self.mdb.getStatus(eClass);
                    eClass.set('name',results[0]);
                    eClass.set('abstract',results[1]);
                    status.setInitialized('name','abstract');
                    
    

                    if(featureInit)
                    {
                      
                        //initialize eReferences
                        for (let i in results[3])
                        {                        
                            //initialize eType of reference
                            let eType=self.lookup(results[5][i].v);
                            if(!eType){
                                eType=Ecore.EClass.create();      
                                eType.set('name',results[9][i]);     
                                eType.set('abstract',results[10][i]);                   
                                let eType_ePackage=await self.initEPackage(results[11][i].v);  
                                eType_ePackage.get('eClassifiers').add(eType);
                                self.mdb.add(results[5][i].v,eType);
                                let eTypeStatus=self.mdb.getStatus(eClass);
                                eTypeStatus.setInitialized('name','abstract');
                            }

                            let eFeature=self.lookup(results[3][i].v);
                            if(!eFeature){
                                eFeature=Ecore.EReference.create({
                                    name: results[4][i],
                                    eType: eType,
                                    containment: results[6][i],
                                    lowerBound: results[7][i],
                                    upperBound: results[8][i],
                                });
                                self.mdb.add(results[3][i].v,eFeature);
                            }
                         
                            if(!self.utils.isContained(eClass,'eStructuralFeatures',eFeature))  eClass.get("eStructuralFeatures").add(eFeature);                                     

                        }   


                        //initialize eAttributes                   
                        for (let i in results[12])
                        {                        
                            //initialize eType of attribute
                            let eType=null;
                            if(results[16][i]=='EDataType'){
                                if(self.utils.isLocalEcoreElement(results[15][i]))
                                {
                                    eType=self.utils.getLocalEcoreElement(results[15][i]);                                    
                                }
                                else
                                {
                                    eType=self.lookup(results[14][i].v);
                                    if(!eType){
                                        eType=Ecore.EDataType.create();
                                        eType.set('name',results[15][i]);
                                        eType.set('instanceClassName',results[17][i]);
                                        self.mdb.add(results[14][i].v,eType);
                                        let eTypeStatus=self.mdb.getStatus(eType);
                                        eTypeStatus.setInitialized('name','instanceClassName');
                                    }
                                }      
                            } else if(results[16][i]=='EEnum'){
                                
                                eType=self.lookup(results[14][i].v);
                                if(!eType){
                                    eType=Ecore.EEnum.create();
                                    eType.set('name',results[15][i]);
                                    eType.set('instanceClassName',results[17][i]);
                                    self.mdb.add(results[14][i].v,eType);
                                    let eTypeStatus=self.mdb.getStatus(eType);
                                    eTypeStatus.setInitialized('name','instanceClassName');                                   
                                    await self.initEENum(results[14][i].v)
                                }
                            }
                             
                            let eFeature=self.lookup(results[12][i].v);
                            if(!eFeature){
                                eFeature=Ecore.EAttribute.create({
                                    name: results[13][i],
                                    eType: eType
                                });
                                self.mdb.add(results[12][i].v,eFeature);
                            }
                            
                            if(!self.utils.isContained(eClass,'eStructuralFeatures',eFeature))  eClass.get("eStructuralFeatures").add(eFeature);  
                        }  
                    }

                    //retrieve status from model database and update status

                 
                    if(featureInit)
                    {
                        status.setInitialized('eStructuralFeatures');
                    }

                    return eClass;
            });

            eClass=eClass?eClass:res

            
        }

        return eClass       
    }

    async getEClass(nsURI,name){

        var eClass=this.mdb.getEClass(nsURI,name);
        if(!eClass)
        {
            let cmd=CMD.Cmp();
            cmd.Get(QRY.Met('CLASS',[nsURI,name]))
            cmd.Get(new eoq2.Qry().His(0).Pth("name"))
            cmd.Get(new eoq2.Qry().His(0).Pth("abstract"))
            cmd.Get(new eoq2.Qry().His(0).Met("PACKAGE"));      
            var results=await this.eoq2domain.Do(cmd);
            eClass=this.lookup(results[0].v);
            if(!eClass)
            {
                eClass=Ecore.EClass.create();
                eClass.set('name',results[1]);
                eClass.set('abstract',results[2]);
                var ePackage=await this.initEPackage(results[3].v);
                ePackage.get('eClassifiers').add(eClass);
                this.mdb.add(results[0].v,eClass);
                let status=this.mdb.getStatus(eClass);
                status.setInitialized('name','abstract');            
            }
        }
        return eClass;
    }

    async initEPackage(oid)
    {
        //initializes locally an ePackage object
        var self=this;
        if(!Number.isInteger(oid)) throw 'supplied object id is not an Integer / EPackage'
        var ePackage=this.lookup(oid);        
        if(ePackage && !this.isTypeOf(ePackage,'EPackage')) throw 'object associated to supplied oid (#'+oid+') is not of type EPackage'
        if(!ePackage)
        {
            let operation={name:'initEPackage',args:arguments};
            ePackage=await this.opHandler.run(operation, async function(){
                var cmd = new eoq2.Cmp().Get(new eoq2.Qry().Obj(oid).Met("PARENT"))
                .Get(new eoq2.Qry().Met("IF",[new eoq2.Qry().His(-1),new eoq2.Qry().His(-1).Met("CLASSNAME"),null]))
                .Get(new eoq2.Qry().Obj(oid).Pth("nsURI"))
                .Get(new eoq2.Qry().Obj(oid).Pth("name"))
                .Get(new eoq2.Qry().Obj(oid).Pth("nsPrefix"));
                var results=await self.eoq2domain.Do(cmd);
                var ePackage=Ecore.EPackage.create();
                ePackage.set("nsURI",results[2]);       
                ePackage.set("name",results[3]);   
                ePackage.set("nsPrefix",results[4]);       

                //the full ascending ePackage containment structure is resolved
                //TODO: this might be deferred for better performance, if not required elsewhere    
                if(results[1]=="EPackage")
                {        
                    let parentPackage=await self.initEPackage(results[0].v);
                    parentPackage.get('eSubpackages').add(ePackage);
                }       

                self.mdb.add(oid,ePackage);    
                return ePackage
            });       
        }
        return ePackage;
    }

    async initEENum(oid)
    {
        //initializes locally an eENum object
        var self=this;
        var eENum=this.lookup(oid);  
        if(eENum && !this.isTypeOf(eENum,'EEnum')) throw 'object associated to supplied oid (#'+oid+') is not of type EENum ('+eENum.eClass.get('name')+')'
        if(!eENum)
        {
            eENum=Ecore.EEnum.create();
            self.mdb.add(oid,eENum);
        }
        var status=this.mdb.getStatus(eENum);
        if(!status.isInitialized('name','eLiterals'))
        {
            let operation={name:'initEENum',args:arguments};
            eENum=await self.opHandler.run(operation, async function(){
                var cmd = new eoq2.Cmp();
                cmd.Get(QRY.Obj(oid).Pth('name'))
                cmd.Get(QRY.Obj(oid).Pth('eLiterals'))

                var results=await self.eoq2domain.Do(cmd);
                
                eENum.set('name',results[0]);

                for(let i in results[1])
                {
                    let eLiteral=Ecore.EEnumLiteral.create();
                    eLiteral.set("name",results[1][i]);
                    eLiteral.set("literal",results[1][i]);
                    eLiteral.set("value",i);
                    eENum.get('eLiterals').add(eLiteral);
                }     
                 
                return eENum
            });   
        }
        return eENum
    }

}