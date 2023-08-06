import GraphEvent from './GraphEvent.js'

export default class VertexContainer{
    initializer(){
        this.vertices=[];
        
        if(!this.events)
        {
            this.events={};           
        }

        this.events["VERTEX_ADDED"]=new GraphEvent(true);
        this.events["VERTEX_REMOVED"]=new GraphEvent(true);        
        this.events["LABEL_CHANGED"]=new GraphEvent(true);
    }
    
    on(event,cb){
        if(this.events[event])
        {
            return this.events[event].addListener(cb)
        }
        else
        {
            return -1
        }
    }

    containsVertex(vertex){
        var idx=this.vertices.indexOf(vertex);
        // doesn't work?
        if(idx > -1){ return true } else { return false }       
    }

    addVertex(vertex)
    {
        this.vertices.push(vertex);
        vertex.parent=this;                
        this.events["VERTEX_ADDED"].raise(vertex);   
    }

    removeVertex(vertex)
    {
        let idx=this.vertices.indexOf(vertex);
        if(idx > -1)
        {
            this.vertices.splice(idx, 1);
        }      

        if(vertex.hasVertices())
        {
            vertex.removeAllVertices();
        }

        this.events["VERTEX_REMOVED"].raise(vertex);   
    }

    removeAllVertices(){
        var self=this;
        if(this.hasVertices())
        {
            let subVertices=this.vertices;
            subVertices.forEach(function(vertex){
                self.removeVertex(vertex);
            })
        }
    }

    async arrange(){
        var self=this;
        var anchors={"north":[],"east":[],"south":[],"west":[],"list":[],"body":[],"relative":[]}
        this.vertices.forEach(function(v){

            let positioning=v.type.model.get("positioning")?v.type.model.get("positioning"):'RELATIVE' //default value, because ecore implementation is faulty
            
            switch(positioning)
            {
                case "NORTH":
                anchors.north.push(v);
                break;
                case "EAST":
                anchors.east.push(v);
                break;
                case "SOUTH":
                anchors.south.push(v);
                break;
                case "WEST":
                anchors.west.push(v);
                break;
                case "LIST":
                anchors.list.push(v);
                break;
                case "BODY":
                anchors.body.push(v);
                break;
                case "RELATIVE":
                anchors.relative.push(v);
                break;
                default:
                anchors.list.push(v);
                break;
            }      
        
        })

        //Determine space requirements 
        var reqSize={north:0,east:0,south:0,west:0};
        var spacing=0.5;

        anchors.north.forEach(function(v,i){
            if(i==0) reqSize.north=2*v.size.x*spacing;
            reqSize.north+=v.size.x+v.size.x*spacing;
        });

        anchors.east.forEach(function(v,i){
            if(i==0) reqSize.east=2*v.size.y*spacing;
            reqSize.east+=v.size.y+v.size.y*spacing;
        });

        anchors.south.forEach(function(v,i){
            if(i==0) reqSize.south=2*v.size.x*spacing;
            reqSize.south+=v.size.x+v.size.x*spacing;
        });

        anchors.west.forEach(function(v,i){
            if(i==0) reqSize.west=2*v.size.y*spacing;
            reqSize.west+=v.size.y+v.size.y*spacing;
        });
      
        var reqSizeX=Math.max(reqSize.north,reqSize.south);
        var reqSizeY=Math.max(reqSize.east,reqSize.west);

       this.setMinSize(reqSizeX,reqSizeY);
       this.minSize.x=reqSizeX;
       this.minSize.y=reqSizeY;

       if(this.size.x<reqSizeX || this.size.y<reqSizeY)
       {  
           this.resize(Math.max(reqSizeX,this.size.x),Math.max(reqSizeY,this.size.y));
           //arrange will be called on resize again
       }
       else
       {    
            //Placing subvertices with relative positioning
            var absOffsets={north:0,east:0,south:0,west:0};

            anchors.north.forEach(function(v,i){
                if(i==0) absOffsets.north=v.size.x*spacing;
                let absX=absOffsets.north+v.size.x*0.5;     
                absOffsets.north+=v.size.x+v.size.x*spacing;
                let relX=absX/self.size.x;
                let relY=0
                //Model-defined static offsets
                let relOffset=self.getRelativeOffset(v);           
                v.position.x=relOffset.x+relX;
                v.position.y=relOffset.y+relY;
            })

            anchors.south.forEach(function(v,i){
                if(i==0) absOffsets.south=v.size.x*spacing;
                let absX=absOffsets.south+v.size.x*0.5;       
                absOffsets.south+=v.size.x+v.size.x*spacing;
                let relX=absX/self.size.x;
                let relY=1;
                //Model-defined static offsets
                let relOffset=self.getRelativeOffset(v);           
                v.position.x=relOffset.x+relX;
                v.position.y=relOffset.y+relY;
            })

            anchors.west.forEach(function(v,i){
                if(i==0) absOffsets.west=v.size.y*spacing;
                let absY=absOffsets.west+v.size.y*0.5;     
                absOffsets.west+=v.size.y+v.size.y*spacing;  
                let relX=0
                let relY=absY/self.size.y;      
                //Model-defined static offsets
                let relOffset=self.getRelativeOffset(v);           
                v.position.x=relOffset.x+relX;
                v.position.y=relOffset.y+relY;
            })

            anchors.east.forEach(function(v,i){
                if(i==0) absOffsets.east=v.size.y*spacing;
                let absY=absOffsets.east+v.size.y*0.5;     
                absOffsets.east+=v.size.y+v.size.y*spacing;            
                let relX=1;
                let relY=absY/self.size.y;
                //Model-defined static offsets
                let relOffset=self.getRelativeOffset(v);           
                v.position.x=relOffset.x+relX;
                v.position.y=relOffset.y+relY;
            })

        
            anchors.list.forEach(function(v,i){
                let yOffset=5/self.size.y;;
                let x=0.5;     
                let y=(1+i)*yOffset; 
                let relOffset=self.getRelativeOffset(v)            
                v.position.x=relOffset.x+x;
                v.position.y=relOffset.y+y;
            })

            anchors.relative.forEach(function(v,i){        
                let x=0.5;     
                let y=0.5; //center of container
                let relOffset=self.getRelativeOffset(v)            
                v.position.x=relOffset.x+x;
                v.position.y=relOffset.y+y; 
            })


           
            for( let v of anchors.body )
            {
                //auto-center
                let x=0.5;     
                let y=0.5;
                let xOffset=(-v.size.x/2)/self.size.x;
                let yOffset=(-v.size.y/2)/self.size.y;

                let relOffset=self.getRelativeOffset(v)      
                     
                //Default values
                v.position.x=x+relOffset.x+xOffset
                v.position.y=y+relOffset.y+yOffset

                //Loaded vertex position
                let vertexPosition=await self.graphModel.layout.getVertexPosition(v)
                if(!VertexContainer.isDefault){
                    v.position.x=vertexPosition.x
                    v.position.y=vertexPosition.y
                }

            }

        this.labels.forEach(function(v,i){
                    var x=0;
                    var y=0;
                    switch(v.anchor)
                    {
                        case 'NORTH':
                            x=0.5;
                            y=0;
                        break;
                        case 'EAST':
                            x=1;
                            y=0.5;
                        break;
                        case 'SOUTH':
                            x=0.5;
                            y=1;
                        break;
                        case 'WEST':
                            x=0;
                            y=0.5;
                        break;
                        case 'NORTHEAST':
                            x=1;
                            y=0;
                        break;
                        case 'NORTHWEST':
                            x=0;
                            y=0;
                        break;
                        case 'SOUTHEAST':
                            x=1;
                            y=1;
                        break;
                        case 'SOUTHWEST':
                            x=0;
                            y=1;
                        break;
                        case 'CENTER':
                            x=0.5;
                            y=0.5;
                        break;
                        default:
                            x=0;
                            y=0;
                    }
                    let relOffset=self.getRelativeOffset(v);
                    v.position.x=x+relOffset.x;
                    v.position.y=y+relOffset.y;
                });
        }

    }

    getVertexByObjectId(objectId){
        var self=this;
        return this.vertices.find(function(v){
            return v.getEObjectId()==objectId
        });
    }

    getVertexByEObject(eObject){
        var self=this;
        return this.vertices.find(function(v){
            return v.getEObject()==eObject
        });        
    }


    hasVertices(){
        return this.vertices.length ? true : false
    }

    hasStaticVertices(){
        return this.vertices.filter(v => v.type.model.eClass.get('name')=='StaticSubVertex').length ? true : false
    }

    getVertices(){
        return this.vertices
    }

    getStaticVertices(){
        return this.vertices.filter(v => v.type.model.eClass.get('name')=='StaticSubVertex')
    }

    getClosest(orientation='NORTH'){
        let res=this
        if(this.hasStaticVertices())
        {
            let staticVertices=this.getStaticVertices()

          
            let order=staticVertices
            if(orientation == 'NORTH' || orientation =='SOUTH')
            {
                order=[...staticVertices].sort((a,b)=>{                
                    let res=0;                 
                    if(a.offset.y+a.size.y > b.offset.y+b.size.y)
                    { 
                        res=1 
                    } else if( a.offset.y+a.size.y < b.offset.y+b.size.y ){
                        res=-1 
                    } 
                    return res           
                
                })
            }

            if(orientation=='EAST' || orientation == 'WEST')
            {
                order=[...staticVertices].sort((a,b)=>{ 
                    let res=0;                 
                    if(a.offset.x+a.size.x > b.offset.x+b.size.x)
                    { 
                        res=1 
                    } else if( a.offset.x+a.size.x < b.offset.x+b.size.x ){
                        res=-1 
                    } 
                    return res         

                })
            }

            let mostNorth=order[0]
            let mostSouth=order[order.length -1]
            let mostEast=order[0]
            let mostWest=order[order.length - 1]

            if(orientation=='NORTH' && mostNorth.offset.y < 0)
            {
                res=mostNorth
            }

            if(orientation=='SOUTH' && mostSouth.offset.y+mostSouth.size.y > this.size.y/2)
            {
                res=mostSouth
            }

            if(orientation=='EAST' && mostEast.offset.x+mostEast.size.x > this.size.x/2)
            {
                res=mostEast
            }

            if(orientation=='WEST' && mostWest.offset.x < -this.size.x/2)
            {
                res=mostWest   
            }        
        }
        else
        {
            console.error('NO STATIC VERTICES')
        }
        
        return res
    }
       

}