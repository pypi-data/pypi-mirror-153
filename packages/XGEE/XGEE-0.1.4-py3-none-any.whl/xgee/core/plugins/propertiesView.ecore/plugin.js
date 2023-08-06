//init namespace

export function init(pluginAPI,config) {  
    //plug-in statics and configuration
    var scriptIncludes=[
        "js/EObjectPropertiesPaneProvider.js",
        "js/EObjectPropertiesPane.js"
    ];

    var stylesheetIncludes=[];
    //stylesheetIncludes.push("skin-win8/ui.fancytree.css"); 
    
    //init the plug-in
    return pluginAPI.loadScripts(scriptIncludes).then(function(){ 
        return pluginAPI.loadStylesheets(stylesheetIncludes).then(function(){ 
            let params = config;
            pluginAPI.implement('propertiesView.pane',new PROPERTIES_VIEW_ECORE.EObjectPropertiesPaneProvider(pluginAPI,params));     
            return Promise.resolve(); });   
        });
};

export var meta={
    id:"propertiesView.ecore",
    description:"A generic propertiesView editor for EObjects, showing all its protperties",
    author:"Bjoern Annighoefer",
    version:"1.0.0",
	config : { //The default config of the plugin, this might be overwritten during initialization
        name : "EObject",
        importance : 5,
        ecoreSyncId : 'ecoreSync'
	  },
    requires:[
        "propertiesView",
        "ecoreSync.ui"
    ]
};



