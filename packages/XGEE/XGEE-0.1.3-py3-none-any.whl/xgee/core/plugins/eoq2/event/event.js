/*
*
* 2019 Bjoern Annighoefer
*/

var eoq2 = eoq2 || {};
eoq2.event = eoq2.event || {};

Object.assign(eoq2.event,(function() {

    var EvtTypes = {
        CHG : "CHG",  // change
        WAT : "WAT",  // watch event (not implemented)
        OUP : "OUP",  // output of a call
        INP : "INP",  // input for a call
        CST : "CST",  // call status change
        CVA : "CVA",  // call value change event
        MSG : "MSG",  // message event
        CUS : "CUS",  // custom event with user defined structure
    }
    
    var ChgTypes = {
        SET : 'SET',
        ADD : 'ADD',
        REM : 'REM',
        MOV : 'MOV',
		ADC : 'ADC',
		RMC : 'RMC',
    }

    ALL_EVENT_TYPES = [EvtTypes.CHG,EvtTypes.OUP,EvtTypes.INP,EvtTypes.CST,EvtTypes.CVA,EvtTypes.MSG,EvtTypes.CUS];
    
        
  
    function Evt(ctype,key,args) {
            this.evt = ctype;
            this.k = key;
            this.a = args;
    };
  
    function ChgEvt(cid,ctype,target,feature,newVal=None,oldVal=None,oldOwner=None,oldFeature=None,oldIndex=None,tid=0,user='',sessionNumber=0) {
        let key = target+":"+ctype+":"+feature;
        Evt.call(this,EvtTypes.CHG,key,[cid,ctype,target,feature,newVal,oldVal,oldOwner,oldFeature,oldIndex,tid,user,sessionNumber])
    }
        
        
    function OupEvt(callId,channelName,data) {
        let key = callId.toString();
        Evt.call(this,EvtTypes.OUP,key,[callId,channelName,data])
    };
    OupEvt.prototype = Object.create(Evt.prototype);
        
    function InpEvt(callId,channelName,data) {
        let key = callId.toString();
        Evt.call(this,EvtTypes.INP,key,[callId,channelName,data])
    };
    InpEvt.prototype = Object.create(Evt.prototype);
        
    function CstEvt(callId,status,info='') {
        let key = callId.toString();
        Evt.call(this,EvtTypes.CST,key,[callId,status,info]);
    };
    CstEvt.prototype = Object.create(Evt.prototype);
        
    function CvaEvt(callId,value) {
        let key = callId.toString();
        Evt.call(this,EvtTypes.CVA,key,[callId,value]);
    };
    CvaEvt.prototype = Object.create(Evt.prototype);

    function MsgEvt(key,msg) {
        Evt.call(this,EvtTypes.MSG,key,msg);
    };
    MsgEvt.prototype = Object.create(Evt.prototype);

    function CusEvt(key,data) {
        Evt.call(this,EvtTypes.CUS,key,data);
    };
    CusEvt.prototype = Object.create(Evt.prototype);
        
        
        
    /*
    *   EventProvider
    */
            
    function EvtProvider() {
        this.observers = new Map() // callbackFct -> event
    };

    EvtProvider.prototype.Observe = function(callbackFct,eventTypes=ALL_EVENT_TYPES) { //by default register for all events
        this.observers.set(callbackFct,eventTypes);
    };
        
    EvtProvider.prototype.Unobserve = function(self,callbackFct) {
        this.observers.delete(callbackFct)
    };
    
    EvtProvider.prototype.NotifyObservers = function(evts,excludedObserver=None) { //sends multiple events 
        let self = this;
        this.observers.forEach(function(allowedEvts,callback){
            let filterdEvts = evts.filter(function(e) {
                return allowedEvts.includes(e.evt)
            });
            try{
                if(0<filterdEvts.length) {
                    callback(filterdEvts,self)
                }
            } catch(e) {
                console.warn("EvtProvider: Warning observer callback failed:"+e)
            }
        });
    }; 

    return {
        EvtTypes : EvtTypes,
        ALL_EVENT_TYPES : ALL_EVENT_TYPES,
        ChgTypes : ChgTypes,
        Evt : Evt,
        ChgEvt : ChgEvt,
        OupEvt : OupEvt,
        MsgEvt : MsgEvt,
        CusEvt : CusEvt,
        EvtProvider : EvtProvider
    };

})());