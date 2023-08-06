import GraphObjectType from './GraphObjectType.js'

export default class ContainerType extends GraphObjectType{
    constructor(ecoreSync,model){
        super(ecoreSync,model)
        this.shape=null;
    }

    getStyle()
    {           
        if(this.model.get("geometricShape")){
            switch(this.model.get("geometricShape").eClass.get("name"))
            {
                case "Rectangle":
                    return "shape=rectangle;fillColor=#"+this.model.get("geometricShape").get("bgcolor")+";strokeColor=#"+this.model.get("geometricShape").get("color")+";strokeWidth=#"+this.model.get("geometricShape").get("borderWidth")+";";
              
                case "RoundedRectangle":
                    return "shape=rectangle;rounded=1;fillColor=#"+this.model.get("geometricShape").get("bgcolor")+";strokeColor=#"+this.model.get("geometricShape").get("color")+";strokeWidth=#"+this.model.get("geometricShape").get("borderWidth")+";";
              
                case "IsoscelesTriangle":
                    return "shape=triangle;fillColor=#"+this.model.get("geometricShape").get("bgcolor")+";strokeColor=#"+this.model.get("geometricShape").get("color")+";strokeWidth=#"+this.model.get("geometricShape").get("borderWidth")+";";
               
                default:
                    return "shape=image;image=data:image/svg+xml,"+btoa(this.shape)+";";
                
            }
        }
        else
        {
            return "shape=image;image=data:image/svg+xml,"+btoa(this.shape)+";imageAspect=0;";
        }
        //return "shape=rectangle;fillColor=#00b0f0;strokeColor=#000000;strokeWidth=2;fontColor=#000000;imageAspect=0;verticalLabelPosition="+labelPosition+";align="+labelAlign+";fontColor=#000000;"
    }
}