var WorkspaceProviderJobs=function()
{

    this.updateDirectory=function(directory)
    {
        var task=this;
        this.taskName="workspaceProvider.updateDirectory";
        this.directory=directory;
        this.queue=null;
        this.ecoreSync=null;
        this.done=null;
        this.action=function()
        {         
            task.directory.update(function(){ task.done(); });
        };       
    };

    this.loadResources=function(directory,filter,each,sync)
    {
        var task=this;
        this.taskName="workspaceProvider.loadResources";
        this.directory=directory;
        this.filter=filter;
        this.eachAction=each;
        this.sync=sync;
        this.queue=null;
        this.ecoreSync=null;
        this.done=null;
        this.action=function()
        {               
            var filteredContents=task.directory.getContents().filter(task.filter);
                    
            var queueGroup=new task.ecoreSync.jobQueue.queueGroup(function()
            {
                task.done();
            });

            for(let i in filteredContents)
            {    
                console.warn("Loading..."+filteredContents[i].name);
                let queue=new task.ecoreSync.jobQueue.queue();            
                queue.addJob(new workspaceProviderJobs.loadResource(filteredContents[i],task.eachAction,task.sync));
                queueGroup.addQueue(queue);
            }
            
            queueGroup.run();
            
        }
    };


    this.loadResource=function(workspaceResource,each,sync)
    {
        var task=this;
        this.taskName="workspaceProvider.loadResource";
        this.workspaceResource=workspaceResource;
        this.eachAction=each;
        this.sync=sync;
        this.queue=null;
        this.ecoreSync=null;
        this.done=null;
        this.action=function()
        {
            task.workspaceResource.getRootObject().then(function(eObject)
            {                
                if(task.eachAction!=null)
                {
                    task.queue.addJob(new task.ecoreSync.jobQueue.CustomJob(function(thistask){   
                        console.warn("Performed action.")                
                        task.eachAction(eObject);
                        thistask.done();
                    })); 
                }
                else
                {
                    console.warn('No action on result performed: no action defined. name='+workspaceResource.name);
                }

                if(task.sync)
                {
                    let syncTask=new task.ecoreSync.mirror.ObjectSync(eObject.noproxy);
                    task.queue.addJob(syncTask);  
                    task.done();                          
                }  

            });
        };
    };


    this.loadAll=function(directory,filter,each,sync)
    {
        var task=this;
        this.taskName="workspaceProvider.loadAll";
        this.directory=directory;
        this.filter=filter;
        this.eachAction=each;
        this.sync=sync;
        this.queue=null;
        this.ecoreSync=null;
        this.done=null;
        this.action=function()
        {         
            //let updateTask=new workspaceProviderJobs.updateDirectory(task.directory);
            let loadResources=new workspaceProviderJobs.loadResources(task.directory,task.filter,task.eachAction,task.sync);
            task.queue.addJobAsNext(loadResources);   
            //task.queue.addJobAsNext(updateTask);                     
            task.done();           
        };     
    };

};

var workspaceProviderJobs=new WorkspaceProviderJobs();