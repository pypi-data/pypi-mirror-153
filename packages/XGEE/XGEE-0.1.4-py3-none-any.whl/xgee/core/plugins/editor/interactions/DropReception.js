import GraphInteraction from './GraphInteraction.js'
import { replaceTemplates } from '../lib/libaux.js'

/** 
 * Class for the description of drop receptions of the graph (drag&drop, built-in graph interaction)
 * @extends GraphInteraction
*/
class DropReception extends GraphInteraction{

     /**
     * Create the drop recepetion
     * @param {ecoreSyncInstance} ecoreSync - The ecoreSync instance used by this graph interaction
     */
    constructor(ecoreSync){
        super(ecoreSync);       
        this.dropItemNsURI='';
        this.dropItemClassName='';
        this.cmdString=''    
        this.cmd=null;    
        this.controller=null;
        this.cmdDefinition=null;
    }

     /**
     * Indicates wether this drop reception is associated with the supplied drop target object 
     * @param {object} dropTarget - The object on which another object was dropped
     * @returns {boolean} True if the supplied object is associated with this drop reception, false otherwise.
     */
    isTargeting(dropTarget)
    {
        if(!dropTarget) throw 'no drop target was supplied to DropReception'
        return dropTarget.eClass.get("name")==this.className && dropTarget.eClass.eContainer.get("nsURI")==this.nsURI
    }

     /**
     * Indicates wether this drop reception can process the supplied drop item object
     * @param {object} dropItem - The object that was dropped on another object
     * @returns {boolean} True if the supplied object can be processed by the drop reception, false otherwise.
     */
    isReceiving(dropItem)
    {
        if(!dropItem) throw 'no drop item was supplied to DropReception'
        return dropItem.eClass.get("name")==this.dropItemClassName && dropItem.eClass.eContainer.get("nsURI")==this.dropItemNsURI
    }
   
    /**
     * Gets the EOQ command that should be executed when the drop item is dropped on the drop target. Replaces all placeholders in the command with help of a generated value set.
     * @param {object} dropTarget - The object on which another object was dropped
     * @param {object} dropItem - The object that was dropped on another object
     * @returns {EOQCmd} The EOQ command that should be executed when the drop item is dropped on the drop target.
     */
    async getCmd(dropTarget,dropItem){      

        var valueSet={};
        let ts=new eoq2.serialization.TextSerializer();
        try{        
            valueSet["PARENT"]=this.controller.eObject
            valueSet["ROOT"]=await this.ecoreSync.getObject(0)
            valueSet["MODELROOT"]=await this.ecoreSync.utils.getModelRoot(dropTarget)
            valueSet["RESOURCE"]=await this.ecoreSync.utils.getResource(dropTarget)
            valueSet["DROPTARGET"]=dropTarget
            valueSet["DROPITEM"]=dropItem
        }
        catch(e)
        {
            console.error('cmd preparation failed, because valueSet definition failed: '+e);
        }
                
        if(this.cmdDefinition)
        {
            var dropCmd=new eoq2.Cmp();
            var cmds=this.cmdDefinition.get("cmds").array();
            cmds.forEach(function(cmd){            
                try{              
                    let str=cmd.get("cmdStr");                  
                    str=replaceTemplates(valueSet,str);
                    let addCmd = ts.deserialize(str);
                    dropCmd.a.push(addCmd);
                    // eval('dropCmd.'+str)
                }
                catch(e){
                    console.error('cmd preparation failed for drop reception: '+e);
                };
            })
            return dropCmd;
        }
        else
        {
            console.warn('drop reception preparation failed: no definition')
        }

            
    }
}

export default DropReception