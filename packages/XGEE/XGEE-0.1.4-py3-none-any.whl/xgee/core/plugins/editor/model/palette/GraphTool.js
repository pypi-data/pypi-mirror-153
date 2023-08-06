import GraphResourceProvider from '../../graph/GraphResourceProvider.js'

export default class GraphTool{
    constructor(ecoreSync,resourceProvider,toolDef,palette){
        this.ecoreSync=ecoreSync;
        this.toolDefinition=toolDef;
        this.resourceProvider = resourceProvider;  
        this.icon=this.resourceProvider.LoadResource(this.toolDefinition.get("icon")) 
        this.palette=palette;
        this.factoryCmdResults=null
        this.template=null
        this.isActive=false
    }

    init(){        
    }

    initUI(elementId)
    {

    }

    async activate(){
        var result=await this.palette.controller.activateTool(this);
        if(result)
        {
            $("#"+this.elementId).addClass("palette-item-active");
            this.isActive=true;
        }
        return result
    }

    async deactivate(){
        var result=await this.palette.controller.deactivateTool(this);
        if(result)
        {           
            $("#"+this.elementId).removeClass("palette-item-active");     
            this.isActive=false;
        }
        return result
    }

    toggle(){     
        if(this.isActive){ 
            this.deactivate() 
        } else { 
            this.activate()
        }
    }

    initUI(elementId){
        var self=this;
        this.elementId=elementId;
        $("#"+elementId).click(function(){
            self.toggle();
        });  
    }


    async execFactoryCmd(){
        let valueSet={}; 
        let factoryCmd=new eoq2.Cmp();
        let factoryCmds=this.toolDefinition.get("factoryCmd").get("cmds").array(); 
        let ts=new eoq2.serialization.TextSerializer();
        
        if(factoryCmds.length)
        {
            let resultAliases=[];   
        
                factoryCmds.forEach(function(cmd){
                    try{
                    let AddCmd = ts.deserialize(cmd.get("cmdStr"));
                    factoryCmd.a.push(AddCmd);
                    // factoryCmd.a.push(AddCmd[0]); //version eoq2 752e
                    // this is quite hacky, there is probably a better way

                    // eval('factoryCmd.'+cmd.get("cmdStr"));
                    resultAliases.push(cmd.get("alias"));
                    }
                    catch(e)
                    {
                        console.error('factory cmd failed: '+e,'cmd:'+cmd.get("cmdStr"));
                        throw e
                    }
                })
    

            try{
                var res=await this.ecoreSync.exec(factoryCmd);
                res.forEach(function(result,idx){
                    valueSet[resultAliases[idx]]=result;
                });                  
            }
            catch(e)
            {
                throw 'failed to initialize template for tool: '+e;
            }
            this.factoryCmd=factoryCmd
            this.factoryCmdResults=valueSet
        }

        return valueSet
    }


    async initTemplate(){
        let template=null
        if(this.toolDefinition.get("providesTemplate"))
        {           
            if(!this.factoryCmdResults)
            {
               await this.execFactoryCmd() 
            }      

            if(this.factoryCmdResults["TEMPLATE"])
            {
                template=this.factoryCmdResults["TEMPLATE"]  
            }

            this.template=template
        }
        return template
    }

    getName(){
        return this.toolDefinition.get("name")
    }

    getId(){
        return this.toolDefinition.get("id")
    }

    getIcon(){
        return this.icon
    }

    getTooltip(){
        return this.toolDefinition.get("tooltip")
    }
}