//jsApplication plugin information

export function init(pluginAPI) {  
    
    pluginAPI.expose({"error":"API unavailable"});
	
    return pluginAPI.loadScripts([
		"model/model.js",
		"domains/domain.js",
		"domains/httppostdomain.js",
		"valueparser.js",
		"commandparser.js",
		"resultparser.js"
	]);
};

export var meta={
	"id":"eoq1",
	description:"JS implentation of Essential Object Query (EOQ) v1",
	"author":"Bjoern Annighoefer",
	"version":"1.0.0",
	"date":"2019-06-01",
	"requires":[]
};



