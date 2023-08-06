// 2020 Bjoern Annighoefer

var ACTIONS = ACTIONS || {};

Object.assign(ACTIONS,(function(){

    function ActionParameterControl(parameter,container) {
        this.container = container;
        this.parameter = parameter;
        this.paramtereId = this.container.attr('id')+'-parameter-'+this.parameter.name;
        this.parameterFormRow = $('<div class="form-group row"></div>');
        this.parameterLabel = $('<label for="'+this.paramtereId+'" class="col-sm-2 col-form-label">'+this.parameter.name+' : '+parameter.type+'</label>');
        this.parameterInputDiv = $('<div class="col-sm-10"></div>');
        if(parameter.choices.length>0) {
            this.parameterInput = $('<select class="form-control" id="'+this.paramtereId+'" value="'+this.parameter.default+'">');
            for(var i=0;i<parameter.choices.length;i++) {
                var choice = parameter.choices[i];
                this.parameterInput.append('<option value="'+choice.value+'">'+choice.value+'</option>');
            }
        } else {
            this.parameterInput = $('<input class="form-control" id="'+this.paramtereId+'" value="'+this.parameter.default+'">');
        }

        this.parameterFormRow.append(this.parameterLabel);
        this.parameterFormRow.append(this.parameterInputDiv);
        this.parameterInputDiv.append(this.parameterInput);
        
        this.container.append(this.parameterFormRow);
    }



    function ActionDialog(params,createDom=true) {
        jsa.Modal.call(this,params,false);

        //parameters
        this.containerStyle = ['jsa-modal-container','actions-dialog'];
        this.action = null;
        
        //copy paramters
        jsa.CopyParams(this,params)
        
        if(createDom) {
            this.CreateDom();
        }

        return this;
    }
    
    ActionDialog.prototype = Object.create(jsa.Modal.prototype);

    ActionDialog.prototype.CreateDom = function() {
        //call the underlying dialog Dom creation
        jsa.Modal.prototype.CreateDom.call(this);

        //create action specific content
        this.description = new jsa.CustomUiElement({
            elementType: 'p',
            style: ['description'],
            content: this.action.description
        });
        this.AddChild(this.description)

        this.propertiesTable = new jsa.Table({
            style: ['action-arguments-table']
        });
        this.AddChild(this.propertiesTable);
       
        //Draw the dialog
        this.argumentRows = [];
        
        for(let i=0;i<this.action.parameters.length;i++) {
            let param = this.action.parameters[i];

            let argumentRow = new jsa.TableRow();
            this.propertiesTable.AddChild(argumentRow);
            let argumentNameCol = new jsa.TableCol({
                style: ['name'],
                content: param.name
            });
            argumentRow.AddChild(argumentNameCol);
            let argumentValueCol = new jsa.TableCol({
                style: ['value']
            });
            argumentRow.AddChild(argumentValueCol);

            //add a row for descriptions
            let argumentDescriptionRow = new jsa.TableRow();
            this.propertiesTable.AddChild(argumentDescriptionRow);
            let argumentDescriptionCol1 = new jsa.TableCol({
                style: ['description'],
                content: ''
            });
            argumentDescriptionRow.AddChild(argumentDescriptionCol1);

            let argumentDescriptionCol2 = new jsa.TableCol({
                style: ['description'],
                content: param.description
            });
            argumentDescriptionRow.AddChild(argumentDescriptionCol2);

            let argumentCtrlParams = {
                // style: ['form-group','no-margin'],
                // ctrlStyle: ['form-control','form-control-sm'],
                value: param.default,
                readonly : false,
                placeholder : param.type,
                data: {eObject: null, featureName: ''},
                onChangeCallback : function(e) {
                    return true;         
                }
            };

            let argumentCtrl = null;
            switch(param.type) {
                case "String":
                    argumentCtrl = new ECORESYNC_UI.EStringCtrl(argumentCtrlParams);
                    break;
                case "Bool":
                case "Boolean":
                    argumentCtrl = new ECORESYNC_UI.EBoolCtrl(argumentCtrlParams);
                    break;
                case "Integer":
                case "Int":
                    argumentCtrl = new ECORESYNC_UI.EIntCtrl(argumentCtrlParams);
                    break;
                case "Real":
                case "Float":
                    argumentCtrl = new ECORESYNC_UI.EFloatCtrl(argumentCtrlParams);
                    break;
                case "Double":
                    argumentCtrl = new ECORESYNC_UI.EDoubleCtrl(argumentCtrlParams);
                    break;
                case "Date":
                    argumentCtrl = new ECORESYNC_UI.EDateCtrl(argumentCtrlParams);
                    break;      
                default:
                    //assume that this are object inputs
                    argumentCtrlParams = {
                        // style: ['form-group','no-margin'],
                        // ctrlStyle: ['form-control','form-control-sm'],
                        value: param.upperBound==1?null:[],
                        readonly : false,
                        placeholder : param.type + ((param.upperBound==1)?'':'['+param.lowerBound+'..'+((param.upperBound==-1)?'*':param.upperBound)+']'),
                        upperBound: param.upperBound,
                        lowerBound: param.lowerBound,
                        typeName: param.type,
                        containment: false,
                        packageNs: '', //TODO
                        ecoreSync: $app.ecoreSync,
                        data: null,
                        onChangeCallback : function(e) {
                            return true;     
                        },
                        inputTransferFunction : function(value) {
                            let valueStr = value;
                            return valueStr;
                        },
                        outputTransferFunction : function(valueStr) {
                            let value = ''; 
                            let valueSegments = valueStr.split(';');
                            let objectIds = [];
                            for(let i=0;i<valueSegments.length;i++) {
                                let valueSegment = valueSegments[i];
                                let idStrs = valueSegment.match(/#\d+/g);
                                if(idStrs) { //neglect any illegal segments, which does not contain an object id.
                                    let idStr = idStrs[0]; //array must have exactly one element since it was validated before
                                    objectIds.push(Number.parseInt(idStr.substring(1))); //omit the # at the beginning
                                }
                            }
                            if(this.upperBound==1) {
                                if(objectIds.length==0) {
                                    //value = '';
                                    value = null;
                                } else {
                                    let objectId = objectIds[0]; //always take the first one
                                    //value = '#'+objectId;
                                    value = new eoq2.Qry().Obj(objectId);
                                }
                            } else { //upper bound > 1
                                value = [];
                                for(let i=0;i<objectIds.length;i++) {
                                    value.push(new eoq2.Qry().Obj(objectIds[i]));
                                }
                                // if(objectIds.length==0) {
                                //     //value = '[]';
                                    
                                // } else {
                                //     //value = '[#'+objectIds.join(',#')+']';
                                //     value = new eoq2.Qry().Obj(objectId);
                                // }
                            }
                            return value;
                        }
                    }
                    argumentCtrl = new ECORESYNC_UI.EReferenceCtrl(argumentCtrlParams);
                    break;
            }
            argumentValueCol.AddChild(argumentCtrl);

            this.argumentRows[param.name] = {
                row : argumentRow,
                labelCol : argumentNameCol,
                valueCol: argumentValueCol,
                ctrl: argumentCtrl
            };
        }
     
        return this;
    };

    //methods
    ActionDialog.prototype.RestoreUserValues = function(app) {
        for(let i=0;i<this.action.parameters.length;i++) {
            let param = this.action.parameters[i];
            //see if there are any stored values for that field 
            key = 'eoq.actions.'+this.action.categories.join('.')+'.'+this.action.name+'.userParameterValues.'+param.name;
            if(app.settingsManager.Has(key)) {
                let value = app.settingsManager.Get(key)
                let ctrl = this.argumentRows[param.name].ctrl;
                ctrl.SetRawValue(value);
            }
        }
    };

    //methods
    ActionDialog.prototype.PreserveUserValues = function(app) {
        for(let i=0;i<this.action.parameters.length;i++) {
            let param = this.action.parameters[i];
            //see if there are any stored values for that field 
            key = 'eoq.actions.'+this.action.categories.join('.')+'.'+this.action.name+'.userParameterValues.'+param.name;
            let ctrl = this.argumentRows[param.name].ctrl;
            let value = ctrl.GetRawValue();
            app.settingsManager.Set(key,value);
        }
    };

    //methods
    ActionDialog.prototype.UpdatePreview = function() {
        var previewHtml = this.ComposeCommandStr();
        this.previewInput.val(previewHtml);
    };

    /*
    ActionDialog.prototype.GetArguments = function() {
        var args = [];
        for(var i=0;i<this.action.parameters.length;i++) {
            this.action.parameters
            var strVal = this.parameterControls[i].parameterInput.val();

            var val = null;
            switch(this.action.parameters[i].type) {
                case 'String':
                    val = strVal;
                    break;
                case 'Int':
                    val = Number.parseInt(strVal);
                    break;
                case 'Float':
                    val = Number.parseInt(strVal);
                    break;

            }

            args.push(val);
        }
        return args;
    }; */

    // ActionDialog.prototype.ComposeCommandStr = function() {
    //     var commandStr = 'ASYNCCALL '+this.action.name;
    //     commandStr += ' '+this.ComposeArgsStr();
    //     return commandStr;
    // };

    // ActionDialog.prototype.ComposeArgsStr = function() {
    //     var actionParameters = [];
    //     for(var i=0;i<this.action.parameters.length;i++) {
    //         let param = this.action.parameters[i];
    //         let ctrl = this.argumentRows[param.name].ctrl;
    //         let value = ctrl.GetValue();
    //         actionParameters.push(this.ParameterToString(param,value));
    //     }
    //     return '['+actionParameters.join(',')+']';
    // };

    ActionDialog.prototype.GetArgValues = function() {
        var argValues = [];
        for(var i=0;i<this.action.parameters.length;i++) {
            let param = this.action.parameters[i];
            let ctrl = this.argumentRows[param.name].ctrl;
            let value = ctrl.GetValue();
            argValues.push(value);
        }
        return argValues;
    };

    ActionDialog.prototype.ParameterToString = function(parameter,value) {
        paramString = '';
        if(parameter.type == "String") {
            paramString = '\''+value.toString()+'\'';
        } else {
            paramString = value.toString();
        }
        return paramString;
    };

    // ActionDialog.prototype.BuildCommandExample = function() {
    //     var commandStr = 'ASYNCCALL '+this.action.name;
    //     var actionParameters = [];
    //     for(var i=0;i<this.action.parameters.length;i++) {
    //         var parameter = this.action.parameters[i];
    //         actionParameters.push('&lt;'+parameter.name+':'+parameter.type+'&gt;');
    //     }
    //     commandStr += ' ['+actionParameters.join(',')+']';
    //     return commandStr;
    // };

    // ActionDialog.prototype.BuildResultExampleStr= function() {
    //     var resultStr = 'OK &lt;transcationId:Int&gt; CALL ';
    //     var resultParameters = [];
    //     for(var i=0;i<this.action.results.length;i++) {
    //         var resultParameter = this.action.results[i];
    //         resultParameters.push('&lt;'+resultParameter.name+':'+resultParameter.type+'&gt;');
    //     }
    //     resultStr += ' ['+resultParameters.join(',')+'] [&lt;output1:String&gt;&lt;output2:String&gt;,...]';
    //     return resultStr;
    // };


    function ActionRunnerDialog(params,createDom=true) {
        jsa.Modal.call(this,params,false);

        //parameters
        this.action = null;
        
        //copy params
        jsa.CopyParams(this,params);

        if(createDom) {
            this.CreateDom();
        }

        return this;
    };

    ActionRunnerDialog.prototype = Object.create(jsa.Modal.prototype);

    ActionRunnerDialog.prototype.CreateDom = function(text) {
        jsa.Modal.prototype.CreateDom.call(this);

        //this.panel = $('<div class="actions-dialog"></div>');

        //this.form = $('<form><form>');
        //this.previewPanel = $('<div class="form-group"></div>');
        //this.previewInput = $('<input class="form-control preview" value="'+commandStr+'" readonly/>');
        //this.outputPanel = $('<div class="form-group"></div>');
        //this.outputArea = $('<div class="div-textarea form-control bg-secondary text-white output" rows="10" readonly/></div>');
        this.outputArea = new jsa.CustomFlatContainer({
            style: ['output']
        });
        this.AddChild(this.outputArea);
        //this.progressPanel = $('<div class="form-group progress"></div>');
        //this.progressBar = $('<div class="progress-bar progress progress-bar-striped progress-bar-animated" role="progressbar" aria-valuenow="75" aria-valuemin="0" aria-valuemax="100" style="width: 75%"></div>')
        this.progressBar = new jsa.Progressbar({
            hasInfo: true,
            isAnimated: true
        });
        this.AddChild(this.progressBar);
        // this.resultPanel = $('<div class="result"></div>');
        this.resultPanel = new jsa.CustomFlatContainer({
            style: ['result'],
            startVisible: false
        });
        this.AddChild(this.resultPanel);
        // this.errorPanel = $('<div class="error"></div>');
        this.errorPanel = new jsa.CustomFlatContainer({
            style: ['error'],
            startVisible: false
        });
        this.AddChild(this.errorPanel);
        // this.successPanel = $('<div class="success"></div>');
        this.successPanel = new jsa.CustomFlatContainer({
            style: ['success'],
            startVisible: false
        });
        this.AddChild(this.successPanel);
        //this.errorArea = $('<div class="form-control bg-secondary output error"/></div>');
        
        //compose dialog
        //this.previewPanel.append(this.previewInput);

        //this.outputPanel.append(this.outputArea);

        //this.progressPanel.append(this.progressBar);

        //this.resultPanel.append(this.resultArea)

        //this.form.append(this.previewPanel);
        //this.form.append(this.outputPanel);
        //this.form.append(this.progressBar);
        //this.form.append(this.progressPanel);
        
        // this.panel.append(this.form);

        // this.panel.append(this.successPanel);
        // this.successPanel.hide();
        // this.panel.append(this.errorPanel);
        // this.errorPanel.hide();
        // this.panel.append(this.resultPanel);
        // this.resultPanel.hide();
        

        // this.GetContainingDom().appendChild(this.panel[0]);

        return this;
    };

    ActionRunnerDialog.prototype.SetOutput = function(text) {
        this.outputArea.SetContent(text);
        $(this.outputArea.GetDomElement()).scrollTop(this.outputArea.GetDomElement().scrollHeight);
    };

    ActionRunnerDialog.prototype.SetProgress = function(progress) {
        //this.progressBar.css('width', progress+'%').attr('aria-valuenow', progress);  
        this.progressBar.SetProgress(progress);
    };

    ActionRunnerDialog.prototype.SetStatus = function(status) {
        // this.progressBar.html(status);  
        this.progressBar.SetInfo(status);
    };

    ActionRunnerDialog.prototype.SetRun = function(info) {
        this.successPanel.Show();
        this.successPanel.SetContent(info);
    };

    ActionRunnerDialog.prototype.SetFinished = function(info) {
        this.SetProgress(100);
        this.progressBar.SetAnimated(false);
        this.progressBar.SetSuccess(true);
        // this.progressBar.addClass("bg-success").removeClass("progress-bar-animated");
        this.successPanel.Show();
        this.successPanel.SetContent(info);
    };

    ActionRunnerDialog.prototype.SetResult = function(resultStr) {
        if(resultStr && '' != resultStr) {
            this.resultPanel.Show();
            this.resultPanel.SetContent(resultStr);
        }
    };

    ActionRunnerDialog.prototype.SetAborted = function(info) {
        this.progressBar.SetAnimated(false);
        this.progressBar.SetError(true);
        this.SetStatus("USER ABORTED")
        this.errorPanel.Show();
        this.errorPanel.SetContent(info);
    };

    ActionRunnerDialog.prototype.SetFailed = function(reason) {
        this.progressBar.SetAnimated(false);
        this.progressBar.SetError(true);
        this.SetStatus("FAILED");
        if(!reason || '' === reason) {
            reson = 'UNDOCUMENTED INTERNAL ERROR';
        }
        this.errorPanel.Show();
        this.errorPanel.SetContent(reason);
    };

    // ActionRunnerDialog.prototype.GetMainPanel = function() {
    //     return this.panel;
    // };

    function OpenDefaultActionsDialog(app,action) {
        //create a new actions dialog without creating the DOM
        var dialog = new ActionDialog({
            style: ['jsa-modal','actions-dialog'],
            name: action.name,
            action: action,         
        },false);
        //replace the buttons
        dialog.buttons = {
            cancel: {
                name: 'Cancel',
                startEnabled: true,
                data: dialog,
                onClickCallback: function(event) {
                    this.data.Dissolve(); //Destroy the dialog
                }
            },
            run: {
                name: 'Run',
                startEnabled: true,
                data: dialog,
                onClickCallback: function(event) {
                    //save user values for the action
                    dialog.PreserveUserValues(app);
                    //call the action
                    let args = dialog.GetArgValues();
                    let domain = app.domain;
                    RunActionInRunnerDialog(app,domain,action,args)
                    this.data.Dissolve();
                }
            }
        };
        dialog.CreateDom();
        //if the same action was called before, restore the values.
        dialog.RestoreUserValues(app);
        //show the dialog
        app.AddChild(dialog);

        return dialog;
    }

    function RunActionInRunnerDialog(app,domain,action,args) {
        //create a new actions dialog without creating the DOM
        let serializer = new eoq2.serialization.TextSerializer();
        let dialog = new ActionRunnerDialog({
            style: ['jsa-modal','actions-dialog'],
            name: action.name,
            action: action
        },false);
        //create a runner with control on the dialog
        var actionRunner = new ACTIONS.ActionRunner({
            domain : domain,
            actionName : action.id,
            args : args,
            onRunCallback : function(info) {
                dialog.SetRun(info)
            },
            onFailedCallback : function(info) {
                dialog.SetFailed(info)
                dialog.EnableButton('close');
                dialog.DisableButton('cancel');
            },
            onStatusUpdateCallback : function(statusInfo) {
                dialog.SetOutput(statusInfo.output);
                dialog.SetProgress(statusInfo.progress);
                dialog.SetStatus(statusInfo.callStatusStr);
            },
            onFinishedCallback : function(info) {
                dialog.SetFinished(info);
                dialog.EnableButton('close');
                dialog.DisableButton('cancel');
            },
            onAbortedCallback : function(info) {
                dialog.SetAborted(info);
                dialog.EnableButton('close');
                dialog.DisableButton('cancel');
            },
            onResultCallback : function(res) {
                if(null!=res) { //do not show null results, that looks weired
                    let resStr = "";
                    try {
                        resStr = serializer.Ser(res);
                    } catch(e) {
                        resStr = "ERROR: Parsing results failed: "+e.toString();
                    }
                dialog.SetResult(resStr);
                }
            }
        })

        //bind the dialog to the runner
        //replace the dialog buttons
        dialog.buttons = {
            cancel: {
                name: 'Cancel',
                startEnabled: true,
                data: dialog,
                onClickCallback: function(event) {
                    actionRunner.Abort();
                }
            },
            close: {
                name: 'Close',
                startEnabled: false,
                data: dialog,
                onClickCallback: function(event) {
                    this.data.Dissolve(); 
                }
            }
        };
        //create and show the dialog
        dialog.CreateDom();
        app.AddChild(dialog);

        actionRunner.Run();
    };


    return {
        ActionParameterControl : ActionParameterControl,
        ActionDialog : ActionDialog,
        ActionRunnerDialog : ActionRunnerDialog,
        OpenDefaultActionsDialog : OpenDefaultActionsDialog,
        RunActionInRunnerDialog : RunActionInRunnerDialog
    }
})());