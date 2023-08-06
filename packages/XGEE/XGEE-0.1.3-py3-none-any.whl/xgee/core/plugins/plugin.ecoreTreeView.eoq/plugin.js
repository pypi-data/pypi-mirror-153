export function init(pluginAPI) {  

    var WorkspaceView=function(iconPath)
    {
        var self=this;
        this.iconPath=iconPath;
        this.apply=function(data)
        {
            var view={};
            if(data.type=='eObject')
            {
                switch(data.value.eClass.get("name"))
                {
                    case 'Workspace':
                        view={title: 'Workspace', folder:true, eObject: data.value, modifiers:data.modifiers, lazy: true}; 
                        break;
                    case 'Directory':
                        view={title: data.value.get("name"), folder:true, eObject: data.value, modifiers:data.modifiers, lazy: true}; 
                        break;
                    case 'ModelResource':
                        view={title: data.value.get("name"), eObject: data.value, modifiers:data.modifiers, lazy: true}; 
                        break;
                }
            }       
            return view;
        };

        this.canDisplay=function(data)
        {
            if(data.type!='eObject')
            {
                return false;
            }
            else
            {
                var displayableClasses=[{name:'Workspace',nsURI:"http://www.eoq.de/workspacemdbmodel/v1.0"},{name:'Directory',nsURI:"http://www.eoq.de/workspacemdbmodel/v1.0"},{name:'ModelResource',nsURI:"http://www.eoq.de/workspacemdbmodel/v1.0"}];                
                if(data.value)
                {
                    if(displayableClasses.find(function(e){ return e.name==data.value.eClass.get("name") && e.nsURI==data.value.eClass.eContainer.get("nsURI")}))
                    {
                        return true;
                    }
                }
                else
                {
                    console.error(data)
                }

            }
        }
    }

    var WorkspaceController=function(ecoreSync)
    {
        var ecoreSync=ecoreSync;   
        var self=this;
        this.onUpdate=function(parentEObject,eObject,callbackFcn)
        {
            eObject.on('add:subdirectories',function(){
                self.load(parentEObject,eObject).then(function(loadedData){
                    callbackFcn(loadedData);
                })
            });
            eObject.on('add:resources',function(){              
                self.load(parentEObject,eObject).then(function(loadedData){
                    callbackFcn(loadedData);
                })
            })
            eObject.on('remove:subdirectories',function(){
                self.load(parentEObject,eObject).then(function(loadedData){
                    callbackFcn(loadedData);
                })
            });
            eObject.on('remove:resources',function(){
                self.load(parentEObject,eObject).then(function(loadedData){
                    callbackFcn(loadedData);
                })
            })
        }
        
        this.onChange=function(data,callbackFcn)
        {
            if(data.type='eObject')
            {
                data.value.on('change',function(){
                    callbackFcn(data.value)
                });
            }
        }

        this.canLoad=function(data)
        {
            return data.node.data.eObject.eClass.eContainer.get("nsURI")=='http://www.eoq.de/workspacemdbmodel/v1.0' && data.node.data.eObject.eClass.get('name')=='Workspace';
        }
      
        this.load=function(parentEObject,eObject)
        {            
            var load=[];
            switch(eObject.eClass.get("name"))
            {
                default:                
                    load=ecoreSync.utils.isEClassInitialized(eObject.eClass).then(function(){  
                        var subdirectories=ecoreSync.get(eObject,"subdirectories").then(function(results){
                            return Promise.all( results.map(function(e){ return ecoreSync.get(e,"name"); })).then(function(){                          
                                return Promise.resolve(results.map(function(e){ return {type:'eObject', value: e,modifiers:{}}}));
                            });      
                        });    

                        var resources=ecoreSync.get(eObject,"resources").then(function(results){
                            return Promise.all( results.map(function(e){ return ecoreSync.get(e,"name"); })).then(function(){                              
                                return Promise.resolve(results.map(function(e){ return {type:'eObject', value: e,modifiers:{}}}));
                            });                            
                        }); 

                        return Promise.all([subdirectories,resources]).then(function(values){
                            var contents=values[0];  
                            contents=contents.concat(values[1]);                                                  
                            return Promise.resolve(contents);
                        });
                                       
                    });                    
            }                
    
            return load;
        };
    };
    
    var DirectoryController=function(ecoreSync)
    {
        var ecoreSync=ecoreSync;
        var self=this;
        this.onUpdate=function(parentEObject,eObject,callbackFcn)
        {
            eObject.on('add:subdirectories',function(){
              
                self.load(parentEObject,eObject).then(function(loadedData){
                    callbackFcn(loadedData);
                })
            });
            eObject.on('add:resources',function(){ 
                        
                self.load(parentEObject,eObject).then(function(loadedData){
                    callbackFcn(loadedData);
                })
            })
            eObject.on('remove:subdirectories',function(){
               
                self.load(parentEObject,eObject).then(function(loadedData){
                    callbackFcn(loadedData);
                })
            });
            eObject.on('remove:resources',function(){
                
                self.load(parentEObject,eObject).then(function(loadedData){
                    callbackFcn(loadedData);
                })
            })
        }

        this.onChange=function(data,callbackFcn)
        {
            if(data.type='eObject')
            {
                data.value.on('change',function(){
                    callbackFcn(data.value)
                });
            }  
        }

        this.canLoad=function(data)
        {
            return data.node.data.eObject.eClass.eContainer.get("nsURI")=='http://www.eoq.de/workspacemdbmodel/v1.0' && data.node.data.eObject.eClass.get('name')=='Directory';
        }

        this.load=function(parentEObject,eObject)
        {
            var load=[];
            switch(eObject.eClass.get("name"))
            {
                default:                
                    load=ecoreSync.utils.isEClassInitialized(eObject.eClass).then(function(){

                        var subdirectories=ecoreSync.get(eObject,"subdirectories").then(function(results){
                            return Promise.all( results.map(function(e){ return ecoreSync.get(e,"name"); })).then(function(){
                                return Promise.resolve(results.map(function(e){ return {type:'eObject', value: e,modifiers:{}}}));
                            });      
                        });    

                        var resources=ecoreSync.get(eObject,"resources").then(function(results){
                            return Promise.all( results.map(function(e){ return ecoreSync.get(e,"name"); })).then(function(){
                                return Promise.resolve(results.map(function(e){ return {type:'eObject', value: e,modifiers:{}}}));
                            });                            
                        });    
                        
                        return Promise.all([subdirectories,resources]).then(function(values){

                            var contents=values[0];  
                            contents=contents.concat(values[1]);                          
                            return Promise.resolve(contents);
                        },
                        function(msg){
                            console.error('failed to load')
                        });
                                       
                    });                    
            }                
    
            return load;
        };

  
    };



    var ResourceController=function(ecoreSync)
    {
        var ecoreSync=ecoreSync;
        this.canLoad=function(data)
        {
            return data.node.data.eObject.eClass.eContainer.get("nsURI")=='http://www.eoq.de/workspacemdbmodel/v1.0' && data.node.data.eObject.eClass.get('name')=='ModelResource';
        }

        this.onUpdate=function()
        {
           //ResourceController does not provide updates     
        }

        this.onChange=function()
        {
          //ResourceController does not provide changes       
        }

        this.load=function(parentEObject,eObject)
        {            
            var load=[];
            switch(eObject.eClass.get("name"))
            {
                default:                
                    load=ecoreSync.utils.isEClassInitialized(eObject.eClass).then(function(){
                    
                            return ecoreSync.get(eObject,"contents").then(function(contents)
                            {
                                return ecoreSync.utils.isEClassInitialized(contents[0].eClass).then(function(){
                                    return Promise.resolve([{type:'eObject',value: contents[0],modifiers:{eOwner: eObject}}]);
                                });

                    
                            });
                                           
                                       
                    });                    
            }                
    
            return load;
        };    
    };  


    var WorkspaceContextMenu=function(ecoreSync)
    {
        var self=this;
        this.ecoreSync=ecoreSync;
        this.orderPriority=1;
        this.canDisplayMenuFor=function(data){
            if(!data.eObject)
            {
                return false;
            }
            else
            {
                var nsURI="http://www.eoq.de/workspacemdbmodel/v1.0";
                switch(data.eObject.eClass.get("name"))
                {
                    case 'EReference':                       
                        return data.eObject.eContainer.eContainer.get("nsURI").includes(nsURI);
                    case 'EAttribute':
                        return data.eObject.eContainer.eContainer.get("nsURI").includes(nsURI);
                    default:
                        return data.eObject.eClass.eContainer.get("nsURI").includes(nsURI);

                }      

            }            
        };

        this.display=function(node){
                    var data=node.data;
                    
               
                    let dirCreatableItems={                   
                        "subdir-create": {name: 'Directory', icon: 'directory', callback:async function(){ 

    
                            var subDirNames=await ecoreSync.exec(new eoq2.Get(new eoq2.Obj(data.eObject.get("_#EOQ")).Pth('subdirectories').Pth('name')));
                            
                            var dirBaseName="newSubdir";
                            var currentDirName=dirBaseName;
                            var collisions=0;
                            var nameFound=false;
                            while(!nameFound)
                            {
                                var nameTaken=false;
                                
                                for(let n in subDirNames)
                                {
                                    if(subDirNames[n]==currentDirName)
                                    {
                                        nameTaken=true;
                                        break;
                                    }
                                }

                                if(nameTaken)
                                {
                                    currentDirName=dirBaseName+(collisions+1);
                                    collisions+=1;
                                }
                                else
                                {
                                    nameFound=true;
                                }
                            }

                            var cmd=new eoq2.Cmp();
                            cmd.Crn('http://www.eoq.de/workspacemdbmodel/v1.0','Directory');
                            cmd.Set(new eoq2.His(-1),'name',currentDirName);
                            cmd.Add(new eoq2.Obj(data.eObject.get("_#EOQ")),'subdirectories',new eoq2.His(0));
                            ecoreSync.exec(cmd)
                            
                        }}                        
                    };

                    var eoqMenu={
                        callback: function(key, options) {
                            //TODO: menu actions
                            if(key=="delete")
                            {
                                var dialog = new jsa.MsgBox({
                                    content : 'Do you really want to delete ' + data.eObject.get("name") + '? This action can not be undone.',
                                    buttons : {
                                        yes: {
                                          name: 'Yes',
                                          startEnabled: true,
                                          data: this,
                                          onClickCallback: function(event) {
                                            //MB: why is there another layer above ecoreSync?
                                            pluginAPI.getGlobal('app').commandManager.Execute(new ERemoveCommand(ecoreSync,data.eObject.eContainer,data.eObject.eContainingFeature.get("name"),data.eObject));
                                            dialog.Dissolve();
                                          }
                                        },
                                        no: {
                                            name: 'No',
                                            startEnabled: true,
                                            data: this,
                                            onClickCallback: function(event) {
                                                dialog.Dissolve();
                                            }
                                        }
                                    }
                                });
                                pluginAPI.getGlobal('app').AddChild(dialog);

                                /*
                                ecoreSync.remove(data.eObject.eContainer,data.eObject.eContainingFeature.get("name"),data.eObject).then(function(){
                                    if ($DEBUG) console.debug('eObject successfully removed from reference')
                                })     
                                */
                            }    
                            
                            if(key=="rename")
                            {
                                node.editStart();
                            }


      
                       
                        },
                        items: {       
                               }
                    };

    
                    if(data.eObject.eClass.get("name")=="Directory" || data.eObject.eClass.get("name")=="Workspace" )
                    {
                        eoqMenu.items['create']={name: 'Create', icon: 'add', action:false, items: dirCreatableItems }; 
                    }    
                    if(data.eObject.eClass.get("name")!="Workspace")
                    {
                       eoqMenu.items['delete']={name: "Delete", icon: "delete"};  
                    }

                    return eoqMenu;
             
        };
    }


    pluginAPI.implement("plugin.ecoreTreeView.views",WorkspaceView);
    pluginAPI.implement("plugin.ecoreTreeView.controllers",WorkspaceController);
    pluginAPI.implement("plugin.ecoreTreeView.controllers",DirectoryController);
    pluginAPI.implement("plugin.ecoreTreeView.controllers",ResourceController);
    pluginAPI.implement('plugin.ecoreTreeView.menus',WorkspaceContextMenu);
    return Promise.resolve();
    
};

export var meta={"id":"plugin.ecoreTreeView.eoq",description:"EOQ Plugin for Ecore Tree View","author":"Matthias Brunner","version":"0.0.1","requires":['plugin.ecoreTreeView']};



