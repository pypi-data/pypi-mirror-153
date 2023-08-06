export function init(pluginAPI) {      
    return pluginAPI.loadScripts(["sax-js-master/lib/sax.js","ecore.xmi.js"]).then(function(){ 
        return Promise.resolve(); 
    });    
};

export var meta={
    "id":"ecore",
    "description":"ecore javascript implementation",
    "author":"Guillaume Hillairet, Isaac Z. Schlueter et al.",
    "version":"0.0.0",
    "requires":[]
};



