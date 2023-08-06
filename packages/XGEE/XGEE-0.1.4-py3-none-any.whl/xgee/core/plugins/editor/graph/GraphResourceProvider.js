/* GRAPH RESOURCE PROVIDER */

function GraphResourceProvider(basePath) {
    this.basePath = basePath;

    this.resourceCache = new Map(); // do not load a resource twice
    this.URLCache=new Map();

    return this;
};

GraphResourceProvider.prototype.LoadResource = function(path) {
    var realPath = this.basePath+path;
    if(this.resourceCache.has(realPath)) {
        return this.resourceCache.get(realPath);
    }
    var resource = this.__LoadResourceExternaly(realPath);
    this.resourceCache.set(realPath,resource);
    return resource;
};

GraphResourceProvider.prototype.__LoadResourceExternaly = function(path) {
	var xhttp = new XMLHttpRequest();
    xhttp.open("GET", path, false);
    try {
        xhttp.send();
    } catch {
        console.trace();
        console.error("Could not load resource: "+path);
        throw new Error("Could not load resource: "+path);
    }
	return xhttp.responseText;
};


GraphResourceProvider.prototype.LoadResourceToBlobURL = function(path) {
    var realPath = this.basePath+path;
    if(this.URLCache.has(realPath)) {
        return this.URLCache.get(realPath);
    }
    var resource = this.__LoadResourceExternaly(realPath);
    let blob = new Blob([resource], {type: 'image/svg+xml'});
    let url = URL.createObjectURL(blob);
    this.URLCache.set(realPath,url);
    return url;
};

export default GraphResourceProvider