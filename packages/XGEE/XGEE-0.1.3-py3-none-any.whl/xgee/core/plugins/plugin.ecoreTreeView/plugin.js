
var extensionPoints={};


var DefaultView=function(iconPath)
{
    var self=this;
    this.iconPath=iconPath;
    this.apply=function(data)
    {
        var view=null;    
        if(data.type=='eObject')
        {
            switch(data.value.eClass.get("name"))
            {
                case "EReference":
                    if(data.value.get("containment"))
                    {
                        view={title: data.value.get("name"), icon:iconPath+"EReference.gif", eObject: data.value, modifiers:data.modifiers, lazy: true}; 
                    }
                    break;
                case "EAttribute":
                    view=null;
                    break;
                default:
                    view={title: data.value.eClass.get("name"), icon:iconPath+"EObject.gif", eObject: data.value,modifiers:data.modifiers, lazy: true}; 
            }
        }
        
        if(data.type=='value')
        {
            view={title: "value("+data.value.dataType+")="+data.value.value }; 
        }

        return view;
    };
}

/*
var DefaultObserver=function(ecoreSync,treeDOM)
{
    var ecoreSync=ecoreSync;
    this.eventListeners=[];
    this.treeDOM=treeDOM;
    this.observerInstances=[];

    this.invalidateNode=function(view,eObject)
    {
        //Invalidates all nodes refering to the supplied eObject
        //for all invalidated nodes the tree representation will be updated using the supplied view

        var self=this;
        var tree=$.ui.fancytree.getTree("#"+self.treeDOM.getAttribute("id"));                     
        tree.visit(function(e){
            if(e.data.eObject==eObject)
            {
                e.fromDict(view.apply({type:'eObject',value: eObject}));
            }
        })        
    }

    this.invalidateChildNodes=function(loader=null,view=null,parentEObject=null,eObject=null)
    {     
        console.error('Invalidated child nodes for #'+parentEObject.get("_#EOQ")+'/'+eObject.get("_#EOQ"))   
        var self=this;
        var tree=$.ui.fancytree.getTree("#"+self.treeDOM.getAttribute("id"));   
        loader.load(parentEObject,eObject).then(function(loadedData){

            //Synchronizing model and tree         

            var node=tree.findFirst(function(e){
                if(e.data.eObject==eObject && e.parent.data.eObject==parentEObject)
                {
                    return true;
                }           
                return false;
            })
            if(node)
            {
                var currentChildren=node.getChildren();
                var addedChildren=loadedData.filter(function(e){
                    var match=currentChildren.find(function(c){        
                        return e.value==c.data.eObject
                    })
                    if(match)
                    {
                        return false
                    }
                    else
                    {
                        return true
                    }
                })
                var removedChildren=currentChildren.filter(function(e){
                    var match=loadedData.find(function(c){        
                        return e.data.eObject==c.value
                    })
                    if(match)
                    {
                        return false
                    }
                    else
                    {
                        return true
                    }
                })
                addedChildren.map(function(e){
                    self.observe(e.value,e,loader,view) 
                    node.addNode(view.apply(e),'child');
                });            
                removedChildren.map(function(e){
                    node.removeChild(e);
                })               
            }
        });

    }


    this.observe=function(parentEObject,data,loader,view)
    {
        this.parentEObject=parentEObject    
        var self=this;
        
        //Actual Observer object
        var Observer=function(item)
        {
            this.loader=loader;
            this.view=view;
            var observer=this;
            if(item.type=='eObject')
            {
                let eObject=item.value;
                switch(eObject.eClass.get("name"))
                {
                    case "EReference":
                        parentEObject.on('add:'+eObject.get("name"),function(){ 
                            self.invalidateChildNodes(observer.loader,observer.view,parentEObject,eObject);
                        })
                        parentEObject.on('remove:'+eObject.get("name"),function(){ 
                            self.invalidateChildNodes(observer.loader,observer.view,parentEObject,eObject);                           
                        })            
                        break;
                    case "EAttribute":
                        console.error('Observe EAttribute');
                        console.error(eObject);
                        break;
                    default:                
                        console.error('Observe EObject of Misc Type');               
                        eObject.on('change',function(){
                            self.invalidateNode(observer.view,eObject)
                        });

                        break;                            
                }  
            }
            else
            {
                console.error('Observe item of type != eObject (NOT IMPLEMENTED)')
            }
        }

        //Create Observers for the supplied data items
        if(Array.isArray(data))
        {
            data.map(function(item){        
                self.observerInstances.push(new Observer(item));
            });     
        }
        else
        {
            self.observerInstances.push(new Observer(data));
        }    
    }
}
*/

var DefaultController=function(ecoreSync,treeDOM,eventBroker)
{
    var ecoreSync=ecoreSync;
    this.treeDOM=treeDOM;
    this.observerInstances=[];
    this.eventBroker = eventBroker;

    this.invalidateNode=function(view,eObject)
    {
        //Invalidates all nodes refering to the supplied eObject
        //for all invalidated nodes the tree representation will be updated using the supplied view

        var self=this;
        var tree=$.ui.fancytree.getTree("#"+self.treeDOM.getAttribute("id"));                     
        tree.visit(function(e){
            if(e.data.eObject==eObject)
            {
                e.fromDict(view.apply({type:'eObject',value: eObject}));
            }
        })        
    }

    this.invalidateChildNodes=function(view=null,parentEObject=null,eObject=null)
    {                
        var self=this;
        var tree=$.ui.fancytree.getTree("#"+self.treeDOM.getAttribute("id"));   
        self.load(parentEObject,eObject).then(function(loadedData){

            //Synchronizing model and tree         

            var node=tree.findFirst(function(e){
                if(e.data.eObject==eObject && e.parent.data.eObject==parentEObject)
                {
                    return true;
                }           
                return false;
            })
            if(node)
            {
                var currentChildren=node.getChildren();
                var addedChildren=loadedData.filter(function(e){
                    var match=currentChildren.find(function(c){        
                        return e.value==c.data.eObject
                    })
                    if(match)
                    {
                        return false
                    }
                    else
                    {
                        return true
                    }
                })
                var removedChildren=currentChildren.filter(function(e){
                    var match=loadedData.find(function(c){        
                        return e.data.eObject==c.value
                    })
                    if(match)
                    {
                        return false
                    }
                    else
                    {
                        return true
                    }
                })
                addedChildren.map(function(e){
                    self.startObserving(e.value,e,view) 
                    node.addNode(view.apply(e),'child');
                });            
                removedChildren.map(function(e){
                    node.removeChild(e);
                })               
        }
        });

    }

    this.onUpdate=function()
    {
       /* todo */  
       if($DEBUG) console.debug("default controller update detected")
    }

    this.onChange=function()
    {
      /* todo */     
      if($DEBUG) console.debug("default controller change detected")
    }

    this.startObserving=function(parentEObject,data,view)
    {
        this.parentEObject=parentEObject    
        var self=this;
        
        //Actual Observer object
        var Observer=function(item)
        {           
            this.view=view;
            var observer=this;
            if(item.type=='eObject')
            {
                let eObject=item.value;
                switch(eObject.eClass.get("name"))
                {
                    case "EReference":
                        parentEObject.on('add:'+eObject.get("name"),function(){ 
                            self.invalidateChildNodes(observer.view,parentEObject,eObject);
                        })
                        parentEObject.on('remove:'+eObject.get("name"),function(){ 
                            self.invalidateChildNodes(observer.view,parentEObject,eObject);                           
                        })            
                        break;
                    case "EAttribute":
                        break;
                    default:                     
                        eObject.on('change',function(){
                            self.invalidateNode(observer.view,eObject)
                        });

                        break;                            
                }  
            }
            else
            {
                if($DEBUG) console.debug('Observer for item of type != eObject is not implemented')
            }
        }

        //Create Observers for the supplied data items
        if(Array.isArray(data))
        {
            data.map(function(item){        
                self.observerInstances.push(new Observer(item));
            });     
        }
        else
        {
            self.observerInstances.push(new Observer(data));
        }    
    }
    
    this.load=function(parent,eObject)
    {        
        $.notify("Default Contoller used");
        var load=[];
        switch(eObject.eClass.get("name"))
        {
            case "EReference":
                load=ecoreSync.get(parent,eObject.get("name")).then(function(results){
                    var value=[];
                    if(Array.isArray(results))
                    {                      
                        value=results;
                    }
                    else
                    {
                        if(results!=null)
                        {
                        value=[results];
                        }                        
                    }
                    return Promise.resolve(value.map(function(e){ return {type:'eObject', value: e, modifiers:{}}}));
                });
                break;
            case "EAttribute":
                load=ecoreSync.get(parent,eObject.get("name")).then(function(value){
                    return Promise.resolve([{type:'value', value: {dataType: eObject.get("eType").get("name"), value: value, modifiers:{}} }]);
                });
                break;
            default:                
                load=ecoreSync.utils.isEClassInitialized(eObject.eClass).then(function(){
                    var features=eObject.eClass.get("eStructuralFeatures").array();
                    return Promise.resolve(features.map(function(e){ return {type:'eObject', value: e,modifiers:{eOwner:eObject}}}));
                });
                
                
                
        }           
   
        return load;
    };


}







export async function init(pluginAPI) { 
    
    var contextMenu=pluginAPI.require('contextMenu');
    var clipboard=pluginAPI.require('clipboard');

    var modules=await pluginAPI.loadModules(['js/TreeViewContextMenuProvider.js']);

    extensionPoints.controllers=pluginAPI.provide("plugin.ecoreTreeView.controllers");
    extensionPoints.views=pluginAPI.provide("plugin.ecoreTreeView.views");
    pluginAPI.provide("plugin.ecoreTreeView.menus");


    var menuProviders=[];
    extensionPoints.menus=pluginAPI.provide('ecoreTreeView.menus',modules[0].TreeViewContextMenuProvider,function(event){
        menuProviders.push(event.extension);
    });


    extensionPoints.edit=pluginAPI.provide("plugin.ecoreTreeView.edit");


  


    

    var create=async function(ecoreSync,id,DOMelement,rootObjectId=0,rootObjectName=null,theme=null){
        
        var controllers=pluginAPI.evaluate('plugin.ecoreTreeView.controllers').map(function(Controller){
            return new Controller(ecoreSync,DOMelement);
        });

        var views=pluginAPI.evaluate('plugin.ecoreTreeView.views').map(function(View){
            return new View(ecoreSync);
        });

        /*
        var menus=pluginAPI.evaluate('plugin.ecoreTreeView.menus').map(function(Menu){
            return new Menu(ecoreSync);
        });
        */



        var rootObject=await ecoreSync.getObject(rootObjectId);
        if(!rootObject) throw 'root object could not be resolved #'+rootObjectId
        var treeViewId=id;
        DOMelement.innerHTML='<br>';
        var rootObjectName=(rootObjectName || rootObject.get("name")) || 'Root';

        var eventBroker=pluginAPI.require('eventBroker');
        var SelectionChangedEvent = eventBroker.SelectionChangedEvent;

        var defaultView=new DefaultView(pluginAPI.getPath()+"ecore-icons/");  
        var defaultController=new DefaultController(ecoreSync,DOMelement,eventBroker); 
        
        
        //var defaultObserver=new DefaultObserver(ecoreSync,DOMelement);
        //window["debug"]={source: view.apply({ eObject: rootObject, featureName:null})};


        var view=views.find(function(e){ return e.canDisplay({type:'eObject',value: rootObject, modifiers:{}}); });
        if(!view)
        {
            view=defaultView;
        }                  

        $(DOMelement).fancytree({clickFolderMode:1,selectMode: 2, source: [view.apply({type:'eObject',value: rootObject})], lazyLoad: function (event, data) { 
            
                //select controller
                var controller=controllers.find(function(e){ return e.canLoad(data); });
                if(!controller)
                {
                    controller=defaultController;
                }

                var parentEObject=data.node.parent.data.eObject;
                if(data.node.data.modifiers)
                {
                    if(data.node.data.modifiers["eOwner"])
                    {
                        parentEObject=data.node.data.modifiers["eOwner"];
                    }
                }
            
                data.result = controller.load(parentEObject,data.node.data.eObject).then(function(loadedData){
                    var treeData=loadedData.map(function(nodeData){                            
                            var view=views.find(function(e){ return e.canDisplay(nodeData); }) || defaultView;
        
                            controller.onChange(nodeData,function(eObject){
                                //Updating node                                
                                var tree=$.ui.fancytree.getTree("#"+DOMelement.getAttribute("id"));                     
                                tree.visit(function(e){
                                    if(e.data.eObject==eObject)
                                    {
                                        e.fromDict(view.apply({type:'eObject',value: eObject}));
                                    }
                                })        
                                if($DEBUG) console.debug('plugin.ecoreTreeView updated changed node')
                            });    
                            return view.apply(nodeData);
                    }).filter(function(e){ return e!==null;}); 

                    controller.onUpdate(parentEObject,data.node.data.eObject,function(loadedData){
                            //controllers should fire this update if children are added or removed
                            //it should/can not be used for update events of children attributes (e.g. if a name changes)
                            //use onChange if you need to react to attribute changes   

                            //Synchronizing model and tree      
                            var tree=$.ui.fancytree.getTree("#"+DOMelement.getAttribute("id"));        
                            var node=tree.findFirst(function(e){
                                if(e.data.eObject==data.node.data.eObject && e.parent.data.eObject==parentEObject)
                                {
                                    return true;
                                }           
                                return false;
                            })
                            if(node)
                            {
                                var currentChildren=node.getChildren();
                                var addedChildren=loadedData.filter(function(e){
                                    var match=currentChildren.find(function(c){        
                                        return e.value==c.data.eObject
                                    })
                                    if(match)
                                    {
                                        return false
                                    }
                                    else
                                    {
                                        return true
                                    }
                                })
                                var removedChildren=currentChildren.filter(function(e){
                                    var match=loadedData.find(function(c){        
                                        return e.data.eObject==c.value
                                    })
                                    if(match)
                                    {
                                        return false
                                    }
                                    else
                                    {
                                        return true
                                    }
                                })

                                
                                addedChildren.map(function(c){   

                                    var view=views.find(function(v){ return v.canDisplay(c); });  
                                    controller.onChange(c,function(eObject){
                                        //Updating node                                
                                        var tree=$.ui.fancytree.getTree("#"+DOMelement.getAttribute("id"));                     
                                        tree.visit(function(e){
                                            if(e.data.eObject==eObject)
                                            {
                                                e.fromDict(view.apply({type:'eObject',value: eObject}));
                                            }
                                        })        
                                        if($DEBUG) console.debug('plugin.ecoreTreeView updated changed node')
                                    });        
                                    
                                    var successor=null;
                                    let idx= loadedData.indexOf(c)
                                    if(loadedData[idx+1])
                                    {
                                        successor=tree.findFirst(function(e){
                                            if(e.data.eObject==loadedData[idx+1].value && e.parent.data.eObject==eObject)
                                            {
                                                return true;
                                            }           
                                            return false;
                                        })
                                    }                          
                                    if(successor)
                                    {
                                        node.addChildren([view.apply(c)],successor);
                                    }
                                    else
                                    {
                                        node.addChildren([view.apply(c)]);
                                    }
                                });     
                                
                                removedChildren.map(function(e){
                                    node.removeChild(e);
                                })               
                            }
                            else
                            {
                                console.error('Node not found!')
                            }                               
                });

                return Promise.resolve(treeData);
                });
            },
            activate: function(event,data){
                var node = data.node;
                var tree = data.tree;                
                if(!event.ctrlKey && !event.shiftKey)
                {
                    tree.visit(function(node){
                        node.setSelected(false);
                    });

                    node.setActive(true);                  
                    node.setSelected(true);                  
                    
                }
                if(event.ctrlKey)
                {
                    node.toggleSelected();
                    return false;
                }                 
            },
            select: function(event, data) {
                // Display list of selected nodes
                var nodeSelection = data.tree.getSelectedNodes().join(", ");  
                var selectedEObjects=data.tree.getSelectedNodes().map(function(e){
                    return e.data.eObject
                })
                var activeNode=data.tree.getActiveNode();
                if(activeNode)
                {                   
                    var labelDom= activeNode.span.children[2];      
                    
                    //Depricated
                    // $app.selectionManager.SetSelection(new jsa.Selection({
                    //     elements: selectedEObjects,
                    //     eventSource: this,
                    //     domElement: labelDom
                    // })); 

                    //try new event broker
                    let changeEvent = new SelectionChangedEvent(this,selectedEObjects,labelDom);
                    eventBroker.publish("SELECTION/CHANGE",changeEvent);
                }
                
            },  
            edit: {
                // Available options with their default:
                adjustWidthOfs: 4,   // null: don't adjust input size to content
                inputCss: { minWidth: "3em" },
                triggerStart: ["f2"],
                beforeEdit: $.noop,   // Return false to prevent edit mode
                edit: $.noop,         // Editor was opened (available as data.input)
                beforeClose: $.noop,  // Return false to prevent cancel/save (data.input is available)
                save: function(){ return true },         // Save data.input.val() or return false to keep editor open
                close: $.noop,        // Editor was removed
            }         
        });

       //make connectors visible (dotted lines)
       $(".fancytree-container").addClass("fancytree-connectors");
       if(theme)
       {
        $(".fancytree-container").addClass(theme);
       }

       var mergeItems=function(itemsA,itemsB)
       {
            var items=Object.assign({},itemsA);;
            for(let key in itemsB)
            {
                if(items[key])
                {
                    
                    if(items[key]['items'] && itemsB[key]['items'])
                    {
                        items[key]['items']=mergeItems(items[key]['items'],itemsB[key]['items']);
                    }
                    else
                    {
                        console.error('cannot merge items')
                    }
                }
                else
                {
                    items[key]=itemsB[key];
                }
            }
            return items;
       }

       var mergeMenus=function(menus,node){
        var items={};
        var itemCallbacks={};
        for(let i in menus)
        {
            var menuDisplay=menus[i].display(node)
            for(const key in menuDisplay.items)
            {
                if(!items[key])
                {
                    items[key]=menuDisplay.items[key]
                    itemCallbacks[key]=menuDisplay.callback
                }
                else
                {
                    
                    if(items[key]['items'] && menuDisplay.items[key]['items'])
                    {
                       items[key]['items']=mergeItems(items[key]['items'],menuDisplay.items[key]['items']);                        
                    }
                    else
                    {
                        console.error('Cannot reassign key='+key+' for context menu of ecoreTreeView')
                    }
                }
            }
        }

        return {
            items: items,
            callback: function(key,options){
                if(itemCallbacks[key])
                {
                    return itemCallbacks[key](key,options);
                }
                else
                {
                    if($DEBUG) console.error('No callback known for context menu key='+key)
                }
            }
        }



       }




   


       var menus=pluginAPI.evaluate('plugin.ecoreTreeView.menus').map(function(Menu){
        return new Menu(ecoreSync);
       });


       var cmenuProviders=pluginAPI.evaluate('ecoreTreeView.menus');

       
       //registering context menu with tree
       $.contextMenu({
            selector: '#'+DOMelement.id+' .fancytree-title',  
            build: function($triggerElement, e){

                e.preventDefault();
                var menu=null;
                var node = $.ui.fancytree.getNode(e);  
                var offset=$($triggerElement).offset();         

                var applicableMenuProviders=cmenuProviders.filter(function(e){ return e.isApplicableToNode(node); })    
                if(applicableMenuProviders.length > 0)
                {
                    contextMenu.showContextMenu({x:offset.left+50,y:offset.top+10},contextMenu.util.collectAndMerge(applicableMenuProviders,node));        
                }        

                return false;                          
            }
        });

        //registering copy, cut and paste-handlers with tree
        $(DOMelement).on('paste','.fancytree-node',async function(event){
            var node = $.ui.fancytree.getNode(event);  
            await clipboard.evalEvent(event.originalEvent);      
            try{
                if(node.data.eObject.eClass.get('name')!='EReference')
                {
                    await clipboard.pasteToEObject(node.parent.data.eObject);
                }
                else
                {
                    await clipboard.pasteToEObject(node.data.eObject);
                }
            }
            catch(e)
            {
                console.error(e)
            }
            event.stopPropagation();
        });

        $(DOMelement).on('copy','.fancytree-node',async function(event){
            var node = $.ui.fancytree.getNode(event);                      
            await clipboard.evalEvent(event.originalEvent,ecoreSync.utils.getObjectURL(node.data.eObject));
            event.stopPropagation();
        });

        $(DOMelement).on('cut','.fancytree-node',async function(event){
            var node = $.ui.fancytree.getNode(event);                      
            await clipboard.evalEvent(event.originalEvent,ecoreSync.utils.getObjectURL(node.data.eObject));
            event.stopPropagation();
        });

        //TODO: Move to plugin?
        $(DOMelement).on('dblclick','.fancytree-node',async function(event){
            var node = $.ui.fancytree.getNode(event);
            eventBroker.publish('PROPERTIESVIEW/OPEN',{eObject:node.data.eObject,DOM:node.span.children[2]}); 
            event.stopPropagation();    
        })
        
   


        
    }



    
    pluginAPI.expose({create:create});
    return true;
};

export var meta={
    "id":"plugin.ecoreTreeView",
    description:"Ecore TreeView",
    "author":"Matthias Brunner",
    "version":"0.0.1",
    "requires":[
        'ecoreSync',
        'plugin.fancyTree',
        'plugin.contextMenu',
        'eventBroker',
        'contextMenu',
        'clipboard'
    ]
};



