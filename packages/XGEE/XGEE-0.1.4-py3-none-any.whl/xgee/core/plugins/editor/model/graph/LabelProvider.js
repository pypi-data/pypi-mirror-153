export default class LabelProvider{
    initializer(){
        this.labels=[];
    }

    hasLabels()
    {
        return this.labels.length>0
    }
    
    hasLabel(label){
        var idx=this.labels.indexOf(label);
        if(idx > -1){ return true } else { return false }       
    }

    addLabel(label){
        if(label==null) throw 'supplied label is invalid'
        label.parent=this;
        this.labels.push(label)
    }

    removeLabel(label)
    {

    }    
}