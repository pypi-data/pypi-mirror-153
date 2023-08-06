
/**
 * Palette view module
 * @author Matthias Brunner
 * @copyright 2019-2021 University of Stuttgart, Institute of Aircraft Systems, Matthias Brunner
*/

/** Class managing the palette view  */
class PaletteView{
    /**
     * Create a graph view and its outline 
     * @param {ecoreSyncInstance} ecoreSync - The ecoreSync instance that should be used.
     * @param {PaletteController} controller - The associated palette controller.
     * @param {DOMelement} container - The DOM element to which the palette view should be added.
     */
    constructor(ecoreSync,controller,palette,container){
        this.ecoreSync=ecoreSync;
        this.controller=controller;
        this.palette=palette;
        this.container=$(container);       
        this.postProcessing=[]; 
    }   

    /**
     * Adds a function call to the palette view's post processing.
     * @param {function} func - The function to be called during post processing.
    */
    addToPostProcessing(func){
        this.postProcessing.push(func);
    }

    /**
     * Renders a tool icon of the palette view.
     * @private
    */
    _renderToolIcon(icon)
    {
        return icon;
    }

    /**
     * Renders a category of the palette view.
     * @private
    */
    _renderCategory(category,categoryContainer){
        var contents='';
        var self=this;
        category.tools.forEach(function(tool){      
            var uuid = new Uint32Array(1);
            uuid=window.crypto.getRandomValues(uuid).toString();   
            
            let jsaToolElement=new jsa.CustomUiElement({
                elementType:'div',
                content:'<div class="palette-item" id="'+uuid+'"><span class="palette-item-icon">'+self._renderToolIcon(tool.getIcon())+'</span><span class="palette-item-label">&nbsp;&nbsp;&nbsp;'+tool.getName()+'</span></div>',
                tooltip: tool.getTooltip()
            })

            // Adds the tooltip event only if a tooltip is present
            if(jsaToolElement.tooltip && jsaToolElement.tooltip != '')
            {
                let DOM=jsaToolElement.GetDomElement()
                DOM.onmouseover=(event)=>{ $app.TriggerTooltip(jsaToolElement,0,0) }
                DOM.onmouseout=(event)=>{ $app.StopTooltip() }
            }

            categoryContainer.AddChild(jsaToolElement)
          
            self.addToPostProcessing(function(){ tool.initUI(uuid); })
        });
        return contents;
    }

    /**
     * Renders the palette view within its container.
    */
    render(){
        var self=this;
        this.container.empty();    

        let paletteContainer= new jsa.CustomContainer({});

        $app.AddChild(paletteContainer)
        
        this.palette.categories.forEach(function(cat){

            let catUiElement = new jsa.CustomContainer({
                elementType:'div', 
                content:cat.getName()
              });

              catUiElement.SetStyle(['palette-category','palette-category-label', 'unselectable'])

              self._renderCategory(cat,catUiElement)
              paletteContainer.AddChild(catUiElement)
        })
    
        this.container.append(paletteContainer.GetDomElement());   
        this.postProcess();
    }
    
    /**
     * Executes the palette view's post processing.
    */
    postProcess(){
        this.postProcessing.forEach(function(c){
            c.apply();
        });
        this.postProcessing=[];
    }
}

export default PaletteView



