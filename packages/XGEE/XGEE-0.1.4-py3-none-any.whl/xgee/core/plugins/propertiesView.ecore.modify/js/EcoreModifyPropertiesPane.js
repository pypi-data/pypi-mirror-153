/* EOBJECTPROPERTIESPANE */
var PROPERTIES_VIEW_ECORE_MODIFY = PROPERTIES_VIEW_ECORE_MODIFY || {};

Object.assign(PROPERTIES_VIEW_ECORE_MODIFY,(function(){
    
    function EcoreModifyPropertiesPane(params={},createDom=true) {
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

    EcoreModifyPropertiesPane.prototype = Object.create(jsa.CustomFlatContainer.prototype);


    EcoreModifyPropertiesPane.prototype.CreateDom = function() {
        jsa.CustomFlatContainer.prototype.CreateDom.call(this);

        if(this.eObject) {
            //COPY
            let copyButton = new jsa.Button({
                content : 'Copy',
                enabled : false,
                style : ['jsa-button','copy-button'],
                onClickCallback : function(evt) {
                    alert('Copy')
                }
            });
            this.AddChild(copyButton);
            copyButton.Disable();
            //CLONE
            let cloneButton = new jsa.Button({
                content : 'Clone',
                enabled : false,
                style : ['jsa-button','clone-button'],
                onClickCallback : function(evt) {
                    alert('Clone')
                }
            });
            this.AddChild(cloneButton);
            //DELETE
            let deleteButton = new jsa.Button({
                content : 'Delete',
                enabled : true,
                style : ['jsa-button','delete-button'],
                onClickCallback : function(evt) {
                    alert('Delete')
                }
            });
            this.AddChild(deleteButton);

        } else {
            this.GetDomElement().innerHTML = "Error: No EObject given!";
        }
        return this;
    };

    EcoreModifyPropertiesPane.prototype.UpdateLabelAndPath = function() {
        var id = this.eObject.get("_#EOQ");
        var className = this.eObject.eClass.get("name");
        var name = this.eObject.get("name");

        var label = className+'[#'+id+']'+(name?(':\''+name+'\''):'');
        this.label.GetDomElement().innerHTML = label;

        return this;
    };

    return {
        EcoreModifyPropertiesPane : EcoreModifyPropertiesPane
    };
})());