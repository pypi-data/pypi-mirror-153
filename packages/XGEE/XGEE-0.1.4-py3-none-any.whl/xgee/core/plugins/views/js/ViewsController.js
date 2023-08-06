// 2020 Bjoern Annighoefer

var VIEWS = VIEWS || {};

Object.assign(VIEWS,(function(){
    let VIEW_EXT_POINT_ID = 'views.view';

    function ViewsController(pluginApi,params) {
        //params
        Object.assign(this,params); //copy params

        //internals
        this.app = pluginApi.getGlobal('app'); 
        this.pluginApi = pluginApi;
        this.viewManager = null;
    } 

    ViewsController.prototype.Init = function() {
        this.viewManager = this.app.viewManager;
        if(this.viewManager) {
            //get all registered tools
            let providers = this.pluginApi.evaluate(VIEW_EXT_POINT_ID).sort(function(a,b){
                return a.position - b.position; //lowest position first
            });

            for(let j=0;j<providers.length;j++) {
                let provider = providers[j];
                this.CreateAndAddView(provider);
            }
        } else {
            Error("Application has no viewManager!")
        }
    };

    ViewsController.prototype.OnPluginImplement = function(pluginExtensionEvent) {
        if(this.viewManager) {
            if("IMPLEMENT" == pluginExtensionEvent.id) {
                let provider = pluginExtensionEvent.extension;
                this.CreateAndAddView(provider); //TODO: position of latly added view is not considered.
            }
        }
    };

    ViewsController.prototype.CreateAndAddView = function(provider) {
        try {
            let view = provider.CreateView();
            this.viewManager.AddChild(view);
            if(provider.activate) {
                this.viewManager.ActivateView(view);
            }
        }catch(e) {
            console.warn("VIEWS: Could not create view "+provider.providerId+": "+e.toString());
        }
    };

    return {
        VIEW_EXT_POINT_ID : VIEW_EXT_POINT_ID,
        ViewsController : ViewsController
    };
})());