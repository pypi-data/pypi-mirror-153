/*
 * Bjoern Annighoefer 2019
 */

var eoq2 = eoq2 || {};
eoq2.serialization = eoq2.serialization || {};

Object.assign(eoq2.serialization,(function() {

    function Serializer() {
        //ABSTRACT
    };    

    Serializer.prototype.Ser = function(val) {
        throw new Error("Not implemented.");
    }

    Serializer.prototype.Des = function(code) {
        throw new Error("Not implemented.");
    };
    
    //legacy support
    Serializer.prototype.serialize = function(val) {
        return this.Ser(val);
    };

    Serializer.prototype.deserialize = function(code) {
        return this.Des(code);
    };    

    return {
        Serializer : Serializer
    };
})());
    