import GraphObjectManager from './GraphObjectManager.js'
import VertexManager from './VertexManager.js'

export default class ContainerManager extends GraphObjectManager{
    constructor(...args){
        super(...args)     
    }

    async load(valueSet){    
      
       var self=this;  
       var container=null;
       if(valueSet["PARENT"])
       {     
        container=this.model.getContainerByEObject(valueSet["PARENT"]);       
        if(!container) container=self.graphModelFactory.createContainer(this.model,this.type,valueSet["PARENT"]);       
       }  
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
                    container.addVertex(managerResult[i]);                    
                }
            }
        });       


       return [container]
    }

    async observe(valueSet,callback){     

        var self=this;
        var container=null;  
        if(valueSet["PARENT"])
        {     
            container=this.model.getContainerByEObject(valueSet["PARENT"]);                  
        }  
        if(container)
        {                            
            self.subManagers.filter(function(manager){ return manager instanceof VertexManager }).forEach(function(manager){ 
                manager.observe(valueSet,function(){ console.error('container resident changed!!!') },container);                              
            }); 
        }
        else
        {
            $.notify("CONTAINER ERROR")
        }
    }    

}