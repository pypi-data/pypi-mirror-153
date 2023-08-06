import GraphEvent from './GraphEvent.js'

export default class LocatableObject{
    initializer(){
        this.position={x:0,y:0}  
        this.offset={x:0,y:0}   
        this.events["MOVE"]=new GraphEvent(); 
    }  

    isMovable(){
        return true
    }

    getPosition()
    {
        return Object.assign({},this.position);
    }

    setPosition(x,y){
        this.position.x=x;
        this.position.y=y;   
    }

    moveBy(dx,dy){
        if(this.isMovable()) this.moveTo(this.position.x+dx,this.position.y+dy)    
    }

    moveTo(x,y){
        if(this.isMovable())
        {
            if(this.position.x!=x || this.position.y!=y)
            {
                var info={end:{x:x,y:y},start:{x:this.position.x,y:this.position.y},increment:{dx:x-this.position.x,dy:y-this.position.y}};
                this.setPosition(x,y);    
                this.events["MOVE"].raise(info);
            }
        }
    }

}