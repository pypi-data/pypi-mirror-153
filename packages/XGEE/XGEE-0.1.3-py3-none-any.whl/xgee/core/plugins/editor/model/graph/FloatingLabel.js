import GraphObject from './GraphObject.js'
import SizableObject from './SizableObject.js'
import LocatableObject from './LocatableObject.js'
import Label from './Label.js'
import { multipleClasses }  from '../../lib/libaux.js'

export default class FloatingLabel extends multipleClasses(Label){
    constructor(){
        super();        
    }
}