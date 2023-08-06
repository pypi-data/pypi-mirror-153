import GraphObjectController from './GraphObjectController.js'

export default class LabelController extends GraphObjectController{
    constructor(ecoreSync,graphController) {
        super(ecoreSync,graphController)  
        this.type=null;
        this.eObject=null;
        this.label=null;
        this.queryControllers=[];    
    }

    async load(valueSet){     
        var queryResults=[];
        console.error('LBL CTRLS: ')
        console.error(this.queryControllers);
        this.queryControllers.forEach(function(qc){
            queryResults.push(qc.exec(valueSet));
        })
        queryResults=await Promise.all(queryResults);
        queryResults.forEach(function(qr){
            mergeValueSets(valueSet,qr,["PARENT","ROOT","MODELROOT","RESOURCE"]);
        })
        this.label=graphModelFactory.createLabel(this.type);
        this.label.setContent(replaceTemplates(valueSet,this.label.type.model.get("content")))
        return this.label
    }
}