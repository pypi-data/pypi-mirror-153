import GraphEvent from './GraphEvent.js'

export default class EventProvider{
    constructor(){
        this.events={};
    }
    initializer(){
        this.events={};
    }

    on(event,cb){
        if(this.events[event])
        {
            return this.events[event].addListener(cb)
        }
        else
        {
            return -1
        }
    }

    raise(event,evtData)
    {
        this.events[event].raise(evtData)
    }

    createEvent(event)
    {        
        this.events[event]=new GraphEvent()
        return this.events[event]
    }


}