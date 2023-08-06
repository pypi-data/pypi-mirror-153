import GraphObjectManager from './GraphObjectManager.js'
import VertexManager from './VertexManager.js'
import LabelManager from './LabelManager.js'

export default class StaticVertexManager extends GraphObjectManager{
    constructor(...args){
        super(...args)        
    }

    async load(valueSet){    
      
       var self=this;  
       let results=[]
       var staticVertex=null;
       if(valueSet["PARENT"])
       {     
        let staticVertices=this.model.getByEObject(valueSet["PARENT"],this.type)  
        staticVertex=staticVertices.length?staticVertices[0]:null

        if(this.type.isConditional)
        {
            var vSet=Object.assign({},valueSet);
            var conditionQry=this.type.condition.build(vSet);
            var condition=await this.ecoreSync.exec(new eoq2.Get(conditionQry))
            if(!condition)
            {
                staticVertex=null
            }
            else
            {
                staticVertex=self.graphModelFactory.createStaticVertex(this.model,this.type,valueSet["PARENT"]);
            }
        }
        else
        {
            if(!staticVertex) staticVertex=self.graphModelFactory.createStaticVertex(this.model,this.type,valueSet["PARENT"]);       
        }
       }  

       if(staticVertex)
       {
            let loadingSubManagers=[];

            this.subManagers.forEach(function(manager){
                loadingSubManagers.push(manager.load(valueSet));      
            });

            var vSetEvaluation=await Promise.all(loadingSubManagers)   

            vSetEvaluation.forEach(function(managerResult,managerIdx){
                
                for(let i in managerResult)
                {
                    if(self.subManagers[managerIdx] instanceof VertexManager)
                    {
                        staticVertex.addVertex(managerResult[i]);                    
                    }

                    if(self.subManagers[managerIdx] instanceof StaticVertexManager)
                    {                
                        staticVertex.addVertex(managerResult[i]);                   
                    }

                    if(self.subManagers[managerIdx] instanceof LabelManager)
                    {
                        if(!staticVertex.hasLabel(managerResult[i])){
                            staticVertex.addLabel(managerResult[i]);      
                        }     
                    }
                }
            });   
            results=[staticVertex]    
        }
 
       return results
    }
    
    async observe(valueSet,callback,container){
        var self=this
        var staticVertex=null;
        if(valueSet["PARENT"])
        {     
            let staticVertices=this.model.getByEObject(valueSet["PARENT"],this.type)  
            staticVertex=staticVertices.length?staticVertices[0]:null
        }

        if(staticVertex)
        {                    
            //Initialize observance for the already present static vertex

            //Initialize label observance           
            this.subManagers.filter(function(manager){ return (manager instanceof LabelManager) }).forEach(function(manager){    
            manager.observe(valueSet,function(){ },staticVertex);             
            });   
        
            //Initialize vertex manager observance
            this.subManagers.filter(function(manager){ return (manager instanceof VertexManager) }).forEach(function(manager){               
                    manager.observe(valueSet,function(){  },staticVertex);                     
            });  
            
            //Initialize static vertex manager observance
            this.subManagers.filter(function(manager){ return (manager instanceof StaticVertexManager) }).forEach(function(manager){               
                    manager.observe(valueSet,function(){  },staticVertex);                     
            });          
            
        }
        
        if(this.type.isConditional)
        {
            var vSet=Object.assign({},valueSet);
            var conditionQry=this.type.condition.build(vSet);
            var observerToken=await this.ecoreSync.observe(conditionQry, async (condition)=>{
                let results=[]
                
                if(condition)
                {                       
                    if(!staticVertex){          
                        staticVertex=self.graphModelFactory.createStaticVertex(this.model,this.type,valueSet["PARENT"]);                  
                     
                        let loadingSubManagers=[] 
                        self.subManagers.forEach(function(manager){
                            loadingSubManagers.push(manager.load(valueSet));      
                        });

                        var vSetEvaluation=await Promise.all(loadingSubManagers)   
                        var transaction=await staticVertex.startTransaction()                    
                        vSetEvaluation.forEach(function(managerResult,managerIdx){              
                        
                            for(let i in managerResult)
                            {
                                if(self.subManagers[managerIdx] instanceof VertexManager)
                                {
                                    staticVertex.addVertex(managerResult[i]);
                                }
            
                                if(self.subManagers[managerIdx] instanceof StaticVertexManager)
                                {                
                                    staticVertex.addVertex(managerResult[i]);                   
                                }
            
                                if(self.subManagers[managerIdx] instanceof LabelManager)
                                {                                   
                                    staticVertex.addLabel(managerResult[i]);                                         
                                }
                            }      
                        })
                        staticVertex.endTransaction(transaction)                       
            
                        //Initialize observance for the static vertex created during this observer event
                        
                        //Initialize label observance           
                        self.subManagers.filter(function(manager){ return (manager instanceof LabelManager) }).forEach(function(manager){    
                            manager.observe(valueSet,function(){ },staticVertex);             
                        });   
                    
                        //Initialize vertex manager observance
                        self.subManagers.filter(function(manager){ return (manager instanceof VertexManager) }).forEach(function(manager){               
                                manager.observe(valueSet,function(){  },staticVertex);                     
                        });  
                        
                        //Initialize static vertex manager observance
                        self.subManagers.filter(function(manager){ return (manager instanceof StaticVertexManager) }).forEach(function(manager){               
                                manager.observe(valueSet,function(){  },staticVertex);                     
                        });  
                
                        
                    }            
                                        
                    container.addVertex(staticVertex)        
                }
                else
                {
                    if(staticVertex)
                    {
                        container.removeVertex(staticVertex)                  
                    }
              
                }
                
            })

        }
       


    }



}