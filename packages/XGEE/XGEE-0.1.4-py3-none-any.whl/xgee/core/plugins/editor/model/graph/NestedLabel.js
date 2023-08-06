import GraphObject from './GraphObject.js'
import SizableObject from './SizableObject.js'
import LocatableObject from './LocatableObject.js'
import Label from './Label.js'
import { multipleClasses }  from '../../lib/libaux.js'



export default class NestedLabel extends multipleClasses(Label){
    constructor(){
        super();        
    }




    toString(){
        let parentSize=this.parent.getSize()
        return '<div style="padding:5px;color:#000000; white-space:normal; min-width:'+parentSize.x+'px;overflow:hidden; max-height:'+parentSize.y+'px; pointer-events:none;">'+this.content+'</div>'
    }
}