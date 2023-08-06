
export async function init(pluginAPI) {      

    var eventBroker=pluginAPI.require('eventBroker')
    var contextMenu=pluginAPI.require('contextMenu');
    var iconProvider=pluginAPI.require('iconProvider');
    var modules=await pluginAPI.loadModules(["js/Filter.js"]);


    var filters=[];
    pluginAPI.provide('contextMenu.ecore.filters',modules[0].Filter,function(event){
        filters.push(event.extension);
    });

    
    class EditorCanvasContextMenuProvider extends pluginAPI.getInterface('editor.menus'){
        constructor(){
            super();
        }
        isApplicableToTarget(target){
            return target.isCanvas 
        }
        getContextMenu(target){
            var cMenu=false;
            if(target.isCanvas)
            {
                 cMenu=contextMenu.createContextMenu('ecore-context-menu','Ecore Context Menu',1);
                 cMenu.addNewEntry('properties','Properties',async function(){
                    eventBroker.publish('PROPERTIESVIEW/OPENMODAL',target);                                            
                 },'edit');
                 cMenu.addNewEntry('paste','Paste',async function(){
                    eventBroker.publish('CLIPBOARD/CMD/LOCALPASTE',target.eObject);                                            
                },'paste');
                cMenu.addNewEntry('reinit','Reinitialize',async function(){
                    // Remember the current XGEE view
                    let eObject=$app.viewManager.activeView.XGEEInstance.graphController.eObject
                    let allEditors=$app.plugins.require('editor').getEditors(eObject)
                    let editorIdx=allEditors.indexOf($app.viewManager.activeView.editor)
                    if(editorIdx>=0)
                    {
                        //Close the editor
                        $app.viewManager.activeView.Close()
                        //Re-open the editor
                        $app.plugins.require('editor').open(eObject,true,editorIdx)
                    }                   
                },'refresh');

            }
            return cMenu;
        }
    }

    class GraphObjectContextMenuProvider extends pluginAPI.getInterface('editor.menus'){
        constructor(){
            super();
        }
        isApplicableToTarget(target){
            return target.isGraphObject
        }
        getContextMenu(target)
        {
            var cMenu=false;
            if(target.isGraphObject){
                if(target.isVertex)
                {
                    cMenu=cMenu?cMenu:contextMenu.createContextMenu('ecore-context-menu','Ecore Context Menu',1)  
                    
                    cMenu.addNewEntry('properties','Properties',async function(){
                        eventBroker.publish('PROPERTIESVIEW/OPEN',target);                                            
                    },'edit');

                    cMenu.addNewEntry('copy','Copy',async function(){
                        eventBroker.publish('CLIPBOARD/CMD/COPY',target.eObject);                        
                    },'copy');

                    cMenu.addNewEntry('copy-here','Copy here',async function(){
                        var copy=await ecoreSync.clone(target.eObject);        
                        var pos=target.position
                        pos.x+=target.graphObject.getSize().x
                        pos.y+=target.graphObject.getSize().y             
                        $app.viewManager.activeView.XGEEInstance.getGraphController().paste(copy,target.graphObject.parent.getEObject(),pos)
                        $app.viewManager.activeView.XGEEInstance.getGraphController().select(null)                        
                    },'copy');

                    cMenu.addNewEntry('cut','Cut',async function(){
                        eventBroker.publish('CLIPBOARD/CMD/CUT',target.eObject);                        
                    },'cut');
                }
                
                
                if(target.graphObject.isDeletable())
                {
                    cMenu=cMenu?cMenu:contextMenu.createContextMenu('ecore-context-menu','Ecore Context Menu',1)
                    if(target.isVertex){
                        cMenu.addNewEntry('delete','Delete',async function(){ 
                            target.graphObject.delete()
                        },'delete');
                    }
                    if(target.isEdge){
                        cMenu.addNewEntry('delete','Delete',async function(){                             
                            target.graphObject.delete(target.edgeSource,target.edgeTarget)
                        },'delete');
                    }
                }

                
            }
            return cMenu;
        }
    }



    class EcoreContextMenuProvider extends pluginAPI.getInterface('ecoreTreeView.menus'){
        constructor(){
            super();
        }

        isApplicableToNode(node)
        {

            if(filters.reduce(function(accumulator, currentValue){
                return accumulator || currentValue.select(node.data.eObject)
            },false)){
                //this node was filtered
                return false;
            }



            switch(node.data.eObject.eClass.get("name"))
            {
                case 'EReference':            
                    return node.data.eObject.get('containment')
                case 'EAttribute':
                    return false;
                default:
                    return true;
            }      
        }

        getContextMenu(node)
        {
            var cMenu=false;     
            
            switch(node.data.eObject.eClass.get("name"))
            {
                case 'EReference':      
                    if(node.data.eObject.get('containment'))
                    {
                        cMenu=contextMenu.createContextMenu('ecore-context-menu','Ecore Context Menu',1);

                        if(node.data.eObject.get('eType').get('abstract'))
                        {
                            var creationMenu=contextMenu.createContextMenu('ecore-context-menu-sub-create','New',1,'add');
                            cMenu.addSubMenu('create',creationMenu);        
                            creationMenu.addEntryProvider('prov-concrete-classes',async function(){ 

                                var cmd=new eoq2.Cmp();
                                cmd.Get(new eoq2.Obj(ecoreSync.rlookup(node.data.eObject.get('eType'))).Met('ALLIMPLEMENTERS').Sel(new eoq2.Pth('abstract').Equ(false)));
                                cmd.Get(new eoq2.His(-1).Pth('name'))                          
                                var res=await ecoreSync.remoteExec(cmd,true);
                                var entries={};
                                var creatableClasses=res[0]                          

                                creatableClasses.forEach(function(c,i){
                                    entries["create-class-"+i]={type:'entry', value: contextMenu.createContextMenuEntry(c.get('name')+' <img src="'+iconProvider.getPathToIcon(c)+'" class="ctxtEcore-inline-img" onerror="this.style.display=\'none\'">', async function(){                          
                                        var createdObject= await ecoreSync.create(c)
                                        var upperBound=node.data.eObject.get("upperBound");  

                                        if(upperBound!=1)
                                        {
                                            ecoreSync.add(node.data.modifiers['eOwner'],node.data.eObject.get('name'),createdObject)
                                        }
                                        else
                                        {
                                            ecoreSync.set(node.data.modifiers['eOwner'],node.data.eObject.get('name'),createdObject)
                                        }
                                    },'add')};                             
                                })

                                return entries;
                            });


                        }
                        else
                        {

                            cMenu.addEntryProvider('prov-concrete-classes',async function(){ 

                                         var entries={};
                                         var contents=await ecoreSync.get(node.data.modifiers['eOwner'],node.data.eObject.get('name'))
                                         var upperBound=node.data.eObject.get("upperBound");  

                                         entries['create-object']={type:'entry', value: contextMenu.createContextMenuEntry('New '+node.data.eObject.get('eType').get("name")+' <img src="'+iconProvider.getPathToIcon(node.data.eObject.get('eType'))+'" class="ctxtEcore-inline-img" onerror="this.style.display=\'none\'">',async function(){ 
                                            var createdObject= await ecoreSync.create(node.data.eObject.get('eType'))
                                            
                                            if(upperBound!=1)
                                            {
                                                ecoreSync.add(node.data.modifiers['eOwner'],node.data.eObject.get('name'),createdObject)
                                            }
                                            else
                                            {
                                                ecoreSync.set(node.data.modifiers['eOwner'],node.data.eObject.get('name'),createdObject)
                                            }
                                        },'add')};
                                    
                                        
                                        if(upperBound==1 && contents)
                                        {
                                            entries['create-object'].value.disable(); //disable creation for upper bound=1 and non-empty reference
                                        }

                                        return entries
                            });
                        }

                        cMenu.addNewEntry('copy-all','Copy all',async function(){
                            eventBroker.publish('CLIPBOARD/CMD/COPY',await ecoreSync.get(node.data.modifiers.eOwner,node.data.eObject.get("name")));                        
                        },'copy');

                        cMenu.addNewEntry('paste','Paste',async function(){
                            eventBroker.publish('CLIPBOARD/CMD/LOCALPASTE',node.data.modifiers.eOwner);                        
                        },'paste');

                    }                           
                    break;
                case 'EAttribute':
                    break;
                default:
                    cMenu=contextMenu.createContextMenu('ecore-context-menu','Ecore Context Menu',1);
                   

                    cMenu.addNewEntry('properties','Properties',async function(){
                        eventBroker.publish('PROPERTIESVIEW/OPEN',{eObject:node.data.eObject,DOM:node.span.children[2]});                                            
                    },'edit');

                    cMenu.addNewEntry('copy','Copy',async function(){
                        eventBroker.publish('CLIPBOARD/CMD/COPY',node.data.eObject);                        
                    },'copy');

                    cMenu.addNewEntry('copy-here','Copy here',async function(){
                        var copy=await ecoreSync.clone(node.data.eObject);
                        await ecoreSync.add(node.data.eObject.eContainer,node.data.eObject.eContainingFeature.get("name"),copy)                         
                    },'copy');

                    cMenu.addNewEntry('cut','Cut',async function(){
                        eventBroker.publish('CLIPBOARD/CMD/CUT',node.data.eObject);                        
                    },'cut');

                    cMenu.addNewEntry('delete','Delete',async function(){ 
                        if(node.data.eObject.eContainingFeature.get('upperBound')!=1)
                        {
                            ecoreSync.remove(node.data.eObject.eContainer,node.data.eObject.eContainingFeature.get("name"),node.data.eObject)
                        }
                        else
                        {
                            ecoreSync.unset(node.data.eObject.eContainer,node.data.eObject.eContainingFeature.get("name"));
                        }
                    },'delete');



                    break;                    
            }  

            return cMenu;
        }
    }

    await pluginAPI.loadStylesheets(['css/contextMenu.css'])

    pluginAPI.implement('ecoreTreeView.menus', new EcoreContextMenuProvider());
    pluginAPI.implement('editor.menus', new GraphObjectContextMenuProvider());
    pluginAPI.implement('editor.menus', new EditorCanvasContextMenuProvider());


    return true;
};
export var meta={"id":"contextMenu.ecore",description:"contextMenu provider for ecore eObjects","author":"Matthias Brunner","version":"0.1.0","requires":['eventBroker','contextMenu','plugin.ecoreTreeView','editor']};



