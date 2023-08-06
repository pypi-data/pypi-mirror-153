var START_MODELING_DASH = START_MODELING_DASH || {};

Object.assign(START_MODELING_DASH,(function(){
    function StartModelingDashListEntry(params,createDom=true) {
        jsa.CustomFlatContainer.call(this,params,false);

        //members
        this.elementType = 'li',
        this.style = ['start-modeling-dash-default-entry'],
        this.onMouseOverCallback = function(evt){this.OnMouseOver();},
        this.onMouseOutCallback = function(evt){this.OnMouseOut();}
        this.name = null;
        this.eObject = null;
        this.ecoreSync = null;
        this.eventBroker = null;
        this.onLinkClickedCallback = null;
        this.canEdit = true;
        this.canDelete = false;
        this.featureName = null; //important for delete
        this.eContainer = null; //necessary for delete
        //this.application = null//hack, because app is not propergated properly
        
        //copy parameters
        jsa.CopyParams(this,params);

        //internals
        this.link = null;
        this.editCtrl = null;
        this.deleteCtrl = null;
        this.isDissolved=false

        //Create DOM
        if(createDom) {
            this.CreateDom(); //prevent calling the wrong CreateDOM function if inheritating this class
        }
    };

    StartModelingDashListEntry.prototype = Object.create(jsa.CustomFlatContainer.prototype);

    StartModelingDashListEntry.prototype.CreateDom = function() {
        jsa.CustomFlatContainer.prototype.CreateDom.call(this);

        this.link = new jsa.CustomUiElement({
            elementType : 'a',
            content : this.name,
            href : '#',
            data : this,
            onClickCallback : function(event) {
                this.data.onLinkClickedCallback(event);
            }
        })
        
        this.AddChild(this.link);
        if(this.canEdit) {
            this.editCtrl = new jsa.CustomUiElement({
                elementType : 'span',
                style: ['start-modeling-dash-edit-icon'],
                data : {
                    eObject : this.eObject,
                    eventBroker : this.eventBroker
                },
                onClickCallback : function(event) {
                    if(this.data.eventBroker) {                  
                        this.data.eventBroker.publish("PROPERTIESVIEW/OPEN",{eObject:this.data.eObject,DOM:this.GetDomElement()});
                    }
                }

            });
            this.AddChild(this.editCtrl);
            this.editCtrl.Hide();
        }

        if(this.canDelete) {
            this.deleteCtrl = new jsa.CustomUiElement({
                elementType : 'span',
                style: ['start-modeling-dash-delete-icon'],
                data : this,
                onClickCallback : function(event) {
                    this.data.OnDeleteClicked(event);
                }

            });
            this.AddChild(this.deleteCtrl);
            this.deleteCtrl.Hide();
        }
        
        //listen to object name changes
        if(this.eObject) {
            this.eObject.on('change:name',this.OnNameChange,this);
        }
    };

    StartModelingDashListEntry.prototype.OnNameChange = function(change) {
        //remove change listener
        let newName = this.eObject.get('name');
        this.link.SetContent(newName);
    };

    StartModelingDashListEntry.prototype.OnDeleteClicked = function(event) {
        //remove change listener
        let name = this.eObject.get('name');
        this.dialog = new jsa.MsgBox({
            content : 'Do you really want to delete ' + name + '?',
            buttons : {
                yes: {
                  name: 'Yes',
                  startEnabled: true,
                  data: this,
                  onClickCallback: function(event) {
                    this.data.OnDeleteYes();
                  }
                },
                no: {
                    name: 'No',
                    startEnabled: true,
                    data: this,
                    onClickCallback: function(event) {
                        this.data.OnDeleteNo();
                    }
                }
            }
        });
        this.GetApp().AddChild(this.dialog);
    };

    StartModelingDashListEntry.prototype.OnDeleteYes = function() {
        this.GetApp().commandManager.Execute(new ERemoveCommand(this.ecoreSync,this.eContainer,this.featureName,this.eObject));
        this.dialog.Dissolve();
    };

    StartModelingDashListEntry.prototype.OnDeleteNo = function() {
        this.dialog.Dissolve();
    };

    StartModelingDashListEntry.prototype.OnMouseOver = function(event) {
        if(this.editCtrl) this.editCtrl.Show();
        if(this.deleteCtrl) this.deleteCtrl.Show();
    };

    StartModelingDashListEntry.prototype.OnMouseOut = function(event) {
        if(this.editCtrl) this.editCtrl.Hide();
        if(this.deleteCtrl) this.deleteCtrl.Hide();
    };

    StartModelingDashListEntry.prototype.Dissolve = function() {
        //remove change listener
        if(this.eObject) {
            this.eObject.off('change:name',this.OnNameChange,this);
        }
        jsa.CustomFlatContainer.prototype.Dissolve.call(this);
        this.isDissolved=true
    };


return {
    StartModelingDashListEntry : StartModelingDashListEntry
};

})());