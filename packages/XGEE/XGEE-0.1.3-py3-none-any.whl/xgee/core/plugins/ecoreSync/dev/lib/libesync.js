class ESCore{

    constructor(eoq2domain){
        this.eoq2domain=eoq2domain;
        this.mdb=new ESModelDatabase();
        this.publicAPI=new ESPublicAPI(this);
    }


    async getEPackage(oid){
        var res=null;
        var cmd = new eoq2.Cmp().Get(new eoq2.Qry().Obj(oid).Met("PARENT"))
        .Get(new eoq2.Qry().Met("IF",[new eoq2.Qry().His(-1),new eoq2.Qry().His(-1).Met("CLASSNAME"),null]))
        .Get(new eoq2.Qry().Obj(oid).Pth("nsURI"));

        if(!this.mdb.containsObjectId(oid))
        {
            var results=await this.eoq2domain.Do(cmd);
            var ePackage=Ecore.EPackage.create();
            ePackage.set("nsURI",results[2]);

            //ePackage containment, the full ascending structure is resolved
            //TODO: this might be deferred for better performance, if not required elsewhere
            if(results[1].v=="EPackage")
            {
                let parentPackage=await this.getEPackage(results[0].v);
                parentPackage.get('eSubPackages').add(ePackage);
            }

            this.mdb.add(ePackage);
            res=ePackage;
        }
        else
        {
            res=this.mdb.getById(oid);
        }

        return res
    }

    async initEReference(oid,data=null)
    {
        if(data==null)
        {
            let cmd=new eoq2.Cmp();
            cmd.Get(new eoq2.Qry().Obj(oid).Pth("name"))
            cmd.Get(new eoq2.Qry().Obj(oid).Pth("eType"))
            cmd.Get(new eoq2.Qry().Obj(oid).Pth("containment"))
            cmd.Get(new eoq2.Qry().Obj(oid).Pth("lowerBound"))
            cmd.Get(new eoq2.Qry().Obj(oid).Pth("upperBound"))
            cmd.Get(new eoq2.Qry().His(1).Pth("name"))
            cmd.Get(new eoq2.Qry().His(1).Met("PACKAGE"))
        }
        else
        {

        }
    }


    async initEClass(oid, complete=false){
   
        var eClass=null;
        var status=null;
        var basicInitState=false;
        var completeInitState=false;

        if(!oid)
        {
            throw 'invalid object id during class initialization'
        }
        else
        {
            eClass=this.mdb.getById(oid);
            if(eClass) status=this.mdb.getStatus(eClass);           
        }

        if(status)
        {
            let _AND=function(prev,curr){ return prev && curr};
            basicInitState=!status.isDangling() && status.getFeaturesInitState('name','abstract').reduce(_AND,true);
            completeInitState=basicInitState && status.getFeaturesInitState('eAllReferences','eAllAttributes').reduce(_AND,true);
        }

        if( !basicInitState || complete && !completeInitState )
        {

            let cmd=new eoq2.Cmp();

            cmd.Get(new eoq2.Qry().Obj(oid).Pth("name"))
            cmd.Get(new eoq2.Qry().Obj(oid).Pth("abstract"))
            cmd.Get(new eoq2.Qry().Obj(oid).Met("PACKAGE"))

            if(complete)
            {
                cmd.Get(new eoq2.Qry().Obj(oid).Pth("eAllReferences"))
                cmd.Get(new eoq2.Qry().His(3).Pth("name"))
                cmd.Get(new eoq2.Qry().His(3).Pth("eType"))
                cmd.Get(new eoq2.Qry().His(3).Pth("containment"))
                cmd.Get(new eoq2.Qry().His(3).Pth("lowerBound"))
                cmd.Get(new eoq2.Qry().His(3).Pth("upperBound"))
                cmd.Get(new eoq2.Qry().His(5).Pth("name"))
                cmd.Get(new eoq2.Qry().His(5).Met("PACKAGE"))
                cmd.Get(new eoq2.Qry().Obj(oid).Pth("eAllAttributes"))
                cmd.Get(new eoq2.Qry().His(9).Pth("name"))
                cmd.Get(new eoq2.Qry().His(9).Pth("eType"))
                cmd.Get(new eoq2.Qry().His(11).Pth("name"))
                cmd.Get(new eoq2.Qry().His(11).Met("CLASS").Pth("name"))

            }

            var results=await this.eoq2domain.Do(cmd)
            var ePackage=await initPackage(results.v[2].v);
    
            if(eClass)
            {
                if(!status.isFeatureInitialized('name')) eClass.set('name',results.v[0].v);
                if(!status.isFeatureInitialized('abstract')) eClass.set('abstract',results.v[1].v);
                if(status.isDangling()) eClass.set('abstract',results.v[1].v);
            }
            else
            {
                //add eClass to model database
                this.mdb.add(eClass);
                ePackage.get('eClassifiers').add(eClass);
            }


                    
            

          
            

            //retrieve status from model database and update status
            status=this.mdb.getStatus(eClass);
            status.setFeaturesInitialized('name','abstract');
            if(complete)
            {
                status.setFeaturesInitialized('eAllReferences','eAllAttributes');
            }
        }

        return eClass       
    }


    createQueryObserver(cmd,callback,decode)
    {
        
    }

    destroyQueryObserver(observerToken)
    {

    }

}