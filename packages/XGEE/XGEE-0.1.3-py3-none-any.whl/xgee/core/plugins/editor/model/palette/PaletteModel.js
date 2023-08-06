import GraphEvent from '../../model/graph/GraphEvent.js'
import GraphResourceProvider from '../../graph/GraphResourceProvider.js'
import DragAndDropTool from './DragAndDropTool.js'
import EdgeRoutingTool from './EdgeRoutingTool.js'
import ToolGenerator from './ToolGenerator.js'
import SelectionTool from './SelectionTool.js';

export default class PaletteModel{
    constructor(ecoreSync,repositoryURL,controller,paletteDefinition,graphController){
        this.ecoreSync=ecoreSync;
        this.controller=controller;
        this.graphController=graphController;
        this.categories=[];
        this.events={};
        this.paletteDefinition=paletteDefinition;
        this.events["PALETTE_CHANGED"]=new GraphEvent(false);
        this.resourceProvider = new GraphResourceProvider(repositoryURL);
    }   

    async init(){
        var self=this;       
        if(this.paletteDefinition){
            let cats=this.paletteDefinition.get("categories").array();
            var initializations=[];
            cats.forEach(function(cat){
                let paletteCategory=new PaletteCategory(self.ecoreSync,self.resourceProvider,self,cat)
                initializations.push(paletteCategory.init());
                self.addCategory(paletteCategory);
            })
            await Promise.all(initializations)
            this.events["PALETTE_CHANGED"].enable();
        }

        this.invalidate();
    }

    addCategory(category){
        this.categories.push(category);
    }

    removeCategory(category){
        var idx=this.tools.indexOf(category);
        if(idx>-1){
            this.tools.splice(idx,1)
        }
    }

    invalidate(){
        this.events["PALETTE_CHANGED"].raise();
    }

}


class PaletteCategory{
    constructor(ecoreSync,resourceProvider,palette,categoryDefinition){
        this.ecoreSync=ecoreSync;
        this.resourceProvider=resourceProvider
        this.tools=[];
        this.toolGenerators=[];
        this.categoryDefinition=categoryDefinition;
        this.palette=palette;
    }   

    async init(){
        var self=this;
        let tools=this.categoryDefinition.get("tools").array();
        for(let i in tools)
        {
            let graphTool=null;
            if(tools[i].eClass.get("name")=="DragAndDrop")
            {
                graphTool=new DragAndDropTool(self.ecoreSync,self.resourceProvider,tools[i],self.palette)
                graphTool.init();
                self.addTool(graphTool);
            }

            if(tools[i].eClass.get("name")=="EdgeRouting")
            {
                graphTool=new EdgeRoutingTool(self.ecoreSync,self.resourceProvider,tools[i],self.palette)
                graphTool.init();
                self.addTool(graphTool);
            }      
            
            if(tools[i].eClass.get("name")=="SelectionTool")
            {
                graphTool=new SelectionTool(self.ecoreSync,self.resourceProvider,tools[i],self.palette)
                graphTool.init();
                self.addTool(graphTool);
            }  
        }

        try{
            let toolGenerators=this.categoryDefinition.get("toolGenerators").array();

            //Tool Generator initialization and tool generation
                for(let i in toolGenerators)
                {
                    var toolGen=new ToolGenerator(self.ecoreSync,toolGenerators[i],self); //toolgen init
                    var generatedTools=await toolGen.generate(); //generate the tools     
                    toolGen.observe(function(toolReplacements,addedTools,removedTools){

                        removedTools.forEach(function(tool){
                            var t=self.findTool(tool)
                            if(t){ self.removeTool(t); }
                        });

                        addedTools.forEach(function(tool){
                            let graphTool=null;
                            try{                            
                                if(tool.eClass.get("name")=="DragAndDrop")
                                {
                                    graphTool=new DragAndDropTool(self.ecoreSync,self.resourceProvider,tool,self.palette)
                                    graphTool.init();     
                                    self.addTool(graphTool);                       
                                }
                    
                                if(tool.eClass.get("name")=="EdgeRouting")
                                {
                                    graphTool=new EdgeRoutingTool(self.ecoreSync,self.resourceProvider,tool,self.palette)
                                    graphTool.init();     
                                    self.addTool(graphTool);                         
                                } 
                            }
                            catch(e){
                                console.error('tool initialization failed:' +e);
                            }                           
                        });

                        toolReplacements.forEach(function(toolReplacement){
                            let graphTool=null;
                            var t=self.findToolByToolDefinition(toolReplacement.old)
                            if(t)
                            {                        
                                let tool=toolReplacement.new

                                if(tool.eClass.get("name")=="DragAndDrop")
                                {
                                    graphTool=new DragAndDropTool(self.ecoreSync,self.resourceProvider,tool,self.palette)
                                    graphTool.init();     
                                    self.replaceTool(t,graphTool);                       
                                }
                    
                                if(tool.eClass.get("name")=="EdgeRouting")
                                {
                                    graphTool=new EdgeRoutingTool(self.ecoreSync,self.resourceProvider,tool,self.palette)
                                    graphTool.init();     
                                    self.replaceTool(t,graphTool);                         
                                }                     
                            }
                            else
                            {
                                console.warn('The specified tool was not found during tool replacement.')
                            }
                        })

                    });
                    
                    //initialize the generated tools
                    generatedTools.forEach(function(tool){
                        let graphTool=null;
                        try{
                            
                            if(tool.eClass.get("name")=="DragAndDrop")
                            {
                                graphTool=new DragAndDropTool(self.ecoreSync,self.resourceProvider,tool,self.palette)
                                graphTool.init();     
                                self.addTool(graphTool);                       
                            }
                
                            if(tool.eClass.get("name")=="EdgeRouting")
                            {
                                graphTool=new EdgeRoutingTool(self.ecoreSync,self.resourceProvider,tool,self.palette)
                                graphTool.init();     
                                self.addTool(graphTool);                         
                            } 
                        }
                        catch(e){
                            console.error('tool initialization failed:' +e);
                        }                           
                    });


                                        
                    this.toolGenerators.push(toolGen)
                }
            }
        catch(e)
        {
            console.error('tool generation failed: '+e)
        }


    }

    getName(){
        return this.categoryDefinition.get("name")
    }

    replaceTool(oldTool,newTool)
    {
        let pos=this.tools.indexOf(oldTool)
        if (pos != -1){
            this.tools[pos]=newTool
        }
        this.palette.invalidate();
    }

    addTool(tool){
        this.tools.push(tool);
        this.palette.invalidate();
    }

    removeTool(tool){
        var idx=this.tools.indexOf(tool);
        if(idx>-1){
            this.tools.splice(idx,1);
        }
        this.palette.invalidate();
    } 

    findToolByToolDefinition(toolDef)
    {
        let res=null
        res=this.tools.find(function(tool){
            return tool.toolDefinition == toolDef
        })
        return res
    }

    findTool(toolDef){
        return this.tools.find(function(tool){
            return tool.toolDefinition.get("id") == toolDef.get("id")
        })
    }
}


