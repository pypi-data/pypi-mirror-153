import TypedObject from './TypedObject.js'
import EObjectOwner from './EObjectOwner.js'
import { multipleClasses }  from '../../lib/libaux.js'
import Vertex from './Vertex.js'
import StaticVertex from './StaticVertex.js'

export default class Anchor extends multipleClasses(TypedObject,EObjectOwner){
    constructor(graphModel,parent=null){
        super();
        this.graphModel=graphModel;
        this.parent=parent;
    }

    getUUID(){  
        let anchorObject=null
        if(this.eObject==null){ throw 'anchor eObject is null' }
        let graphModelObjects=this.graphModel.getByEObject(this.eObject);

        if(graphModelObjects.length){
            graphModelObjects=graphModelObjects.filter(graphObject => { return graphObject instanceof Vertex || graphObject instanceof StaticVertex })
            graphModelObjects=graphModelObjects.sort((a,b)=>{ 
                //Prefer vertices over static vertices
                let res=0
                let isVertexA=a instanceof Vertex
                let isVertexB=b instanceof Vertex              
                if(isVertexA < isVertexB){
                    res=1
                } else if (isVertexA > isVertexB){
                    res=-1
                }     

                return res
            })

            let vertex=graphModelObjects[0] //taking the first possible Vertex/StaticVertex
            if(vertex && vertex.hasStaticVertices())
            {               
               anchorObject=vertex.getClosest(this.type.model.get("attach"))
            }
            else
            {
                anchorObject=vertex
            }            
       
            if(anchorObject){ 
                return anchorObject.uuid
            }
            
        }
        
        return 'NO_UUID';      
    }

    getType(){
        return this.type.model.get("type")
    }
}