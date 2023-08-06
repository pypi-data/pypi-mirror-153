// A central update handler for all active instance of EObject Ctrls
// Will add on update callbacks if not attached to an eObject.
// Will remove callbacks if nobody listens to the eObject any more.
// Bjoern Annighoefer 2020

var ECORESYNC_UI = ECORESYNC_UI || {};

Object.assign(ECORESYNC_UI,(function(){

    /* Internal Data structures */
    function CtrlEntry(ctrl,callback) {
        this.ctrl = ctrl;
        this.callback = callback;
    };

    function EventEntry(eventType,featureName) {
        this.eventType = eventType;
        this.featureName = featureName;
        this.ctrls = new Map();
    };

    function EObjectEntry(eObject) {
        this.eObject = eObject;
        this.events = new Map();
    };

    /* GLOBALS  */
    // This is the central update handler that distributes changes to all regitered listeners
    // Attention, this functions will not he called in the scope of EOjectCtrlUpdateHanlder, so this is meaningless
    function GenEventStr(eventType,featureName) {
        return eventType+":"+featureName;
    }


    function HandleUpdate(eventType,change) {
        let featureName = change.eContainingFeature.get('name');
        let eObject = change.eContainer;
        let eventStr = GenEventStr(eventType,featureName);
        //find the matchin controls to be updated
        let oid = ecoreSync.rlookup(eObject);
        let ctrls = ECORESYNC_UI.EObjectCtrlUpdateHandler.eObject.get(oid).events.get(eventStr).ctrls;

        //call all controlls with the necessary information
        for(let [key, value] of ctrls) {
            let ctrl = value.ctrl;
            let callback = value.callback;
            callback(eObject,eventType,featureName,ctrl);
        }
    }

    function HandleChange(change) {
        HandleUpdate('change',change);
    };

    function HandleAdd(change) {
        HandleUpdate('add',change);
    };

    function HandleRemove(change) {
        HandleUpdate('remove',change);
    };

    /* EOBJECTCTRLUPDATE HANDLER */
    function EObjectCtrlUpdateHandler() {
        this.objects = new Map();
        return this;
    };

    EObjectCtrlUpdateHandler.prototype.Observe = function(eObject,eventType,featureName,ctrl,callback) {
        //see if the object is alrady observed
        let oid = eObject.get('_#EOQ');
        let objectEntry = this.objects.get(oid);
        if(!objectEntry) {
            objectEntry = new EObjectEntry(eObject);
            this.objects.set(oid,objectEntry); //add a new entry
        }
        //see if the event is already observed
        let eventStr = GenEventStr(eventType,featureName);
        let eventEntry = objectEntry.events.get(eventStr);
        if(!eventEntry) {
            eventEntry = new EventEntry(eventType,featureName);
            objectEntry.events.set(eventStr,eventEntry);
            switch(eventType) {
                case "change":
                    eObject.on(eventStr,HandleChange);
                    break;
                case "add":
                    eObject.on(eventStr,HandleAdd);
                    break;
                case "remove":
                    eObject.on(eventStr,HandleRemove);
                    break;
                default:
                    throw new Error("Unknown event type to observe: "+eventType);
            }
        }
        //each ctrl is only allowed to listen once to each event type, so overwirte any existing ctrl registration
        let ctrlEntry = new CtrlEntry(ctrl,callback);
        let ctrlId = ctrl.id; //this relies on unique ids
        eventEntry.ctrls.set(ctrlId,ctrlEntry);
    };

    EObjectCtrlUpdateHandler.prototype.Unobserve = function(eObject,eventType,featureName,ctrl) {
        //see if the object is alrady observed
        let oid = eObject.get('_#EOQ');
        let objectEntry = this.objects.get(oid);
        if(objectEntry) {
            let eventStr = GenEventStr(eventType,featureName);
            let eventEntry = objectEntry.events.get(eventStr);
            if(eventEntry) {
                let ctrlId = ctrl.id; //this relies on unique ids
                eventEntry.ctrls.delete(ctrlId); //delete without checking
                //if the event has no more ctrs, unregister the event handlers
                if(0==eventEntry.ctrls.size) {
                    switch(eventEntry.eventType) {
                        case "change":
                            eObject.off(eventStr,HandleChange);
                            break;
                        case "add":
                            eObject.off(eventStr,HandleAdd);
                            break;
                        case "remove":
                            eObject.off(eventStr,HandleRemove);
                            break;
                        default:
                            //Can never go here, since unknown event types are never registerd
                            throw new Error("Unknown event type to unobserve: "+eventType);
                    }
                    objectEntry.events.delete(eventStr);
                }
            }
            //if the object has no more events delete it from the observation list
            if(0==objectEntry.events.size) {
                this.objects.delete(oid);
            }
        }
    };

  

    return {
        EObjectCtrlUpdateHandler : new EObjectCtrlUpdateHandler() //create the only instance
    }
    

})());