class EcoreSyncDebugger{

    constructor(ecoreSync,eventBroker){
        this.ecoreSync=ecoreSync;
        this.eventBroker=eventBroker;
    }

    async trace(cmd,stack,res,mode='auto'){
        var self=this;
        var traceStart=new Date();
        var results=await res  
        var traceEnd=new Date();  
        let queryTraceData = {
            cmd: cmd,
            queryString: this.ecoreSync.textSerializer.cmdTranslator(cmd), // string representation will become available once jseoq is updated
            queryDuration: traceEnd.getTime() - traceStart.getTime(), // in ms
            queryResult: results, //is currently not the same for locally and remotely queries! 
            queryId: 0, // query id returned from eoq
            queryIssuer: 'ecoreSync', // component string of query issuer
            queryStackTrace: stack.split('\n'), // stack trace that lead to query
            queryMode: mode, // as shown in your table (not sure what it does)    
            dateStart: traceStart, // datetime when query was sent
            dateEnd: traceEnd, // datetime when response was received    
            dataTarget: 'unknown', // optional css selector for element that shall receive data from query
        }
        this.publishQueryTraceData(queryTraceData);
    }

    rerun(queryTraceData){
        if(queryTraceData.mode=='auto'){ return this.ecoreSync.exec(queryTraceData.cmd); } if(queryTraceData.mode=='remote'){ return this.ecoreSync.remoteExec(queryTraceData.cmd);}
    }

    async compareExecModes(cmd)
    {
        var remStart=new Date();
        var remoteResult=await this.ecoreSync.remoteExec(cmd); 
        var remoteDecodedResult=await this.ecoreSync.decode(remoteResult.v);
        var remEnd=new Date(); 

        var lclStart=new Date();
        var localResult=await this.ecoreSync.exec(cmd); 
        var lclEnd=new Date(); 

        var lResult=await ApplyToAllElements(localResult,this.ecoreSync.encode)
        var rResult=remoteResult.v
        var resultsMatch=JSON.stringify(lResult)==JSON.stringify(rResult)

        var remDur=remEnd.getTime()-remStart.getTime();
        var lclDur=lclEnd.getTime()-lclStart.getTime();

        return {remDuration: remDur, lclDuration: lclDur, resultsMatch: resultsMatch, lclResult: lResult, remResult: rResult, lclDecodedResult: localResult,remDecodedResult: remoteDecodedResult}
    }

    async analyze(cmd,breakdownAnalysis=false){

            
        var breakdownAnalysisResults=[];
        if(breakdownAnalysis)
        {

            if(cmd.cmd=="GET" && cmd.a.v.length > 1)
            {
                var qryBreakdown=[];
                cmd.a.v.forEach(function(e,i){
                    if(i!=0)
                    {   
                        let newCmd=Object.assign({},cmd);
                        newCmd.a=Object.assign({},cmd.a);
                        newCmd.a.v=cmd.a.v.slice(0,-i);
                       
                        qryBreakdown.push(newCmd);
                    }
                    else
                    {
                        qryBreakdown.push(cmd);
                    }
                });
                qryBreakdown.reverse();
                
                for(let i=0;i<qryBreakdown.length;i++)
                {
                    breakdownAnalysisResults.push(await this.analyze(qryBreakdown[i],false));
                }
            }
            else
            {
                //breakdown analysis is only available for GET commands
            }
        }

        var comparison=await this.compareExecModes(cmd);  

        let queryAnalysisResults={
            cmd: cmd,
            lclResult: comparison.lclResult,
            remResult: comparison.remResult,
            lclResultDecoded: comparison.lclDecodedResult,
            remResultDecoded: comparison.remDecodedResult,
            remoteExecutionDuration: comparison.remDuration,
            localExecutionDuration: comparison.lclDuration,
            breakdownAnalysisResults: breakdownAnalysisResults,
            resultsMatch: comparison.resultsMatch
        };

       return queryAnalysisResults; 
    }

    async batchAnalysis(queries,breakdownAnalysis=false){
        var resultsBatch=[];
        for(let i=0; i<queries.length; i++)
        {
            resultsBatch.push(await this.analyze(queries[i].cmd));
        }
        
        var resultsCount=resultsBatch.length;
        var totalRemDuration=0;
        var totalLclDuration=0;
        var avgDelta=0;
        var matchedResults=0;
        var remLessDur=0;
        var lclLessDur=0;
        var eqlDur=0;

        resultsBatch.forEach(function(e){
            totalRemDuration+=e.remoteExecutionDuration;
            totalLclDuration+=e.localExecutionDuration;
            avgDelta+=(e.remoteExecutionDuration-e.localExecutionDuration);
            if(e.resultsMatch) matchedResults+=1;
            if(e.remoteExecutionDuration>e.localExecutionDuration) lclLessDur+=1;
            if(e.remoteExecutionDuration<e.localExecutionDuration) remLessDur+=1;
            if(e.remoteExecutionDuration==e.localExecutionDuration) eqlDur+=1;
        })

        var results={
            results: resultsBatch,
            resultsCount: resultsCount,
            totalRemDuration: totalRemDuration,
            totalLclDuration: totalLclDuration,
            avgDelta: avgDelta/resultsCount,
            matchedResults: matchedResults,
            matchedResultsP: matchedResults/resultsCount,
            remLessDur: remLessDur,
            remLessDurP: remLessDur/resultsCount,
            lclLessDur: lclLessDur,
            lclLessDurP: lclLessDur/resultsCount,
            eqlDur: eqlDur,
            eqlDurP: eqlDur/resultsCount,
            queries:null,
        }

        return results;
    }

    publishQueryTraceData(queryTraceData){
       this.eventBroker.publish('debug/ecoreSync/queries',queryTraceData);
    }


}