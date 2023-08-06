import Query from '../../queries/Query.js'
import GraphObjectType from './GraphObjectType.js'

export default class AnchorType extends GraphObjectType{
    constructor(ecoreSync,model){
        super(ecoreSync,model)
        this.query=new Query(this.ecoreSync,this.model.get("alias"),this.model.get("queryStr"),this.model.get("queryTarget"),this.model.get("queryTargetAlias"))
    }
    
    getType(){
        return this.model.get("type")
    }
}