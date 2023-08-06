// 2020 Bjoern Annighoefer

var DASHBOARD_VIEW = DASHBOARD_VIEW || {};

Object.assign(DASHBOARD_VIEW,(function(){
    let DASH_EXT_POINT_ID = 'dashboardView.dashes';

    function DashboardViewProvider(pluginApi,params) {
        
        //params
        this.viewId = '#DASHBOARD';
        this.position = 0;
        this.viewName = 'Dashboard';
        this.viewIcon = pluginApi.getPath()+'img/view-dashboard.svg';
        this.viewStyle = 'dashboard-view';
        this.viewContainerStyle = ['jsa-view-container','jsa-dashboard-view'];
        this.hasHeader = true;
        this.rows = 3;
        this.closable = false; //whether the view can be closed
        this.activateView = true; //activate view after creation
        Object.assign(this,params); //copy params

        VIEWS.ViewProvider.call(this,this.viewId,this.position,this.activateView);

        //internals
        this.app = pluginApi.getGlobal('app'); 
        this.pluginApi = pluginApi;
        this.view = null;
    }
    DashboardViewProvider.prototype = Object.create(VIEWS.ViewProvider.prototype);

    //@Override
    DashboardViewProvider.prototype.CreateView = function() {
        //CREATE VIEW
        let self = this;
        this.view = new jsa.DashboardView({
            id: this.viewId,
            name: this.viewName,
            icon: this.viewIcon,
            content: '',
            hasHeader: this.hasHeader,
            containerStyle: this.viewContainerStyle,
            style: ['jsa-view',this.viewStyle],
            closable : this.closable,
            onFocusCallback : function() { 
                self.app.stickies.workspaceSticky.Enable();
                self.app.stickies.paletteSticky.Collapse().Disable();
                self.app.stickies.outlineSticky.Collapse().Disable();
                self.app.stickies.viewManagerSticky.Enable();
                }
        });

        //add the number of rows
        for(let i=0;i<this.rows;i++) {
            let row = new jsa.CustomFlatContainer({
                style: ['jsa-row']
            });
            this.view.AddChild(row);

            //get all registered dashes
            let providers = this.pluginApi.evaluate(DASH_EXT_POINT_ID).filter(function(p){
                return (p.dashboardId == self.viewId && p.row == i)
            }).sort(function(a,b){
                return a.position - b.position; //lowest position first
            });

            for(let j=0;j<providers.length;j++) {
                let provider = providers[j];
                this.CreateAndAddDash(row,provider);
            }
        }

        return this.view;
    }

    DashboardViewProvider.prototype.OnPluginImplement = function(pluginExtensionEvent) {
        if(this.viewManager) {
            if("IMPLEMENT" == pluginExtensionEvent.id) {
                let provider = pluginExtensionEvent.extension;
                let row = this.view.children(provider.row);
                this.CreateAndAddDash(row,provider); //TODO: position of lately added dash is not considered.
            }
        }
    }

    DashboardViewProvider.prototype.CreateAndAddDash = function(row,provider) {
        try {
            let dash = provider.CreateDash();
            row.AddChild(dash);
        } catch(e) {
            console.warn("DASHBOARD("+this.viewId+"): Could not create dash "+provider.providerId+": "+e.toString());
        }
    };


    return {
        DASH_EXT_POINT_ID : DASH_EXT_POINT_ID,
        DashboardViewProvider : DashboardViewProvider
    };
})());