class ApplicationClipboard{

    constructor(){
        this.contents='';
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


}

export {ApplicationClipboard}