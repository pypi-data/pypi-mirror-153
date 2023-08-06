// Workspace Provider
// Enables support for workspaces on the remote server 
// (C) 2019 Matthias Brunner

var WorkspaceProvider=function(ecoreSync)
{
    var self=this;
    this.ecoreSync=ecoreSync;
    this.name="workspace";


    this.delay=function(until=100)
    {
        return new Promise(function(resolve,reject)
        {
            setTimeout(resolve,until);
        });
    };

    var Resource=function(workspace,objectId)
    {
        //API to access resources

        var self=this;
        this.workspace=workspace;
        this.objectId=objectId; //the resource object Id (workspace model)
        this.rootObjectId=objectId; //the root object Id (resource)
        this.name="";
        this.isResource=true;
        this.isWorkspaceObject=true;
        this.isLoaded=false;
        this.isDirty=false;
        this.eObject=null; //the resource eObject (workspace model)
        this.rootObject=null; // the root object of the resource (resource)
        this.__listeners=[];
        this.__update=new rateLimitedFunctionCall(function(){self.fireOnUpdate();},10); 
        this.isInitialized=function()
        {
            //A resource is initialized (!=loaded) if its name and its EObject (not the root object) is present
            return new Promise(function(resolve,reject)
            { 
                self.getEObject().then(function(){
                    self.getName().then(function(){ resolve(); });
                });
            });
        }
        this.getEObject=function()
        {
            //Gets the resources EObject
            var setupListeners=function(eObject)
            {
                eObject.on('change',function(change){
                    self.update();
                });
            };
            return new Promise(function(resolve,reject){
                self.workspace.ecoreSync.getObjectById(self.objectId).then(function(eObject){      
                    self.eObject=ecoreSync.getProxiedObject(eObject);
                    setupListeners(eObject.noproxy);
                    resolve(self.eObject);
                });
            });
        };
        this.getName=function()
        {
            //Gets the resource's file name

            return new Promise(function(resolve,reject)
            {               
                self.workspace.ecoreSync.isAttributeInitialized(self.eObject,"name").then(function(){resolve();});                
            });
        };
        this.update=function()
        {
            //Updates the resources state variables
            self.isDirty=self.eObject.get("isDirty");
            self.name=self.eObject.get("name");     
            self.fireOnUpdate();      
        };      
        this.getRootObject=function()
        {
            //This function gets the resource's root object, the actual model root. If the root object is requested,
            //the resource is also loaded on the remote server. 
            //Note: This resource object also contains another eObject (see getEObject()) referring to its workspace model object.
            return new Promise(function(resolve,reject){
                if(!self.isLoaded)
                {                
                    self.load().then(function(){               
                        resolve(self.rootObject);
                    });                
                }
                else
                {
                    resolve(self.rootObject);
                }        
            });    
        };         
        this.load=function()
        {
            //Loads the resource on the remote server and stores the root object (and id) in the workspace model
            return new Promise(function(resolve,reject){
                if(!self.isLoaded)
                {
                    self.workspace.ecoreSync.loadResource(self.objectId,function(rootObjectId){
                        self.isLoaded=true;
                        self.rootObjectId=rootObjectId;
                        self.rootObject=ecoreSync.getProxiedObject(self.workspace.ecoreSync.index.getById(rootObjectId));   
                        self.workspace.ecoreSync.isClassInitialized(self.rootObject.eClass).then(resolve());                      
                    });        
                }
                else
                {
                    resolve();
                }
            });
        };
        this.save=function()
        {
            //Saves the resource on the remote server
            if(self.isLoaded)
            {
                let query="CALL 'save-resource' [#"+objectId+"]";
                let onSuccess=function(){$app.notesManager.PutNote("Saved.","success");};
                let onFailure=function(){$app.notesManager.PutNote("Saving failed.","error");};
                self.workspace.ecoreSync.domain.DoFromStr(query,onSuccess,onFailure);
            }
        }
        this.onUpdate=function(cb)
        {
            //Registers a callback function (cb) to fire in the case of an update (onUpdate event)
            if(self.__listeners.indexOf(cb)==-1)
            {
                self.__listeners.push(cb);
            }
        };
        this.fireOnUpdate=function()
        {
            //fires the onUpdate event
            for(let i in self.__listeners)
            {
                setTimeout(self.__listeners[i],1);
            }
        } 
    };

    var Directory=function(workspace,objectId,isRoot=false,name="")
    {
        var self=this;
        this.workspace=workspace;
        this.objectId=objectId;
        this.eObject=null;
        this.__eObjectListeners=false;
        this.name=name;
        this.resources=[];
        this.directories=[];
        this.metamodels=[];
        this.isRoot=isRoot;
        this.isDirectory=true;
        this.isWorkspaceObject=true;
        this.__listeners=[];       
        this.__initialized=false;
        this.pendingUpdate=Promise.resolve();        
        this.__update=new rateLimitedFunctionCall(function(){  self.pendingUpdate.then(function(){self.updateContents().then(self.fireOnUpdate);});  },10); 
        this.update=function(){ self.__update.runRateLimited();};
        this.getEObject=function()
        {
            console.trace();
            var setupListeners=function()
            {
                return new Promise(function(resolve,reject){
                

                //Sets up eObject listeners to react to object changes

                if(!self.__eObjectListeners)
                {
                    //Listen to properties changes
                    self.eObject.noproxy.on('change',function(change)
                    {                      
                        self.update();                                            
                    });    

                    //Listen to references add/remove
                    let observedFeatures=[];
                    if(self.isRoot)
                    {
                        observedFeatures=['subdirectories','resources'/*,'metamodels'*/];
                    }
                    else
                    {
                        observedFeatures=['subdirectories','resources'];
                    }
                    for(let i in observedFeatures)
                    {
                        self.eObject.noproxy.on('add:'+observedFeatures[i],function(change)
                        {                             
                           self.update();                                            
                        });    
                        self.eObject.noproxy.on('remove:'+observedFeatures[i],function(change)
                        {                                  
                           self.update();                                                     
                        });    
                        self.eObject.get(observedFeatures[i]);
                    }
                    self.__eObjectListeners=true;
                }
                   
                    resolve();                 
                });               
            };

            return new Promise(function(resolve,reject){
                self.workspace.ecoreSync.getObjectById(self.objectId).then(function(eObject){      
                    self.eObject=self.workspace.ecoreSync.getProxiedObject(eObject);
                    self.workspace.ecoreSync.isClassInitialized(self.eObject.eClass).then(
                        function(){
                            setupListeners().then(resolve(self.eObject));  
                            resolve();
                        }  
                    );               
                });
            });
        };
        this.__addResource=function(id)
        {
            let resource=self.resources.find(function(e){return e.objectId==id;});
            if(!resource)
            {
                resource=new Resource(self.workspace,id); 
                let resourceInitialized=resource.isInitialized();   
                resourceInitialized.then(function(){  
                    self.resources.push(resource);                    
                });
                return resourceInitialized;
            }       
            else
            {
                return Promise.resolve();
            } 
        };

        this.__addDirectory=function(id)
        {
            let dir=self.directories.find(function(e){return e.objectId==id;});
            if(!dir)
            {
                dir=new Directory(self.workspace,id);            
                let dirInitialized=dir.isInitialized()
                dirInitialized.then(function()
                {                   
                    self.directories.push(dir);
                }
                );   
                return dirInitialized;            
            }  
            else
            {
                return Promise.resolve();
            }       
        };
        this.__addMetamodel=function(id)
        {
            let metamodel=self.metamodels.find(function(e){return e.objectId==id;});
            if(!metamodel)
            {
                metamodel=new Metamodel(self.workspace,id);        
                self.metamodels.push(metamodel);
            }   
            return Promise.resolve();     
        }

        this.updateContents=function()
        {
 
            var contentUpdate=function()
            {
                return new Promise(
                function(resolve,reject)
                {                                              
                    
                    var featuresInitialized=[];          
                    featuresInitialized.push(self.workspace.ecoreSync.isReferenceInitialized(self.eObject,"subdirectories"));
                    featuresInitialized.push(self.workspace.ecoreSync.isReferenceInitialized(self.eObject,"resources"));
                    if(self.isRoot)
                    {
                        //featuresInitialized.push(self.workspace.ecoreSync.isReferenceInitialized(self.eObject,"metamodels"));
                    }
                    else
                    {
                        featuresInitialized.push(self.workspace.ecoreSync.isAttributeInitialized(self.eObject,"name"));
                    }

                    Promise.all(featuresInitialized).then(function(){
                
                        var objectsInitialized=[];                

                        //update the workspace
                        let dirs=self.eObject.get("subdirectories").array();
                        for(let i in dirs)
                        {
                            objectsInitialized.push(self.__addDirectory(dirs[i].get("_#EOQ")));
                        }                        
                        let resources=self.eObject.get("resources").array();
                        for(let i in resources)
                        {
                            objectsInitialized.push(self.__addResource(resources[i].get("_#EOQ")));
                        }
                        if(self.isRoot)
                        {
                            //only the root directory provides meta models
                            // let metas=self.eObject.get("metamodels").array();
                            // for(let i in metas)
                            // {
                            //     objectsInitialized.push(self.__addMetamodel(metas[i].get("_#EOQ")));
                            // }
                            //$.notify("metas "+metas.length);
                        }
                        else
                        {
                            self.name=self.eObject.get("name");                              
                        }                      

                        Promise.all(objectsInitialized).then(function(){                                        
                            self.__initialized=true;                                                   
                            resolve();                                    
                        }); 

                    });
                });
            };            

            return new Promise(function(resolve,reject){                
                self.pendingUpdate=new Promise(function(updateComplete,updateFailed){
                             contentUpdate().then(function(){  updateComplete();  }).catch(function(reason){ alert(' An error occured: '+reason); console.trace(); })
                });
                self.pendingUpdate.then(function(){ self.fireOnUpdate(); resolve()});
            });       
        };

        this.getContents=function()
        {
            let contents=[];
            contents=contents.concat(self.directories);
            contents=contents.concat(self.resources);
            //contents=contents.concat(self.metamodels);
            return contents;
        };
        this.onUpdate=function(cb,remove=false)
        {
            if(!remove)
            {
                if(self.__listeners.indexOf(cb)==-1)
                {
                    self.__listeners.push(cb);
                }
            }
            else
            {
                let rcb=self.__listeners.find(function(e){ return e==cb; });
                if(rcb)
                {
                    self.__listeners.splice(self.__listeners.indexOf(rcb),1);
                }
            }
        };
        this.fireOnUpdate=function()
        {
            for(let i in self.__listeners)
            {
                setTimeout(self.__listeners[i],1);
            }
        };        
        this.isInitialized=function(){

             //A directory is initialized if all subordinate objects and its name and eObject are initialized

            return new Promise(function(resolve,reject){
            console.warn("Directory initializing "+self.name);
                self.getEObject()
                .then(function(eObject){                 
                  return self.updateContents();
                })
                .then(function(){
                    resolve();
                });               
            });
        };

    };

    //setup workspace directory
    this.workspaceDirectory=new Directory(this,0,true,"Workspace");
 
    var Metamodel=function(workspace,objectId)
    {
        var self=this;
        this.workspace=workspace;
        this.objectId=objectId;
        this.name="";
        this.isMetamodel=true;
        this.isWorkspaceObject=true;
    };

    var ModelObject=function(workspace,eObject,featureObj=null)
    {
        var self=this;
        this.__listeners=[];
        this.workspace=workspace;
        this.eObject=eObject;
        this.featureObj = featureObj
        this.feature=featureObj?featureObj.get('name'):null;
        this.isModelObject=true;
        this.isWorkspaceObject=true;
        this.__update=new rateLimitedFunctionCall(function(){self.fireOnUpdate();},10); 
        this.onUpdate=function(cb)
        {
            if(self.__listeners.indexOf(cb)==-1)
            {
                self.__listeners.push(cb);
            }
        };
        this.fireOnUpdate=function()
        { 
            for(let i in self.__listeners)
            {
                setTimeout(self.__listeners[i],1);
            }
        }        
        if(eObject)
        {
            if(self.feature==null)
            {
                self.eObject.noproxy.on('change',function(change)
                {
                    self.__update.runRateLimited();                      
                });    
            }
            else
            {
                //BA: changed
                //let featureName = self.feature.get('name');
                if(self.featureObj.get('upperBound')==1) {
                    self.eObject.noproxy.on('change:'+self.feature,function(change)
                    {               
                        self.__update.runRateLimited();                          
                    }); 
                } else { 
                    self.eObject.noproxy.on('add:'+self.feature,function(change)
                    {               
                        self.__update.runRateLimited();                          
                    });    
                    self.eObject.noproxy.on('remove:'+self.feature,function(change)
                    {
                        self.__update.runRateLimited();                           
                    });    
                }
            }
        }
    };

 
    this.getType=function(object)
    {    
        if(object)
        {
            if(object==self)
            {
                return "WORKSPACE";
            }  

            if(object.hasOwnProperty("isWorkspaceObject"))
            {
                if(object.isResource)
                {
                    return "RESOURCE";
                }
                if(object.isDirectory)
                {
                    return "DIRECTORY";
                }
                if(object.isMetamodel)
                {            
                    return "METAMODEL";
                }
                if(object.isModelObject)
                {       
                    return "MODELOBJECT";
                }
            }
        }    
    };

    this.createModelObject=function(eObject,feature)
    {
        var modelObject=new ModelObject(self,eObject,feature);
        return modelObject;
    }

    this.getContents=function()
    {
        return this.workspaceDirectory.getContents();
    }

    this.isInitialized=function()
    {      
        //Proxy for workspace directory initialization
        return self.workspaceDirectory.isInitialized();     
    }

    this.onUpdate=function(cb)
    {
        this.workspaceDirectory.onUpdate(cb); 
    }

}

