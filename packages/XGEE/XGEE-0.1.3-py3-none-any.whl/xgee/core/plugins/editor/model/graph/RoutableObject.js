import GraphEvent from './GraphEvent.js'

export default class RoutableObject{
    initializer(){
        this.supportPoints=[]       
        this.events["ROUTED"]=new GraphEvent(); 
    }  

    setSupportPoints(supportPoints)
    {
        if(supportPoints)
        {
            this.supportPoints=supportPoints
            this.events["ROUTED"].raise(supportPoints)
        }
    }

    getSupportPoints()
    {
        return [...this.supportPoints]
    }

}