import { replaceTemplates } from '../lib/libaux.js'

/**
 * XGEE Query module
 * @author Matthias Brunner
 * @copyright 2019-2021 University of Stuttgart, Institute of Aircraft Systems, Matthias Brunner
*/

/** Generic Query builder class */
class Query
{

    /**
     * Create a graph view and its outline 
     * @param {ecoreSyncInstance} ecoreSync - The ecoreSync instance used by this query object.
     * @param {string} alias - The alias the result value is associated with.
     * @param {string} queryStr - The raw query from the XGEE model containing palceholders {ALIAS}.
     * @param {string} queryTarget - The object this query should use as the query root segment identified by a literal alias (e.g. PARENT). The literal is used to access the valueSet when the query is built.
     * @param {string} queryTargetAlias - The literal alias that should be used for getting the queryTarget, only evaluated if queryTarget=CUSTOM
     */
    constructor(ecoreSync,alias,queryStr,queryTarget,queryTargetAlias)
    {
        this.ecoreSync=ecoreSync
        if(ecoreSync==null)
        {
            console.trace()
            throw 'FATAL ERROR: ecoreSync handle not provided while defining a query'
        }
        this.alias=alias;
        this.queryStr=queryStr;
        this.queryTarget=queryTarget;
        this.queryTargetAlias=queryTargetAlias;      
    }

    /**
     * Builds the query and replaces the placeholders so that it can be evaluated with EOQ
     * @param {directory} valueSet - The valueSet contains values from previous queries (e.g. of parent graph objects) and the automatically set literals (e.g. PARENT, MODELROOT etc.)
     * @param {boolean} [noEval=false] - Flag indicating wether evaluation of the query string into a EOQ query should be suppressed. By default the string is evaluated and the return value is a EOQ query object. Otherwise the unevaluated string is returned.
     * @returns {EOQQuery|string} Returns a EOQ query object if noEval=False, otherwise the unevaluated string is returned
    */
    build(valueSet,noEval=false)
    {
        var res=null
        var cmd="";
        var ts=new eoq2.serialization.TextSerializer();

        if($DEBUG) console.debug('Query from model:      ' + this.queryStr + ', Query target: ' + this.queryTarget);
        //Setting Query Target

        //Sanity checks
        if($DEBUG){
            if(!valueSet){
                console.error(valueSet);
                throw 'no value set was supplied'
            }
            if(!Object.keys(valueSet).length)
            {
                throw 'value set is empty';
            }
        }
        
        switch(this.queryTarget)
        {
            case "CUSTOM":
                cmd += '#' + this.ecoreSync.rlookup(valueSet[this.queryTargetAlias])
                // TODO adapt
                break;
            case "ROOT":
                cmd += '#' + this.ecoreSync.rlookup(valueSet["ROOT"])
                // TODO not sure if it is working
                break;
            case "MODELROOT":
                cmd += '#' + this.ecoreSync.rlookup(valueSet["MODELROOT"])
                break;
            case "EDITORROOT":
                cmd += '#' + this.ecoreSync.rlookup(valueSet["EDITORROOT"])
                break;
            case "PARENT":
                cmd += '#' + this.ecoreSync.rlookup(valueSet["PARENT"])
                break;
            case "RESOURCE":
                cmd += '#' + this.ecoreSync.rlookup(valueSet["RESOURCE"])
                break;
            case "DETACHED":
                break;
            default:
                cmd+="#0"
        }

        cmd+=this.queryStr+""  
        cmd=replaceTemplates(valueSet,cmd) 
        res=cmd
        if(!noEval)
        {
            try{
                res=ts.deserialize(cmd);
                if($DEBUG) console.debug('Deserialized command: ' + res.toString());
            }
            catch(e)
            {
                console.error(valueSet);
                console.error('Query evaluation failed: '+e)
                throw e
            }
        }
        return res
    }


    /**
     * Creates the value sets for an result array
     * @param {directory} valueSet - The valueSet contains values from previous queries (e.g. of parent graph objects) and the automatically set literals (e.g. PARENT, MODELROOT etc.)
     * @param {Array|eObject} results - The results returned from a query for which the respective valueSets should be created. Can be a list of eObjects or a single eObject.
     * @returns {Array|dictionary} Returns an array of valueSets if multiple eObjects were supplied, otherwise a single valueSet dictionary is returned.
    */
    async makeValueSets(valueSet,results){
        var self=this;
        if(Array.isArray(results))
        {
            let vSets=[];
            var fillVSet=async (vSet,eObject) => {
                vSet["MODELROOT"]=await this.ecoreSync.utils.getModelRoot(eObject)
                vSet["RESOURCE"]=await this.ecoreSync.utils.getResource(eObject)    
                return vSet;
            };
            for(let i=0;i<results.length;i++)
            {
                let vSet=Object.assign({},valueSet);
                if(self.alias)
                {
                    vSet[self.alias]=results[i];
                }
                vSet["PARENT"]=results[i]
            
                vSets.push(fillVSet(vSet,results[i]));
            }
            return Promise.all(vSets);
        }
        else
        {
            let vSet=Object.assign({},valueSet);
            if(self.alias)
            {
                vSet[this.alias]=results;                
            }            
            vSet["PARENT"]=results
            vSet["MODELROOT"]=await this.ecoreSync.utils.getModelRoot(results)
            vSet["RESOURCE"]=await this.ecoreSync.utils.getResource(results)
            
            return vSet
        }
    }

    /**
     * Checks wether an alias was specified for this query
     * @returns {boolean} Returns true if a valid alias was specified, false otherwise.
    */
    hasAlias(){
        if(this.alias){
            return true
        }
        return false
    }
    
    /**
     * Gets the alias specified for this query.
     * @returns {string} Returns the literal alias specified for this query.
    */
    getAlias(){
        return this.alias
    }

}

export default Query
