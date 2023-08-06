// This is the baseclass for all plugins that would like to provide a context menu
// 2020 Matthias Brunner

class ContextMenu{

    constructor(id,name,priority,icon=null){
        this.id=id;
        this.priority=priority;
        this.name=name;
        this.entries={};
        this.icon=icon;
    }

    getName(){
        return this.name;
    }

    getIcon()
    {
        return this.icon;
    }

    addNewEntry(key,name,callback,icon=null){
        var entry=new ContextMenuEntry(name,callback,icon);
        this.entries[key]={type:'entry',value:entry};
        return entry;
    }

    addEntry(key,entry)
    {
        this.entries[key]={type: 'entry',value:entry};
    }
    

    addNewSubMenu(key,id,name,priority)
    {
        var subMenu=new ContextMenu(id,name,priority);
        this.entries[key]={type:'submenu',value:subMenu};
        return subMenu;
    }

    addSubMenu(key,subMenu)
    {
        this.entries[key]={type:'submenu',value:subMenu};
    }

    addEntryProvider(key,providerFunc)
    {
        this.entries[key]={type:'provider',value:providerFunc};
    }
   
    async getEntries(){
        return this.entries
    }

    has(key){
        if(this.entries[key])
        {
            return true;
        }
        else
        {
            return false;
        }
    }

    get(key){
        if(this.entries[key])
        {
            return this.entries[key];
        }
        else
        {
            return null;
        }
    }

    set(key,value){
        this.entries[key]=value;
    }

    copy()
    {
        var copy=new ContextMenu(this.id+'_copy',this.name,this.priority,this.icon);
        for(let key in this.entries)
        {
            if('entry'==this.entries[key].type){
                copy.addEntry(key,this.entries[key].value.copy())
            }

            if('submenu'==this.entries[key].type){
                copy.addSubMenu(key,this.entries[key].value.copy())
            }

            if('provider'==this.entries[key].type){
                copy.addEntryProvider(key,this.entries[key].value)
            }
        }
        return copy;
    }

}

class ContextMenuEntry{

    constructor(name,callback,icon=null)
    {
        this.name=name;
        this.callback=callback;
        this.icon=icon;
        this.disabled=false;
    }

    copy()
    {
        var copy=new ContextMenuEntry(this.name,this.callback,this.icon)
        if(this.disabled)
        {
            copy.disable();
        }
        return copy;
    }

    disable()
    {
        this.disabled=true;
    }

    enable()
    {
        this.disabled=false;
    }
}

class ContextMenuFactory{
    constructor(){

    }
    createContextMenu(id,name,priority=0,icon=null)
    {
        return new ContextMenu(id,name,priority,icon);
    }

    createContextMenuEntry(name,callback=null,icon=null)
    {
        return new ContextMenuEntry(name,callback,icon);
    }

}

var contextMenuFactory=new ContextMenuFactory();
export {ContextMenuEntry,ContextMenu,contextMenuFactory}



