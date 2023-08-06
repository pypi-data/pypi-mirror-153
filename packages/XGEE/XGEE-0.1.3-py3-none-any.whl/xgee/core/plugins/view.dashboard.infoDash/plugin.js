export function init(pluginAPI,config) {  
    //plug-in statics and configuration
    var scriptIncludes=[
        "js/InfoDashProvider.js",
    ];

    var stylesheetIncludes=[
    ];
    
    //init the plug-in
    return pluginAPI.loadScripts(scriptIncludes).then(function(){ 
        return pluginAPI.loadStylesheets(stylesheetIncludes).then(function(){ 
            for(let i=0;i<config.instances.length;i++) {
                let params = config.instances[i];
                //create a provider which handles the dash creation if demanded.
                let dashName = pluginAPI.getMeta().id+"("+params.name+")";
                let provider = new INFO_DASH.InfoDashProvider(pluginAPI,dashName,params);
                pluginAPI.implement(DASHBOARD_VIEW.DASH_EXT_POINT_ID,provider);
            }
            return Promise.resolve(); });   
        });
};

export var meta={
    id : "view.dashboard.infoDash",
    description : "Adds a dash element beeing a starting point for model interactions",
    author : "Bjoern Annighoefer",
    version : "1.0.0",
    config : {
        instances : [
            {
                name: 'Start Modelling',
                content: 'Any HTML text',
                row : 0, //a dashboard must be configured to a number rows
                tiles : 4, //relative width in the range of 1-12, where 12 is 100% 
                position : 1, //the lower the position, the more left the dash is in its row
                dashboardId : '#DASHBOARD' //referres to the dashboard, when multiple dashboard views shall be created.
            }
        ]
    },
    requires :[
        "view.dashboard",
    ]
};



