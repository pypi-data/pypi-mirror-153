//ecoreSync model database
import EsModelDatabase from '../mdb/esModelDatabase.js'
import EsLookup from './esLookup.js'
import EsMdbAccessor from '../mdb/esMdbAccessor.js'

//ecoreSync internal operation handling
import EsOperationHandling from './esOperationHandler.js'

//ecoreSync object synchronization
import EsObjectAccessors from './esObjectAccessors.js'
import EsMetaSync from './esMetaSync.js'

//EOQ queries for ecoreSync
import EsQueries from '../queries/esQueries.js'
import EsCmdRunner from '../queries/esCmdRunner.js'

import EsChanges from '../changes/esChanges.js'

//Auxiliaries and utilities
import * as aux from '../util/auxiliaries.js'
import EsUtils from '../util/esUtils.js'

export default class EsDomain extends aux.multipleClasses(EsLookup,EsObjectAccessors,EsMetaSync,EsOperationHandling,EsQueries,EsUtils){
    constructor(eoq2domain,eventBroker,esInstance){
        super();
        this.eoq2domain=eoq2domain;
        this.eventBroker=eventBroker;
        this.esInstance=esInstance;
        this.changes=new EsChanges(this);

        //domain model-database
        this.mdb=new EsModelDatabase(esInstance,eventBroker);
        this.mdbAccessor=new EsMdbAccessor(this);
        this.cmdRunner=new EsCmdRunner(this);
    }

    getEoqDomain(){
        return this.eoq2domain;
    }

} 

