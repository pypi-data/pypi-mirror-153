//XGEE API
//(C) 2020 Matthias Brunner

import * as jsaIntegation from './libjsa.js'
import GraphModelFactory from '../model/graph/GraphModelFactory.js'
import GraphConrollerFactory from '../controllers/graph/GraphControllerFactory.js'
import PaletteController from '../controllers/palette/PaletteController.js'
import GraphView from '../view/GraphView.js'
import Vertex from '../model/graph/Vertex.js'
import Edge from '../model/graph/Edge.js'
import Container from '../model/graph/Container.js'
import Label from '../model/graph/Label.js'
import UUID from './uuid.js'
import XGEEPresentationModel from '../model/PresentationModel.js'

var classMap={};
var editorResourceSet=null;
var editorTabs=[];
var editorRegistry=[]; 
var metaModel=null;
var app=null;

class XGEEInstance{
    constructor(ecoreSync,pathToEditorModel,editorModel,eObject,editorDOM,outlineDOM,paletteDOM){
        
        this.ecoreSync=ecoreSync;

        let repositoryURL=pathToEditorModel+editorModel.get("repositoryURL")
        this.repositoryURL=repositoryURL

        //Create graph view
        this.graphView=new GraphView(editorDOM,outlineDOM);

        //Factories
        this.graphModelFactory=new GraphModelFactory(repositoryURL)
        this.graphControllerFactory=new GraphConrollerFactory(this.graphModelFactory)     
          
        //Create controllers
        this.graphController=this.graphControllerFactory.createGraphController(ecoreSync,repositoryURL,editorModel,this.graphView,eObject);
        this.paletteController=new PaletteController(ecoreSync,repositoryURL,editorModel.get("palette"),eObject,paletteDOM,this.graphController)

        //Initialize graph
        this.graphController.init(this.paletteController);

        //Initialize palette
        this.paletteController.init()
    }

    getGraphModel(){
        return this.graphController.model
    }

    getGraphView(){
        return this.graphView
    }

    getGraphController(){
        return this.graphController
    }

    getPaletteModel(){
        return this.paletteController.model
    }

    getPaletteView(){
        return this.paletteController.view
    }

    getPaletteController(){
        return this.paletteController
    }

    getPaletteController(){
        return this.paletteController
    }

    getGraph(){
        return this.graphView.graph
    }
}


export class XGEEPrivateAPI{
    constructor(pluginAPI){
        this.pluginAPI=pluginAPI
    }

    addClass(nsURI,name)
    {
        classes.push({nsURI:nsURI,name:name});
    }

    removeClass(nsURI,name)
    {
        var rmClass=classes.find(function(e){
            return e.nsURI==nsURI && e.name==name;
        });

        if(rmClass)
        {               
            if(classes.indexOf(rmClass)!=-1)
            {
                classes.splice(classes.indexOf(rmClass),1);
            }
        }
    }
    
    setEditorRegistry(editors)
    {   
        editorRegistry=editors;
    }

    getEditorRegistry()
    {
        return editorRegistry;
    }

    getClassMap()
    {
        return classMap;
    }

    async registerEditorFromModelPath(modelPath)
    { 

        var commonPath=function(path1,path2)
        {
            var pth1=path1.split("/")
            var pth2=path2.split("/")

            var minLength=Math.min(pth1.length,pth2.length)
            let i=0
            while(i<minLength && pth1[i]==pth2[i])
            {
                i++;
            }

            let pth=pth1.slice(0,i).join("/")
            if(pth.length && pth.slice(-1) !="/" )
            {
                pth+='/'
            }

            return pth
        }

        if(modelPath)
        { 
           
            let pathToRoot=''
            let common=commonPath(this.pluginAPI.getPath(),modelPath)
            let splitPath=this.pluginAPI.getPath().replace(common,'').split("/")
            let pathDepth=splitPath.length - 2
    
            if(splitPath[0]=='.')
            {
                pathDepth-=1
            }
    
            for(let i=0;i<=pathDepth;i++)
            {
                pathToRoot+='../'
            }
            
            let pathToModelResource=pathToRoot+modelPath.replace(common,'')           
            let results=await this.pluginAPI.loadXMLResources([pathToModelResource])               
            let uuid=new UUID.v4
            let model=editorResourceSet.create({ uri: uuid.toString() });        
            model.parse(results[0].txt,Ecore.XMI)

            //Relative to index.html
            let pathSegmentsToModel=modelPath.split('/')   
            let pathToModel=pathSegmentsToModel.slice(0,pathSegmentsToModel.length-1).join('/')+'/'    
            this.registerEditor(new XGEEPresentationModel(pathToModel,model.get('contents').array()[0]))
        }
    }

    registerEditor(editor)
    {
        if(editor)
        {           
            editorRegistry.push(editor);

            var refersTo=editor.getModel().get('refersTo').array();
            refersTo.forEach(function(reference){

                var nsURI=reference.get('refNsURI');
                var name=reference.get('refClassname');

                if(classMap[nsURI]){
                    if(classMap[nsURI][name])
                    {
                        classMap[nsURI][name].push(editor);
                    }
                    else
                    {
                        classMap[nsURI][name]=[];
                        classMap[nsURI][name].push(editor);
                    }
                }
                else
                {
                    classMap[nsURI]={};
                    classMap[nsURI][name]=[];
                    classMap[nsURI][name].push(editor);
                }
            });
        }
    }

    unregisterEditor(editor)
    {
        if(editorRegistry.indexOf(editor)!=-1)
        {
            editorRegistry.splice(editorRegistry.indexOf(editor),1);
        }
    }
   
    setResourceSet(resourceSet){
        editorResourceSet=resourceSet;
    }

    setMetaModel(metaModel)
    {
        metaModel=metaModel;
    }

    setApplication(application){
        app=application;
    }

}


export class XGEEPublicAPI{
    constructor(){

    }

    open(eObject,activate=false,editorIdx=0)
    {
        //opens a jsApplication tab containing the editor, returns the graphView if the operation succeeded
        var res=null;
        if(this.canOpen(eObject))
        {
            var presentationModel=this.getEditors(eObject)[editorIdx]

            var editorModel=presentationModel.getModel()
            var objectId = ecoreSync.rlookup(eObject);
            var editorInstanceId = "edit"+objectId;
            var editorName = editorModel.get('name');
            var name = editorName+" ([#"+objectId+"])";
            var editorId = editorModel.get("id");

            var tab = app.viewManager.GetChildById(editorInstanceId);
            if(!tab)
            {
                tab=new jsaIntegation.EditorTab({
                    id: editorInstanceId,
                    name: name,
                    icon: presentationModel.getPath()+'/'+editorModel.get('repositoryURL')+editorModel.get('icon'),
                    editor: presentationModel,
                    eObject: eObject,
                    ecoreSync: ecoreSync,
                    style: ['jsa-view','xgee-graph-view','xgee-graph-view-'+editorId],
                    containerStyle: ['jsa-view-container','xgee-graph-view-container','xgee-graph-view-container-'+editorId],
                    hasHeader: true,
                    isClosable: true
                });

                
                app.viewManager.AddChild(tab);
            }


            if(activate) {
                app.commandManager.Execute(new jsa.ChangeViewCommand(app.viewManager,tab));
            }

            editorTabs.push(tab);
            res=tab;
        }

        return res;
    }

    canOpen(eObject)
    {
        var res=false;
        var nsURI=eObject.eClass.eContainer.get("nsURI");
        var name=eObject.eClass.get("name");

        if(classMap[nsURI])
        {
            if(classMap[nsURI][name])
            {
                if(Array.isArray(classMap[nsURI][name]))
                {
                    res=true;
                }
            }
        }
       
        return res
    }

    getEditors(eObject)
    {
        var res=[];
        var nsURI=eObject.eClass.eContainer.get("nsURI");
        var name=eObject.eClass.get("name");

        if(classMap[nsURI])
        {
            if(classMap[nsURI][name])
            {
                if(Array.isArray(classMap[nsURI][name]))
                {
                    res=classMap[nsURI][name];
                }
            }
        }
       
        return res
    }

    initializeEditor(ecoreSync,presentationModel,eObject,editorDOM,outlineDOM,paletteDOM)
    {
       return new XGEEInstance(ecoreSync,presentationModel.getPath(),presentationModel.getModel(),eObject,editorDOM,outlineDOM,paletteDOM)
    }

    listClassNames(){
        //List the names of the classes that can be edited
        var res=[];
        for(let nsURI in classMap)
        {
            for(let name in classMap[nsURI])
            {
                res.push(name);
            }
        }
        return res;
    }

    isOpen(eObject)
    {

    }
    
    close(eObject)
    {

    }

    closeAll(){

    }

    getResourceSet(){
        return editorResourceSet;
    }

    getMetaModel(){
        return metaModel
    }

    isGraphObjectType(obj,type)
    {
        let res=false;
        switch(type)
        {
            case 'Vertex':
                res=(obj instanceof Vertex)
                break;
            case 'Edge':
                res=(obj instanceof Edge)
                break;
            case 'Container':
                res=(obj instanceof Container)
                break;
            case 'Label':
                res=(obj instanceof Label)
                break;
            default:
                break;
        }
        return res;
    }

}




