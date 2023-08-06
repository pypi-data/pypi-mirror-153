// 2020 Bjoern Annighoefer

var ACTIONS = ACTIONS || {};

Object.assign(ACTIONS, (function () {
    function ActionsController(pluginApi, params) {
        //params
        this.menuId = '#ACTION';
        this.menuName = 'Actions';
        this.appendBefore = false;
        this.appendMenuId = null;
        Object.assign(this, params); //copy params

        //internals
        this.app = pluginApi.getGlobal('app');
        this.pluginApi = pluginApi;
        this.eventBroker = null;
        this.actionsMenuEntry = null;
        this.currentSelection = null;
    }

    ActionsController.prototype.Init = function () {
        this.InitMenu();

        //Now start listen to selection change events
        this.InitSelectionEventListener();
    };

    ActionsController.prototype.InitMenu = function () {
        this.actionsMenuEntry = new jsa.MenuEntry({
            id: this.menuId,
            content: this.menuName,
            startEnabled: false,
            hasPopup : true
        });
        //attach the new menu
        if (this.appendMenuId) {
            let appendMenu = this.app.menu.GetChildById(this.appendMenuId);
            if(appendMenu) {
                let i = this.app.menu.GetChildren().findIndex(elem => elem==appendMenu);
                if (this.appendBefore) {
                    this.app.menu.AddChildAtIndex(this.actionsMenuEntry, i);
                } else {
                    this.app.menu.AddChildAtIndex(this.actionsMenuEntry, i+1);
                }
            }
        } else {
            if (this.appendBefore) {
                this.app.menu.AddChildAtIndex(this.actionsMenuEntry, 0); //attach at the beginning
            } else {
                this.app.menu.AddChild(this.actionsMenuEntry);
            }
        }
    
        let actionsMenu = new jsa.Menu({
            isPopup: true,
            popupDirection : 'bottom'
        });
        this.actionsMenuEntry.SetSubmenu(actionsMenu);

        
        /* Asynchronously fill the automations menu */
        let self = this;
        ACTIONS.FetchActions(this.app.domain).then(function (actions) {
            return new Promise(function (resolve, reject) {
                resolve(actions.filter(self.actionFilterFunction));
            });
        }).then(function (actions) {
            let menuPrefix = self.menuId + '_'; // TODO: check if this or self
            let actionSubmenus = new Map(); //a look-up table for all categories
            actions.forEach((action) => {
                let categoryMenu = actionsMenu;
                //find the right category or create it if not existing
                for (let j = 0; j < action.categories.length; j++) {
                    let category = action.categories[j];
                    let subMenuId = menuPrefix + action.categories.slice(0, j + 1).join('_');
                    let newSubmenu = actionSubmenus.get(subMenuId);
                    if (!newSubmenu) { //if it not exists create a new one
                        let newSubmenuEntry = new jsa.MenuEntry( {
                            id: subMenuId,
                            content: category,
                            hasPopup : true
                        });
                        categoryMenu.AddChild(newSubmenuEntry);

                        newSubmenu = new jsa.Menu({
                            isPopup: true,
                            popupDirection : 'right'
                        });
                        newSubmenuEntry.SetSubmenu(newSubmenu);
                        actionSubmenus.set(subMenuId, newSubmenu);
                    }
                    categoryMenu = newSubmenu;
                }
                //finally add the action entry
                categoryMenu.AddChild(new jsa.MenuEntry({
                    id: menuPrefix + action.categories.join('_') + '_' + action.name,
                    content: action.name,
                    data: action,
                    onClickCallback: function () {
                        ACTIONS.OpenDefaultActionsDialog(self.app, this.data); // TODO: check if this or self is appropriate
                    },
                    hasTooltip: true,
                    tooltip: action.description
                }));
            });
            if (actions.length > 0) {
                self.actionsMenuEntry.Enable();
                // self.app.menuManager.Update();
            }
        }).catch(function (e) {
            console.warn("Failed to load actions: " + e.toString());
        });


        //make the menu available to other plugins
        this.pluginApi.setGlobal("actionsMenu", this.actionsMenuEntry);
    };

    ActionsController.prototype.InitSelectionEventListener = function () {
        this.eventBroker = this.pluginApi.require('eventBroker');
        let self = this;
        this.eventBroker.subscribe("SELECTION/CHANGE", function (evt) {
            self.OnSelectionChanged(evt)
        });
    };

    ActionsController.prototype.OnSelectionChanged = function (evt) {
        this.currentSelection = evt.data.selection; //store the current selection for the case that an automation dialog is opened
    };

    return {
        ActionsController: ActionsController
    };
})());