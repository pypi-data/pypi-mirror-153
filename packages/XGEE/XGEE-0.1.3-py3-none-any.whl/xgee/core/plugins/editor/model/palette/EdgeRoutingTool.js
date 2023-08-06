import GraphTool from './GraphTool.js'
import { replaceTemplates } from '../../lib/libaux.js'



class EdgeDefinition{
    constructor(ecoreSync,model){
        this.ecoreSync=ecoreSync
        this.model=model
        this.anchors=this.model.get('anchors').array()        
    }    

    isStrict()
    {
        return this.model.get('isStrict')?true:false
    }

    async getAnchorTypes(vertices)
    {
        let ts=new eoq2.serialization.TextSerializer();
        var self=this
        let anchorTypes=vertices.map((v)=>{ return [] })
        let encodedEObjects=this.ecoreSync.utils.encode(vertices.map( (v) => v.eObject )) 
        for(let i=0;i<this.anchors.length;i++)
        {
            if(this.anchors[i].get('selectionQuery')!=null &&  this.anchors[i].get('selectionQuery')!='')
            {
                let cmd=new eoq2.Cmp()
                encodedEObjects.forEach( (o) => {
                    // cmd.Get(eval('new eoq2.Obj('+o.v+').'+this.anchors[i].get('selectionQuery')))
                    let cmdStr = "#"+o.v + this.anchors[i].get('selectionQuery')
                    let addCmd = ts.deserialize(cmdStr)
                    console.log('Anchor cmdStr:            '+ cmdStr)
                    cmd.Get(addCmd)
                })    

                //remote call due to performance issues of the local query runner
                let selectionResults=await this.ecoreSync.remoteExec(cmd)             
                vertices.forEach((v,idx)=>{
                    if(selectionResults[idx])
                    {
                        anchorTypes[idx].push(self.anchors[i])
                    }
                })                
            }
        }

        return anchorTypes
    }
}


export default class EdgeRoutingTool extends GraphTool{
    constructor(...args){
        super(...args)
        var self=this
        this.isActive=false;
        this.isEdgeTool=true;
        this.elementId=null;
        this.template=null;
        this.edgeItem=null;
        this.anchorCache=[]; //holds the currently known valid targets

        //Initialize edge definitions
        var edgeDefinitions=this.toolDefinition.get('edgeDefinitions').array()
        this.edgeDefinitions=edgeDefinitions.map((def) => {
            return new EdgeDefinition(self.ecoreSync,def)
        })
    }    

    async activate(){
        if(super.activate()) await this.enableConnectables();
    }

    async deactivate(){
        if(super.deactivate()){
            this.anchorCache=[];
            this.disableConnectables();   
        }
    }

    async isAnchor(eObject)
    {
        var anchors=this.toolDefinition.get("anchors").array();        
        for(let i in anchors)
        {                        
            if(eObject.eClass.get("name")==anchors[i].get("className") && eObject.eClass.eContainer.get("nsURI") == anchors[i].get("nsURI"))
            {
                var res=false;
                if(anchors[i].get("isConditional"))
                {
                    let valueSet={};
                    valueSet["ANCHOR"]=this.ecoreSync.rlookup(eObject);  
                    // TODO this probably needs to be converted to text                  
                    let cmd=eval(replaceTemplates(valueSet,'new eoq2.Get(new eoq2.Obj('+this.ecoreSync.rlookup(eObject)+').'+anchors[i].get("condQuery")+')'));
                    res=await this.ecoreSync.exec(cmd);
                }
                else
                {
                    res=true;
                }
                if(res) { return true }                                             
            }               
        }
        return false                 
    }

    async getAnchorType(eObject)
    {
        var anchors=this.toolDefinition.get("anchors").array();        
        for(let i in anchors)
        {                        
            if(eObject.eClass.get("name")==anchors[i].get("className") && eObject.eClass.eContainer.get("nsURI") == anchors[i].get("nsURI"))
            {
                var res=false;
                if(anchors[i].get("isConditional"))
                {
                    // TODO this probably needs to be converted to text
                    let cmd=eval('new eoq2.Get(new eoq2.Obj('+this.ecoreSync.rlookup(eObject)+').'+anchors[i].get("condQuery")+')');
                    res=await this.ecoreSync.exec(cmd);
                }
                else
                {
                    res=true;
                }
                if(res) { return anchors[i] }                                             
            }               
        }
        return null   
    }

    async filterConnectables(vertices,cache=false){
        var self=this
        var selection=vertices.map((v) => { return false })
        
        if(!this.edgeDefinitions.length)
        {
           console.error('Edge definitions missing')
        }
        else
        {
        
            for(let j=0;j<this.edgeDefinitions.length;j++)
            {
                //Get All Anchor Types of the Edge Definition for all vertices
                let anchorTypes=await this.edgeDefinitions[j].getAnchorTypes(vertices)

                
                for(let i=0;i<vertices.length;i++)
                {                      
                    if(anchorTypes[i].length)
                    {                  
                        selection[i]=true
                        if(cache){
                            anchorTypes[i].forEach(anchorType => {
                                self.anchorCache.push({eObject:vertices[i].eObject,edgeDefinition:this.edgeDefinitions[j],anchorType:anchorType}); 
                            })
                        }
                    }

          
                }
            }
    
        }       

        return selection
    }

    async enableConnectables(){
        var self=this
        this.anchorCache=[];
        this.palette.graphController.setConnectable(async (vertices) => { return self.filterConnectables(vertices,true) })
    }

    disableConnectables(){
        var self=this
        this.palette.graphController.setNotConnectable(async (vertices) => { return self.filterConnectables(vertices,false) });
        this.anchorCache=[];
    }

    async init(){   
        if(!this.toolDefinition) { throw 'tool initialization failed, because no definition was provided' }
        let template=await this.initTemplate()
        if(template)
        {
        this.edgeItem=ecoreSync.clone(this.template)
        await self.ecoreSync.utils.isEClassInitialized(this.edgeItem.eClass)
        }
    }

    getEdgeSpan(source,target)
    {
        var edgeSpan={valid:false, edgeDefinition:null, source:null,target:null,inverted:false};       

        //Collect possible anchors
        var allSourceAnchors=this.anchorCache.filter(function(e){
            return (e.eObject==source || (!e.edgeDefinition.isStrict() && e.eObject==target)) && (e.anchorType.get('type')=='SOURCE' || e.anchorType.get('type')=='BOTH' || e.anchorType.get('type')==null)
        });

        var allTargetAnchors=this.anchorCache.filter(function(e){
            return (e.eObject==target || (!e.edgeDefinition.isStrict() && e.eObject==source)) && (e.anchorType.get('type')=='TARGET' || e.anchorType.get('type')=='BOTH' || e.anchorType.get('type')==null)           
        });
 
  

        for(let sourceAnchor of allSourceAnchors)
        {
            for(let targetAnchor of allTargetAnchors)
            {
                if(sourceAnchor.edgeDefinition == targetAnchor.edgeDefinition)
                {
                    //Match found
                    edgeSpan.edgeDefinition=sourceAnchor.edgeDefinition
                    edgeSpan.source=sourceAnchor
                    edgeSpan.target=targetAnchor
                    
                    //Inversion check
                    if(sourceAnchor.eObject == source && targetAnchor.eObject == target)
                    {
                        edgeSpan.valid=true
                        edgeSpan.inverted=false
                    }
                    else if(!edgeSpan.edgeDefinition.isStrict() && sourceAnchor.eObject == target && targetAnchor.eObject == source)
                    {
                        edgeSpan.valid=true
                        edgeSpan.inverted=true
                    } 

                    break
                }
            }
        }

        return edgeSpan
    }


    canCreate(source,target)
    {
        var edgeSpan=this.getEdgeSpan(source,target)
        return edgeSpan.valid
        sourceAnchor=sourceAnchor ? sourceAnchor.anchor : null
        targetAnchor=targetAnchor ? targetAnchor.anchor : null

        //Sanity check
        if(sourceAnchor && !sourceAnchor.get('type')){
            console.warn('source Anchor type undefined, defaulted to BOTH')
            sourceAnchor.set('type','BOTH')
        }

        if(targetAnchor && !targetAnchor.get('type')){
            console.warn('target Anchor type undefined, defaulted to BOTH')
            targetAnchor.set('type','BOTH')
        }

        if(sourceAnchor && targetAnchor)
        {
            //strict cases where only source->target
            let strictCases={
                "CASE_SOURCE_TO_TARGET": sourceAnchor.get('type')=='SOURCE' && targetAnchor.get('type')=='TARGET',
                "CASE_SOURCE_TO_BOTH": sourceAnchor.get('type')=='SOURCE' && targetAnchor.get('type')=='BOTH',
                "CASE_BOTH_TO_BOTH": sourceAnchor.get('type')=='BOTH' && targetAnchor.get('type')=='BOTH',
                "CASE_BOTH_TO_TARGET": sourceAnchor.get('type')=='BOTH' && targetAnchor.get('type')=='TARGET',
            }

            //non-strict cases where target->source is allowed
            let nonStrictCases={
                "CASE_TARGET_TO_SOURCE": sourceAnchor.get('type')=='TARGET' && targetAnchor.get('type')=='SOURCE',
                "CASE_TARGET_TO_BOTH": sourceAnchor.get('type')=='TARGET' && targetAnchor.get('type')=='BOTH',
                "CASE_BOTH_TO_SOURCE": sourceAnchor.get('type')=='BOTH' && targetAnchor.get('type')=='SOURCE',
            }

            let keys=Object.keys(strictCases);            
            for (let i = 0; i < keys.length; i++) {
                results=results||strictCases[keys[i]]
                if(results) break;
            }

            if(!isStrict && !results)
            {
                let keys=Object.keys(nonStrictCases);     
                for (let i = 0; i < keys.length; i++) {
                    results=results||nonStrictCases[keys[i]]
                    if(results) break;
                }
            }      
        }

        return results;
    }

    async getEdgeItem(){
        let edgeItem=this.edgeItem
        this.edgeItem=ecoreSync.clone(this.template)
        return await edgeItem
    }

    getCmd(edgeItem){
        let valueSet={"ROOT":this.ecoreSync.rlookup(this.palette.graphController.eObject),"EDGE_ITEM":this.ecoreSync.rlookup(edgeItem)}      
        return eval(replaceTemplates(valueSet,this.toolDefinition.get("cmd")))
        // TODO this probably needs to be converted to text
    }

    async routeEdge(edgeDefinition,source, target){
        let ts=new eoq2.serialization.TextSerializer();

        let valueSet={"ROOT":this.palette.graphController.eObject,"SOURCE":source,"TARGET":target} 

        if(this.toolDefinition.get("providesTemplate"))
        {
            let edgeItem=await this.getEdgeItem()
            valueSet["EDGEITEM"]=edgeItem
        }
     
        let routingCmd=new eoq2.Cmp();

        let routingCmds=edgeDefinition.model.get("routingCmd").get("cmds").array();

        routingCmds.forEach(function(cmd){
            try{
                let cmdStr = replaceTemplates(valueSet,cmd.get("cmdStr"))
                let addCmd = ts.deserialize(cmdStr)
                routingCmd.a.push(addCmd);
                // eval('routingCmd.'+replaceTemplates(valueSet,cmd.get("cmdStr")));
            }
            catch(e)
            {
                console.error('routing cmd failed: '+e,'cmd:'+cmd.get("cmdStr"));
                throw e
            }
        })
  
       await this.ecoreSync.exec(routingCmd);
    }

    async create(source,target)
    {     

        var self=this;
        let inverted=false
        var edgeSpan=this.getEdgeSpan(source,target)

        //Check if edge span is valid
        if(!edgeSpan.valid || edgeSpan.edgeDefinition.isStrict() && edgeSpan.inverted)
        {
            throw 'edge span is invalid'
        }

        if(!edgeSpan.inverted)
        {
            this.routeEdge(edgeSpan.edgeDefinition,source,target)
        }
        else
        {
            this.routeEdge(edgeSpan.edgeDefinition,target,source)
        }
        
       

       return true
    
     
    
       
        
        var sourceAnchor=this.anchorCache.find(function(e){
            return e.eObject==source
        });
        var targetAnchor=this.anchorCache.find(function(e){
            return e.eObject==target        
        });

        sourceAnchor=sourceAnchor ? sourceAnchor.anchor : null
        targetAnchor=targetAnchor ? targetAnchor.anchor : null
        
        if(sourceAnchor && !sourceAnchor.get('type')){
            console.warn('source Anchor type undefined, defaulted to BOTH')
            sourceAnchor.set('type','BOTH')
        }

        if(targetAnchor && !targetAnchor.get('type')){
            console.warn('target Anchor type undefined, defaulted to BOTH')
            targetAnchor.set('type','BOTH')
        }                 

        if(sourceAnchor && targetAnchor)
        {
            //strict cases where only source->target
            let strictCases={
                "CASE_SOURCE_TO_TARGET": sourceAnchor.get('type')=='SOURCE' && targetAnchor.get('type')=='TARGET',
                "CASE_SOURCE_TO_BOTH": sourceAnchor.get('type')=='SOURCE' && targetAnchor.get('type')=='BOTH',
                "CASE_BOTH_TO_BOTH": sourceAnchor.get('type')=='BOTH' && targetAnchor.get('type')=='BOTH',
                "CASE_BOTH_TO_TARGET": sourceAnchor.get('type')=='BOTH' && targetAnchor.get('type')=='TARGET',
            }

            //non-strict cases where target->source is allowed
            let nonStrictCases={
                "CASE_TARGET_TO_SOURCE": sourceAnchor.get('type')=='TARGET' && targetAnchor.get('type')=='SOURCE',
                "CASE_TARGET_TO_BOTH": sourceAnchor.get('type')=='TARGET' && targetAnchor.get('type')=='BOTH',
                "CASE_BOTH_TO_SOURCE": sourceAnchor.get('type')=='BOTH' && targetAnchor.get('type')=='SOURCE',
            }

            let keys=Object.keys(strictCases);            
            for (let i = 0; i < keys.length; i++) {
                if(strictCases[keys[i]])
                {
                    matched=true   
                    inverted=false               
                    break;
                }
                
            }

            if(!isStrict && !matched)
            {
                let keys=Object.keys(nonStrictCases);     
                for (let i = 0; i < keys.length; i++) {
                    if(nonStrictCases[keys[i]])
                    {
                        matched=true
                        inverted=true
                        break;
                    }
                }
            }      
        }    
           
        if(matched && source && target)
        {
           if(!inverted){
                this.routeEdge(source,target)
           }
           else
           {
                this.routeEdge(target,source)
           }
           
        }
        else
        {
            throw 'edge routing tool: no suitable match found'
        }
    }
}