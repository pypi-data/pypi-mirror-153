// This is the baseclass for all plugins that would like to provide a propertiesView pane
// 2020 Bjoern Annighoefer

var PROPERTIES_VIEW = PROPERTIES_VIEW || {};

Object.assign(PROPERTIES_VIEW,(function(){

    function LoadOnDemandView(params,createDom=true) {
        jsa.View.call(this,params,false);

        //members
        this.style = ['jsa-view','properties-view'];
        this.containerStyle = ['jsa-view-container','properties-view-container'];
        this.paneProvider = null;
        this.selection = null;

        this.onFocusCallback = function() { 
            if(!this.isInitialized) {
                try {
                    //create the properties view
                    this.pane = this.paneProvider.CreatePane(this.selection);
                } catch (error) {
                    let errorMsg = error.toString();
                    this.pane = new jsa.CustomFlatContainer({
                        content : errorMsg
                    });
                }
                this.AddChild(this.pane);
                this.isInitialized = true;
            }
        };

        //copy parameters
        jsa.CopyParams(this,params);

        //internals
        this.isInitialized = false;
        this.pane = null;

        //Create DOM
        if(createDom) {
            this.CreateDom();
        }
    };

    LoadOnDemandView.prototype = Object.create(jsa.View.prototype);

    // CreateOnDemandPropertiesView.prototype.CreateDom = function() {
    //     jsa.View.prototype.CreateDom.call(this);

    //     return this;
    // };

    return {
        LoadOnDemandView : LoadOnDemandView
    };

})());