// This is the baseclass for all plugins that would like to use the autostart mechanism. 
// Either Autostarter can be instantiated with the given level and init function, or a 
// custom autostart instance has to be derived.  
// 2020 Bjoern Annighoefer

var autostart = autostart || {};

Object.assign(autostart,(function(){
    function Autostarter(name,level="COMPLETE",initCallback=null,priority=10) {
        this.name = name;
        this.level = level;
        this.initCallback = initCallback;
        this.priority = priority
    };
    
    Autostarter.prototype.GetName = function() {
        return this.name; 
    };

    Autostarter.prototype.GetLevel = function() {
        return this.level; 
    };

    Autostarter.prototype.GetPriority = function() {
        return this.priority; 
    };
    
    Autostarter.prototype.Init = function() {
        //must return a promise in order to support delayed loading
        var res = this.initCallback();
        //must return a promise in order to support delayed loading
        return Promise.resolve(res)
    };

    return {
        Autostarter : Autostarter
    }
})());