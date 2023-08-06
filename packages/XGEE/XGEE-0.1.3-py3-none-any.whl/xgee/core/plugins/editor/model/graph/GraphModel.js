
import VertexContainer from './VertexContainer.js'
import EdgeContainer from './EdgeContainer.js'
import EObjectOwner from './EObjectOwner.js'
import Vertex from './Vertex.js'
import Container from './Container.js'
import GraphEvent from './GraphEvent.js'
import { multipleClasses }  from '../../lib/libaux.js'
import TransactionObject from './TransactionObject.js'

export default class GraphModel extends multipleClasses(EObjectOwner,VertexContainer,EdgeContainer,TransactionObject){
    constructor(){
        super();
        this.layout=null;
        this._index=new Map();
        this.manager=null;
        this.events["OBJECT_INVALID"]=new GraphEvent(false);
        this.events["LAYOUT_INVALID"]=new GraphEvent(false);
    }
    
    async init(){

        var self=this
        await this.layout.init();
        this.layout.on('CACHE_BUILT',function(){
            self.events["LAYOUT_INVALID"].raise()
        })

        let valueSet=new Object();

        //XGEE built-in aliases
        valueSet["ROOT"]=await ecoreSync.getObject(0) // workspace root
        valueSet["MODELROOT"]=await ecoreSync.utils.getModelRoot(this.eObject) // the root of the model
        valueSet["EDITORROOT"]=this.eObject // the editor root element  
        valueSet["PARENT"]=this.eObject // the parent element      
        valueSet["RESOURCE"]=await ecoreSync.utils.getResource(this.eObject) // the model resource

        await this.manager.load(valueSet);  // load initial model data
        await this.manager.initObservers(valueSet) //initialize observers

        this.events["VERTEX_ADDED"].enable();
        this.events["VERTEX_REMOVED"].enable();
        this.events["EDGE_ADDED"].enable();
        this.events["EDGE_REMOVED"].enable();
        this.events["OBJECT_INVALID"].enable();
        this.events["LAYOUT_INVALID"].enable();
        
        this.initialized=true;
    }

    addVertex(vertex){   
        this.addToIndex(vertex);      
        super.addVertex(vertex); 
    }

    removeVertex(vertex)
    {      
        super.removeVertex(vertex);   
        this.removeFromIndex(vertex);
    }

    addEdge(edge){ 
        this.addToIndex(edge);  
        super.addEdge(edge);
    }

    removeEdge(edge)
    {            
        super.removeEdge(edge); 
        this.removeFromIndex(edge);
    }

    addToIndex(item)
    {
        if(this._index.has(item.uuid))
        {
            throw 'UUID='+item.uuid+' is already in use. The conflicting vertex must be removed from the index first.'
        }
        this._index.set(item.uuid,item)
    }

    removeFromIndex(item){
        if(this._index.has(item.uuid))
        {
            if(this._index.delete(item.uuid))
            {
                console.info('removed uuid='+item.uuid+' from index');
            }
            else
            {
                throw 'could not remove uuid='+item.uuid+' from index';
            }
        }
    }

    getIndex()
    {
        return new Map(this._index);
    }

    getByUUID(uuid){
        return this._index.get(uuid)
    }

    getByObjectId(objectId)
    {
        let indexObjects=[];

        /*
        if(ecoreSync.rlookup(this.eObject)==objectId)
        {
            return [this];
        }
        */

        for (const [uuid, item] of this._index){
            if(item.eObject)
            {
                if(ecoreSync.rlookup(item.eObject)==objectId)
                {
                    indexObjects.push(this._index.get(uuid));
                }
            }
        }
        return indexObjects;
    }

    getByEObject(eObject,type=null)
    {
        let res=[]
        if(eObject==null || Array.isArray(eObject))
        {
            console.error(eObject);
            console.trace();
            console.error('argument must be a valid eObject')
            return null
        }

        res=this.getByObjectId(ecoreSync.rlookup(eObject))

        if(type)
        {
           res=res.filter(graphObject => {
               let res=false
               if(graphObject.type && graphObject.type==type)
               {
                    res=true
               }
               return res
           }) 
        }
    
        return res
    }

    getVertexByEObject(eObject){
        var items=this.getByEObject(eObject);
        if(items)
        {
            var vertices=items.filter(function(e){
                if(e instanceof Vertex){
                    return true
                }
                return false;
            })
            if(vertices.length>1) { console.warn('ambigous solution, returning first vertex match')}
            if(vertices.length>0) { return vertices[0] }
        }
    }

    getVertexByObjectId(objectId){
        var items=this.getByObjectId(objectId);
        if(items)
        {
            var vertices=items.filter(function(e){
                if(e instanceof Vertex){
                    return true
                }
                return false;
            })
            if(vertices.length>1) { console.warn('ambigous solution, returning first vertex match')}     
            if(vertices.length>0) { return vertices[0] }
        }
    }

    getContainerByEObject(eObject){
        var items=this.getByEObject(eObject);
        if(items)
        {
            var vertices=items.filter(function(e){
                if(e instanceof Container){
                    return true
                }
                return false;
            })
            if(vertices.length>1) { console.warn('ambigous solution, returning first container match')}
            if(vertices.length>0) { return vertices[0] }
        }
    }

    getContainerByObjectId(objectId){
        var items=this.getByObjectId(objectId);
        if(items)
        {
            var vertices=items.filter(function(e){
                if(e instanceof Container){
                    return true
                }
                return false;
            })
            if(vertices.length>1) { console.warn('ambigous solution, returning first container match')}     
            if(vertices.length>0) { return vertices[0] }
        }
    }

    invalidate(graphObject){
        this.events["OBJECT_INVALID"].raise(graphObject);
    }

    getIndexItem(i){
        var res=null;
        if(i>=0)
        {
            if(i<=this._index.size-1)
            {      
                res=Array.from(this._index)[i][1]
            }
        }
        else
        {
            if(this._index.size-i>0)
            {                  
                res=Array.from(this._index)[this._index.size+i][1];
            }
        }
        return res
    }

}
