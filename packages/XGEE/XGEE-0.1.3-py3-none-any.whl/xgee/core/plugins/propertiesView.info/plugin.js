//init namespace

export function init(pluginAPI,config) {  
    //plug-in statics and configuration
    var scriptIncludes=[
        "js/InfoPropertiesPaneProvider.js",
    ];

    var stylesheetIncludes=[];
    //stylesheetIncludes.push("skin-win8/ui.fancytree.css"); 
    
    //init the plug-in
    return pluginAPI.loadScripts(scriptIncludes).then(function(){ 
        return pluginAPI.loadStylesheets(stylesheetIncludes).then(function(){ 
            pluginAPI.implement('propertiesView.pane',new PROPERTIES_VIEW_INFO.InfoPropertiesPaneProvider(config.name));     

            return Promise.resolve(); });   
        });
};

export var meta={
    id: "propertiesView.info",
    description : "A generic propertiesView for any kind of objects.",
    author : "Bjoern Annighoefer",
    version : "1.0.0",
    config : { //The default config of the plugin, this might be overwritten during initialization
		name : "Info"
	  },
    requires:[
        "propertiesView"
    ]
};



