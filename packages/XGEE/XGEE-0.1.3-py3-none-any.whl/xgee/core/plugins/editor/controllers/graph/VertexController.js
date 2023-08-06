import GraphObjectController from './GraphObjectController.js'

export default class VertexController extends GraphObjectController{
    constructor(ecoreSync,graphController) { 
        super(ecoreSync,graphController)
        this.type=null;
        this.vertices=[];
        this.vertexControllers=[];
        this.edgeControllers=[];
        this.labelControllers=[];
        this.queryTarget=null;
        this.queryTargetAlias=null;
        this.queryStr=null;
        this.alias=null; 
    }   

    async observe(valueSet){
        var self=this;
        var query=BuildQuery(valueSet,this.queryTarget,this.queryStr,this.queryTargetAlias)   
        var reactToChanges=async function(results){ 
            $.notify("CHANGES DETECTED") 

            var currentEObjects=self.vertices.map(function(v){ return v.getEObject() })
            var addedEObjects=results.filter(function(resultObject){
                var match=currentEObjects.find(function(currentObject){
                    return compareEObjects(resultObject,currentObject)
                })
                if(match){ return false }else{ return true }
               
            });

            var removedEObjects=currentEObjects.filter(function(currentObject){
                var match=results.find(function(resultObject){
                    return compareEObjects(resultObject,currentObject)
                })
                if(match){ return false }else{ return true }              
            });

            console.error(addedEObjects)
            console.error(removedEObjects)


            removedEObjects.forEach(function(removedObject){
                var vertex=self.vertices.find(function(v){   return compareEObjects(removedObject,v.getEObject())  });
                if(vertex && vertex.parent){ vertex.parent.removeVertex(vertex) }            
            })
            var vertices=addedEObjects.map(function(e){
                return graphModelFactory.createVertex(self.graphController.model,self.type,e)
            })
            await self.initVertices(vertices);

            vertices.forEach(function(v){
                vertices.push(v);
            })

            //where to add the vertices?
    
            
        };

        ecoreSync.observe(query,reactToChanges)
    }

    async initVertices(vertices)
    {
        var self=this;
        for(let i=0;i<vertices.length;i++)
        {   

            //Sub vertices
            let vertexValueSet=new Object();
            vertexValueSet["PARENT"]=vertices[i].eObject
            vertexValueSet["ROOT"]=await ecoreSync.getObject(0)
            vertexValueSet["MODELROOT"]=await ecoreSync.utils.getModelRoot(vertices[i].eObject);
            vertexValueSet["RESOURCE"]=await ecoreSync.utils.getResource(vertices[i].eObject)
            
            if(this.alias!=null && this.alias!="")
            {
                vertexValueSet[this.alias]=vertices[i].eObject    
            }
         
            let subVertices=[];
            let subEdges=[];
            self.vertexControllers.forEach(function(e){           
                    subVertices.push(e.load(copyValueSet(vertexValueSet)))           
            });
            
            self.edgeControllers.forEach(function(e){
                subEdges.push(e.load(copyValueSet(vertexValueSet))) 
            });

            subVertices= await Promise.all(subVertices)
            subEdges= await Promise.all(subEdges)

            subVertices.forEach(function(vcr){
                vcr.forEach(function(v){
                    vertices[i].addVertex(v);
                })                
            })

            subEdges.forEach(function(ecr){
                ecr.forEach(function(e){
                    vertices[i].addEdge(e);
                })
            })     
            
            vertices[i].on('RESIZE',function(){
                self.graphController.layout.setVertexSize(vertices[i],vertices[i].size.x,vertices[i].size.y)
            });

            vertices[i].on('MOVE',function(){
                self.graphController.layout.setVertexPosition(vertices[i],vertices[i].position.x,vertices[i].position.y)
            });         

            
            let labels=[];
            self.labelControllers.forEach(function(e){
                labels.push(e.load(copyValueSet(vertexValueSet)))                 
            });
            labels=await Promise.all(labels);
            labels.forEach(function(lbl){
                vertices[i].addLabel(lbl);
            })
            
        }
    }
    async load(valueSet){
        var self=this
        var cmd = BuildGetCommand(valueSet,this.queryTarget,this.queryStr,this.queryTargetAlias)               
        var eObjects=await ecoreSync.exec(cmd)        
        if(!Array.isArray(eObjects)) { console.trace(); console.error(this.type); console.error(valueSet);}
        if(!Array.isArray(eObjects)) throw 'Vertex queryStr='+this.queryStr+' failed with queryTarget='+this.queryTarget+' #'+ecoreSync.rlookup(valueSet["PARENT"])
        var vertices=eObjects.map(function(e){
            return graphModelFactory.createVertex(self.graphController.model,self.type,e)
        })
        await this.initVertices(vertices);     
        this.vertices=vertices;        
        this.observe(valueSet);
        return this.vertices   
    }    

}