import GraphEvent from './GraphEvent.js'

export default class ContainerProvider{
    initializer(){
        this.containers=[];
        this.events["CONTAINER_ADDED"]=new GraphEvent(true);
        this.events["CONTAINER_REMOVED"]=new GraphEvent(true);
    }
    addContainer(container){
        container.parent=this
        this.containers.push(container)
    }
    removeContainer(container){
        let idx=this.containers.indexOf(container);
        if(idx > -1)
        {
            this.containers.splice(idx, 1);
        }      
        this.events["CONTAINER_REMOVED"].raise(container);   
    }
}