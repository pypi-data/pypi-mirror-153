export function init(pluginAPI,config) {  
    //plug-in statics and configuration
    var scriptIncludes=[
        "js/NotesTool.js",
        "js/NotesToolProvider.js"
    ];

    var stylesheetIncludes=[
        "css/NotesTool.css"
    ];
    
    //init the plug-in
    return pluginAPI.loadScripts(scriptIncludes).then(function(){ 
        return pluginAPI.loadStylesheets(stylesheetIncludes).then(function(){ 
            let params = config
            //create a provider which handles the tool creation if demanded.
            let toolName = pluginAPI.getMeta().id;
            let provider = new NOTES_TOOL.NotesToolProvider(pluginAPI,toolName,params);
            pluginAPI.implement(TOOLS.TOOL_EXT_POINT_ID,provider);

            return Promise.resolve(); });   
        });
};

export var meta={
    id : "tool.notes",
    description : "Adds a tool that popup notes issued to the application in boxes and provides means to read old notes.",
    author : "Bjoern Annighoefer",
    version : "1.0.0",
    config : {},
    requires :[
        "tools",
    ]
};



