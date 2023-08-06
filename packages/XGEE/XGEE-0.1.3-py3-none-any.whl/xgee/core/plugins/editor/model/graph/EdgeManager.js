
import GraphObjectManager from './GraphObjectManager.js'
import AnchorManager from './AnchorManager.js'
import ContainerManager from './ContainerManager.js'

export default class EdgeManager extends GraphObjectManager{
    constructor(...args){
        super(...args)
    }
    async load(valueSet){

        var self=this;
        var results=await super.load(valueSet);
        var valueSets=await this.type.query.makeValueSets(valueSet,results.map(function(e){ return e.getEObject() }));

        var pendingVSets=valueSets.map(function(vSet){
            //for each loaded edge, apply the submanagers load routine
            let loadingSubManagers=[];
            self.subManagers.forEach(async function(manager){            
                    loadingSubManagers.push(manager.load(vSet));              
            });
            return Promise.all(loadingSubManagers)
        });

        try{
            var evaluatedVSets=await Promise.all(pendingVSets)     
        }
        catch(e){
            console.error('pending vSet evaluation: '+e);
        }
        
        if(evaluatedVSets)
        {
            evaluatedVSets.forEach(function(vSetEvaluation,resultIdx)
            {
                vSetEvaluation.forEach(function(managerResult,managerIdx){
                
                    for(let i in managerResult)
                    {
                        if(self.subManagers[managerIdx] instanceof AnchorManager)
                        {
                            results[resultIdx].addAnchor(managerResult[i]);                    
                        }

                        if(self.subManagers[managerIdx] instanceof ContainerManager)
                        {                                     
                            results[resultIdx].addContainer(managerResult[i]);                                                                     
                        }
                    }

                })
            })
        }

        return results;
    }

    async observe(valueSet,callback,container){

        var self=this; 

        var ObserverCallback=async function(results,addedEdges,removedEdges){       

         
            for(let i=0;i<addedEdges.length;i++)
            {
                let edge=addedEdges[i];
                container.addEdge(edge);       
                let vSet=await self.type.query.makeValueSets(valueSet,edge.getEObject())    
                
                
                self.subManagers.forEach(function(manager){                         
                    manager.observe(vSet,function(results){  },edge);
                });        
               
            }

            removedEdges.forEach(function(edge){                    
                if(edge.parent){  container.removeEdge(edge); }else{ console.warn('supplied edge was not found in model') }
            })    
                //maybe the graph can get out of sync with the observer and we have to synchronize the full results with the graph model ?                
            }  
        
        //start observing & get the current query results
        var vSet=Object.assign({},valueSet);        
        var query=this.type.query.build(vSet);

        var queryStr=this.type.query.build(vSet,true);
        try{
            var observerToken=await this.ecoreSync.observe(query,async function(results,deltaPlus,deltaMinus){             
                self._interceptObserverCallback(valueSet,function(results,deltaPlus,deltaMinus){ ObserverCallback(results,deltaPlus,deltaMinus); },await self._postProcessResults(results,container),await self._postProcessResults(deltaPlus,container),await self._postProcessResults(deltaMinus,container)); 
            })
        }
        catch(e)
        {
            console.error('failed to observe edges: '+e)
        }

        var results=await self._postProcessResults(this.ecoreSync.utils.getObserverState(observerToken).results,container);   

        var valueSets=await this.type.query.makeValueSets(valueSet,results.map(function(e){ return e.getEObject() }));
        valueSets.forEach(function(vSet,i){
            self.subManagers.forEach(function(manager){                              
                manager.observe(vSet,function(results,deltaPlus,deltaMinus){  },results[i]);
            });                   
        });  
        
    }

    async _interceptObserverCallback(valueSet,callback,results,deltaPlus,deltaMinus){

        var self=this;
        var valueSets=await this.type.query.makeValueSets(valueSet,deltaPlus.map(function(e){ return e.getEObject() }));

        var pendingVSets=valueSets.map(function(vSet){
            //for each loaded edge, apply the submanagers load routine
            let loadingSubManagers=[];
            self.subManagers.forEach(function(manager){
                loadingSubManagers.push(manager.load(vSet));         
            });
            return Promise.all(loadingSubManagers)
        });
        var evaluatedVSets=await Promise.all(pendingVSets)


        evaluatedVSets.forEach(function(vSetEvaluation,resultIdx)
        {
            vSetEvaluation.forEach(function(managerResult,managerIdx){
               
                for(let i in managerResult)
                {
                    if(self.subManagers[managerIdx] instanceof AnchorManager)
                    {
                        deltaPlus[resultIdx].addAnchor(managerResult[i]);
                    }

                    if(self.subManagers[managerIdx] instanceof ContainerManager)
                    {
                        deltaPlus[resultIdx].addContainer(managerResult[i]);         
                    }
                }

            })
        })

        callback(results,deltaPlus,deltaMinus); //feedthrough
    }

    /*
    async _postProcessResults(results){

        
        var self=this;
        return results.map(function(eObject){
            let edge=self.model.getEdgeByEObject(eObject) //dangerous, because eObjects could be in the graph multiple times (for whatever reason)
            if(!edge) edge=self.graphModelFactory.createEdge(self.model,self.type,eObject)
            return edge 
        })
    }*/

    async _postProcessResults(results,container=null){
        var self=this;
        if(!Array.isArray(results)) { results=[results] }
        if(!container) { 
            return results.map(function(eObject){  
                return self.graphModelFactory.createEdge(self.model,self.type,eObject);
            });
        }
        return results.map(function(eObject){    
            let edge=container.getEdgeByEObject(eObject)
            
            if(!edge) { 
                edge=self.graphModelFactory.createEdge(self.model,self.type,eObject) 
            }
            else{
                if(edge.type!=self.type){
                    edge=self.graphModelFactory.createEdge(self.model,self.type,eObject)
                }
            }
            return edge
        })
    }

}