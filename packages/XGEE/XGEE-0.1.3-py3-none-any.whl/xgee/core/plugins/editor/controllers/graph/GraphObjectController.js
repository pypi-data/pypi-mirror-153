export default class GraphObjectController{
    constructor(ecoreSynck,graphController){
        this.ecoreSync=ecoreSync;
        this.graphController=graphController  

        //Register with graphController
        this.graphController.registerController(this)   
    }
}