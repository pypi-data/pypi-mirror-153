//2020 Matthias Brunner
var pluginMeta={
    "id":"eventBroker",
    "description":"Event Broker implementation",
    "author":"Matthias Brunner",
    "version":"0.0.1",
    "requires":[]
};

export async function init(pluginAPI) { 

    //plug-in statics and configuration
    var scriptIncludes=[
        "BasicEvent.js",
        "SelectionChangedEvent.js"
    ];

    var subscribedTopics={};


    var buildTopicList=function(topic)
    {
        var topics=[];
        topics.push('*');

        if(!topic.includes('/'))
        {   
            topics.push(topic);            
        }
        else
        {
        
            var subtopics=topic.split('/');
            
            subtopics.forEach(function(e,i){
           
                if(i+1<subtopics.length)
                {
                    var subStar=subtopics.slice();
                    subStar[i]='*';   
                    topics.push(subStar.join('/'));                
                    topics.push(subtopics.slice(0,i+1).join('/')+'/*');
                }
                else
                {
                    let sTopic=subtopics.slice(0,i+1).join('/');
                    if(topics.indexOf(sTopic)==-1)
                    {
                        topics.push(sTopic);
                    }
                }
            });
        }

        return topics;
    }

    var publish=function(topic,data=null)
    {
        return new Promise(function(resolve,reject){

            if(topic.includes("*"))
            {
                reject("wild-card character * is not permitted in published topics");
            }

            var logicalTopics=buildTopicList(topic);
            var event={"topic":topic,"data":data};
            logicalTopics.map(function(lt){
                if(subscribedTopics[lt])
                {
                    subscribedTopics[lt].subscribers.map(function(sb){
                        sb(event);
                    });
                }                
            });
            resolve();       
        });
    }

    var initTopic=function(topic)
    {
        if(!subscribedTopics[topic])
        {
            subscribedTopics[topic]={"topic":topic,"subscribers":[]};
        }
    }

    var subscribe=function(topic,eventHandler)
    {
        if(!subscribedTopics[topic])
        {
            initTopic(topic);
        }        
        subscribedTopics[topic].subscribers.push(eventHandler);        
    }

    var unsubscribe=function(eventHandler,topic=null)
    {    
        var res=false;
        if(topic)
        {
            if(subscribedTopics[topic])
            {
                var idx=subscribedTopics[topic].subscribers.indexOf(eventHandler);
                if(idx>=0)
                {
                    subscribedTopics[topic].subscribers.splice(idx,1);    
                    res=true;   
                }
            }
        }
        else
        {
            let keys=Object.keys(subscribedTopics);
            keys.forEach(function(e){
                var idx=subscribedTopics[e].subscribers.indexOf(eventHandler);
                if(idx>=0)
                {
                    subscribedTopics[e].subscribers.splice(idx,1);
                    res=true;
                }    
            })            
        }

        return res;
    }

    var debug=function(){
        return subscribedTopics
    }

    //init plugin

    //init the plug-in
    await pluginAPI.loadScripts(scriptIncludes)
    pluginAPI.expose({
        //functions 
        publish :publish,
        subscribe :subscribe,
        unsubscribe :unsubscribe,
        debug: debug,
        //classes
        BasicEvent : eventBroker.BasicEvent,
        SelectionChangedEvent : eventBroker.SelectionChangedEvent
    });
    return true 
};

export var meta=pluginMeta;



