import * as util from "./js/util.js"

async function convertMenuEntry(menuItems,key,entry)
{
    if('entry'==entry.type)
    {
        menuItems[key]=entry.value
        menuItems[key]['isHtmlName']=true
    }

    if('submenu'==entry.type)
    {
        menuItems[key]={name:entry.value.getName(),icon:entry.value.getIcon(), items: convertMenu(entry.value,false),action:false};
    }

    if('provider'==entry.type)
    {
        var res=await entry.value();
        for(let pkey in res)
        {
            await convertMenuEntry(menuItems,pkey,res[pkey]);
        }                
    }    
}


async function convertMenu(contextMenu,root=true)
{
    //Converts the ContextMenu to the jquery ContextMenu datastructure
    var cMenu=await contextMenu;

    if(cMenu)
    {
        var entries=await cMenu.getEntries();
        var menuItems={};

        for(let key in entries)
        {
            await convertMenuEntry(menuItems,key,entries[key]);        
        }

        var keys=Object.keys(menuItems);
        if(keys.length)
        {
            if(root)
            {
                return {
                        callback:function(){},
                        items:menuItems
                    };
            }
            else
            {
                return menuItems;
            }
        }
        else
        {
            return false;
        }
    }    
    
    return false;
}

async function mergeMenus(menus)
{
    if(menus.length >0)
    {
        return await menus[0];
    }
    else
    {
        return null;
    }
}

export async function init(pluginAPI) {      
    var contextMenuModules=await pluginAPI.loadModules(["js/ContextMenu.js","js/util.js"])         
    var factory=contextMenuModules[0].contextMenuFactory


    var contextMenuDOM=document.createElement('div');
    contextMenuDOM.id='jsa-contextMenu-plugin';
    document.body.appendChild(contextMenuDOM);
    $('#jsa-contextMenu-plugin').css('z-index', 9999);

    $.contextMenu( { selector: '#jsa-contextMenu-plugin', build:  function($trigger,e){  if(e.menu){ return e.menu; } else { return false } },  trigger: 'none' } );
    
    pluginAPI.expose({createContextMenu: factory.createContextMenu,createContextMenuEntry: factory.createContextMenuEntry,showContextMenu:async function(position,contextMenu){
        var menu=await convertMenu(await contextMenu);
        if(menu)
        {          
           $('#jsa-contextMenu-plugin').trigger($.Event('contextmenu', {pageX: position.x, pageY: position.y,menu:menu}))    
        }
    }, util:util});
    return true;     
};

export var meta={"id":"contextMenu",description:"Generic contextMenu Definition","author":"Matthias Brunner","version":"0.1.0","requires":['plugin.contextMenu']};



