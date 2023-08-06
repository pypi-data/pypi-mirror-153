import GraphObject from './GraphObject.js'
import VertexContainer from './VertexContainer.js'
import EdgeContainer from './EdgeContainer.js'
import TypedObject from './TypedObject.js'
import LabelProvider from './LabelProvider.js'
import SizableObject from './SizableObject.js'
import LocatableObject from './LocatableObject.js'
import EObjectOwner from './EObjectOwner.js'
import { multipleClasses }  from '../../lib/libaux.js'

export default class Container extends multipleClasses(GraphObject,VertexContainer,EdgeContainer,TypedObject,LabelProvider,SizableObject,LocatableObject,EObjectOwner){
    constructor(graphModel){
        super();
        this.graphModel=graphModel;      
    }
    
    init(){   
        var self=this;
         
        //Position
        this.position={x:0,y:0}

        //Size
        let sizeX=Number.parseFloat(this.type.model.get("sizeX"))
        if(Number.isNaN(sizeX)) sizeX=0
        let sizeY=Number.parseFloat(this.type.model.get("sizeY"))
        if(Number.isNaN(sizeY)) sizeY=0
        this.size={x:sizeX,y:sizeY}
        this.minSize={x:sizeX*0.5,y:sizeY*0.5}
        this.maxSize={x:sizeX*2,y:sizeY*2}

        //Offset
        let offsetX=Number.parseFloat(this.type.model.get("offsetX"));
        if(Number.isNaN(offsetX)) offsetX=0
        let offsetY=Number.parseFloat(this.type.model.get("offsetY"));
        if(Number.isNaN(offsetY)) offsetY=0
        this.offset={x:offsetX,y:offsetY};


        this.on('VERTEX_ADDED',async function(vertex){           
            if(self.parent)
            {
                await self.arrange();
                self.graphModel.events["VERTEX_ADDED"].raise(vertex);
            }     
       })
    
       this.on('VERTEX_REMOVED',async function(vertex){
            if(self.parent)
            {
                await self.arrange();
                self.graphModel.events["VERTEX_REMOVED"].raise(vertex);
            }
       })
    }

    isMovable(){
        return false
    }

    isResizable(){
        return false
    }

    toString()
    {
        return '';
    }

    addVertex(vertex)
    {
        super.addVertex(vertex);
        this.graphModel.addToIndex(vertex)
    }

    removeVertex(vertex)
    {
        super.removeVertex(vertex);
        this.graphModel.removeFromIndex(vertex)
    }

}