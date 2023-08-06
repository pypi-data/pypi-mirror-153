export function init(pluginAPI,config) {  
    //plug-in statics and configuration
    var scriptIncludes=[
        "js/ViewsMenuController.js"
    ];

    var stylesheetIncludes=[
    ];
    
    //init the plug-in
    return pluginAPI.loadScripts(scriptIncludes).then(function(){ 
        return pluginAPI.loadStylesheets(stylesheetIncludes).then(function(){ 
            //create an properties view controller that handles all the logic stuff.
            let viewsMenuController = new VIEWSMENU.ViewsMenuController(pluginAPI,config);
            
            //register to autostart in order to get started, when the GUI is available
            pluginAPI.implement('autostart',new autostart.Autostarter("viewsMenu",'APP/STARTUP/VIEWS',function() {
                viewsMenuController.Init();
            })); 

            return Promise.resolve(); });   
        });
};

export var meta={
    id : "viewsMenu",
    description : "Adds a menu entry that shows all open views",
    author : "Bjoern Annighoefer",
    version : "1.0.0",
    config : {
        menuId : '#VIEWS',
        menuName : 'Views',
        appendBefore: false, 
        appendMenuId: null, //if none is given, the menu is attached at the beginning or end.
    },
    requires :[
        "autostart",
    ]
};



