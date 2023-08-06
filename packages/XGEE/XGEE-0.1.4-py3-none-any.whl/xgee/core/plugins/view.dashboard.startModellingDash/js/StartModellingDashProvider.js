// 2020 Bjoern Annighoefer

var START_MODELING_DASH = START_MODELING_DASH || {};

Object.assign(START_MODELING_DASH,(function(){
    function StartModellingDashProvider(pluginApi,name,params) {
        
        //params
        this.name = 'Start Modelling';
        this.modelSuffix = '.oaam';
        this.existingSectionLabel = 'Open existing model';
        this.createNewSectionLabel = 'Create new model';
        this.createTemplate = null;
        this.preferredEditors = [];
        this.row = 0; //a dashboard must be configured to a number rows
        this.tiles = 2; //relative width in the range of 1-12, where 12 is 100%
        this.position = 1; //the lower the position, the more left the dash is in its row 
        this.dashboardId = '#DASHBOARD';
        this.ecoreSyncId = 'ecoreSync'
        Object.assign(this,params); //copy params

        DASHBOARD_VIEW.DashProvider.call(this,name,this.row,this.dashboardId,this.position);

        //internals
        this.app = pluginApi.getGlobal('app'); 
        this.pluginApi = pluginApi;
        this.ecoreSync = pluginApi.require('ecoreSync').getInstanceById(this.ecoreSyncId);
        this.eventBroker = pluginApi.require('eventBroker');
    } 
    StartModellingDashProvider.prototype = Object.create(DASHBOARD_VIEW.DashProvider.prototype);

    //@Overwrite
    StartModellingDashProvider.prototype.CreateDash = function() {
        //Create new dash
        let dash = new START_MODELING_DASH.StartModelingDash({
            name : this.name,
            modelSuffix : this.modelSuffix,
            existingSectionLabel : this.existingSectionLabel,
            createNewSectionLabel : this.createNewSectionLabel,
            createTemplate : this.createTemplate,
            preferredEditors : this.preferredEditors,
            tiles: this.tiles, 
            domain : this.app.domain,
            legacyDomain : this.app.legacyDomain,
            ecoreSync : this.ecoreSync,
            eventBroker :this.eventBroker
        });

        return dash;
    };

    return {
        StartModellingDashProvider : StartModellingDashProvider
    };
})());