function DomainStatusTool(params={},createDom=true) {
    jsa.Tool.call(this,params,false);
    jsa.Observer.call(this);
    
    //parameters
    this.domainInfo = 'UNKNOWN'
    this.domainStatistics = null;
    this.containerStyle = ['jsa-tool-container','tool-domain-status'];
    this.showTime = 100; //ms
    this.updateInProgress = false;
    this.updateDelay = 500; //ms
    this.activeStyle = 'tool-domain-status-up-down';
    this.onClickCallback = function (e) {
        this.ShowInfo();
    };
    this.onNotifyCallback = function(event) { 
        if(event.observable == this.domainStatistics && event.eventId == 'CHANGED') {
            this.NotifyActivity();
            this.UpdateBubble(event.data.stats);
            // if(this.infoBubble && this.infoBubble.visible) {
            //     let content = this.BuildInfoContent(event.data.stats);
            //     this.infoBubble.SetContent(content);
            // }
        }
    }

    jsa.CopyParams(this,params);

    //internals
    this.showTimeout = null;
    this.updateTimeout= null;
    this.isActive = false;
    this.infoBubble = null;
    this.bubbleContent = 'No information available';

    //start listen to Events
    //make the domain status tool listen to the domain statistics
    if(this.domainStatistics) {
        this.domainStatistics.StartObserving(this);
    }

    if(createDom) {
        this.CreateDom();
    }

    return this;
}

DomainStatusTool.prototype = Object.create(jsa.Tool.prototype);
jsa.Mixin(DomainStatusTool,jsa.Observer);

DomainStatusTool.prototype.NotifyActivity = function() {
    if(this.showTimeout) {
        window.clearTimeout(this.showTimeout);
    }
    this.SetStateActive();
    var self = this;
    this.showTimeout = window.setTimeout(function() {
        self.SetStateInactive();
    },this.showTime);
    return this;
};

DomainStatusTool.prototype.ShowInfo = function() {
    let app = this.GetApp();
    if(app) {
        if(!this.infoBubble) {
            this.infoBubble = new jsa.Bubble({
                name: '',
                enabled: true,
                resizable: false,
                content: '',
                minimizable: false, 
                autoHide: true,
                closeable: false,
                borderOffset: 25, //px
                penalityN: 0,
                penalityE: 2000,
                penalityS: 0,
                penalityW: 2000,
                style: ['tool-domain-status-info-bubble']
            });
            app.AddChild(this.infoBubble);
        }
        this.infoBubble.SetContent(this.bubbleContent);

        this.infoBubble.PopupOnDomElement(this.GetDomElement());
    }
    return this;
};

DomainStatusTool.prototype.SetStateActive = function() {
    if(!this.isActive) {
        this.GetContainingDom().classList.add(this.activeStyle);
        this.isActive = true;
    }
    return this;
};

DomainStatusTool.prototype.SetStateInactive = function() {
    if(this.isActive) {
        this.GetContainingDom().classList.remove(this.activeStyle);
        this.isActive = false;
    }
    return this;
};

DomainStatusTool.prototype.Dissolve = function() {
    if(this.infoBubble) {
        this.infoBubble.Dissolve();
    }
    if(this.updateTimeout) {
        window.clearTimeout(this.updateTimeout);
    }
    jsa.Tool.prototype.Dissolve.call(this);
}

// DomainStatusTool.prototype.UpdateInfo = function() {
//     if(this.infoBubble) {
//         let content = this.BuildInfoContent(this.domainStatistics.domain,this.domainStatistics.domain);
//         this.infoBubble.SetContent(content);
//     }
//     return this;
// };

DomainStatusTool.prototype.UpdateBubble = function(stats) {
    if(!this.updateInProgress) {
        this.updateInProgress = true;

        let actualStats = stats;
        let self = this;
        let delayedUpdater = function() {
            self.bubbleContent = self.BuildInfoContent(actualStats);
            if(self.infoBubble && self.infoBubble.visible) {
                self.infoBubble.SetContent(self.bubbleContent);
            }
            self.updateInProgress = false;
        }
        //do not update info for every event and not inside the event loop, because that degrades performance. Instead set an minimum update delay. 
        this.updateTimeout = window.setTimeout(delayedUpdater,this.updateDelay);
    }
};

DomainStatusTool.prototype.BuildInfoContent = function(stats) {
    
    content = '<p>Connected to '+this.domainInfo+'</p>';
    if(stats) {
        content +='<table>';
        for(let prop in stats) {
            content +='<tr><td>'+prop+'</td><td>'+stats[prop]+'</td></tr>';
        }
        content +='</table>';
    } else {
        content += 'No stats available.'
    }
    return content;
};

