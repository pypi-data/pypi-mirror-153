//init namespace

export function init(pluginAPI,config) {  
    //plug-in statics and configuration
    var scriptIncludes=[
        "js/EcoreEditorsPropertiesPane.js",
        "js/EcoreEditorsPropertiesPaneProvider.js"        
    ];

    var stylesheetIncludes=[
        "css/EcoreEditorsPropertiesPane.css"
    ]; 
    
    //init the plug-in
    return pluginAPI.loadScripts(scriptIncludes).then(function(){ 
        return pluginAPI.loadStylesheets(stylesheetIncludes).then(function(){ 
            //nothing is created, this is only a library     
            let params = config;
            pluginAPI.implement('propertiesView.pane',new PROPERTIES_VIEW_ECORE_EDITORS.EcoreEditorsPropertiesPaneProvider(pluginAPI,params)); 
            return Promise.resolve(); });   
        });
};

export var meta={
    id:"propertiesView.ecore.editors",
    description:"Lists available editors and allows opening them.",
    author:"Bjoern Annighoefer",
    version:"1.0.0",
	config : { //The default config of the plugin, this might be overwritten during initialization
        name : "Editors",
        importance : 7, //the higher, the more left the tab is shown
        ecoreSyncId : 'ecoreSync' //currently not used
	  },
    requires:[
        "ecoreSync",
        "propertiesView"
    ]
};



