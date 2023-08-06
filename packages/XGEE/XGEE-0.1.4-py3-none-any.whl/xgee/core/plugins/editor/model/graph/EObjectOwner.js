export default class EObjectOwner{
    constructor(){
        this.eObject=null;
    }
    initializer(){
        this.eObject=null;
    }
    getEObject(){
        return this.eObject;
    }
    getEObjectId(){
        return ecoreSync.rlookup(this.eObject)
    }
}