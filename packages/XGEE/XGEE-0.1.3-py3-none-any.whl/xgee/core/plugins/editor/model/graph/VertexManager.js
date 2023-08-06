import GraphObjectManager from './GraphObjectManager.js'
import StaticVertexManager from './StaticVertexManager.js'
import EdgeManager from './EdgeManager.js'
import LabelManager from './LabelManager.js'

export default class VertexManager extends GraphObjectManager{
    constructor(...args){
        super(...args)
    }

    async load(valueSet){

        var self=this;
        var results=await super.load(valueSet);
        var valueSets=await this.type.query.makeValueSets(valueSet,results.map(function(e){ return e.getEObject() }));

        var pendingVSets=valueSets.map(function(vSet){
            //for each loaded vertex, apply the submanagers load routine
            let loadingSubManagers=[];
            self.subManagers.forEach(function(manager){
                loadingSubManagers.push(manager.load(vSet))
            });        
          
            return Promise.all(loadingSubManagers)
        });



        var evaluatedVSets=await Promise.all(pendingVSets)
      
        for(let resultIdx=0;resultIdx<evaluatedVSets.length;resultIdx++)
        {       
            let vSetEvaluation=evaluatedVSets[resultIdx]

            var transaction=await results[resultIdx].startTransaction()
            vSetEvaluation.forEach(function(managerResult,managerIdx){
               
                for(let i in managerResult)
                {
                    if(self.subManagers[managerIdx] instanceof VertexManager)
                    {
                        results[resultIdx].addVertex(managerResult[i]);
                    }

                    if(self.subManagers[managerIdx] instanceof StaticVertexManager)
                    {                
                        results[resultIdx].addVertex(managerResult[i]);                   
                    }

                    if(self.subManagers[managerIdx] instanceof EdgeManager)
                    {
                       results[resultIdx].addEdge(managerResult[i]);           
                    }

                    if(self.subManagers[managerIdx] instanceof LabelManager)
                    {
                        results[resultIdx].addLabel(managerResult[i]);           
                    }
                }

                results[resultIdx].endTransaction(transaction)

            })
        }




        return results;
    }

    async observe(valueSet,callback,container){
        var self=this; 
        if(!container) throw ' no container supplied '


            var ObserverCallback=async function(results,addedVertices,removedVertices){     

           
                for(let i=0;i<removedVertices.length;i++)
                {       
                    let vertex=removedVertices[i];

                        if(vertex){  
                            let vSet=await self.type.query.makeValueSets(valueSet,vertex.getEObject())
                            self.unobserve(vertex);
                            container.removeVertex(vertex); 
                        }
                        else
                        { 
                            console.error('removed vertex was not found in model') 
                        }                 
                    
                }  
               

                                    
                for(let i=0;i<addedVertices.length;i++)
                {
                    let vertex=addedVertices[i];
                    var tempPos=self.model.layout.getTemporaryVertexPosition(vertex.getEObjectId(),ecoreSync.rlookup(valueSet["PARENT"]));
                    if(tempPos) vertex.position={x:tempPos.x-vertex.size.x*0.5,y:tempPos.y-vertex.size.y*0.5};    
                    if(tempPos) self.model.layout.setVertexPosition(vertex,tempPos.x,tempPos.y);                  
          
                    container.addVertex(vertex);                               

                    let vSet=await self.type.query.makeValueSets(valueSet,vertex.getEObject())
             
                    //Initialize observance of sub managers
                    self.subManagers.forEach(function(manager)
                    {      
                      
                        if(manager instanceof VertexManager)
                        {                          
                            manager.observe(vSet,function(results){  },vertex);                           
                        }

                        if(manager instanceof StaticVertexManager)
                        {                          
                            manager.observe(vSet,function(results){  },vertex);                           
                        }

                        if(manager instanceof EdgeManager)
                        {                          
                            manager.observe(vSet,function(results){  },vertex);                          
                        }

                        if(manager instanceof LabelManager)
                        {
                           manager.observe(vSet,function(results){  },vertex);                       
                        }

                    });                                         
                        
                  
                } 

                

        }  
        
        //start observing all vertices & get the current query results
        var vSet=Object.assign({},valueSet);        
        var query=this.type.query.build(vSet);
        var observerToken=await this.ecoreSync.observe(query,async function(results,deltaPlus,deltaMinus){ 

            //Force unique results
            results=[...new Set(results)];
            deltaPlus=[...new Set(deltaPlus)];
            deltaMinus=[...new Set(deltaMinus)];       

                   
            self._interceptObserverCallback(valueSet,function(results,deltaPlus,deltaMinus){ ObserverCallback(results,deltaPlus,deltaMinus); },await self._postProcessResults(results,container),await self._postProcessResults(deltaPlus,container),await self._postProcessResults(deltaMinus,container)); 
          
        });
        

   
        this.observers.set(container,observerToken);

        var transaction=await container.startTransaction()
        var results=await self._postProcessResults(this.ecoreSync.utils.getObserverState(observerToken).results,container);   
        container.endTransaction(transaction)

        //All subitems
        var valueSets=await this.type.query.makeValueSets(valueSet,results.map(function(e){ return e.getEObject() }));
        valueSets.forEach(function(valueSet,i){

            //Initialize label observance           
            self.subManagers.filter(function(manager){ return (manager instanceof LabelManager) }).forEach(function(manager){    
                manager.observe(valueSet,function(){ },results[i]);             
            });   
          
            //Initialize vertex manager observance
            self.subManagers.filter(function(manager){ return (manager instanceof VertexManager) }).forEach(function(manager){               
                    manager.observe(valueSet,function(){  },results[i]);                     
            });  
            
            //Initialize static vertex manager observance
            self.subManagers.filter(function(manager){ return (manager instanceof StaticVertexManager) }).forEach(function(manager){               
                    manager.observe(valueSet,function(){  },results[i]);                     
            });     
            
            //Initialize edge manager observance
            self.subManagers.filter(function(manager){ return (manager instanceof EdgeManager) }).forEach(function(manager){               
                manager.observe(valueSet,function(){ console.error('Edge ') },results[i]);                     
            });    
   
        });
        
              
    }

    unobserve(vertex)
    {

        //unobserves this vertex and all nested graph objects        
        var self=this;
        if(this.observers.has(vertex))
        {
            ecoreSync.unobserve(this.observers.get(vertex));
            this.observers.delete(vertex);
        }

        this.subManagers.forEach(function(manager)
        {  
                                    
            if(manager instanceof LabelManager)
            {
                vertex.labels.forEach(function(label){
                    manager.unobserve(label);          
                });
            }

            if(manager instanceof VertexManager)
            {
                vertex.vertices.forEach(function(vertex){
                    manager.unobserve(vertex);          
                });
            }

            if(manager instanceof EdgeManager)
            {
                vertex.edges.forEach(function(edge){
                    manager.unobserve(edge);          
                });
            }
          
        });
    }

    async _interceptObserverCallback(valueSet,callback,results,deltaPlus,deltaMinus){    

        //execute submanagers load functions for the newly added vertices (deltaPlus)
        
        var self=this;
        var valueSets=await this.type.query.makeValueSets(valueSet,deltaPlus.map(function(e){ return e.getEObject() }));


        var pendingVSets=valueSets.map(function(vSet){
            //for each loaded vertex, apply the submanagers load routine
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
                    if(self.subManagers[managerIdx] instanceof VertexManager)
                    {
                        if(!deltaPlus[resultIdx].containsVertex(managerResult[i])){
                            deltaPlus[resultIdx].addVertex(managerResult[i]);
                        }
                    }

                    if(self.subManagers[managerIdx] instanceof StaticVertexManager)
                    {                
                        deltaPlus[resultIdx].addVertex(managerResult[i]);                   
                    }

                    if(self.subManagers[managerIdx] instanceof EdgeManager)
                    {
                        if(!deltaPlus[resultIdx].containsEdge(managerResult[i])){
                            deltaPlus[resultIdx].addEdge(managerResult[i]);       
                        }    
                    }

                    if(self.subManagers[managerIdx] instanceof LabelManager)
                    {                       
                        if(!deltaPlus[resultIdx].hasLabel(managerResult[i])){
                            deltaPlus[resultIdx].addLabel(managerResult[i]);      
                        }                          
                    }
                }

            })
        })
        
        callback(results,deltaPlus,deltaMinus);        
    }

    async _postProcessResults(results,container=null){
        var self=this;
        if(!Array.isArray(results)) { results=[results] }
        if(!container) { 
            return results.map(function(eObject){  
                return self.graphModelFactory.createVertex(self.model,self.type,eObject);
            });
        }

        return results.map(function(eObject){    
            let vertex=container.getVertexByEObject(eObject)
            if(!vertex) { 
                vertex=self.graphModelFactory.createVertex(self.model,self.type,eObject) 
            }
            else{
                if(vertex.type!=self.type){
                    vertex=self.graphModelFactory.createVertex(self.model,self.type,eObject)
                }
            }
            return vertex
        })
    }
}