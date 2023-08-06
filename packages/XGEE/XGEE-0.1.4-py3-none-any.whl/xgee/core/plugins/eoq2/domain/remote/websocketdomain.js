/*
*
* 2019 Bjoern Annighoefer
*/


var jseoq2 = jseoq2 || {};
eoq2.domain = eoq2.domain || {};
eoq2.domain.remote = eoq2.domain.remote || {};

Object.assign(eoq2.domain.remote,(function(){

    /*
    * Websocket domain
    */

    function EoqWebSocketCmdInfo(cmdId,resolve,reject,startTime,timeout) {
        this.cmdId = cmdId;
        this.resolve = resolve;
        this.reject = reject;
        this.startTime = startTime;
        this.timeout = timeout;
    };

    function WebSocketDomain(url,timeout=0,logger=new eoq2.util.NoLogging()) {
        eoq2.domain.Domain.call(this,logger);
        this.url = url;
        this.timeout = timeout; //no timeout
        this.sessionId = null; //set later

        this.serializer = new eoq2.serialization.JsonSerializer();
        
        //initialize a command queue
        this.cmdCounter = 0;
        this.cmdQueue = {};

        //initialize web socket
        this.ws = null;
        
        return this;
    };
    WebSocketDomain.prototype = Object.create(eoq2.domain.Domain.prototype);

    WebSocketDomain.prototype.Open = function() {
        let self = this;
        return new Promise(function(resolve,reject){ 
            let ws = new WebSocket(self.url);
            ws.onopen = function() {
                self.logger.Info('EOQ web socket connected to '+ self.url);
                resolve(self);
            };
            ws.onmessage = function (evt) {
                self.logger.PassivatableLog(eoq2.util.LogLevels.DEBUG,function(){return ('Web socket received: '+evt.data);});
                self.OnMessage(evt.data);
            };
            ws.onerror = function (err) {
                self.logger.Error('EOQ websocket Error:'+err);
            };
            ws.onclose = function(evt) {
                if (evt.code == 3001) {
                    self.logger.Info('ws closed');
                    self.ws = null;
                } else {
                    self.ws = null;
                    self.logger.Error('ws connection error');
                    reject(new Error('ws connection error'));
                }
            };
            self.ws = ws;
        });
    };

    WebSocketDomain.prototype.InitSession = function(user,passwort) {
        let self = this;
        return new Promise(function(resolve,reject){ 
            let cmd = new eoq2.command.Hel(user,passwort);
            self.Do(cmd).then(function(sessionId) {
                resolve(sessionId);
            }).catch(function(e) {
                reject(e);
            });
        });
    };


    WebSocketDomain.prototype.RawDo = function(cmd,version=eoq2.version) {
        let self = this;
        return new Promise(function(resolve,reject) {
            self.cmdCounter++;
            let cmdId = self.cmdCounter;
            self.logger.PassivatableLog(eoq2.util.LogLevels.DEBUG,function(){return ('Sending cmd '+cmdId+': '+cmd);});
            let startTime = new Date();
            let frame = new eoq2.frame.Frame(eoq2.frame.FrameTypes.CMD,cmdId,cmd,version);
            let frames = [frame];
            try {
                //let frameStr = JSON.stringify([frame]);
                let framesStr = self.serializer.Ser(frames);
                self.ws.send(framesStr);
                //store request information in the db in order to reply on message received
                self.cmdQueue[cmdId] = new EoqWebSocketCmdInfo(cmdId,resolve,reject,startTime,0);
                //inform about raw messages
                self.NotifyObservers([new eoq2.event.CusEvt("rawout",{time:startTime,frames:frames,framesStr:framesStr})],self);
            } catch(e) {
                self.logger.Error("Could not send frame:"+e.toString());
                res = new eoq2.Res(cmd.type,eoq2.ResTypes.ERR,e.toString());
                resolve(res);
            }
        });
    };

    /*
    * PRIVATE METHODS
    */

    WebSocketDomain.prototype.OnMessage = function(data) {
        //let frames = JSON.parse(data);
        let frames = this.serializer.Des(data);
        let endTime = new Date();
        let duration = 0;
        let evts = []; //collect all events in the message
        for(let i=0; i<frames.length; i++) {
            frame = frames[i]
            if(frame.eoq == eoq2.frame.FrameTypes.RES) {
                let resId = frame.uid;
                let res = frame.dat;
                this.logger.PassivatableLog(eoq2.util.LogLevels.DEBUG,function(){return ('Response for cmd '+resId+': '+res);});
                try {
                    let cmdInfo = this.cmdQueue[resId];
                    duration = endTime-cmdInfo.startTime
                    //this.logger.LogEnd(res,endTime-cmdInfo.startTime);
                    cmdInfo.resolve(res);
                    delete this.cmdQueue[resId];
                } catch {
                    //do nothing since this is a message that was not expected.
                    this.logger.Warn("Websocket Domain ("+this.url+"): Received result message with unknown id or broken content: "+ data);
                }
            } else if(frame.eoq == eoq2.frame.FrameTypes.EVT) {
                evts.push(frame.dat);
            } else {
                this.logger.Error("Websocket Domain ("+this.url+"): Received invalid message: "+ data);
            }
        }
        if(evts.length>0) {
            
            this.NotifyObservers(evts,this);
        }
        //notify the raw receival of the message
        this.NotifyObservers([new eoq2.event.CusEvt("rawin",{time:endTime,frames:frames,framesStr:data,duration:duration})],this);
    };

    return {
        WebSocketDomain : WebSocketDomain
    };

})());