//jsApplication integration library for XGEEInstance
//(C) 2020 Matthias Brunner

// XGEEInstance API




// XGEEInstance jsApplication Tab 

/* GRAPHLAYOUTCOMMAND*/
function GraphLayoutCommand(graph,layout,name) {
    jsa.CommandA.call(this);

    //members
    this.name = 'Layout: '+name;
    this.graph = graph;
    this.layout = layout;

    this.description = 'This is a command';

    return this;
};

GraphLayoutCommand.prototype = Object.create(jsa.CommandA.prototype);

GraphLayoutCommand.prototype.Do = function() {
    this.layout.execute(this.graph.getDefaultParent());
    return this;
};

GraphLayoutCommand.prototype.Undo = function() {
    //TODO: implement undo for graph layouts
    return this;
};

/* GRAPH RESOURCE PROVIDER */

function GraphResourceProvider(basePath) {
    this.basePath = basePath;

    this.resourceCache = new Map(); // do not load a resource twice
    return this;
};

GraphResourceProvider.prototype.LoadResource = function(path) {
    var realPath = this.basePath+path;
    if(this.resourceCache.has(realPath)) {
        return this.resourceCache.get(realPath);
    }
    var resource = this.__LoadResourceExternaly(realPath);
    this.resourceCache.set(realPath,resource);
    return resource;
};

GraphResourceProvider.prototype.__LoadResourceExternaly = function(path) {
	var xhttp = new XMLHttpRequest();
    xhttp.open("GET", path, false);
    try {
        xhttp.send();
    } catch {
        console.trace();
        console.error("Could not load resource: "+path);
        throw new Error("Could not load resource: "+path);
    }
	return xhttp.responseText;
};



function EditorTab(params,createDom=true) {
    jsa.View.call(this,params,false);

    //members
    this.editor = null;
    this.eObject = null;
    this.eResource = null; //will be obtained later if unknown
    this.layoutResource = null; //will be obtained later if unknown
    this.ecoreSync = null;

    this.pathStr = '?';
    this.objectClassName = '?';
    this.objectName = '?';

    this.onFocusCallback = function() { 
        try {
            this.app.stickies.workspaceSticky.Enable();
            this.app.stickies.paletteSticky.Enable();
            this.app.stickies.outlineSticky.Enable().Uncollapse(); //outline must be uncollapsed in order to make the editor work
            this.app.stickies.viewManagerSticky.Enable();

            //enable palette and outline
            this.app.stickies.paletteSticky.AddChild(this.palette);
            this.app.stickies.outlineSticky.AddChild(this.outline);
        
            if(!this.isInitialized) {
                this.InitGraph();
            }
        
            //enable menu
            this.arrangeMenuEntry.Show();
        } catch (error) {
            this.app.Note('focus callback'+error.toString(),'error');
        }
    };
    this.onUnfocusCallback = function() { 
        try {
            this.app.stickies.paletteSticky.RemoveChild(this.palette);
            this.app.stickies.outlineSticky.RemoveChild(this.outline);
            //disable menu
            this.arrangeMenuEntry.Hide();
        } catch(error) {
            this.app.Note(error.toString(),'error');
        }
    };

    //copy parameters
    jsa.CopyParams(this,params);

    //internals
    this.isInitialized = false;
    this.onResourceChangeCallback = null;
    this.onObjectChangeCallback = null;

    //Create DOM
    if(createDom) {
        this.CreateDom();
    }

};

EditorTab.prototype = Object.create(jsa.View.prototype);

EditorTab.prototype.CreateDom = function() {
    jsa.View.prototype.CreateDom.call(this);

    //this.domElement.classList.add('graph-view');

    this.canvas = document.createElement('div');
    this.canvas.id = "canvas"+this.id;
    this.canvas.classList.add("canvas");
    this.GetContainingDom().appendChild(this.canvas);

    
    this.editorCanvas = document.createElement('div');
    this.editorCanvas.id = "editorCanvas"+this.id;
    this.editorCanvas.classList.add("editor");
    this.editorCanvas.setAttribute('tabindex','0');

    this.canvas.appendChild(this.editorCanvas)


    //container.append("<div id=\"canvas"+id+"\" class=\"canvas\"><div id=\"editorCanvas"+id+"\" tabindex=\"0\" class=\"editor\"></div></div>"/*+uiBoxes+uiIcons+uiContextMenu*/+uiCanvasSearch);

    //Initialize Canvas Background
    /*
    this.canvasBackground = document.createElement('svg');
    this.canvasBackground.id = "canvasBackground"+this.id;
    this.canvasBackground.setAttribute('width','100%');
    this.canvasBackground.setAttribute('height','100%');
    this.canvasBackground.setAttribute('xmlns','http://www.w3.org/2000/svg');
    this.canvasBackground.innerHTML = "<defs> <pattern id=\"smallGrid"+this.id+"\" width=\"8\" height=\"8\" patternUnits=\"userSpaceOnUse\"> <path d=\"M 8 0 L 0 0 0 8\" fill=\"none\" stroke=\"lightgray\" stroke-width=\"0.5\"/> </pattern> <pattern id=\"grid"+this.id+"\" width=\"80\" height=\"80\" patternUnits=\"userSpaceOnUse\"> <rect width=\"80\" height=\"80\" fill=\"url(#smallGrid"+this.id+")\"/> <path d=\"M 80 0 L 0 0 0 80\" fill=\"none\" stroke=\"gainsboro\" stroke-width=\"2\"/> </pattern> </defs> <rect width=\"100%\" height=\"100%\" fill=\"url(#grid"+this.id+")\" /> ";
    this.canvas.appendChild(this.canvasBackground);
    */
    //BA: must use jquery here, because creating the svg with the above commands does not show up properly ???
    $(this.canvas).append("<svg id=\"canvasBackground"+this.id+"\" width=\"100%\" height=\"100%\" xmlns=\"http://www.w3.org/2000/svg\"> <defs> <pattern id=\"smallGrid"+this.id+"\" width=\"8\" height=\"8\" patternUnits=\"userSpaceOnUse\"> <path d=\"M 8 0 L 0 0 0 8\" fill=\"none\" stroke=\"lightgray\" stroke-width=\"0.5\"/> </pattern> <pattern id=\"grid"+this.id+"\" width=\"80\" height=\"80\" patternUnits=\"userSpaceOnUse\"> <rect width=\"80\" height=\"80\" fill=\"url(#smallGrid"+this.id+")\"/> <path d=\"M 80 0 L 0 0 0 80\" fill=\"none\" stroke=\"gainsboro\" stroke-width=\"2\"/> </pattern> </defs> <rect width=\"100%\" height=\"100%\" fill=\"url(#grid"+this.id+")\" /> </svg>");
    //$("#canvas"+id).append("<svg id=\"canvasBackground"+id+"\" width=\"100%\" height=\"100%\" xmlns=\"http://www.w3.org/2000/svg\"> <defs> <pattern id=\"smallGrid"+id+"\" width=\"8\" height=\"8\" patternUnits=\"userSpaceOnUse\"> <path d=\"M 8 0 L 0 0 0 8\" fill=\"none\" stroke=\"lightgray\" stroke-width=\"0.5\"/> </pattern> <pattern id=\"grid"+id+"\" width=\"80\" height=\"80\" patternUnits=\"userSpaceOnUse\"> <rect width=\"80\" height=\"80\" fill=\"url(#smallGrid"+id+")\"/> <path d=\"M 80 0 L 0 0 0 80\" fill=\"none\" stroke=\"gainsboro\" stroke-width=\"2\"/> </pattern> </defs> <rect width=\"100%\" height=\"100%\" fill=\"url(#grid"+id+")\" /> </svg>");

    //let uiContextMenu="";
    this.contextMenu = document.createElement('div');
    this.contextMenu.id = "contextMenu"+this.id;
    this.GetContainingDom().appendChild(this.contextMenu);
    //uiContextMenu+="<div id=\"contextMenu"+id+"\"></div>";
    
    //let uiCanvasSearch="";
    this.canvasSearch = document.createElement('div');
    this.canvasSearch.id = "canvasSearch"+this.id;
    this.canvasSearch.classList.add('uiCanvasSearch');
    this.canvasSearch.innerHTML = "<div class=\"col-auto\"> <label class=\"sr-only\" for=\"inlineFormInputGroup\">Search</label> <div class=\"input-group input-group-sm mb-2\"> <div class=\"input-group-prepend\"> <div class=\"input-group-text\">Search</div> </div> <input type=\"text\" class=\"form-control form-control-sm bg-secondary text-white\" id=\"canvasSearchField"+this.id+"\"></div></div>";
    this.GetContainingDom().appendChild(this.canvasSearch);
    //uiCanvasSearch+="<div class=\"uiCanvasSearch\" id=\"canvasSearch"+id+"\"> <div class=\"col-auto\"> <label class=\"sr-only\" for=\"inlineFormInputGroup\">Search</label> <div class=\"input-group input-group-sm mb-2\"> <div class=\"input-group-prepend\"> <div class=\"input-group-text\">Search</div> </div> <input type=\"text\" class=\"form-control form-control-sm bg-secondary text-white\" id=\"canvasSearchField\"></div></div></div>";
    
    this.canvasSearchResult = document.createElement('div');
    this.canvasSearchResult.id = "canvasSearchResults"+this.id;
    this.canvasSearchResult.classList.add('uiCanvasSearchResults');
    this.canvasSearchResult.innerHTML = 'canvasSearchResults';
    this.GetContainingDom().appendChild(this.canvasSearchResult);
    //uiCanvasSearch+="<div class=\"uiCanvasSearchResults\" id=\"canvasSearchResults"+id+"\">canvasSearchResults</div>";
    

    //initialize empty placeholders for palette and outline
    this.palette = new jsa.CustomFlatContainer({
        id: 'paletteContents'+this.id,
        style: ['graph-view-palette']
    });

    this.outline = new jsa.CustomFlatContainer({
        id: 'outlineContents'+this.id,
        style: ['graph-view-outline']
    });

   /*
   //create floating boxes for pallet and outline
   uiBoxes+="<div  class=\"uiBox uiEditorBox paletteBox\" id=\"elementsPalette"+tab.name+"\"><div id=\"paletteScrollBox"+tab.name+"\" class=\"uiScrollBox\"><div id=\"paletteContents"+tab.name+"\" class=\"paletteContainer\"></div></div></div>";
   uiBoxes+="<div id=\"treeViewBox"+tab.name+"\" class=\"uiBox uiEditorBox treeViewBox\"><div id=\"treeScrollBox"+tab.name+"\" class=\"uiScrollBox\"><div id=\"treeContainer"+tab.name+"\" class=\"treeViewContainer\"></div></div></div>";
   uiBoxes+="<div id=\"outline"+tab.name+"\" class=\"uiBox uiEditorBox outlineBox\"><div id=\"outlineCanvas"+tab.name+"\" class=\"outlineCanvas\"></div></div>";
   uiBoxes+="<div id=\"propertiesBox"+tab.name+"\" class=\"uiBox uiEditorBox propertiesBox\"><div id=\"propertiesScrollBox"+tab.name+"\" class=\"uiScrollBox\"><div id=\"propertiesContainer"+tab.name+"\" class=\"propertiesViewContainer\"><span style=\"white-space:nowrap\" >Nothing to display.</span></div></div></div>";
   */
  
    this.InitObject();
    this.InitResource();
    this.InitPath();

    return this;
};

EditorTab.prototype.InitGraph = function() {

    var self = this;

    try{   
        self.XGEEInstance=$app.plugins.require('editor').initializeEditor(ecoreSync,this.editor,this.eObject,this.editorCanvas,this.outline.GetContainingDom(),this.palette.GetContainingDom())
        this.InitMenus();
        this.isInitialized = true;
    }
    catch(e)
    {
        console.error('graph initialziation failed: '+e);
    }

    return this;
};

EditorTab.prototype.InitMenus = function() {
    let self = this; //for callbacks
    //Init menu
    this.arrangeMenuEntry = new jsa.MenuEntry({
        id :'GRAPH_MENU_ARRANGE_'+this.id,
        content : 'Arrange',
        hasPopup : true
    });
    this.app.menu.AddChildAtIndex(this.arrangeMenuEntry,10); //TODO: pluginize this

    this.arrangeMenu = new jsa.Menu({
        isPopup: true,
        popupDirection : 'bottom'
    });
    this.arrangeMenuEntry.SetSubmenu(this.arrangeMenu);

    this.arrangeMenu.AddChild( new jsa.MenuEntry( {
        id : 'GRAPH_MENU_ARRANGE_CIRCLE_'+this.id,
        content : 'Auto-layout: Circle',
        data : this,
        onClickCallback : function() {
            //let graph = this.data.graph;
            let graph = self.XGEEInstance.getGraph(); //TODO: Is are a better way to access the graph?
            let layout = new mxCircleLayout(graph);
            this.data.app.commandManager.Execute(new GraphLayoutCommand(graph,layout,'Circle'));
        }
    }));

    // BA: disabled because layouts other than circle are currently not working
    this.arrangeMenu.AddChild( new jsa.MenuEntry( {
        id : 'GRAPH_MENU_ARRANGE_PARTITION_'+this.id,
        content : 'Auto-layout: Partition',
        data : this,
        onClickCallback : function() {
            var graph = self.XGEEInstance.getGraph();
            // parameters should be variated due to a better look
            var layout = new mxPartitionLayout(graph,false,40, 40);
            layout.resizeVertices=false; // has to be used cause somehow this does not work in the creation of the mxgraph object
            this.data.app.commandManager.Execute(new GraphLayoutCommand(graph,layout,'Partition'));
        }
    }));

    this.arrangeMenu.AddChild( new jsa.MenuEntry( {
        id : 'GRAPH_MENU_ARRANGE_COMPOSITE_'+this.id,
        content : 'Auto-layout: Composite',
        data : this,
        onClickCallback : function() {
            var graph = self.XGEEInstance.getGraph();
            var circleLayout = new mxCircleLayout(graph);
            var partitionLayout = new mxPartitionLayout(graph);
            partitionLayout.resizeVertices = false;
            var layout = new mxCompositeLayout(graph, [partitionLayout,circleLayout]);
            this.data.app.commandManager.Execute(new GraphLayoutCommand(graph,layout,'Composite'));
        }
    }));

    this.arrangeMenu.AddChild( new jsa.MenuEntry( {
        id : 'GRAPH_MENU_ARRANGE_FASTORGANIC_'+this.id,
        content : 'Auto-layout: Fast Organic',
        data : this,
        onClickCallback : function() {
            var graph = self.XGEEInstance.getGraph();
            var layout = new mxFastOrganicLayout(graph);
            this.data.app.commandManager.Execute(new GraphLayoutCommand(graph,layout,'Fast Organic'));
        }
    }));

    this.arrangeMenu.AddChild( new jsa.MenuEntry( {
        id : 'GRAPH_MENU_ARRANGE_PARALLELEDGE_'+this.id,
        content : 'Auto-layout: Parallel Edge',
        data : this,
        onClickCallback : function() {
            var graph = self.XGEEInstance.getGraph();
            var layout = new mxParallelEdgeLayout(graph);
            this.data.app.commandManager.Execute(new GraphLayoutCommand(graph,layout,'Parallel Edge'));
        }
    }));

    this.arrangeMenu.AddChild( new jsa.MenuEntry( {
        id : 'GRAPH_MENU_ARRANGE_STACK_'+this.id,
        content : 'Auto-layout: Stack',
        data : this,
        onClickCallback : function() {
            var graph = self.XGEEInstance.getGraph();
            var layout = new mxStackLayout(graph,1,50);
            this.data.app.commandManager.Execute(new GraphLayoutCommand(graph,layout,'Stack'));
        }
    }));

    this.arrangeMenu.AddChild( new jsa.MenuEntry( {
        id : 'GRAPH_MENU_ARRANGE_EDGELABEL_'+this.id,
        content : 'Auto-layout: Edge Label',
        data : this,
        onClickCallback : function() {
            var graph = self.XGEEInstance.getGraph();
            var layout = new mxEdgeLabelLayout(graph);
            this.data.app.commandManager.Execute(new GraphLayoutCommand(graph,layout,'Edge Label'));
        }
    }));

    this.arrangeMenu.AddChild( new jsa.MenuEntry( {
        id : 'GRAPH_MENU_ARRANGE_RADIALTREE_'+this.id,
        content : 'Auto-layout: Radial Tree',
        data : this,
        onClickCallback : function() {
            var graph = self.XGEEInstance.getGraph();
            var layout = new mxRadialTreeLayout(graph);
            this.data.app.commandManager.Execute(new GraphLayoutCommand(graph,layout,'Radial Tree'));
        }
    }));


    this.arrangeMenu.AddChild( new jsa.MenuEntry( {
        id : 'GRAPH_MENU_ARRANGE_COMPACTTREE_'+this.id,
        content : 'Auto-layout: Compact Tree',
        data : this,
        onClickCallback : function() {
            var graph = self.XGEEInstance.getGraph();
            var layout = new mxCompactTreeLayout(graph);
            this.data.app.commandManager.Execute(new GraphLayoutCommand(graph,layout,'Compact Tree'));
        }
    }));

    this.arrangeMenu.AddChild( new jsa.MenuEntry( {
        id : 'GRAPH_MENU_ARRANGE_HIERARCHICAL_'+this.id,
        content : 'Auto-layout: Hierarchical',
        data : this,
        onClickCallback : function() {
            var graph = self.XGEEInstance.getGraph();
            var layout = new mxHierarchicalLayout(graph,'west');
            layout.disableEdgeStyle = false;
            layout.edgeStyle = mxHierarchicalEdgeStyle.STRAIGHT;
            layout.intraCellSpacing = 250; // spacing between the "arms of the model"
            layout.interRankCellSpacing = 250; // spacing between the different connected nodes
            layout.traverseAncestors=false
            this.data.app.commandManager.Execute(new GraphLayoutCommand(graph,layout,'Hierarchical'));
        }
    }));

    this.arrangeMenu.AddChild( new jsa.MenuEntry( {
        id : 'GRAPH_MENU_ARRANGE_HIERARCHICAL_'+this.id,
        content : 'Auto-layout: Tree',
        data : this,
        onClickCallback : function() {
            var graph = self.XGEEInstance.getGraph();
            var layout = new mxHierarchicalLayout(graph,'north');
            layout.disableEdgeStyle = false;
            layout.edgeStyle = mxHierarchicalEdgeStyle.STRAIGHT;
            layout.intraCellSpacing = 250; // spacing between the "arms of the model"
            layout.interRankCellSpacing = 250; // spacing between the different connected nodes
            this.data.app.commandManager.Execute(new GraphLayoutCommand(graph,layout,'Hierarchical'));
        }
    }));


    
    
    return this;
};



EditorTab.prototype.UpdateTitle = function() {
    //update the title with full object path 
    let editorName = this.editor.getModel().get('name');
    let objectId = this.ecoreSync.rlookup(this.eObject);
    //var isDirty = this.eObject.get('eResource').get('isDirty');
    //var self = this;
    let title = editorName+' '+this.objectClassName+'[#'+objectId+']:\''+this.objectName+'\' ('+this.pathStr+')';
    this.SetName(title);
    // if(this.container) {
    //     this.container.NotifyViewChange(this);
    // }
};

EditorTab.prototype.InitResource = function() {
    let self = this;

    this.onResourceChangeCallback = function(featureName) {
        if('name' == featureName) {
            self.ecoreSync.getObjectShortPath(self.eObject).then(function(pathStr){
                self.pathStr = pathStr;
                self.UpdateTitle();
            });
        }
    };

    this.ecoreSync.utils.getResource(this.eObject).then(function(eResource) {
        self.ecoreSync.get(eResource,'name').then(function(name) {
            // self.ecoreSync.isAttributeInitialized(eResource,'isDirty').then(function(unused2) {
            self.eResource = eResource;
            //self.isDirty = eResource.get('isDirty');
            self.UpdateTitle();

            //TODO: attach change listener to resource dirty and name
            self.eResource.on('change',self.onResourceChangeCallback);  
        // });
        });
    });
};

EditorTab.prototype.InitPath = function() {
    let self = this;
    this.ecoreSync.utils.getObjectShortPath(this.eObject).then(function(pathStr){
        self.pathStr = pathStr;
        self.UpdateTitle();
    });
};

EditorTab.prototype.InitObject = function() {
    let self = this;
    this.ecoreSync.utils.isEClassInitialized(this.eObject.eClass).then(function(unused){
        let name  = self.eObject.eClass.get('name');
        self.objectClassName = name?name:'?';
        self.UpdateTitle();
    });

    //TODO: make local command once Try is locally supported
    this.ecoreSync.remoteExec(new eoq2.Get(new eoq2.Obj(this.ecoreSync.rlookup(this.eObject)).Try(QRY.Pth('name')))).then(function(name){
        self.objectName = name?name:'?';
        self.UpdateTitle();
    });

    this.onObjectChangeCallback = function(featureName) {
        if('name'==featureName) {
            let name = self.eObject.get('name');
            self.objectName = name?name:'?';
            self.UpdateTitle();
        }
    };

    this.eObject.on('change',this.onObjectChangeCallback);  
};

//@overwrite
EditorTab.prototype.Close = function() {
    this.Dissolve();
    return this;
};

//@overwrite
EditorTab.prototype.Dissolve = function() {
    if(this.eResource && this.onResourceChangeCallback) {
        this.eResource.off('change',this.onResourceChangeCallback);
    }
    if(this.eObject && this.onObjectChangeCallback) {
        this.eObject.off('change',this.onObjectChangeCallback);
    }

    jsa.View.prototype.Dissolve.call(this);
};




export {EditorTab};