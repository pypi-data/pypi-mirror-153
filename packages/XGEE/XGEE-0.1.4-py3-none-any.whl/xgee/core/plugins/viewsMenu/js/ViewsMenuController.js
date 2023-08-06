// 2020 Bjoern Annighoefer

var VIEWSMENU = VIEWSMENU || {};

Object.assign(VIEWSMENU,(function(){
    function ViewsMenuController(pluginApi,params) {
        //params
        this.menuId = 'VIEW_MENUS',
        this.menuName = 'Views',
        this.appendBefore = false, 
        this.appendMenuId = null
        Object.assign(this,params); //copy params

        //internals
        this.app = pluginApi.getGlobal('app'); 
        this.pluginApi = pluginApi;
        this.viewsMenu = null;
        this.viewsMenuEntry = null;
        this.viewsMenuUpdater = null;
    } 

    ViewsMenuController.prototype.Init = function() {
        this.InitMenu();
        this.InitEvenListener();
    };

    ViewsMenuController.prototype.InitMenu = function() {
        //create the views menu

        this.viewsMenuEntry = new jsa.MenuEntry( {
            id : this.menuId,
            content : this.menuName,
            startEnabled : false,
            hasPopup : true
        });

        //attach the new menu
        if (this.appendMenuId) {
            let appendMenu = this.app.menu.GetChildById(this.appendMenuId);
            if(appendMenu) {
                let i = this.app.menu.GetChildren().findIndex(elem => elem==appendMenu);
                if (this.appendBefore) {
                    this.app.menu.AddChildAtIndex(this.viewsMenuEntry, i);
                } else {
                    this.app.menu.AddChildAtIndex(this.viewsMenuEntry, i+1);
                }
            }
        } else {
            if (this.appendBefore) {
                this.app.menu.AddChildAtIndex(this.viewsMenuEntry, 0); //attach at the beginning
            } else {
                this.app.menu.AddChild(this.viewsMenuEntry);
            }
        }

        this.viewsMenu = new jsa.Menu( {
            isPopup : true,
            popupDirection : 'bottom'
        });
        this.viewsMenuEntry.SetSubmenu(this.viewsMenu);

        /* Fill the views menu */
        let views = this.app.viewManager.GetChildren();
        for(let i=0;i<views.length;i++) {
            let view = views[i];
            //let activeView = this.app.viewManager.GetActiveView();
            this.viewsMenu.AddChild(this.CreateViewMenuEntry(view));
        }
        if(views.length>0) {
            this.viewsMenuEntry.Enable();
        }

        this.pluginApi.setGlobal("viewsMenu",this.viewsMenu);
    }

    ViewsMenuController.prototype.InitEvenListener = function() {
        this.viewsMenuUpdater = new jsa.Observer( {
            data : this,
            onNotifyCallback : function(event) {
                this.data.OnViewChanged(event);
            }
        });

        this.app.viewManager.StartObserving(this.viewsMenuUpdater);       
    };

    ViewsMenuController.prototype.CreateViewMenuEntry = function(view) {
        let newMenuEntry = new jsa.MenuEntry( {
            id : this.menuId+'_'+view.id,
            content : view.name,
            icon : view.icon,
            data : view,
            startEnabled : (this.app.viewManager.GetActiveView() != view),
            data : { 
                view : view,
                app : this.app
            },
            onClickCallback : function() {
                this.data.app.viewManager.ActivateView(this.data.view);
            }
        });
        return newMenuEntry;
    };

    ViewsMenuController.prototype.OnViewChanged = function(event) {
        //rebuild the view menu
        if(jsa.EVENT.IS_INSTANCE(event,jsa.EVENT.TYPES.ADD_CHILD) || 
        jsa.EVENT.IS_INSTANCE(event,jsa.EVENT.TYPES.REMOVE_CHILD)) {
            //clear the menu
            let currentMenuEntries = this.viewsMenu.GetChildren();
            for(let i=0;i<currentMenuEntries.length;i++) {
                this.viewsMenu.RemoveChild(currentMenuEntries[i]);
            }
            //rebuild the menu
            let views = this.app.viewManager.GetChildren();
            if(views.length>0) {
                for(let i=0;i<views.length;i++) {
                    let view = views[i];
                    this.viewsMenu.AddChild(new jsa.MenuEntry( {
                        id : this.menuId+'_'+view.id,
                        content : view.name,
                        icon : view.icon,
                        data : view,
                        isEnabledCallback : function() {
                            return (this.app.viewManager.GetActiveView() != this);
                        },
                        onClickCallback : function() {
                            this.app.commandManager.Execute(new jsa.ChangeViewCommand(this.app.viewManager,this.data));
                        }
                    }));
                }
                this.viewsMenuEntry.Enable();
            } else {
                this.viewsMenuEntry.Disable();
            }
        } else if(jsa.EVENT.IS_INSTANCE(event,jsa.EVENT.TYPES.SET_ACTIVE_VIEW)) {
            let oldViewMenuEntry = this.viewsMenu.GetChildById(this.menuId+'_'+event.oldValue.id);
            if(oldViewMenuEntry) oldViewMenuEntry.Enable();
            let newViewMenuEntry = this.viewsMenu.GetChildById(this.menuId+'_'+event.value.id);
            if(newViewMenuEntry) newViewMenuEntry.Disable();
        }
    };    

    return {
        ViewsMenuController : ViewsMenuController
    };
})());