import Query from '../../queries/Query.js'
import GraphObjectType from './GraphObjectType.js'

export default class LabelType extends GraphObjectType{
    constructor(ecoreSync,model){
        super(ecoreSync,model)
        this.queries=new Query(this.ecoreSync,this.model.get("alias"),this.model.get("queryStr"),this.model.get("queryTarget"),this.model.get("queryTargetAlias"))
    }
}