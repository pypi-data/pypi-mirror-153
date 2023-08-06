import EdgeManager from './EdgeManager.js'
import VertexManager from './VertexManager.js'
import StaticVertexManager from './StaticVertexManager.js'

export default class GraphModelManager{
    constructor(graphModelFactory,ecoreSync,model,resourceProvider){
        this.graphModelFactory=graphModelFactory;
        this.ecoreSync=ecoreSync;
        this.model=model;
        this.subManagers=[];
        this.resourceProvider=resourceProvider;
    }   

    async load(valueSet){

        console.info('Loading model...')
        var self=this;
        this.model.vertices=[];
        this.model.edges=[];

        var loadingSubManagers=[];
     
        this.subManagers.forEach(function(manager){
            loadingSubManagers.push(manager.load(valueSet));                     
        });

        loadingSubManagers=await Promise.all(loadingSubManagers)

        console.info('Submanagers completed loading.')


        for(let i in loadingSubManagers)
        {
            if(self.subManagers[i] instanceof VertexManager)
            {
                loadingSubManagers[i].forEach(function(v){
                    self.model.addVertex(v);
                })
            }

            if(self.subManagers[i] instanceof StaticVertexManager)
            {
                loadingSubManagers[i].forEach(function(v){
                    self.model.addVertex(v);
                })
            }

            if(self.subManagers[i] instanceof EdgeManager)
            {
                loadingSubManagers[i].forEach(function(e){
                    self.model.addEdge(e);
                })
            }
        }

        //Layout data
        var toplevelGraphObjects=[]

        var initEdgeSupportPoints=async function(e){  
            let results=[]           
            let rawSupportPoints=await self.model.layout.getEdgeSupportPoints(e);    
            
            rawSupportPoints.sort((a,b)=>{ 
                if(a.get('pointIndex') < b.get('pointIndex'))
                {
                    return -1
                }
                if(a.get('pointIndex') > b.get('pointIndex'))
                {
                    return 1
                }
                return 0;
            })
            for(let rawSupportPoint of rawSupportPoints)
            {
                results.push({x:rawSupportPoint.get('x'),y:rawSupportPoint.get('y')})
            }
            return results
        }
        var initEdge=async function(e){
            let supportPoints=await initEdgeSupportPoints(e)
            e.supportPoints=supportPoints
        }
        var initVertexPosition=async function(v){ 
            var position=self.model.layout.getVertexPosition(v);           
            if(position) return position
            return {x:0,y:0}
        }
        var initVertexSize=async function(v){ 
            var size=self.model.layout.getVertexSize(v);          
            if(size) return size
            return {x:0,y:0}
        }
        var initVertex=async function(v)
        {       
            v.position=await initVertexPosition(v)
            let size=await initVertexSize(v);
            if(size.x>0 && size.y>0)
            {
                v.size=size;
            }
            var vertices=[];           
            v.vertices.forEach(function(sv){
                vertices.push(initVertex(sv));
            });
            return await Promise.all(vertices)
        }

        for(let vertex of this.model.vertices)
        {
            toplevelGraphObjects.push(initVertex(vertex))
        }
        for(let edge of this.model.edges)
        {
            toplevelGraphObjects.push(initEdge(edge))
        }
        await Promise.all(toplevelGraphObjects)   

        console.info('Loading successfully completed')
        return true
    }

    async initObservers(valueSet)
    {
        var self=this; 
        this.subManagers.filter(function(v){ return v.getTypeName() =='Vertex' || v.getTypeName() =='Edge' }).forEach(function(manager){
            manager.observe(valueSet,function(){ console.warn('unhandled observer interception'); },self.model);             
        });

    }

}