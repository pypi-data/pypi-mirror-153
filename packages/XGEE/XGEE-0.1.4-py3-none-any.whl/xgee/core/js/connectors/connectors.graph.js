var GraphConnector=function(EObject,editor,tab,resourceProvider)
{
    var self=this;
    this.palette=null;
    this.EObject=EObject;
    this.editor=editor;
    this.resourceProvider = resourceProvider;
    this.eventBroker = $app.plugins.require('eventBroker');//should better be an argument if this is located in a plugin

    this.graphModel=null;
    this.graph=null;
    /*
    var layoutsDirectory=workspace.getContents().find(function(e){ return e.name==".layouts" && e.isDirectory; }); 
    this.layout=new GraphLayout(layoutsDirectory.getContents().find(function(e){return e.name=="workspace.layout" && e.isResource}),EObject);
    */
    this.presentation=null;


    this.__selectionProvider=selectionProvider;
    this.__itemRegistry=[];
    //this.__tree=new TreeConnector("#0","Workspace"); //BA: not necessary any more since there is only one tree for all views 
    this.__selection=new SelectionConnector(this.__selectionProvider,tab.name); 
    this.__ignoreSelectionEvent=false;
    this.tab=tab; //BA: is never used later?
    this.__selectionProvider.subscribe(function(selection){       
         var cells=graph.getChildCells(graph.getDefaultParent());      
         self.__ignoreSelectionEvent=true;
         self.__graph.clearSelection();         
         for(let i in cells)
         {
             if(cells[i].value)
             {
                 if(compareEObjects(cells[i].value.__eObject,selection.eObject))
                 {
                    self.__ignoreSelectionEvent=false;   
                    self.__graph.setSelectionCell(cells[i]);
                    break;
                 }
             }
         }
         self.__ignoreSelectionEvent=false;   
    });





    var CanvasContextMenu=function(dataConnector)
    {
        var dataConnector=dataConnector;
        var self=this;
        this.isArmed=false;
        this.arm=function()
        {
            self.isArmed=true;
        }
        this.disarm=function()
        {
            self.isArmed=false;
        }
        this.cell=null;
        this.build=function($triggerElement, e){
            if(self.cell)
            {                
                var items= {delete: {name: "Delete",icon:"delete", action:function(){ self.cell.value.onDelete(); }},toConsole: {name: "to console", action:function(){ console.log(self.cell); }}};
                return {  callback:  function(itemKey,opt){items[itemKey].action.apply();}, items: items }               
            }
            else
            {
                var items= {refresh: {name: "Refresh", action:function(){ dataConnector.refresh(); }}};
                return {  callback:  function(itemKey,opt){items[itemKey].action.apply();}, items: items }           
            }
        };        
    };

    this.__contextMenu=new CanvasContextMenu(this);

    this.init=function(graph,selectionContainer=null)
    {

        self.__graph=graph;
        graph["_connector"]=self;
        graph.getSelectionModel().addListener(mxEvent.CHANGE, function(sender, evt)
        {
            if(!self.__ignoreSelectionEvent)
            {
                var cell = self.__graph.getSelectionCell();
                if(cell)
                {
                    if(cell.value)
                    {
                        self.__selectionProvider.setSelection({eObject:cell.value.__eObject,feature:null});
                    }
                }
                else
                {
                        self.__selectionProvider.setSelection({eObject:self.EObject,feature:null});
                }

                //BA: add $apps change listener
                {
                    var nElements = sender.cells.length
                    if(nElements>0) {
                        var elements = [];
                        for(var i=0;i<nElements;i++) {
                            if(sender.cells[i].value)
                            {
                            elements.push(sender.cells[i].value.__eObject);
                            }
                        }
                        var geometry = sender.cells[0].getGeometry(); //take the first cell as origin
                        var domElement = null; 
                        var cellState = self.__graph.view.getState(sender.cells[0]);
                        if(cellState)
                        {
                            var domElement = cellState.shape.node;
                            //depricated
                            // $app.selectionManager.SetSelection(new jsa.Selection({
                            //     elements: elements,
                            //     eventSource: this,
                            //     domElement: domElement
                            // })); 

                            //TODO: intermediate solution. This should be part of the graph plugins
                            let changeEvent = new eventBroker.SelectionChangedEvent(self,elements,domElement);
                            self.eventBroker.publish("SELECTION/CHANGE",changeEvent);
                        }
                    }
                }
                //end BA added
            }
        });

        graph.connectionHandler.addListener(mxEvent.CONNECT, function(sender, evt)
        {
            var cell = evt.getProperty('cell');
            self.__graph.removeCells([cell]);  
            var source = graph.getModel().getTerminal(cell, true);
            var target = graph.getModel().getTerminal(cell, false);
            //var tool=self.palette.getActiveTool();
            if(tool)
            { 
                tool.onCreate(source,target);
               
            }
            return true;
        }
        );

        
        graph.getEdgeValidationError = function(edge, source, target)
        {          
          //var tool=self.palette.getActiveTool();
          if(tool)
          { 
            if(!tool.isValid(edge,source,target))
            {
                return 'Invalid Edge Defintion';
            }
          }

          return mxGraph.prototype.getEdgeValidationError.apply(this, arguments);
        }

        self.__selection.setContainer(selectionContainer);
    


        

        self.paletteController=new PaletteController(editor.get("palette"),ecoreSync.proxy.unproxy(self.EObject),domContainer)
        self.paletteController.init();


        self.graphController=graphControllerFactory.createGraphController(editor,new GraphViewX(self.graph),ecoreSync.proxy.unproxy(self.EObject))  
        
        self.graphController.on('initBegin',function(){
            $app.splash.Show();
        });

        self.graphController.on('initEnd',function(){
            $app.splash.Hide();
        });

        self.graphController.init();  
        
        

    };

    this.addItem=function(item)
    {
        self.__itemRegistry.push(item);
    }

    this.removeItem=function(item)
    {
        self.__itemRegistry.splice(self.__itemRegistry.indexOf(item),1);
    }

    this.getItem=function(EObject)
    {
       let item=self.__itemRegistry.find(function(e){return e.__eObject.get("_#EOQ")==EObject.get("_#EOQ");});
       return item;
    };

    this.filterItems=function(func)
    {
        let items=self.__itemRegistry.filter(func);
        return items;
    }

    this.refresh=function()
    {
            setTimeout(function(){self.presentation.refresh()},0);;
    }

    this.refreshNow=function()
    {
            setTimeout(function(){self.presentation.refreshNow()},0);;
    }

    this.refreshAllItems=function()
    {
        for(let i in self.__itemRegistry)
        {
            self.__itemRegistry[i].refresh();
        }
    }

    this.isInRegistry=function(EObject,parent=null)
    {   
        //Checks if an EObject is contained in the graph's item registry
        if(parent==null)
        {
            if(EObject)
            {
                if(self.__itemRegistry.find(function(e){return e.__eObject.get("_#EOQ")==EObject.get("_#EOQ") || e.__eObject.noproxy == EObject.noproxy;}))
                {
                    return true;
                }
            }
            else
            {
                return null;
            }
            return false;
        }
        else
        {

            if(EObject)
            {

                if(self.__itemRegistry.find(function(e){return compareEObjects(e.__eObject,EObject) && e.__cell.parent == parent.__cell}))
                {
                    return true;
                }
            }
            else
            {
                return null;
            }
            return false;

        }
    }


    this.createEventListeners=function()
    {

    };

   

    this.setConnectable=function(filterFunc,state)
    {
        //Sets the connectable state according to the state variable for the items that are found through the filter function
        var items=self.__itemRegistry.filter(filterFunc);
        for(let i in items)
        {
            items[i].__cell.setConnectable(state);
        }
    };

};
