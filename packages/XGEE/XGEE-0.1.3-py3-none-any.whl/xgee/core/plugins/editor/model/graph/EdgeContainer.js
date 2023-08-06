
import GraphEvent from './GraphEvent.js'

export default class EdgeContainer{
    initializer(){
        this.edges=[];        
        if(!this.events)
        {
            this.events={};           
        }        
        this.events["EDGE_ADDED"]=new GraphEvent(true);
        this.events["EDGE_REMOVED"]=new GraphEvent(true);
        this.events["EDGE_ANCHORS_CHANGED"]=new GraphEvent(true);
    }
    
    containsEdge(edge){
        var idx=this.edges.indexOf(edge);
        if(idx > -1){ return true } else { return false }       
    }

    addEdge(edge)
    {
        this.edges.push(edge);
        edge.parent=this;        
        this.events["EDGE_ADDED"].raise(edge);  
    }

    removeEdge(edge)
    {
        edge.parent=null
        let idx=this.edges.indexOf(edge);
        if(idx > -1)
        {
            this.edges.splice(idx, 1);
        }          
        this.events["EDGE_REMOVED"].raise(edge);   
    }

    getEdgeByObjectId(objectId){
        var self=this;
        return this.edges.find(function(e){
            return e.getEObjectId()==objectId
        });
    }

    getEdgeByEObject(eObject){
        var self=this;
        return this.edges.find(function(e){
            return e.getEObject()==eObject
        });
    }

}