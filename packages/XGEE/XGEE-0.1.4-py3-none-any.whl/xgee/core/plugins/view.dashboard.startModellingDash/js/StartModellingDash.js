var START_MODELING_DASH = START_MODELING_DASH || {};





Object.assign(START_MODELING_DASH,(function(){
    function StartModelingDash(params,createDom=true) {
        jsa.Dash.call(this,params,false);
        let self = this;
        //members
        this.name = 'Start Modeling';
        this.modelSuffix = '.oaam';
        this.existingSectionLabel = 'Open existing model';
        this.createNewSectionLabel = 'Create new model';
        this.createTemplate = null;
        this.preferredEditors = []; //String list of the name ot the editors to be opened first in descending order.
        this.domain = null;
        this.legacyDomain = null;
        this.ecoreSync = null;
        this.eventBroker = null;
        this.newModelName = 'newModel';
        this.newSubdirName = 'newSubdir';
        this.rootQry = QRY.Obj(0);
        //this.application = null//hack, because app is not propergated properly
        
        //copy parameters
        jsa.CopyParams(this,params);


        this.rootObject = null; //the root of the dash
        this.rootContainer = null;

        //ecoreSync observers
        this.subdirObserverToken=null
        this.resourceObserverToken=null

        //Create DOM
        if(createDom) {
            this.CreateDom(); //prevent calling the wrong CreateDOM function if inheriting this class
        }
        
        //add the dynamic content

        this.UpdateRootObject().then(async function(res) {
            await self.InitElements();
            self.ListenToRootChanges(self.rootObject)
        });
    };

    StartModelingDash.prototype = Object.create(jsa.Dash.prototype);

    StartModelingDash.prototype.CreateDom = function() {
        jsa.Dash.prototype.CreateDom.call(this);

        //create static entries
        //EXISTING SECTION
        this.existingSection = new jsa.CustomFlatContainer({
            style: ['start-modeling-dash-existing-section']
        });
        this.AddChild(this.existingSection);


        this.existingSectionHeader = new jsa.CustomUiElement({
            elementType: 'h6',
            content: this.existingSectionLabel,
            // style: ['card-subtitle','mb-2','text-muted']
        });
        this.existingSection.AddChild(this.existingSectionHeader);

        //build new sections
        this.existingSectionDirs = new jsa.CustomFlatContainer({
            elementType : 'ul',
            style: ['start-modeling-dash-existing-section-dirs']
        });
        this.existingSection.AddChild(this.existingSectionDirs);

        this.existingSectionModels = new jsa.CustomFlatContainer({
            elementType : 'ul',
            style: ['start-modeling-dash-existing-section-models']
        });
        this.existingSection.AddChild(this.existingSectionModels);

        //CREATE NEW SECTION
        this.createNewSection = new jsa.CustomFlatContainer({
            style: ['start-modeling-dash-create-new-section']
        });
        this.AddChild(this.createNewSection);

        this.createNewSectionHeader = new jsa.CustomUiElement({
            elementType: 'h6',
            content: this.createNewSectionLabel,
            // style: ['card-subtitle','mb-2','text-muted']
        });
        this.createNewSection.AddChild(this.createNewSectionHeader);
        
        this.newElementsSection = new jsa.CustomFlatContainer({
            elementType : 'ul',
            style: ['start-modeling-dash-existing-new-elements']
        });
        this.AddChild(this.newElementsSection);

        let addModelEntry = new START_MODELING_DASH.StartModelingDashListEntry({
            style: ['start-modeling-dash-entry','start-modeling-dash-new-model-entry'],
            name : "Create new model",
            ecoreSync : this.ecoreSync,
            data : {
                dash : this
            },
            onLinkClickedCallback : function(event) {
                this.data.dash.CreateNewModel();
            },
            canEdit : false
        });
        this.newElementsSection.AddChild(addModelEntry);

        let addSubdirEntry = new START_MODELING_DASH.StartModelingDashListEntry({
            style: ['start-modeling-dash-entry','start-modeling-dash-new-subdir-entry'],
            name : "Create new sub directory",
            ecoreSync : this.ecoreSync,
            data : {
                dash : this
            },
            onLinkClickedCallback : function(event) {
                this.data.dash.CreateNewSubdir();
            },
            canEdit : false
        });
        this.newElementsSection.AddChild(addSubdirEntry);
    };

    StartModelingDash.prototype.OpenExistingModel = function(model) {
        alert(model.name);

        return this;
    };

    StartModelingDash.prototype.getExistingSubdirNames=async function()
    {
        let rid=this.ecoreSync.rlookup(this.rootObject);
        let names=await this.ecoreSync.exec(CMD.Get(QRY.Obj(rid).Pth('subdirectories').Pth('name')))        
        return names
    } 

    StartModelingDash.prototype.getExistingModelNames=async function(){
        let self=this
        let rid=this.ecoreSync.rlookup(this.rootObject);
        let names=await this.ecoreSync.exec(CMD.Get(QRY.Obj(rid).Pth('resources').Pth('name')))               
        return names.filter(name => name.endsWith(self.modelSuffix))
    } 

    StartModelingDash.prototype.GenerateNewFreeName = function(prefix, suffix, existingNames) {
        let name = prefix + suffix;;
        let i = 0;
        while(existingNames.includes(name)) {
            name = prefix + i + suffix;
            i++;
        } 
        return name;
    };

    StartModelingDash.prototype.CreateNewSubdir = async function() {
        
        let newName = this.GenerateNewFreeName(this.newSubdirName,'',await this.getExistingSubdirNames());
        let rid = this.ecoreSync.rlookup(this.rootObject);// the id of the target directory

        let cmd = new eoq2.Cmp();

        cmd.Crn("http://www.eoq.de/workspacemdbmodel/v1.0","Directory",1)
            .Set(new eoq2.Qry().His(-1),"name",newName)
            .Add(new eoq2.Qry().Obj(rid),"subdirectories",new eoq2.Qry().His(-2));

        var self = this;
        try{
            await this.ecoreSync.exec(cmd,true)
            self.app.Note('Created new '+newName+'.','success');
        }
        catch(e)
        {
            self.app.Note('Failed to create '+newName+': '+e.toString(),'error');
        }    
        
        return this;
    };

    StartModelingDash.prototype.CreateNewModel = async function() {
        
        let newName = this.GenerateNewFreeName(this.newModelName,this.modelSuffix,await this.getExistingModelNames());
        let rid = this.ecoreSync.rlookup(this.rootObject)// the id of the target directory

        let cmd = new eoq2.Cmp();

        if(this.createTemplate) {
            //decompose the path 
            let pathSegments = this.createTemplate.split('/');
            let templateDirectories = [];
            for(var i=0;i<pathSegments.length-1;i++) {
                templateDirectories.push(pathSegments[i]);
            }
            let templateName = pathSegments[pathSegments.length-1];
            //build a mathich query for the template
            let retrieveTemplateQry = new eoq2.Qry();
            for(let i=0;i<templateDirectories.length;i++) {
                retrieveTemplateQry.Pth("subdirectories").Sel(new eoq2.Qry().Pth("name").Equ(templateDirectories[i])).Idx(0);
            }
            retrieveTemplateQry.Pth("resources").Sel(new eoq2.Qry().Pth("name").Equ(templateName)).Idx(0);

            cmd.Get(retrieveTemplateQry)
                .Get(new eoq2.Qry().His(-1).Pth("contents").Idx(0))
                .Clo(new eoq2.Qry().His(-1),eoq2.CloModes.FUL)
                .Crn("http://www.eoq.de/workspacemdbmodel/v1.0","ModelResource",1)
                .Set(new eoq2.Qry().His(-1),"name",newName)
                .Add(new eoq2.Qry().His(-2),"contents",new eoq2.Qry().His(-3))
                .Add(new eoq2.Qry().Obj(rid),"resources",new eoq2.Qry().His(-3));

        } else { 
            cmd.Crn("http://www.eoq.de/workspacemdbmodel/v1.0","ModelResource",1)
                .Set(new eoq2.Qry().His(-1),"name",newName)
                .Add(new eoq2.Qry().Obj(rid),"resources",new eoq2.Qry().His(-2));
        }

        
        var self = this;
        try{
            await this.ecoreSync.exec(cmd)
            if(self.createTemplate) {
                self.app.Note('Created '+newName+' from '+self.createTemplate+'.','success');
            } else {
                self.app.Note('Created new '+newName+'.','success');
            }
        }
        catch(e){
            self.app.Note('Failed to create '+newName+': '+e.toString(),'error');
        }
        
        return this;
    };


    StartModelingDash.prototype.OpenEditorsForResource = function(resourceId,resourceName) {

        var xgee=this.app.plugins.require('editor');

        let editableClasses = xgee.listClassNames();

        //let cmdStrs = ["CALL 'load-resource' [#"+resourceId+"]"];//make sure the resource is opened before checking for editable objects
        let cmdStrs = [];
        let nEditableClasses = editableClasses.length;
        for(let i=0;i<nEditableClasses;i++) {
            let className = editableClasses[i];
            cmdStrs.push('RETRIEVE #'+resourceId+' $'+className);
        }

        let cmdStr = cmdStrs.join('\n');

        let cmd = jseoq.CommandParser.StringToCommand(cmdStr);
        let self = this;
        this.legacyDomain.DoSync(cmd).then(function(result) {
            if(jseoq.ResultParser.IsResultOk(result)) {
                let objectsToBeOpened = [];
                for(let i=0;i<nEditableClasses;i++) {
                    let nObjectsOfClass = result.results[i].value.v.length; //+1 because the first result is that of the load-resource command
                    for(let j=0;j<nObjectsOfClass;j++) { 
                        objectsToBeOpened.push({
                            id : result.results[i].value.v[j].v, //+1 because the first result is that of the load-resource command
                            className : editableClasses[i]
                        });
                    }
                }
                let nObjectsToBeOpened = objectsToBeOpened.length;
                let summary = [];
                for(let i=0;i<nObjectsToBeOpened;i++) {
                    var objectToBeOpened = objectsToBeOpened[i];
                    summary.push(objectToBeOpened.className+': #'+objectToBeOpened.id);
                }

                if(0==nObjectsToBeOpened) {
                    self.app.AddChild(new jsa.MsgBox({
                        name: 'Warning',
                        content: 'No specialized Editor found for the elements of '+resourceName+'.'
                    }));
                } else { 
                    //Wait for all editors to be open and then switch to the first one
                    //SerialPromise is a workaround here to avoid collisions in getObjectById/resolveContainment, rework should be done there too
                    serialPromise(objectsToBeOpened,function(objectToBeOpened){
                        return new Promise(function(resolve,reject){
                            let id = objectToBeOpened.id;
                            self.ecoreSync.getObject(id).then(function(eObject){
                                //self.ecoreSync.resolveContainment(eObject).then(function(){
                                    //self.ecoreSync.isClassInitialized(eObject.eClass).then(function(unused) {                          
                                     
                                        let newGraphView = xgee.open(eObject,false);                                                                  
                                                                                                                              
                                        
                                        resolve(newGraphView);
                                    //});
//});
                            });
                        });
                    }).then(function(views) {
                        //Find the editor to open first 
                        let preferredView = null;
                        for(let i=0;i<self.preferredEditors.length;i++) {
                            let preferredEditorName = self.preferredEditors[i];
                            for(let j=0;j<views.length;j++) {
                                let view = views[j];
                                if(view.name.includes(preferredEditorName)) {
                                    preferredView = view;
                                    break;
                                }
                            }
                            if(preferredView) {
                                break; //exit the outerloop
                            }
                        }
                        if(preferredView) {
                            self.app.viewManager.ActivateView(preferredView);
                            //self.app.commandManager.Execute(new jsa.ChangeViewCommand(self.app.viewManager,preferredView));
                        } else {//Open the first of all views      
                            self.app.viewManager.ActivateView(views[0]);          
                            //self.app.commandManager.Execute(new jsa.ChangeViewCommand(self.app.viewManager,views[0]));
                        }
                    });
                }

            } else {
                self.app.AddChild(new jsa.MsgBox({
                    name: 'Error Opening',
                    content: 'Failed to open '+resourceName+': '+jseoq.ResultParser.GetErrorString(result)
                }));
            }
        });

        return this;
    }

    StartModelingDash.prototype.UpdateRootObject = async function() {
 
        let self = this;
  
        let rootObject= await self.ecoreSync.exec(CMD.Get(self.rootQry))              
        let rid = self.ecoreSync.rlookup(rootObject);
        self.SetNewModelRoot(rootObject);            

        let rootContainer=await self.ecoreSync.exec(CMD.Get(QRY.Obj(rid).Met("PARENT")))       
        self.rootContainer = rootContainer?rootContainer:null;                  
        return true 
      
    };

    StartModelingDash.prototype.ListenToRootChanges = async function(rootObject) {        
        let rid = this.ecoreSync.rlookup(rootObject)        
        this.subdirObserverToken=await this.ecoreSync.observe(new eoq2.Obj(rid).Pth('subdirectories'),this.OnSubdirChange.bind(this))
        this.resourceObserverToken=await this.ecoreSync.observe(new eoq2.Obj(rid).Pth('resources'),this.OnModelChange.bind(this))
    }

    StartModelingDash.prototype.StopListenToRootChanges = function() {
        if(this.subdirObserverToken) this.ecoreSync.unobserve(this.subdirObserverToken)
        this.subdirObserverToken=null
        if(this.resourceObserverToken) this.ecoreSync.unobserve(this.resourceObserverToken)
        this.resourceObserverToken=null
    }

    StartModelingDash.prototype.SetNewModelRoot = function(newModelRoot) {
        if(this.rootObject) {
            this.StopListenToRootChanges();
        }
        this.rootObject = newModelRoot;
    }

    StartModelingDash.prototype.OpenSubdir = function(eObject) {
        this.SetNewModelRoot(eObject);
        let self = this;
        let rid = this.ecoreSync.rlookup(this.rootObject)
        self.ecoreSync.exec(CMD.Get(QRY.Obj(rid).Met("PARENT"))).then(async function(rootContainer) {
                self.rootContainer = rootContainer
                await self.InitElements()
                self.ListenToRootChanges(self.rootObject)            
        });        
    };


    StartModelingDash.prototype.InitSubdirsList = async function() {

        let self = this;

        //get all existing children and dissolve them
        let entries = this.existingSectionDirs.children;  
        entries.forEach(entry => entry.Dissolve())       


        //retrieve subdir list and names
        let rid=this.ecoreSync.rlookup(this.rootObject);
        var cmd=CMD.Cmp();
        cmd.Get(QRY.Obj(rid).Pth('name'))
        cmd.Get(QRY.Obj(rid).Pth('subdirectories'))
        cmd.Get(QRY.His(-1).Trm().Pth('name'))
        var res=await this.ecoreSync.exec(cmd);

        //add parent folder
        if(self.rootContainer) {    
            let name=res[0];
            let entry = new START_MODELING_DASH.StartModelingDashListEntry({
                style: ['start-modeling-dash-entry','start-modeling-dash-parent-entry'],
                name : name,
                eObject : self.rootObject,
                ecoreSync : self.ecoreSync,
                eventBroker : self.eventBroker,
                data : {
                    dash : self,
                    eObject : self.rootContainer
                },
                onLinkClickedCallback : function(event) {
                    console.error(self.rootContainer)
                    this.data.dash.OpenSubdir(this.data.eObject);
                },
                canEdit : false
            });
            self.existingSectionDirs.AddChildAtIndex(entry,0);       
        }


        //add all regular directories
        for(let i=0;i<res[1].length;i++) {
            let subdir = res[1][i];
            let name = res[2][i]   
            if(!name.startsWith('.')) {
                let entry = new START_MODELING_DASH.StartModelingDashListEntry({
                    style: ['start-modeling-dash-entry','start-modeling-dash-subdir-entry'],
                    name : name,
                    eObject : subdir,
                    ecoreSync : self.ecoreSync,
                    eventBroker : self.eventBroker,
                    data : {
                        dash : self,
                        eObject : subdir
                    },
                    onLinkClickedCallback : function(event) {
                        this.data.dash.OpenSubdir(this.data.eObject);
                    },
                    canDelete : true,
                    eContainer : self.rootObject,
                    featureName : 'subdirectories',
                });
                self.existingSectionDirs.AddChild(entry)
            }         
        }     
        
    };

    StartModelingDash.prototype.InitModelsList = async function() {
        
        let self = this;     

        let entries = this.existingSectionModels.children;
        entries.forEach(entry => entry.Dissolve())     

        //get current entries
        let rid=this.ecoreSync.rlookup(this.rootObject);
        var cmd=CMD.Cmp();
        cmd.Get(QRY.Obj(rid).Pth('resources'))
        cmd.Get(QRY.His(-1).Trm().Pth('name'))
        var res=await this.ecoreSync.exec(cmd);
        for(let i=0;i<res[0].length;i++) {
                let model = res[0][i];
                let name = res[1][i];
                if(name.endsWith(self.modelSuffix)) { //only show elements corresponding to the current suffix
                    let entry = new START_MODELING_DASH.StartModelingDashListEntry({
                        style: ['start-modeling-dash-entry','start-modeling-dash-model-entry'],
                        name : name,
                        eObject : model,
                        ecoreSync : self.ecoreSync,
                        eventBroker : self.eventBroker,
                        data : self,
                        onLinkClickedCallback : function(event) {
                            let oid = self.ecoreSync.rlookup(this.eObject);
                            let modelName = this.eObject.get('name');
                            this.data.OpenEditorsForResource(oid, modelName);
                        },
                        canDelete : true,
                        eContainer : self.rootObject,
                        featureName : 'resources',
                    });                    
                    self.existingSectionModels.AddChild(entry);     
       
                }                
        }


    };

    StartModelingDash.prototype.InitElements = async function() {
        await Promise.all([this.InitSubdirsList(), this.InitModelsList()]);       
    };

    StartModelingDash.prototype.OnSubdirChange = async function(results,addedSubdirs,removedSubdirs){
       
        let self=this
        let entries = this.existingSectionDirs.children;

        removedSubdirs.forEach(function(eObject){
            let entry=entries.find(entry => { return entry.eObject==eObject})
            entry.Dissolve()
        })

        let addedSubdirsNames=await Promise.all(addedSubdirs.map((dir)=>{ return self.ecoreSync.get(dir,'name') }))

        addedSubdirs.filter(subdir =>  subdir.get('name')?(!subdir.get('name').startsWith('.')):false).forEach(function(subdir,idx){
            let entry=entries.find(entry => { return entry.eObject==subdir})
            if(!entry)
            {
                entry = new START_MODELING_DASH.StartModelingDashListEntry({
                    style: ['start-modeling-dash-entry','start-modeling-dash-subdir-entry'],
                    name : addedSubdirsNames[idx],
                    eObject : subdir,
                    ecoreSync : self.ecoreSync,
                    eventBroker : self.eventBroker,
                    data : {
                        dash : self,
                        eObject : subdir
                    },
                    onLinkClickedCallback : function(event) {
                        this.data.dash.OpenSubdir(this.data.eObject);
                    },
                    canDelete : true,
                    eContainer : self.rootObject,
                    featureName : 'subdirectories',
                });                
                self.existingSectionDirs.AddChild(entry)
            }            
        })

    };

    StartModelingDash.prototype.OnModelChange = async function(results,addedModels,removedModels) {
        let self=this
        let entries = this.existingSectionModels.children;

        removedModels.forEach(function(eObject){
            let entry=entries.find(entry => { return entry.eObject==eObject})
            entry.Dissolve()
        })

        let addedModelsNames=await Promise.all(addedModels.map((dir)=>{ return self.ecoreSync.get(dir,'name') }))

        addedModels.filter(model => model.get('name')?model.get('name').endsWith(self.modelSuffix):false).forEach(function(model,idx){            
            let entry=entries.find(entry => { return entry.eObject==model})
            if(!entry)
            {
                entry = new START_MODELING_DASH.StartModelingDashListEntry({
                    style: ['start-modeling-dash-entry','start-modeling-dash-model-entry'],
                    name : addedModelsNames[idx],
                    eObject : model,
                    ecoreSync : self.ecoreSync,
                    eventBroker : self.eventBroker,
                    data : self,
                    onLinkClickedCallback : function(event) {
                        let oid = self.ecoreSync.rlookup(this.eObject);
                        let modelName = this.eObject.get('name');
                        this.data.OpenEditorsForResource(oid, modelName);
                    },
                    canDelete : true,
                    eContainer : self.rootObject,
                    featureName : 'resources',
                });                 
                self.existingSectionModels.AddChild(entry)
            }            
        })

        this.existingModels =  entries.map( entry => { if(!entry.isDissolved) { return entry.name }else{return null} }).filter(entry => { return entry!=null});
    };

    //@Override
    StartModelingDash.prototype.Dissolve = function() {
        if(this.rootObject) {
            this.StopListenToRootChanges(this.rootObject);
        }
        jsa.Dash.prototype.Dissolve.call(this);
    };

    return {
        StartModelingDash : StartModelingDash
    };
    
})());