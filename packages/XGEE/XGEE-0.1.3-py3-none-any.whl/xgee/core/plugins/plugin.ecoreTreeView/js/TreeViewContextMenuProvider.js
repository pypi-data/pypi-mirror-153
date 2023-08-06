class TreeViewContextMenuProvider{
    constructor(){
        if (this.constructor == TreeViewContextMenuProvider) {
            throw new Error("Interface classes can not be instantiated.");
        }
    }

    // to implement this interface, simply inherit from this class

    isApplicableToNode(node)
    {
        return true; //must return a boolean, return true if this context menu applies to the supplied node
    }

    getContextMenu(node){
       
        return null; //must return a context menu for the target node
    }

}

export {TreeViewContextMenuProvider}