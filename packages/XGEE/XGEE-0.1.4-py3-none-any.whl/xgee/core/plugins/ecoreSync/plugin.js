/* ecoreSync v2.0.0 plugin for jsApplication */
/*(C) 2020 Institute of Aircraft Systems, Matthias Brunner */

import EcoreSync from "./ecoreSync.js"
var ecoreSync=null;

export async function init(pluginAPI,config) {
    //initialize ecoreSync   

    await pluginAPI.loadScripts(['queries/esQueryUtils.js']);
    
    ecoreSync=new EcoreSync(pluginAPI.require('eventBroker'));

    let instances=[];
    for(let i=0;i<config.instances.length;i++) {
        let params = config.instances[i];
        let eoq2Domain = pluginAPI.require('eoq2').instances[params.eoq2DomainId];
        if(eoq2Domain){
            instances.push(ecoreSync.getInstance(eoq2Domain,params.ecoreSyncId));
        }
        else
        {
            console.error('An invalid EOQ2 domain was specified for the ecoreSync instance id='+config.id);
        }
    }

    if($DEBUG) console.debug('Initialized '+instances.length+' instance(s) of ecoreSync during startup')


    //expose ecoreSync instance API
    pluginAPI.expose(ecoreSync)
    return true;
};

export var meta={
        id:"ecoreSync",
        description:"Ecore object synchronization via EOQ (v2)",
        author:"Matthias Brunner",
        date:"2020-07-01",
        version:"2.0.0",
        requires:[
            'ecore',
            'eoq2',
            'eventBroker'
        ]
    };


