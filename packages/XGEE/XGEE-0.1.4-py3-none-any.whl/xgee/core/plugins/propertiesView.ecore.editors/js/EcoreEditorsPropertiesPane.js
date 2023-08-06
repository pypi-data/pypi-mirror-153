/* EOBJECTPROPERTIESPANE */
var PROPERTIES_VIEW_ECORE_EDITORS = PROPERTIES_VIEW_ECORE_EDITORS || {};

Object.assign(PROPERTIES_VIEW_ECORE_EDITORS,(function(){
    
    function EcoreEditorsPropertiesPane(params={},createDom=true) {
        jsa.CustomFlatContainer.call(this,params,false);

        //members
        this.eObject = null;
        this.ecoreSync = null;
        this.style = ['properties-pane','ecore-modify-properties-pane'];

        //copy params
        jsa.CopyParams(this,params);

        //internals
        // this.featureRows = {};

        if(createDom) {
            this.CreateDom();
        }
        return this;
    };

    EcoreEditorsPropertiesPane.prototype = Object.create(jsa.CustomFlatContainer.prototype);


    EcoreEditorsPropertiesPane.prototype.CreateDom = function() {
        jsa.CustomFlatContainer.prototype.CreateDom.call(this);

        if(this.eObject) {
            
            this.SetContent('List of all editors.')

        } else {
            this.GetDomElement().innerHTML = "Error: No EObject given!";
        }
        return this;
    };

    EcoreEditorsPropertiesPane.prototype.UpdateLabelAndPath = function() {
        var id = this.eObject.get("_#EOQ");
        var className = this.eObject.eClass.get("name");
        var name = this.eObject.get("name");

        var label = className+'[#'+id+']'+(name?(':\''+name+'\''):'');
        this.label.GetDomElement().innerHTML = label;

        return this;
    };

    return {
        EcoreEditorsPropertiesPane : EcoreEditorsPropertiesPane
    };
})());