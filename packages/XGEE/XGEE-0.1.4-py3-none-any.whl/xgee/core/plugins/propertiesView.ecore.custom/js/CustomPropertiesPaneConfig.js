// 2020 Bjoern Annighoefer

var PROPERTIES_VIEW_ECORE_CUSTOM = PROPERTIES_VIEW_ECORE_CUSTOM || {};

Object.assign(PROPERTIES_VIEW_ECORE_CUSTOM,(function(){
    //define the display of every class and feature of the class
    //this is an example config that is never used.
    let DEFAULT_CONFIG = {
        // entries in the form
        'namespaceURI': {
            'ClassName' : {
                'FeatureName' : {
                    'name' : 'display name', //null means default
                    'description' : 'This is a demo feature. You will never the able to set it', //textual description
                    'scope' : 'local',//'global','custom',
                    'customFilter' : QRY.His(-1).Pth('name'), //, null. for references and containments: only show elements that are retrieved by the following query. Use His(-1) to refer to start the query relative to the selected element. null means all elements are selected
                    'emptyAutocompleteMsg' : 'None' //Text that is shown, if no elements can be selected 
                }
            },
        }
    };

    return {
        DEFAULT_CONFIG : DEFAULT_CONFIG
    }
})());