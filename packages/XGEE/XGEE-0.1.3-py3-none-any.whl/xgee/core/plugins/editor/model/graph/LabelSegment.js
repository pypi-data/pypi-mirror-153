
import TypedObject from './TypedObject.js'
import { replaceTemplates, mergeValueSets } from '../../lib/libaux.js'

export default class LabelSegment extends TypedObject{

    constructor(parent=null,content=''){
        super();
        this.parent=parent;
        this.content=content
        this.valueSet=null;
    }

    setParent(parent){
        this.parent=parent;
    }

    setContent(content='', noParentRefresh=false)
    {
        this.content=content;
        if(this.parent && !noParentRefresh)
        {
            this.parent.refreshContent();
        }
    }

    getContent()
    {
        let style="pointer-events:none;display:inline;"
        if(this.type.model.get("color")!=null && this.type.model.get("color").length == 6)
        {
            style+="color:#"+this.type.model.get("color")+";"
        }
        if(this.type.model.get("size")!=null)
        {
            style+="font-size:"+this.type.model.get("size")+"px;"
        }
        return '<div style="'+style+'">'+this.content+'</div>'
    }

    updateValueSet(valueSet,overwrite=false,noRefresh=false,noParentRefresh=false)
    {
        if(!overwrite)
        {
            this.valueSet=mergeValueSets(this.valueSet,valueSet);            
        }
        else
        {
            this.valueSet=valueSet;
        }
        
        //remove special values from valueSet
        delete this.valueSet["ROOT"]
        delete this.valueSet["PARENT"]
        delete this.valueSet["MODELROOT"]
        delete this.valueSet["RESOURCE"]
   
        if(!noRefresh) this.refreshContent(noParentRefresh);
    }

    refreshContent(noParentRefresh=false){
        if(this.valueSet!=null)
        {
            let refreshedContent=replaceTemplates(this.valueSet,this.type.model.get('content'));
            if(this.content!=refreshedContent)
            {
                this.content=refreshedContent;
                if(this.parent && !noParentRefresh) this.parent.refreshContent();
            }
        }
    }
}

