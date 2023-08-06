import { replaceTemplates } from '../../lib/libaux.js'

export default class DeletableObject{
    initializer(){

    }  

    isDeletable(){
        return this.type.model.get('isDeletable')?true:false
    }
    
    async delete(valueSet={}){
        
        valueSet["SELF"]=this.eObject
        if(this.parent && this.parent.eObject)
        {
            valueSet["PARENT"]=this.parent.eObject
        }        

        if(!this.type.model.get('onDeletion'))
        {
            let objId=ecoreSync.rlookup(this.eObject)
            ecoreSync.exec(new eoq2.Rem(new eoq2.Obj(objId).Met('PARENT'),new eoq2.Obj(objId).Met('CONTAININGFEATURE').Pth('name'),new eoq2.Obj(objId)))
        }
        else
        {
            let deletionCmd=new eoq2.Cmp()
            let cmds=this.type.model.get('onDeletion').get('cmds').array()

            for(let cmd of cmds)
            {
                eval('deletionCmd.'+replaceTemplates(valueSet,cmd.get('cmdStr')))
            }

            ecoreSync.exec(deletionCmd)
        }
    }

}