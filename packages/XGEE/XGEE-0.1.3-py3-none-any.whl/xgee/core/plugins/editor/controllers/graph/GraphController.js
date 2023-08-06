
import GraphEvent from '../../model/graph/GraphEvent.js'

export default class GraphController{
    constructor(ecoreSync) {   
        var self=this;
        this.ecoreSync=ecoreSync;
        this.eObject=null;
        this.model=null;
        this.layout=null;
        this.view=null;
        this.interactions=[];
        this.paletteController=null;
        this.vertexControllers=[];   
        this.edgeControllers=[];   
        this._controllers=[];
        this.controllerEvents={};

        this.controllerEvents["initBegin"]=new GraphEvent();
        this.controllerEvents["initEnd"]=new GraphEvent();
        this.controllerEvents["EDGE_CONNECTED"]=new GraphEvent();

        this.on('initBegin',function(){
            $(self.view.loadingIndication).show();
        })

        this.on('initEnd',function(){
            $(self.view.loadingIndication).hide();
            self.view.enableAutoRefresh();
            self.view.init()
        })
    
    }     


    on(event,cb){
        if(this.controllerEvents[event])
        {
            return this.controllerEvents[event].addListener(cb)
        }
        else
        {
            return -1
        }
    }

    registerController(controller)
    {
        this._controllers.push(controller)
    }

    async loadModelData(){
        var self=this
        this.model=new GraphModel();
        if(this.eObject)
        {                      
                let valueSet=new Object();
                valueSet["PARENT"]=this.eObject
                valueSet["ROOT"]=await ecoreSync.getObject(0)
                valueSet["MODELROOT"]=await ecoreSync.utils.getModelRoot(this.eObject)
                valueSet["RESOURCE"]=await ecoreSync.utils.getResource(this.eObject)
                var vertices=[];
                var edges=[];
                this.vertexControllers.forEach(function(e){                               
                    vertices.push(e.load(copyValueSet(valueSet)))                         
                })
                this.edgeControllers.forEach(function(e){            
                    edges.push(e.load(copyValueSet(valueSet)))
                })

                vertices= await Promise.all(vertices).catch(function(e){ console.error('Error loading vertices: '+e); return [] })
                edges= await Promise.all(edges).catch(function(e){ console.error('Error loading edges: '+e);  return [] })

                vertices.forEach(function(vcr){
                    vcr.forEach(function(v){
                        self.model.addVertex(v);
                    })                    
                })

                edges.forEach(function(ecr){
                    ecr.forEach(function(e){
                        self.model.addEdge(e);
                    })    
                })

                return true
            }
            else
            {
                return false
            }
    }

    async loadLayoutData()
    {
        var self=this;
        var toplevelVertices=[]
        var initVertexPosition=async function(v){ 
            var position=self.layout.getVertexPosition(v);          
            if(position) return position
            return {x:0,y:0}
        }
        var initVertex=async function(v)
        {       
            v.position=await initVertexPosition(v)
            var vertices=[];           
            v.vertices.forEach(function(sv){
                vertices.push(initVertex(sv));
            });
            return await Promise.all(vertices)
        }
        for(let i in this.model.vertices)
        {
            toplevelVertices.push(initVertex(this.model.vertices[i]))
        }
        await Promise.all(toplevelVertices)        
    }

    
    async init(paletteController){
        this.paletteController=paletteController
        this.controllerEvents["initBegin"].raise();
        var t0 = performance.now();
        var self=this
        await this.model.init()
        await this.view.reset();

        var initContainer=async function(c){           
            self.view.addContainerToGraph(c);   
            await c.arrange();  
            for(let subVertex of c.vertices)
            {
                await initVertex(subVertex);
            }
        }
        var initEdge=async function(e){
            self.view.addEdgeToGraph(e);         
            for(let container of e.containers)
            {
                await initContainer(container);
            }
        }        
        var initVertex=async function(v){ 
            self.view.addVertexToGraph(v);
            await v.arrange();

            for(let subVertex of v.vertices)
            {
                await initVertex(subVertex);
            }
            for(let subEdge of v.edges)
            {
                await initEdge(subEdge);
            }

            v.labels.forEach(function(lbl){
                self.view.addLabelToGraph(lbl);
            });        
                
        }

        
        this.view.graph.model.beginUpdate()
  
        for(let vertex of this.model.vertices)
        {
            await initVertex(vertex);
        }  

        for(let edge of this.model.edges)
        {
            await initEdge(edge);
        }  
  
        this.view.graph.model.endUpdate()

        //controller reaction to model changes
        this.model.on('VERTEX_ADDED',function(vertex){       

            initVertex(vertex);
            let notDisplayedEdges=self.view.getUndisplayedEdges();
            notDisplayedEdges.forEach(function(edge){
                //Check if any undrawn edge can be displayed
                let sourceAnchors=edge.getSourceAnchors();
                let targetAnchors=edge.getTargetAnchors();   
              
                if(sourceAnchors.length && targetAnchors.length && sourceAnchors.some((sourceAnchor)=>{self.view.isDisplayed(sourceAnchor.getUUID())}) && targetAnchors.some((targetAnchor)=>{self.view.isDisplayed(targetAnchor.getUUID())}))
                {                   
                    self.view.addEdgeToGraph(edge); //re-attempt to display the edge
                }               
            });
        })
        
        this.model.on('VERTEX_REMOVED',function(vertex){
            if(vertex.parent!=self.model)  self.model.invalidate(vertex.parent);           
            self.view.removeVertexFromGraph(vertex);
        })

        this.model.on('EDGE_ADDED',function(edge){
            initEdge(edge);           
        })
        
        this.model.on('EDGE_REMOVED',function(edge){           
            self.view.removeEdgeFromGraph(edge);
        })

        this.model.on('EDGE_ANCHORS_CHANGED',function(edge){          
           
            if(self.view.isEdgeDisplayed(edge))
            {             
                self.view.removeEdgeFromGraph(edge);
            }     

            initEdge(edge);
        })


        this.model.on('OBJECT_INVALID',function(graphObject){
            self.view.refresh(graphObject.getUUID())
        })

        this.model.on('LAYOUT_INVALID',function(){
            self.reloadLayout()
        })

        var t1 = performance.now();
        console.debug("Loading graph took " + (t1 - t0) + " milliseconds.");    
        this.controllerEvents["initEnd"].raise();   
    }


    selectDropReceiver(dropTarget,dropItem){
        return this.interactions.find(function(interaction){ return interaction.isTargeting(dropTarget) && interaction.isReceiving(dropItem) })
    }


    isDroppable(dropTarget,dropLocation,dropItem)
    {
        var dropReceiver=null;
        if(!dropTarget){ 
            dropReceiver=this.selectDropReceiver(this.eObject,dropItem); 
        }
        else
        {
            dropReceiver=this.selectDropReceiver(dropTarget,dropItem); 
        }
        
        if(dropReceiver) { return true }
        return false;
    }

    async drop(dropTarget,dropLocation,dropItem){
        //this allows drag&drop from any sourcev
        var res=false;
        var dropReceiver=null;
        if(!dropTarget || dropTarget == this.eObject){
            //drop occured on the canvas
            dropTarget=this.eObject;
            this.model.layout.addTemporaryVertexPosition(ecoreSync.rlookup(dropItem),ecoreSync.rlookup(dropTarget),dropLocation);
            dropReceiver=this.selectDropReceiver(this.eObject,dropItem);       
        }
        else{
            //drop occured on a graph object
            dropReceiver=this.selectDropReceiver(dropTarget,dropItem); 
        }

        if(dropReceiver){     
            this.ecoreSync.exec(await dropReceiver.getCmd(dropTarget,dropItem))
            res=true;
        }
        return res;
    }


    isPastable(pasteItem){
        //just an alias for isDroppable        
        var selectedCells=this.view.graph.getSelectionCells();
        var pasteTarget=null;
        if(selectedCells.length==1)
        {
            pasteTarget=selectedCells[0].value.getEObject();
        }
        var res=this.isDroppable(pasteTarget,null,pasteItem);
        return res;
    }

    paste(pasteItem,pasteTarget=null,location={x:0,y:0}){
        // Pastes an item to a paste target at a certain (relative) location
        if(pasteTarget == null)
        {
            var selectedCells=this.view.graph.getSelectionCells();
            if(selectedCells.length==1 && !ignoreSelection)
            {
                pasteTarget=selectedCells[0].value.getEObject();
            }
        }
        var res= this.drop(pasteTarget,location,pasteItem);
        return res;
    }

    select(eObjects)
    {
        if(eObjects)
        {
            if(Array.isArray(eObjects))
            {
                //TODO
            }
            else
            {
                //TODO
            }
        }
        else
        {
            this.view.clearSelection()
        }
    }
    
    getAllVertices(){
        var vertices=[...this.model.vertices]        
        var getSubVertices=(vertex)=>{
            vertex.vertices.forEach((v)=>{
                vertices.push(v)
                getSubVertices(v)
            })
        }
        vertices.forEach(getSubVertices)
        return vertices
    }

    async setConnectable(filter){
        //async, because filter is async, therefore, it takes some time to initialize the tool    
        var self=this;
        let allVertices=this.getAllVertices()
        var selection=await filter(allVertices)
        let vertexList=allVertices.flatMap((vertex,index) =>   selection[index] ? vertex : [])
        vertexList.forEach(function(vertex){
            //should this be dependend on the GraphModel ?           
            self.view.setVertexConnectable(vertex);
        })
    }

    async setNotConnectable(filter){
        //async, because filter is async, therefore, it takes some time to initialize the tool    
        var self=this;
        let allVertices=this.getAllVertices()
        var selection=await filter(allVertices)
        let vertexList=allVertices.flatMap((vertex,index) =>  selection[index] ? vertex : [])
        vertexList.forEach(function(vertex){
            //should this be dependend on the GraphModel ?           
            self.view.setVertexNotConnectable(vertex);
        })
    }

    canCreateEdge(source,target)
    {
        var tool=this.paletteController.getActiveTool()
        if(tool.isEdgeTool)
        {
            return tool.canCreate(source.value.getEObject(),target.value.getEObject());
        }
        return false;
    }

    createEdge(source,target)
    {
        var tool=this.paletteController.getActiveTool()
        if(tool.isEdgeTool)
        {
            tool.create(source.value.getEObject(),target.value.getEObject());
        }
    }

    getBoundingBox()
    {
        let x_min=null
        let x_max=null
        let y_min=null
        let y_max=null

        x_min=this.model.vertices[0].position.x-this.model.vertices[0].size.x*0.5
        x_max=this.model.vertices[0].position.x+this.model.vertices[0].size.x*0.5
        y_min=this.model.vertices[0].position.y-this.model.vertices[0].size.y*0.5
        y_max==this.model.vertices[0].position.y+this.model.vertices[0].size.y*0.5

        for(let i=1;i<this.model.vertices.length;i++)
        {
            x_min=Math.min(x_min,this.model.vertices[i].position.x-this.model.vertices[i].size.x*0.5)
            x_max=Math.max(x_max,this.model.vertices[i].position.x+this.model.vertices[i].size.x*0.5)
            y_min=Math.min(y_min,this.model.vertices[i].position.y-this.model.vertices[i].size.y*0.5)
            y_max=Math.max(y_max,this.model.vertices[i].position.y+this.model.vertices[i].size.y*0.5)
        }

        //10 Percent padding
        x_min-=0.1*x_min
        x_max+=0.1*x_max
        y_min-=0.1*y_min
        y_max+=0.1*y_max

        return {x:x_min,y:y_min,width:x_max-x_min,height:y_max-y_min,centerX:x_min+0.5*(x_max-x_min),centerY:y_min+0.5*(y_max-y_min)}
    }

    highlightByEObject(eObjects,color='#FF0000')
    {
        var self=this

        var highlightedElements=[]
        eObjects.forEach((eObject) => {   
            self.model.getByEObject(eObject).forEach((elem)=>{ highlightedElements.push(elem) }) 
        })

        var removeHighlights=self.view.highlight(highlightedElements,color)
        return removeHighlights        
    }

    async highlightByQuery(query,color='#FF0000')
    {
        var self=this
        var removeHighlights=()=>{}
        var highlightedElements=[]
        var eObjects=await this.ecoreSync.exec(new eoq2.Get(query))

        //Adjust filter
        var observerToken=await this.ecoreSync.observe(query,(results,deltaPlus,deltaMinus)=>{
            removeHighlights()
            results.forEach((eObject) => {   
                self.model.getByEObject(eObject).forEach((elem)=>{ highlightedElements.push(elem) }) 
            })
            eObjects=results
            removeHighlights=self.view.highlight(highlightedElements,color)
        })


        //React to display changes
        self.model.on('VERTEX_ADDED',function(vertex){ 
            if(eObjects.includes(vertex.eObject)){
                highlightedElements.push(vertex)
                removeHighlights()
                removeHighlights=self.view.highlight(highlightedElements,color)
            } 
        })

        self.model.on('EDGE_ADDED',function(vertex){ 
            if(eObjects.includes(vertex.eObject)){
                highlightedElements.push(vertex)
                removeHighlights()
                removeHighlights=self.view.highlight(highlightedElements,color)
            } 
        })


        //Initial highlighting
        if (Array.isArray(eObjects)){           

    
            eObjects.forEach((eObject) => {   
                self.model.getByEObject(eObject).forEach((elem)=>{ highlightedElements.push(elem) }) 
            })

            removeHighlights=self.view.highlight(highlightedElements,color)
        }
        return () => {            
            self.ecoreSync.unobserve(observerToken)
            removeHighlights()
        }        
    }

    async reloadLayout()
    {
        let self=this
        let vertices=this.model.vertices
        for(let i=0;i<vertices.length;i++)
        {
            let vertex=vertices[i]
            if(self.model.layout.isVertexInLayout(vertex))
            {
                let position=await self.model.layout.getVertexPosition(vertex)
                vertex.setPosition(position.x,position.y)            
            }
        }
      
        self.view.refreshVertices(vertices)     
    }


}










