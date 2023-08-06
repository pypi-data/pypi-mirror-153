export default class QueryController{
    constructor(queryTarget,queryTargetAlias,queryStr,alias){
        this.queryTarget=queryTarget;
        this.queryTargetAlias=queryTargetAlias;
        this.queryStr=queryStr;
        this.alias=alias;
        this.queryControllers=[];
    }

    async exec(valueSet)
    {
        var cmd = BuildGetCommand(valueSet,this.queryTarget,this.queryStr,this.queryTargetAlias)     
        var results=await ecoreSync.exec(cmd);
        valueSet[this.alias]=results;
        var subQueryResults=[];
        if(this.queryControllers.length)
        {
            this.queryControllers.forEach(function(qc){
                subQueryResults.push(qc.exec(valueSet))
            })           
        }
        var subQueryResults=await Promise.all(subQueryResults)     
        subQueryResults.forEach(function(e){
            return mergeValueSets(valueSet,e,["PARENT","ROOT","MODELROOT","RESOURCE"])
        })

        return valueSet
    }
}
