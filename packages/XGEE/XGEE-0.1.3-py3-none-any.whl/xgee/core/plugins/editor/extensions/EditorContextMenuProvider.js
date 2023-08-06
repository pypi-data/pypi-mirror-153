/**
 * XGEE Context Menu module
 * @author Matthias Brunner
 * @copyright 2019-2021 University of Stuttgart, Institute of Aircraft Systems, Matthias Brunner
*/

/** Interface class for XGEE graph context menu providers
 *  Implementation of this interface is required when extending the context menu via the xgee.menus extension point
 *  @interface
*/
class EditorContextMenuProvider{

    /**
     * Create the context menu provider
     * @param {ecoreSyncInstance} ecoreSync - The ecoreSync instance used by this graph interaction
     */
    constructor(){
        //Throws an error if this interface is directly instantiated
        if (this.constructor == EditorContextMenuProvider) {
            throw new Error("Interface classes can not be instantiated.");
        }
    }

    /**
     * Indicates whether the provider is able to provide context menu for a target object
     * 
     * The target object provides the following information:
     *      - target.editorId
     *      - target.eObject
     *      - target.graphObject
     *      - target.isCanvas
     *      - target.isGraphObject 
     *      - target.isVertex  
     *      - target.isEdge
     *      - target.DOM
     * 
     * @param {target} ecoreSync - The ecoreSync instance used by this graph interaction
     * @returns {boolean} True if the provider is able to provide a context menu for the supplied target, false otherwise.
     */
    isApplicableToTarget(target)
    {
        //you can use the target information with the above attributes to decide whether you provide a context menu

        return true; //must return a boolean, return true if this context menu applies to the target
    }

    /**
     * Gets the context menu prepared by the provider for a target object
     * 
     * The target object provides the following information:
     *      - target.editorId
     *      - target.eObject
     *      - target.graphObject
     *      - target.isCanvas
     *      - target.isGraphObject 
     *      - target.isVertex  
     *      - target.isEdge
     *      - target.DOM
     * 
     * @param {target} ecoreSync - The ecoreSync instance used by this graph interaction
     * @returns {contextMenu} A context menu object 
     */
    getContextMenu(target){

        //you can use the target information with the above attributes to create a context menu

        return null; //must return a context menu for the target
    }

}

export {EditorContextMenuProvider}