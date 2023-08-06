//init namespace

export function init(pluginAPI,config) {  
    //plug-in statics and configuration
    var scriptIncludes=[
        "js/EcoreModifyPropertiesPane.js",
        "js/EcoreModifyPropertiesPaneProvider.js"        
    ];

    var stylesheetIncludes=[
        "css/EcoreModifyPropertiesPane.css"
    ]; 
    
    //init the plug-in
    return pluginAPI.loadScripts(scriptIncludes).then(function(){ 
        return pluginAPI.loadStylesheets(stylesheetIncludes).then(function(){ 
            //nothing is created, this is only a library     
            let params = config;
            pluginAPI.implement('propertiesView.pane',new PROPERTIES_VIEW_ECORE_MODIFY.EcoreModifyPropertiesPaneProvider(pluginAPI,params)); 
            return Promise.resolve(); });   
        });
};

export var meta={
    id:"propertiesView.ecore.modify",
    description:"Provides modifications actions as delete, copy, clone.",
    author:"Bjoern Annighoefer",
    version:"1.0.0",
	config : { //The default config of the plugin, this might be overwritten during initialization
        name : "Modify",
        importance : 7, //the higher, the more left the tab is shown
        ecoreSyncId : '' //currently not used
	  },
    requires:[
        "ecoreSync",
        "propertiesView"
    ]
};



