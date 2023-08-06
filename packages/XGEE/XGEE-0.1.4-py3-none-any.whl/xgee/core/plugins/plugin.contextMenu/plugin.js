export function init(pluginAPI) {      
    var loadScripts=pluginAPI.loadScripts(["jQuery-contextMenu-2.8/jquery.contextMenu.min.js","jQuery-contextMenu-2.8/jquery.ui.position.min.js"]).then(function(){ return Promise.resolve(); });    
    var loadStyles=pluginAPI.loadStylesheets(["jQuery-contextMenu-2.8/jquery.contextMenu.min.css"]).then(function(){ return Promise.resolve(); });  
    return Promise.all([loadScripts, loadStyles]).then(function(){ return Promise.resolve(); });
};
export var meta={"id":"plugin.contextMenu",description:"jQuery contextMenu","author":"Björn Brala, Rodney Rehm, Christian Baartse, Addy Osmani","version":"2.8.0","requires":[]};



