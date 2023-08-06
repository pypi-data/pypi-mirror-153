import PaletteModel from '../../model/palette/PaletteModel.js'
import PaletteView from '../../view/PaletteView.js'

export default class PaletteController{
    constructor(ecoreSync,repositoryURL,paletteDefinition,eObject,DOMcontainer,graphController){
        var self=this
        this.ecoreSync=ecoreSync;
        this.eObject=eObject;   
        this.model=new PaletteModel(ecoreSync,repositoryURL,this,paletteDefinition,graphController);
        this.view=new PaletteView(ecoreSync,this,this.model,DOMcontainer);
        this.activeTool=null;
        this.model.events["PALETTE_CHANGED"].addListener(() => {
            self.view.render()
        })
    }
    async init(){
        await this.model.init();
        this.view.render();
    }

    async activateTool(tool)
    {
        await this.deactivateCurrent();        
        this.activeTool=tool;
        return true
    }

    async deactivateTool(tool)
    {
        if(this.activeTool==tool)
        {
            this.activeTool=null;
        }
        return true
    }

    async deactivateCurrent()
    {
        if(this.activeTool)
        {
            await this.activeTool.deactivate();
        }   
    }

    getActiveTool()
    {
       return this.activeTool 
    }
}