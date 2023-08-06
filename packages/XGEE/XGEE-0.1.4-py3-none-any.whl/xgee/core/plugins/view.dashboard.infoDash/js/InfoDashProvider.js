// 2020 Bjoern Annighoefer

var INFO_DASH = INFO_DASH || {};

Object.assign(INFO_DASH,(function(){
    function InfoDashProvider(pluginApi,name,params) {
        
        //params
        this.name = 'Start Modelling';
        this.content = 'Any HTML text';
        this.tiles = 2; //relative width in the range of 1-12, where 12 is 100%
        this.row = 0;
        this.dashboardId = '#DASHBOARD';
        this.position = 0;
        Object.assign(this,params); //copy params

        DASHBOARD_VIEW.DashProvider.call(this,name,params.row,params.dashboardId,params.position);

        //internals
        this.app = pluginApi.getGlobal('app'); 
        this.pluginApi = pluginApi;
    } 
    InfoDashProvider.prototype = Object.create(DASHBOARD_VIEW.DashProvider.prototype);

    //@Overwrite
    InfoDashProvider.prototype.CreateDash = function() {
        //Create new dash
        let dash = new jsa.Dash({
            name : this.name,
            content : this.content,
            tiles: this.tiles, 
        });

        return dash;
    };

    return {
        InfoDashProvider : InfoDashProvider
    };
})());