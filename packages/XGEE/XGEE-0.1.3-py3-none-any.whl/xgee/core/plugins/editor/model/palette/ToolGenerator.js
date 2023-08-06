import Query from '../../queries/Query.js'
import { ecoreLocalClone, replaceTemplates } from '../../lib/libaux.js'

export default class ToolGenerator{

    constructor(ecoreSync,definition,paletteCategory)
    {
        this.ecoreSync=ecoreSync; //the ecoreSync instance used by this object
        this.definition=definition; // the definition of this tool generator
        this.paletteCategory=paletteCategory; //the category in which this tool generator is included
        this.generatedTools={}

        this.toolUpdateListeners=[]
    }
    

    getAllToolDefinitions(){
        let tools=[]
        for( let tool in this.generatedTools){
            tools.push(this.generatedTools['toolDefinition'])
        }
        return tools
    }

    async __generateToolDefinitions(QueryObj,valueSet,results)
    {       

        let self=this;
        var toolDefinitions=[]
        let valueSets=await QueryObj.makeValueSets(valueSet,results);
        let observerTokens=[]
        let ts=new eoq2.serialization.TextSerializer();
        for(let idx in results)
        {
            let toolDef=null
            try{                               
                toolDef=ecoreLocalClone(this.definition.get("tool"))
               
                var toolGenCmd=new eoq2.Cmp();
                let toolGenCmds=this.definition.get("toolGenCmd").get("cmds").array();  
                let resultAliases=[];   
      

                let toolObserverQueries=[] // observable queries in the toolGenCmd
                let toolObserverAliases=[] // the aliases associated with the observable queries

                toolGenCmds.forEach(function(cmd){
                    try{          
                        let cmdStr=cmd.get("cmdStr");
                        cmdStr=replaceTemplates(valueSets[idx],cmdStr);                      
                        let addCmd = ts.deserialize(cmdStr);
                        toolGenCmd.a.push(addCmd);
                        // eval('toolGenCmd.'+cmdStr);    
            
                        if (typeof(cmdStr) == 'string' && cmdStr.substr(0,3) == 'GET'){                
                            let qry=replaceTemplates(valueSets[idx],cmdStr.substr(4))
                            let addCmdQry = ts.deserialize(qry);
                            toolObserverQueries.push(addCmdQry)
                            // toolObserverQueries.push(eval(qry))
                            toolObserverAliases.push(cmd.get("alias"))
                        }
                   
                        resultAliases.push(cmd.get("alias"));
                    }
                    catch(e)
                    {
                        console.error('tool generator cmd failed: '+e,'cmd:'+cmd.get("cmdStr"));
                        throw e
                    }
                })                

                
                var res=await this.ecoreSync.exec(toolGenCmd);              

                res.forEach(function(result,i){
                    valueSets[idx][resultAliases[i]]=result;
                });
                
                self.__generateToolDefinition(toolDef,valueSets[idx])


                let prevToolDef=toolDef //Observer state, original generated tool definition
                observerTokens=await self.__observeTool(toolObserverQueries,toolObserverAliases,valueSets[idx],(newValueSet)=>{ 
                    self.generatedTools[this.ecoreSync.rlookup(valueSets[idx]["TOOL"])]['toolDefinition']=self.__generateToolDefinition(ecoreLocalClone(self.definition.get("tool")),newValueSet)         
                    self.__fireToolUpdated(prevToolDef,self.generatedTools[this.ecoreSync.rlookup(valueSets[idx]["TOOL"])]['toolDefinition'])
                    prevToolDef=self.generatedTools[this.ecoreSync.rlookup(valueSets[idx]["TOOL"])]['toolDefinition']
                })
                
            }
            catch(e)
            {
                console.trace()
                console.error('tool generation: cmd generation failed: '+e);
            }
            
            self.generatedTools[this.ecoreSync.rlookup(valueSets[idx]["TOOL"])]={'toolDefinition':toolDef,'observerTokens':observerTokens}
            toolDefinitions.push(toolDef);
        }

        return toolDefinitions;
    }

    __generateToolDefinition(toolDef,valueSet){
        //Generates a tool definition using the supplied tooldefinition template and the valueSet

        //EString Attributes adaption 
        toolDef.eClass.get('eAllAttributes').filter(function(e){ return e.get("eType").get("name")=="EString";}).forEach(function(attr){                 
            toolDef.set(attr.get("name"),replaceTemplates(valueSet,toolDef.get(attr.get("name"))));
        })

        //Cmd adaption             
        let cmds=toolDef.get("factoryCmd").get("cmds").array();

        cmds.forEach(function(cmd){
            cmd.set('cmdStr',replaceTemplates(valueSet,cmd.get("cmdStr")));             
        })

        return toolDef
    }

    async __observeTool(toolObserverQueries,toolObserverAliases,vSet,callback){
        let self=this
        let valueSet=Object.assign({},vSet)
        let observerTokens=[]
        let observerFcn=(alias,value) => {
            valueSet[alias]=value
            callback(valueSet)
        }        

        //Install observers   
        for (let qry of toolObserverQueries){
            let idx=toolObserverQueries.indexOf(qry)
            if (toolObserverAliases[idx] != null){
                let alias=toolObserverAliases[idx]
                let token=await self.ecoreSync.observe(qry,(results,deltaPlus,deltaMinus) => {
                    observerFcn(alias,results)                   
                })
                observerTokens.push(token)
            }                  
        }
        
        return observerTokens
    }

    __unobserveTool(tool)
    {
        tool['observerTokens'].forEach((token) => {
            self.ecoreSync.unobserve(token)
        })
    }


    async generate()
    {

        // Generate the tool generator results

        var res=null;
        var self=this;
        let valueSet=new Object();
        valueSet["PARENT"]=this.paletteCategory.palette.graphController.eObject;
        valueSet["ROOT"]=await this.ecoreSync.getObject(0)
        valueSet["MODELROOT"]=await this.ecoreSync.utils.getModelRoot(this.paletteCategory.palette.graphController.eObject)
        valueSet["RESOURCE"]=await  this.ecoreSync.utils.getResource(this.paletteCategory.palette.graphController.eObject)

        //Tool Generator Tool Base Item Query
        let QueryObj=new Query(this.ecoreSync,'TOOL',this.definition.get("queryStr"),this.definition.get("queryTarget"),this.definition.get("queryTargetAlias"));
        let cmd=new eoq2.Get(QueryObj.build(valueSet)); 
        let results=await this.ecoreSync.exec(cmd);  
   
        res=await this.__generateToolDefinitions(QueryObj,valueSet,results);  
        return res 
    }

    __fireToolUpdated(oldTool,newTool)
    {
        for(let listener of this.toolUpdateListeners){
            listener(oldTool,newTool)
        }    
    }

    onToolUpdated(callback)
    {
        //Registers a tool update listener
        let token=null
        this.toolUpdateListeners.push(callback)
        return token
    }

    async observe(callback)
    {
        //Observes the tool generator results

        var self=this;
        let valueSet=new Object();
        valueSet["PARENT"]=this.paletteCategory.palette.graphController.eObject;
        valueSet["ROOT"]=await  this.ecoreSync.getObject(0)
        valueSet["MODELROOT"]=await  this.ecoreSync.utils.getModelRoot(this.paletteCategory.palette.graphController.eObject)
        valueSet["RESOURCE"]=await  this.ecoreSync.utils.getResource(this.paletteCategory.palette.graphController.eObject)

        // Observes addition/removal of tools
        let QueryObj=new Query(this.ecoreSync,'TOOL',this.definition.get("queryStr"),this.definition.get("queryTarget"),this.definition.get("queryTargetAlias"));  
        await this.ecoreSync.observe(QueryObj.build(valueSet),async function(results,deltaPlus,deltaMinus){
            console.debug('Tool generator re-evaluated')

            let removedTools=deltaMinus.map( (tool) => {
                let res=self.generatedTools[self.ecoreSync.rlookup(tool)]

                self.__unobserveTool(res)

                delete self.generatedTools[self.ecoreSync.rlookup(tool)]
                return res['toolDefinition']
            })

            let addedTools=await self.__generateToolDefinitions(QueryObj,valueSet,deltaPlus);
        
            callback([],addedTools,removedTools);
        }); 
        
        //Observes tool changes
        self.onToolUpdated((oldTool,newTool)=>{         
            callback([{'old':oldTool, 'new': newTool}],[],[])
        })
    }


    
}