import GraphController from './GraphController.js'
import VertexController from './VertexController.js'
import EdgeController from './EdgeController.js'
import ContainerController from './ContainerController.js'
import LabelController from './LabelController.js'
import QueryController from './QueryController.js'
import AnchorController from './AnchorController.js'
import DropReception from '../../interactions/DropReception.js'

// Graph Controller Factory
class GraphControllerFactory{
    constructor(graphModelFactory){
        this.graphModelFactory=graphModelFactory        
    }
    createGraphController(ecoreSync,repositoryURL,model,view,eObject){
        var self=this     
        var graphController=new GraphController(ecoreSync);

        var vertexControllers=model.get("displayableObjects").array().filter(function(e){ return e.eClass.get("name")=="Vertex"})
        var edgeControllers=model.get("displayableObjects").array().filter(function(e){ return e.eClass.get("name")=="Edge"})
        

        graphController.vertexControllers=vertexControllers.map(function(e){      
                return self.createVertexController(ecoreSync,graphController,e)   
        })   



        graphController.edgeControllers=edgeControllers.map(function(e){      
            return self.createEdgeController(ecoreSync,graphController,e)   
        })


        graphController.eObject=eObject;
        graphController.model=this.graphModelFactory.createModel(ecoreSync,model,eObject);
        graphController.view=view;

        graphController.interactions=model.get("interactions").array().map(function(interaction){
            var results=null;
            if(interaction.eClass.get("name")=="DropReception")
            {
                results=new DropReception(ecoreSync);
                results.nsURI=interaction.get("nsURI")
                results.className=interaction.get("className")
                results.dropItemNsURI=interaction.get("dropItemNsURI")
                results.dropItemClassName=interaction.get("dropItemClassName")
                results.modifiers={shiftPressed:interaction.get("shiftPressed"),ctrlPressed:interaction.get("ctrlPressed"),altPressed:interaction.get("altPressed")}
                results.cmdString=interaction.get("cmd")
                results.cmdDefinition=interaction.get("compoundCmd")
                results.controller=graphController;
            }
            return results;
        })
        view.graphController=graphController
        graphController.repositoryURL=repositoryURL
        return graphController     
    }

    createVertexController(ecoreSync,graphController,model){
      
        var self=this     
        var vertexController=new VertexController(ecoreSync,graphController);  
        var vertexControllers=model.get("subVertices").array()

        vertexController.vertexControllers=vertexControllers.filter(subVertex => {return subVertex.eClass.get('name')=='SubVertex'}).map(function(e){
            return self.createVertexController(ecoreSync,graphController,e);
        })         

        var edgeControllers=model.get("subEdges").array()
        vertexController.edgeControllers=edgeControllers.map(function(e){
            return self.createEdgeController(ecoreSync,graphController,e);
        })   

        vertexController.type=this.graphModelFactory.createVertexType(ecoreSync,model,graphController.repositoryURL,graphController.resourceProvider)
        vertexController.queryTarget=model.get("queryTarget");
        vertexController.queryStr=model.get("queryStr")
        vertexController.queryTargetAlias=model.get("queryTargetAlias")    
        vertexController.alias=model.get("alias")    

        var labelControllers=model.get("labels").array()
        vertexController.labelControllers=labelControllers.map(function(e){
            return self.createLabelController(ecoreSync,graphController,e);
        });

        return vertexController        
    }

    createLabelController(ecoreSync,graphController,model,eObject){
        var self=this     
        var labelController=new LabelController(ecoreSync,graphController);  
        labelController.type=this.graphModelFactory.createLabelType(ecoreSync,model)
        labelController.eObject=eObject;  
        return labelController        
    }

    createQueryController(model)
    { 
        throw 'deprecated fucntion call'
        /* A generic query controller, that initially executes the query and listens on changes */
        /* TODO: Should be used by every querying controller, to reduce redundant code */
        var self=this;
        var queryController=new QueryController(model.get("queryTarget"),model.get("queryTargetAlias"),model.get("queryStr"),model.get("alias"));
        if(model.get("subQueries") && model.get("subQueries").array().length)
        {
            queryController.queryControllers=model.get("subQueries").array().map(function(e){
                return createQueryController(e);
            })            
        }
        return queryController;
    }

    createEdgeController(ecoreSync,graphController,model){
        var self=this
        var edgeController=new EdgeController(ecoreSync,graphController);
        var containerControllers=model.get("containers").array()
        edgeController.containerControllers=containerControllers.map(function(e){
            return self.createContainerController(ecoreSync,graphController,e);
        })

        var anchorControllers=model.get("anchors").array()
        edgeController.anchorControllers=anchorControllers.map(function(e){
            return self.createAnchorController(ecoreSync,graphController,e);
        })
        
        edgeController.type=this.graphModelFactory.createEdgeType(ecoreSync,model)
        edgeController.queryTarget=model.get("queryTarget");
        edgeController.queryStr=model.get("queryStr")
        edgeController.queryTargetAlias=model.get("queryTargetAlias")

        return edgeController
    }

    createContainerController(ecoreSync,graphController,model){
        var self=this;
        var containerController=new ContainerController(ecoreSync,graphController)
        var vertexControllers=model.get("subVertices").array()
        containerController.vertexControllers=vertexControllers.map(function(e){
            return self.createVertexController(ecoreSync,graphController,e);
        }) 
        containerController.type=this.graphModelFactory.createContainerType(ecoreSync,model)
        return containerController 
    }

    createAnchorController(ecoreSync,graphController,model){
        var self=this;
        var anchorController=new AnchorController(ecoreSync,graphController)
        anchorController.type=this.graphModelFactory.createAnchorType(ecoreSync,model);
        anchorController.queryTarget=model.get("queryTarget");
        anchorController.queryStr=model.get("queryStr")
        anchorController.queryTargetAlias=model.get("queryTargetAlias")
        return anchorController 
    }

}

export default GraphControllerFactory