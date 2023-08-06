var autostart = autostart || {};

Object.assign(autostart,(function(){
    function AppStartupObserver(app,eventBroker){
        jsa.Observer.call(this, {
            onNotifyCallback: this.OnAppStatusChange 
        });
        this.app = app;
        this.eventBroker = eventBroker;
    };
    AppStartupObserver.prototype = Object.create(jsa.Observer);
    
    AppStartupObserver.prototype.OnAppStatusChange = function(event) {
        if(jsa.EVENT.IS_INSTANCE(event,jsa.EVENT.TYPES.SET_STARTUP_LEVEL)) {
            let level = event.value;
            let appStartupEvent = new autostart.AppStartupEvent(this,level,this.app);
            this.eventBroker.publish(autostart.APP_STARTUP_EVENT_BASE_ID+level,appStartupEvent);
        }
    };

    return {
        AppStartupObserver : AppStartupObserver
    }
})());


