// 2020 Bjoern Annighoefer

export function init(pluginAPI,config) { 
    //static methods and propertiesView
    var PROPERTIES_PANE_EXT_ID = "propertiesView.pane";

    var scriptIncludes=[
        "js/PropertiesPaneProvider.js",
        "js/PropertiesViewController.js",
        "js/LoadOnDemandView.js"
    ];

    var stylesheetIncludes=[
        "css/PropertiesView.css"
    ]; 

    //basic plug-in initialization routine    
    return pluginAPI.loadScripts(scriptIncludes).then(function(){ 
        return pluginAPI.loadStylesheets(stylesheetIncludes).then(function(){ 
            //create an properties view controller that handles all the logic stuff.
            let propertiesViewController = new PROPERTIES_VIEW.PropertiesViewController(pluginAPI,PROPERTIES_PANE_EXT_ID,config);

            //exhibit internal classes
            pluginAPI.expose({
                PropertiesPaneProvider : PROPERTIES_VIEW.PropertiesPaneProvider,
                propertiesViewController : propertiesViewController
            });

            //exhibit extension points
            pluginAPI.provide(PROPERTIES_PANE_EXT_ID,PROPERTIES_VIEW.PropertiesPaneProvider);

            //register to autostart in order to get started, when the GUI is available
            pluginAPI.implement('autostart',new autostart.Autostarter("propertiesView",'APP/STARTUP/TOOLS',function() {
                propertiesViewController.Init();
            })); 
        });   
    });
};

export var meta={
    id : "propertiesView",
    description : "Basic plug-in, for the editing of selected elements.",
    author : "Bjoern Annighoefer",
    version : "1.0.0",
    config : {
        mode: 'BUBBLE',
        enabledModeChanges : true
    },
    requires : [
        "autostart",
        "eventBroker"
    ]
};



