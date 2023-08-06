// 2020 Bjoern Annighoefer

var PROPERTIES_VIEW_ECORE_EDITORS = PROPERTIES_VIEW_ECORE_EDITORS || {};

Object.assign(PROPERTIES_VIEW_ECORE_EDITORS,(function(){

    function EcoreEditorsPropertiesPaneProvider(pluginApi,params) {
        this.name = "Custom";
        this.importance = 7; //the higher, the more left the tab is shown
        this.ecoreSyncId = 'ecoreSync'; //currently not used
        Object.assign(this,params);

        //super constructor
        PROPERTIES_VIEW.PropertiesPaneProvider.call(this,this.name,this.importance);

        //internals 
        this.pluginApi = pluginApi;
        this.app = pluginApi.getGlobal('app');
        this.ecoreSync = pluginApi.require('ecoreSync').getInstanceById(this.ecoreSyncId);

        return this;
    }
    EcoreEditorsPropertiesPaneProvider.prototype = Object.create(PROPERTIES_VIEW.PropertiesPaneProvider.prototype);
    
    EcoreEditorsPropertiesPaneProvider.prototype.IsApplicable = function(selection) {
        let eObject = null;
        //see if this is a single or multi-selection
        if(selection && selection.length==1) {
            eObject = selection[0];
        } else if(selection) {
            eObject = selection;
        } 
        //see if this is a supported object 
        if(eObject) {
            return this.IsEObject(eObject);
        }
        //everthing else is not supported
        return false;
    };
    
    EcoreEditorsPropertiesPaneProvider.prototype.CreatePane = function(selection) {
        eObject = selection.eClass?selection:selection[0]; // Either of both must be an eObject, since this was checked in IsApplicable before    
        let paneParams = {
            eObject: eObject,
            ecoreSync: this.ecoreSync,
            app: this.app, //TODO: import from the outside
        };
        let pane = new PROPERTIES_VIEW_ECORE_EDITORS.EcoreEditorsPropertiesPane(paneParams);
        return pane;
    };

    EcoreEditorsPropertiesPaneProvider.prototype.IsEObject = function(eObject) {
        return (eObject && eObject.eClass);
    };

    return {
        EcoreEditorsPropertiesPaneProvider : EcoreEditorsPropertiesPaneProvider
    }
})());


