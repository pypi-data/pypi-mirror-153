export async function init(pluginAPI) {      
    var iconProviderModules=await pluginAPI.loadModules(["js/IconProvider.js"])         

    var providers=[];
    pluginAPI.provide('iconProvider.providers',iconProviderModules[0].IconProvider,function(event){
        providers.push(event.extension);
    });
      

    var getPathToIcon=function(eObject){
        var iconPath=null;
        var provider=providers.find(function(provider){
            return provider.isApplicable(eObject);
        });

        if(provider){
            iconPath=provider.getPathToIcon(eObject); 
        }        

        return iconPath;
    }  
    
    var test=async function(qry){
        console.info('Running icon tests for supplied classes...')
        var missingIcons=0
        function checkIcon(imageSrc) {
            return new Promise((resolve,reject)=>{
                var img = new Image();
                img.onload = ()=>{resolve(true)}; 
                img.onerror = ()=>{resolve(false)};
                img.src = imageSrc;
            })
        }

        let allClassIds=await ecoreSync.remoteExec(new eoq2.Get(qry))
        for(let aClass of allClassIds)
        {
            let clazz=await ecoreSync._esDomain.initEClass(aClass.v)
            if(!clazz.values.abstract)
            {
                let path=getPathToIcon(clazz)
                try{
                    let testResult=await checkIcon(path)
                    if(!testResult)
                    {
                        missingIcons+=1
                        console.error('Missing icon: '+path+' EClass '+clazz.values.name+' @ '+clazz.eContainer.get('nsURI'))
                    }
                }
                catch(e)
                {
                    console.error('Fatal error during icon test: '+path+' EClass '+clazz.values.name+' @ '+clazz.eContainer.get('nsURI'))             
                }          
            }
            
        }

        console.info('Test complete. Missing icons='+missingIcons)    
        if(missingIcons)
        {
            return false
        }
        else
        {
            return true
        }
    }


    pluginAPI.expose({getPathToIcon: getPathToIcon, test: test});
    return true;     
};

export var meta={"id":"iconProvider",description:"Generic IconProvider Definition","author":"Matthias Brunner","version":"0.1.0","requires":[]};



