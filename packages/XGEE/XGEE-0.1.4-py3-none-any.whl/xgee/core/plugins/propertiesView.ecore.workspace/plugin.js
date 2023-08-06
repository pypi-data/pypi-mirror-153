//init namespace

export function init(pluginAPI,config) {  
    //plug-in statics and configuration
    var scriptIncludes=[
        "js/WorkspacePropertiesPaneConfig.js"      
    ];

    var stylesheetIncludes=[];
    
    //init the plug-in
    return pluginAPI.loadScripts(scriptIncludes).then(function(){ 
        return pluginAPI.loadStylesheets(stylesheetIncludes).then(function(){ 
            let params = config;
            params.config = PROPERTIES_VIEW_ECORE_WORKSPACE.DEFAULT_CONFIG;
            pluginAPI.implement('propertiesView.pane',new PROPERTIES_VIEW_ECORE_CUSTOM.CustomPropertiesPaneProvider(pluginAPI,config));     

            return Promise.resolve(); });   
        });
};

export var meta={
    id:"propertiesView.ecore.workspace",
    description:"A specialized properties editor for the EOQ workspace model.",
    author:"Bjoern Annighoefer",
    version:"1.0.0",
	config : { //The default config of the plugin, this might be overwritten during initialization
        name : "Workspace",
        importance : 10, //the higher, the more left the tab is shown
        readonly : false, // disable all inputs if true
        ecoreSyncId : '' //currently not used
	  },
    requires:[
        "propertiesView.ecore.custom"
    ]
};



