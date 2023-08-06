// 2020 Bjoern Annighoefer

export function init(pluginAPI,config) {  
    //plug-in statics and configuration
    var scriptIncludes=[
        "js/ViewsController.js",
        "js/ViewProvider.js",
    ];

    var stylesheetIncludes=[
    ];
    
    //init the plug-in
    return pluginAPI.loadScripts(scriptIncludes).then(function(){ 
        return pluginAPI.loadStylesheets(stylesheetIncludes).then(function(){ 
            let params = config;
            //create an tools controller that handles all the logic stuff.
            let viewsController = new VIEWS.ViewsController(pluginAPI,params);
        
            //register to autostart in order to get started, when the toolbar is available
            let name = pluginAPI.getMeta().id;
            pluginAPI.implement('autostart',new autostart.Autostarter(name,'APP/STARTUP/VIEWS',function() {
                viewsController.Init();
            })); 
            //provide an extension point
            pluginAPI.provide(VIEWS.VIEW_EXT_POINT_ID,VIEWS.ViewProvider,function(evt){
                viewsController.OnPluginImplement(evt)}
            );
            
            return Promise.resolve();
        });   
    });
};

export var meta={
    id : "views",
    description : "Provides the posibility to add views by plugin",
    author : "Bjoern Annighoefer",
    version : "1.0.0",
    config : {},
    requires :[
        "autostart",
    ]
};



