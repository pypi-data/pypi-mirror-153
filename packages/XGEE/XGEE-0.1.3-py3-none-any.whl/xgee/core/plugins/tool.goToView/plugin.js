export function init(pluginAPI,config) {  
    //plug-in statics and configuration
    var scriptIncludes=[
        "js/GoToViewTool.js",
        "js/GoToViewToolProvider.js"
    ];

    var stylesheetIncludes=[
        "css/GoToViewTool.css"
    ];
    
    //init the plug-in
    return pluginAPI.loadScripts(scriptIncludes).then(function(){ 
        return pluginAPI.loadStylesheets(stylesheetIncludes).then(function(){ 
            for(let i=0;i<config.instances.length;i++) {
                let params = config.instances[i];
                //create a provider which handles the tool creation if demanded.
                let toolName = pluginAPI.getMeta().id+"("+params.viewId+")";
                let provider = new GO_TO_VIEW_TOOL.GoToViewToolProvider(pluginAPI,toolName,params);
                pluginAPI.implement(TOOLS.TOOL_EXT_POINT_ID,provider);
            }
            return Promise.resolve(); });   
        });
};

export var meta={
    id : "tool.goToView",
    description : "Adds a tool that opens a specific view. If the view does not exist, the tool is not shown",
    author : "Bjoern Annighoefer",
    version : "1.0.0",
    config : {instances: {
        viewId : 'DASHBOARD_VIEW'
    }},
    requires :[
        "tools",
    ]
};



