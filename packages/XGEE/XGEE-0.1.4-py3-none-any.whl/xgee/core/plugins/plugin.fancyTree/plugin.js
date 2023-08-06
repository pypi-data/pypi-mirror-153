export function init(pluginAPI) {  

    var scriptIncludes=[];
    scriptIncludes.push("jquery.fancytree-all-deps.min.js");    
    var stylesheetIncludes=[];
    stylesheetIncludes.push("skin-win8/ui.fancytree.css");    
    
    return pluginAPI.loadScripts(scriptIncludes).then(function(){ 
        return pluginAPI.loadStylesheets(stylesheetIncludes).then(function(){ 
            return Promise.resolve(); });   
        });
};

export var meta={"id":"plugin.fancyTree",description:"FancyTree","author":"Martin Wendt","version":"2.33.0","requires":[]};



