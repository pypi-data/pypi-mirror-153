// 2020 Bjoern Annighoefer

var GO_TO_VIEW_TOOL = GO_TO_VIEW_TOOL || {};

Object.assign(GO_TO_VIEW_TOOL,(function(){
    function GoToViewToolProvider(pluginApi,name,params) {
        TOOLS.ToolProvider.call(this,name,params.position);
        //params
        this.viewId = 'DASHBOARD_VIEW';
        Object.assign(this,params); //copy params

        //internals
        this.app = pluginApi.getGlobal('app'); 
        this.pluginApi = pluginApi;
        this.tool = null
    } 
    GoToViewToolProvider.prototype = Object.create(TOOLS.ToolProvider.prototype);

    //@Overwrite
    GoToViewToolProvider.prototype.CreateTool = function() {
        //Create new dash
        let viewManager = this.app.viewManager;
        if(viewManager) {
            this.tool = new GO_TO_VIEW_TOOL.GoToViewTool({
                viewId : this.viewId,
                viewManager : viewManager
            });
        }
        return this.tool;
    };

    return {
        GoToViewToolProvider : GoToViewToolProvider
    };
})());