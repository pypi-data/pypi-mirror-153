import * as contextMenus from './extensions/EditorContextMenuProvider.js'
import {XGEEPublicAPI, XGEEPrivateAPI} from './lib/libapi.js'
import * as mxGraphIntegration from './graph/mxGraphIntegration.js' //sets global mxGraph variables and overwrites mxGraph functions

import GraphViewMenu from './view/GraphViewMenu.js'


import { serialPromise } from './lib/libaux.js'
//Editor main plugin 

export async function init(pluginAPI) {      
    
    
    var contextMenu=pluginAPI.require('contextMenu');
    var eventBroker=pluginAPI.require('eventBroker');
    var editorResourceSet = Ecore.ResourceSet.create();
    
    //Read meta model
    try{
        let xmlResources=await pluginAPI.loadXMLResources(["model/editorModel.ecore"]) 
        var metaModel=xmlResources[0];             
        var metaModelResource = editorResourceSet.create({ uri: 'EditorModels' });             
        metaModelResource.parse(metaModel.txt,Ecore.XMI); 
        Ecore.EPackage.Registry.register(metaModelResource.get("contents").array()[0])
    }
    catch(e)
    {
        throw 'XGEE meta-model initialization failed: '+e
    }    

   

    // Initialize API
    var privateAPI=new XGEEPrivateAPI(pluginAPI);
    privateAPI.setResourceSet(editorResourceSet);
    privateAPI.setMetaModel(metaModel);
    privateAPI.setApplication(pluginAPI.getGlobal('app'));

    var publicAPI=new XGEEPublicAPI();

    //Compatibility hack (TODO: remove these global functions)
    window["serialPromise"]=serialPromise

  
    let stylesSheets=await pluginAPI.loadStylesheets(["css/loading.css", "css/xgeeJsaIntegration.css"]);



        var editorRegistry=[]; 
        var editorContextMenuRegistry=[];
    
        var editorModels=pluginAPI.provide('xgee.models',null,function(event){
                ///register editor
                 privateAPI.registerEditorFromModelPath(event.extension.modelPath);
        });
        


        //automatically provide edit entries for editable objects
        class EditorGenericMenuProvider extends pluginAPI.getInterface('ecoreTreeView.menus'){
            constructor(){
                super();
            }

            isApplicableToNode(node)
            {
                return publicAPI.canOpen(node.data.eObject);
            }

            getContextMenu(node)
            {
                var cMenu=false;
                if(publicAPI.canOpen(node.data.eObject))
                {
                    
                    cMenu=contextMenu.createContextMenu('xgee-context-menu','XGEE Context Menu',100);
                    var editors=publicAPI.getEditors(node.data.eObject);

                    if(editors.length==1)
                    {
                        cMenu.addNewEntry('xgee-edit','Edit',function(){
                            publicAPI.open(node.data.eObject,true);
                        },'edit')
                    } else if(editors.length>1)
                    {
                        var editMenu=contextMenu.createContextMenu('xgee-edit-with-submenu','Edit with...',100,'edit');
                        editors.forEach(function(editor,i){
                            editMenu.addNewEntry('xgee-edit-'+i,editor.get('name'),function(){
                                publicAPI.open(node.data.eObject,true,i);
                            },'edit')
                        });
                        cMenu.addSubMenu('xgee-edit-with',editMenu);    
                    }
                }
                return cMenu;
            }

        }
        pluginAPI.implement('ecoreTreeView.menus',new EditorGenericMenuProvider());
            
        
        var menuProviders=[];

        //Built-In XGEE Menu Entries
        menuProviders.push(new GraphViewMenu(contextMenu))


        pluginAPI.provide('editor.menus',contextMenus.EditorContextMenuProvider,function(event){
           menuProviders.push(event.extension);
        });
        

        
        //the eventBroker should be avoided in the future for this functionality, but for the moment this shall suffice
        eventBroker.subscribe('XGEE/CONTEXTMENU',function(evt){
            var applicableMenuProviders=menuProviders.filter(function(p){
                return p.isApplicableToTarget(evt.data.target);
            });
            if(applicableMenuProviders.length > 0)
            {
                contextMenu.showContextMenu({x:evt.data.event.pageX,y:evt.data.event.pageY},contextMenu.util.collectAndMerge(applicableMenuProviders,evt.data.target));        
            }                       
        });

        pluginAPI.expose(publicAPI); 
      
        return true;       

};

export var meta={
    "id":"editor",
    "description":"A model-based Graphical Editor for Ecore Models",
    "author":"Matthias Brunner",
    "version":"0.1.0",
    "requires":["ecore","ecoreSync",'eventBroker',"plugin.ecoreTreeView",'contextMenu']
};



