// 2020 Bjoern Annighoefer

var DASHBOARD_VIEW = DASHBOARD_VIEW || {};

Object.assign(DASHBOARD_VIEW,(function(){
    function DashProvider(providerId,row,dashboardId,position) {
        this.providerId = providerId;
        this.row = row;
        this.dashboardId = dashboardId;
        this.position = position;
    } 

    DashProvider.prototype.CreateDash = function() {
        //to be overwritten
    };

    
    return {
        DashProvider : DashProvider
    };
})());