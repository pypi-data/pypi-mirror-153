// This is the baseclass for all plugins that would like to provide a filter for contextMenu.ecore
// 2020 Matthias Brunner

class Filter{
    constructor(){
        
    }

    select(eObject)
    {

        return false; //must return a Boolean, for each selected eObject (true), contextMenu.ecore will not install a context menu
    }

}

export {Filter}



