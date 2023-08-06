/* ecoreSync (v2) mdb accessor compatibility layer (MACL) */

/* The ecoreSync mdbAccessor EOQ compatibility layer is used to enable hybrid (local/remote) query evaluation.  
   It provides access to the ecoreSync model database in a EOQ2 compatible manner. */

/* The ecoreSync mdbAccessor is based on the pyeoq2 mdbAccessor. The original python code was written by Björn Annighöfer */
/* (C) 2020 Instiute of Aircraft Systems, Matthias Brunner */


export default class EsMdbAccessor
{
    constructor(esDomain){
        this._esDomain=esDomain;
    }

    async Lock(){
        //reserved for future use
    }

    async Release(){
         //reserved for future use
    }

    async GetAllMetamodels(){
        console.debug('get all meta model unsupported')
    }

    async RegisterMetamodel(pck){
        console.debug('register meta model unsupported')
    }

    async UnregisterMetamodel(pck){
        console.debug('unregister meta model unsupported')
    }

    /* MODEL ACCESSORS */

    async GetRoot(){
        var root=await this._esDomain.getObject(0)
        return this._esDomain.utils.encode(root)
    }

    async Get(obj,feature){
        /* Gets the feature contents for an encoded object */
        /* Returns encoded objects */
      
        if(!obj) { throw 'FATAL ERROR in mdbAccessor Get Operation: object is undefined, feature='+feature }
        var res=null;
        var decodedObject=await this._esDomain.utils.decode(obj)  
         
        if(decodedObject)
        {     
            try{
            var value=await this._esDomain.get(decodedObject,feature)             
            res=this._esDomain.utils.encode(value);
            }
            catch(e){
                throw 'mdbAccessor failed to get #'+this._esDomain.rlookup(decodedObject)+'/'+feature+': '+e;
            }
        }
        else
        {
            if(obj.eClass.getEStructuralFeature(feature).get("upperBound")!=1)
            {
                res=[]
            }
        }
        return res
    }

    async Set(obj,feature,value){
        var decodedObject=await this._esDomain.utils.decode(obj)  
        var decodedValue=value
        if(value && value.qry=="OBJ"){  decodedValue=await this._esDomain.utils.decode(value)  } 
        return this._esDomain.set(decodedObject,feature,decodedValue)
    }

    async GetParent(obj){ 
        var res=null;
        var decodedObject=await this._esDomain.utils.decode(obj) 
        if(decodedObject.eContainer)
        {
            res=this._esDomain.utils.encode(decodedObject.eContainer)
        }
        else
        {
            res=await ecoreSync.remoteExec(new eoq2.Get(new eoq2.Obj(obj.v).Met('PARENT')))
        }    
        return res
    }

    async GetAssociates(obj,root){ 
        //ecoreSync is currently not able to track whether this query has already been carried out  (or has changed), so we have to do it remotely everytime
        var root=await root
        var res= await this._esDomain.remoteExec(new eoq2.Get(new eoq2.Obj(obj.v).Met('ASSOCIATES',new eoq2.Obj(root.v))))
        return res
    }
   


    async GetAllParents(obj){
        let parents=[]
        let parent=await this.GetParent(obj)
        parents.push(parent)

        while(parent != null)
        {
            parent=await this.GetParent(parent)
            if(parent!=null)
            {              
                parents.push(parent)
            }

        }
        parents.reverse()        
        return parents
    }

    GetIndex(obj){
        console.debug('get index unsupported')
    }

    async GetContainingFeature(obj){
        let decodedObject=await this._esDomain.utils.decode(obj)
        if(decodedObject.eContainingFeature==null)
        {
           //causes ecoreSync to load the parent and populate the containing feature
           let parentObj=await this.GetParent(obj)
           let featureName=await this._esDomain.remoteExec(new eoq2.Get(new eoq2.Obj(obj.v).Met('CONTAININGFEATURE').Pth('name')))
           await this._esDomain.get(await this._esDomain.utils.decode(parentObj),featureName)
        }     
        return decodedObject.eContainingFeature
    }

    async Add(obj,feature,child){
        var res=null;
        var decodedObject=await this._esDomain.utils.decode(obj)
        var decodedChild=await this._esDomain.utils.decode(child)
        if(decodedObject!=null && decodedChild!=null)
        {
            res=await this._esDomain.add(decodedObject,feature,decodedChild)
        }
        return res;
    }

    async Remove(obj,feature,child)
    {        
        var res=null;
        var decodedObject=await this._esDomain.utils.decode(obj)
        var decodedChild=await this._esDomain.utils.decode(child)
        if(decodedObject!=null && decodedChild!=null)
        {
            res=await this._esDomain.remove(decodedObject,feature,decodedChild)
        }
        return res;  
    }

    async RemoveMany(obj,feature,children)
    {
        var res=null;
        var decodedObject=await this._esDomain.utils.decode(obj)
        var decodedChildren=await this._esDomain.utils.decode(children)   
        res=await this._esDomain.removeMany(decodedObject,feature,decodedChildren)
        return res;  
    }

    Move(obj,newIndex){
        console.debug('move unsupported')
    }

    async Clone(obj,mode){
        var res=null;
        var cloneModes=new Map([['CLS','class'],['DEP','deep'],['ATT','attributes'],['FUL','full']]);       
        if(!cloneModes.has(mode)) throw 'the supplied clone mode is invalid'
        var decodedObject=await this._esDomain.utils.decode(obj)
        res=this._esDomain.clone(decodedObject,1,cloneModes.get(mode))
        return res;
    }

    async Create(clazz,n,constructorArgs=[])
    {
        var res=null;
        var response=await this._esDomain.create(clazz,n)    
        if(n>1)
        {
            res=response.map(function(r){
                return this._esDomain.utils.encode(r);
            })
        }
        else
        {   
            if(n==1){
                res=this._esDomain.utils.encode(response);
            }
            else
            {
                res=response //returns []
            }
        }    
        return res;
    }

    async CreateByName(packageName,className,n,constructorArgs=[])
    {    
        var self=this;
        var res=null;
        let response=await this._esDomain.createByName(packageName,className,n);
        if(n>1)
        {
            res=response.map(function(r){
                return self._esDomain.utils.encode(r);
            })
        }
        else
        {   
            if(n==1){
                res=this._esDomain.utils.encode(response);
            }
            else
            {
                res=response //returns []
            }
        }    
        return res;
    }

    async GetClassByName(packageName,className){
        return this._esDomain.utils.encode(await this._esDomain.getEClass(packageName,className))
    }

    async Class(obj){
        var decodedObject=await this._esDomain.utils.decode(obj)
        return ecoreSync.utils.encode(decodedObject.eClass)
    }

    async ClassName(obj){
        var decodedObject=await this._esDomain.utils.decode(obj)
        return decodedObject.eClass.get("name")
    }

/* CLASS ACCESSORS */

    Package(clazz){
        return clazz.eContainer
    }

    Supertypes(clazz){
        console.debug('supertypes unsupported')
    }

    async AllSupertypes(clazz){
        //ecoreSync is currently not able to track whether this query has already been carried out  (or has changed), so we have to do it remotely everytime
        var res= await this._esDomain.remoteExec(new eoq2.Get(new eoq2.Obj(clazz.v).Met('ALLSUPERTYPES')))
        return res
    }

    async Implementers(clazz){
        //unfortunaetly, we can never know whether the whole meta model is present locally, therefore we have to resort to an external call
        //ecoreSync is currently not able to track whether this query has already been carried out  (or has changed), so we have to do it remotely everytime
        var res= await this._esDomain.remoteExec(new eoq2.Get(new eoq2.Obj(clazz.v).Met('IMPLEMENTERS')));
        return res.v;
    }
    
    async AllImplementers(clazz){
        //unfortunaetly, we can never know whether the whole meta model is present locally, therefore we have to resort to an external call
        //ecoreSync is currently not able to track whether this query has already been carried out (or has changed), so we have to do it remotely everytime
        var res= await this._esDomain.remoteExec(new eoq2.Get(new eoq2.Obj(clazz.v).Met('ALLIMPLEMENTERS')));
        return res.v;
    }

    async GetAllChildrenOfType(obj,className){
        var res=[];
        if(obj!=null)
        {
            var cmd=CMD.Get(QRY.Obj(obj.v).Cls(className));
            res=await this._esDomain.remoteExec(cmd); //remote answering the query
        }
        return res
    }

    async GetAllChildrenInstanceOfClass(obj,className){
        var res=[];
        if(obj!=null)
        {
            var cmd=CMD.Get(QRY.Obj(obj.v).Ino(className));
            res=await this._esDomain.remoteExec(cmd); //remote answering the query
        }
        return res
    }

    GetAllFeatures(obj){
        return obj.eClass.get("eStructuralFeatures").array()
    }

    GetAllFeatureNames(obj){
        return obj.eClass.get("eStructuralFeatures").array().map(function(e){ return e.get("name")})
    }

    GetAllFeatureValues(obj){
        console.debug('feature values unsupported')
    }

    GetAllAttributes(obj){
        console.debug('attributes values unsupported')
    }
    
    GetAllAttributeNames(obj){
        console.debug('attributes unsupported')
    }

    GetAllAttributes(obj){
        console.debug('attributes unsupported')
    }
    
    GetAllAttributeNames(obj){
        console.debug('attributes unsupported')
    }
        
    GetAllAttributeValues(obj){
        console.debug('attributes unsupported')
    }

    GetAllReferences(obj){
        console.debug('references unsupported')
    }
    
    async GetAllReferenceNames(obj){
       var decodedObject=await this._esDomain.utils.decode(obj)  
       await this._esDomain.utils.isEClassInitialized(decodedObject.eClass)
       var references=decodedObject.eClass.get('eAllReferences')
       return references.map((ref) => { return ref.get('name') })   
    }
        
    GetAllReferenceValues(obj){
        console.debug('references unsupported')
    }

    GetAllContainments(obj){
        console.debug('containments unsupported')
    }
    
    GetAllContainmentNames(obj){
        console.debug('containments unsupported')
    }
        
    GetAllContainmentValues(obj){
        console.debug('containments unsupported')
    }

}



