import GraphObjectController from './GraphObjectController.js'

export default class EdgeController extends GraphObjectController{
    constructor(ecoreSync,graphController) {  
        super(ecoreSync,graphController)      
        this.type=null;      
        this.edges=[];  
        this.containerControllers=[];  
        this.anchorControllers=[];
        this.queryTarget=null;
        this.queryTargetAlias=null;
        this.queryStr=null;
    }     

    async load(valueSet){
        var self=this
        var cmd = BuildGetCommand(valueSet,this.queryTarget,this.queryStr,this.queryTargetAlias)               
        var eObjects=await ecoreSync.exec(cmd)  
        var edges=eObjects.map(function(e){
            return graphModelFactory.createEdge(self.graphController.model,self.type,e)
        })

        for(let i=0;i<edges.length;i++)
        {
            let edgeValueSet=Object.assign({},valueSet);
            edgeValueSet["PARENT"]=edges[i].eObject
            edgeValueSet["ROOT"]=await ecoreSync.getObject(0)
            edgeValueSet["MODELROOT"]=await ecoreSync.utils.getModelRoot(edges[i].eObject);
            edgeValueSet["RESOURCE"]=await ecoreSync.utils.getResource(edges[i].eObject);

            if(this.queryTargetAlias!=null && this.queryTargetAlias!="")
            {
                edgeValueSet[this.queryTargetAlias]=edges[i].eObject
            }
            
            let containers=[];
            let anchors=[];
            self.containerControllers.forEach(function(e){             
                containers.push(e.load(copyValueSet(edgeValueSet))) 
            });

            self.anchorControllers.forEach(function(e){            
                anchors.push(e.load(copyValueSet(edgeValueSet))) 
            });
  
            containers= await Promise.all(containers)
            anchors= await Promise.all(anchors)

            containers.forEach(function(ccr){
                ccr.forEach(function(c){
                    edges[i].addContainer(c);
                })                
            })        
            
            anchors.forEach(function(acr){
                acr.forEach(function(a){
                    edges[i].addAnchor(a);
                })                
            })     

        }

        this.edges=edges;
        return this.edges   
    }

}
