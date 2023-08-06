

class IconProvider {
    constructor(name){
        this.name=name;
    };

    isApplicable(eObject){
        return true; //must return a Boolean, returns true, if the icon provider can provide an icon for the eObject
    }

    getPathToIcon(eObject){
        return null; //must return a string containing the path relative to the application root
    }

}


export {IconProvider};