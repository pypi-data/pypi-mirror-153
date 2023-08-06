var ECORESYNC_UI = ECORESYNC_UI || {};

Object.assign(ECORESYNC_UI,(function(){

    function GenerateTypeString(typeName,lowerBound,upperBound) {
        return typeName + ((upperBound==1)?'':'['+lowerBound+'..'+((upperBound==-1)?'*':upperBound)+']');
    }

    /* EOBJECTCTRLFACTORY */    

    function EObjectCtrlFactory() {
        return this;
    }

    EObjectCtrlFactory.prototype.CreateDefaultCtrlForFeature = function(ecoreSync,eObject,eFeature,userParams={},observeChanges=false,commandManager=null) {
        let ctrl = null;

        //change callbacks for single value attributes
        let onAttributeChangeCallbackNoCommand = function(e) {
            if(this.Validate()) {
                var newValue = this.GetValue();
                this.eObject.set(this.featureName,newValue);    
            }          
        };
        let onAttributeChangeCallbackCommand = function(e) {
            if(this.Validate()) {
                var newValue = this.GetValue();
                this.commandManager.Execute(new ESetCommand(this.ecoreSync,this.eObject,this.featureName,newValue));    
            }          
        };
        //multi value change callbacks
        let onAttributeAddRemoveCallbackCommand = function(e) {
            this.RefreshAutocompleteCheckedStatus();
            if(this.Validate()) {
                let self = this;
                this.GetValue().then(function(newValue){
                    if(self.upperBound==1) {
                        self.commandManager.Execute(new ESetCommand(self.ecoreSync,self.eObject,self.featureName,newValue)); 
                    } else { //upper bound > 0
                        self.commandManager.Execute(new UpdateReferenceCommand(self.ecoreSync,self.eObject,self.featureName,newValue));                        
                    }
                });
            }          
        };
        let onAttributeAddRemoveCallbackNoCommand = function(e) {
            this.RefreshAutocompleteCheckedStatus();
            if(this.Validate()) {
                let self = this;
                this.GetValue().then(function(newValue){
                    if(self.upperBound==1) {
                        self.ecoreSync.set(eObject,self.featureName,newValue); 
                    } else { //upper bound > 0
                        let command = new UpdateReferenceCommand(self.ecoreSync,self.eObject,self.featureName,newValue);
                        command.Do();
                    }
                });
            }          
        };


    
        //gather the basic information on this feature
        let featureName = eFeature.get("name");
        let featureType = eFeature.get("eType")

        if(featureType){ //for some reason, this was necessary to get FTML to work

            let typeName = featureType.get("name");
            let promisedValue = new Promise(async function(resolve,reject){
                try{
                    resolve(await self.ecoreSync.get(eObject,featureName));
                }catch(e){
                    reject(e);
                }
            });
            let upperBound = eFeature.get('upperBound');
            let lowerBound = eFeature.get('lowerBound');
        
            //value will be resolved later           
            let value = "loading...";
            let readonly = true; //will enable the control later

            //define the general parameters of the ctrl
            let ctrlParams = {
                value: value,
                promisedValue : promisedValue,
                readonly : readonly,
                placeholder : GenerateTypeString(typeName,lowerBound,upperBound),

                ecoreSync : ecoreSync,
                eObject: eObject, 
                featureName: featureName,
                lowerBound: lowerBound,
                upperBound: upperBound,
                typeName: typeName,
                observeChanges : observeChanges,
                commandManager: commandManager
            };
            Object.assign(ctrlParams,userParams);
            
            //decide which control to create
            let featureTypeName = eFeature.eClass.get('name');
            switch(featureTypeName) {
                case 'EAttribute': {
                    let attributeCtrlParams = {
                        onChangeCallback : commandManager?onAttributeChangeCallbackCommand:onAttributeChangeCallbackNoCommand
                    }
                    Object.assign(ctrlParams,attributeCtrlParams);
        
                    switch(typeName) {
                        case "EString":
                            ctrl = new ECORESYNC_UI.EStringCtrl(ctrlParams);
                            break;
                        case "EBoolean":
                            ctrl = new ECORESYNC_UI.EBoolCtrl(ctrlParams);
                            break;
                        case "EInt":
                            ctrl = new ECORESYNC_UI.EIntCtrl(ctrlParams);
                            break;
                        case "EFloat":
                            ctrl = new ECORESYNC_UI.EFloatCtrl(ctrlParams);
                            break;
                        case "EDouble":
                            ctrl = new ECORESYNC_UI.EDoubleCtrl(ctrlParams);
                            break;
                        case "EDate":
                            ctrl = new ECORESYNC_UI.EDateCtrl(ctrlParams);
                            break;      
                        default:
                            var attributeTypeClassName = featureType.eClass.get("name");
                            switch (attributeTypeClassName){
                                case "EEnum":             
                                    var literalStrs = [];
                                    var literals=featureType.get("eLiterals").array();
                                    for(var j=0;j<literals.length;j++) {
                                        var literal = literals[j];
                                        literalStrs.push(literal.get("literal"));
                                    }       
                                    ctrlParams.values = literalStrs;
                                    ctrlParams.labels = literalStrs;               
                                    ctrl = new ECORESYNC_UI.EEnumCtrl(ctrlParams);           
                                    break
                                default:
                                    ctrl = new ECORESYNC_UI.EStringCtrl(ctrlParams);
                                    break;
                            }
                            break;
                    }
                    break;
                }
                case 'EReference': {
                    //define additional params and callback for referneces
                    let containment = eFeature.get('containment');
                    let referenceCtrlParams = {
                        readonly : containment,
                        readOnlyAfterInitialized: containment, //containments shall not be modifiable
                        containment: containment,
                        packageNs: '', //TODO
                        //scope: 'local',
                        onChangeCallback : commandManager?onAttributeAddRemoveCallbackCommand:onAttributeAddRemoveCallbackNoCommand
                    }
                    Object.assign(ctrlParams,referenceCtrlParams);
        
                    //create ctrl
                    ctrl = new ECORESYNC_UI.EReferenceCtrl(ctrlParams);
                    break;
                }
                default:
                    console.log("Can not create a ctrl for feature type "+featureTypeName);
                    ctrl = null
                    //Do nothing
            }
        }
        else
        {
            console.error(eFeature.get("name")+' has no eType or incompatible eType');
            ctrl=null;
        }
        return ctrl;
    }

    return {
        EObjectCtrlFactory : new EObjectCtrlFactory() //create the only instance
    }
    

})());


