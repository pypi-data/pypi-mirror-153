
// XGEE Presentation Model class


export default class XGEEPresentationModel{
    constructor(pathToModel,presentationModel){
        this.pathToModel=pathToModel
        this.presentationModel=presentationModel
    }

    getPath(){
        return this.pathToModel
    }

    getModel(){
        return this.presentationModel
    }
}


