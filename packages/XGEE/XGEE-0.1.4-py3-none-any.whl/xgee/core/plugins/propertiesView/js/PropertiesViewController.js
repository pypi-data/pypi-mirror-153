// This is the baseclass for all plugins that would like to provide a propertiesView pane
// 2020 Bjoern Annighoefer

var PROPERTIES_VIEW = PROPERTIES_VIEW || {};

Object.assign(PROPERTIES_VIEW,(function(){
    function PropertiesViewController(pluginApi,paneProviderExtId,params) {

        //params       
        this.enableModeChanges = true;
        Object.assign(this,params);

        //internals
        this.app = pluginApi.getGlobal('app'); 
        this.pluginApi = pluginApi;
        this.paneProviderExtId = paneProviderExtId;
        this.currentSelectionData=null
        
        this.bubble = null;
        this.eventBroker = null;
        this.propertyPaneViews = []; //all possible panes fo the current element

        //basic UI elements
        this.mainPane = null;
        this.viewManager = null;
        this.tabbar = null;
    } 

    PropertiesViewController.prototype.Init = function() {
        //The properties bubble can show several views. Init the basic viewmanager and pane for that 
        this.mainPane = new jsa.CustomFlatContainer({
            style : ['propertiesView-main-pane']
        });

        this.viewManager = new jsa.ViewManager({
            style : ['jsa-view-manager','jsa-tab-controlled-container-tap-bottom']
        });
        this.mainPane.AddChild(this.viewManager);

        this.tabbar = new jsa.Tabbar({
            style : ['jsa-tabbar','jsa-tabbar-bottom','propertiesView-tabbar']
        });
        this.mainPane.AddChild(this.tabbar);
        this.tabbar.SyncWithViewManager(this.viewManager,false);

        //init the containing element for the properties view
      
        this.InitBubble();
        this.InitModal();
        

        //Now start listen to selection change events
        this.InitEventListeners();
    };

    PropertiesViewController.prototype.InitBubble = function() {
        this.bubble = new jsa.Bubble({
            name: 'Properties',
            enabled: true,
            isResizable: true,
            isMinimizable: true,
            isClosable: true,
            isMinimized: false,
            autoHide: true,
            style: ['jsa-bubble','properties-bubble']
        });
        this.app.AddChild(this.bubble);
    };

    PropertiesViewController.prototype.InitModal = function() {
        var self=this
        this.modal = new jsa.Modal({
            startVisible:false,
            name: 'Properties',
            buttons:{
                done: {
                name: 'Done',
                startEnabled: true,
                onClickCallback: function(event) {
                    self.modal.Hide()
                }
                }
            }
        });
        this.app.AddChild(this.modal);
    };

    PropertiesViewController.prototype.InitEventListeners = function() {

        this.eventBroker=this.pluginApi.require('eventBroker');
        let self = this;

        this.eventBroker.subscribe("SELECTION/CHANGE",function(evt){
            self.OnSelectionChanged(evt)
        });

        this.eventBroker.subscribe("PROPERTIESVIEW/OPEN",function(evt){
            self.OnOpen(evt)
        });

        this.eventBroker.subscribe("PROPERTIESVIEW/OPENMODAL",function(evt){
            self.OnOpen(evt,"MODAL")
        });

        this.eventBroker.subscribe("PROPERTIESVIEW/CLOSE",function(evt){
            self.OnClose(evt)
        });
    };

    PropertiesViewController.prototype.OnSelectionChanged = async function(evt) {
        var ecoreSync=this.pluginApi.require('ecoreSync').getInstanceById('ecoreSync');
        var selection = evt.data.selection;
        this.currentSelectionData=evt.data      
    };

    PropertiesViewController.prototype.OnOpen = async function(evt,mode="BUBBLE"){
        let selection=[]
        let domElements=[]
        if(evt.data){
            if(evt.data.eObject)
            {         
                selection=[evt.data.eObject]
                if(evt.data.DOM)
                {
                    domElements=evt.data.DOM
                }
            }            
        }
        else if(this.currentSelectionData != null )
        {
            selection = this.currentSelectionData.selection;            
            domElements = this.currentSelectionData.domElements;         
        }

        var selectedObjects=selection.map(function(eObject){
            return ecoreSync.utils.isEClassInitialized(eObject.eClass)
        })

        await Promise.all(selectedObjects)


        if(selection.length)
        {
            //find the applicable editors
            let paneProviders=this.pluginApi.evaluate(this.paneProviderExtId).filter(function(paneProvider){
                let isApplicable = false;
                try { //be fault tolerant against errors in properties panes
                    isApplicable = paneProvider.IsApplicable(selection);
                } catch(e) {
                    console.error('PROPERTIESVIEW: Failed to test applicability for selection for '+paneProvider.name+':'+e.toString() );
                }
                return isApplicable;
            }).sort(function(a,b){
                return b.importance - a.importance; //highest importance first
            });
    
            let nPaneProviders = paneProviders.length;
            if(0<nPaneProviders) {
                this.CreatePropetiesPanes(paneProviders,selection);
                if(mode=="BUBBLE") {              
                    this.ShowBubble(selection,domElements);
                } else if (mode=="MODAL"){
                    this.ShowModal(selection,domElements)
                }
            }
        }


    }


    PropertiesViewController.prototype.OnClose = async function(evt){
        this.modal.subelements.userContainer.RemoveChild(this.mainPane);
        this.bubble.RemoveChild(this.mainPane);
        this.bubble.Hide()
        this.modal.Hide()
    }

    PropertiesViewController.prototype.CreatePropetiesPanes = function(paneProviders,selection) {
        //first, delete all existing ones
        for(let i=0;i<this.propertyPaneViews.length;i++) {
            this.propertyPaneViews[i].Dissolve();
        }
        this.propertyPaneViews = [];
        //create the new ones
        for(let i=0;i<paneProviders.length;i++) {
            let paneProvider = paneProviders[i];
            let name = paneProvider.name;
            let view = new PROPERTIES_VIEW.LoadOnDemandView({
                name : name,
                paneProvider : paneProvider,
                selection : selection
            })
            this.propertyPaneViews.push(view);
            this.viewManager.AddChild(view);
        }
        this.viewManager.ActivateView(this.propertyPaneViews[0]); //activate the first view default.
    };

    PropertiesViewController.prototype.ShowBubble = function(selection,domElements) {
        this.bubble.Restore()
        if(domElements) {
            this.bubble.PopupOnDomElement(domElements);
        } else {
            this.bubble.Popup(0,0);
        }
        this.bubble.AddChild(this.mainPane);
        //this.bubble.AddChild(this.propertyPaneViews[0]);
    };

    PropertiesViewController.prototype.ShowModal = function(selection,domElements) {
       this.modal.SetName('Properties')
       this.modal.subelements.userContainer.AddChild(this.mainPane);
       $(this.modal.subelements.userContainer.domElement).height(window.innerHeight*0.5)
       this.modal.Show()      
    };
    

    return {
        PropertiesViewController : PropertiesViewController
    };
})());