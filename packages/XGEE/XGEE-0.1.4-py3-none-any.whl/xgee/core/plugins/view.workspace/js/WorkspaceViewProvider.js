// 2020 Bjoern Annighoefer

var WORKSPACE_VIEW = WORKSPACE_VIEW || {};

Object.assign(WORKSPACE_VIEW,(function(){

    function WorkspaceViewProvider(pluginApi,params) {
        
        //params
        this.viewId = '#WORKSPACE';
        this.position = 0;
        this.viewName = 'Dashboard';
        this.viewIcon = pluginApi.getPath()+'img/view-workspace.svg';
        this.viewStyle = 'workspace-view';
        this.viewContainerStyle = ['jsa-view-container'];
        this.hasHeader = true;
        this.ecoreSync = null; //is set later
        this.isClosable = false; //wheter the view can be closed
        this.activateView = false; //activate view after creation
        Object.assign(this,params); //copy params

        VIEWS.ViewProvider.call(this,this.viewId,this.position,this.activateView);

        //internals
        this.app = pluginApi.getGlobal('app'); 
        this.pluginApi = pluginApi;
        this.view = null;
    }
    WorkspaceViewProvider.prototype = Object.create(VIEWS.ViewProvider.prototype);

    //@Override
    WorkspaceViewProvider.prototype.CreateView = function() {
        //CREATE VIEW
        let self = this;
        this.view = new jsa.View({
            id: this.viewId,
            name: this.viewName,
            icon: this.viewIcon,
            content: '',
            hasHeader: this.hasHeader,
            containerStyle: this.viewContainerStyle,
            style: ['jsa-view',this.viewStyle],
            isClosable : this.closable,
            onFocusCallback : function() { 
                self.app.stickies.workspaceSticky.Hide();
                self.app.stickies.paletteSticky.Collapse().Disable();
                self.app.stickies.outlineSticky.Collapse().Disable();
                self.app.stickies.viewManagerSticky.Enable();
            },
            onUnfocusCallback : function() {
                self.app.stickies.workspaceSticky.Show();
            }
        });
    
        //attache the tree provider
        this.ecoreSync = this.app.ecoreSync;//TODO: hand it in from the outside
        let treeProvider = this.pluginApi.require('plugin.ecoreTreeView');
        let treeView=treeProvider.create(this.ecoreSync,
            'workspaceViewTree',
            this.view.GetContainingDom(),
            0,'Workspace'
        );

        return this.view;
    }

    return {
        WorkspaceViewProvider : WorkspaceViewProvider
    };
})());