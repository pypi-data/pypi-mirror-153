/**
 * GraphInteraction module
 * @author Matthias Brunner
 * @copyright 2019-2021 University of Stuttgart, Institute of Aircraft Systems, Matthias Brunner
*/

/** Generic class for the description of graph interactions
 * @abstract
*/
class GraphInteraction{

    /**
     * Create the graph interaction
     * @param {ecoreSyncInstance} ecoreSync - The ecoreSync instance used by this graph interaction
     */
    constructor(ecoreSync){
        this.ecoreSync=ecoreSync;
        this.nsURI='';
        this.className='';
    }

    /**
    * Gets the namespace URI of the class associated with this interaction
    * @returns {string} - The namespace URI of the package containg the class this interaction is applicable to
    */
    getNsURI(){
        return this.nsURI
    }
    
    /**
    * Gets the name of the class associated with this interaction
    * @returns {string} - The name of the class this interaction is applicable to
    */
    getClassName(){
        return this.className
    }

}


export default GraphInteraction