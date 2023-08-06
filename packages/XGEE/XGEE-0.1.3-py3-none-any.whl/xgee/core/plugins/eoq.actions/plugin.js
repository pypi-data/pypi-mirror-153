export function init(pluginAPI,config) {  
    //plug-in statics and configuration
    var scriptIncludes=[
        "js/ActionsController.js",
        "js/ActionsCore.js",
        "js/ActionsUi.js"
    ];

    var stylesheetIncludes=[
        "css/ActionsUi.css"
    ];
    
    //init the plug-in
    return pluginAPI.loadScripts(scriptIncludes).then(function(){ 
        return pluginAPI.loadStylesheets(stylesheetIncludes).then(function(){ 
            //create an properties view controller that handles all the logic stuff.
            let actionsController = new ACTIONS.ActionsController(pluginAPI,config);
            
            //register to autostart in order to get started, when the GUI is available
            pluginAPI.implement('autostart',new autostart.Autostarter("eoq.actions",'APP/STARTUP/DATA',function() {
                actionsController.Init();
            })); 

            return Promise.resolve(); });   
        });
};


export var meta={
    id : "eoq.actions",
    description : "Enables the execution of actions on EOQ models",
    author : "Bjoern Annighoefer",
    version : "1.0.0",
    config : {
        menuId : '#ACTIONS',
        menuName : 'Action',
        appendBefore: false, 
        appendMenuId: null, //if none is given, the menu is attached at the beginning or end.
        actionFilterFunction: action => !action.tags.includes("advanced") || window.location.search.includes('advanced')
    },
    requires :[
        "autostart",
        "eventBroker",
        "ecoreSync.ui"
    ]
};



