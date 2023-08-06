export function init(pluginAPI,config) {  
    //plug-in statics and configuration
    var scriptIncludes=[
        "js/DashboardViewProvider.js",
        "js/DashProvider.js",
    ];

    var stylesheetIncludes=[
        "css/DashboardView.css"
    ];
    
    //init the plug-in
    return pluginAPI.loadScripts(scriptIncludes).then(function(){ 
        return pluginAPI.loadStylesheets(stylesheetIncludes).then(function(){ 
            //see if there are instances to be created
            let providers = {};
            for(let i=0; i<config.instances.length;i++) {
                let params = config.instances[i];
                //create an properties view controller that handles all the logic stuff.
                let dashboardViewProvider = new DASHBOARD_VIEW.DashboardViewProvider(pluginAPI,params);
            
                //register to autostart in order to get started, when the GUI is available
                let name = pluginAPI.getMeta().id;
                pluginAPI.implement(VIEWS.VIEW_EXT_POINT_ID,dashboardViewProvider); 

                providers[params.viewId] = dashboardViewProvider; //store for events
            }
            //provide an extension point
            pluginAPI.provide(DASHBOARD_VIEW.DASH_EXT_POINT_ID,DASHBOARD_VIEW.DashProvider,function(evt) {
                let provider = evt.extension;
                if(evt.id=="IMPLEMENT" && providers[provider.viewId]) {
                    providers[provider.viewId].OnPluginImplement(evt);
                }
            });
            
            return Promise.resolve();
        });   
    });
};

export var meta={
    id : "view.dashboard",
    description : "Opens a view that can contain dash ui elements",
    author : "Bjoern Annighoefer",
    version : "1.0.0",
    config : {
        instances : [{
            viewId : '#DASHBOARD',
            position : 0,
            viewName : 'Dashboard',
            hasHeader : true,
            //viewIcon : pluginApi.getPath()+'img/view-dashboard.svg',
            viewStyle : 'dashboard-view',
            rows : 3, //number of rows that are created
            closable : false, //wheter the view can be closed
            activateView: true //activate on start
        }]
    },
    requires :[
        "views",
    ]
};



