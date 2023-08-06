export function init(pluginAPI) {  

    var scriptIncludes=[
        "js/EObjectCtrls.js",
        "js/EObjectCtrlFactory.js",
        //"js/EObjectCtrlUpdateHandler.js"
    ];

    var stylesheetIncludes=[
        "css/EObjectCtrls.css"
    ];
    //stylesheetIncludes.push("skin-win8/ui.fancytree.css");    
    
    return pluginAPI.loadScripts(scriptIncludes).then(function(){ 
        return pluginAPI.loadStylesheets(stylesheetIncludes).then(function(){ 
            return Promise.resolve(); });   
        });
};

export var meta={
    "id":"ecoreSync.ui",
    "description":"Form elements for EObjects and its properties, e.g. text boxes, auto completion",
    "author":"Bjoern Annighoefer",
    "version":"1.0.0",
    "requires":["ecoreSync"]
};



