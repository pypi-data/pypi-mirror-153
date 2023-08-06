import GraphObjectController from './GraphObjectController.js'

export default class AnchorController extends GraphObjectController{
    constructor(ecoreSync,graphController) {  
        super(ecoreSync,graphController)
        this.type=null; 
        this.anchors=[];
        this.queryTarget=null;
        this.queryTargetAlias=null;
        this.queryStr=null;   
    }   
   
    async load(valueSet)
    {
        var self=this
        var cmd = BuildGetCommand(valueSet,this.queryTarget,this.queryStr,this.queryTargetAlias)               
        var eObjects=await ecoreSync.exec(cmd)  
        //TODO: Force Queries to return arrays and get rid of the following
        if(!Array.isArray(eObjects)){
            eObjects=[eObjects]
        }
        var anchors=eObjects.map(function(e){
            return graphModelFactory.createAnchor(self.graphController.model,self.type,e)
        })
        this.anchors=anchors;
        return this.anchors   
    }
  
}