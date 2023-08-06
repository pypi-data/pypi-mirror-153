//init namespace

export function init(pluginAPI,config) {  
    //plug-in statics and configuration
    var scriptIncludes=[
        "js/CustomPropertiesPaneConfig.js",
        "js/CustomPropertiesPane.js",
        "js/CustomPropertiesPaneProvider.js"        
    ];

    var stylesheetIncludes=[]; 
    
    //init the plug-in
    return pluginAPI.loadScripts(scriptIncludes).then(function(){ 
        return pluginAPI.loadStylesheets(stylesheetIncludes).then(function(){ 
            //nothing is created, this is only a library     

            return Promise.resolve(); });   
        });
};

export var meta={
    id:"propertiesView.ecore.custom",
    description:"Provides generic base classes to show customized properties editors by configuration",
    author:"Bjoern Annighoefer",
    version:"1.0.0",
	config : { },
    requires:[
        "ecoreSync.ui"
    ]
};



