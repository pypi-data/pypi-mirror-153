// Plugin Management Extension for jsapplication
// This extends jsapplication with a runtime plugin management system. The required plugins are automatically resolved and an eclipse-like extension mechanism via extension points is provided.
// Plugins must be provided as ECMAScript6 modules.
// (C) 2019-2020 University of Stuttgart, Institute of Aircraft Systems, Matthias Brunner

function PluginManager(pluginConfig,repository='./plugins/',basePath='../',globals={})
{
    this.pluginConfig=pluginConfig;
    this.repository=repository;
    this.basePath=basePath; // the basepath is the relative path from this file to the directory to which the repository path relates 
    this.globals = globals; //variables that are accessible to all plugins and can also be extended during loading
    this.plugins=[];
    this.extensionPoints={};
    this.pending={};
    this.parameters={};

    //start loading the plugins
    let dependencies = [];
    for(d in pluginConfig) dependencies.push(d);
    this.dependenciesResolved=this.resolveDependencies(dependencies).then(function(){ return Promise.resolve() });
}

PluginManager.prototype.getGlobal = function(name) {
    return this.globals[name];
};

PluginManager.prototype.setGlobal = function(name,value) {
    this.globals[name] = value;
};

PluginManager.prototype.resolveDependencies=function(dependencies)
{
    //Attempts the imports missing plugins
    var self=this;
    var plugins=dependencies.map(function(d){
        //check if there configuration data for the plug-in currently looked for
        let enabled = true; //plug-ins are enabled by default, e.g. hidden dependencies.
        if(self.pluginConfig[d] && self.pluginConfig[d].enabled == false) {
            enabled = false; //only retrieve the information if precise configuration is available
        }
        if(enabled) {
            var plugin=self.plugins.find(function(e){ 
                return e.id==d;
            });
            if(plugin && !self.pending[d]) {            
                return Promise.resolve(plugin);
            } else {
                if(self.pending[d]) {        
                    if($DEBUG) console.debug("plugin is pending: "+d)      
                    return self.pending[d];
                } else {   
                    if($DEBUG) console.debug("resolving plugin: "+d) 
                    let pluginPath = self.repository; //global plugin path
                    if(self.pluginConfig[d] && self.pluginConfig[d].pluginPath ) {
                        pluginPath = self.pluginConfig[d].pluginPath //overwrite with a customization
                    }
                    self.pending[d]=self.import(d,pluginPath+d+'/plugin.js').catch(function(e){
                        console.error('plugin '+d+' could not be resolved, '+e);
                        return Promise.reject('unresolved plugin '+d)
                    });
                    return self.pending[d];
                }
                
                
            }
        }
    });
    return Promise.all(plugins);
}

PluginManager.prototype.pluginAPI=function(pluginMeta)
{
    var self=this;
    var pluginId = pluginMeta.id;
    var plugin=this.get(pluginId);   

    var getPluginPath=function(pluginMetaId)
    {
        return function(){
            return plugin["path"];
        };
    }
    var exposePublicAPI=function()
    {
        return function(publicAPI)
        {
            plugin["public"]=publicAPI;
        }
    }
    var loadScripts=function()
    {
        return function(relativePaths) { return self.loadScripts(relativePaths.map(function(relPath){
          return plugin["path"]+relPath;  
        }))};
    };  
    var loadStylesheets=function()
    {
        return function(relativePaths) { return self.loadStylesheets(relativePaths.map(function(relPath){
          return plugin["path"]+relPath;  
        }))};
    }; 
    var loadXMLResources=function()
    {
        return function(relativePaths) { return self.loadXMLResources(relativePaths.map(function(relPath){
          return plugin["path"]+relPath;  
        }))};
    }; 
    var loadModules=function()
    {
        return function(relativePaths) { return self.loadModules(relativePaths.map(function(relPath){
          return plugin["path"]+relPath;  
        }))};
    }; 
    return {
            provide:function(extensionPoint,interface=null,callback=null){ return self.provide(plugin,extensionPoint,interface,callback) },
            implement:function(extensionPoint, extension){ return self.implement(plugin,extensionPoint, extension) },
            evaluate:function(extensionPoint){  return self.evaluate(plugin,extensionPoint) },
            getInterface:function(extensionPoint){   if(self.extensionPoints[extensionPoint]){ return self.extensionPoints[extensionPoint].interface }else { return false; } },
            require: function(id){ return self.require(id); },
            getPath:getPluginPath(),
            getGlobal:function(name){return self.getGlobal(name);},
            setGlobal:function(name,value){return self.setGlobal(name,value);}, 
            loadScripts:loadScripts(),
            loadStylesheets:loadStylesheets(),
            loadXMLResources:loadXMLResources(),
            loadModules:loadModules(),
            expose:exposePublicAPI(),
            getMeta:function(){return pluginMeta}
           };
};

PluginManager.prototype.import=function(id,path)
{
    var self=this;  
    if($DEBUG) console.debug('plugin import from path='+path) 
    return import(self.basePath+path).then(function(plugin){
        
        return self.pending[plugin.meta.id]=self.resolveDependencies(plugin.meta.requires).then(function(){      
                      
                self.register(plugin.meta,path);
                    let config = plugin.meta.config?plugin.meta.config:{}; 
                    //see if the user has specified additional informtion for the plugin      
                    if(self.pluginConfig[id] && self.pluginConfig[id].config) {
                        let userConfig = self.pluginConfig[id].config;
                        Object.assign(config,userConfig);
                    } 
                    return plugin.init(self.pluginAPI(plugin.meta),config).then(function(){ 
                        if($DEBUG) console.debug('plugin path='+path+' successfully initialized');  
                    
                        if(self.pending[plugin.meta.id])
                        {
                            delete self.pending[plugin.meta.id];
                        }                  
                        return Promise.resolve();
                    }).catch(function(error){
                        console.error('internal plugin error occured during initialization, path='+path+', error='+error);  
                        self.unregister(plugin.meta.id);
                        return Promise.reject("plugin initialization failed");
                    });
            
             
            });   
    }).catch(function(error){  
        return Promise.reject(error);
    });;    
};

PluginManager.prototype.importAll=function(plugins)
{
    return Promise.all(plugins.map(function(e){
        return import(e).then(function(object){
            //TODO: is there something to fix here?
            /*
                this.resolveDependencies(object.meta.dependencies).then(function(){

                });               
            */
        });
    }));
};

PluginManager.prototype.register=function(pluginMeta,path)
{
    //registers a plugin, regards dependencies if dependencies were supplied   
    
    var plugin=Object.assign({},pluginMeta);
    let splitPath=path.split("/");
    plugin["path"]=splitPath.slice(0,splitPath.length-1).join('/')+'/';
    if($DEBUG) console.debug('plugin path='+path+' successfully registered');  
    this.plugins.push(plugin); 
      
}

PluginManager.prototype.unregister=function(plugin)
{
    //unregisters a plugin, unregisters all dependend plugins as well
    //causes re-evaluation of extensionPoints
}

PluginManager.prototype.provide=function(plugin,extensionPointId,interface=null,callback=null)
{
    //provides an extensionPoint
    //called by facade in plugin
    if(this.extensionPoints[extensionPointId])
    {
        console.error('The extension point '+extensionPointId+' already exists. Plugin='+plugin.id+', extension point provision failed');
    }
    else
    {
        this.extensionPoints[extensionPointId]={
            id: extensionPointId,
            owner: plugin,
            implementations:[],
            interface:interface,
            callback: callback //is called if a plugin adds to the extension point.
        };
    }
}

PluginManager.prototype.implement=function(plugin,extensionPointId,extension)
{
    //adds an implemention to an extensionPoint
    //only existing extensionPoints can be implemented
    //causes re-evaluation of extensionPoints
    //called by facade in plugin
    let extensionPoint = this.extensionPoints[extensionPointId];
    if(!extensionPoint)
    {       
        console.error('The extension point '+extensionPointId+' does not exist. Plugin='+plugin.id+', extension point implementation failed');
    }
    else
    {
        //TODO: call validation        
        extensionPoint.implementations.push({implementation: extension, owner: plugin});
        //inform any listener
        if(extensionPoint.callback) {
            try {
                let pluginImplementEvent = new PluginExtensionEvent("IMPLEMENT",extensionPoint,extension);
                // let pluginImplementEvent = {
                //     id : "IMPLEMENT",
                //     extension : extension
                // }
                extensionPoint.callback(pluginImplementEvent);
            } catch(e) {
                console.warn("Plugin implent callback: Callback on implement of "+extensionPointId+" failed: "+e.toString());
            }
        }
    }
}

PluginManager.prototype.evaluate=function(plugin,extensionPoint)
{    
    if(!this.extensionPoints[extensionPoint])
    {
        console.error('The extension point '+extensionPoint+' does not exist. Plugin='+plugin.id+', extension point evaluation failed');
    }
    else
    {
        if(this.extensionPoints[extensionPoint].owner!=plugin)
        {
            console.warn('The extension point '+extensionPoint+' evaluation failed. Extension points can only be evaluated by owners. Plugin='+plugin.id);
            return [];
        }
        else
        {
            return this.extensionPoints[extensionPoint].implementations.map(function(e){
                return e.implementation;
            });            
        }
    }
}

PluginManager.prototype.getImplementers=function(extensionPoint)
{
    //returns an array containing all plugins providing an extension for the extensionPoint
    if(!this.extensionPoints[extensionPoint])
    {
        return [];
    }
    else
    {
        
        var implementers=this.extensionPoints[extensionPoint].implementations.map(function(e){
            return e.owner.id
        });
        return implementers;
    }
}

PluginManager.prototype.list=function()
{
    //returns an array containing all registered plugins
};

PluginManager.prototype.require=function(id)
{
    //returns the public API of a plug-in
    let plugin=this.plugins.find(function(e){return e.id==id;});
    if(plugin)
    {  
        return plugin.public;
    }
    else
    {      
        throw 'required plugin '+id+' is not loaded'
    }
}

/* MARKED FOR DELETION */
PluginManager.prototype.get=function(id) //DUPLICATE FUNCTION?
{
    //returns the public API of a plug-in
    let plugin=this.plugins.find(function(e){return e.id==id;});
    if(plugin)
    {
        return plugin;
    }
    else
    {
        throw 'required plugin '+id+' is not loaded'
    }
}
/* END MARKED FOR DELETION */

//AUX for loading entities

PluginManager.prototype.loadScripts=function(paths)
{
    var self=this;
    var loadStatus=[];
    paths.map(function(e){
        if($DEBUG) console.debug('loading script from path:'+e)
        loadStatus.push(self.load.script(e));
    });
    return Promise.all(loadStatus);
}

PluginManager.prototype.loadStylesheets=function(paths)
{
    var self=this;
    var loadStatus=[];
    paths.map(function(e){
        if($DEBUG) console.debug('loading stylesheet from path:'+e)
        loadStatus.push(self.load.stylesheet(e));
    });
    return Promise.all(loadStatus);
}

PluginManager.prototype.loadXMLResources=function(paths)
{
    var self=this;
    var loadStatus=[];
    paths.map(function(e){
        if($DEBUG) console.debug('loading XML resource from path:'+e)
        loadStatus.push(self.load.xml(e));
    });
    return Promise.all(loadStatus);
}

PluginManager.prototype.loadModules=function(paths)
{
    var self=this;
    var loadStatus=[];
    paths.map(function(e){
        if($DEBUG) console.debug('loading module from path:'+e)
        loadStatus.push(import(self.basePath+e));
    });
    return Promise.all(loadStatus);
}

PluginManager.prototype.load=(function(){

    var __documentLoad=function(arg)
    {
        return function(url) {
            return new Promise(function(resolve,reject){
                var element = document.createElement(arg.tag);       
                element.onload=function(){    
                    if($DEBUG) console.debug("resource loaded: "+url);           
                    resolve();
                }
                element.onerror=function(){
                    reject();
                }
                element[arg.urlAttribute]=url;
                for (var attr in arg.attributes){
                    element[attr]=arg.attributes[attr];
                }
                document[arg.parent].appendChild(element);
            });            
        }
    };

    var __xmlRequest=function()
    {
        return function(url)
        {
            return new Promise(function(resolve,reject){
             var xhttp = new XMLHttpRequest();     
             xhttp.open("GET", url);
             xhttp.send();
             xhttp.onload=function()
             {
                 resolve({xml: xhttp.responseXML, txt: xhttp.responseText});
             }
             xhttp.onerror=function()
             {
                 reject(xhttp.statusText);
             }          
            });
        }
    };

    return {
        script: __documentLoad({tag:'script',urlAttribute:'src',attributes:{async:false,type:'text/javascript'},parent:'head'}),
        stylesheet: __documentLoad({tag:'link',urlAttribute:'href',attributes:{rel:'stylesheet'},parent:'head'}),
        xml: __xmlRequest()
    };
})();



PluginManager.prototype.loadScript=function(pluginPath,type="text/javascript")
{
    //loads a script, might be replaced by ES6 import mechanisms
    document.write('<script type=\"'+type+'\" src=\"'+pluginPath+'\"></script>');
}

PluginManager.prototype.linkStylesheet=function(pluginPath,type="text/javascript")
{
    //loads a stylesheet
    document.write('<script type=\"'+type+'\" src=\"'+pluginPath+'\"></script>');
}

function PluginExtensionEvent(id,extensionPointId,extension) {
    this.id = id;
    this.extensionPoint = extensionPointId;
    this.extension = extension;
};

