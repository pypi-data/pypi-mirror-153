var jseoq = jseoq || {};
jseoq.domains = jseoq.domains || {};

jseoq.domains.Domain = (function() {
    function Domain() {
        this._logger = null;
        return this;
    }

    Domain.prototype.Do = function(command,successCallback=null,failCallback=null) {
        throw('Abstract, not implemented!');
    };

    Domain.prototype.DoSync = function(command) {
        throw('Abstract, not implemented!');
    };

    Domain.prototype.DoFromStr = function(commandStr,successCallback=null,failCallback=null) {
        var cmd = jseoq.CommandParser.StringToCommand(commandStr);
        return this.Do(cmd,successCallback,failCallback);
    };

    Domain.prototype.SetLogger = function(logger) {
        this._logger = logger;
    };

    Domain.prototype.GetLogger = function() {
        return this._logger;
    };

    return Domain;
})();