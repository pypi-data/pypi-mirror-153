import Vertex from './Vertex.js'
import EventProvider from './EventProvider.js'
import Container from './Container.js'
import Edge from './Edge.js'
import { castToFloat } from '../../lib/libaux.js'
import GraphEvent from './GraphEvent.js';

const XGEE_LAYOUT_UPDATE_PERIOD=500 //ms;


export default class GraphLayoutManager extends EventProvider{
    constructor(eObject){
        super();
        this.ecoreSync=ecoreSync;
        this.eObject=eObject;

        this.resource=null;
        this.root=null;
        this.layout=null;

        this.cache=new Map();

        this.vertexCache=new Map();

        this.scaleUpdate=null
        this.translateUpdate={x:null,y:null}

        this.updates=new eoq2.Cmp();
        this.scheduledUpdate=null;
        this.updatesEnabled=true;

        //Temporary positions that are only available locally
        this.temporaryPositions=[];

        //Layout requests
        this.positionRequests=[]
        this.sizeRequests=[]
        this.scheduledRequest=null;

        //Layout events
        this.createEvent('CACHE_BUILT')
    }

    async init(){
        this.resource=await this.getLayoutResource()
        this.observeResource()
        
        //Init
        this.root=await this.getRoot();
        this.layout=await this.getLayout();    
        await this.buildCache()
    }


    async buildCache(){
        var self=this
        var invalidEntries=[]
        //Command for retrieving layout information
        let cmd=new eoq2.Cmp()
        cmd.Get(new eoq2.Obj(this.ecoreSync.rlookup(this.layout)).Cls('Vertex'))
        cmd.Get(new eoq2.His(0).Pth('refersTo'))
        cmd.Get(new eoq2.His(0).Pth('parent').Trm().Pth('refersTo'))
        cmd.Get(new eoq2.His(0).Pth('sizeX'))
        cmd.Get(new eoq2.His(0).Pth('sizeY'))
        cmd.Get(new eoq2.His(0).Pth('x'))
        cmd.Get(new eoq2.His(0).Pth('y'))
   
        var results=await this.ecoreSync.exec(cmd)
   
        //Building the cache
        results[1].forEach((obj,idx) => {
            let oid=null
            let pid=null
            let parent=results[2][idx]

            if(obj!=null){ oid=this.ecoreSync.rlookup(obj) }        
            if(parent!=null){ pid=this.ecoreSync.rlookup(parent)}   

            if(oid)
            {
                    let entryKey='default'
                    if(pid!=null)
                    {
                        entryKey=String(pid)+'.'+String(oid)
                    }
                    else
                    {
                        entryKey=String(oid)
                    }

                    if(!self.vertexCache.has(entryKey))
                    {
                        self.vertexCache.set(entryKey,results[0][idx])
                    }
                
            }

            if(obj==null) invalidEntries.push(idx)
        })
           
        //Remove invalid entries from layout
        //this.clearEntries(results[0].filter((v,idx) => { return invalidEntries.includes(idx) }).map((obj) => { return this.ecoreSync.rlookup(obj) }))

        this.raise('CACHE_BUILT')
    }



    async update(){
        //scheduled canceable update action 
        const scheduledLayoutUpdate = (layoutManager,interval) => {
            var timer=null;
            var rejectUpdate=()=>{};
            var scheduledUpdate=new Promise(function(resolve,reject){
                reject=rejectUpdate;
                timer = setTimeout(function(){
                    layoutManager.updateNow();
                    resolve();                    
                }, interval);
            });
            
            return {
                promise: scheduledUpdate,
                cancel: () => { 
                    clearTimeout(timer); 
                    timer=null;
                    rejectUpdate();
                    rejectUpdate=()=>{};
                }
            }            
        };

        if(this.scheduledUpdate!=null)
        {
            this.scheduledUpdate.cancel();
            this.scheduledUpdate=scheduledLayoutUpdate(this,XGEE_LAYOUT_UPDATE_PERIOD);
        }
        else
        {
            this.scheduledUpdate=scheduledLayoutUpdate(this,XGEE_LAYOUT_UPDATE_PERIOD);
        } 
    }

    async updateNow(){
        //uncancelable update action 
        this.scheduledUpdate=null;
        var pendingUpdates=this.updates;
        this.updates=new eoq2.Cmp();

        if(this.scaleUpdate)
        {
            pendingUpdates.Set(new eoq2.Obj(this.ecoreSync.rlookup(this.layout)),"scale",castToFloat(this.scaleUpdate))
            this.scaleUpdate=null
        }

        if(this.translateUpdate){
            if(this.translateUpdate.x) pendingUpdates.Set(new eoq2.Obj(this.ecoreSync.rlookup(this.layout)),"translateX",castToFloat(this.translateUpdate.x))
            if(this.translateUpdate.y) pendingUpdates.Set(new eoq2.Obj(this.ecoreSync.rlookup(this.layout)),"translateY",castToFloat(this.translateUpdate.y))
            this.translateUpdate.x=null
            this.translateUpdate.y=null
        }

        if(pendingUpdates.a.length)
        {
            await this.ecoreSync.exec(pendingUpdates);
        }
    }


    async createLayoutResource(directory,layoutResourceName){       

        let cmd=new eoq2.Cmp()
        cmd.Crn("http://www.xgee.de/layout/v1","LayoutContainer",1)
        cmd.Crn("http://www.eoq.de/workspacemdbmodel/v1.0","ModelResource",1)
        cmd.Set(new eoq2.Qry().His(1),"name",layoutResourceName)
        cmd.Add(new eoq2.Qry().His(1),"contents",new eoq2.Qry().His(0))
        cmd.Add(new eoq2.Qry().Obj(this.ecoreSync.rlookup(directory)),"resources",new eoq2.Qry().His(1));

        var result=await this.ecoreSync.exec(cmd)  

        return result[1]
    }

    async getLayoutResource(){        
        if(this.resource!=null) { return this.resource }
        let res=await this.ecoreSync.utils.getResource(this.eObject)
        let directory=await this.ecoreSync.utils.getContainer(res);      
        if(directory)
        {
            var layoutResourceName=await ecoreSync.get(res,'name')+'.layout';
            let cmd=new eoq2.Get(QRY.Obj(this.ecoreSync.rlookup(directory)).Pth('resources').Sel(QRY.Pth('name').Equ(layoutResourceName)).Trm(QRY.Met('SIZE').Equ(0),null).Idx(0));
            var layoutResource=await this.ecoreSync.remoteExec(cmd,true);
            if(layoutResource==null){
                layoutResource==await this.createLayoutResource(directory,layoutResourceName);
            }
            return layoutResource
        }
        else
        {
            throw(' Resource could not be found')
        }
    }

    async getRoot(){
        if(this.root!=null){ return this.root}
        var layoutResource=await this.getLayoutResource();
        var resourceContents=await this.ecoreSync.get(layoutResource,"contents");
        if(resourceContents.length)
        {
            return resourceContents[0]
        }
        else
        {
            //transparently repair resource
            let cmd=new eoq2.Cmp()
            cmd.Crn("http://www.xgee.de/layout/v1","LayoutContainer",1)
            cmd.Add(new eoq2.Obj(this.ecoreSync.rlookup(layoutResource)),"contents",new eoq2.His(-1))
            var res=this.ecoreSync.remoteExec(cmd,true);
            return res[0]
        }
    }

    async getLayout(){

        if(this.layout==null){
            var root=await this.getRoot();
            let cmd=new eoq2.Cmp();
            cmd.Get(new eoq2.Obj(this.ecoreSync.rlookup(root)).Pth('layouts').Sel(new eoq2.Qry().Pth('refersTo').Equ(new eoq2.Obj(this.ecoreSync.rlookup(this.eObject)))).Trm(QRY.Met('SIZE').Equ(0),null).Idx(0))
            cmd.Get(new eoq2.Met('IF',[new eoq2.His(0).Neq(null),new eoq2.His(0).Pth('scale'),null]));
            cmd.Get(new eoq2.Met('IF',[new eoq2.His(0).Neq(null),new eoq2.His(0).Pth('translateX'),null]));
            cmd.Get(new eoq2.Met('IF',[new eoq2.His(0).Neq(null),new eoq2.His(0).Pth('translateY'),null]));
            let resLayout=await this.ecoreSync.remoteExec(cmd,true);

            if(resLayout[0]!=null)
            {
                this.layout=resLayout[0];
            }
            else
            {
                let cmd=new eoq2.Cmp();
                cmd.Crn("http://www.xgee.de/layout/v1/def","Layout",1)
                cmd.Set(new eoq2.Qry().His(-1),"refersTo",new eoq2.Obj(this.ecoreSync.rlookup(this.eObject)))
                //should be obsolete if default values work correctly
                cmd.Set(new eoq2.Qry().His(0),"scale",castToFloat(1))
                cmd.Set(new eoq2.Qry().His(0),"translateX",castToFloat(0))
                cmd.Set(new eoq2.Qry().His(0),"translateY",castToFloat(0))
                cmd.Add(new eoq2.Obj(this.ecoreSync.rlookup(root)),"layouts",new eoq2.Qry().His(0))
                let res=await this.ecoreSync.remoteExec(cmd,true);
                this.layout=res[0];
            }
        }
        return this.layout;
    }  

    async getScale(){
        var layout=await this.getLayout();
        return await this.ecoreSync.get(layout,"scale")        
    }

    async setScale(scale){
        var res=false;        
        if(this.layout)
        {            
            this.scaleUpdate=scale
            res=true;
            this.update();
        }
        return res;
    }

    async setTranslate(x=null,y=null)
    {
        if(this.layout)
        {
            if(x) this.translateUpdate.x=x
            if(y) this.translateUpdate.y=y
            this.update();
            return true
        }
    }

    async getTranslate()
    {
        if(this.layout)
        {
            var cmd=new eoq2.Cmp();
            cmd.Get(new eoq2.Obj(this.ecoreSync.rlookup(this.layout)).Pth('translateX'))
            cmd.Get(new eoq2.Obj(this.ecoreSync.rlookup(this.layout)).Pth('translateY'))
            var res=await this.ecoreSync.remoteExec(cmd,true);
            return {x:res[0],y:res[1]}
        }
    }
    
    async createVertexLayoutItem(eObject,x=null,y=null,parent=null)
    {
        var vertexLayoutItem=null;
        let cmd=new eoq2.Cmp()
        let oid=this.ecoreSync.rlookup(eObject);
        if(parent!=null) var poid=this.ecoreSync.rlookup(parent);
        if(oid==null) throw 'invalid eObject supplied: oid is null'
        if(parent!=null && poid==null) throw 'invalid parent supplied: oid is null'


        cmd.Crn('http://www.xgee.de/layout/v1/def','Vertex',1)
        cmd.Set(new eoq2.Qry().His(0),"refersTo",new eoq2.Obj(oid))
        cmd.Add(new eoq2.Obj(this.ecoreSync.rlookup(this.layout)),"contents",new eoq2.Qry().His(0))
        if(x!=null && y!=null)
        {
            cmd.Set(QRY.His(0),"x",x)
            cmd.Set(QRY.His(0),"y",y)
        }
        cmd.Get(new eoq2.Qry(),QRY.His(0).Pth('x'))
        cmd.Get(new eoq2.Qry(),QRY.His(0).Pth('y'))
        cmd.Get(new eoq2.Qry(),QRY.His(0).Pth('sizeX'))
        cmd.Get(new eoq2.Qry(),QRY.His(0).Pth('sizeY'))

        if(poid!=null) cmd.Set(new eoq2.Qry().His(0),'parent',QRY.Obj(poid))
        var result= await this.ecoreSync.exec(cmd)
        vertexLayoutItem=result[0];
        if(parent!=null) await this.ecoreSync.set(vertexLayoutItem,"parent",parent)
        return vertexLayoutItem
    }

    async createEdgeLayoutItem(eObject,supportPoints=null)
    {
        let cmd=new eoq2.Cmp()
        cmd.Crn('http://www.xgee.de/layout/v1/def','Edge',1)
        cmd.Set(new eoq2.Qry().His(-1),"refersTo",new eoq2.Obj(this.ecoreSync.rlookup(eObject)))
        cmd.Add(new eoq2.Obj(this.ecoreSync.rlookup(this.layout)),"contents",new eoq2.Qry().His(-2))
        if(supportPoints!=null)
        {
           
        }
        var result= await this.ecoreSync.remoteExec(cmd)
        return this.ecoreSync.getObjectById(result[0].v)
    }


    async getVertexLayoutItem(vertex)
    {
        var layout=await this.getLayout();       
        var parentVertex=null;
        var vertexLayoutItem=null;

        if(!this.cache.has(vertex))
        {

            if(vertex.parent && ( vertex.parent instanceof Vertex || vertex.parent instanceof Container))
            {
                parentVertex=await this.getVertexLayoutItem(vertex.parent) 
                if(!parentVertex) throw 'missing parent layout item'
            }

            if(parentVertex)
            {    
                let cmd=CMD.Get(new eoq2.Obj(this.ecoreSync.rlookup(layout)).Pth('contents').Cls('Vertex').Sel(new eoq2.Qry().Pth('refersTo').Equ(new eoq2.Obj(ecoreSync.rlookup(vertex.eObject)))).Sel(new eoq2.Qry().Pth('parent').Equ(new eoq2.Obj(this.ecoreSync.rlookup(parentVertex)))).Idx('FLATTEN').Trm(QRY.Met('SIZE').Equ(0),null).Idx(0))
                let result=await this.ecoreSync.remoteExec(cmd,true)

                if(result!=null)
                {
                    vertexLayoutItem=result;
                }
                else
                {
                    vertexLayoutItem=await this.createVertexLayoutItem(vertex.eObject,null,null,parentVertex)  
                }
            }
            else
            {
                let cmd=CMD.Get(new eoq2.Obj(this.ecoreSync.rlookup(this.layout)).Pth('contents').Cls('Vertex').Sel(new eoq2.Qry().Pth('refersTo').Equ(new eoq2.Obj(ecoreSync.rlookup(vertex.eObject)))).Idx('FLATTEN').Trm(QRY.Met('SIZE').Equ(0),null).Idx(0))
                let result=await this.ecoreSync.remoteExec(cmd,true)
                if(result!=null)
                {
                    vertexLayoutItem=result;
                }
                else{
                    vertexLayoutItem=await this.createVertexLayoutItem(vertex.eObject) 
                }          
            }

            this.cache.set(vertex,vertexLayoutItem);
        }
        else
        {
            vertexLayoutItem=this.cache.get(vertex);        
        }
        
        return vertexLayoutItem;
    }

    async getEdgeLayoutItem(edge)
    {  
        if(!this.layout){
            this.layout=await this.getLayout()
            if(!this.layout) throw 'Failed getting layout'
        }

       

        var parentVertex=null;
        if(edge.parent && edge.parent.eObject)
        {
            parentVertex=await this.getVertexLayoutItem(edge.parent) 
            if(!parentVertex) throw 'missing parent layout item'
        }

        if(parentVertex)
        {    
            let cmd=new eoq2.Get(new eoq2.Obj(this.ecoreSync.rlookup(this.layout)).Pth('contents').Sel(new eoq2.Qry().Met('CLASSNAME').Equ('Edge')).Sel(new eoq2.Qry().Pth('refersTo').Equ(new eoq2.Obj(ecoreSync.rlookup(edge.eObject)))).Sel(new eoq2.Qry().Pth('parent').Equ(new eoq2.Obj(this.ecoreSync.rlookup(parentVertex)))).Idx('FLATTEN'))
            let result=await this.ecoreSync.remoteExec(cmd)
            if(result.length)
            {
                return this.ecoreSync.utils.decode(result[0])
            }
            else
            {
                var edgeLayoutItem=await this.createEdgeLayoutItem(edge.eObject)
                await this.ecoreSync.set(edgeLayoutItem,"parent",parentVertex)
                return edgeLayoutItem
            }
        }
        else
        {

            let cmd=new eoq2.Get(new eoq2.Obj(this.ecoreSync.rlookup(this.layout)).Pth('contents').Cls('Edge').Sel(new eoq2.Qry().Pth('refersTo').Equ(new eoq2.Obj(ecoreSync.rlookup(edge.eObject)))).Idx('FLATTEN'))
            let result=await this.ecoreSync.remoteExec(cmd)

            if(result.length)
            {         
                return await this.ecoreSync.utils.decode(result[0])
            }
            else{
                return await this.createEdgeLayoutItem(edge.eObject)
            }          
           
        }
    }


    isVertexInLayout(vertex)
    {
        let entryKey=null
        let oid=this.ecoreSync.rlookup(vertex.eObject)  
        if(vertex.parent instanceof Vertex || vertex.parent instanceof Container )
        {
            pid=this.ecoreSync.rlookup(vertex.parent.eObject)
            entryKey=String(pid)+'.'+String(oid)
        }
        else
        {
            entryKey=String(oid)
        }
        return this.vertexCache.has(entryKey)
    }

    async getVertexPosition(vertex)
    {               
        var position={x:0,y:0, isDefault:true}
        let oid=this.ecoreSync.rlookup(vertex.eObject)      
        let pid=null
        if(oid)
        {

            
            let entryKey=null
            if(vertex.parent instanceof Vertex || vertex.parent instanceof Container )
            {
                pid=this.ecoreSync.rlookup(vertex.parent.eObject)
                entryKey=String(pid)+'.'+String(oid)
            }
            else
            {
                entryKey=String(oid)
            }

           

            if(this.vertexCache.has(entryKey))
            {
                position.x=this.vertexCache.get(entryKey).get('x')
                position.y=this.vertexCache.get(entryKey).get('y')
            }

        }
        else
        {

            try{        
                var vertexLayoutItem=await this.getVertexLayoutItem(vertex)
                if(vertexLayoutItem)
                {
                    position={x:await this.ecoreSync.get(vertexLayoutItem,"x"),y:await this.ecoreSync.get(vertexLayoutItem,"y")}
                }
                else
                {
                    throw 'missing layout item'
                }
            }
            catch(e)
            {
                console.error('Failed getting vertex position: '+e)
            }
            }
        return position;
    }


    async getVertexSize(vertex)
    {
        var size={x:0,y:0};

        let oid=this.ecoreSync.rlookup(vertex.eObject)      
        let pid=null
        if(oid)
        {            
            let entryKey=null
            if(vertex.parent instanceof Vertex || vertex.parent instanceof Container )
            {
                pid=this.ecoreSync.rlookup(vertex.parent.eObject)
                entryKey=String(pid)+'.'+String(oid)
            }
            else
            {
                entryKey=String(oid)
            }           

            if(this.vertexCache.has(entryKey))
            {
                size.x=this.vertexCache.get(entryKey).get('sizeX')
                size.y=this.vertexCache.get(entryKey).get('sizeY')
            }
        }
        else
        {
            try{        
                var vertexLayoutItem=await this.getVertexLayoutItem(vertex)
                if(vertexLayoutItem)
                {
                    size={x:await this.ecoreSync.get(vertexLayoutItem,"sizeX"),y:await this.ecoreSync.get(vertexLayoutItem,"sizeY")}
                }
                else
                {
                    throw 'missing layout item'
                }
            }
            catch(e)
            {
                console.error('Failed getting vertex size: '+e)
            }
        }
        return size;
    }

    async observeResource()
    {
        var self=this
        this.ecoreSync.observe(new eoq2.Obj(this.ecoreSync.rlookup(this.resource)).Pth('contents'),async function(contents){ 
            if(contents.length)
            {
                self.root=null
                self.layout=null
                self.root=await self.getRoot();
                self.layout=await self.getLayout();    
                self.vertexCache=new Map();
                await self.buildCache()
            }
        });
    }


    async observeVertexPosition(vertex,callback)
    {
        return true;
        var pos={x:0,y:0};
        var timeout = null;
        var timeoutInterval=100;
        var resetTimer=function(){
            if(timeout){ clearTimeout(timeout);  }  timeout=window.setTimeout(function(){ callback(pos); }, timeoutInterval);
        }

        try{        
            var vertexLayoutItem=await this.getVertexLayoutItem(vertex)
            if(vertexLayoutItem)
            {            
                this.ecoreSync.observe(new eoq2.Obj(this.ecoreSync.rlookup(vertexLayoutItem)).Pth('x'),function(val){ pos.x=val;    resetTimer();   });
                this.ecoreSync.observe(new eoq2.Obj(this.ecoreSync.rlookup(vertexLayoutItem)).Pth('y'),function(val){ pos.y=val;    resetTimer();   });
                return true
            }
            else
            {
                throw 'missing layout item'
            }
        }
        catch(e)
        {
            console.error('Failed observing vertex position: '+e)
        }
        return false
    }


    addTemporaryVertexPosition(objectId,parentObjectId,pos)
    {
        var tempPosition={objectId:objectId,parent:parentObjectId,pos:pos};
        this.temporaryPositions.push(tempPosition);
    }

    getTemporaryVertexPosition(objectId,parentObjectId)
    {
        var tempPosition=this.temporaryPositions.find(function(tempPos){
            return tempPos.objectId==objectId && tempPos.parent == parentObjectId
        })
        if(tempPosition){
            this.removeTemporaryVertexPosition(tempPosition);  
            return tempPosition.pos;
        }
        return null   
    }

    removeTemporaryVertexPosition(tempPosition)
    {
        var idx=this.temporaryPositions.indexOf(tempPosition)
        if(idx > -1)
        {
            this.temporaryPositions.splice(idx,1);
        }
    }


    async setVertexPosition(vertex,x,y)
    {
        var vertexLayoutItem=await this.getVertexLayoutItem(vertex)
        this.updates.Set(new eoq2.Obj(this.ecoreSync.rlookup(vertexLayoutItem)),"x",castToFloat(x))
        this.updates.Set(new eoq2.Obj(this.ecoreSync.rlookup(vertexLayoutItem)),"y",castToFloat(y))
        vertexLayoutItem.set('x',castToFloat(x))
        vertexLayoutItem.set('y',castToFloat(y))
        this.update();
        return vertexLayoutItem
    }




    async observeVertexSize(vertex,callback)
    {
        return true;
        var size={x:0,y:0};
        var timeout = null;
        var timeoutInterval=100;
        var resetTimer=function(){
            if(timeout){ clearTimeout(timeout);  }  timeout=window.setTimeout(function(){ callback(size); }, timeoutInterval);
        }

        try{        
            var vertexLayoutItem=await this.getVertexLayoutItem(vertex)
            if(vertexLayoutItem)
            {            
                this.ecoreSync.observe(new eoq2.Obj(this.ecoreSync.rlookup(vertexLayoutItem)).Pth('sizeX'),function(val){ size.x=val;    resetTimer();   });
                this.ecoreSync.observe(new eoq2.Obj(this.ecoreSync.rlookup(vertexLayoutItem)).Pth('sizeY'),function(val){ size.y=val;    resetTimer();   });
                return true
            }
            else
            {
                throw 'missing layout item'
            }
        }
        catch(e)
        {
            console.error('Failed observing vertex size: '+e)
        }
        return false
    }

    async setVertexSize(vertex,x=null,y=null)
    {
        var vertexLayoutItem=await this.getVertexLayoutItem(vertex)
        if(x!=null && y!=null)
        {
            this.updates.Set(new eoq2.Obj(this.ecoreSync.rlookup(vertexLayoutItem)),"sizeX",x)
            this.updates.Set(new eoq2.Obj(this.ecoreSync.rlookup(vertexLayoutItem)),"sizeY",y)
            this.update();
            return true
        }
    }

    async getEdgeSupportPoints(edge)
    {
        var edgeLayoutItem=await this.getEdgeLayoutItem(edge)   
        var fetchSupportPoints=new eoq2.Cmp()
        fetchSupportPoints.Get(new eoq2.Obj(this.ecoreSync.rlookup(edgeLayoutItem)).Pth('supportPoints'))
        fetchSupportPoints.Get(new eoq2.His(0).Pth('x'))
        fetchSupportPoints.Get(new eoq2.His(0).Pth('y'))
        fetchSupportPoints.Get(new eoq2.His(0).Pth('pointIndex'))
        let results=await this.ecoreSync.exec(fetchSupportPoints)
        return results[0]        
    }

    async updateEdge(edge,supportPoints)
    {
        if(supportPoints)
        {                  
            await this.clearEdgeSupportPoints(edge)
            let edgeLayoutItem=await this.getEdgeLayoutItem(edge)   

         
            // Process added support points           
            if(supportPoints.length)
            {
                let updateCmd=new eoq2.Cmp()
                updateCmd.Crn('http://www.xgee.de/layout/v1/def','Point',supportPoints.length)
                if(supportPoints.length > 1)
                {
                    let idx=0
                    for(let supportPoint of supportPoints)
                    {       
                        updateCmd.Set(new eoq2.His(0).Idx(idx),'x',castToFloat(supportPoint.x))           
                        updateCmd.Set(new eoq2.His(0).Idx(idx),'y',castToFloat(supportPoint.y))    
                        updateCmd.Set(new eoq2.His(0).Idx(idx),'pointIndex',idx)         
                        updateCmd.Add(new eoq2.Obj(this.ecoreSync.rlookup(edgeLayoutItem)),'supportPoints',new eoq2.His(0).Idx(idx))
                        idx+=1
                    }
                }
                else
                {
                    updateCmd.Set(new eoq2.His(0),'x',castToFloat(supportPoints[0].x))         
                    updateCmd.Set(new eoq2.His(0),'y',castToFloat(supportPoints[0].y))        
                    updateCmd.Add(new eoq2.Obj(this.ecoreSync.rlookup(edgeLayoutItem)),'supportPoints',new eoq2.His(0))
                }
                this.ecoreSync.exec(updateCmd)
            }           
        }
    }

    async clearEdgeSupportPoints(edge)
    {
        let edgeLayoutItem=await this.getEdgeLayoutItem(edge)
        await this.ecoreSync._esDomain.clear(edgeLayoutItem,'supportPoints')      
    }

    // async setEdgeSupportPoints(edge,supportPoints)
    // {      
    //     console.error('setting edge support points')  
    //     var edgeLayoutItem=await this.getEdgeLayoutItem(edge)
    //     let cmd=new eoq2.Cmp()
    //     cmd.Get(new eoq2.Obj(this.ecoreSync.rlookup(edgeLayoutItem)).Pth('supportPoints'))
    //     cmd.Rem(new eoq2.Obj(this.ecoreSync.rlookup(edgeLayoutItem)),"supportPoints",new eoq2.Qry().His(-1))
    //     if(supportPoints && Array.isArray(supportPoints) && supportPoints.length)
    //     {
    //         console.error('There are support points')
    //         cmd.Crn('http://www.xgee.de/layout/v1/def','Point',supportPoints.length)
    //         cmd.Add(new eoq2.Obj(this.ecoreSync.rlookup(edgeLayoutItem)),"supportPoints",new eoq2.Qry().His(-1))
    //         for(let i in supportPoints)
    //         {
    //             console.error(i);
    //             cmd.Set(new eoq2.His(-2-i).Idx(i),"x",castToFloat(supportPoints[i].x))
    //             cmd.Set(new eoq2.His(-3).Idx(i),"y",castToFloat(supportPoints[i].y))
    //         }
    //     }
    //     console.error(cmd);
    //     var result=await this.ecoreSync.exec(cmd)        
    //     return result;
    // }  
    
    //Removes entries from the layout model
    async clearEntries(objectIds){
        let objects=objectIds.filter((objId) => { return !Number.isNaN(objId)}).map((objId)=> { return new eoq2.Obj(objId)})   
        let lid=this.ecoreSync.rlookup(this.layout)

        if(objects.length && !Number.isNaN(lid))
        {
            console.info('Clearing '+objects.length+' entries from layout...')
            try{
                let cmd=new eoq2.Rem(new eoq2.Obj(lid),'contents',new eoq2.Arr(objects))
                this.ecoreSync.remoteExec(cmd) 
            }
            catch(e)
            {
                console.error('Failed to clear layout entries:'+e)
            }    
        }    
    }

}