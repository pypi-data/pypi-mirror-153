import * as util from './js/util.js'

export async function init(pluginAPI) {      

    var contextMenu=pluginAPI.require('contextMenu');
    var iconProvider=pluginAPI.require('iconProvider');
    var EoqWorkspaceUtils=new util.EoqWorkspaceUtils(pluginAPI.getGlobal('app'));
    //prevent contextMenu.ecore from installing contextMenu to EOQ items
    class EOQFilter extends pluginAPI.getInterface('contextMenu.ecore.filters'){
        constructor(){
            super()
        }        
        select(eObject){
            if(eObject.eClass.eContainer.get("nsURI").includes("http://www.eoq.de/workspacemdbmodel/v1.0"))
            {
                return true;
            }
        }
    }
    pluginAPI.implement('contextMenu.ecore.filters', new EOQFilter());


    //register a context menu provider with ecoreTreeView, which will provide context menus for the EOQ items
    class EoqContextMenuProvider extends pluginAPI.getInterface('ecoreTreeView.menus'){
        constructor(){
            super();
        }

        isApplicableToNode(node)
        {
           
            if(node.data.eObject.eClass.eContainer.get("nsURI").includes("http://www.eoq.de/workspacemdbmodel/v1.0"))
            {
                switch(node.data.eObject.eClass.get("name"))
                {
                    case 'Workspace':            
                        return true
                    case 'Directory':
                        return true;
                    case 'ModelResource':
                        return true;
                    default:
                        return false;
                }      
            }
            return false;
        }

        getContextMenu(node)
        {
            var cMenu=false; 
            
            if(node.data.eObject.eClass.eContainer.get("nsURI").includes("http://www.eoq.de/workspacemdbmodel/v1.0"))
            {
                switch(node.data.eObject.eClass.get("name"))
                {
                    case 'Workspace':
                        cMenu=contextMenu.createContextMenu('eoq-context-menu','Eoq Context Menu',9999);

                        var creationMenu=contextMenu.createContextMenu('ecore-context-menu-sub-create','New',1,'add');
                        cMenu.addSubMenu('create',creationMenu);        
         
                        creationMenu.addNewEntry('create-dir','Directory',function(){
                            EoqWorkspaceUtils.createDirectory(node.data.eObject);
                        },'add')

                        break;
                    case 'Directory':
                        cMenu=contextMenu.createContextMenu('eoq-context-menu','Eoq Context Menu',9999);

                        var creationMenu=contextMenu.createContextMenu('ecore-context-menu-sub-create','New',1,'add');
                        cMenu.addSubMenu('create',creationMenu);        

                        creationMenu.addNewEntry('create-dir','Directory',function(){
                            EoqWorkspaceUtils.createDirectory(node.data.eObject);
                        },'add')

                        cMenu.addNewEntry('delete','Delete',function(){
                            EoqWorkspaceUtils.deleteDirectory(node.data.eObject);
                        },'delete');
                        break;
                    case 'ModelResource':
                        cMenu=contextMenu.createContextMenu('eoq-context-menu','Eoq Context Menu',9999);
                        cMenu.addNewEntry('delete','Delete',function(){
                            EoqWorkspaceUtils.deleteFile(node.data.eObject);
                        },'delete');
                        break;
                    default:
                        return false;
                }      
            }
            
        
            return cMenu;
        }
    }

    pluginAPI.implement('ecoreTreeView.menus', new EoqContextMenuProvider());


    pluginAPI.expose({util:EoqWorkspaceUtils});

    return true;
};
export var meta={"id":"contextMenu.eoq",description:"contextMenu provider for the EOQ workspace","author":"Matthias Brunner","version":"0.1.0","requires":['ecoreSync','contextMenu','contextMenu.ecore','plugin.ecoreTreeView']};



