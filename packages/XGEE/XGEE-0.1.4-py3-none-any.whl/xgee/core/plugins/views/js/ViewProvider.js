// 2020 Bjoern Annighoefer

var VIEWS = VIEWS || {};

Object.assign(VIEWS,(function(){
    function ViewProvider(providerId,position,activate) {
        this.providerId = providerId;
        this.position = position; //lower comes first
        this.activate = activate;
    } 

    ViewProvider.prototype.CreateView = function() {
        //to be overwritten
    };

    
    return {
        ViewProvider : ViewProvider
    };
})());