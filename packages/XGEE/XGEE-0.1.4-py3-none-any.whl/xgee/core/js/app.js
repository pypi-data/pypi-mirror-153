var graph;
var workspaceLayouts;
var graphs = [];
var outline;
var mouseX=-1;
var mouseY=-1;
var canvasSearchEnabled=false;
var canvasSearchAutoComplete;
var loaderDialog=null;
var debugEvt=null;


function InitApplication(params) {
    let app = new jsa.Application(params);
    
    //link document title to the app and views name
    document.title = app.name;
    var titleUpdater = new jsa.Observer({
        data : this,
        onNotifyCallback : function(event) {
            if(jsa.EVENT.IS_INSTANCE(event,jsa.EVENT.TYPES.SET_ACTIVE_VIEW)) {
                let view = event.value;
                if(view) {
                    document.title = app.name + ' - ' + view.name;
                }
            }
        }
    });
    app.viewManager.StartObserving(titleUpdater);

    //show the name and version on the status bar on startup
    if(app.statusbar) {
        app.statusbar.SetContent(app.name + ' ' + app.version);
    }

    return app;
};

function InitPlugins(params,app) {
    let plugins= new PluginManager(params.plugins,params.pluginPath,params.pluginManagerBasePath,{app:app});
    // return once all dependencies have been resolved
    app.plugins = plugins; /* TODO, get rid of global plugins access */
    return plugins.dependenciesResolved.then(function(){
        return Promise.resolve(plugins); 
    });
}

// function InitFileMenu(app) {
//     let fileMenu = new jsa.Menu( {
//         id :'#DATA',
//         name : 'Data'
//     });

//     fileMenu.AddEntry( new jsa.MenuEntry( {
//         id : '#DATA_SAVE',
//         name : 'Save',
//         enabled : false,
//         onClickCallback : function() {
//             app.viewManager.GetActiveView().Save();
//         }
//     }));

//     app.menuManager.AddEntry(fileMenu);
//     return fileMenu;
// };

function InitEditMenu(app) {
    let editMenuEntry = new jsa.MenuEntry( {
        id :'EDIT_MENU',
        content : 'Edit',
        hasPopup : true
    });
    app.menu.AddChild(editMenuEntry);

    let editMenu = new jsa.Menu({
        isPopup: true,
        popupDirection : 'bottom'
    });
    editMenuEntry.SetSubmenu(editMenu);

    var undoMenuEntry = new jsa.MenuEntry( {
        id : 'EDIT_MENU_UNDO',
        content : 'Undo',
        icon : 'jsa-icon-undo-light',
        startEnabled : false,
        onClickCallback : function() {
            app.commandManager.Undo();
        },
        hasTooltip : true,
        tooltip: 'Shows the last action that can be undone.'
    });
    editMenu.AddChild(undoMenuEntry);

    let redoMenuEntry = new jsa.MenuEntry( {
        id : 'EDIT_MENU_REDO',
        content : 'Redo',
        icon : 'jsa-icon-redo-light',
        startEnabled : false,
        onClickCallback : function() {
            app.commandManager.Redo();
        },
        hasTooltip : true,
        tooltip: 'Shows the last action that can be redone.'
    });
    editMenu.AddChild(redoMenuEntry);

    let undoRedoUpdater = new jsa.Observer( {
        onNotifyCallback : function(event) {
            //rebuild the view menu
            if(EVENT.IS_INSTANCE(event,EVENT.TYPES.METHOD_CALL)) {
                let lastCommand = app.commandManager.GetLastCommand();
                if(lastCommand) {
                    undoMenuEntry.SetContent('Undo: '+lastCommand.GetName());
                    undoMenuEntry.Enable();
                } else {
                    undoMenuEntry.Disable();
                    undoMenuEntry.SetContent('Undo');
                }
                let nextCommand = app.commandManager.GetNextCommand();
                if(nextCommand) {
                    redoMenuEntry.SetContent('Redo: '+nextCommand.GetName());
                    redoMenuEntry.Enable();
                } else {
                    redoMenuEntry.Disable();
                    redoMenuEntry.SetContent('Redo');
                }
            }
        }});


    app.commandManager.StartObserving(undoRedoUpdater);

    return editMenu;
};

function InitHelpMenu(app) {
    let helpMenuEntry = new jsa.MenuEntry( {
        id :'HELP_MENU',
        content : 'Help',
        hasPopup : true
    });
    app.menu.AddChild(helpMenuEntry);

    let helpMenu = new jsa.Menu( {
        isPopup : true,
        popupDirection : 'bottom'
    });
    helpMenuEntry.SetSubmenu(helpMenu);

    helpMenu.AddChild( new jsa.MenuEntry( {
        id : 'HELP_MENU_ABOUT',
        content : 'About',
        onClickCallback : function() {
            app.AddChild(new jsa.MsgBox({
                name: 'About',
                content: '<p>This is '+app.name+' v'+app.version+'.</p>'+
                        '<p>Third-party tribute:</p>'+
                        '<ul>'+
                        '<li>Ecore Editor (<a target="_blank" href="https://www.ils.uni-stuttgart.de/">Institute of Aircraft Systems</a>)</li>'+
                        '<li>jsApplication (<a target="_blank" href="https://jsapplication.gitlab.io/jsapplication/">jsapplication.gitlab.io/jsapplication/</a>)</li>'+
                        '<li>Essential Object Query (<a target="_blank" href="https://gitlab.com/eoq/essentialobjectquery/">gitlab.com/eoq/essentialobjectquery/</a>)</li>'+
                        '<li>jQuery (<a target="_blank" href="https://jquery.com/">jquery.com</a>)</li>'+
                        '<li>Fancytree (<a target="_blank" href="https://wwwendt.de/">wwwendt.de</a>)</li>'+
                        '<li>jsTree (<a target="_blank" href="https://www.jstree.com/">www.jstree.com</a>)</li>'+
                        '<li>jQuery UI (<a target="_blank" href="https://jqueryui.com/">jqueryui.com</a>)</li>'+
                        '<li>jQuery contextMenu (<a target="_blank" href="https://swisnl.github.io/jQuery-contextMenu/">swisnl.github.io/jQuery-contextMenu</a>)</li>'+
                        '</ul>',
            }));
        }
    }));

    helpMenu.AddChild( new jsa.MenuEntry( {
        id : 'HELP_MENU_RESET_PROP',
        content : 'Reset Properties View',
        onClickCallback : function() {
            //TODO: this is only a temporary solution
            let propertiesBubble = app.plugins.require('propertiesView').propertiesViewController.bubble;
            if(propertiesBubble) {
                propertiesBubble.Reset();
            }
        }
    }));

    helpMenu.AddChild( new jsa.MenuEntry( {
        id : 'HELP_MENU_SETTINGS_CLEAR',
        content : 'Clear Settings',
        onClickCallback : function() {app.settingsManager.Clear();}
    }));

    return helpMenu;
};

function ShowSplash(app) {
var splash = new jsa.Splash({
    content : '<div class="jsa-loading"></div>'+
              '<div>Loading...</div>'
});

app.AddChild(splash);

splash.Show();

return splash;
};


function InitWorkspace(app) {
    return Promise.resolve(null)
};

function InitTools(app){
    // let homeTool  = new jsa.Tool({
    //     containerStyle : ['jsa-tool-container','tool-home'],
    //     onClickCallback : function(event) {
    //         let dashboardView = app.viewManager.GetChildById('DASHBOARD');
    //         if(dashboardView && dashboardView != app.viewManager.GetActiveView()) {
    //             app.commandManager.Execute(new jsa.ChangeViewCommand(app.viewManager,dashboardView));
    //         }
    //     }
    // }); 
    // app.toolBar.AddChild(homeTool);

    // let domainStatusTool = new DomainStatusTool({
    //     domainInfo: app.settings.eoqServer,
    //     domainStatistics: app.domainStatistics
    // });
    // app.toolBar.AddChild(domainStatusTool);

    // let notesTool = new NotesTool({
    //     notesManager: app.notesManager
    // });
    // app.toolBar.AddChild(notesTool);

    // let tools = {
    //     homeTool : homeTool,
    //     domainStatusTool : domainStatusTool,
    //     notesTool : notesTool,
    // };

    //listen to domain messages, e.g. autosafe notes
    let onDomainMessage = function(evts,src) {
        for(let i=0;i<evts.length;i++) {
            let evt = evts[i];
            app.notesManager.PutNote(evt.a,'info');
        }
    }
    app.domain.Observe(onDomainMessage,[eoq2.event.EvtTypes.MSG]);

    //listen to all changes
    if($DEBUG) {
        let onDomainChanges = function(evts,src) {
            let chgMsgs = []
            for(let i=0;i<evts.length;i++) {
                let evt = evts[i];
                let cid = evt.a[0];
                let type = evt.a[1];
                let targetId = evt.a[2].v;
                let featureName = evt.a[3];
                chgMsgs.push(cid+": "+type+" #"+targetId+" "+featureName);
            }
            let chgMsg = chgMsgs.join("\n");
            app.notesManager.PutNote(chgMsg,'info');
        }
        app.domain.Observe(onDomainChanges,[eoq2.event.EvtTypes.CHG]);
    }

    // return tools;
}

async function InitAppData(app)
{    
    return true;
}

function InitStickys(app) {
    let workspaceSticky = new jsa.Sticky( {
        name : 'Workspace',
        direction : 'nw',
        icon : app.settings.iconPath+'/tree.svg',
        content : '',
        startEnabled : false,
        isResizable : true,
        startCollapsed : true,
        style : ['jsa-sticky','workspace-sticky']
    });

    let paletteSticky = new jsa.Sticky( {
        name : 'Palette',
        direction : 'ne',
        icon : app.settings.iconPath+'/edit.svg',
        content : '',
        startEnabled : false,
        isResizable : true,
        startCollapsed : true,
        style : ['jsa-sticky','palette-sticky']
    }); 

    let outlineSticky = new jsa.Sticky( {
        name : '',
        direction : 'se',
        icon : app.settings.iconPath+'/globe.svg',
        content : '',
        startEnabled : false,
        isResizable : true,
        startCollapsed : true,
        style : ['jsa-sticky','outline-sticky'],
        containerStyle : ['jsa-sticky-container','outline-sticky-container']
    });

    let viewManagerSticky = new jsa.Sticky( {
        name : 'Views',
        direction : 'sw',
        icon : app.settings.iconPath+'/eye.svg',
        startEnabled : false,
        isResizable : true,
        startCollapsed : true,
        style : ['jsa-sticky','view-manager-sticky']
    });

    //Create a select ctrl based view selector
    let labels = [];
    let values = [];
    let views = app.viewManager.GetChildren();
    for(let i=0;i<views.length;i++) {
        let view = views[i];
        values.push(view);
        labels.push(view.name);
    }

    let viewSelector = new jsa.SelectCtrl({
        style : ['jsa-select-ctrl','jsa-col-12t'],
        labels: labels,
        values: values,
        onChangeCallback: function(event) {
            let view = this.GetValue();
            app.commandManager.Execute(new jsa.ChangeViewCommand(app.viewManager,view));
        }
    });
    let activeView = app.viewManager.GetActiveView();
    viewSelector.SetValue(activeView);
    viewManagerSticky.AddChild(viewSelector);

    let selectSelectorUpdater = new jsa.Observer( {
        data : viewSelector,
        onNotifyCallback : function(event) {
            //rebuild the view menu
            if(jsa.EVENT.IS_INSTANCE(event,jsa.EVENT.TYPES.ADD_CHILD) || 
            jsa.EVENT.IS_INSTANCE(event,jsa.EVENT.TYPES.REMOVE_CHILD)) {
                viewSelector.RemoveAllOptions();
                let views = app.viewManager.GetChildren();
                for(let i=0;i<views.length;i++) {
                    let view = views[i];
                    viewSelector.AddOption(view.name,view);
                }
                let activeView = app.viewManager.GetActiveView();
                viewSelector.SetValue(activeView);

            } else if(jsa.EVENT.IS_INSTANCE(event,jsa.EVENT.TYPES.SET_ACTIVE_VIEW)) {
                let view = event.value;
                viewSelector.SetValue(view);
            }
        }
    });

    app.viewManager.StartObserving(selectSelectorUpdater);

    //add stickies to the app
    var stickies = [workspaceSticky,paletteSticky,outlineSticky,viewManagerSticky];
    for(var i=0;i<stickies.length;i++) {
        app.AddChild(stickies[i]);
    }

    return {
        workspaceSticky: workspaceSticky,
        paletteSticky: paletteSticky,
        outlineSticky: outlineSticky,
        viewManagerSticky: viewManagerSticky
    }
};

function AttachTreeToWorkspaceSticky(app) {
    let treeView=$app.plugins.require('plugin.ecoreTreeView').create(app.ecoreSync,'workspaceStickyTree',app.stickies.workspaceSticky.GetContainingDom(),0,'Workspace','tree-workspaceSticky');
    return treeView;
};

function HideSplash(app) {
    app.splash.Hide();
};

function TerminateWithError(app,title,msg) {
    var msgBox = new jsa.Modal({
        name: title,
        content : msg,
        buttons : {
            restart: {
              name: 'Restart',
              startEnabled: true,
              data: this,
              onClickCallback: function(event) {
                location.reload(); 
              }
            }
          }
      });
      app.AddChild(msgBox);
};