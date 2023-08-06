
import GraphTool from './GraphTool.js'
import { replaceTemplates } from '../../lib/libaux.js'

export default class SelectionTool extends GraphTool{
    constructor(...args){
        super(...args)
        let self=this
        this.isSelectionTool=true  
    }

    async init(){   
        if(!this.toolDefinition) { throw 'tool initialization failed, because no definition was provided' }
        //TODO FactoryCMD for selection tools that produce an eObject
    }

    async activate(){
        if(super.activate()){
            var currentSelection=this.palette.graphController.view.getCurrentGraphSelection()  
            if(currentSelection!=null && Array.isArray(currentSelection))    
            {   
                if(await this.canUse(currentSelection)==true)
                {
                    this.applyTo(currentSelection)
                }
            }
        }
    }

    async canUse(selection){
        let ts=new eoq2.serialization.TextSerializer();

        let res=false
        if(selection.length){
            var selectorQry=new eoq2.Qry(selection.map((obj) => { return this.ecoreSync.utils.encode(obj)}))
            let selectorStr = this.toolDefinition.get('selector')
            selectorQry.Sel(ts.deserialize(selectorStr))
            // eval('selectorQry.Sel(QRY.'+this.toolDefinition.get('selector')+')')
            var selectorResults=await this.ecoreSync.exec(new eoq2.Get(selectorQry))
            
            if(this.toolDefinition.get('usesSingleTarget'))
            {
                if(this.toolDefinition.get('selector')!=null && this.toolDefinition.get('selector')!='')
                {                   
                    res=selectorResults.length==1
                }                   
            }
            else
            {
                res=selectorResults.length>0
            }
        }
        return res
    }

    async applyTo(selection){
        let ts=new eoq2.serialization.TextSerializer();
        
        var selectorQry=new eoq2.Qry(selection.map((obj) => { return this.ecoreSync.utils.encode(obj)}))
        let selectorStr = this.toolDefinition.get('selector')
        selectorQry.Sel(ts.deserialize(selectorStr))
        // eval('selectorQry.Sel(QRY.'+this.toolDefinition.get('selector')+')')
        var selectorResults=await this.ecoreSync.exec(new eoq2.Get(selectorQry))
        let valueSet={"ROOT":this.ecoreSync.lookup(0),"MODELROOT":this.palette.graphController.eObject} 

        if(this.toolDefinition.get('usesSingleTarget'))
        {
            if(this.toolDefinition.get('selector')!=null && this.toolDefinition.get('selector')!='')
            {                   
                if(selectorResults.length==1)
                {
                    valueSet["SELECTION"]=selectorResults[0]
                }
            }                   
        }
        else
        {
            if(selectorResults.length)
            {
                valueSet["SELECTION"]=selectorResults
            }
        }
        
        if(valueSet.hasOwnProperty('SELECTION'))
        {
            let selectionCmd=new eoq2.Cmp();
            let selectionCmds=this.toolDefinition.get("selectionCmd").get("cmds").array(); 
            selectionCmds.forEach(function(cmd){
                try{
                    // eval('selectionCmd.'+replaceTemplates(valueSet,cmd.get("cmdStr")));
                    let addCmd = ts.deserialize(replaceTemplates(valueSet,cmd.get("cmdStr")));
                    selectionCmd.a.push(addCmd)
                }
                catch(e)
                {
                    console.error('selection cmd failed: '+e,'cmd:'+cmd.get("cmdStr"));
                    throw e
                }
            })
      
           await this.ecoreSync.exec(selectionCmd);
        }
        
        this.deactivate()
    }




}