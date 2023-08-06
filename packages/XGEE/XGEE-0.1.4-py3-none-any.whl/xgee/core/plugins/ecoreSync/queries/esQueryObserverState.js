//ecoreSync observer state for query observers
//(C) 2020 Matthias Brunner / University of Stuttgart, Institute of Aircraft Systems

export default class EsQueryObserverState{
    constructor(){
        this.results=null;
        this.deltaPlus=null;
        this.deltaMinus=null;
    }

    update(results){
        var self=this;

        if(Array.isArray(results) && Array.isArray(this.results))
        {
           if(results.length == this.results.length)
           {    
                let compResult=true;
                results.forEach(function(e,i){
                    compResult=compResult && (e == self.results[i])
                })
                if(compResult) return false //No update
           }           

        }
        else
        {
            if(this.results == results) return false //No update
        }
        
        if(!this.results)
        {
            this.results=results;
            this.deltaPlus=results;
            this.deltaMinus=[];
        }
        else
        {
                if(!Array.isArray(results))
                {
                    this.deltaMinus=this.results; 
                    this.deltaPlus=results;
                    this.results=results;
                }
                else
                {
                    if(results)
                    {
                        if(Array.isArray(results))
                        {              
                            if(this.results)
                            {     
                            this.deltaPlus=results.filter(x => !self.results.includes(x));
                            this.deltaMinus=this.results.filter(x => !results.includes(x));
                            this.results=[...results];
                        }
                        else
                        {
                            this.results=results;
                            this.deltaPlus=results;
                            this.deltaMinus=[];
                        }
                    }
                    else
                    {    
                        this.results=results;
                        this.deltaMinus=results;
                        this.deltaPlus=[];
                    }
                }
            }
        }  
        
        return true;
    }

    getResults(){
        return this.results;
    }

    getDeltaPlus()
    {
        return this.deltaPlus;
    }

    getDeltaMinus()
    {
        return this.deltaMinus;
    }
}