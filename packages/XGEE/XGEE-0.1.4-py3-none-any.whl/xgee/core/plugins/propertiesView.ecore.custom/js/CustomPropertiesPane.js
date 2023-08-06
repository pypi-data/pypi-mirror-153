/* EOBJECTPROPERTIESPANE */
var PROPERTIES_VIEW_ECORE_CUSTOM = PROPERTIES_VIEW_ECORE_CUSTOM || {};

Object.assign(PROPERTIES_VIEW_ECORE_CUSTOM,(function(){
    
    function CustomPropertiesPane(params={},createDom=true) {
        jsa.CustomFlatContainer.call(this,params,false);

        //members
        this.id = 'ecorepropertiespane';
        this.eObject = null;
        this.ecoreSync = null;
        this.style = ['properties-pane'];
        this.config = PROPERTIES_VIEW_ECORE_CUSTOM.DEFAULT_CONFIG;

        //copy params
        jsa.CopyParams(this,params);

        //internals
        // this.featureRows = {};

        if(createDom) {
            this.CreateDom();
        }
        return this;
    };

    CustomPropertiesPane.prototype = Object.create(jsa.CustomFlatContainer.prototype);


    CustomPropertiesPane.prototype.CreateDom = function() {
        jsa.CustomFlatContainer.prototype.CreateDom.call(this);

        if(this.eObject) {
            let eClass = this.eObject.eClass;
            let className = eClass.get('name');
            let nsURI = eClass.eContainer.get('nsURI');

            let ctrlConfig = this.config[nsURI][className];
            
            if(ctrlConfig) {
                let featureNames = Object.keys(ctrlConfig).filter(function(k) {
                    let e = ctrlConfig[k];
                    return (undefined === e.show || true == e.show);
                }).sort(function(ka,kb) {
                    let a = ctrlConfig[ka];
                    let b = ctrlConfig[kb];
                    if(a.priority && b.priority) {
                        return (a.priority-b.priority)
                    } 
                    return 0; //so sorting possible
                });

                if(0 < featureNames.length) {
                    //var id = this.eObject.get("_#EOQ");
                    //label
                    this.label = new jsa.CustomFlatContainer({
                        elementType: 'h1',
                        style: ['title']
                    })
                    this.AddChild(this.label);
                    
                    this.propertiesTable = new jsa.Table({
                        style: ['properties-table']
                    });
                    this.AddChild(this.propertiesTable);
                    //load path by callback
                    this.UpdateLabelAndPath();

                    //Add all features as desired
                    let allFeatures = eClass.get("eAllStructuralFeatures");
                    for(let i=0;i<featureNames.length; i++) {
                        let featureName = featureNames[i];
                        let featureConfig = ctrlConfig[featureName];
                        feature = allFeatures.find(function(f){
                            return f.get('name')==featureName;
                        })
                        if(feature) {
                            //add the parameter
                            let featureRow = new jsa.TableRow();
                            this.propertiesTable.AddChild(featureRow);
                            let featureLabelCol = new jsa.TableCol({
                                style: ['feature'],
                                content: featureConfig.name?featureConfig.name:featureName
                            });
                            featureRow.AddChild(featureLabelCol);
                            let featureValueCol = new jsa.TableCol({
                                style: ['value']
                            });
                            featureRow.AddChild(featureValueCol);
   
                            let customFilter = featureConfig.customFilter?featureConfig.customFilter:null;
                            let customFilterScope = featureConfig.filterScope?featureConfig.filterScope:'SELF';
                            let scope = featureConfig.scope?featureConfig.scope:'local';


                            let ctrlParams = {
                                // style: ['form-group','no-margin'],
                                // ctrlStyle: ['form-control','form-control-sm'],
                                scope : scope,
                                customFilter : customFilter,
                                customFilterScope : customFilterScope,
                                emptyAutocompleteMsg : featureConfig.emptyAutocompleteMsg?featureConfig.emptyAutocompleteMsg:'None'
                            };

                            let featureValueInput = ECORESYNC_UI.EObjectCtrlFactory.CreateDefaultCtrlForFeature(this.ecoreSync,this.eObject,feature,ctrlParams,true,this.app.commandManager);
                            featureValueCol.AddChild(featureValueInput);

                        
                            if(featureConfig.description) {
                                //Add the description
                                let featureDescriptionRow = new jsa.TableRow();
                                this.propertiesTable.AddChild(featureDescriptionRow);
                                let featureDescriptionCol1 = new jsa.TableCol({
                                    style: ['description'],
                                    content: ''
                                });
                                featureDescriptionRow.AddChild(featureDescriptionCol1);

                                let featureDescriptionCol2 = new jsa.TableCol({
                                    style: ['description'],
                                    content: featureConfig.description
                                });
                                featureDescriptionRow.AddChild(featureDescriptionCol2);
                            }

                            // //store all values for later cleanup
                            // this.featureRows[featureName] = {
                            //     featureRow : featureRow,
                            //     labelCol : featureLabelCol,
                            //     entryCol: featureValueCol,
                            //     ctrl: featureValueInput,
                            //     desctiptionRow : featureDescriptionRow,
                            //     descriptionCol1 : featureDescriptionCol1,
                            //     descriptionCol2 : featureDescriptionCol2,
                            // };
                        }
                    }
                }
            }
        } else {
            this.GetDomElement().innerHTML = "Error: No OAAM given!";
        }
        return this;
    };

    CustomPropertiesPane.prototype.UpdateLabelAndPath = function() {
        var id = this.ecoreSync.rlookup(eObject);
        var className = this.eObject.eClass.get("name");
        var name = this.eObject.get("name");

        var label = className+'[#'+id+']'+(name?(':\''+name+'\''):'');
        this.label.GetDomElement().innerHTML = label;

        return this;
    };

    return {
        CustomPropertiesPane : CustomPropertiesPane
    };
})());