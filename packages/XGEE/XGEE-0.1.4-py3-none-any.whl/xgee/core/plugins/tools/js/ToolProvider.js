// 2020 Bjoern Annighoefer

var TOOLS = TOOLS || {};

Object.assign(TOOLS,(function(){
    function ToolProvider(name,position) {
        name = name;
        position = position; //lower comes first
    } 

    ToolProvider.prototype.CreateTool = function() {
        //to be overwritten
    };

    
    return {
        ToolProvider : ToolProvider
    };
})());