import GraphObjectManager from './GraphObjectManager.js'


export default class AnchorManager extends GraphObjectManager{
    constructor(...args){
        super(...args)
    }


    async observe(valueSet,callback,edge){
        
        var ObserverCallback=function(all,deltaPlus,deltaMinus){       

            if(!Array.isArray(all)){ all=[all] }
            if(!Array.isArray(deltaPlus)){ deltaPlus=[deltaPlus] }
            if(!Array.isArray(deltaMinus)){ deltaMinus=[deltaMinus] }

            deltaMinus.forEach(function(anchor){
                edge.removeAnchor(anchor);
            })
            deltaPlus.forEach(function(anchor){
                edge.addAnchor(anchor);
            })
            callback(all,deltaPlus,deltaMinus);
        };

        var vSet=Object.assign({},valueSet);        
        var self=this;
        var query=this.type.query.build(vSet);

        var queryStr=this.type.query.build(vSet,true);
        if(!window["AM_QUERIES"])
        {
            window["AM_QUERIES"]=[]
        }

        window["AM_QUERIES"].push(query);
        
        try{
            var observerToken=this.ecoreSync._esDomain.observe(query,async function(results,deltaPlus,deltaMinus){ self._interceptObserverCallback(valueSet,ObserverCallback,await self._postProcessResults(results,edge),await self._postProcessResults(deltaPlus,edge),await self._postProcessResults(deltaMinus,edge)); })
        }
        catch(e){
            console.error('AnchorManager failed to observe anchors: '+e)
        }
    }

    async _postProcessResults(results,edge=null){
        try{
            var self=this;
            if(Array.isArray(results)){ 
                return results.filter(function(r){ return r!=null }).map(function(result){
                    let anchor=null;
                    if(edge) anchor=edge.getAnchorByEObject(result)
                    if(!anchor)
                    {
                        anchor=self.graphModelFactory.createAnchor(self.model,self.type,result);
                    }
                    else
                    {
                        if(anchor.type!=self.type){
                            anchor=self.graphModelFactory.createAnchor(self.model,self.type,result);
                        }
                    }
                    return anchor;
                })
            }
            else
            {
                if(results)
                {
                    let anchor=null;
                    if(edge) anchor=edge.getAnchorByEObject(results) 
                    if(!anchor)
                    {
                        anchor=[self.graphModelFactory.createAnchor(self.model,self.type,results)]
                    }
                    else
                    {
                        if(anchor.type!=self.type){
                            anchor=self.graphModelFactory.createAnchor(self.model,self.type,result);
                        }
                    }
                    return anchor
                }
                else
                {
                    return [];
                }
            }        
            
        }
        catch(e){
            console.error('failed to post process anchor results: '+e);
        }
    }
}