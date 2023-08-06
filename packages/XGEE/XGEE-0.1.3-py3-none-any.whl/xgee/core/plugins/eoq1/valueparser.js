var jseoq = jseoq || {};
jseoq.ValueParser = (function() {
	function isAlpha(str)
	{
		return str.length === 1 && str.match(/[a-z]/i);
	};
	
    function ValueToString (value) {
        if(value.type == jseoq.model.ValueTypesE.INT)
        {
            return value.v.toString();
        }  else if(value.type == jseoq.model.ValueTypesE.FLOAT) {
            if(Number.isInteger(value.v))
            {
                return value.v.toString()+".0";
            }
            else
            {
                return value.v.toString(); 
            }            
        } else if(value.type == jseoq.model.ValueTypesE.BOOL) {
            if(value.v) {
                return 'true';
            } else {
                return 'false';
            }
        } else if(value.type == jseoq.model.ValueTypesE.STRING) {
            return "'"+encodeURIComponent(value.v)+"'";
        } else if(value.type == jseoq.model.ValueTypesE.OBJECTREF) {
            return '#'+value.v;
        } else if(value.type == jseoq.model.ValueTypesE.HISTORYREF) {
            return '$'+value.v;
        } else if(value.type == jseoq.model.ValueTypesE.EMPTY) {
            return '%';
        } else if(value.type == jseoq.model.ValueTypesE.LIST) {
            var substrs = [];
            for(var i=0; i<value.v.length; i++) {
            	var subvalue = value.v[i];
                substrs.push(ValueToString(subvalue));
            }
            return '['+substrs.join(',')+']';
        } else {
            throw new Error('Cannot convert EOQ value of type '+value.type+' string');
        }
    };
    
    function StringToValue (valueStr) {
        //definition of the parser states
        var VALUE_START = 1;
        var VALUE = 2;
        var VALUE_END = 3;
        //start of parsing
        var rootValueContainer = new jseoq.model.ListValue(); //initialize the value with an empty list
        var currentValueContainer = rootValueContainer;
        var parentContainers = [];
        var state = VALUE_START;
        var valueStart = 0;
        var valueEnd = 0;
        var valueType = 0;
        var nOpenBrakets = 0;
        
        var n = valueStr.length;
        for(var i=0;i<n;i++) {
            var c = valueStr[i];
            if(VALUE_START == state) {
                valueStart = i;
                valueEnd = i;
                if(('0' <= c && c <= '9') || '-' == c) {
                    valueType = jseoq.model.ValueTypesE.INT;
                    state = VALUE;
                } else if('.'==c) {
                    valueType = jseoq.model.ValueTypesE.FLOAT;
                    state = VALUE;
                } else if('t'==c || 'f'==c) {
                    valueType = jseoq.model.ValueTypesE.BOOL;
                    state = VALUE;
                } else if('#'==c) {
                    valueStart = i+1;
                    valueEnd = i+1;
                    valueType = jseoq.model.ValueTypesE.OBJECTREF;
                    state = VALUE;
                } else if('\''==c) {
                    valueStart = i+1;
                    valueEnd = i+1;
                    valueType = jseoq.model.ValueTypesE.STRING;
                    state = VALUE;
                } else if('%'==c) {
                    valueStart = i+1;
                    valueEnd = i+1;
                    valueType = jseoq.model.ValueTypesE.EMPTY;
                    state = VALUE;
                } else if('$'==c) {
                    valueStart = i+1;
                    valueEnd = i+1;
                    valueType = jseoq.model.ValueTypesE.HISTORYREF;
                    state = VALUE;
                } else if('['==c) {
                    valueType = jseoq.model.ValueTypesE.LIST;
                    nOpenBrakets += 1;
                    sublist = new jseoq.model.ListValue();
                    currentValueContainer.v.push(sublist);
                    parentContainers.push(currentValueContainer);
                    currentValueContainer = sublist;
                    state = VALUE_START;
                } else if(']'==c) { //occures only for empty lists
                	nOpenBrakets -= 1;
                    currentValueContainer = parentContainers.pop(); 
                    state = VALUE_END;
                } else {
                    throw new Error('Unexpected character \''+c+'\' at '+i+' in '+valueStr);
                }
            } else if(VALUE == state) {
                if(']'==c) {
                	currentValueContainer.v.push(__StringToPritiveValue(valueStr.substring(valueStart,valueEnd+1),valueType));
                    nOpenBrakets -= 1;
                    currentValueContainer = parentContainers.pop(); 
                    state = VALUE_END; //change the state to prevent that the next closing ] saves the value again
                } else if(','==c && nOpenBrakets>0) {
                    currentValueContainer.v.push(__StringToPritiveValue(valueStr.substring(valueStart,valueEnd+1),valueType));
                    state = VALUE_START;
                } else if(jseoq.model.ValueTypesE.OBJECTREF==valueType && ('0' <= c && c <= '9')) {
                    valueEnd = i;
				} else if((jseoq.model.ValueTypesE.INT==valueType || jseoq.model.ValueTypesE.FLOAT==valueType) && ('0' <= c && c <= '9')) {
                    valueEnd = i;
				} else if(jseoq.model.ValueTypesE.INT==valueType && '.'==c) {
                    valueEnd = i;
                    valueType = jseoq.model.ValueTypesE.FLOAT
                } else if(jseoq.model.ValueTypesE.FLOAT==valueType && ('0' <= c && c <= '9')) {
                    valueEnd = i;
				} else if(jseoq.model.ValueTypesE.HISTORYREF==valueType && (('0' <= c && c <= '9') || '-' == c)) {
                    valueEnd = i;
                } else if(jseoq.model.ValueTypesE.BOOL==valueType && isAlpha(c)) {
                    valueEnd = i;
                } else if(jseoq.model.ValueTypesE.STRING==valueType && '\''!=c) {
                    valueEnd = i;
                } else if(jseoq.model.ValueTypesE.STRING==valueType && '\''==c) {
                    valueEnd = i-1; //this is necessary for emtpy string
                } else {
                    throw new Error('Unexpected character \''+c+'\' at '+i+' in '+valueStr);
            	}
            } else if(VALUE_END==state) {
                if(']'==c) {
                    nOpenBrakets -= 1 
                    currentValueContainer = parentContainers.pop(); //TODO
                } else if(','==c && nOpenBrakets>0) {
                    state = VALUE_START;
                } else {
                    throw new Error('Unexpected character \''+c+'\' at '+i+' in '+valueStr);
                }
            }
        }
        if(nOpenBrakets>0) {
            throw new Error(nOpenBrakets+' lists are not closed in '+ valueStr);
        }
        
        if(VALUE==state) {
        	currentValueContainer.v.push(__StringToPritiveValue(valueStr.substring(valueStart,valueEnd+1),valueType));
        }
        
        return rootValueContainer.v[0];
    };
    
    function __StringToPritiveValue (valueStr,valueType) {
        var value = null;
        if(valueType == jseoq.model.ValueTypesE.INT) {
            value = new jseoq.model.IntValue();
            value.v = Number.parseInt(valueStr);
        } else if(valueType == jseoq.model.ValueTypesE.FLOAT) {
            value = new jseoq.model.FloatValue();
            value.v = Number.parseFloat(valueStr);
        } else if(valueType == jseoq.model.ValueTypesE.STRING) {
            value = new jseoq.model.StringValue();
            value.v = decodeURIComponent(valueStr);
        } else if(valueType == jseoq.model.ValueTypesE.BOOL) {
            value = new jseoq.model.BoolValue();
            if('true' == valueStr) {
                value.v = true;
            } else if('false' == valueStr) {
                value.v = false;
            } else {
                throw new Error("Unsupported boolean value '"+valueStr+". Should be 'true' or 'false'");
            }
        } else if(valueType == jseoq.model.ValueTypesE.OBJECTREF) {
            value = new jseoq.model.ObjectRefValue();
            value.v = Number.parseInt(valueStr);
        } else if(valueType == jseoq.model.ValueTypesE.EMPTY) {
            value = new jseoq.model.EmptyValue();
        } else if(valueType == jseoq.model.ValueTypesE.HISTORYREF) {
            value = new jseoq.model.HistoryRefValue();
            value.v = Number.parseInt(valueStr);
        } else {
            throw new Error("Unknown value type "+ valueType);
        }
        return value;
    };
    
    function JsToValue (pvalue) {
    	var value = 0;
        if(typeof pvalue == "number" && Number.isInteger(pvalue)) {
            value = new jseoq.model.IntValue();
            value.v=pvalue;
        } else if(typeof pvalue == "number" /*&& Number.isFloat(pvalue)*/) {
        	value = new jseoq.model.FloatValue();
        	value.v = pvalue;
        } else if(typeof pvalue == "boolean") {
        	value = new jseoq.model.BoolValue();
        	value.v = pvalue;
        } else if(typeof pvalue == "string") {
        	value = new jseoq.model.StringValue();
        	value.v = pvalue;
        } else if(pvalue instanceof jseoq.model.ObjectRefValue) {
        	value = pvalue;
        } else if(pvalue instanceof jseoq.model.HistoryRefValue) {
        	value = pvalue;
        } else if(null == pvalue) {
        	value = new jseoq.model.EmptyValue();
        } else if(pvalue instanceof Array) {
            value = new jseoq.model.ListValue();
            for(var i=0;i<pvalue.length;i++) {
                value.v.push(this.JsToValue(pvalue[i]));
            }
            return value;
        } else {
            throw Error('Cannot convert python data type '+(typeof pvalue)+' to EOQ value: '+pvalue);
        }
        return value;
    };
        
    function ValueToJs (value) {
        if([jseoq.model.ValueTypesE.INT,jseoq.model.ValueTypesE.FLOAT,jseoq.model.ValueTypesE.BOOL,jseoq.model.ValueTypesE.STRING].includes(value.type)) {
            return value.v;
        } else if([jseoq.model.ValueTypesE.OBJECTREF,jseoq.model.ValueTypesE.HISTORYREF].includes(value.type)) {
            return value;
        } else if(value.type == jseoq.model.ValueTypesE.EMPTY) {
            return null
        } else if(value.type == jseoq.model.ValueTypesE.LIST) {
            var pvalue = [];
            for(var i=0;i<value.v.length;i++) {
                pvalue.push(this.ValueToJs(value.v[i]));
            }
            return pvalue;
        }else {
            throw new Error('Cannot convert EOQ value '+(typeof value)+' to python data type '+value);
        }
    };

    function IsList(value) {
        return (value.type == jseoq.model.ValueTypesE.LIST);
    };

    function IsBool(value) {
        return (value.type == jseoq.model.ValueTypesE.BOOL);
    };

    function IsInt(value) {
        return (value.type == jseoq.model.ValueTypesE.INT);
    };

    function IsFloat(value) {
        return (value.type == jseoq.model.ValueTypesE.FLOAT);
    };

    function IsString(value) {
        return (value.type == jseoq.model.ValueTypesE.STRING);
    };

    function IsObjectRef(value) {
        return (value.type == jseoq.model.ValueTypesE.OBJECTREF);
    };

    function IsHistoryRef(value) {
        return (value.type == jseoq.model.ValueTypesE.HISTORYREF);
    };

    function IsEmpty(value) {
        return (value.type == jseoq.model.ValueTypesE.EMPTY);
    }

    return {
        ValueToString : ValueToString,
        StringToValue : StringToValue,
        JsToValue : JsToValue,
        ValueToJs : ValueToJs,
        IsList : IsList,
        IsBool : IsBool,
        IsInt : IsInt,
        IsFloat : IsFloat,
        IsString : IsString,
        IsObjectRef : IsObjectRef,
        IsHistoryRef : IsHistoryRef,
        IsEmpty : IsEmpty
    };
})();
        