// An event for selection changed operations
var eventBroker = eventBroker || {};
Object.assign(eventBroker,(function(){
    var SELECTION_CHANGED_EVENT_ID = "SELECTION/CHANGE";

    function SelectionChangedEvent(source=null,selection=[],domElements=[],data=null) {
        eventBroker.BasicEvent.call(this,"SelectionEvent",source,data);

        this.selection = selection; //the array of selected elements
        this.domElements = domElements;

    };

    SelectionChangedEvent.prototype = Object.create(eventBroker.BasicEvent.prototype);

    return {
        SELECTION_CHANGED_EVENT_ID : SELECTION_CHANGED_EVENT_ID,
        SelectionChangedEvent : SelectionChangedEvent
    };
})());


