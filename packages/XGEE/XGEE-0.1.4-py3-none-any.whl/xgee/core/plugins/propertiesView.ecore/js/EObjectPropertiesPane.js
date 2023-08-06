/* EOBJECTPROPERTIESPANE */
var PROPERTIES_VIEW_ECORE = PROPERTIES_VIEW_ECORE || {};

Object.assign(PROPERTIES_VIEW_ECORE,(function(){
    function EObjectPropertiesPane(params={},createDom=true) {
        jsa.CustomFlatContainer.call(this,params,false);

        //members
        this.id = 'ecorepropertiespane';
        this.eObject = null;
        this.ecoreSync = null;
        this.style = ['properties-pane'];

        //copy params
        jsa.CopyParams(this,params);

        if(createDom) {
            this.CreateDom();
        }

        return this;
    };

    EObjectPropertiesPane.prototype = Object.create(jsa.CustomFlatContainer.prototype);


    EObjectPropertiesPane.prototype.CreateDom = function() {
        jsa.CustomFlatContainer.prototype.CreateDom.call(this);

        if(this.eObject) {
            var id = this.ecoreSync.rlookup(this.eObject);
            var className = this.eObject.eClass.get("name");
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

            this.pathRow = new jsa.TableRow({});
            this.propertiesTable.AddChild(this.pathRow);

            this.pathRow.AddChild(new jsa.TableCol({
                style: ['feature'],
                content: 'EOQ path',
            }));
            this.pathEntryCol = new jsa.TableCol();
            this.pathRow.AddChild(this.pathEntryCol);
            this.pathEntryInput = new jsa.TextCtrl({
                // style: ['form-group','no-margin'],
                // ctrlStyle: ['form-control','form-control-sm'],
                value: 'loading...',
                readonly: true
            });
            this.pathEntryCol.AddChild(this.pathEntryInput);

            //load path by callback
            this.UpdateLabelAndPath();


            this.attributeRows = {}
            //Add attribute rows
            var attr = this.eObject.eClass.get("eAllAttributes");
            attr.sort(function(a,b){
                //BA: force name and id to the top
                var nameA = a.get("name");
                var nameB = b.get("name");
                if("name" == nameA) { 
                    return -100000;
                } else if("name" == nameB) { 
                    return 100000;
                }
                if("id" == nameA) { 
                    return -50000;
                } else if("id" == nameB) { 
                    return 50000;
                }
                return (nameA < nameB);
            });

            if(attr) {
                if(attr.length > 0) {   
                    for (let i in attr) {
                        let attributeName = attr[i].get("name");
                        //skip internal attributes
                        if(attributeName.startsWith("_")) {
                            continue;
                        }

                        let attributeRow = new jsa.TableRow();
                        this.propertiesTable.AddChild(attributeRow);
                        let attributeLabelCol = new jsa.TableCol({
                            style: ['feature'],
                            content: attributeName
                        });
                        attributeRow.AddChild(attributeLabelCol);
                        let attributeValueCol = new jsa.TableCol({
                            style: ['value']
                        });
                        attributeRow.AddChild(attributeValueCol);

                        //Create the appropriate input control denpending on the type
                        //Prepare the create arguments, because the are the same for most inputs
                        let attributeCtrlParams = {
                            // style: ['form-group','no-margin'],
                            // ctrlStyle: ['form-control','form-control-sm'],
                        };

                        let attributeValueInput = ECORESYNC_UI.EObjectCtrlFactory.CreateDefaultCtrlForFeature(this.ecoreSync,this.eObject,attr[i],attributeCtrlParams,true,this.app.commandManager);

                        attributeValueCol.AddChild(attributeValueInput);
                        
                        this.attributeRows[attributeName] = {
                            row : attributeRow,
                            labelCol : attributeLabelCol,
                            entryCol: attributeValueCol,
                            ctrl: attributeValueInput
                        };
                    }
                } 
            }

            //show all references
            var ref = this.eObject.eClass.get("eAllReferences");
            ref.sort(function(a,b){
                var nameA = a.get("name");
                var nameB = b.get("name");
                return (nameA < nameB);
            });

            this.referenceRows = {}
            //Add reference rows
            
            if(ref) {
                if(ref.length > 0) {   
                    for (let i in ref) {
                        let referenceName = ref[i].get("name");
                       
                        let referenceRow = new jsa.TableRow();
                        this.propertiesTable.AddChild(referenceRow);
                        let referenceLabelCol = new jsa.TableCol({
                            style: ['feature'],
                            content: referenceName
                        });
                        referenceRow.AddChild(referenceLabelCol);
                        let referenceValueCol = new jsa.TableCol({
                            style: ['value']
                        });
                        referenceRow.AddChild(referenceValueCol);

                        let referenceCtrlParams = {
                            // style: ['form-group','no-margin'],
                            // ctrlStyle: ['form-control','form-control-sm'],
                        };

                        let referenceValueInput = ECORESYNC_UI.EObjectCtrlFactory.CreateDefaultCtrlForFeature(this.ecoreSync,this.eObject,ref[i],referenceCtrlParams,true,this.app.commandManager);


                        referenceValueCol.AddChild(referenceValueInput);

                        this.referenceRows[referenceName] = {
                            row : referenceRow,
                            labelCol : referenceLabelCol,
                            entryCol: referenceValueCol,
                            ctrl: referenceValueInput,
                        };

                    }
                }
            }

            //show all containments
            var containmentFeatures = this.eObject.eClass.get("eAllContainments");
            containmentFeatures.sort(function(a,b){
                var nameA = a.get("name");
                var nameB = b.get("name");
                return (nameA < nameB);
            });

            this.containmentRows = {}
            //Add reference rows
            
            if(containmentFeatures) {
                if(containmentFeatures.length > 0) {   
                    for (let i in containmentFeatures) {
                        let containmentFeature = containmentFeatures[i];
                        let containmentName = containmentFeature.get("name");

                        let containmentRow = new jsa.TableRow();
                        this.propertiesTable.AddChild(containmentRow);
                        let containmentLabelCol = new jsa.TableCol({
                            style: ['feature'],
                            content: containmentName
                        });
                        containmentRow.AddChild(containmentLabelCol);
                        let containmentValueCol = new jsa.TableCol({
                            style: ['value']
                        });
                        containmentRow.AddChild(containmentValueCol);

                        // let upperBound = containmentFeature.get('upperBound');
                        // let lowerBound = containmentFeature.get('lowerBound');
                        let containmentCtrlParams = {
                            // style: ['form-group','no-margin'],
                            // ctrlStyle: ['form-control','form-control-sm'],
                        };

                        //let containmentValueInput = new ECORESYNC_UI.EReferenceCtrl(containmentCtrlParams);
                        let containmentValueInput = ECORESYNC_UI.EObjectCtrlFactory.CreateDefaultCtrlForFeature(this.ecoreSync,this.eObject,containmentFeature,containmentCtrlParams,true,this.app.commandManager);


                        containmentValueCol.AddChild(containmentValueInput);
  
                        //store all values for later cleanup
                        this.containmentRows[containmentName] = {
                            row : containmentRow,
                            labelCol : containmentLabelCol,
                            entryCol: containmentValueCol,
                            ctrl: containmentValueInput,
                        };

                    }
                }
            }

        } else {
            this.GetDomElement().innerHTML = "Error: No EObject given!";
        }
        return this;
    };

    EObjectPropertiesPane.prototype.UpdateLabelAndPath = function() {
        var id = this.ecoreSync.rlookup(this.eObject);eObject.get("_#EOQ");
        var className = this.eObject.eClass.get("name");
        var name = this.eObject.get("name");

        var label = className+'[#'+id+']'+(name?(':\''+name+'\''):'');
        this.label.GetDomElement().innerHTML = label;

        var self = this;
        this.ecoreSync.utils.getObjectStringPath(this.eObject).then(function(pathStr){
            self.pathEntryInput.SetValue(pathStr);
        });


        return this;
    };

    return {
        EObjectPropertiesPane : EObjectPropertiesPane
    };
})());