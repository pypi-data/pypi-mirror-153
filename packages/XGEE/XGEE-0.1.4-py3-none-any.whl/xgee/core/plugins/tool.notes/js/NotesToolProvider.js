// 2020 Bjoern Annighoefer

var NOTES_TOOL = NOTES_TOOL || {};

Object.assign(NOTES_TOOL,(function(){
    function NotesToolProvider(pluginApi,name,params) {
        TOOLS.ToolProvider.call(this,name,params.position);
        //params
        Object.assign(this,params); //copy params

        //internals
        this.app = pluginApi.getGlobal('app'); 
        this.pluginApi = pluginApi;
        this.tool = null
    } 
    NotesToolProvider.prototype = Object.create(TOOLS.ToolProvider.prototype);

    //@Overwrite
    NotesToolProvider.prototype.CreateTool = function() {
        //Create new dash
        let notesManager = this.app.notesManager;
        if(notesManager) {
            this.tool = new NOTES_TOOL.NotesTool({
                app : this.app,
                notesManager : notesManager
            });
        }

        return this.tool;
    };

    return {
        NotesToolProvider : NotesToolProvider
    };
})());