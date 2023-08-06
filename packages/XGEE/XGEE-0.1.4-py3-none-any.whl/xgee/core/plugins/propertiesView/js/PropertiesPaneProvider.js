// This is the baseclass for all plugins that would like to provide a propertiesView pane
// 2020 Bjoern Annighoefer

var PROPERTIES_VIEW = PROPERTIES_VIEW || {};

Object.assign(PROPERTIES_VIEW,(function(){
    function PropertiesPaneProvider(name,importance=0) {
        //All propertiesView panes must inherit from this class
        this.name = name;
        this.importance = importance;
    };
    
    PropertiesPaneProvider.prototype.IsApplicable = function(selection) {
        return false; //return true if this is an matching
    };
    
    PropertiesPaneProvider.prototype.CreatePane = function(selection) {
        return null; //must return an instance of a jsa.UiElement
    };

    return {
        PropertiesPaneProvider : PropertiesPaneProvider
    }
})());


