// 2020 Bjoern Annighoefer

var PROPERTIES_VIEW_ECORE_WORKSPACE = PROPERTIES_VIEW_ECORE_WORKSPACE || {};

Object.assign(PROPERTIES_VIEW_ECORE_WORKSPACE,(function(){
    //define the display of every class and feature of the class
    let DEFAULT_CONFIG = {
        'http://www.eoq.de/workspacemdbmodel/v1.0': {
            'Workspace': {
                'name' : {
                    'name' : 'Name', //null means default
                },
            },
            'Directory': {
                'name' : {
                    'name' : 'Name', //null means default
                },
            },
            'ModelResource': {
                'name' : {
                    'name' : 'Name', //null means default
                },
            },
            'XmlResource': {
                'name' : {
                    'name' : 'Name', //null means default
                },
            },
            'TextResource': {
                'name' : {
                    'name' : 'Name', //null means default
                },
            },
            'RawResource': {
                'name' : {
                    'name' : 'Name', //null means default
                },
            },
        }
    };

    return {
        DEFAULT_CONFIG : DEFAULT_CONFIG
    }
})());