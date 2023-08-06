// 2020 Bjoern Annighoefer

var PROPERTIES_VIEW_ECORE_CUSTOM = PROPERTIES_VIEW_ECORE_CUSTOM || {};

Object.assign(PROPERTIES_VIEW_ECORE_CUSTOM,(function(){

    function CustomPropertiesPaneProvider(pluginApi,params) {
        this.name = "Custom";
        this.config = PROPERTIES_VIEW_ECORE_CUSTOM.DEFAULT_CONFIG; //defining the features and order to be shown
        this.importance = 10; //the higher, the more left the tab is shown
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
    CustomPropertiesPaneProvider.prototype = Object.create(PROPERTIES_VIEW.PropertiesPaneProvider.prototype);
    
    CustomPropertiesPaneProvider.prototype.IsApplicable = function(selection) {
        let eObject = null;
        //see if this is a single or multi-selection
        if(selection && selection.length==1) {
            eObject = selection[0];
        } else if(selection) {
            eObject = selection;
        } 
        //see if this is a supported object
        if(eObject) {
            return this.IsEObject(eObject) && this.IsKnownObjectType(eObject,this.config);
        }
        //everthing else is not supported
        return false;
    };
    
    CustomPropertiesPaneProvider.prototype.CreatePane = function(selection) {
        eObject = selection.eClass?selection:selection[0]; // Either of both must be an eObject, since this was checked in IsApplicable before    
        let paneParams = {
            eObject: eObject,
            ecoreSync: this.ecoreSync,
            app: this.app, //TODO: import from the outside
            config : this.config,
        };
        let pane = new PROPERTIES_VIEW_ECORE_CUSTOM.CustomPropertiesPane(paneParams);
        return pane;
    };

    CustomPropertiesPaneProvider.prototype.IsEObject = function(eObject) {
        return (eObject && eObject.eClass);
    };

    CustomPropertiesPaneProvider.prototype.IsKnownObjectType = function(eObject,config) {
        let eClass = eObject.eClass;
        let package = eClass.eContainer;
        if(package) {
            let className = eClass.get('name');
            let nsUri = package.get('nsURI');
            if(config[nsUri] && config[nsUri][className]) {
                return true;
            }
        }
        return false;
    };

    return {
        CustomPropertiesPaneProvider : CustomPropertiesPaneProvider
    }
})());


