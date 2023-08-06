/*
 * Bjoern Annighoefer 2019
 */

var eoq2 = eoq2 || {};
eoq2.serialization = eoq2.serialization || {};

Object.assign(eoq2.serialization,(function() {

    function JsonSerializer() {
        
    };  
    JsonSerializer.prototype = Object.create(eoq2.serialization.Serializer.prototype);  

    JsonSerializer.prototype.Ser = function(val) {
        return JSON.stringify(val);
    }

    JsonSerializer.prototype.Des = function(code) {
		console.log(code);
        let jsonObj = JSON.parse(code);
        let val = this.RecreateObjects(jsonObj);
        return val;
    };

    JsonSerializer.prototype.RecreateObjects = function(jsonObj) {
        //TODO: Implement object creation if necessary
        return jsonObj;
    };
    

    return {
        JsonSerializer : JsonSerializer
    };
})());