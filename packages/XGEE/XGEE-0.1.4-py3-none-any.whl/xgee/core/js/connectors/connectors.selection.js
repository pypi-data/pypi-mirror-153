var SelectionConnector=function(selectionProvider,namespace="global")
{
    var self=this;
    this.__currentSelection=null;
    this.__isRegistered=false;
    this.__registeredObjects=[];
    this.__selectionProvider=selectionProvider;
    this.__selectionProvider.subscribe(function(selection){       
        self.deregister(); //?
        self.__currentSelection=selection;
        self.register();
        self.__renderSelection(selection);
    });
    this.__container=null;  
    this.setContainer=function(container)
    {
        self.__container=container;
    }    
    this.__renderSelection=function(selection)
    {
       if(self.__container!=null)
       {
           if(selection.object)
           {
            if(selection.object.isModelObject)
            {
                if(selection.object.feature==null)
                {
                    UIPropertiesPane(self.__container,selection.object.eObject,namespace);
                }
                else
                {                
                    UIReferencesPreview(self.__container,selection.object.eObject,selection.object.feature);             
                }
            }

            if(selection.object.isResource)
            {        
                    if(selection.object.isLoaded)    
                    {
                        UIPropertiesPane(self.__container,selection.object.getEObject(),namespace);      
                    }
                    else
                    {
                        self.__container.empty();
                        self.__container.append('You can load the resource by opening it in the tree.')
                    }    
            }
        
           }
           else
           {
            if(selection.feature==null)
            {
                UIPropertiesPane(self.__container,selection.eObject,namespace);
            }
            else
            {                
                UIReferencesPreview(self.__container,selection.eObject,selection.feature);             
            }
           }
        }    
    }
    this.__eventReceiver=function(changed)
    {
        self.__renderSelection(self.__currentSelection);
    };
    this.register=function()
    {
        if(self.__currentSelection!=null)
        {
            if(self.__currentSelection.eObject)
            {
                self.__currentSelection.eObject.on("change",self.__eventReceiver);
                if(self.__currentSelection.feature!=null)
                {
                    self.registerFeature();
                }
                self.__isRegistered=true;
            }
        }
    };
    this.deregister=function()
    {        
       if(self.__currentSelection!=null && self.__isRegistered)
       {
            self.__currentSelection.eObject.off("change",self.__eventReceiver);
            if(self.__currentSelection.feature!=null)
            {
                self.deregisterFeature();
            }
       }
       self.__isRegistered=false;
    };
    this.registerFeature=function()
    {
        if(!self.__isRegistered)
        {
            self.__currentSelection.eObject.on("add:"+self.__currentSelection.feature,self.__eventReceiver);
            self.__currentSelection.eObject.on("remove:"+self.__currentSelection.feature,self.__eventReceiver);
        }

        var feat=self.__currentSelection.eObject.get(self.__currentSelection.feature);
        if(feat!=undefined)
        {
            var features=feat.array();
            for(let i in features)
            {
                if(self.__registeredObjects.indexOf(features[i])==-1)
                {
                    features[i].on("change",self.__eventReceiver);
                    self.__registeredObjects.push(features[i]);
                }
            }
        }
    };

    this.deregisterFeature=function()
    {
        self.__currentSelection.eObject.off("add",self.__eventReceiver);
        self.__currentSelection.eObject.off("remove",self.__eventReceiver);

        for(let i in self.__registeredObjects)
        {
            self.__registeredObjects[i].off("change",self.__eventReceiver);
        }

        self.__registeredObjects=[];
    };
    
}