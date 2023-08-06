// 2020 Bjoern Annighoefer

var PROPERTIES_VIEW_INFO = PROPERTIES_VIEW_INFO || {};

Object.assign(PROPERTIES_VIEW_INFO,(function(){
    function InfoPropertiesPaneProvider(name) {
        PROPERTIES_VIEW.PropertiesPaneProvider.call(this,name,0);
        //All propertiesView panes must inherit from this class
        this.INDENTSTR = "&nbsp;&nbsp;";
    }
    InfoPropertiesPaneProvider.prototype = Object.create(PROPERTIES_VIEW.PropertiesPaneProvider.prototype);
    
    InfoPropertiesPaneProvider.prototype.IsApplicable = function(selection) {
        return true;
    };
    
    InfoPropertiesPaneProvider.prototype.CreatePane = function(selection) {
        let content = "";
        if(this.IsArray(selection)){
            let nSelection = selection.length;
            content = "<p>Array with "+nSelection+" Element"+(nSelection==1?"":"s")+"</p>";
            for(let i=0;i<selection.length;i++) {
                let elem = selection[i];
                content += this.ElemToText(elem);
            }
        } else {
            content = this.ElemToText(selection);
        }

        let pane = new jsa.CustomFlatContainer({
            content: content
        });
        return pane;
    };

    InfoPropertiesPaneProvider.prototype.ElemToText = function(elem) {
        let type = this.GetTypeName(elem);
        value = this.ValueToText(elem,true);
        let text = "<h2>"+type+"</h2>" +
                    "<p>"+value+"</p>";
        return text; 
    };

    InfoPropertiesPaneProvider.prototype.ValueToText = function(elem,recurse) {
        let valueStr = "EMPTY";
        if(null == elem) {
            valueStr = "null";
        } else if(this.IsFunction(elem)) {
            valueStr = "Function";
        } else if(this.IsArray(elem)) {
            if(recurse) {
                let textSegs = [];
                for(let i=0;i<elem.length;i++) {
                    textSegs.push(this.ValueToText(elem[i],false));
                }
                textSegs.push("}");
                valueStr = "["+textSegs.join(", ")+"]";
            } else {
                valueStr = "Array(length: "+elem.length+")";
            }
        } else if(this.IsObject(elem)) {
            if(recurse) {
                let textSegs = [];
                for(let a in elem) {
                    textSegs.push(a + " : " + this.ValueToText(elem[a],false));
                }
                valueStr = "{<br/>"+this.INDENTSTR+textSegs.join(",</br>"+this.INDENTSTR)+"<br/>}";
            } else {
                valueStr = this.GetTypeName(elem);
            }
        } else if(this.IsString(elem)) {
            valueStr = '"'+elem+'"';
        } else {
            valueStr = elem.toString();
        }
        return valueStr;
    };

    InfoPropertiesPaneProvider.prototype.IsFunction = function(elem) {
        return (elem instanceof Function);
    };

    InfoPropertiesPaneProvider.prototype.IsArray = function(elem) {
        return (elem instanceof Array);
    };

    InfoPropertiesPaneProvider.prototype.IsObject = function(elem) {
        return (elem instanceof Object);
    };

    InfoPropertiesPaneProvider.prototype.IsString = function(elem) {
        return (typeof(elem)=="string");
    };

    InfoPropertiesPaneProvider.prototype.GetTypeName = function(elem) {
        let type = "UNKNOWN";
        if(elem.constructor && elem.constructor.name) {
            type = elem.constructor.name;
        } else {
            type = typeof(elem);
        }
        return type;
    };

    return {
        InfoPropertiesPaneProvider : InfoPropertiesPaneProvider
    }
})());


