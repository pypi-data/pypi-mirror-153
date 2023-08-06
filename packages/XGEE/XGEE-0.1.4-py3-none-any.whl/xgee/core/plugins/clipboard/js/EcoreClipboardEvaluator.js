import * as ClipboardEvaluator from "./ClipboardEvaluator.js"

class EcoreClipboardEvaluator extends ClipboardEvaluator.ClipboardEvaluator{
    constructor(){
        super();
      }

    canHandle(eObject){
        var res=false;
        if(eObject.eClass)
        {
            res=true;
        }
        return res;
    }

    async copy(eObject){
        //copy action handler
        var res=await ecoreSync.clone(eObject);
        return res;
    }

    async cut(eObject){
        //cut action handler
        await ecoreSync.remove(eObject.eContainer,eObject.eContainingFeature.get("name"),eObject);
        console.error('removed ')
        return eObject;    
    }

    canPaste(target,eObject,cmd){
        var res=false;
        if(target.eClass && eObject.eClass)
        {
            var refs=target.eClass.get('eAllReferences').filter(function(e){  return e.get("eType").get("_#EOQ")==eObject.eClass.get("_#EOQ")})
            var cnts=target.eClass.get('eAllContainments').filter(function(e){  return e.get("eType").get("_#EOQ")==eObject.eClass.get("_#EOQ")})

            if(refs.length+cnts.length==1)
            {
                if(refs.length==1 && cmd=='COPY')
                {
                    res=true;
                }
                if(cnts.length==1)
                {
                    res=true;
                }
            }
            else
            {
                if(target.eClass.get("_#EOQ")==eObject.eClass.get("_#EOQ")){
                    res=true;
                }
            }
        }
        return res;
    }

    async paste(target,eObject,cmd){
        //paste action handler
        //expects eObject to be the processed through copy/cut action handlers

    
            var refs=target.eClass.get('eAllReferences').filter(function(e){  return ecoreSync.rlookup(e.get("eType"))==ecoreSync.rlookup(eObject.eClass)})
            var cnts=target.eClass.get('eAllContainments').filter(function(e){  return ecoreSync.rlookup(e.get("eType"))==ecoreSync.rlookup(eObject.eClass)})

            if(refs.length+cnts.length==1)
            {      
                if(refs.length==1)
                {
                    if(cmd=='COPY')
                    {
                        if(refs[0].get('upperBound')!=1)
                        {
                            ecoreSync.add(target,refs[0].get('name'),eObject);
                        }
                        else
                        {
                            ecoreSync.set(target,refs[0].get('name'),eObject);
                        }
                    }
                }

                if(cnts.length==1)
                {            
                    if(cnts[0].get('upperBound')!=1)
                    {
                        ecoreSync.add(target,cnts[0].get('name'),eObject);
                    }
                    else
                    {
                        ecoreSync.set(target,cnts[0].get('name'),eObject);
                    }            
                }
            }
            else
            {                 

                if(ecoreSync.rlookup(target.eClass)==ecoreSync.rlookup(eObject.eClass))
                {
                    if(target.eContainingFeature.get('upperBound')!=1)
                    {
                        ecoreSync.add(target.eContainer,target.eContainingFeature.get('name'),eObject);
                    }
                    else
                    {
                        ecoreSync.set(target.eContainer,target.eContainingFeature.get('name'),eObject);
                    }
                }
            }    

    

    }
}

export { EcoreClipboardEvaluator }