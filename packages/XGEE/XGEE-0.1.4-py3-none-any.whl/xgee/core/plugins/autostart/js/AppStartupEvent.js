// An event for selection changed operations
var autostart = autostart || {};
Object.assign(autostart,(function(){
    var APP_STARTUP_EVENT_BASE_ID = "APP/STARTUP/";

    function AppStartupEvent(source=null,level=null,app=null,data=null) {
        eventBroker.BasicEvent.call(this,"AppStartupEvent",source,data);
        this.level = level;
        this.app = app; 

    };

    AppStartupEvent.prototype = Object.create(eventBroker.BasicEvent.prototype);

    return {
        APP_STARTUP_EVENT_BASE_ID : APP_STARTUP_EVENT_BASE_ID,
        AppStartupEvent : AppStartupEvent
    };
})());


