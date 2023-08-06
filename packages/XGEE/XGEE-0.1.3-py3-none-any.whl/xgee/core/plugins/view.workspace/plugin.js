export function init(pluginAPI,config) {  
    //plug-in statics and configuration
    var scriptIncludes=[
        "js/WorkspaceViewProvider.js",
    ];

    var stylesheetIncludes=[
        "css/WorkspaceView.css"
    ];
    
    //init the plug-in
    return pluginAPI.loadScripts(scriptIncludes).then(function(){ 
        return pluginAPI.loadStylesheets(stylesheetIncludes).then(function(){ 
            //see if there are instances to be created
            for(let i=0; i<config.instances.length;i++) {
                let params = config.instances[i];
                //create an properties view controller that handles all the logic stuff.
                let viewProvider = new WORKSPACE_VIEW.WorkspaceViewProvider(pluginAPI,params);
            
                //register to autostart in order to get started, when the GUI is available
                let name = pluginAPI.getMeta().id;
                pluginAPI.implement(VIEWS.VIEW_EXT_POINT_ID,viewProvider); 
            }
            return Promise.resolve();
        });   
    });
};

export var meta={
    id : "view.workspace",
    description : "Opens a view to browse the workspace of an EOQ domain",
    author : "Matthias Brunner",
    version : "1.0.0",
    config : {
        instances : [{
            viewId : '#WORKSPACE',
            position : 0,
            viewName : 'Workspace',
            hasHeader : true,
            ecoreSync : null,
            //viewIcon : pluginApi.getPath()+'img/view-dashboard.svg',
            viewStyle :'workspace-view',
            closable : false, //wheter the view can be closed
            activateView: false //activate on start
        }]
    },
    requires :[
        "views",
        "ecoreSync",
        "plugin.ecoreTreeView"
    ]
};



