import GraphObject from './GraphObject.js'
import VertexContainer from './VertexContainer.js'
import EdgeContainer from './EdgeContainer.js'
import TypedObject from './TypedObject.js'
import LabelProvider from './LabelProvider.js'
import SizableObject from './SizableObject.js'
import DeletableObject from './DeletableObject.js'
import LocatableObject from './LocatableObject.js'
import EObjectOwner from './EObjectOwner.js'
import { multipleClasses }  from '../../lib/libaux.js'



export default class Vertex extends multipleClasses(GraphObject,VertexContainer,EdgeContainer,TypedObject,DeletableObject,LabelProvider,SizableObject,LocatableObject,EObjectOwner){
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
        this.maxSize={x:sizeX*20,y:sizeY*20}

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

       this.on('EDGE_ADDED',function(edge){           
            if(self.parent)
            {
                self.graphModel.events["EDGE_ADDED"].raise(edge);
            }     
        })

        this.on('EDGE_REMOVED',function(edge){
            if(self.parent)
            {
                self.graphModel.events["EDGE_REMOVED"].raise(edge);
            }
        })


        //Update remote position
        this.on('MOVE',function(translate){
            self.graphModel.layout.setVertexPosition(self,translate.end.x,translate.end.y);
        });

        //Update remote size
        this.on('RESIZE',async function(transform){
            await self.arrange();
            self.graphModel.layout.setVertexSize(self,transform.end.x,transform.end.y);
        });
       
    }

    addVertex(vertex)
    {
        this.graphModel.addToIndex(vertex)
        super.addVertex(vertex);  
    }

    removeVertex(vertex)
    {
        this.graphModel.removeFromIndex(vertex)
        super.removeVertex(vertex);        
    }
    
    addEdge(edge)
    {
        this.graphModel.addToIndex(edge)
        super.addEdge(edge);
    }

    removeEdge(edge)
    {
        this.graphModel.removeFromIndex(edge)
        super.removeEdge(edge);        
    }

    isMovable(){
        return this.type.model.get("isMovable") == "true" //TODO: adjust model to return boolean, this is not how it should be!!!!
    }

    isResizable(){
        return this.type.model.get("isMovable") === "true"
    }

    toString()
    {
        return '';
    }
}
