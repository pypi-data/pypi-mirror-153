

import GraphEvent from './GraphEvent.js'

export default class SizableObject{
    initializer(){
       this.size={x:0,y:0}
       this.minSize={x:0,y:0}
       this.maxSize={x:0,y:0}
       this.events["RESIZE"]=new GraphEvent();
    }  
    isResizable(){
        return true
    }
    setSize(sizeX,sizeY){
        var info={start:{x:this.size.x,y:this.size.y},end:{x:sizeX,y:sizeY},increment:{dX:sizeX-this.size.x,dY:sizeY-this.size.y}};
        this.size.x=sizeX;
        this.size.y=sizeY;
        return info
    }
    getSize(){
        return this.size
    }
    setMinSize(x,y){
        this.minSize.x=x;
        this.minSize.y=y;
    }
    setMaxSize(x,y){
        this.maxSize.x=x;
        this.maxSize.y=y;
    }
    resizeRelative(growthX,growthY=null)
    {
        if(growthY==null){ growthY=growthX };
        this.resize(this.sizeX*growthX,this.sizeY*growthY)           
    }
    resize(sizeX,sizeY){
        if((this.size.x!=sizeX || this.size.y!=sizeY) && sizeX>0 && sizeY>0)
        {        
            var info={start:{x:this.size.x,y:this.size.y},end:{x:sizeX,y:sizeY},increment:{dX:sizeX-this.size.x,dY:sizeY-this.size.y}};
            this.size.x=sizeX;
            this.size.y=sizeY;
            this.events["RESIZE"].raise(info);    
        }
    }
    getRelativeOffset(vertex)
    {
        return {x:vertex.offset.x/this.size.x,y:vertex.offset.y/this.size.y};
    }

    getRelativeX(x)
    {
        return x/this.size.x
    }

    getRelativeY(y)
    {
        return y/this.size.y
    }
}