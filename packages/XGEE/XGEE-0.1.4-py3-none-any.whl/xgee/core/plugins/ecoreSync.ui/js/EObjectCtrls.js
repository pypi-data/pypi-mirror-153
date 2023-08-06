var ECORESYNC_UI = ECORESYNC_UI || {};

Object.assign(ECORESYNC_UI,(function(){

     /* EATTRIBUTETEXTCTRL ABSTRACT */
     function EAttributeTextCtrlA(params={}, createDom=true) {
        jsa.TextCtrl.call(this,params,false);

        //parameters
        this.ecoreSync = null;
        this.eObject = null; 
        this.featureName = '';
        this.promisedValue = null; //create the control with a value that is not ready and update it when the promise is fulfilled
        this.lowerBound = 0;
        this.upperBound = 1;
        this.typeName = 'EObject';
        this.observeChanges = false; //if true, changes to the eObject are observed.
        this.commandManager = null; //if a command manager is given, commands are executed on changes
        this.readOnlyAfterInitialized = false; //the ctrl stay read only even if the values become ready

        jsa.CopyParams(this,params);

        if(createDom) {
            this.CreateDom();
        }

        return this;
    }
    EAttributeTextCtrlA.prototype = Object.create(jsa.TextCtrl.prototype);

    //@Override
    EAttributeTextCtrlA.prototype.CreateDom = function() {
        jsa.TextCtrl.prototype.CreateDom.call(this);
        //custom initialization
        if(this.observeChanges && this.eObject) {
            if(this.upperBound==1) {
                this.eObject.on('change:'+this.featureName,this.OnObjectChange,this);
                // this.eObject.on('change',this.OnObjectChange,this);
            } else {
                this.eObject.on('add:'+this.featureName,this.OnObjectAdd,this);
                this.eObject.on('remove:'+this.featureName,this.OnObjectRemove,this);
            }
        }
        //listen to late initilization
        let self = this;
        if(this.promisedValue instanceof Promise) {
            this.promisedValue.then(function(value) {
                self.OnPromisedValue(value);
            });
        }
    };

    //@Override
    EAttributeTextCtrlA.prototype.Dissolve = function() {
        //custom dissolve
        if(this.observeChanges && this.eObject) {
            if(this.upperBound==1) {
                this.eObject.off('change:'+this.featureName,this.OnObjectChange,this);
                // this.eObject.off('change',this.OnObjectChange,this);
            } else {
                this.eObject.off('add:'+this.featureName,this.OnObjectAdd,this);
                this.eObject.off('remove:'+this.featureName,this.OnObjectRemove,this);
            }
        }
        //super type dissolve
        jsa.TextCtrl.prototype.Dissolve.call(this);
    };


    //generic event listeners
    EAttributeTextCtrlA.prototype.OnObjectChange = function(change) {
        var newValue = this.eObject.get(this.featureName);
        this.SetValue(newValue);
        //this.SetReadonly(this.readOnlyAfterInitialized);
    };

    EAttributeTextCtrlA.prototype.OnObjectAdd = function(change) {
        var newValue = this.eObject.get(this.featureName);
        this.SetValue(newValue);
        //this.SetReadonly(this.readOnlyAfterInitialized);
    };

    EAttributeTextCtrlA.prototype.OnObjectRemove = function(change) {
        var newValue = this.eObject.get(this.featureName);
        this.SetValue(newValue);
        //this.SetReadonly(this.readOnlyAfterInitialized);
    };

    EAttributeTextCtrlA.prototype.OnPromisedValue = function(newValue) {
        this.SetValue(newValue);
        this.SetReadonly(this.readOnlyAfterInitialized);
    };

    /* EATTRIBUTESELECTCTRL ABSTRACT */
    function EAttributeSelectCtrlA(params={}, createDom=true) {
        jsa.SelectCtrl.call(this,params,false);

        //parameters
        this.ecoreSync = null;
        this.eObject = null; 
        this.featureName = '';
        this.promisedValue = null; //create the control with a value that is not ready and update it when the promise is fulfilled
        this.lowerBound = 0;
        this.upperBound = 1;
        this.typeName = 'EObject';
        this.observeChanges = true; //if true, changes to the eObject are observed.
        this.commandManager = null; //if a command manager is given, commands are executed on changes
        this.readOnlyAfterInitialized = false; //the ctrl stay read only even if the values become ready

        jsa.CopyParams(this,params);

        if(createDom) {
            this.CreateDom();
        }

        return this;
    }
    EAttributeSelectCtrlA.prototype = Object.create(jsa.SelectCtrl.prototype);

    //@Override
    EAttributeSelectCtrlA.prototype.CreateDom = function() {
        jsa.SelectCtrl.prototype.CreateDom.call(this);
        //custom initialization
        if(this.observeChanges && this.eObject) {
            if(this.upperBound==1) {
                this.eObject.on('change:'+this.featureName,this.OnObjectChange,this);
                // this.eObject.on('change',this.OnObjectChange,this);
            } else {
                this.eObject.on('add:'+this.featureName,this.OnObjectAdd,this);
                this.eObject.on('remove:'+this.featureName,this.OnObjectRemove,this);
            }
        }
        let self = this;
        if(this.promisedValue instanceof Promise) {
            this.promisedValue.then(function(value) {
                self.OnPromisedValue(value);
            });
        }
    };

    //@Override
    EAttributeSelectCtrlA.prototype.Dissolve = function() {
        //custom dissolve
        if(this.observeChanges && this.eObject) {
            if(this.upperBound==1) {
                this.eObject.off('change:'+this.featureName,this.OnObjectChange,this);
                // this.eObject.off('change',this.OnObjectChange,this);
            } else {
                this.eObject.off('add:'+this.featureName,this.OnObjectAdd,this);
                this.eObject.off('remove:'+this.featureName,this.OnObjectRemove,this);
            }
        }
        //super type dissolve
        jsa.SelectCtrl.prototype.Dissolve.call(this);
    };


    //generic event listeners
    EAttributeSelectCtrlA.prototype.OnObjectChange = function(change) {
        var newValue = this.eObject.get(this.featureName);
        this.SetValue(newValue);
        this.SetReadonly(this.readOnlyAfterInitialized);
    };

    EAttributeSelectCtrlA.prototype.OnObjectAdd = function(change) {
        var newValue = this.eObject.get(this.featureName);
        this.SetValue(newValue);
        this.SetReadonly(this.readOnlyAfterInitialized);
    };

    EAttributeSelectCtrlA.prototype.OnObjectRemove = function(change) {
        var newValue = this.eObject.get(this.featureName);
        this.SetValue(newValue);
        this.SetReadonly(this.readOnlyAfterInitialized);
    };

    EAttributeSelectCtrlA.prototype.OnPromisedValue = function(newValue) {
        this.SetValue(newValue);
        this.SetReadonly(this.readOnlyAfterInitialized);
    };

    // EAttributeTextCtrlA.prototype.OnObjectChange = function(featureName) {
    //     if(this.featureName==featureName) {
    //         var newValue = this.eObject.get(this.featureName);
    //         this.SetValue(newValue);
    //         this.SetReadonly(this.readOnlyAfterInitialized);
    //     };
    // };


    /* ESTRINGCTRL */
    function EStringCtrl(params={}, createDom=true) {
        EAttributeTextCtrlA.call(this,params,false);

        //parameters
        this.validateFunction = function(valueStr) {
            if(/['"#\$\[\]\/\\]/.test(valueStr)) {
                throw new Error('Illegal value: String should not contain \',",#,$,[,],\\ or /!');
            }
            return true;
        } //Shall throw an Error if validation fails

        jsa.CopyParams(this,params);

        if(createDom) {
            this.CreateDom();
        }

        return this;
    }
    EStringCtrl.prototype = Object.create(EAttributeTextCtrlA.prototype);


    /* EDATECTRL */
    function EDateCtrl(params={}, createDom=true) {
        EAttributeTextCtrlA.call(this,params,false);

        //parameters
        this.validateFunction = function(valueStr) {
            if(Number.isNaN(Date.parse(valueStr))) {
                throw new Error('Illegal value: Please give date as YYYY-MM-DD hh:mm:ss!');
            }
            return true;
        } //Shall throw an Error if validation fails

        jsa.CopyParams(this,params);

        if(createDom) {
            this.CreateDom();
        }

        return this;
    }
    EDateCtrl.prototype = Object.create(EAttributeTextCtrlA.prototype);


    /* EBOOLCTRL */
    function EBoolCtrl(params={}, createDom=true) {
        EAttributeSelectCtrlA.call(this,params,false);

        //parameters
        this.values = [true,false];
        this.labels = ['Yes','No'];
        this.inputTransferFunction = function(value) {
            return (value?'true':'false');
        };

        jsa.CopyParams(this,params);

        if(createDom) {
            this.CreateDom();
        }

        return this;
    }
    EBoolCtrl.prototype = Object.create(EAttributeSelectCtrlA.prototype);


    /* EENUMCTRL */
    function EEnumCtrl(params={}, createDom=true) {
        EAttributeSelectCtrlA.call(this,params,false);

        //parameters

        jsa.CopyParams(this,params);

        if(createDom) {
            this.CreateDom();
        }

        return this;
    }
    EEnumCtrl.prototype = Object.create(EAttributeSelectCtrlA.prototype);



    /* EINTCTRL */
    function EIntCtrl(params={}, createDom=true) {
        EAttributeTextCtrlA.call(this,params,false);

        //parameters
        this.inputTransferFunction = function(value) {
            var valueStr = value.toString(); 
            return valueStr;
        };
        this.outputTransferFunction = function(valueStr) {
            var value = Number.parseInt(valueStr); 
            return value;
        };
        this.validateFunction = function(valueStr) {
            if(!Number.isInteger(Number.parseInt(valueStr))) {
                throw new Error('Illegal value: Value is not an integer!');
            }
            return true;
        } //Shall throw an Error if validation fails

        jsa.CopyParams(this,params);

        if(createDom) {
            this.CreateDom();
        }

        return this;
    }
    EIntCtrl.prototype = Object.create(EAttributeTextCtrlA.prototype);

    EIntCtrl.prototype.CreateDom = function() {
        EAttributeTextCtrlA.prototype.CreateDom.call(this);

        // let configEInt = {
        //     decrementButton: "<strong>-</strong>", // button text
        //     incrementButton: "<strong>+</strong>", // ..
        //     groupClass: "", // css class of the resulting input-group
        //     buttonsClass: "btn-outline-secondary",
        //     buttonsWidth: "25px",
        //     textAlign: "center",
        //     autoDelay: 500, // ms holding before auto value change
        //     autoInterval: 100, // speed of auto value change
        //     boostThreshold: 10, // boost after these steps
        //     boostMultiplier: "auto", // you can also set a constant number as multiplier
        //     locale: null // the locale for number rendering; if null, the browsers language is used
        // };
        // $(this.input).inputSpinner(configEInt);

        return this;
    }

    // //Override because of input spinner
    // EIntCtrl.prototype.SetRawValue = function(valueStr,notify=false) {
    //     $(this.input).val(valueStr);
    //     if(notify) {
    //         this.input.dispatchEvent(new Event('change', { 'bubbles': true }));
    //     }
    //     return this;
    // };


    /* EFLOATCTRL */
    function EFloatCtrl(params={}, createDom=true) {
        EAttributeTextCtrlA.call(this,params,false);

        //parameters
        this.inputTransferFunction = function(value) {
            var valueStr = value.toString(); 
            return valueStr;
        };
        this.outputTransferFunction = function(valueStr) {
            var value = Number.parseFloat(valueStr); 
            return value;
        };
        this.validateFunction = function(valueStr) {
            if(Number.isNaN(Number.parseFloat(valueStr))) {
                throw new Error('Illegal value: Value is not an number!');
            }
            return true;
        } //Shall throw an Error if validation fails

        jsa.CopyParams(this,params);

        if(createDom) {
            this.CreateDom();
        }

        return this;
    }
    EFloatCtrl.prototype = Object.create(EAttributeTextCtrlA.prototype);

    EFloatCtrl.prototype.CreateDom = function() {
        EAttributeTextCtrlA.prototype.CreateDom.call(this);

        // this.input.setAttribute('data-decimals','4');
        // this.input.setAttribute('step','0.1');

        // let configEFloat = {
        //     decrementButton: "<strong>-</strong>", // button text
        //     incrementButton: "<strong>+</strong>", // ..
        //     groupClass: "", // css class of the resulting input-group
        //     buttonsClass: "btn-outline-secondary",
        //     buttonsWidth: "25px",
        //     textAlign: "center",
        //     autoDelay: 500, // ms holding before auto value change
        //     autoInterval: 100, // speed of auto value change
        //     boostThreshold: 10, // boost after these steps
        //     boostMultiplier: "auto", // you can also set a constant number as multiplier
        //     locale: null // the locale for number rendering; if null, the browsers language is used
        // };
        // $(this.input).inputSpinner(configEFloat);

        return this;
    }

    // //Override because of input spinner
    // EFloatCtrl.prototype.SetRawValue = function(valueStr,notify=false) {
    //     $(this.input).val(valueStr);
    //     if(notify) {
    //         this.input.dispatchEvent(new Event('change', { 'bubbles': true }));
    //     }
    //     return this;
    // };


    /* EDOUBLECTRL */
    function EDoubleCtrl(params={}, createDom=true) {
        EAttributeTextCtrlA.call(this,params,false);

        //parameters
        this.inputTransferFunction = function(value) {
            var valueStr = value.toString(); 
            return valueStr;
        };
        this.outputTransferFunction = function(valueStr) {
            var value = Number.parseFloat(valueStr); 
            return value;
        };
        this.validateFunction = function(valueStr) {
            if(Number.isNaN(Number.parseFloat(valueStr))) {
                throw new Error('Illegal value: Value is not an number!');
            }
            return true;
        } //Shall throw an Error if validation fails

        jsa.CopyParams(this,params);

        if(createDom) {
            this.CreateDom();
        }

        return this;
    }
    EDoubleCtrl.prototype = Object.create(EAttributeTextCtrlA.prototype);

    EDoubleCtrl.prototype.CreateDom = function() {
        EAttributeTextCtrlA.prototype.CreateDom.call(this);

        // this.input.setAttribute('data-decimals','8');
        // this.input.setAttribute('step','0.1');

        // let configEDouble = {
        //     decrementButton: "<strong>-</strong>", // button text
        //     incrementButton: "<strong>+</strong>", // ..
        //     groupClass: "", // css class of the resulting input-group
        //     buttonsClass: "btn-outline-secondary",
        //     buttonsWidth: "25px",
        //     textAlign: "center",
        //     autoDelay: 500, // ms holding before auto value change
        //     autoInterval: 100, // speed of auto value change
        //     boostThreshold: 10, // boost after these steps
        //     boostMultiplier: "auto", // you can also set a constant number as multiplier
        //     locale: null // the locale for number rendering; if null, the browsers language is used
        // };

        // $(this.input).inputSpinner(configEDouble);

        return this;
    }

    // //Override because of input spinner
    // EDoubleCtrl.prototype.SetRawValue = function(valueStr,notify=false) {
    //     $(this.input).val(valueStr);
    //     if(notify) {
    //         this.input.dispatchEvent(new Event('change', { 'bubbles': true }));
    //     }
    //     return this;
    // };



    /* EREFERENCECTRL */
    function EReferenceCtrl(params={}, createDom=true) {
        EAttributeTextCtrlA.call(this,params,false);

        //parameters
        this.typeName = 'EObject';
        this.packageNs = '';
        this.containment = false;
        this.scope = 'global';
        this.customFilter = null; //if not null, the local filter can be used.
        this.customFilterScope = 'SELF'; //can be SELF, RESOURCE, ROOT
        this.emptyAutocompleteMsg = 'None';


        this.inputTransferFunction = function(value) {
            //forward string values directly
            if(typeof(value) === 'string') { 
                return value;
            }
            //the input is expected to be an array of eObjects synced by EOQ which means they have an id 
            if(this.upperBound == -1 || this.upperBound > 1) { 
                let valueArray = value;//.array();
                let nObjects = valueArray.length;
                let valueStrs = [];
                for(let i=0;i<nObjects;i++) {
                    let o = valueArray[i];
                    let c = o.eClass;
                    let valueStr = this.CreateObjectTxtLabel(c.get('name'),
                                                            this.ecoreSync.rlookup(o),
                                                            o.get('name'));
                    valueStrs.push(valueStr);
                }
                let valueStr = valueStrs.join(';');
                return valueStr;
            } else if(this.upperBound==1) {
                let valueStr = '';
                if(value) {
                    let o = value;
                    let c = o.eClass;
                    valueStr = this.CreateObjectTxtLabel(c.get('name'),
                                                         this.ecoreSync.rlookup(o),
                                                            o.get('name'));
                }
                return valueStr;
            }
            return 'ERROR'; //should never go here
        };
        this.outputTransferFunction = function(valueStr) {
            let value = null; 
            let valueSegments = valueStr.split(';');
            let objectIds = [];
            for(let i=0;i<valueSegments.length;i++) {
                let valueSegment = valueSegments[i];
                let idStrs = valueSegment.match(/#\d+/g);
                if(idStrs) { //neglegt any illegal segments, which does not contain an object id.
                    let idStr = idStrs[0]; //array must have exactly one element since it was validated before
                    objectIds.push(Number.parseInt(idStr.substring(1))); //omit the # at the beginning
                }
            }
            if(this.upperBound==1) {
                if(objectIds.length==0) {
                    value = Promise.resolve(null);
                } else {
                    let objectId = objectIds[0]; //allways take the first one
                    value = this.ecoreSync.getObject(objectId);
                }
            } else { //upper bound > 1
                if(objectIds.length==0) {
                    value = Promise.resolve([]);
                } else {
                    let promises = [];
                    for(let i=0;i<objectIds.length;i++) {
                        let objectId = objectIds[i];
                        promises.push(this.ecoreSync.getObject(objectId));
                    }
                    value = Promise.all(promises);
                }
            }
            return value;
        };
        this.validateFunction = function(valueStr) {
            if(valueStr!='') { //empty string is the deletion of any reference
                let valueSegments = valueStr.split(';');
                let errorIndications = [];
                for(let i=0;i<valueSegments.length;i++) {
                    let valueSegment = valueSegments[i];
                    let idStrs = valueSegment.match(/#\d+/g);
                    if(!idStrs || idStrs.length!=1 || idStrs[0]=='') {
                        errorIndications.push('Segment '+i+'is invalid. (no or multiple ids #...)');
                    }
                }
                if(errorIndications.length>0) {
                    throw new Error(errorIndications.join('</br>'));
                }
            }
            return true;
        }; //Shall throw an Error if validation fails

        jsa.CopyParams(this,params);

        //internals
        this.autoCompleteEntries = null;
        //internal callbacks
        var self = this;
        this.autoHideLock = true;
        this.onClickDocumentAutocompleteClose = function(event) {
            if(!self.autoHideLock) {
                self.HideAutocomplete();
            }
        };
        /*
        this.onClickAutocompleteStayOpen = function(event){
            event.stopPropagation();
        };
        */
        this.releaseAutoHideLock = function(){
            self.autoHideLock = false;
        };
        this.engageAutoHideLock = function(){
            self.autoHideLock = true;
        };

        //create the DOM
        if(createDom) {
            this.CreateDom();
        }

        return this;
    };
    EReferenceCtrl.prototype = Object.create(EAttributeTextCtrlA.prototype);

    EReferenceCtrl.prototype.CreateDom = function() {
        EAttributeTextCtrlA.prototype.CreateDom.call(this);

        let self = this;
        this.autoCompleteBox = new EReferenceAutoCompleteBox({
            parentCtrl: this,
            scope: this.scope,
            startVisible: false,
            hasSelectButtons: !(1==this.upperBound),
            hasScopeCustom: this.customFilter,
            onSelectAllCallback: function(event) {self.OnAutocompleteSelectAll(event);},
            onSelectNoneCallback: function(event) {self.OnAutocompleteSelectNone(event);},
            onSelectInvertCallback: function(event) {self.OnAutocompleteSelectInvert(event);},
            onFilterInputCallback: function(event) {self.OnAutocompleteFilterInput(event)}
        }); 

        jsa.RedirectDomCallbackToUiElement(this.input,'click',this,this.OnFocusCallback);
        //jsa.RedirectDomCallbackToUiElement(this.input,'onblur',this,this.OnUnfocusCallback);

        //listen to promisedValues
        // let self = this;
        // if(this.promisedValue instanceof Promise) {
        //     this.promisedValue.then(function(value) {
        //         self.OnPromisedValue(value);
        //     });
        // }

        return this;
    };

    EReferenceCtrl.prototype.OnFocusCallback = function(event) {
        if(!this.readonly) {
            this.ShowAutocomplete();
        }
    };

    /*
    EReferenceCtrl.prototype.OnUnfocusCallback = function(event) {
        this.HideAutocomplete();
    };
    */

    EReferenceCtrl.prototype.ShowAutocomplete = function() {
        let app = this.GetApp();
        if(app) {

            if(!this.autoCompleteBox.isVisible) {
                //this.autoCompleteBox.GetDomElement().addEventListener('mousedown', this.onClickAutocompleteStayOpen);
                this.autoCompleteBox.GetDomElement().addEventListener('mouseout', this.releaseAutoHideLock);
                this.autoCompleteBox.GetDomElement().addEventListener('mouseover', this.engageAutoHideLock);
                document.addEventListener('mousedown', this.onClickDocumentAutocompleteClose);
                app.AddChild(this.autoCompleteBox);
                this.autoCompleteBox.Show();
                /*HACK: Delay the auto hide function, otherwise event propagation it will 
                immediately close the bubble with the same event. 
                Moreover, the delay prevents double click issues. */
                this.autoHideLock = true;
                var self = this;
                this.autoHideDelayTimeout = window.setTimeout(function() {
                    self.releaseAutoHideLock();
                },this.autoHideDelay);
            }

            this.AdaptAutocompleteSize();

            //load the contents 
            if(null == this.autoCompleteEntries) {
                this.LoadAutocompleteList();
            }
        }
        return this;
    };

    EReferenceCtrl.prototype.AdaptAutocompleteSize = function() {
        //set the position of the box
        let bh = jsa.GetBrowserHeight();
        //retrieve the current position
        let rect = this.domElement.getBoundingClientRect();
        //top or bottom?
        let deltaTop = rect.top-20;
        let deltaBottom = bh-rect.bottom;
        let x = rect.left;
        let y = 0;
        let w = rect.width;
        let mh = Math.max(deltaTop,deltaBottom); //max height
        //max-heigh must be set before, such that the real height can be read back afterwards
        let fixedElemtHeight = this.autoCompleteBox.filterInputCtrl.domElement.getBoundingClientRect().height+
                                this.autoCompleteBox.info.domElement.getBoundingClientRect().height;
        this.autoCompleteBox.list.domElement.style.maxHeight = (mh-fixedElemtHeight)+'px'; //-x corrects for the filter input

        let acRect = this.autoCompleteBox.domElement.getBoundingClientRect();
        let h = acRect.height; //real height
        if(deltaTop > deltaBottom) {
            y = rect.top-h;
        } else {
            y = rect.bottom;
        }
        this.autoCompleteBox.domElement.style.left = x+'px';
        this.autoCompleteBox.domElement.style.top = y+'px';
        this.autoCompleteBox.domElement.style.width = w+'px';
    };

    EReferenceCtrl.prototype.HideAutocomplete = function() {
        let app = this.GetApp();
        if(app) {
            if(this.autoCompleteBox.isVisible) {
                window.clearTimeout(this.autoHideDelayTimeout);
                //this.autoCompleteBox.GetDomElement().removeEventListener('mousedown', this.onClickAutocompleteStayOpen);
                this.autoCompleteBox.GetDomElement().removeEventListener('mouseout', this.releaseAutoHideLock);
                this.autoCompleteBox.GetDomElement().removeEventListener('mouseover', this.engageAutoHideLock);
                document.removeEventListener('mousedown', this.onClickDocumentAutocompleteClose);
                this.autoCompleteBox.Hide();
                app.RemoveChild(this.autoCompleteBox);
            }
        } 
        return this;
    };

    EReferenceCtrl.prototype.CreateObjectTxtLabel = function(typeName,id,name) {
        let unknown = '';
        let nameTag = '';
        let typeTag = '???';
        if(name) {
            let conflictFreeName = name.replace(';','').replace('\'','').replace('#','');
            nameTag = '\''+conflictFreeName+'\':';
        }
        if(typeName) {
            typeTag = typeName;
        }
        
        return nameTag+typeTag+'[#'+id+']';
    };

    EReferenceCtrl.prototype.RefreshAutocompleteCheckedStatus = function() {
        if(this.autoCompleteEntries) {
            let valueStr = this.input.value;
            for(let i=0;i<this.autoCompleteEntries.length;i++) {
                let entry = this.autoCompleteEntries[i];
                let checked = valueStr.includes('#'+entry.data.objectInfo.id);
                entry.SetValue(checked);
            }
        }
    };
    
    EReferenceCtrl.prototype.ClearAutocompleteList = function() {
        //clear the old list
        if(null == this.autoCompleteEntries || this.autoCompleteEntries.length==0) { //null  happens only the first time, when no objects were loaded before
            this.autoCompleteBox.list.SetContent('');   
        } else { 
            for(let i=0;i<this.autoCompleteEntries.length;i++) {
                this.autoCompleteEntries[i].Dissolve();
            }   
        }
        this.autoCompleteBox.info.SetContent('');   
        return this;
    };

    EReferenceCtrl.prototype.IndicateAutocompleteError = function(message) {
        //clear the old list
        this.ClearAutocompleteList();
        this.autoCompleteBox.info.SetContent('Error: '+message);   
        this.AdaptAutocompleteSize();
        return this;
    };

    EReferenceCtrl.prototype.RebuildAutocompleteList = function(objectInfoList) {
        //clear the old list
        this.ClearAutocompleteList();
        //create new entry elements
        this.autoCompleteEntries = [];
        let n = objectInfoList.length;
        if(n>0) {
            //pick the right constructor
            entryConstructor = (this.upperBound==1)?jsa.RadioCtrl:jsa.CheckboxCtrl;
            //let valueStr = this.input.value;
            for(let i=0;i<n;i++) {
                let o = objectInfoList[i];
                //let checked = valueStr.includes('#'+o.id);
                let pathStr = '';
                for(let j=0;j<o.parentNames.length;j++) {
                    let pname = o.parentNames[j];
                    let pid = o.parentIds[j];
                    pathStr += (pname?pname:'#'+pid)+'/';
                }
                let objectLabel = this.CreateObjectTxtLabel(o.type,o.id,o.name);
                let label = objectLabel + '('+pathStr+')';
                let entryName = this.autoCompleteBox.id+'_autocompleteEntry'; //shall be unique in order to make the radio buttons work
                let newEntry = new entryConstructor({
                    name: entryName,
                    content: label,
                    checked: false, //will be updated afterwards
                    data: {
                        cleanLabel: label,
                        ctrl: this,
                        objectInfo: o
                    },
                    onChangeCallback: function(event) {
                        let isChecked = this.GetValue();
                        let referenceCtrl = this.data.ctrl;
                        let o = this.data.objectInfo;
                        let currentValue = referenceCtrl.input.value;
                        let newValue = '';
                        if(referenceCtrl.upperBound==1) {
                            if(true==isChecked) {
                                newValue = referenceCtrl.CreateObjectTxtLabel(o.type,o.id,o.name);
                            }
                        } else { //upper bound > 1
                            if(true==isChecked) { //an element has been added
                                let selectIndex = referenceCtrl.input.selectionStart;
                                let splitPosition = currentValue.substring(0,selectIndex).lastIndexOf(';');
                                let firstPart = currentValue.substring(0,splitPosition);
                                let lastPart = currentValue.substring(splitPosition+1);
                                let firstSegments = (''==firstPart)?[]:firstPart.split(';');
                                let lastSegments = (''==lastPart)?[]:lastPart.split(';');
                                let newPart = referenceCtrl.CreateObjectTxtLabel(o.type,o.id,o.name);
                                let newValueSegments = firstSegments.concat([newPart]).concat(lastSegments);
                                newValue = newValueSegments.join(';');
                            } else { //false
                                let valueSegments = currentValue.split(';');
                                let newValueSegments = [];
                                for(let i=0;i<valueSegments.length;i++) {
                                    let segment = valueSegments[i];
                                    if(!segment.includes('#'+o.id)) {
                                        newValueSegments.push(segment);
                                    }
                                }
                                newValue = newValueSegments.join(';');
                            }
                        }
                        referenceCtrl.input.value = newValue;
                        referenceCtrl.onChangeCallback(null);
                    }
                });
                this.autoCompleteBox.list.AddChild(newEntry);
                this.autoCompleteEntries.push(newEntry);
            }
            this.RefreshAutocompleteCheckedStatus();
            this.autoCompleteBox.info.SetContent(n+' elements available.'); 
        } else {
            this.autoCompleteBox.list.SetContent(this.emptyAutocompleteMsg); 
            this.autoCompleteBox.info.SetContent('0 elements available.'); 
        }

        this.AdaptAutocompleteSize();

        return this;
    };

    EReferenceCtrl.prototype.RefreshAutocompleteCheckedStatus = function() {
        if(this.autoCompleteEntries) {
            let valueStr = this.input.value;
            for(let i=0;i<this.autoCompleteEntries.length;i++) {
                let entry = this.autoCompleteEntries[i];
                let checked = valueStr.includes('#'+entry.data.objectInfo.id);
                entry.SetValue(checked);
            }
        }
    };

    EReferenceCtrl.prototype.LoadAutocompleteList = function() {
        if(this.ecoreSync) {
            let cmd = CMD.Cmp();
            let cmdOffset = 0;
            
            switch(this.scope) {
                case 'local': //based on the current resource
                    //find the containing resource
                    if(this.eObject) {
                        let oid = this.ecoreSync.rlookup(eObject);
                        cmd.Get(QRY.Obj(oid).Met('ALLPARENTS'));
                        cmd.Get(QRY.His(-1).Sel(QRY.Met('CLASSNAME').Equ('ModelResource')));
                        cmd.Get(QRY.Met('IF',[QRY.His(-1).Met('SIZE').Equ(1),QRY.His(-1).Idx(0),QRY.Obj(0)]));
                        cmd.Get(QRY.His(-1).Ino(this.typeName))
                        cmdOffset = 3;
                    } else {
                        cmd.Get(QRY.Obj(0));
                    }
                    break;
                case 'global': //complete workspace
                    cmd.Get(QRY.Obj(0).Ino(this.typeName));
                    break;
                case 'custom':
                    switch(this.customFilterScope) {
                        case 'SELF':{
                                let oid = this.ecoreSync.rlookup(eObject);
                                let qry = QRY.Obj(oid);
                                Array.prototype.push.apply(qry.v, this.customFilter.v);//append the custom query to the self object
                                cmd.Get(qry);
                            }
                            break;
                        case 'RESOURCE': {
                                let oid = this.ecoreSync.rlookup(eObject);
                                cmd.Get(QRY.Obj(oid).Met('ALLPARENTS'));
                                cmd.Get(QRY.His(-1).Sel(QRY.Met('CLASSNAME').Equ('ModelResource')));
                                cmd.Get(QRY.Met('IF',[QRY.His(-1).Met('SIZE').Equ(1),QRY.His(-1).Idx(0),QRY.Obj(0)]));
                                cmdOffset = 3;
                                let qry = QRY.His(-1);
                                Array.prototype.push.apply(qry.v, this.customFilter.v); //append what shall be done with the resource
                                cmd.Get(qry);
                            }
                            break;
                        case 'ROOT': {
                                cmd.Get(this.customFilter);
                            }
                            break;
                        default:
                            throw new Error('Unknown custom filter scope: '+this.customFilterScope);
                    }
                    break;
                default:
                    throw new Error('Unknown scope: '+this.scope);
            }
            
            
            cmd.Get(QRY.His(-1).Met("CLASSNAME"))
            cmd.Get(QRY.His(-2).Try(QRY.Pth("name"),''))
            cmd.Get(QRY.His(-3).Met("ALLPARENTS"))
            cmd.Get(QRY.His(-1).Try(QRY.Pth("name"),''));

            var self = this;
            ecoreSync.remoteExec(cmd).then(function(val) {
                //update the content of the autocomplete box
                var nElements = val[cmdOffset+0].length;
                let possibleObjects = [];
                for(let i=0;i<nElements;i++) {
                    let parentNames = val[cmdOffset+4][i];
                    let parentIds = [];
                    for(let j=0;j<val[cmdOffset+3][i].length;j++) {
                        parentIds.push(val[cmdOffset+3][i][j].v);
                    }
                    //store all the information gathered
                    possibleObjects.push({
                        id: val[cmdOffset+0][i].v,
                        type: val[cmdOffset+1][i],
                        name: val[cmdOffset+2][i],
                        parentNames: parentNames,
                        parentIds: parentIds
                    });
                }
                self.RebuildAutocompleteList(possibleObjects);
            }).catch(function(e) {
                self.IndicateAutocompleteError(e.toString());
            });
        }
        return this;
    };

    //@Override
    EReferenceCtrl.prototype.OnObjectChange = function(change) {
        var self=this;
        var newValue = this.eObject.get(this.featureName);
        if(newValue) {
                self.SetValue(newValue);
                self.SetReadonly(this.readOnlyAfterInitialized);
        } else { //value is null
            this.SetValue(newValue);
            this.SetReadonly(this.readOnlyAfterInitialized);
        }
    };

    EReferenceCtrl.prototype.OnAutocompleteFilterInput = function(event) {
        let expression = this.autoCompleteBox.filterInputCtrl.GetValue();
        let n = expression.length;
        if(2 < n) {
            this.FilterAutocompleteList(expression);
        } else if(0 == n) {
            this.UnfilterAutocompleteList();    
        }
    };

    EReferenceCtrl.prototype.FilterAutocompleteList = function(expression) {
        let n = this.autoCompleteEntries.length;
        let b = 0;
        for(let i=0;i<n;i++) {
            let entry = this.autoCompleteEntries[i];
            let name = entry.data.cleanLabel;
            if(name.includes(expression)) {
                //highlight filter match
                let re = RegExp("("+expression+")",'g');
                let hlContent = name.replace(re,"<span class='hl'>$1</span>");
                entry.SetContent(hlContent);
                entry.Show();
                b++;
            } else {
                entry.Hide();
            }
        } 
        this.autoCompleteBox.info.SetContent(b+' of '+n+' match \''+expression+'\'.'); 
    };

    EReferenceCtrl.prototype.UnfilterAutocompleteList = function() {
        let n = this.autoCompleteEntries.length;
        for(let i=0;i<n;i++) {
            let entry = this.autoCompleteEntries[i];
            entry.SetContent(entry.data.cleanLabel); //delete any highlighting
            entry.Show();
        } 
        this.autoCompleteBox.info.SetContent(n+' elements available.'); 
    };

    EReferenceCtrl.prototype.AutocompleteSelectAll = function(event) {
        let n = this.autoCompleteEntries.length;
        for(let i=0;i<n;i++) {
            let entry = this.autoCompleteEntries[i];
            if(entry.isVisible) { //restrict button to the visible list
                entry.SetRawValue(true,true);
            }
        }
    };

    EReferenceCtrl.prototype.AutocompleteSelectNone = function(event) {
        for(let i=0;i<this.autoCompleteEntries.length;i++) {
            let entry = this.autoCompleteEntries[i];
            if(entry.isVisible) { //restrict button to the visible list
                entry.SetRawValue(false,true);
            }
        }
    };

    EReferenceCtrl.prototype.AutocompleteSelectInvert = function(event) {
        for(let i=0;i<this.autoCompleteEntries.length;i++) {
            let entry = this.autoCompleteEntries[i];
            if(entry.isVisible) { //restrict button to the visible list
                let b = entry.GetValue();
                entry.SetRawValue(!b,true);
            }
        }
    };

    EReferenceCtrl.prototype.OnAutocompleteSelectAll = function(event) {
        this.AutocompleteSelectAll();
    };

    EReferenceCtrl.prototype.OnAutocompleteSelectNone = function(event) {
        this.AutocompleteSelectNone();
    };

    EReferenceCtrl.prototype.OnAutocompleteSelectInvert = function(event) {
        this.AutocompleteSelectInvert();
    };

    //@Override
    EReferenceCtrl.prototype.OnObjectAdd = function(change) {
        this.OnObjectAddOrRemove(change);
    };

    //@Override
    EReferenceCtrl.prototype.OnObjectRemove = function(change) {
        this.OnObjectAddOrRemove(change);
    };

    //generic multi element change handler
    EReferenceCtrl.prototype.OnObjectAddOrRemove = function(change) {
        // var newValue = this.eObject.get(this.featureName);
        let self = this;
        this.ecoreSync.get(this.eObject,this.featureName).then(function(newValue) {
            self.SetValue(newValue);
        })
    };

    EReferenceCtrl.prototype.Dissolve = function() {
        if(this.autoCompleteBox) {
            this.autoCompleteBox.Dissolve();
        }
        EAttributeTextCtrlA.prototype.Dissolve.call(this);
    };

    /* EREFERENCECTRLAUTOCOMPLETEBOX */

    function EReferenceAutoCompleteBox(params,createDom=true) {
        jsa.CustomFlatContainer.call(this,params,false);

        //params
        this.parentCtrl = null;
        this.scope = 'local';
        this.style = ['reference-textctrl-autocomplete-box'];
        this.onSelectAllCallback = function(event) {};
        this.onSelectNoneCallback = function(event) {};
        this.onSelectInvertCallback = function(event) {};
        this.onFilterInputCallback = function(event) {};
        this.hasScopeGlobal = true;
        this.hasScopeLocal = true;
        this.hasScopeCustom = true;
        this.hasSelectButtons = false;
        

        jsa.CopyParams(this,params);

        //internals
        this.list = null;

        this.scopeButtons = { 
            local : {
                styles: ['autocomplete-box-scope-local'],
                activeStyles: ['autocomplete-box-scope-local','autocomplete-box-scope-local-active'],
                onClickCallback: function() {this.OnScopeSelect('local');},
                enabled: this.hasScopeLocal
            },
            global : {
                styles: ['autocomplete-box-scope-global'],
                activeStyles: ['autocomplete-box-scope-global','autocomplete-box-scope-global-active'],
                onClickCallback: function() {this.OnScopeSelect('global');},
                enabled: this.hasScopeGlobal
            },
            custom : {
                styles: ['autocomplete-box-scope-custom'],
                activeStyles: ['autocomplete-box-scope-custom','autocomplete-box-scope-custom-active'],
                onClickCallback: function() {this.OnScopeSelect('custom');},
                enabled: this.hasScopeCustom
            }
        };

        this.buttons = {
            close : {
                styles: ['autocomplete-box-close'],
                onClickCallback: function() {this.OnCloseButton();}
            }
        };

        //select control buttons
        this.selectButtons = {
            selectAll : {
                styles: ['autocomplete-box-select-all'],
                onClickCallback: this.onSelectAllCallback
            },
            selectNone : {
                styles: ['autocomplete-box-select-none'],
                onClickCallback: this.onSelectNoneCallback
            },
            selectInvert : {
                styles: ['autocomplete-box-select-invert'],
                onClickCallback: this.onSelectInvertCallback
            }
        };

        //Create DOM elements
        if(createDom) {
            this.CreateDom();
        }

        return this;
    }

    EReferenceAutoCompleteBox.prototype = Object.create(jsa.CustomFlatContainer.prototype);

    EReferenceAutoCompleteBox.prototype.CreateDom = function() {
        jsa.CustomFlatContainer.prototype.CreateDom.call(this);
        //search filter input
        this.filterInputCtrl = new jsa.TextCtrl({
            style: ['jsa-text-ctrl','reference-textctrl-autocomplete-box-filter-textctrl'],
            // ctrlStyle: ['jsa-text-ctrl-input','autocomplete-box-filter-textctrl-ctrl'],
            placeholder : 'Type filter list',
            onInputCallback : this.onFilterInputCallback
        });
        this.AddChild(this.filterInputCtrl);

        //list of entries
        this.list = new jsa.CustomContainer({
            style: ['reference-textctrl-autocomplete-box-list'],
            containerStyle : ['reference-textctrl-autocomplete-box-list-container'],
            content: '',
            visible: false
        });
        this.AddChild(this.list);

         //info bar
         this.info = new jsa.CustomContainer({
            containerElementType: 'small',
            style: ['reference-textctrl-autocomplete-box-info'],
            content: 'Loading...',
            visible: false
        });
        this.AddChild(this.info);


        //add buttons 
        for(b in this.buttons) {
            let buttonInfo = this.buttons[b];
            let button = new jsa.CustomUiElement({
                style: buttonInfo.styles
            }); 
            this.AddChild(button);
            if(buttonInfo.onClickCallback) {
                jsa.RedirectDomCallbackToUiElement(button.GetDomElement(),'click',this,buttonInfo.onClickCallback);
            }
            buttonInfo.button = button;
        }

        for(b in this.scopeButtons) {
            let buttonInfo = this.scopeButtons[b];
            if(buttonInfo.enabled) {
                let styles = (b==this.scope)?buttonInfo.activeStyles:buttonInfo.styles;
                let button = new jsa.CustomUiElement({
                    style: styles
                }); 
                this.AddChild(button);
                if(buttonInfo.onClickCallback) {
                    jsa.RedirectDomCallbackToUiElement(button.GetDomElement(),'click',this,buttonInfo.onClickCallback);
                }
                buttonInfo.button = button;
            }
        }

        if(this.hasSelectButtons) {
            for(b in this.selectButtons) {
                let buttonInfo = this.selectButtons[b];
                let button = new jsa.CustomUiElement({
                    style: buttonInfo.styles
                }); 
                this.AddChild(button);
                if(buttonInfo.onClickCallback) {
                    jsa.RedirectDomCallbackToUiElement(button.GetDomElement(),'click',this,buttonInfo.onClickCallback);
                }
                buttonInfo.button = button;
            }
        }

        //hack
        if(!this.startVisible) {
            this.Hide();
        }

        return this;

    };

    EReferenceAutoCompleteBox.prototype.OnCloseButton = function() {
        this.parentCtrl.HideAutocomplete();
    };

    EReferenceAutoCompleteBox.prototype.OnScopeSelect = function(scope) {
        if(this.scope != scope) {
            this.scope = scope;
            for(b in this.scopeButtons) {
                let buttonInfo = this.scopeButtons[b];
                if(buttonInfo.button) { // only process visible buttons
                    let styles = (b==this.scope)?buttonInfo.activeStyles:buttonInfo.styles;
                    let button = buttonInfo.button;
                    button.SetStyle(styles);
                }
            }
            this.parentCtrl.scope = scope;
            this.parentCtrl.LoadAutocompleteList();
        }
    };


    return {
        EBoolCtrl : EBoolCtrl,
        EIntCtrl : EIntCtrl,
        EFloatCtrl : EFloatCtrl,
        EDoubleCtrl : EDoubleCtrl,
        EStringCtrl : EStringCtrl,
        EDateCtrl : EDateCtrl,
        EEnumCtrl : EEnumCtrl,
        EReferenceCtrl : EReferenceCtrl,
        EReferenceAutoCompleteBox : EReferenceAutoCompleteBox
    };


})());
