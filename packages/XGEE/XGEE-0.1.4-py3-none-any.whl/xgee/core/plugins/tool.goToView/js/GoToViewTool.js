// 2020 Bjoern Annighoefer

var GO_TO_VIEW_TOOL = GO_TO_VIEW_TOOL || {};

Object.assign(GO_TO_VIEW_TOOL,(function(){

    function GoToViewTool(params={},createDom=true) {
        jsa.Tool.call(this,params,false);
        jsa.Observer.call(this);
        
        //parameters
        this.viewManager = null;
        this.viewId = null;
        this.detachedStyle = 'tool-go-to-view-disabled';
        this.style = ['jsa-tool',this.detachedStyle];
        this.containerStyle = ['jsa-tool-container','tool-go-to-view'];


        let self = this;
        this.onClickCallback = function(event) {
            self.OnClick(event);
        };

        this.onNotifyCallback = function(event) { 
            self.OnViewManagerChanges(event);
        };

        jsa.CopyParams(this,params);

        //internals
        this.view = null;
        
        if(createDom) {
            this.CreateDom();
        }

        //init
        let view = this.viewManager.GetChildById(this.viewId);
        this.AttacheToView(view);

        //start listen to Events
        //make the domain status tool listen to the domain statistics
        if(this.viewManager) {
            this.viewManager.StartObserving(this);
        }
        return this;
    };

    GoToViewTool.prototype = Object.create(jsa.Tool.prototype);
    jsa.Mixin(GoToViewTool,jsa.Observer);

    GoToViewTool.prototype.AttacheToView = function(view) {
        if(view) {
            this.view = view;
            this.GetDomElement().classList.remove(this.detachedStyle);
            //try to copy the icon
            let icon = view.icon;
            if(icon) {
                this.GetContainingDom().style.backgroundImage = "url("+icon+")";
            }
        }
    }

    GoToViewTool.prototype.DetachFromView = function(view) {
        this.GetDomElement().classList.add(this.detachedStyle);
    }

    GoToViewTool.prototype.OnClick = function(event) {
        if(this.view) {
            this.viewManager.ActivateView(this.view);
        }
    };

    GoToViewTool.prototype.OnViewManagerChanges = function(event,source) {
        if(jsa.EVENT.IS_INSTANCE(event,jsa.EVENT.TYPES.ADD_CHILD)) {
            let view = event.value;
            if(view.id == this.viewId) {
                this.AttacheToView(view);
            }
        } else if(jsa.EVENT.IS_INSTANCE(event,jsa.EVENT.TYPES.REMOVE_CHILD)){
            let view = event.value;
            if(view.id == this.viewId) {
                this.DetachFromView(view);
            }
        }
    };

    //@Override
    GoToViewTool.prototype.Dissolve = function() {
        if(this.viewManager) {
            this.viewManager.StopObserving(this);
        }
        jsa.Tool.prototype.Dissolve.call(this);
    };

    return {
        GoToViewTool : GoToViewTool
    };
})());

