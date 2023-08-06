import * as AppClipboard from "./AppClipboard.js"

var clipboardContents='';


class ClipboardPublicAPI{

    constructor(){ 
    }

    async writeText(text)
    {
        if((typeof text)=='string')
        {
            this.contents=text;
        }
    }

    async readText()
    {
        return this.contents;
    }

    async write(serializableObject)
    {
        try{
            this.contents=JSON.stringify(serializableObject);
        }
        catch(e)
        {
            console.warn('could not write non-serializable object to clipboard')
        }

    }

    async read()
    {
        var res=null;
        try{
            res=JSON.parse(this.contents);
        }
        catch(e)
        {
            console.warn('clipboard context not readable as object')
        }
        return res;
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

    updateFromDataTransfer(dataTransfer){
        this.contents=dataTransfer.getData('text/plain');
    }




}

class ClipboardPublicAPI{

}



var clipboardPublicAPI=new ClipboardPublicAPI();
var clipboardPrivateAPI=new ClipboardPublicAPI();
export {clipboardPublicAPI,clipboardPrivateAPI}