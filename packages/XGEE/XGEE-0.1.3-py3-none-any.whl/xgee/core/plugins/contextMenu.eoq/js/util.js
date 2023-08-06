// EOQ Workspace Utils
// 2020 Matthias Brunner



class EoqWorkspaceUtils{

    constructor(app)
    {
        this.app=app;
    }

    async createModelResource(dir,baseName,fileExtension,nsURI,className)
    {
        var resourceNames=await ecoreSync.exec(new eoq2.Get(new eoq2.Obj(this.app.ecoreSync.rlookup(dir)).Pth('resources').Pth('name')));
                                  
        var currentResourceName=baseName+'.'+fileExtension;
        var collisions=0;
        var nameFound=false;
        while(!nameFound)
        {
            var nameTaken=false;
            
            for(let n in resourceNames)
            {
                if(resourceNames[n]==currentResourceName)
                {
                    nameTaken=true;
                    break;
                }
            }

            if(nameTaken)
            {
                currentResourceName=baseName+(collisions+1)+'.'+fileExtension;
                collisions+=1;
            }
            else
            {
                nameFound=true;
            }
        }


        var cmd=new eoq2.Cmp();
        cmd.Crn("http://www.eoq.de/workspacemdbmodel/v1.0","ModelResource",1)
        .Set(new eoq2.Qry().His(-1),"name",currentResourceName)
        .Crn(nsURI,className)
        .Add(new eoq2.His(0),'contents',new eoq2.His(-1))
        .Add(new eoq2.Qry().Obj(this.app.ecoreSync.rlookup(dir)),"resources",new eoq2.Qry().His(0));
        ecoreSync.exec(cmd);
    }



    async createDirectory(dir){
        var subDirNames=await ecoreSync.exec(new eoq2.Get(new eoq2.Obj(this.app.ecoreSync.rlookup(dir)).Pth('subdirectories').Pth('name')));
                            
        var dirBaseName="newSubdir";
        var currentDirName=dirBaseName;
        var collisions=0;
        var nameFound=false;
        while(!nameFound)
        {
            var nameTaken=false;
            
            for(let n in subDirNames)
            {
                if(subDirNames[n]==currentDirName)
                {
                    nameTaken=true;
                    break;
                }
            }

            if(nameTaken)
            {
                currentDirName=dirBaseName+(collisions+1);
                collisions+=1;
            }
            else
            {
                nameFound=true;
            }
        }

        var cmd=new eoq2.Cmp();
        cmd.Crn('http://www.eoq.de/workspacemdbmodel/v1.0','Directory');
        cmd.Set(new eoq2.His(-1),'name',currentDirName);
        cmd.Add(new eoq2.Obj(this.app.ecoreSync.rlookup(dir)),'subdirectories',new eoq2.His(0));
        ecoreSync.exec(cmd)

    }

    deleteDirectory(dir){
        var self=this;
        var dialog = new jsa.MsgBox({
            content : 'Do you really want to delete the directory ' + dir.get("name") + ' and all its contents? This action can not be undone.',
            buttons : {
                yes: {
                  name: 'Yes',
                  startEnabled: true,
                  data: this,
                  onClickCallback: function(event) {                    
                    self.app.commandManager.Execute(new ERemoveCommand(ecoreSync,dir.eContainer,dir.eContainingFeature.get("name"),dir));
                    dialog.Dissolve();
                  }
                },
                no: {
                    name: 'No',
                    startEnabled: true,
                    data: this,
                    onClickCallback: function(event) {
                        dialog.Dissolve();
                    }
                }
            }
        });
        this.app.AddChild(dialog);
    }

    deleteFile(file){
        var self=this;
        var dialog = new jsa.MsgBox({
            content : 'Do you really want to delete ' + file.get("name") + '? This action can not be undone.',
            buttons : {
                yes: {
                  name: 'Yes',
                  startEnabled: true,
                  data: this,
                  onClickCallback: function(event) {                    
                    self.app.commandManager.Execute(new ERemoveCommand(ecoreSync,file.eContainer,file.eContainingFeature.get("name"),file));
                    dialog.Dissolve();
                  }
                },
                no: {
                    name: 'No',
                    startEnabled: true,
                    data: this,
                    onClickCallback: function(event) {
                        dialog.Dissolve();
                    }
                }
            }
        });
        this.app.AddChild(dialog);
    }


    move(source,dest,name=null,recurse=false){
        
    }

    copy(source,dest,name=null,recurse=false){

    }



}

export {EoqWorkspaceUtils}



