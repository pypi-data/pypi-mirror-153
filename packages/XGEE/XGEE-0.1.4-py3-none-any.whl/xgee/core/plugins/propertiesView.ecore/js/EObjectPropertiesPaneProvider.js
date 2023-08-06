// 2020 Bjoern Annighoefer

var PROPERTIES_VIEW_ECORE = PROPERTIES_VIEW_ECORE || {};

Object.assign(PROPERTIES_VIEW_ECORE,(function(){
    function EObjectPropertiesPaneProvider(pluginApi,params) {
        this.name = 'EObject';
        this.importance = 5;
        this.ecoreSyncId = 'ecoreSync';
        Object.assign(this,params);

        PROPERTIES_VIEW.PropertiesPaneProvider.call(this,this.name,this.importance);
        
        //internals 
        this.pluginApi = pluginApi;
        this.app = pluginApi.getGlobal('app');
        this.ecoreSync = pluginApi.require('ecoreSync').getInstanceById(this.ecoreSyncId);

        return this;
    }
    EObjectPropertiesPaneProvider.prototype = Object.create(PROPERTIES_VIEW.PropertiesPaneProvider.prototype);
    
    EObjectPropertiesPaneProvider.prototype.IsApplicable = function(selection) {
        if(selection && selection.length==1 && selection[0].eClass) {
            return true;
        } else if(selection && selection.eClass) {
            return true;
        } else {
            return false;
        }
    };
    
    EObjectPropertiesPaneProvider.prototype.CreatePane = function(selection) {
        let eObject = selection.eClass?selection:selection[0]; // Either of both must be an eObject, since this was checked in IsApplicable before    
        let pane = new PROPERTIES_VIEW_ECORE.EObjectPropertiesPane({
            eObject: eObject,
            ecoreSync: this.ecoreSync, //TODO: import from the outside
            app: this.app //TODO: import from the outside
        });
        return pane;
    };

    return {
        EObjectPropertiesPaneProvider : EObjectPropertiesPaneProvider
    }
})());


