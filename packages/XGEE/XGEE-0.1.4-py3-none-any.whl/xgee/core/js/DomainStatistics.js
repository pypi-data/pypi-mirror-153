function DomainStatitics(domain) {
    jsa.Observable.call(this);

    this.domain = domain;
    //this.domain.SetLogger(this);

    let self = this;
    this.onDomainEventCallback = function(evts,src) {
        self.OnDomainEvent(evts,src);
    }
    this.domain.Observe(this.onDomainEventCallback,[eoq2.event.EvtTypes.CUS]);

    //statistics
    let startTime = new Date();
    this.stats = {
        currentChangeId: 0,
        currentTransactionId: 0,
        currentResponseTime: 0,
        totalTransactionTime: 0,
        totalBytesSend: 0,
        totalBytesReceived: 0,
        numberOfCommands: 0,
        numberOfTransactions: 0,
        averageTransactionDuration: 0.0,
        totalTime: 0,
        startTime: startTime
    };
};

DomainStatitics.prototype = Object.create(jsa.Observable.prototype);

DomainStatitics.prototype.OnDomainEvent = function(evts,src) {
    for(let i=0;i<evts.length;i++) {
        let evt = evts[i];
        let type = evt.a[0];
        let data = evt.a[1];
        switch(type) {
            case "rawout":
                this.HandleRawOut(data);
                break;
                
            case "rawin":
                this.HandleRawIn(data);
                break;
        };
    }
    var nSubcommands = 1;
    if(command.type == jseoq.model.CommandTypesE.COMPOUND) {
        nSubcommands = command.commands.length;
    }
    this.stats.numberOfCommands += nSubcommands;
    this.stats.numberOfTransactions++;
    this.stats.totalBytesSend += commandStr.length;

    this.Notify(new jsa.ObservedEvent(this,'CHANGED', {
        stats : this.stats,
        domain : this.domain
    }));
};

DomainStatitics.prototype.HandleRawOut = function(data) {
    let frames = data.frames;
    let framesStr = data.framesStr;

    var nSubcommands = 0;
    let frame = frames[0];
    if(frame.eoq==eoq2.frame.FrameTypes.CMD && frame.ver>=200) {
        nSubcommands = 1;
        let cmd = frame.dat;
        if(cmd.cmd == eoq2.CmdTypes.CMP) {
            nSubcommands = cmd.a.length;
        }
    }

    this.stats.numberOfCommands += nSubcommands;
    this.stats.numberOfTransactions++;
    this.stats.totalBytesSend += framesStr.length;

    this.Notify(new jsa.ObservedEvent(this,'CHANGED', {
        stats : this.stats,
        domain : this.domain
    }));
};

DomainStatitics.prototype.HandleRawIn = function(data) {
    let frames = data.frames;
    let timeEllapsed = data.duration;
    let framesStr = data.framesStr;

    let currentTime = new Date();
    this.stats.totalTime = currentTime-this.stats.startTime;
    this.stats.totalBytesReceived += framesStr.length;
    this.stats.totalTransactionTime += timeEllapsed;
    this.stats.averageTransactionDuration = this.stats.averageTransactionDuration+(timeEllapsed-this.stats.averageTransactionDuration)/this.stats.numberOfTransactions;
    this.stats.currentResponseTime = timeEllapsed;

    let frame = frames[0];
    if(frame.eoq==eoq2.frame.FrameTypes.RES && frame.ver>=200) {
        let res = frame.dat;
        this.stats.currentChangeId = res.c;
        this.stats.currentTransactionId = res.n;
    }

    this.Notify(new jsa.ObservedEvent(this,'CHANGED', {
        stats : this.stats,
        domain : this.domain
    }));
};