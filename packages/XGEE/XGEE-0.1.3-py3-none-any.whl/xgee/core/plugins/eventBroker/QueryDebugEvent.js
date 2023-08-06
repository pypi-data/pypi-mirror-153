// The basic event of the event broker. All other event classes should inherit from this
// 2020 Bjoern Annighoefer

var eventBroker = eventBroker || {};
Object.assign(eventBroker,(function(){
    function BasicEvent(type="BasicEvent",source=null,data=null) {
        this.type = type; //String denoting the type of event
        this.source = source; //the producer of the event
        this.data = data; //custom data attached to the event
    }
    return {
        BasicEvent : BasicEvent
    };
})());