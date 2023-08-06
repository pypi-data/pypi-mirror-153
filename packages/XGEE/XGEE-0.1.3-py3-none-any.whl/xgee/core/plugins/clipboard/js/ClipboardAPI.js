var clipboardManager=null;
var clipboardEvaluator=null;

class ClipboardPublicAPI{

    constructor(){ 
    }

    async write(data)
    {
        return clipboardManager.write(data);
    }
    
    async writeText(text)
    {
        return clipboardManager.writeText(text);
    }

    async read()
    {
        return clipboardManager.read();
    }


    async readText()
    {
        return clipboardManager.unpack(await clipboardManager.readText());
    }

    clear(){
        this.contents='';
    }

    hasContents(){
        if(this.contents!='')
        {
            return true
        }
        return false
    }

    evalEvent(event,data){
        var res=false;


        if(event.type=='copy')
        {
            clipboardManager.writeText(clipboardManager.pack({cmd:'COPY',contents:data}));
        } else if(event.type=='cut')
        {
            clipboardManager.writeText(clipboardManager.pack({cmd:'CUT',contents:data})); 
        } else if(event.type=='paste')
        {
            //Synchronize the clipboards
            if(clipboardManager){
                if(event.clipboardData){
                    clipboardManager.appWriteText(event.clipboardData.getData('text/plain'));
                }           
            }   
        }
        //clipboardManager.pack(data);
        return res;
    }

    copyEvent(event,data){
        var res=false;
        if(clipboardManager){
            if(event.clipboardData){        
                clipboardManager.writeText(clipboardManager.pack({cmd:'COPY',contents:data}));
            }
        }
        return res;
    }

    cutEvent(event){
        if(clipboardManager){
            if(event.clipboardData){
                clipboardManager.writeText(clipboardManager.pack({cmd:'CUT',contents:data}));
            }
        }
    }


    pasteEvent(event){
        var res=false;
        if(clipboardManager){
            if(event.clipboardData){
                clipboardManager.updateText(event.clipboardData.getData('text/plain'));
                res=true;
            }   
        }
        return res;
    }


    async hasContents(filter=null){
        var res=false;
        try{
            var data=JSON.parse(atob(await clipboardManager.readText()));
            
            if(data.hasOwnProperty('cmd') && data.hasOwnProperty('contents'))
            {
                var contents=[];
                if(Array.isArray(data.contents)){
                    contents=data.contents.map(function(e){
                        return ecoreSync.utils.getObjectByURL(e);
                    });;
                }
                else
                {
                    contents=[ ecoreSync.utils.getObjectByURL(data.contents)]
                }

                contents=await Promise.all(contents)

                if(filter){
                    try{
                        contents=contents.filter(filter);
                    }
                    catch(e){
                        contents=[]
                        console.error('clipboard error: failed to filter contents. '+e)
                    }
                }
                
                if(contents.length)
                {
                    res=true;
                }
            }
        }
        catch(e)
        {
            //clipboard context not readable as object
            console.error('clipboard error:'+e)
        }
        return res;
    }


        


    async getContents(filter=null,evaluateCmd=true){
        var res=null;
        try{
            var data=JSON.parse(atob(await clipboardManager.readText()));
            
            if(data.hasOwnProperty('cmd') && data.hasOwnProperty('contents'))
            {
                      
                if(Array.isArray(data.contents))
                {                
                    res=data.contents.map(function(e){
                        return ecoreSync.utils.getObjectByURL(e);
                    });;
                }
                else
                {
                    res=[ecoreSync.utils.getObjectByURL(data.contents)]
                }

                res=await Promise.all(res)

                if(filter){
                    res=res.filter(filter);
                }

                if(evaluateCmd)
                {               
                    if(data.cmd=='COPY')
                    {        
                        let copy=async (content) => { return clipboardEvaluator.copy(await content); };             
                        let copiedContents=[];
                        res.forEach(function(content){                           
                            copiedContents.push(copy(content));
                        });            
                        res=await Promise.all(copiedContents);
                        
                    }

                    if(data.cmd=='CUT')
                    {            
                        let cut=async (content) => { return clipboardEvaluator.cut(await content); };              
                        let cutContents=[];
                        res.forEach(function(content){
                            cutContents.push(cut(content));
                        });
                        res=await Promise.all(cutContents);
                    }                  
                }
     
            }
        }
        catch(e)
        {
            //clipboard context not readable as object
            console.error('clipboard error:'+e);
        }
        return res;
    }



    async pasteToEObject(target,filter=null){
        //this is a fire&forget solution if you don't want to intervene with the paste process
        //this only works, if the clipboard contains object urls 
        //be aware, that this pastes the clipboard to the best match within the eObject's references
        if(clipboardEvaluator){     
                let contents=await this.getContents(filter);
                if(contents){
                    contents.forEach(function(content){
                        clipboardEvaluator.paste(target,content);
                    })
                }
                else
                {
                    console.error('nothing to paste');
                }             
            }       
    }
    

}

class ClipboardPrivateAPI{
    constructor(){

    }
    setClipboardManager(manager){
        clipboardManager=manager;
    }

    setClipboardEvaluator(evaluator){
        clipboardEvaluator=evaluator;
    }
}



var pub=new ClipboardPublicAPI();
var priv=new ClipboardPrivateAPI();
export {pub,priv}