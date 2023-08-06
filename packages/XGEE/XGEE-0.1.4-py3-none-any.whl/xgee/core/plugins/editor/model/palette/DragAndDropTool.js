
import GraphTool from './GraphTool.js'

export default class DragAndDropTool extends GraphTool{
    constructor(...args){
        super(...args)
        this.dropItem=null;
        this.template=null;
    }

    async init(){   
        if(!this.toolDefinition) { throw 'tool initialization failed, because no definition was provided' }
        let template=await this.initTemplate()
        if(template)
        {
            this.dropItem=ecoreSync.clone(this.template)
        }
    }

    getTargetedGraph = function(evt)
    {

        var x = mxEvent.getClientX(evt);
        var y = mxEvent.getClientY(evt);
        var elt = document.elementFromPoint(x, y);
   
        if (mxUtils.isAncestorNode($app.viewManager.activeView.domElement, elt))
        {					
            return $app.viewManager.activeView.XGEEInstance.getGraph()
        }

        return null;
    }; 

    initUI(elementId){
        var self=this;
        var element=document.getElementById(elementId)
        var ds=mxUtils.makeDraggable(element, self.getTargetedGraph, function(...args){
            self.drop(...args)
        }, null, 0,0,false,false,true,(graph,x,y) => {
            if(graph.graphView)
            {
                let originalCoordinate=graph.graphView.viewPort.toOriginalCoordinate({x:x,y:y})
                x=originalCoordinate.x
                y=originalCoordinate.y
            }

            return graph.getCellAt(x,y)
        }); 
        
        //could include a better preview here

        ds.isGuidesEnabled = function()
        {
            //return graph.graphHandler.guidesEnabled;
            return true;
        };
        ds.createDragElement = mxDragSource.prototype.createDragElement;

        $("#"+elementId).mousedown(function(){
            self.palette.controller.deactivateCurrent();
        });          
    }

    async getDropItem(){
        let dropItem=this.dropItem
        this.dropItem=ecoreSync.clone(this.template)
        return await dropItem
    }

    async drop(graph,evt,target,x,y){    
        if(graph.graphView)
        {
            //use the drop function of the graphController, that will handle the action depending on the available dropReceivers
            let dropItem=await this.getDropItem();     
            let dropTarget=null;    
            if(target){ dropTarget=target.value.getEObject() } 
            let dropLocation=graph.graphView.viewPort.toOriginalCoordinate({x:x,y:y})
            graph.graphView.graphController.drop(dropTarget,dropLocation,dropItem)
        }
        else
        {        
            throw 'incompatible graph used for drag&drop'
        }        
    }
}