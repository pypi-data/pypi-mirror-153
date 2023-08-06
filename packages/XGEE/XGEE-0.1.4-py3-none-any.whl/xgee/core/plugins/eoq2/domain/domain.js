/*
*
* 2019 Bjoern Annighoefer
*/

var eoq2 = eoq2 || {};
eoq2.domain = eoq2.domain || {};

Object.assign(eoq2.domain,(function(){

    function Domain(logger=new eoq2.util.NoLogging()) {
        eoq2.event.EvtProvider.call(this);
        this.logger = logger;
    }

    Domain.prototype = Object.create(eoq2.event.EvtProvider.prototype);

    Domain.prototype.RawDo = function(cmd) {
        throw new Error("Not implemented");
    };

    Domain.prototype.Do = function(cmd) {
        let self = this;
        return new Promise(function(resolve,reject) {
            self.RawDo(cmd).then(function(res) {
                let value = eoq2.ResGetValue(res);
                resolve(value);
            }).catch(function(e){
                reject(e);
            });
        });
    }

    Domain.prototype.Get = function(target) {
        throw new Error("Not implemented");
    };
    

    return {
        Domain : Domain
    };

})());