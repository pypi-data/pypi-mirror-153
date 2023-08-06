export function init(pluginAPI,config) {  
    //plug-in statics and configuration
    var scriptIncludes=[
        "js/StartModellingDashListEntry.js",
        "js/StartModellingDash.js",
        "js/StartModellingDashProvider.js"
    ];

    var stylesheetIncludes=[
        "css/StartModellingDash.css"
    ];
    
    //init the plug-in
    return new Promise(function(resolve,reject) {
        pluginAPI.loadScripts(scriptIncludes).then(function(){ 
            pluginAPI.loadStylesheets(stylesheetIncludes).then(function(){ 
                for(let i=0;i<config.instances.length;i++) {
                    let params = config.instances[i];

                    let dashName = pluginAPI.getMeta().id+"("+params.name+")";
                    let provider = new START_MODELING_DASH.StartModellingDashProvider(pluginAPI,dashName,params);
                    pluginAPI.implement(DASHBOARD_VIEW.DASH_EXT_POINT_ID,provider);
                }
                resolve(true);
            });   
        });
    });
};

export var meta={
    id : "dashboardView.startModellingDash",
    description : "Adds a dash element beeing a starting point for model interactions",
    author : "Bjoern Annighoefer",
    version : "1.0.0",
    config : {
        instances : [
            {
                name: 'Start Modelling',
                modelSuffix: '.oaam',
                existingSectionLabel: 'Open existing model',
                createNewSectionLabel: 'Create new model',
                createTemplate: null, //path to a blueprint which is copied on creation
                preferredEditors: [], //names of editors
                row : 0, //a dashboard must be configured to a number rows
                tiles : 4, //relative width in the range of 1-12, where 12 is 100% 
                position : 1, //the lower the position, the more left the dash is in its row
                dashboardId : '#DASHBOARD', //referres to the dashboard, when multiple dashboard views shall be created.
                ecoreSyncId : 'ecoreSync' //the ecoreSync object used to retrieve the data
            }
        ]
    },
    requires :[
        "view.dashboard",
        "ecoreSync",
        "eventBroker"
    ]
};



