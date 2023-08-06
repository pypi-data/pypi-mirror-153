
class ClipboardManager{

    constructor(appClipboard=null,useSystemClipboard=true,preferAppClipboard=false){ 
        this.appClipboard=appClipboard;
        this.useSystemClipboard=useSystemClipboard;
        this.preferLocalClipboard=preferAppClipboard;
    }

    setAppClipboard(clipboard)
    {
        this.appClipboard=clipboard;
    }

    async writeText(text){
        if(this.appClipboard)
        {
            this.appClipboard.writeText(text);
        }
        try{
            navigator.clipboard.writeText(text);
        }catch(e){
            //failed to write to system clipboard
        }
    }

    async readText(){
        var res=null;
        if(!this.appClipboard || this.appClipboard && !this.preferLocalClipboard)
        {
            try{
                res=await navigator.clipboard.readText(text);
            }
            catch(e){
                //failed to read from system clipboard, attempt fallback to application clipboard
                if(this.appClipboard) { res=await this.appClipboard.readText(); }
            }
        }
        else
        {
            if(this.appClipboard) { res=await this.appClipboard.readText(); }
            if(res==null)
            {
                //attempt to read from the system clipboard, because the application clipboard was empty or not present
                try{
                    res=await navigator.clipboard.readText(text);
                }
                catch(e)
                {
                    //failed to read from system clipboard as well
                }
            }
      
        }
        return res;
    }

    async sync(){
        if(this.appClipboard){
            if(this.preferAppClipboard){
                try{
                    navigator.clipboard.writeText(this.appClipboard.readText());
                }catch(e){
                    //failed to write to system clipboard
                }
            }
            else
            {
                try{
                    var res=await navigator.clipboard.readText();
                    if(res!=null)
                    {
                        this.appClipboard.writeText(res);
                    }
                }catch(e){
                    //failed to update app clipboard from system clipboard
                }
            }
        }   
    }

    async appWriteText(text)
    {
        if(this.appClipboard)
        {
            this.appClipboard.writeText(text);
        }
    }

    pack(data){   
        var res=data;                   
        if(typeof data=='string')
        {
            this.writeText(data);
            res=true;
        }
        else
        {
            try{
                data=btoa(JSON.stringify(data));         
                res=data;
            }catch(e){
                //contents could not be processed
                console.error('clipboard data not processed: '+e)
            }
        }   
        return res;
    }

    unpack(data){
        var res=null;
        try{
            if(typeof data=='string')
            {
               res=data;
               res=JSON.parse(atob(data)); 
            }
            else
            {
                res=data;
            }
        }catch(e){
            //unpacking failed
        }
        return res;
    }

}

export {ClipboardManager}