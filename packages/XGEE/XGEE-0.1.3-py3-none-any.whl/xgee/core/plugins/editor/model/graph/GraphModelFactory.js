/* Factory Class for Graph Model Objects */

import GraphResourceProvider from '../../graph/GraphResourceProvider.js'
import GraphModel from './GraphModel.js'

//GraphObjects
import Vertex from './Vertex.js'
import VertexType from './VertexType.js'
import StaticVertex from './StaticVertex.js'
import StaticVertexType from './StaticVertexType.js'

import Container from './Container.js'
import ContainerType from './ContainerType.js'

import Edge from './Edge.js'
import EdgeType from './EdgeType.js'


import Anchor from './Anchor.js'
import AnchorType from './AnchorType.js'


import FloatingLabel from './FloatingLabel.js'
import NestedLabel from './NestedLabel.js'
import LabelType from './LabelType.js'

import LabelSegment from './LabelSegment.js'
import LabelSegmentType from './LabelSegmentType.js'

//Managers
import GraphModelManager from './GraphModelManager.js'

import GraphLayoutManager from './GraphLayoutManager.js'

import VertexManager from './VertexManager.js'
import StaticVertexManager from './StaticVertexManager.js'
import ContainerManager from './ContainerManager.js'

import EdgeManager from './EdgeManager.js'

import AnchorManager from './AnchorManager.js'

import LabelManager from './LabelManager.js'
import LabelSegmentManager from './LabelSegmentManager.js'


class GraphModelFactory{
    constructor(repositoryURL){
        this.resourceProvider = new GraphResourceProvider(repositoryURL);
    }

    _getEditorModel(model)
    {
        var lvl=model
        while(lvl.eClass.get("name")!="Editor")
        {
            lvl=lvl.eContainer
            if(!lvl) break;
        }
        return lvl
    }

    _getRepositoryURL(model)
    {
        var url=''
        var editorModel=this._getEditorModel(model)
        if(editorModel)
        {
            url=editorModel.get("repositoryURL")
        }
        return url
    }

    createModel(ecoreSync,model,eObject){
        var graphModel=new GraphModel();
        graphModel.eObject=eObject;
        graphModel.layout=new GraphLayoutManager(eObject);
        graphModel.graphObjectDefinitions=model;       
        graphModel.manager=this.createModelManager(ecoreSync,graphModel,model);  
        return graphModel
    }

    createModelManager(ecoreSync,model,modelDefinition)
    {
        var self=this;
        var graphModelManager=new GraphModelManager(this,ecoreSync,model,this.resourceProvider);

        var initVertexManager=function(graphModelFactory,ecoreSync,model,parentManager,v)
        {
            let vertexType=self.createVertexType(ecoreSync,v);
            let vertexManager=self.createVertexManager(graphModelFactory,ecoreSync,vertexType,model);
            parentManager.subManagers.push(vertexManager);
            let subVertices=v.get("subVertices").array();
            subVertices.filter(subVertex => {return subVertex.eClass.get('name')=='SubVertex'}).forEach(function(v){
               initVertexManager(graphModelFactory,ecoreSync,model,vertexManager,v)
            })

            subVertices.filter(subVertex => {return subVertex.eClass.get('name')=='StaticSubVertex'}).forEach(function(v){
                initStaticVertexManager(graphModelFactory,ecoreSync,model,vertexManager,v)
            })

            let subEdges=v.get("subEdges").array();
            subEdges.forEach(function(e){
                initEdgeManager(graphModelFactory,ecoreSync,model,vertexManager,e)
            })

            let labels=v.get("labels").array();
            labels.forEach(function(lbl){
                initLabelManager(graphModelFactory,ecoreSync,model,vertexManager,lbl)
            })
        }

        var initEdgeManager=function(graphModelFactory,ecoreSync,model,parentManager,e)
        {
            let edgeType=self.createEdgeType(ecoreSync,e);
            let edgeManager=self.createEdgeManager(graphModelFactory,ecoreSync,edgeType,model);
            parentManager.subManagers.push(edgeManager);

            let anchors=e.get("anchors").array();
            anchors.forEach(function(e){
                initAnchorManager(graphModelFactory,ecoreSync,model,edgeManager,e)
            })

            let containers=e.get("containers").array();
            containers.forEach(function(e){
                initContainerManager(graphModelFactory,ecoreSync,model,edgeManager,e);
            });
        }        

        var initAnchorManager=function(graphModelFactory,ecoreSync,model,parentManager,e)
        {
            let anchorType=self.createAnchorType(ecoreSync,e);
            let anchorManager=self.createAnchorManager(graphModelFactory,ecoreSync,anchorType,model);
            parentManager.subManagers.push(anchorManager);
        }        

        var initContainerManager=function(graphModelFactory,ecoreSync,model,parentManager,e)
        {
            let containerType=self.createContainerType(ecoreSync,e);
            let containerManager=self.createContainerManager(graphModelFactory,ecoreSync,containerType,model);                

            let subVertices=e.get("subVertices").array();
            subVertices.forEach(function(v){
               initVertexManager(graphModelFactory,ecoreSync,model,containerManager,v)
            })

            parentManager.subManagers.push(containerManager);     
        }     


        var initStaticVertexManager=function(graphModelFactory,ecoreSync,model,parentManager,sv)
        {
            let staticVertexType=self.createStaticVertexType(ecoreSync,sv);
            let staticVertexManager=self.createStaticVertexManager(graphModelFactory,ecoreSync,staticVertexType,model); 
            parentManager.subManagers.push(staticVertexManager);     

            let labels=sv.get("labels").array();
            labels.forEach(function(lbl){
                initLabelManager(graphModelFactory,ecoreSync,model,staticVertexManager,lbl)
            })
        }   

        var initLabelManager=function(graphModelFactory,ecoreSync,model,parentManager,lbl)
        {
            let labelType=self.createLabelType(ecoreSync,lbl);
            let labelManager=self.createLabelManager(graphModelFactory,ecoreSync,labelType,model);

            let segments=lbl.get("segments").array();

            segments.forEach(function(s){
                initLabelSegmentManager(graphModelFactory,ecoreSync,model,labelManager,s)
            });

            parentManager.subManagers.push(labelManager);
        }   
        
        var initLabelSegmentManager=function(graphModelFactory,ecoreSync,model,parentManager,segment)
        {
            let segmentType=self.createLabelSegmentType(ecoreSync,segment);
            let labelSegmentManager=self.createLabelSegmentManager(graphModelFactory,ecoreSync,segmentType,model);
            parentManager.subManagers.push(labelSegmentManager);
        }    


        //Toplevel Vertices and Edges
        var vertices=modelDefinition.get("displayableObjects").array().filter(function(e){ return e.eClass.get("name")=="Vertex" });
        var staticVertices=modelDefinition.get("displayableObjects").array().filter(function(e){ return e.eClass.get("name")=="StaticVertex" });

        var edges=modelDefinition.get("displayableObjects").array().filter(function(e){ return e.eClass.get("name")=="Edge"});

        vertices.forEach(function(v){            
            initVertexManager(self,ecoreSync,model,graphModelManager,v)            
        })

        staticVertices.forEach(function(v){         
            initStaticVertexManager(self,ecoreSync,model,graphModelManager,v)            
        })

        edges.forEach(function(e){
            initEdgeManager(self,ecoreSync,model,graphModelManager,e)   
        }) 

        return graphModelManager
    }

    createVertexManager(graphModelFactory,ecoreSync,type,model)
    {
        var vertexManager=new VertexManager(graphModelFactory,ecoreSync,type,model,this.resourceProvider)
        return vertexManager
    }

    createStaticVertexManager(graphModelFactory,ecoreSync,type,model)
    {
        var vertexManager=new StaticVertexManager(graphModelFactory,ecoreSync,type,model,this.resourceProvider)
        return vertexManager
    }

    createLabelManager(graphModelFactory,ecoreSync,type,model)
    {
        var labelManager=new LabelManager(graphModelFactory,ecoreSync,type,model,this.resourceProvider)
        return labelManager
    }

    createLabelSegmentManager(ecoreSync,type,model)
    {
        var labelSegmentManager=new LabelSegmentManager(ecoreSync,type,model,this.resourceProvider)
        return labelSegmentManager
    }


    createEdgeManager(graphModelFactory,ecoreSync,type,model)
    {
        var edgeManager=new EdgeManager(graphModelFactory,ecoreSync,type,model,this.resourceProvider)
        return edgeManager
    }

    createAnchorManager(graphModelFactory,ecoreSync,type,model)
    {
        var anchorManager=new AnchorManager(graphModelFactory,ecoreSync,type,model,this.resourceProvider)
        return anchorManager
    }
    
    createVertexType(ecoreSync,model){
        var vertexType=new VertexType(ecoreSync,model)
        vertexType.shape=this.resourceProvider.LoadResource(model.get("shape").get("filepath"))
        return vertexType;
    }

    createStaticVertexType(ecoreSync,model){
        var staticVertexType=new StaticVertexType(ecoreSync,model)
        staticVertexType.shape=this.resourceProvider.LoadResource(model.get("shape").get("filepath"))
        return staticVertexType;
    }

    createVertex(graphModel,type,eObject){
        var vertex=new Vertex(graphModel)
        vertex.eObject=eObject;       
        vertex.type=type;
        vertex.init();
        return vertex
    }

    createStaticVertex(graphModel,type,eObject){
        var staticVertex=new StaticVertex(graphModel)
        staticVertex.eObject=eObject;
        staticVertex.type=type;
        staticVertex.init()
        return staticVertex;
    }

    createEdgeType(ecoreSync,model){
        return new EdgeType(ecoreSync,model)
    }    

    createEdge(graphModel,type,eObject){
        var edge= new Edge(graphModel)
        edge.eObject=eObject;
        edge.type=type;
        edge.init();
        return edge
    }

    createLabelType(ecoreSync,model){
        return new LabelType(ecoreSync,model);
    }

    createLabel(type){
        var label=null

        switch(type.model.eClass.get('name'))
        {
            case 'FloatingLabel':
                label=new FloatingLabel()
                break;
            case 'NestedLabel':
                label=new NestedLabel()
                break;
            default:
                label=null
        }
        
        label.type=type;
        label.content='';
        let offsetX=Number.parseInt(type.model.get("labelOffsetX"));
        let offsetY=Number.parseInt(type.model.get("labelOffsetY"));
        if(Number.isNaN(offsetX)) offsetX=0
        if(Number.isNaN(offsetY)) offsetY=0
        label.offset={x:offsetX,y:offsetY}
        label.align=type.model.get("labelAlignment")
        if(!label.align) label.align='CENTER'
        label.vAlign=type.model.get("labelVerticalAligment")
        if(!label.vAlign) label.vAlign='CENTER'
        label.anchor=type.model.get("anchor")
        if(!label.anchor) label.anchor='CENTER'
        label.rotation=type.model.get("labelRotation")
        if(Number.isNaN(label.rotation)) label.rotation=0.0
        return label;
    }

    createLabelSegmentType(ecoreSync,model){
        return new LabelSegmentType(ecoreSync,model);
    }

    createLabelSegment(type){
        var labelSegment=new LabelSegment();
        labelSegment.type=type;
        labelSegment.content='';
        return labelSegment
    }

    createContainerType(ecoreSync,model){
        var containerType=new ContainerType(ecoreSync,model)
        containerType.shape=this.resourceProvider.LoadResource(model.get("shape").get("filepath"))
        return containerType;
    }

    createContainer(graphModel,type,eObject){
        var container=new Container(graphModel)
        container.eObject=eObject;
        container.type=type;
        container.init()
        return container;
    }


    createContainerManager(graphModelFactory,ecoreSync,type,model)
    {
        var containerManager=new ContainerManager(graphModelFactory,ecoreSync,type,model,this.resourceProvider)
        return containerManager
    }


    createAnchorType(ecoreSync,model){
        return new AnchorType(ecoreSync,model)
    }

    createAnchor(graphModel,type,eObject){
        var anchor=new Anchor(graphModel)
        anchor.eObject=eObject;
        anchor.type=type;
        return anchor;
    }
}

export default GraphModelFactory

