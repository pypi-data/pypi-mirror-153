// 2020 Bjoern Annighoefer

export function init(pluginApi,config) { 

    var scriptIncludes=[
    ];

    var stylesheetIncludes=[
        "css/ViewsTabbar.css"
    ]; 

    //basic plug-in initialization routine    
    return pluginApi.loadScripts(scriptIncludes).then(function(){ 
        return pluginApi.loadStylesheets(stylesheetIncludes).then(function(){ 
            //register to autostart in order to get started, when the basic GUI is available
            pluginApi.implement('autostart',new autostart.Autostarter("viewsTabbar",'APP/STARTUP/MENU',function() {
                let params = config;
                //now add the tabbar
                let app = pluginApi.getGlobal('app'); 
                if(app) {
                    //create a new tabbar
                    let tabbar = new jsa.Tabbar({
                        style: ['jsa-tabbar','jsa-tabbar-top','views-tabbar']
                    });
                    app.AddChild(tabbar);
                    //Sync it with the default view manager
                    tabbar.SyncWithViewManager(app.viewManager,params.syncWithHeaderStyles);
                    //change the style of the default view manager to make the tabbar visibel
                    app.viewManager.GetDomElement().classList.add('views-tabbar-view-manager-mod');
                    //expose this tabbar to the globals
                    pluginApi.setGlobal('viewsTabbar',tabbar)
                } else {
                    console.warn("Plugin viewsTabbar did not find an app to bind to. Plugin is not active.")
                }  
            })); 
        });   
    });
};

export var meta={
    "id":"viewsTabbar",
    "description":"Adding a tabbar on top of the default view manager of the app",
    "author":"Bjoern Annighoefer",
    "version":"1.0.0",
    config : {
        syncWithHeaderStyles : true
    },
    "requires":[
        "autostart"
    ]
};



