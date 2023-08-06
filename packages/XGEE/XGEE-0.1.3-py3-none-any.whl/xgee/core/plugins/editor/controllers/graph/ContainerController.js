import GraphObjectController from './GraphObjectController.js'

export default class ContainerController extends GraphObjectController{
    constructor(ecoreSync,graphController) {  
        super(ecoreSync,graphController)
        this.type=null; 
        this.containers=[];
        this.vertexControllers=[];       
    }   
   
    async load(valueSet)
    {
        var self=this
        var container=graphModelFactory.createContainer(self.graphController.model,self.type,valueSet["PARENT"]);
        var containers=[container];

        var vertices=[];
        this.vertexControllers.forEach(function(e){
            vertices.push(e.load(copyValueSet(valueSet)))
        })

        vertices= await Promise.all(vertices)

        vertices.forEach(function(vcr){
            vcr.forEach(function(v){
                container.addVertex(v);
            })                    
        })
     
        this.containers=containers;
        return containers;
    }
  
}