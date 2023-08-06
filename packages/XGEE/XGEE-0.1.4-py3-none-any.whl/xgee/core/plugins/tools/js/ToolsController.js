// 2020 Bjoern Annighoefer

var TOOLS = TOOLS || {};

Object.assign(TOOLS,(function(){
    let TOOL_EXT_POINT_ID = 'tools.tool';

    function ToolsController(pluginApi,params) {
        //params
        Object.assign(this,params); //copy params

        //internals
        this.app = pluginApi.getGlobal('app'); 
        this.pluginApi = pluginApi;
        this.toolbar = null;
    } 

    // ToolsController.prototype.Init = function() {
    //     this.Init();
    // };

    ToolsController.prototype.Init = function() {
        this.toolbar = this.app.toolbar;
        if(this.toolbar) {
            //get all registered tools
            let toolProviders = this.pluginApi.evaluate(TOOL_EXT_POINT_ID).sort(function(a,b){
                return a.position - b.position; //lowest position first
            });

            for(let j=0;j<toolProviders.length;j++) {
                let toolProvider = toolProviders[j];
                try {
                    let tool = toolProvider.CreateTool();
                    this.toolbar.AddChild(tool);
                }catch(e) {
                    console.warn("TOOLS: Could not create "+toolProvider.name+": "+e.toString());
                }
            }
        } else {
            Error("Application has no toolbar!")
        }
    }

    return {
        TOOL_EXT_POINT_ID : TOOL_EXT_POINT_ID,
        ToolsController : ToolsController
    };
})());