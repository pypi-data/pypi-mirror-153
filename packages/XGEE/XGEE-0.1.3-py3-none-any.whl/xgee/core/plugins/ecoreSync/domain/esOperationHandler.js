class EsOperationHandler{
    constructor(esDomain){
        this.pendingOperations=new Map();
        this.esDomain=esDomain;
    }

    async run(opMeta,operation)
    {
        var self=this;
        var id=null;
        var res=null;

        switch(opMeta.name)
        {
            case "initEClass":
                id=opMeta.name+'/'+opMeta.args[0]+'/'+opMeta.args[1];
            break;
            case "initEPackage":
                id=opMeta.name+'/'+opMeta.args[0];
            break;
            case "initEENum":
                id=opMeta.name+'/'+opMeta.args[0];
            break;
            case "getObject":
                id=opMeta.name+'/'+opMeta.args[0];
            break;
            case "get":
                let oid=this.esDomain.rlookup(opMeta.args[0])
                id=opMeta.name+'/'+oid+'/'+opMeta.args[1];
            break;
            default:
                console.error('defaultOP: '+opMeta.name)
                console.error(opMeta);
            break;
        }

        if(id!=null){
            if(!this.pendingOperations.has(id)){
                this.pendingOperations.set(id,operation());
                this.pendingOperations.get(id).then(function(){
                    self.pendingOperations.delete(id);
                });
            }
            res=this.pendingOperations.get(id);
        }
        else
        {
            res=operation();
        }
        return res;
    }
}

export default class EsOperationHandling{

    initializer(){
        this.opHandler=new EsOperationHandler(this);
    }

}


