import Query from '../../queries/Query.js'
import GraphObjectManager from './GraphObjectManager.js'


export default class LabelSegmentManager extends GraphObjectManager{
    constructor(...args){
        super(...args)
        this.observerIds=new Map();
    }

    async load(valueSet){

        var self=this;
        var vSet=Object.assign({},valueSet); //make copy of valueSet
        var labelSegmentQuery=async function(queryDefinition){

            let isConditional=queryDefinition.get('isConditional')
            let condition=queryDefinition.get('condition')
            let conditionQry=new Query(self.ecoreSync,queryDefinition.get("alias"),condition,queryDefinition.get("queryTarget"),queryDefinition.get("queryTargetAlias"));
            let defaultValue=queryDefinition.get('defaultValue')

            let prefix=queryDefinition.get('prefix')
            if(prefix==null) prefix=''
            let suffix=queryDefinition.get('suffix')
            if(suffix==null) suffix=''

            let cmd=new eoq2.Cmp()

            let res=defaultValue;
            if(res==null) res=''
         
            let qryStr=queryDefinition.get('queryStr')

            if(isConditional)
            {           
                cmd.Get(conditionQry.build(vSet))     
                qryStr="@(IF,("+condition+"),("+qryStr+"),())"   
                // qryStr="Met('IF',[QRY."+condition+", QRY."+qryStr+", new eoq2.Qry(null)])"
                
            }
          
            let qry=new Query(self.ecoreSync,queryDefinition.get("alias"),qryStr,queryDefinition.get("queryTarget"),queryDefinition.get("queryTargetAlias"));
            cmd.Get(qry.build(vSet))         
          
            try{
                let queryRes=await self.ecoreSync.exec(cmd)
                if(isConditional)
                {
                    if(queryRes[0])
                    {
                        res=prefix+queryRes[1]+suffix
                    }                           
                }
                else
                {
                    res=queryRes[0]
                }       
            }
            catch(e)
            {
                console.warn('default value used due to query failure')
                console.warn(cmd);
            }
            
            return res
        }

        var segmentQueries=this.type.model.get("queries").array().map(function(queryDefinition){            
            let QueryObj=new Query(self.ecoreSync,queryDefinition.get("alias"),queryDefinition.get("queryStr"),queryDefinition.get("queryTarget"),queryDefinition.get("queryTargetAlias"))          
            return {query:QueryObj,queryResults:labelSegmentQuery(queryDefinition)}
        })



        //wait until all segments have finished loading
        await Promise.all(segmentQueries.map(function(e){ return e.queryResults}))
        
        //update valueSet
        for(let i in segmentQueries)
        {              
            if(segmentQueries[i].query.hasAlias())
            {
                vSet[segmentQueries[i].query.getAlias()]=await segmentQueries[i].queryResults
            }    
        }
        
     

        var labelSegment=self.graphModelFactory.createLabelSegment(this.type);
        labelSegment.updateValueSet(vSet,true);

        return labelSegment;
    }

    async observe(valueSet,labelSegment){
        var self=this;
        var labelObservers=[];
        if(labelSegment.type != this.type ){ 
            throw 'cannot observe label segment of different type'
        }

        this.type.model.get("queries").array().forEach(function(queryDefinition){      

            let conditionQryStr=queryDefinition.get("condition") 
            let qryStr=queryDefinition.get("queryStr")    
            let obsvQryStr=new eoq2.Qry('')    
            if(queryDefinition.get('isConditional'))
            {
                obsvQryStr="@(IF,("+conditionQryStr+"),("+qryStr+"),%)"
            }
            else
            {
                obsvQryStr=qryStr;
            }                  
            let obsvQry=new Query(self.ecoreSync, queryDefinition.get("alias"),obsvQryStr,queryDefinition.get("queryTarget"),queryDefinition.get("queryTargetAlias"));     

            labelObservers.push(self.ecoreSync.observe(obsvQry.build(valueSet),async function(results,deltaPlus,deltaMinus){ 
                let res=queryDefinition.get('defaultValue')
                let prefix=queryDefinition.get('prefix')
                if(prefix==null) prefix=''
                let suffix=queryDefinition.get('suffix')
                if(suffix==null) suffix=''
                if(results!=null) res=prefix+results+suffix
    
                let vSet={};
                if(queryDefinition.get('alias')!=null)
                {
                    vSet[queryDefinition.get('alias')]=res;
                    labelSegment.updateValueSet(vSet);
                }
            }));

        
        })

        Promise.all(labelObservers).then(function(obsvIds){
            self.observerIds.set(labelSegment,obsvIds);
        })
        return true
    }

    async unobserve(labelSegment)
    {        
        var self=this;
        if(this.observerIds.has(labelSegment)){
            let observerIds=this.observerIds.get(labelSegment);
            observerIds.forEach(function(obsvId){
                self.ecoreSync.unobserve(obsvId);
            })
        }
        return true      
    }

}