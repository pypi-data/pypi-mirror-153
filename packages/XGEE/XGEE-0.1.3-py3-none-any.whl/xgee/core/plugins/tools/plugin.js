export function init(pluginAPI,config) {  
    //plug-in statics and configuration
    var scriptIncludes=[
        "js/ToolsController.js",
        "js/ToolProvider.js",
    ];

    var stylesheetIncludes=[
    ];
    
    //init the plug-in
    return pluginAPI.loadScripts(scriptIncludes).then(function(){ 
        return pluginAPI.loadStylesheets(stylesheetIncludes).then(function(){ 
            let params = config;
            //create an tools controller that handles all the logic stuff.
            let toolsController = new TOOLS.ToolsController(pluginAPI,params);
        
            //register to autostart in order to get started, when the toolbar is available
            pluginAPI.implement('autostart',new autostart.Autostarter("tools",'APP/STARTUP/TOOLS',function() {
                toolsController.Init();
            })); 
            //provide an extension point
            pluginAPI.provide(TOOLS.TOOL_EXT_POINT_ID,TOOLS.ToolProvider);
            
            return Promise.resolve();
        });   
    });
};

export var meta={
    id : "tools",
    description : "Provides the posibility to add tools by plugin",
    author : "Bjoern Annighoefer",
    version : "1.0.0",
    config : { },
    requires :[
        "autostart",
    ]
};



