import GraphObject from './GraphObject.js'
import SizableObject from './SizableObject.js'
import LocatableObject from './LocatableObject.js'
import { multipleClasses }  from '../../lib/libaux.js'

export default class Label extends multipleClasses(GraphObject,SizableObject,LocatableObject){
    constructor(){
        super();
        this.content=''
        this.color="000000";
        this.rotation=0.0;
        this.align='CENTER';
        this.vAlign='CENTER';
        this.anchor='CENTER'
        this.segments=[];
    }

    addSegment(labelSegment){
        labelSegment.setParent(this);
        this.segments.push(labelSegment);
    }

    getContentPrototype(){
        if(this.type){
            return this.type.model.get("content")
        }
        return 'error: no label type set'
    }

    setContent(content,noParentRefresh=false)
    {
        this.content=content;
        if(this.parent && !noParentRefresh)
        {
            this.parent.graphModel.invalidate(this);
        }
    }

    refreshContent(noParentRefresh=false)
    {
        var content='';
        this.segments.forEach(function(segment){
            content+=segment.getContent()
        })
        this.setContent(content,noParentRefresh);
    }

    getStyle(){

        let align='center';
        switch(this.align)
        {
            case 'CENTER':
                align='center'
                break;
            case 'LEFT':
                align='left'
                break;
            case 'RIGHT':
                align='right'
                break;
        }     

        let vAlign='middle';
        switch(this.vAlign)
        {
            case 'CENTER':
                vAlign='middle'
                break;
            case 'TOP':
                vAlign='top'
                break;
            case 'BOTTOM':
                vAlign='bottom'
                break;
        }   

        return "shape=rectangle;fontColor=#"+this.color+";align="+align+";verticalAlign="+vAlign+";autosize=1;resizable=0;pointerEvents:0;editable=0"
    }

    isMovable(){
        return false;
    }

    isResizable(){
        return false;
    }

    toString(){
        return this.content
    }
}