/*
 * 2019 Bjoern Annighoefer
*/

var eoq2 = eoq2 || {};
eoq2.util = eoq2.util || {};

Object.assign(eoq2.util,(function() {

    var LogLevels = {
        DEBUG : "debug",
        INFO : "info",
        WARN : "warn",
        ERROR : "error"
    };

    var DEFAULT_LOG_LEVELS = [LogLevels.INFO,LogLevels.WARN,LogLevels.ERROR];

    function Logger(activeLevels=DEFAULT_LOG_LEVELS) {
            this.activeLevels = activeLevels;
    };
        
    Logger.prototype.ShallLog = function() {
        return true;
    };
    
    Logger.prototype.Log = function(level,msg) {
        if(this.activeLevels.includes(level) && this.ShallLog()) {
            this._Log(level,msg);
        }
    };
            
    Logger.prototype.PassivatableLog = function(level,func) {
        if(this.activeLevels.includes(level) && this.ShallLog()) {
            this._Log(level,func());
        }
    };
    
    Logger.prototype.Debug = function(msg) {
        this.Log(LogLevels.DEBUG, msg);
    }
    
    Logger.prototype.Info = function(msg) {
        this.Log(LogLevels.INFO,msg)
    };
        
    Logger.prototype.Warn = function(msg) {
        this.Log(LogLevels.WARN,msg)
    };
        
    Logger.prototype.Error = function(msg) {
        this.Log(LogLevels.ERROR,msg)
    };
        
    //the following must be overwritten to produce the output
    Logger._Log = function(level,msg) {
        throw new Error("Not implemented");
    };
        
        
    /*
    * A default logger which does nothing
    */

    function NoLogging() {
        Logger.call(this);
    };
    NoLogging.prototype = Object.create(Logger.prototype);
        
    //@Override
    NoLogging.prototype.ShallLog = function() {
        return false;
    };
    
    
    /*
    * A default logger which does nothing
    */

    function ConsoleLogger(activeLevels=DEFAULT_LOG_LEVELS) {
        Logger.call(this,activeLevels);
    };
    ConsoleLogger.prototype = Object.create(Logger.prototype);

    ConsoleLogger.prototype._Log = function(level,msg) {
        switch(level) {
            case LogLevels.DEBUG:
                console.debug(msg);
                break;
            case LogLevels.INFO:
                console.info(msg);
                break;
            case LogLevels.WARN:
                console.warn(msg);
                break;
            case LogLevels.ERROR:
                console.error(msg);
                break;
            default:
                console.log(level + ": "+msg);
        }
    };

    return {
        LogLevels : LogLevels,
        DEFAULT_LOG_LEVELS : DEFAULT_LOG_LEVELS,
        Logger : Logger,
        NoLogging : NoLogging,
        ConsoleLogger : ConsoleLogger
    };
})());


