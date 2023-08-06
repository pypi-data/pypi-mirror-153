


import * as manager from "./js/ClipboardManager.js"
import * as AppClipboard from "./js/AppClipboard.js"
import * as API from "./js/ClipboardAPI.js"
import * as ClipboardEvaluator from "./js/ClipboardEvaluator.js"
import * as EcoreClipboardEvaluator from "./js/EcoreClipboardEvaluator.js"

var selection=null;
var clipboardContents=null;
var appClipboard=new AppClipboard.ApplicationClipboard();
var clipboardManager=new manager.ClipboardManager(appClipboard);
var ecoreClipboardEvaluator= new EcoreClipboardEvaluator.EcoreClipboardEvaluator();

API.priv.setClipboardManager(clipboardManager);
API.priv.setClipboardEvaluator(ecoreClipboardEvaluator);


export async function init(pluginAPI) {      
    var eventBroker=pluginAPI.require('eventBroker');

    pluginAPI.provide('clipboard.pasteHandlerProviders',null,function(evt){

    });
    
	if(eventBroker){
	eventBroker.subscribe("SELECTION/CHANGE",function(evt){ selection=evt.data.selection; });
	eventBroker.subscribe("CLIPBOARD/CMD/*",async function(evt){   
   

        var target=null;
        if(evt.data)
        {
            if(Array.isArray(evt.data))
            {
                target=evt.data;
            }
            else
            {
                target=[evt.data];
            }            
        }
        else if(selection){
            //fallback, use selection as target for the command
            target=selection;
        }
   
 
        var validTarget=target!=null && !(target.length > 1 && evt.topic=='CLIPBOARD/CMD/PASTE');
        var validContents=!(clipboardContents==null && evt.topic=='CLIPBOARD/CMD/PASTE');

        if(validTarget && validContents)
        {
            switch(evt.topic){
                case 'CLIPBOARD/CMD/COPY':                    
                    clipboardContents={cmd:'COPY',contents:target.map(function(e){ return ecoreSync.utils.getObjectURL(e); })}    
                    var contents=btoa((JSON.stringify(clipboardContents)));

                    clipboardManager.writeText(contents);

                break;
                case 'CLIPBOARD/CMD/CUT':
                    clipboardContents={cmd:'CUT',contents:target.map(function(e){ return ecoreSync.utils.getObjectURL(e); })}  
                    var contents=btoa((JSON.stringify(clipboardContents)));

                    clipboardManager.writeText(contents);

                break;
                case 'CLIPBOARD/CMD/PASTE':                       
                          
                    //Fallback to universal ecore paste handler     
                    try{   
                        clipboardContents=JSON.parse(atob(evt.data.clipboardData.getData('Text')));
                        if(clipboardContents.contents)
                        {
                            clipboardContents.contents=clipboardContents.contents.map(function(e){
                                return ecoreSync.utils.getObjectByURL(e);
                            });

                            alert('deprecated')
                        }
                    }
                    catch(e)
                    {
                        //incompatible format or unpacking error
                    }
              
                break;
                case 'CLIPBOARD/CMD/LOCALPASTE':                           
                    //Fallback to universal ecore paste handler     


                    if(!evt.data || (evt.data && !evt.data.preventUpdate))
                    {
                        clipboardManager.sync();                   
                    }

                    try{   
                            clipboardContents=JSON.parse(atob(await clipboardManager.readText()));
                            if(clipboardContents.contents)
                            {
                                clipboardContents.contents=clipboardContents.contents.map(function(e){
                                    return ecoreSync.utils.getObjectByURL(e);
                                });
                                console.error(target);
                                // await UniversalEcorePasteHandler(clipboardContents,target);                               
                            }                        
                    }
                    catch(e)
                    {
                        //incompatible format or unpacking error
                    }          
                break;
                default:
                break;

            }
        }
        else
        {
            console.error('CMD STATE')
            console.error(validTarget);
            console.error(validContents);
            console.error(target);
        }
    }
    ); 
	}
	else
	{
        throw 'missing eventBroker API'
	}
        
    pluginAPI.expose(API.pub);
    return true
};

export var meta={
	"id":"clipboard",
	"description":"Clipboard Plugin for jsApplication",
	"author":"Matthias Brunner",
	"version":"1.0.0",
	"requires":['ecoreSync','eventBroker']
};



