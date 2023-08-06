export default class GraphEvent{
    constructor(enabled=true){
        this.listeners=[];
        this.enabled=enabled;
    }

    raise(eventData){
        if(this.enabled){
            this.listeners.forEach(function(callback){
                callback(eventData);
            });
        }
    }

    enable(){
        this.enabled=true;
    }

    disable(){
        this.enabled=false;
    }

    addListener(callbackFunction){
        this.listeners.push(callbackFunction)
        let listenerId=this.listeners.length-1
        return listenerId
    }

    removeListener(listenerId){
        this.listeners=this.listeners.splice(listenerId,1)
        return true
    }

    removeListenerByFunction(callbackFunction){
        var found=false;
        this.listeners=this.listeners.filter(function(e){
            if(e!=callbackFunction)
            {
                return true
            }
            else
            {
                found=true;
            }
        })
        return found
    }
}