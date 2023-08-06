/**
 * GraphView module
 * @author Matthias Brunner
 * @copyright 2019-2021 University of Stuttgart, Institute of Aircraft Systems, Matthias Brunner
*/

import Label from '../model/graph/Label.js'
import Edge from '../model/graph/Edge.js'
import Vertex from '../model/graph/Vertex.js'
import { GraphViewPort, GraphViewPortOutline } from './GraphViewPort.js'





/** Class managing the graph view and its outline */
class GraphView{
    /**
     * Create a graph view and its outline 
     * @param {DOMelement} editorDOM - The DOM element that should contain the graph visualization.
     * @param {DOMelement} outlineDOM - The DOM element that should contain the graph outline. 
     */
    constructor(editorDOM,outlineDOM)
    {
        var self=this;
        this.autoRefresh=false; //enable auto refresh after items have been added
        this.eventBroker=$app.plugins.require('eventBroker'); // should be set by the constructor instead
        this.lastClickLocation={x:0,y:0}

        try{
            this.graph=this._initializeGraph(editorDOM,outlineDOM); 
        }
        catch(e)
        {
            console.error('graph initialization failed for GraphView: '+e);
        }

      
        this.graphController=null;

        this.loadingIndication=$(document.createElement('div'))
        .addClass('editorLoader')
        .prependTo(this.graph.container)
        .hide();        

        //Enable HTML Labels
        this.graph.setHtmlLabels(true)

        //Event for Zoom In/Zoom Out via mouse wheel
        mxEvent.addMouseWheelListener(
    
            mxUtils.bind(this, function(evt, up){ 
                
                var x = mxEvent.getClientX(evt);
                var y = mxEvent.getClientY(evt);
                var offset = mxUtils.getOffset(self.graph.container);        
                var target={x:x-offset.x,y:y-offset.y}        
                var origin = mxUtils.getScrollOrigin();
                var elt = document.elementFromPoint(mxEvent.getClientX(evt), mxEvent.getClientY(evt));
                while (elt != null && elt != self.graph.container)
                {
                        elt = elt.parentNode;
                }
        
                // Checks if event is inside the bounds of the graph container
                let isContained=elt!=null&& x>=offset.x-origin.x && y>=offset.y-origin.y &&x <= offset.x - origin.x +  self.graph.container.offsetWidth && y <= offset.y - origin.y +  self.graph.container.offsetHeight;
                    if(isContained)
                    {   
                        if(up){ self.viewPort.zoomTo(target,1.1);}else{ self.viewPort.zoomTo(target,1/1.1);}
                        mxEvent.consume(evt);
                    }
        })
        );

        //Paste-Handling for the Editor
        editorDOM.setAttribute('contenteditable',true);
        editorDOM.addEventListener('paste', async (event) => { 
            var clipboard=$app.plugins.require('clipboard');
            await clipboard.evalEvent(event);
            if(await clipboard.hasContents(function(e){ return self.graphController.isPastable(e); })){
                let cnts=await clipboard.getContents(function(e){ return self.graphController.isPastable(e); })        
                cnts.forEach(function(e){        
                   self.graphController.paste(e,null,self.lastClickLocation);
                });
            }    
            event.stopPropagation();
        } )

        //Copy-handling for the editor
        editorDOM.addEventListener('copy', async (event) => { 
            var clipboard=$app.plugins.require('clipboard');
            var eObjects=[];
            var selectedCells=self.graph.getSelectionCells();
            if(selectedCells.length)
            {
                for (let i in selectedCells)
                {
                    eObjects.push(ecoreSync.utils.getObjectURL(selectedCells[i].value.getEObject()))
                }
            }
            if(eObjects.length)
            {
                await clipboard.evalEvent(event,eObjects); 
            }           
            event.stopPropagation();
        } )


        //Cut-handling for the editor
        editorDOM.addEventListener('cut', async (event) => { 
            var clipboard=$app.plugins.require('clipboard');
            var eObjects=[];
            var selectedCells=self.graph.getSelectionCells();
            if(selectedCells.length)
            {
                for (let i in selectedCells)
                {
                    eObjects.push(ecoreSync.utils.getObjectURL(selectedCells[i].value.getEObject()))
                }
            }
            if(eObjects.length)
            {
                await clipboard.evalEvent(event,eObjects); 
            }           
            event.stopPropagation();
        } )

        //SHIFT+D event handling for duplicate/copy here
        editorDOM.addEventListener('keydown', async (event) => { 
            if(event.shiftKey && event.key === 'D')
            {               
                var selectedCells=self.graph.getSelectionCells();
                if(selectedCells.length)
                {
                    let cell=selectedCells[0]
                    let copy=await ecoreSync.clone(cell.value.getEObject());        
                    let pos=cell.value.getPosition()
                    pos.x+=cell.value.getSize().x
                    pos.y+=cell.value.getSize().y             
                    self.graphController.paste(copy,cell.value.parent.getEObject(),pos)
                     this.graph.setSelectionCells(cells);
                }
                event.stopPropagation();
            }
            
           
        } )

        //Context Menu on Right-Click
        var contextMenuArmed=false;
        var panStart=null
        var panTranslate=null
        this.graph.addMouseListener(
        {
            mouseDown: function(sender, evt)
            {
                
                if(mxEvent.isRightMouseButton(evt.evt))
                {                     
                    //Panning Handler start        
                    panStart={x:evt.evt.x,y:evt.evt.y}
                    panTranslate=self.viewPort.getTranslate()
                    contextMenuArmed=true;
                    evt.consume();
                }
                else
                {
                    contextMenuArmed=false;
                }
            },
            mouseMove: function(sender, evt)
            {
                contextMenuArmed=false;  
                if(panStart!=null && panTranslate !=null)
                {
                    let panCurrent={x:evt.evt.x,y:evt.evt.y}
                    let panVector={x:panCurrent.x-panStart.x,y:panCurrent.y-panStart.y}
                    self.viewPort.panRelative(panTranslate,panVector)
                }
                       
            },
            mouseUp: function(sender, evt)
            {       
                if(panStart!=null){
                    panStart=null
                    panTranslate=null
                }   
             
                if(mxEvent.isRightMouseButton(evt.evt))
                {                                              
                    if(contextMenuArmed)
                    {
                        var cell=self.graph.getCellAt(evt.graphX,evt.graphY);    
                        var cellState = self.graph.view.getState(cell);                  
                        var target={};
                        target.editorId=self.graphController.model.editorId;
                        target.DOM=cellState?cellState.shape.node:null
                        target.isGraphObject=false;  
                        target.isVertex=false;
                        target.isEdge=false;        
                        target.graphObject=null;
                        target.originalEvent=evt
                                                
                        if(cell)
                        {
                            target.isCanvas=false    
                            target.graphObject=cell.value;   
                            target.isGraphObject=true;
                            target.isVertex=cell.value instanceof Vertex;
                            target.isEdge=cell.value instanceof Edge;
                            target.eObject=target.graphObject.getEObject();     
                            if(target.isVertex)
                            {
                                target.position=cell.value.getPosition()
                            }        
                            if(target.isEdge)
                            {
                                target.edgeSource=cell.source.value
                                target.edgeTarget=cell.target.value
                            }
                        }
                        else
                        {
                            target.DOM=null
                            target.isCanvas=true
                            target.eObject=self.graphController.eObject;        
                        }
                        
                        self.eventBroker.publish('XGEE/CONTEXTMENU',{event:evt.evt,target:target}) //maybe we should get rid of this nested event later (anti-pattern?)
                    }
                    evt.consume();
                }
            },  
        });




        //Event for handling new edge connections

        this.graph.connectionHandler.addListener(mxEvent.CONNECT, function(sender, evt)
        {
            var cell = evt.getProperty('cell');
            self.graph.removeCells([cell]);  
            var source = self.graph.getModel().getTerminal(cell, true);
            var target = self.graph.getModel().getTerminal(cell, false);
            self.graphController.createEdge(source,target);      
            return true;
        }
        );

        
        this.graph.getEdgeValidationError = function(edge, source, target)
        {       
            if(!self.graphController.canCreateEdge(source,target))
            {
                return 'Invalid Edge Defintion';
            }       
          return mxGraph.prototype.getEdgeValidationError.apply(this, arguments);
        }


        this.graph.isCellSelectable = function(cell){        
            return !(cell.value instanceof Label) 
        }

        //On Press of DEL Key, remove the cell from its parent. The action should also be model-defined in the future.
        var keyHandler = new mxKeyHandler(this.graph);
        keyHandler.bindKey(46, function(evt)
        {
            if (self.graph.isEnabled())
            {					
                var selectedCells=self.graph.getSelectionCells();
                
                for (let cell of selectedCells)
                {
                    if(cell.value.isDeletable && cell.value.isDeletable())
                    {
   
                        
                        if(cell.value instanceof Edge)
                        {
                            cell.value.delete(cell.source.value,cell.target.value)
                        }
                        else
                        {
                            cell.value.delete()
                        }
                        
                       
                        
                    }
                }
            }
            self.graph.getSelectionModel().clear();
        });



        
        //register graph validation function
        this.graph.isValidDropTarget=function(targetCell,dropCells,evt)
        {           
            if(targetCell)
            if(targetCell.value)
            {
                var isDroppable=dropCells.map(function(dropCell){
                    return self.graphController.isDroppable(targetCell.value.eObject,null,dropCell.value.eObject);
                })
                var res=true;
                isDroppable.forEach(function(droppable){
                    res=res&&droppable
                });            
                return res;
            }
            else
            {
                return false;
            }
        }
        


    this.graph.graphHandler.moveCells = function(cells, dx, dy, clone, target, evt)
    {


        if (clone)
        {
            cells = this.graph.getCloneableCells(cells);
        }
        
        // Removes cells from parent
        if (target == null && this.isRemoveCellsFromParent() &&
            this.shouldRemoveCellsFromParent(this.graph.getModel().getParent(this.cell), cells, evt))
        {
            target = this.graph.getDefaultParent();
        }
        
        if(target)
        {
            //capture the move if there is a new target specified
            var allDroppable=true;
            var cellsDroppable=cells.map(function(dropCell){
                return self.graphController.isDroppable(target.value.eObject,null,dropCell.value.eObject);
            })
            cellsDroppable.forEach(function(droppable){
                allDroppable=allDroppable&&droppable
            });

            if(allDroppable)
            {
                cells.forEach(function(dropCell){
                    self.graphController.drop(target.value.eObject,null,dropCell.value.eObject);
                })
            }

        }
        else
        {
            //execute the move
  
            // Cloning into locked cells is not allowed
            clone = clone && !this.graph.isCellLocked(target || this.graph.getDefaultParent());
            
            // Passes all selected cells in order to correctly clone or move into
            // the target cell. The method checks for each cell if its movable.
            cells = this.graph.moveCells(cells, dx - this.graph.panDx / this.graph.view.scale,
                    dy - this.graph.panDy / this.graph.view.scale, clone, target, evt);
            
            if (this.isSelectEnabled() && this.scrollOnMove)
            {
                this.graph.scrollCellToVisible(cells[0]);
            }
                    
            // Selects the new cells if cells have been cloned
            if (clone)
            {
                this.graph.setSelectionCells(cells);
            }
        }
    };

    

   
        //Register own graphView with the mxGraph 
        this.graph.graphView=this;

        this.viewPort=new GraphViewPort($(editorDOM).find("g").get(0),$(editorDOM).width(),$(editorDOM).height())


        this.outline=new GraphViewPortOutline(this.viewPort,outlineDOM)
    }


    init(){

        var self=this

        //Listener for double click on cells
        this.graph.addListener(mxEvent.DOUBLE_CLICK,function(sender,evt){
            var cell = evt.getProperty("cell");
            if(cell)
            {
                var cellState = self.graph.view.getState(cell);
                if(cellState)
                {                  
                    self.eventBroker.publish('PROPERTIESVIEW/OPEN',{eObject:cell.value.eObject,DOM:cellState.shape.node})
                }
            }
        })

        
        //Listener for the selection of cells for updating the selection provider
        this.graph.getSelectionModel().addListener(mxEvent.CHANGE, async function(sender, evt)
        {
           try{
                var nElements = sender.cells.length
                if(nElements>0) {
                    var elements = [];
                    for(var i=0;i<nElements;i++) {
                        if(sender.cells[i].value)
                        {
                            if(!(sender.cells[i].value instanceof Label)) elements.push(sender.cells[i].value.getEObject());                    
                        }
                    }
                    if(self.graphController.paletteController.activeTool && self.graphController.paletteController.activeTool.isSelectionTool && await self.graphController.paletteController.activeTool.canUse(elements))
                    {
                        self.graphController.paletteController.activeTool.applyTo(elements)
                    }
                    else
                    {
                        var domElement = null; 
                        var cellState = self.graph.view.getState(sender.cells[0]);
                        if(cellState)
                        {
                            var domElement = cellState.shape.node;
                            let changeEvent = new eventBroker.SelectionChangedEvent(self,elements,domElement);
                            self.eventBroker.publish("SELECTION/CHANGE",changeEvent);
                        }
                    }
                }
            }
            catch(e)
            {
                console.error('Selection failed: '+e)
            }
        });

        //Events for changing vertex positions and sizes
        this.graph.model.addListener(mxEvent.CHANGE, function(sender, evt)
        {
          var changes = evt.getProperty('edit').changes;
          changes.forEach(function(change){
            
            if(change.cell)
            {                    
                if(change.cell.vertex && change.geometry)
                {                           
                     
                    
                    if( change.geometry.relative )
                    {        
                        let offsetX=0
                        let offsetY=0                    
                        if(change.geometry.offset)
                        {
                            offsetX=change.cell.value.parent.getRelativeX(change.geometry.offset.x)
                            offsetY=change.cell.value.parent.getRelativeY(change.geometry.offset.y)
                        }            
                        change.cell.value.moveTo(Math.min(1,Math.max(0,change.geometry.x+offsetX)),Math.min(1,Math.max(0,change.geometry.y+offsetY)));

                    }
                    else
                    {
                        //Absolute positioning
                        if((change.geometry.x!=change.previous.x) || (change.geometry.y!=change.previous.y))
                        {
                           // self.graphController.model.layout.setVertexPosition(change.cell.value,change.geometry.x,change.geometry.y)
                            change.cell.value.moveTo(change.geometry.x,change.geometry.y);                   
                        }                      
                    }


                    if((change.geometry.width!=change.previous.width) || (change.geometry.height!=change.previous.height))
                    {                       
                        //self.graphController.model.layout.setVertexPosition(change.cell.value,change.geometry.width,change.geometry.height)
                        change.cell.value.resize(change.geometry.width,change.geometry.height);                 
                    } 
           
                }

                if(change.cell.edge)
                {      
                    if(change.cell.value)
                    {
                        change.cell.value.setSupportPoints(change.cell.geometry.points)                 
                    }    
                }
            }
          })                 
        });

        this.graph.addListener(mxEvent.CLICK, function(sender, evt){
            var event = evt.getProperty('event')
            var location=self.viewPort.toOriginalCoordinate({x:event.layerX,y:event.layerY})
            self.lastClickLocation=Object.assign({},location)
            //Propagate click of labels to parent
            var cell = evt.getProperty('cell'); // cell may be null
     
            if (cell != null) {    
                if(cell.value instanceof Label)
                {                           
                    self.graph.selectCellForEvent(cell.parent,evt)                      
                }               
            }
            else
            {
         
                    var selectedCells=self.graph.getSelectionCells();
                    if(selectedCells.length == 1 && selectedCells[0].value instanceof Edge)
                    {                     
                        let edge=selectedCells[0]
                        let state=self.graph.view.getState(edge)            
                      
                        //Remove edge support point
                        if(event.altKey)
                        {           
                          
                            let geo = self.graph.model.getGeometry(edge);
                       
                  
                            if(geo.points != null)
                            {                                                      
                                let dNearestPoint=1000;
                                let nearestPoint=null
                                for(let point of geo.points)
                                {
                                    let d=Math.sqrt(Math.pow(point.x-location.x,2)+Math.pow(point.y-location.y,2))
                                    if(d<dNearestPoint)
                                    {
                                        nearestPoint=point
                                        dNearestPoint=d
                                    }
                                }

                                if(nearestPoint)
                                {
                                    geo.points.splice(geo.points.indexOf(nearestPoint),1)
                                    self.graph.model.setGeometry(edge, geo);
                                    edge.value.setSupportPoints(geo.points) //seems to be necessary because CHANGE event not fired by mxGraph
                                    self.graph.refresh(edge)                           
                                }                      
                                
                            }              
                            evt.consume()
                        }

                        //Add edge support point  
                        if(event.ctrlKey)
                        {               
                            let idx=mxUtils.findNearestSegment(state, location.x,location.y)
                            let geo = self.graph.model.getGeometry(edge);

                            geo = geo.clone();
                            if(!geo.points)
                            {
                                geo.points=[new mxPoint(parseInt(location.x),parseInt(location.y))]
                            }    
                            else
                            {                               
                                geo.points.splice(idx,0,new mxPoint(parseInt(location.x),parseInt(location.y)))
                            }                     

                            self.graph.model.setGeometry(edge, geo);               
                            self.graph.refresh(edge)
                            evt.consume()
                        }

                        
                     
                    }
                
            }

        })

        this.graph.addListener(mxEvent.DOUBLE_CLICK, function(sender, evt){       
            //Propagate click of labels to parent
            var cell = evt.getProperty("cell"); // cell may be null
            if (cell != null) {
                if(cell.value instanceof Label)
                {
                    document.getElementById('uuid::'+cell.getParent().id).dispatchEvent(new MouseEvent('dblclick'))
                    evt.consume()
                }     
            }   
            

        })


        //Install viewport listeners
        this.viewPort.onZoom((scale) => {
            self.graphController.model.layout.setScale(scale)  
        })

        this.viewPort.onPan((translate) => {
            self.graphController.model.layout.setTranslate(translate.x,translate.y)  
        })


    }



    _initializeGraph(editorDOM,outlineDOM)
    {
      	var self=this	
        // Checks if the browser is supported
        if (!mxClient.isBrowserSupported())
        {
            // Displays an error message if the browser is not supported.
            mxUtils.error('Browser is not supported!', 200, false);
        }
        else
        {				
            // Enables guides
            mxGraphHandler.prototype.guidesEnabled = true;
            
            // Alt disables guides
            mxGuide.prototype.isEnabledForEvent = function(evt)
            {
                return mxEvent.isAltDown(evt);
            };
            
            // Enables snapping waypoints to terminals
            mxEdgeHandler.prototype.snapToTerminals = true;
            
            mxEvent.disableContextMenu(document.body);
            
            // Creates the graph inside the given container                
            var model = new mxGraphModel();
            model.maintainEdgeParent=false;
            var graph = new mxGraph(editorDOM, model);            
                    
            graph.setPanning(false);
            graph.disconnectOnMove = false;
            graph.foldingEnabled = false;
            graph.cellsResizable = true;
            graph.cellsMovable = true;
            
            graph.extendParents = false;
            graph.setConnectable(true);
            graph.setAllowDanglingEdges(false);
            graph.graphHandler.setRemoveCellsFromParent(false);
            graph.setDropEnabled(true);

            graph.setConstrainChildren(true);
            graph.setConstrainRelativeChildren(true);
            
            var style = graph.getStylesheet().getDefaultEdgeStyle();
            style['strokeColor'] = '#000000';
            style['strokeWidth'] =4;
                   
            
            var parent = graph.getDefaultParent();
            


            //Disable auto-scroll, disable auto-extend
            graph.autoScroll=false
            graph.autoExtend=false
            graph.allowAutoPanning=false

            
            //Prevents graph panning
            mxPanningHandler.prototype.panningEnabled=false

            //Preserve Edge Style on auto-arrange (circle)
            mxCircleLayout.prototype.disableEdgeStyle=false;
            
            //Prevents the rubberband to be active on right mouse button
            mxRubberband.prototype.mouseDown = function(sender, me)
            {
                if (!me.isConsumed() && this.isEnabled() && this.graph.isEnabled() &&
                    me.getState() == null && !mxEvent.isMultiTouchEvent(me.getEvent()) && !mxEvent.isRightMouseButton(me.getEvent()))
                {
                    var offset = mxUtils.getOffset(this.graph.container);
                    var origin = mxUtils.getScrollOrigin(this.graph.container);
                    origin.x -= offset.x;
                    origin.y -= offset.y;
                    this.start(me.getX() + origin.x, me.getY() + origin.y);

                    // Does not prevent the default for this event so that the
                    // event processing chain is still executed even if we start
                    // rubberbanding. This is required eg. in ExtJs to hide the
                    // current context menu. In mouseMove we'll make sure we're
                    // not selecting anything while we're rubberbanding.
                    me.consume(false);
                }
            };

            //Coordinate transformation for viewport
            mxRubberband.prototype.execute = function(evt)
            {
                if(this.graph.graphView)
                {
                    let pt=this.graph.graphView.viewPort.toOriginalCoordinate({x:this.x,y:this.y})
                    this.x=pt.x
                    this.y=pt.y
                    this.width/=this.graph.graphView.viewPort.getScale()
                    this.height/=this.graph.graphView.viewPort.getScale()
                }
                var rect = new mxRectangle(this.x, this.y, this.width, this.height);
                this.graph.selectRegion(rect, evt);
            };




            // Enables rubberband selection
            new mxRubberband(graph);
                            
            //Disables Editing of cells labels
            graph.setCellsEditable(false);
            
           
            // Disables built-in DnD in IE (this is needed for cross-frame DnD, see below)            
            if (mxClient.IS_IE)
            {
                 mxEvent.addListener(img, 'dragstart', function(evt) {   evt.returnValue = false; });
            }	

            //Initialize Outline
            //var outlineContainer = document.getElementById('outlineCanvas'+tab.name);
            //outline = new mxOutline(graph, outlineDOM);

            
            // Implements perimeter-less connection points as fixed points (computed before the edge style).
            graph.view.updateFixedTerminalPoint = function(edge, terminal, source, constraint)
            {
                mxGraphView.prototype.updateFixedTerminalPoint.apply(this, arguments);
                
                var pts = edge.absolutePoints;
                var pt = pts[(source) ? 0 : pts.length - 1];

                if (terminal != null && pt == null && this.getPerimeterFunction(terminal) == null)
                {
                    edge.setAbsoluteTerminalPoint(new mxPoint(this.getRoutingCenterX(terminal),
                            this.getRoutingCenterY(terminal)), source)
                }
            };
            
            // Changes the default edge style
            graph.getStylesheet().getDefaultEdgeStyle()['edgeStyle'] = 'orthogonalEdgeStyle';
            
            delete graph.getStylesheet().getDefaultEdgeStyle()['endArrow'];
            
            // Implements the connect preview
            graph.connectionHandler.createEdgeState = function(me)
            {
                var edge = graph.createEdge(null, null, null, null, null);
                
                return new mxCellState(graph.view, edge, graph.getCellStyle(edge));
            };
            
            // Overridden to define per-shape connection points
            mxGraph.prototype.getAllConnectionConstraints = function(terminal, source)
            {
                if (terminal != null && terminal.shape != null)
                {
                    if (terminal.shape.stencil != null)
                    {
                        if (terminal.shape.stencil != null)
                        {
                            return terminal.shape.stencil.constraints;
                        }
                    }
                    else if (terminal.shape.constraints != null)
                    {
                        return terminal.shape.constraints;
                    }
                }
        
                return null;
            };
     
            /*
                            function(cell)

            {

                var geometry = this.model.getGeometry(cell);

                

                return this.isCellsLocked() || (geometry != null && this.model.isVertex(cell) && geometry.relative);

            }
            */

            graph.isCellLocked=function(cell)
            {
                return this.isCellsLocked();
            }


          
            

            //End of Mouse Interaction		
        }
        return graph;
    }

    /**
     * Returns the current graph selection as eObjects
     *  @return {Array} An array containing the selected eObjects.
    */
    getCurrentGraphSelection(){
        var selectionCells=this.graph.getSelectionCells()
        return selectionCells.map( (c) => { return c.value.getEObject() })
    }

    /**
     * Clears the graph selection  
    */
    clearSelection(){
        this.graph.clearSelection()
    }

    /**
    *   Sets the scale of the view. The default scale is 1.00.
    */
    setScale(scale=1)
    {
        this.graphController.model.layout.setScale(scale)
    }

    /**
    *   Sets the translate of the view. The default translate is x=0, y=0
    */
    setTranslate(translate={x:0,y:0}){
        this.graphController.model.layout.setTranslate(translate.x,translate.y)  
    }


    /**
    *   Captures and saves the current layout
    */
    captureLayout()
    {        
        var self=this;
        this.graphController.model.layout.setScale(this.viewPort.getScale())  
        var translate=this.viewPort.getTranslate();    
        this.graphController.model.layout.setTranslate(translate.x,translate.y)   
        var allDisplayed=this.getDisplayedItems();
        allDisplayed.forEach(function(e){
            let cell=self.graph.model.getCell(e.uuid);
            if(cell.vertex)
            {
                self.graphController.model.layout.setVertexPosition(e,cell.geometry.x,cell.geometry.y)
                self.graphController.model.layout.setVertexSize(e,cell.geometry.width,cell.geometry.height)
            }
        })

        
    }


    /**
    *   Adds a container to the graph.
    *   @param {container} container - The container graph object. 
    */
    addContainerToGraph(container)
    {
        let parentCell=null;
        var isRelative=false;

        if(container.parent && container.parent.uuid) 
        {
            isRelative=true 
            parentCell=this.graph.model.getCell(container.parent.uuid+'.span(0)')
        }
        else
        {
            parentCell=this.graph.getDefaultParent()
        } 

        if(parentCell){      
            


            let cell=this.graph.insertVertex(parentCell, container.uuid, container, container.position.x, container.position.y, container.size.x, container.size.y,container.type.getStyle(),isRelative);
            cell.getGeometry().offset=new mxPoint(-container.size.x/2,-container.size.y/2);
      
            cell.setConnectable(false);  
   
            
            if(container.isResizable())
            {
                this.graph.setCellStyles(mxConstants.STYLE_RESIZABLE,'1',[cell]); 
            }
            else
            {
                this.graph.setCellStyles(mxConstants.STYLE_RESIZABLE,'0',[cell]); 
            }

            if(container.isMovable())
            {
                this.graph.setCellStyles(mxConstants.STYLE_MOVABLE,'1',[cell]); 
            }
            else
            {
                this.graph.setCellStyles(mxConstants.STYLE_MOVABLE,'0',[cell]); 
            }            
            
        }
        else
        {
            console.warn('Container with UUID:'+container.uuid+' could not be displayed, because the parent cell uuid:'+container.parent.uuid+' is invalid')
        }
    }

    /**
    *   Removes a container from the graph.
    *   @param {container} container - The container graph object. 
    */
    removeContainerFromGraph(container)
    {
        let cell=graph.model.getCell(container.uuid)
        if(cell)
        {
            this.graph.removeCells([cell]); 
        }
        else
        {
            throw 'Container with UUID:'+container.uuid+' is not in graph'
        }
    }

    /**
    *   Adds a vertex to the graph.
    *   @param {vertex} vertex - The vertex graph object. 
    */
    addVertexToGraph(vertex)
    {
        var self=this
        let parentCell=null;
        var isRelative=false;

        if(vertex.parent && vertex.parent.uuid) 
        {
            isRelative=true 
            parentCell=this.graph.model.getCell(vertex.parent.uuid)
        }
        else
        {
            parentCell=this.graph.getDefaultParent()
        }

        if(parentCell){        
            try{
                var cell=this.graph.insertVertex(parentCell, vertex.uuid, vertex, vertex.position.x, vertex.position.y, vertex.size.x, vertex.size.y,vertex.type.getStyle(),isRelative);
            }
            catch(e)
            {
                throw 'displaying vertex failed. reason:'+e
            }
            //cell.getGeometry().offset=new mxPoint(0,0);
      
            cell.setConnectable(false);  
            
            if(vertex.isResizable())
            {
                this.graph.setCellStyles(mxConstants.STYLE_RESIZABLE,'1',[cell]); 
            }
            else
            {
                this.graph.setCellStyles(mxConstants.STYLE_RESIZABLE,'0',[cell]); 
            }

            if(vertex.isMovable())
            {
                this.graph.setCellStyles(mxConstants.STYLE_MOVABLE,'1',[cell]); 
            }
            else
            {
                this.graph.setCellStyles(mxConstants.STYLE_MOVABLE,'0',[cell]); 
            }
           
            //Update view upon graph model changes
            var timeout = null;
            var timeoutInterval=100;
            var refreshTimer=function(){
                if(timeout){ clearTimeout(timeout);  }  timeout=window.setTimeout(function(){ self.refreshVertex(vertex); }, timeoutInterval);
            }
            vertex.on('MOVE',function(){
                 refreshTimer();                  
            });

            vertex.on('RESIZE',function(){
                 refreshTimer();       
            });

            //Track remote position
            this.graphController.model.layout.observeVertexPosition(vertex,function(pos){
                vertex.moveTo(pos.x,pos.y);
            });

            //Track remote size
            this.graphController.model.layout.observeVertexSize(vertex,function(size){
                vertex.resize(size.x,size.y);
            });
            
        }
        else
        {
            throw 'Vertex with UUID:'+vertex.uuid+' could not be displayed, because the parent cell uuid:'+vertex.parent.uuid+' is invalid'
        }
    }

    /**
    *   Removes a vertex from the graph.
    *   @param {vertex} vertex - The vertex graph object. 
    */
    removeVertexFromGraph(vertex)
    {
        let parent=null;
        if(vertex.parent!=this.graph.model)
        {   
            parent=vertex.parent
        }

        let cell=this.graph.model.getCell(vertex.uuid)
        if(cell)
        {
            this.graph.removeCells([cell]);     
        }
        else
        {
            throw 'Vertex with UUID:'+vertex.uuid+' is not in graph'
        }

        if(parent) this.refreshVertex(parent);

    }

    /**
    *   Sets a vertex connectable for tools.
    *   @param {vertex} vertex - The vertex graph object. 
    */
    setVertexConnectable(vertex)
    {
        let cell=this.graph.model.getCell(vertex.uuid)
        if(cell)
        {
            cell.setConnectable(true);
        }
        else
        {
            throw 'Vertex with UUID:'+vertex.uuid+' is not in graph'
        }
    }

    /**
    *   Sets a vertex not connectable for tools.
    *   @param {vertex} vertex - The vertex graph object. 
    */
    setVertexNotConnectable(vertex)
    {
        let cell=this.graph.model.getCell(vertex.uuid)
        if(cell)
        {
            cell.setConnectable(false);
        }
        else
        {
            throw 'Vertex with UUID:'+vertex.uuid+' is not in graph'
        }
    }

    /**
    *   Adds a label to the graph.
    *   @param {label} label - The label graph object. 
    */
    addLabelToGraph(label)
    {
        let parentCell=null;
        var isRelative=false;

        if(label.parent && label.parent.uuid) 
        {
            isRelative=true 
            parentCell=this.graph.model.getCell(label.parent.uuid)
        }
        else
        {
            parentCell=this.graph.getDefaultParent()
        }

        if(parentCell){    
            var labelPosition=label.getPosition();
            let cell = this.graph.insertVertex(parentCell, label.uuid, label, labelPosition.x, labelPosition.y, 0, 0, label.getStyle(), true);  
            cell.setConnectable(false);  
            
            if(label.isResizable())
            {
                this.graph.setCellStyles(mxConstants.STYLE_RESIZABLE,'1',[cell]); 
            }
            else
            {
                this.graph.setCellStyles(mxConstants.STYLE_RESIZABLE,'0',[cell]); 
            }

            if(label.isMovable())
            {
                this.graph.setCellStyles(mxConstants.STYLE_MOVABLE,'1',[cell]); 
            }
            else
            {
                this.graph.setCellStyles(mxConstants.STYLE_MOVABLE,'0',[cell]); 
            }            
        }
        else
        {
            throw 'Label with UUID:'+label.uuid+' could not be displayed, because the parent cell uuid:'+label.parent.uuid+' is invalid'
        }
   
    }

    /**
    *   Removes a label from the graph.
    *   @param {label} label - The label graph object. 
    */
    removeLabelFromGraph(label)
    {
        let cell=graph.model.getCell(label.uuid)
        if(cell)
        {
            this.graph.removeCells([cell]); 
        }
        else
        {
            throw 'Label with UUID:'+label.uuid+' is not in graph'
        }
    }

    /**
    *   Adds an edge to the graph.
    *   @param {edge} edge - The edge graph object. 
    */
    addEdgeToGraph(edge)
    {
  
        let parentCell=null;
        if(edge.parent && edge.parent.uuid) 
        {
            parentCell=this.graph.model.getCell(edge.parent.uuid)
        }
        else
        {
            parentCell=this.graph.getDefaultParent()
        }

        let edgeSpans=edge.getEdgeSpans()
        let spanCount=edgeSpans.length
        let edgeSpanId=0
        for(let edgeSpan of edgeSpans)
        {
            let sourceAnchor=edgeSpan.source
            let targetAnchor=edgeSpan.target;


            var source=null;
            var target=null;

            if(sourceAnchor)
            {
                source=this.graph.model.getCell(sourceAnchor.getUUID());
            }
            
            if(targetAnchor)
            {
                target=this.graph.model.getCell(targetAnchor.getUUID());
            }
                
            if(source && target)
            {            

                let cell=this.graph.insertEdge(parentCell, edge.uuid+'.span('+edgeSpanId+')', edge, source, target,edge.getStyle(sourceAnchor,targetAnchor));
                let supportPoints=edge.getSupportPoints()
                let geo=cell.geometry.clone()
                geo.points=[]
                for(let supportPoint of supportPoints)
                {
                    geo.points.push(new mxPoint(supportPoint.x,supportPoint.y)) //INTEGER?
                }     
                this.graph.model.setGeometry(cell,geo)          
     
            }
            else
            {
                if(!source)
                {
                    console.warn('Edge can not be displayed because source is not present. total anchor count='+edge.anchors.length)

                }

                if(!target)
                {
                    console.warn('Edge can not be displayed because target is not present total anchor count='+edge.anchors.length)
                }

        
            }
            edgeSpanId+=1
        }
       
    }

    /**
    *   Removes an edge from the graph.
    *   @param {edge} edge - The edge graph object. 
    */
    removeEdgeFromGraph(edge)
    {
        let cellUUIDs=Object.keys(this.graph.model.cells).filter( (cellUUID) => { return cellUUID.includes(edge.uuid) }) 
        let cells=cellUUIDs.map((uuid) => { return this.graph.model.getCell(uuid)}).filter( (cell) => { return cell?true:false })     
        this.graph.removeCells(cells);           
    }

    /**
    *   Refreshes a vertex and its subvertices.
    *   @param {vertex} vertex - The vertex graph object. 
    */
    refreshVertex(vertex)
    {
        var self=this
        if(this.isDisplayed(vertex.uuid)){
  
            //Refresh vertex display state
            let cell=this.graph.model.getCell(vertex.uuid)
      
            var geometry=cell.getGeometry().clone();
            
            if(geometry.relative)
            {                
                geometry.x=vertex.position.x
                geometry.y=vertex.position.y  
                geometry.offset=new mxPoint(0,0)     
            }
            else
            {   
                if(geometry.offset)
                {
                    geometry.offset.x=vertex.position.x
                    geometry.offset.y=vertex.position.y
                }
            }
            geometry.width=vertex.size.x;
            geometry.height=vertex.size.y;          
            self.graph.model.setGeometry(cell,geometry);   
    
    
            //Update subvertex positions
            vertex.vertices.forEach(function(v){
                let cell=self.graph.model.getCell(v.uuid)
                if(cell)
                {
                    var geometry=cell.getGeometry().clone();
                    geometry.x=v.position.x
                    geometry.y=v.position.y          
                    self.graph.model.setGeometry(cell,geometry);                
                }        
            });

            self.graph.refresh(); 
        }    
    }

    /**
    *   Refreshes multiple vertices and their subvertices.
    *   @param {Array} vertices - The vertex graph objects. 
    */
   refreshVertices(vertices)
   {
       var self=this
       this.graph.model.beginUpdate()
       vertices.forEach( (vertex) => {
                if(this.isDisplayed(vertex.uuid)){
                    //Refresh vertex display state
                    let cell=this.graph.model.getCell(vertex.uuid)
                    var geometry=cell.getGeometry().clone();
                    geometry.x=vertex.position.x
                    geometry.y=vertex.position.y       
                    geometry.width=vertex.size.x;
                    geometry.height=vertex.size.y;          
                    self.graph.model.setGeometry(cell,geometry);   
            
            
                    //Update subvertex positions
                    vertex.vertices.forEach(function(v){
                        let cell=self.graph.model.getCell(v.uuid)
                        if(cell)
                        {
                            var geometry=cell.getGeometry().clone();
                            geometry.x=v.position.x
                            geometry.y=v.position.y          
                            self.graph.model.setGeometry(cell,geometry);                
                        }        
                    });

                }   
        })
     this.graph.model.endUpdate()    
   }

    /**
    *   Waits asynchronously for a graph object with the given UUID to be dispayed.
    *   @async
    *   @param {UUID} uuid - The uuid of a graph object. 
    *   @return {Promise} Promise object representing a boolean, that indicates wether the graph object identified by the uuid is displayed.
    */
    async isAsyncDisplayed(uuid)
    {
        var self=this
        if(this.graph.getCell(uuid))
        {
            return true
        }
        else
        {
            await new Promise(function(resolve,reject){
                var callback=function(){
                    if(self.graph.getCell(uuid))
                    {
                        self.graph.removeListener(mxEvent.CELLS_ADDED,this);
                        resolve(true);
                    }
                }
                self.graph.addListener(mxEvent.CELLS_ADDED,callback);
            });
        }
    }

    /**
    *   Checks wether a graph object with the given UUID is dispayed.
    *   @param {UUID} uuid - The uuid of a graph object. 
    *   @return {boolean} A boolean, that indicates wether the graph object identified by the uuid is displayed.
    */
    isDisplayed(uuid)
    {
        //TODO: Does not work for edges anymore!
        if(this.graph.model.getCell(uuid))
        {
            return true
        }
        else
        {
            return false
        }
    }

    
    /**
    *   Checks wether an edge is displayed.
    *   @param {edge} edge - The edge graph object. 
    *   @return {boolean} A boolean, that indicates wether edge is displayed.
    */
    isEdgeDisplayed(edge){
        let res=Object.keys(this.graph.model.cells).filter( (cellUUID) => { return cellUUID.includes(edge.uuid) }).length?true:false
        return res
    }


    /**
    *   Returns all displayed graph objects.
    *   @return {Array} An array containg the displayed graph objects.
    */
    getDisplayedItems()
    {
        var self=this;
        var modelIndex=self.graphController.model.getIndex();
        var allDisplayed=[];
        for(const [uuid,item] of modelIndex)
        {
            if(self.isDisplayed(uuid))
            {
                allDisplayed.push(item);
            }
        }
        return allDisplayed;
    }

    /**
    *   Returns the graph object, that has been added last to the view
    *   @return {GraphObject} The last displayed graph object.
    */
    getLastDisplayedItem(){
        var res=null;
        var self=this;
        var modelIndex=self.graphController.model.getIndex();
        var allItems=Array.from(modelIndex).reverse();
        for(let i=0; i<=allItems.length; i++)
        {
            if(self.isDisplayed(allItems[i][0]))
            {
                res=allItems[i][1];
                break;
            }
        }
        return res;
    }

    /**
    *   Returns the DOMelement of a graph object identified by its UUID
    *   @return {DOMelement} The DOMelement of the graph object.
    */
    getItemDOM(uuid){
        var res=null;
        res=document.getElementById("uuid::"+uuid)
        return res;
    }

    /**
    *   Returns all undisplayed graph objects.
    *   @return {Array} An array containg the undisplayed graph objects.
    */
    getUndisplayedItems()
    {
        var self=this;
        var modelIndex=self.graphController.model.getIndex();
        var allNotDisplayed=[];
        modelIndex.forEach((item) => {
            if(!self.isDisplayed(item.uuid)){
                allNotDisplayed.push(item);
            }
        })
        return allNotDisplayed;
    }

    /**
    *   Returns all undisplayed edges.
    *   @return {Array} An array containg the undisplayed edges.
    */
    getUndisplayedEdges(){
        var self=this;
        var modelIndex=self.graphController.model.getIndex();
        var allNotDisplayedEdges=[];
        modelIndex.forEach((item) => {
            if(!self.isDisplayed(item.uuid+'.span(0)')){
                if(item instanceof Edge){
                    allNotDisplayedEdges.push(item);
                }
            }
        })
        return allNotDisplayedEdges;
    }

    /**
    *   Enables automatic refreshes of all graph objects, when graph objects are added/removed to/from the graph. Auto refresh is disabled by default.
    */
    enableAutoRefresh()
    {
        this.autoRefresh=true;
    }    

    /**
    *   Disables automatic refreshes of all graph objects, when graph objects are added/removed to/from the graph. Auto refresh is disabled by default.  
    */
    disableAutoRefresh(){
        this.autoRefresh=false;
    }

    /**
    *   Resets the view's viewport to the scale/translate currently stored in the model's layout data
    *   @async
    */
    async reset()
    {  
        this.viewPort.setScale(await this.graphController.model.layout.getScale())
        this.viewPort.setTranslate(await this.graphController.model.layout.getTranslate())    
    }

    /**
    *   Refreshes a graph object identified by its UUID. If the graph object does not exist, this does nothing.
    */
    refresh(uuid){
        let cell=this.graph.model.getCell(uuid);
        if(cell)
        {
            this.graph.refresh(cell)
        }
    }

    /**
    *   Refreshes the display and attempts to display previously undisplayed edges. Usually called when new vertices are added to the graph.
    */
    refreshDisplay(){    
        var self=this;
        var undisplayedEdges=this.getUndisplayedEdges();
        undisplayedEdges.forEach(function(edge){
            self.addEdgeToGraph(edge);
        })
    }

    /**
    *   Highlights graph objects with a certain color. The default color is red (#FF00000).
    *   @param {Array} graphObjects - An array containg the graph objects to be highlighted. 
    *   @param {string} color - The hex notation of the color as a string including the leading '#'
    *   @returns {function} A callback function that removes the highlight from the graph.
    */
    highlight(graphObjects,color='#FF0000'){
        let highlights=[]
        let destroyHighlight=() => {
            highlights.forEach( highlight => highlight.destroy() )
        }
        
        graphObjects.forEach((graphObject=>{
            if(graphObject.uuid != null)
            {
                let cell=this.graph.model.getCell(graphObject.getUUID());
                var highlight = new mxCellHighlight(this.graph, color, 2);
                highlight.highlight(this.graph.view.getState(cell))              
                highlights.push(highlight)
            }
        }))

        return destroyHighlight
    }

}


/** GraphView integration into mxGraph
 *  Replaces mxGraph functions for XGEE viewport. Integrates XGEE viewport coordinate transformation.
 */      

 mxUtils.convertPoint=function(container,x,y)
 {
     let activeViewport=$app.viewManager.activeView.XGEEInstance.graphView.viewPort
     var origin = mxUtils.getScrollOrigin(container, false);
     var offset = mxUtils.getOffset(container);
     offset.x -= origin.x;
     offset.y -= origin.y;
     let pt=activeViewport.toOriginalCoordinate({x:x-offset.x,y:y-offset.y})
     return new mxPoint(pt.x,pt.y);
 }
 
 mxGraph.prototype.scrollRectToVisible = function(rect)
 {               
     let activeViewport=$app.viewManager.activeView.XGEEInstance.graphView.viewPort
     activeViewport.adjustViewToRegion(rect.x,rect.y,rect.width,rect.height)
 }

export default GraphView