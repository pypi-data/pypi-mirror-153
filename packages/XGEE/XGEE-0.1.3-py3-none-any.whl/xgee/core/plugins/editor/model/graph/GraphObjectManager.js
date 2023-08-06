
export default class GraphObjectManager{
    constructor(graphModelFactory,ecoreSync,type,model,resourceProvider)
    {
        this.graphModelFactory=graphModelFactory
        this.ecoreSync=ecoreSync;
        this.type=type;
        this.model=model;
        this.resourceProvider=resourceProvider;
        this.subManagers=[];
        this.observers=new Map();       
    }

    async load(valueSet){  
        try{      
            var vSet=Object.assign({},valueSet);
            var query=this.type.query.build(vSet);    
            var cmd=new eoq2.Get(query);
            var results=await this.ecoreSync.exec(cmd,false)     
            var res=await this._postProcessResults(results);  
        }
        catch(e){
            throw(this.constructor.name+' failed to load:'+e)
        }
        return res;
    }
    
    async observe(valueSet,callback)
    {   
        var vSet=Object.assign({},valueSet);        
        var self=this;
        var query=this.type.query.build(vSet);
        var observerToken=await this.ecoreSync.observe(query,async function(results,deltaPlus,deltaMinus){ self._interceptObserverCallback(valueSet,callback,await self._postProcessResults(results),await self._postProcessResults(deltaPlus),await self._postProcessResults(deltaMinus)); });
     }

    
    mapObserver(graphObject,observerToken){
        let observerArr=[]
        if(!this.observers.has(graphObject.uuid))
        {            
            this.observers.set(graphObject.uuid,observerArr)           
        }
        else
        {
            observerArr=this.observers.get(graphObject.uuid)
        }

        observerArr.push(observerToken)        
    }

    async unobserve(graphObject){
        console.warn('Observer list')
        console.warn(this.observers);   
    }

    async _postProcessResults(results)
    {
        return results
    }

    async _interceptObserverCallback(valueSet,callback,results,deltaPlus,deltaMinus)
    {
        callback(results,deltaPlus,deltaMinus)
    }

    getTypeName()
    {
        return this.type.model.eClass.get("name")
    }
}