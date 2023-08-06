
var builtInClasses=Object.values(Ecore).filter((val) => { return val.eClass?true:false })

class EsUtilities{
    constructor(esDomain){
        this._esDomain=esDomain;
    }

    async isEClassInitialized(eClass)
    {
        var oid=this._esDomain.rlookup(eClass);
        if(oid!=null){
            return this._esDomain.initEClass(oid,true);
        }
    }

    isContained(eContainer,featureName, eObject)
    {
        var res=false;
        if(eContainer.get(featureName).array().includes(eObject))
        {
            res=true;
        }
        return res;
    }

    isLocalEcoreElement(name){
        let res=false;
        if(name=='EInteger') name='EInt'
        var keys=Object.keys(Ecore);
        if( keys.includes(name) )
        {
            res=true;
        }
        return res;
    }

    getLocalEcoreElement(name){
        let res=null;
        if(name=='EInteger') name='EInt'
        var keys=Object.keys(Ecore);
        if( keys.includes(name) )
        {
            res=Ecore[name]
        }
        return res;
    }

    checkType(eType,value){
        //ecoreSync integrated type checking
        var res=false;
        var typeName=''

        switch(eType.eClass.get('name'))
        {
            case "EDataType":
                typeName=eType.get('name')
                break;
            case "EEnum":
                typeName='EEnum'
                break;
            default:
                typeName='unsupported'
                break;
        }

        switch(typeName)
        {
            case "EChar":
                if(typeof value == 'string' && value.length==1) res=true;
                break;
            case "EString":
                if(typeof value == 'string') res=true;
                break;
            case "EInt":
                if(Number.isInteger(value) && value!=null) res=true;
                break;
            case "EByte":
                if(Number.isInteger(value) && value!=null) res=true;
                break;
            case "EFloat":
                if(typeof value == 'number' && value!=null) res=true;
                break;
            case "EDouble":
                if(typeof value == 'number' && value!=null) res=true;
                break;
            case "EBoolean":
                if(typeof value == 'boolean') res=true;
                break;
            case "EEnum":
                if(typeof value == 'string') res=true; //because EOQ expects it like this
                break;
            case "EInteger":  //ecorejs compatibility support
                if(Number.isInteger(value) && value!=null) res=true;
                break;
            default:
                res=true; //seems to be custom type, we won't bother with that
                break;
        }
        return res;
    }

    valueToQuery(eType,value)
    {
        var res=null;
        
        if(this.checkType(eType,value))
        {

            var typeName=''
            switch(eType.eClass.get('name'))
            {
                case "EDataType":
                    typeName=eType.get('name')
                    break;
                case "EEnum":
                    typeName='EEnum'
                    break;
                default:
                    typeName='unsupported'
                    break;
            }

            switch(typeName)
            {
                case "EChar":
                    res=value;
                    break;
                case "EString":
                    res=String(value);
                    break;
                case "EInt":
                    res=value;
                    break;
                case "EByte":
                    res=value;
                    break;
                case "EFloat":                     
                    res=value;
                    if(Number.isInteger(value)) res+=1e-5;
                    break;
                case "EDouble":
                    res=value;
                    if(Number.isInteger(value)) res+=1e-5;
                    break;
                case "EBoolean":
                    res=value;
                    break;
                case "EEnum":
                    res=value;
                    break;
                case "EInteger":  //ecorejs compatibility support
                    res=value;
                    break;
                default:
                    if(value!=null)
                    {
                        let oid=this._esDomain.rlookup(value);
                        if(oid!=null) {
                            res=QRY.Obj(oid);
                        }
                        else
                        {
                            throw 'unknown datatype conversion'
                        }
                    }
                    else
                    {
                        res=value //no conversion of null value
                    }
                    break;
            }
        }
        else
        {
            throw 'supplied value was of incompatible type'
        }
        return res;
    }

    isBuiltInClass(eClass)
    {
        var Ecore=window["Ecore"]        
        let res=builtInClasses.find((clazz) => { return clazz == eClass})?true:false
        return res
    }

    isObjectURL(url){
        var res=false;
        if(typeof url == 'string')
        {
            if(url.includes('eoq://') && url.includes('/#'))
            {
                res=true;
            }
        }
        return res;
    }

    getObjectURL(eObject){
        var oid=this._esDomain.rlookup(eObject);
        if(oid==null) throw 'the supplied eObject is unknown to ecoreSync'        
        return (this._esDomain.eoq2domain.url+'/#'+oid).replace('ws://','eoq://').replace('ws/eoq.do/','');
    }

    async getObjectByURL(url){
        var res=null;
        if(this.isObjectURL(url))
        {
            let domainHost=url.substr(url.indexOf('eoq://')+6,url.indexOf('/#')-(url.indexOf('eoq://')+6));            
            if(this._esDomain.eoq2domain.url.includes(domainHost))
            {
                let objId=Number.parseInt(url.substr(url.indexOf('/#')+2));
                res=this._esDomain.getObject(objId);
            }
            return res;
        }
    }

    async getResource(eObject)
    {
        //gets the  EOQ resource containing the supplied eObject
        let oid=this._esDomain.rlookup(eObject);
        if(oid==null) throw 'the supplied eObject is unknown to ecoreSync'
        let cmd=CMD.Get(QRY.Obj(oid).Met("ALLPARENTS").Sel(new eoq2.Qry().Met("CLASSNAME").Equ("ModelResource")).Trm(new eoq2.Met('SIZE').Equ(0),null).Idx(0));
        let mdlResource=await this._esDomain.remoteExec(cmd,true);   
        return mdlResource;        
    }

    async getModelRoot(eObject)
    {
        //gets the  EOQ resource containing the supplied eObject
        let oid=this._esDomain.rlookup(eObject);
        if(oid==null) throw 'the supplied eObject is unknown to ecoreSync'
        let cmd=CMD.Get(QRY.Obj(oid).Met("ALLPARENTS").Sel(new eoq2.Qry().Met("CLASSNAME").Equ("ModelResource")).Trm(new eoq2.Met('SIZE').Equ(0),null).Idx(0).Pth('contents').Trm(new eoq2.Met('SIZE').Equ(0),null).Idx(0));
        let mdlRoot=await this._esDomain.remoteExec(cmd,true);   
        return mdlRoot;        
    }

    async getContainer(eObject)
    {
        //gets the eContainer of the supplied object
        var res=null;
        if(eObject.eContainer){
            res=eObject.eContainer;
        }
        else
        {        
            let oid=this._esDomain.rlookup(eObject);
            if(!oid) throw 'the supplied eObject is unknown to ecoreSync'
            let cmd=CMD.Get(QRY.Obj(oid).Met("PARENT"));
            res=await this._esDomain.remoteExec(cmd,true);         
        }       
        return res;
    }

    async getObjectShortPath(eObject)
    {
        //TODO: Update with new EOQ commands?
        var res='';
        let oid=this._esDomain.rlookup(eObject);
        if(!oid) throw 'the supplied eObject is unknown to ecoreSync'
    
        let cmd = new eoq2.Cmp().Get(new eoq2.Qry().Obj(oid).Met("ALLPARENTS"))
                                  .Get(new eoq2.Qry().His(-1).Pth("name"));
       
        let val=await this._esDomain.eoq2domain.Do(cmd)
        let pathSegments = [];
        for(let j=0;j<val[0].length;j++) {
            let segmentName = val[1][j];
            let segmentId = val[0][j].v;
            pathSegments.push(segmentName?segmentName:'#'+segmentId);
        }
        res = pathSegments.join('/')

        return res;    
    }

    async getObjectStringPath(eObject)
    {
        //TODO: Update with new EOQ commands?
        var res='';
        let oid=this._esDomain.rlookup(eObject);
        if(!oid) throw 'the supplied eObject is unknown to ecoreSync'

        if(oid!=0){           
            //return the path to the object
            let cmd = CMD.Cmp()
                .Get(QRY.Obj(oid).Met("INDEX"))
                .Get(QRY.Obj(oid).Met("CONTAININGFEATURE"))
                .Get(QRY.His(-1).Pth("name"))
                .Get(QRY.His(-2).Pth("upperBound"))
                .Get(QRY.Obj(oid).Met("ALLPARENTS").Idx([1,-1,1]))
                .Get(QRY.His(-1).Met("INDEX"))
                .Get(QRY.His(-2).Met("CONTAININGFEATURE"))
                .Get(QRY.His(-1).Pth("name"))
                .Get(QRY.His(-2).Pth("upperBound"))

            let val=await this._esDomain.eoq2domain.Do(cmd)
                var pathSegments = [];
                //do the container segments first
                var n = val[4].length;
                for(var i=0;i<n;i++){ 
                    var index = val[5][i];
                    var featureName = val[7][i];
                    var upperBound = val[8][i];
                    var segmentStr = featureName;
                    if(upperBound!=1) {
                        segmentStr += '.'+index;
                    }
                    pathSegments.push(segmentStr);
                }
                //the last segment need special care 
                {
                    var index = val[0];
                    var featureName = val[2];
                    var upperBound = val[3];
                    var segmentStr = featureName;
                    if(upperBound!=1) {
                        segmentStr += '.'+index;
                    }
                    pathSegments.push(segmentStr);
                }
                res = pathSegments.join('/');       
        }

        return res;   
    }

    async getAllContents(eObject,filter=null)
    {
        var self=this;
        var results=[];
        let oid=this._esDomain.rlookup(eObject);
        if(!oid){
            throw 'cannot get contents: the supplied eObject is unknown to this ecoreSync instance'
        }
        if(filter!=null){
            if(filter(eObject)){
                results.push(eObject);
            }
        }
        await this.isEClassInitialized(eObject.eClass)        
        var containments=eObject.eClass.get("eAllContainments");
        let cmd=new eoq2.Cmp();

        containments.forEach(function(cnt){
            cmd.Get(new eoq2.Obj(oid).Pth(cnt.get("name")));        
        })
        
        var res=await this._esDomain.exec(cmd);
        res.forEach(function(cnts){
            if(Array.isArray(cnts))
            {
                results=results.concat(cnts);
            }
            else
            {
                if(cnts)
                {
                    results.push(cnts);
                }
            }
        });
    
        var subContents=[];
        results.forEach(function(obj){
            if(obj)
            {
                subContents.push(self.getAllContents(obj));
            }
        })
        subContents=await Promise.all(subContents);
        subContents.forEach(function(sc){
            results=results.concat(sc);
        })
    
        if(filter==null)
        {
            return results;
        }
        else
        {
            return results.filter(filter);
        }
    }
    
    getObserverState(observerToken)
    {
        var res=[];
        if(this._esDomain.qryObservers.has(observerToken)){
            var observer=this._esDomain.qryObservers.get(observerToken);
            var state=observer.observerState;
            return {results:state.getResults(), deltaPlus: state.getDeltaPlus(), deltaMinus: state.getDeltaMinus()};
        }
        return res;
    }

    async decode(obj){
        var self=this;
        var res=null;
        if(Array.isArray(obj)){
            try{
                res=await awaitAll(obj.map(function(e){
                    return self.decode(e);
                }));
            }
            catch(e)
            {
                throw 'ecoreSync: Failed while decoding array '+e
            }
        }
        else
        {
            if(obj!=null)
            {
                if(obj.qry=="OBJ")
                {   try{
                        if(!Number.isInteger(obj.v)) throw 'ecoreSync: Invalid input format during decode: object id is invalid'
                            res=await this._esDomain.getObject(obj.v);     
                        }
                    catch(e){
                       throw ('ecoreSync: Failed to get object during decoding '+e);
                    }      
                }
                else
                {
                    res=obj;
                }        
            }
        }
        return res;
    }

    encode(obj){
        var self=this;
        if(Array.isArray(obj)){            
            return obj.map(function(e){
                return self.encode(e);
            });       
        }
        var res=null;
        if(obj!=null)
        {

            switch(obj.constructor.name)
            { 
                case "EObject":
                    let oid=this._esDomain.rlookup(obj);
                    if(oid==null) throw 'cannot encode: the supplied eObject of type '+obj.eClass.get('name')+' is unknown to this ecoreSync instance'
                    res={qry:"OBJ",v:oid}
                    break;
                default:
                    res=obj
                    break;
            }
        }   
        return res
    }


    async awaitAll(obj){
        // aux function to await all promises in an array structure
        var res=obj;
        if(Array.isArray(obj))
        {
            res=[];
            for(let i in obj)
            {
                res.push(awaitAll(obj[i]))
            }   
            res=await Promise.all(res);
        }
        else
        {
            res=await obj
        }
        return res;
    }
}

export default class EsUtils{

    initializer(){
        this.utils=new EsUtilities(this);
    }

}


