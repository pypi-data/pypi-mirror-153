import ScreenshotExport from './ScreenshotExport.js'
import * as contextMenus from '../extensions/EditorContextMenuProvider.js'

/** Class configuring the built-in graph view context menu  */
class GraphViewMenu extends contextMenus.EditorContextMenuProvider{
     /**
     * Create an instance of the screenshot export context menu.
     * @param {contextMenuAPI} contextMenu - The API object of the context menu.
     */
    constructor(contextMenu){
        super();
        this.contextMenu=contextMenu   
    }

    /**
     * Makes the Screenshot context menu available on the graph canvas
    */
    isApplicableToTarget(target){
        return target.isCanvas 
    }

    /**
     * Returns the screenshot context menu
    */
    getContextMenu(target){
        var cMenu=false;
        if(target.isCanvas)
        {
            cMenu=this.contextMenu.createContextMenu('xgee-builtin-context-menu','XGEE Built-In Context Menu',1);

            cMenu.addNewEntry('center-graph','Center graph',async function(){       
                let graphView=$app.viewManager.activeView.XGEEInstance.graphView
                let graphBounds=graphView.graphController.getBoundingBox()        
                graphView.viewPort.panTo(graphBounds.centerX,graphBounds.centerY)
                let scale=Math.min(graphView.viewPort.getWidth()/graphBounds.width,graphView.viewPort.getHeight()/graphBounds.height)
                graphView.viewPort.setScale(scale*0.9)
            },'copy')

            cMenu.addNewEntry('save-screenshot','Save screenshot',async function(){     
                ScreenshotExport.exportSVG()               
            },'copy')

        }
        return cMenu;
    }
}


export default GraphViewMenu