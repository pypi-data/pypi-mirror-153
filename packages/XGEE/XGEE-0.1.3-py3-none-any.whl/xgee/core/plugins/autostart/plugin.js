// AUTOSTART PLUGIN
// This plug-in enables other plugins to be initialized at certain stages of the app initialization.
// Precisely it allows plugins to be initialized on any event released throug the event broker.
// The default events for the app initialization are.
// level "APP/STARTUP/INIT": The $app variable is ready, but nothing else
// level "APP/STARTUP/DATA": The data connection (e.g. ecore sync, eoq, database, ...) is established. Good to add database relient plug-ins here. 
// level "APP/STARTUP/MENU": The menu is initialized. Good to add custom menu extensions here.
// level "APP/STARTUP/TOOLS":  The toolbar is initialized. Good to add custom tools here.
// level "APP/STARTUP/VIEW":  The view manager is initialized good to add custom views here
// level "APP/STARTUP/END": The app is completly initialized and all graphical components are ready
// 2020 Bjoern Annighoefer

export function init(pluginAPI) { 
    //static methods and propertiesView
    var AUTO_START_EXT_ID = "autostart";

    var scriptIncludes=[
        "js/AppStartupEvent.js",
        "js/AppStartupObserver.js",
        "js/Autostarter.js"
    ];

    var stylesheetIncludes=[ ]; 

    //startup event callback
    function OnAppStatusChange(evt) {
        let level = evt.topic;
        let activeAutostarters=pluginAPI.evaluate(AUTO_START_EXT_ID).filter(function(autostarter){
            return (level == autostarter.GetLevel());
        }).sort(function(a,b) {
            a.GetPriority() - b.GetPriority();
        });
    
        for(let i=0;i<activeAutostarters.length;i++) {
            let activeAutostarter = activeAutostarters[i];
            try {
                activeAutostarter.Init();
            } catch(e) {
                console.error("AUTOSTARTER: Failed to start "+activeAutostarter.GetName()+" at level "+ level +" ("+activeAutostarter.GetPriority()+"): "+e.toString());
            }
        }
    };

    //plug-in initialization
    return pluginAPI.loadScripts(scriptIncludes).then(function(){ 
        return pluginAPI.loadStylesheets(stylesheetIncludes).then(function(){ 
            //exhibit internal classes
            pluginAPI.expose({
                Autostarter : autostart.Autostarter
            });  
            //exhibit extension points
            pluginAPI.provide(AUTO_START_EXT_ID,autostart.Autostarter);

            var eventBroker=pluginAPI.require('eventBroker');
            eventBroker.subscribe("APP/STARTUP/*",OnAppStatusChange);
            
            //forward js application events if posible 
            //register and forward some default events
            let app = pluginAPI.getGlobal('app');
            if(app) {
                let appStartupObserver = new autostart.AppStartupObserver(app,eventBroker);
                app.StartObserving(appStartupObserver);
            }
            return Promise.resolve(); 
        });   
    });
};

export var meta={
    "id":"autostart",
    "description":"A plug-in taht enables other plug-ins to be initialized at different stages of the app start-up procedure.",
    "author":"Bjoern Annighoefer",
    "version":"1.0.0",
    "requires":[
        "eventBroker"
    ]
};



