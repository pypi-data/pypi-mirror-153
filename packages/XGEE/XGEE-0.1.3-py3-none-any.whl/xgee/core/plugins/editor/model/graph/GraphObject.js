import TransactionObject from './TransactionObject.js'


export default class GraphObject extends TransactionObject{
    constructor(){
        super();
        this.parent=null;
        var uuid = new Uint32Array(1);
        this.uuid=window.crypto.getRandomValues(uuid).toString();
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
    
    getUUID(){
        return this.uuid;
    }

}