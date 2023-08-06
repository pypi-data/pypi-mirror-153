import * as cmenu from "./ContextMenu.js";

async function collect(providers,selection)
{
    let collection=providers.flatMap(function(provider){ return provider.getContextMenu(selection)});    
    return collection.filter(menu => {return menu!=null})
}


async function merge(menus)
{

    var sortedMenus=menus.sort(function(a,b){
        if(a.priority > b.priority)
        {
            return -1;
        }
        if(a.priority < b.priority)
        {
            return 1;
        }
        return 0
    });

    var menu=sortedMenus[0].copy();

    for(let i=1;i<sortedMenus.length;i++)
    {
        let entries=await sortedMenus[i].getEntries();

        for(let key in entries)
        {
            if(!menu.has(key))
            {
                if('entry'==entries[key].type)
                {
                    menu.addEntry(key,entries[key].value.copy())
                }

                if('submenu'==entries[key].type)
                {
                    menu.addSubMenu(key,entries[key].value.copy())
                }

                if('provider'==entries[key].type)
                {
                    menu.addEntryProvider(key,entries[key].value)
                }
            }
            else
            {
                var presentEntry=menu.get(key);
                if('submenu'==entries[key].type && 'submenu' == presentEntry.type)
                {
                   menu.set(key,{type:'submenu',value:await merge([presentEntry.value,entries[key].value])});
                   
                }
            }
        }
    }   

    return menu;

}

async function collectAndMerge(providers,selection)
{
    var menus=await collect(providers,selection);
    return merge(menus);
}

export {collect,merge,collectAndMerge}
