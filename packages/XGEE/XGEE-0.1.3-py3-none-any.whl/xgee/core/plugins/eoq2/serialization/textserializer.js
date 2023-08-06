/*
 * Bjoern Annighoefer 2019
 *
 *
 * Modified 2020 Christian Mollière
 * Modified 2021 Bjoern Annighoefer
 *
 */

/*
    Helper functions
*/

function SwapKeysAndValues(json){
    let ret = {};
    for(let key in json){
        ret[json[key]] = key;
    }
    return ret;
}

function GetDictionaryValues(json) {
    let values = [];
    for(let key in json){
        values.push(json[key]);
    }
    return values;
}

function DoNothing(){
    // placeholder for unimplemented function
}

/*
    Global Constants & Settings
 */

// Create dictionary from external symbol definition.
// This will be needed later to convert i.e. "!" -> "CLS"
SYMBOLS_2_QRY_DICT = SwapKeysAndValues(eoq2.query.QRY_SYMBOLS);

// List all commands that need a list of args and not *args or a mix
QRY_CMDS_W_LIST_INPUT = ["[","&ZIP"];
QRY_CMDS_W_SINGLE_OR_LIST_INPUT = [":","&EQA"];
QRY_CMDS_W_MIXED_INPUT = ["@"];

// Settings of divider symbols
EXPRESSION_DIVIDERS = [";", "\r", "\n"];
QRY_ARG_DIVIDER = ",";
CMD_ARG_DIVIDER = " ";

// Change this constant to control the context distance of
// the error message if parsing fails.
ERROR_MSG_VIEW_DISTANCE = 3;

// Remove unnecessary outer parentheses for js2txt
REMOVE_OUTER_QRY_PARENTHESES = true;

// Assign stop symbols to starters
STOPPING_SYMBOL_DICT = {
    "(": ")",
    "{": "}",
    "[": "]",
};

// Define parsing cmds enum
PARSING_CMDS = {
    STEP_IN : "!!INN!!",
    STEP_OUT : "!!OUT!!",
};


/*
    Class definition
 */
var eoq2 = eoq2 || {};
eoq2.serialization = eoq2.serialization || {};


Object.assign(eoq2.serialization,(function() {

    function TextSerializer() {
        /*
        *   General
        * */
        this._debugMode = false;

        /*
        *   JS2TXT Translators
        * */
        this.StripOuterQry = function (str) {
            if (REMOVE_OUTER_QRY_PARENTHESES) {
                if (str[0]==="(" && (this._IsQry(str[1]) || this._IsQry(str.slice(1,5))) && str[str.length-1]===")"){
                    return str.slice(1,str.length-1);
                }else{
                    return str;
                }
            }else{
                return str;
            }
        }

        this.cmdTranslator = function(o) {
            if(o.cmd) {
                if (o.cmd === CMD.CmdTypes.CMP){
                    return o.a.map(v => this.Ser(v)).join("\n");
                }else if (Array.isArray(o.a)) {
                    return o.cmd + " " + o.a.map(v => this.StripOuterQry(this.Ser(v))).join(" ");
                }else{
                    let argStr = this.StripOuterQry(this.Ser(o.a));
                    if(0<argStr.length) {
                        return o.cmd + " " + argStr;
                    } else {
                        return o.cmd
                    }
                }
            } else {
                throw new Error(); //forces trying the next translator
            }
        };

        this._TranslateQryArgs = function(a,multiArgs=false,prefix="(",postfix=")",prePostFixForSingleElement=false,separator=",") {
            if(multiArgs && Array.isArray(a)) {
                if(prePostFixForSingleElement || a.length>1) {
                    let argStrs = [];
                    for(let i=0;i<a.length;i++) {
                        argStrs.push(this.Ser(a[i]));
                    }
                    return prefix + argStrs.join(separator) + postfix;
                } else if(a.length==1) {
                    return this.Ser(a[0]);
                } else { //0 element list
                    return '';
                }
            } else {
                if(prePostFixForSingleElement) {
                    return prefix + this.Ser(a) + postfix
                } else {
                    return this.Ser(a)
                }
            }
        };


        this.resTranslator =  function(o) {
            if(o.res) {
                return [o.res,o.s,o.n,o.c].join(" ")+" "+this.Ser(o.v)
            } else {
                throw new Error(); //forces trying the next translator
            }
        };

        this.qryTranslators = new Map();
        this.qryTranslators.set(QRY.QrySegTypes.OBJ, o => QRY.QRY_SYMBOLS[QRY.QrySegTypes.OBJ]+this._TranslateQryArgs(o.v));
        this.qryTranslators.set(QRY.QrySegTypes.HIS, o => QRY.QRY_SYMBOLS[QRY.QrySegTypes.HIS]+this._TranslateQryArgs(o.v));
        this.qryTranslators.set(QRY.QrySegTypes.PTH, o => QRY.QRY_SYMBOLS[QRY.QrySegTypes.PTH]+this._TranslateQryArgs(o.v));
        this.qryTranslators.set(QRY.QrySegTypes.CLS, o => QRY.QRY_SYMBOLS[QRY.QrySegTypes.CLS]+this._TranslateQryArgs(o.v));
        this.qryTranslators.set(QRY.QrySegTypes.INO, o => QRY.QRY_SYMBOLS[QRY.QrySegTypes.INO]+this._TranslateQryArgs(o.v));
        this.qryTranslators.set(QRY.QrySegTypes.MET, o => QRY.QRY_SYMBOLS[QRY.QrySegTypes.MET]+this._TranslateQryArgs(o.v,true));
        this.qryTranslators.set(QRY.QrySegTypes.NOT, o => QRY.QRY_SYMBOLS[QRY.QrySegTypes.NOT]);
        this.qryTranslators.set(QRY.QrySegTypes.TRM, o => QRY.QRY_SYMBOLS[QRY.QrySegTypes.TRM]+this._TranslateQryArgs(o.v,true));
        this.qryTranslators.set(QRY.QrySegTypes.TRY, o => QRY.QRY_SYMBOLS[QRY.QrySegTypes.TRY]+this._TranslateQryArgs(o.v,true));
        this.qryTranslators.set(QRY.QrySegTypes.IDX, o => QRY.QRY_SYMBOLS[QRY.QrySegTypes.IDX]+this._TranslateQryArgs(o.v,true));
        this.qryTranslators.set(QRY.QrySegTypes.SEL, o => this._TranslateQryArgs(o.v,false,'{','}',true));
        this.qryTranslators.set(QRY.QrySegTypes.ARR, o => this._TranslateQryArgs(o.v,true,'[',']',true));
        this.qryTranslators.set(QRY.QrySegTypes.ZIP, o => QRY.QRY_SYMBOLS[QRY.QrySegTypes.ZIP]+this._TranslateQryArgs(o.v,true));
        this.qryTranslators.set(QRY.QrySegTypes.QRY, o => this._TranslateQryArgs(o.v,true,'(',')',true,''));
        this.qryTranslators.set(QRY.QrySegTypes.ANY, o => QRY.QRY_SYMBOLS[QRY.QrySegTypes.ANY]+this._TranslateQryArgs(o.v));
        this.qryTranslators.set(QRY.QrySegTypes.ALL, o => QRY.QRY_SYMBOLS[QRY.QrySegTypes.ALL]+this._TranslateQryArgs(o.v));
        this.qryTranslators.set(QRY.QrySegTypes.EQU, o => QRY.QRY_SYMBOLS[QRY.QrySegTypes.EQU]+this._TranslateQryArgs(o.v));
        this.qryTranslators.set(QRY.QrySegTypes.EQA, o => QRY.QRY_SYMBOLS[QRY.QrySegTypes.EQA]+this._TranslateQryArgs(o.v));
        this.qryTranslators.set(QRY.QrySegTypes.NEQ, o => QRY.QRY_SYMBOLS[QRY.QrySegTypes.NEQ]+this._TranslateQryArgs(o.v));
        this.qryTranslators.set(QRY.QrySegTypes.LES, o => QRY.QRY_SYMBOLS[QRY.QrySegTypes.LES]+this._TranslateQryArgs(o.v));
        this.qryTranslators.set(QRY.QrySegTypes.GRE, o => QRY.QRY_SYMBOLS[QRY.QrySegTypes.GRE]+this._TranslateQryArgs(o.v));
        this.qryTranslators.set(QRY.QrySegTypes.RGX, o => QRY.QRY_SYMBOLS[QRY.QrySegTypes.RGX]+this._TranslateQryArgs(o.v));
        this.qryTranslators.set(QRY.QrySegTypes.ADD, o => QRY.QRY_SYMBOLS[QRY.QrySegTypes.ADD]+this._TranslateQryArgs(o.v));
        this.qryTranslators.set(QRY.QrySegTypes.SUB, o => QRY.QRY_SYMBOLS[QRY.QrySegTypes.SUB]+this._TranslateQryArgs(o.v));
        this.qryTranslators.set(QRY.QrySegTypes.MUL, o => QRY.QRY_SYMBOLS[QRY.QrySegTypes.MUL]+this._TranslateQryArgs(o.v));
        this.qryTranslators.set(QRY.QrySegTypes.DIV, o => QRY.QRY_SYMBOLS[QRY.QrySegTypes.DIV]+this._TranslateQryArgs(o.v));
        this.qryTranslators.set(QRY.QrySegTypes.ORR, o => QRY.QRY_SYMBOLS[QRY.QrySegTypes.ORR]+this._TranslateQryArgs(o.v));
        this.qryTranslators.set(QRY.QrySegTypes.XOR, o => QRY.QRY_SYMBOLS[QRY.QrySegTypes.XOR]+this._TranslateQryArgs(o.v));
        this.qryTranslators.set(QRY.QrySegTypes.AND, o => QRY.QRY_SYMBOLS[QRY.QrySegTypes.AND]+this._TranslateQryArgs(o.v));
        this.qryTranslators.set(QRY.QrySegTypes.NAD, o => QRY.QRY_SYMBOLS[QRY.QrySegTypes.NAD]+this._TranslateQryArgs(o.v));
        this.qryTranslators.set(QRY.QrySegTypes.CSP, o => QRY.QRY_SYMBOLS[QRY.QrySegTypes.CSP]+this._TranslateQryArgs(o.v));
        this.qryTranslators.set(QRY.QrySegTypes.ITS, o => QRY.QRY_SYMBOLS[QRY.QrySegTypes.ITS]+this._TranslateQryArgs(o.v));
        this.qryTranslators.set(QRY.QrySegTypes.UNI, o => QRY.QRY_SYMBOLS[QRY.QrySegTypes.UNI]+this._TranslateQryArgs(o.v));
        this.qryTranslators.set(QRY.QrySegTypes.CON, o => QRY.QRY_SYMBOLS[QRY.QrySegTypes.CON]+this._TranslateQryArgs(o.v));
        
        //primitive types
        this.priTranslators = new Map();
        this.priTranslators.set("boolean", o => o.toString());
        this.priTranslators.set("number", o => o.toString());
        this.priTranslators.set("string", o => this._StringTranslator(o));
        this.priTranslators.set("object", o => this._ArrayTranslator(o));

        /*
        *   TXT2JS Constructors
        * */
        this.cmdConstructors = new Map();
        this.cmdConstructors.set(CMD.CmdTypes.GET, args => CMD.Get(...args));
        this.cmdConstructors.set(CMD.CmdTypes.SET, args => CMD.Set(...args));
        this.cmdConstructors.set(CMD.CmdTypes.ADD, args => CMD.Add(...args));
        this.cmdConstructors.set(CMD.CmdTypes.REM, args => CMD.Rem(...args));
        this.cmdConstructors.set(CMD.CmdTypes.MOV, args => CMD.Mov(...args));
        this.cmdConstructors.set(CMD.CmdTypes.CLO, args => CMD.Clo(...args));
        this.cmdConstructors.set(CMD.CmdTypes.CRT, args => CMD.Crt(...args));
        this.cmdConstructors.set(CMD.CmdTypes.CRN, args => CMD.Crn(...args));
        this.cmdConstructors.set(CMD.CmdTypes.QRF, args => CMD.Qrf(...args));
        this.cmdConstructors.set(CMD.CmdTypes.CPR, args => CMD.Cpr(...args));
        this.cmdConstructors.set(CMD.CmdTypes.MRG, args => CMD.Mrg(...args));
        this.cmdConstructors.set(CMD.CmdTypes.HEL, args => CMD.Hel(...args));
        this.cmdConstructors.set(CMD.CmdTypes.GBY, args => CMD.Gby(...args));
        this.cmdConstructors.set(CMD.CmdTypes.SES, args => CMD.Ses(...args));
        this.cmdConstructors.set(CMD.CmdTypes.GMM, args => CMD.Gmm());
        this.cmdConstructors.set(CMD.CmdTypes.RMM, args => CMD.Rmm(...args));
        this.cmdConstructors.set(CMD.CmdTypes.UMM, args => CMD.Umm(...args));
        this.cmdConstructors.set(CMD.CmdTypes.STS, args => CMD.Sts());
        this.cmdConstructors.set(CMD.CmdTypes.CHG, args => CMD.Chg(...args));
        this.cmdConstructors.set(CMD.CmdTypes.OBS, args => CMD.Obs(...args));
        this.cmdConstructors.set(CMD.CmdTypes.UBS, args => CMD.Ubs(...args));
        this.cmdConstructors.set(CMD.CmdTypes.GAA, args => CMD.Gaa(...args));
        this.cmdConstructors.set(CMD.CmdTypes.CAL, args => CMD.Cal(...args));
        this.cmdConstructors.set(CMD.CmdTypes.ASC, args => CMD.Asc(...args));
        this.cmdConstructors.set(CMD.CmdTypes.ABC, args => CMD.Abc(...args));
        this.cmdConstructors.set(CMD.CmdTypes.CST, args => DoNothing());
        this.cmdConstructors.set(CMD.CmdTypes.CMP, args => CMD.Cmp());
        this.cmdConstructors.set(CMD.CmdTypes.MUT, args => CMD.Mut());
        this.cmdConstructors.set(CMD.CmdTypes.UMT, args => CMD.Umt());

        this.qryConstructors = new Map();
        this.qryConstructors.set(QRY.QrySegTypes.OBJ, args => QRY.Obj(...args));
        this.qryConstructors.set(QRY.QrySegTypes.HIS, args => QRY.His(...args));
        this.qryConstructors.set(QRY.QrySegTypes.PTH, args => QRY.Pth(...args));
        this.qryConstructors.set(QRY.QrySegTypes.CLS, args => QRY.Cls(...args));
        this.qryConstructors.set(QRY.QrySegTypes.INO, args => QRY.Ino(...args));
        this.qryConstructors.set(QRY.QrySegTypes.MET, args => QRY.Met(args[0], args.slice(1)));
        this.qryConstructors.set(QRY.QrySegTypes.NOT, args => QRY.Not());
        this.qryConstructors.set(QRY.QrySegTypes.TRY, args => QRY.Try(args[0],args[1]));
        this.qryConstructors.set(QRY.QrySegTypes.IDX, args => QRY.Idx(args));
        this.qryConstructors.set(QRY.QrySegTypes.ARR, args => QRY.Arr(args));
        this.qryConstructors.set(QRY.QrySegTypes.ZIP, args => QRY.Zip(args));
        this.qryConstructors.set(QRY.QrySegTypes.QRY, args => args.length ? args : QRY.Qry());
        this.qryConstructors.set(QRY.QrySegTypes.ANY, args => QRY.Any(...args));
        this.qryConstructors.set(QRY.QrySegTypes.ALL, args => QRY.All(...args));
        this.qryConstructors.set(QRY.QrySegTypes.EQU, args => QRY.Equ(...args));
        this.qryConstructors.set(QRY.QrySegTypes.EQA, args => QRY.Eqa(args));
        this.qryConstructors.set(QRY.QrySegTypes.NEQ, args => QRY.Neq(...args));
        this.qryConstructors.set(QRY.QrySegTypes.LES, args => QRY.Les(...args));
        this.qryConstructors.set(QRY.QrySegTypes.GRE, args => QRY.Gre(...args));
        this.qryConstructors.set(QRY.QrySegTypes.RGX, args => QRY.Rgx(...args));

        this.combinedConstructors = new Map([...this.cmdConstructors, ...this.qryConstructors]);

        // pool all segments symbols for code segmentation
        this.cmdAndQryRepresentation = new Array(...GetDictionaryValues(QRY.QRY_SYMBOLS), ...Object.keys(CMD.CmdTypes), ...[")","]","}"]);

    };

    /*
    *   GENERAL METHODS
    * */
    TextSerializer.prototype.EnableDebugging = function(){
        this._debugMode=True;
    };

    TextSerializer.prototype.DisableDebugging = function(){
        this._debugMode=False;
    };

    /*
    *   JS2TXT METHODS
    * */

    TextSerializer.prototype = Object.create(eoq2.serialization.Serializer.prototype);

    TextSerializer.prototype._IsNumerical = function(str) {
        for(let i=0;i<str.length;i++) {
            let c = str[i];
            if(!["0","1","2","3","4","5","6","7","8","9","-","+","E","e","."].includes(c)) {
                return false
            }
        }
        return true;
    };

    TextSerializer.prototype._IsNone = function(str) {
        return (str == '%');
    };

    TextSerializer.prototype._ContainsForbiddenCharacter = function(str) {
        if(str.match(/\s/)){
            return true;
        }
        return false;
    };

    TextSerializer.prototype._StringTranslator = function(str) {
        let idx = 0;
        while (idx < str.length){
            let a = str.slice(idx,idx+3).toUpperCase();
            if (this._IsCmdOrQry(str[idx]) || this._IsCmdOrQry(str.slice(idx,idx+3).toUpperCase()) || this._IsCmdOrQry(str.slice(idx,idx+4).toUpperCase()) 
                || this._ContainsForbiddenCharacter(str)) {
                return "'"+str+"'";
            }
            idx++;
        }
        return str;
    };

    TextSerializer.prototype._ArrayTranslator = function(o) {
        if(o == null) {
            return "%";
        } else if(Array.isArray(o)) {
            if (o.length>1){
                return "("+o.map(x => this.Ser(x)).join(",")+")";
            }else if (o.length === 1){
                return "("+this.Ser(o[0])+",)";
            }else{
                return "()";
            }
        }
    };

    TextSerializer.prototype.Ser = function(val) {
        let res = ''
        try {
            res = this.cmdTranslator(val);
        } catch {
            try {
                res = this.resTranslator(val);
            } catch {
                try { 
                    res = this.qryTranslators.get(val.qry)(val);
                } catch {
                    try {
                        res = this.priTranslators.get(typeof val)(val);
                    } catch {
                        throw new Error("Text serializer failed for "+val.toString());
                    }
                }
            }
        }
        return res;
    };

    /*
    *   TXT2JS METHODS
    * */

    // _IsCmd
    TextSerializer.prototype._IsCmd = function(segment) {
        return Object.keys(CMD.CmdTypes).includes(segment);
    };

    // _IsQry
    TextSerializer.prototype._IsQry = function(segment) {
        return GetDictionaryValues(QRY.QRY_SYMBOLS).includes(segment);
    };

    // _IsCmdOrQry
    TextSerializer.prototype._IsCmdOrQry = function(segment) {
        return (this._IsCmd(segment) || this._IsQry(segment));
    };

    // _IsStarterSymbol
    TextSerializer.prototype._IsStarterSymbol = function(segment) {
        return ["(","[","{"].includes(segment);
    };

    // _IsStopperSymbol
    TextSerializer.prototype._IsStopperSymbol = function(segment) {
        return [")","]","}"].includes(segment);
    };

    // _IsQryStart
    TextSerializer.prototype._IsQryStart = function(segment) {
        return (segment === "(");
    };

    // _IsQryEnd
    TextSerializer.prototype._IsQryEnd = function(segment) {
        return (segment === ")");
    };

    // _ShrinkWhitespace
    TextSerializer.prototype._ShrinkWhitespace = function(segments) {
        let _segments = [];
        for(let idx in segments){
            seg = segments[idx];
            if (!(seg === _segments[_segments.length-1] && seg === " ")){
                _segments.push(seg)
            }
        }
        return _segments;
    };

    // _UnwrapSingleItemList
    TextSerializer.prototype._UnwrapSingleItemArrays = function(arr) {
        /*
            Flattens single item arrays in arrays. I. e.
            [1,2,[3]] -> [1,2,3]
            [1,2,[3,4]] -> [1,2,[3,4]]
            This makes the parser more robust to unnecessary query parentheses!
        */
        if(Array.isArray(arr)){
            if(arr.length === 1 && (arr[0] instanceof eoq2.query.Qry || Array.isArray(arr[0]))){
                return this._UnwrapSingleItemArrays(arr[0]);
            }else{
                let subarr = [];
                for(let idx in arr){
                    subarr.push(this._UnwrapSingleItemArrays(arr[idx]));
                }
                return subarr;
            }
        }else{
            return arr;
        }
    };

    // _Unwrap
    TextSerializer.prototype._Unwrap = function(arr){
        /*
        * Avoids flattening of a top level single item array
        * */
        arr = this._UnwrapSingleItemArrays(arr);
        if (Array.isArray(arr)){
            return arr;
        }else{
            return [arr];
        }
    };

    // _IsQryDivider
    TextSerializer.prototype._IsQryDivider = function(segment) {
        return segment === QRY_ARG_DIVIDER;
    };

    // _IsCmdDivider
    TextSerializer.prototype._IsCmdDivider = function(segment) {
        return segment === CMD_ARG_DIVIDER;
    };

    // _IsDivider
    TextSerializer.prototype._IsDivider = function(segment) {
        return (this._IsQryDivider(segment) || this._IsCmdDivider(segment));
    };

    // _IsArgument
    TextSerializer.prototype._IsArgument = function(segment) {
        return !(this._IsCmdOrQry(segment) || this._IsDivider(segment) || this._IsStopperSymbol(segment));
    };

    TextSerializer.prototype._HandlePrimitives = function (code){
        /* convert string to primitive data type
         * using the first character to decide
         */
        let val;
        let c = code[0]; //first character
        let c2 = code[code.length-1]; //last character
        if (c==="\'" && c2==="\'"){
            // quoted string
            val = code.substring(1,code.length-1);
        }else if(this._IsNone(code)){
            val = null;
        }else if(this._IsNumerical(code)){
            // number
            if(code.includes('.')) { //float
                val = parseFloat(code);
            } else if(code.includes('E')) { //engineering float
                val = parseFloat(code)
            } else { //int
                val = parseInt(code);
            }
        }else if(code.toLowerCase() === "true"){
            val = true;
        }else if(code.toLowerCase() === "false"){
            val = false;
        }else{
            // unquoted string
            val = code;
        }
        return val;
    };

    // _GetSegments
    TextSerializer.prototype._GetSegments = function(code) {
      /*
      * GETSEGMENTS splits a textual EOQ expression string into its segments.
      * */
      let segments = [];
      let char_buffer = "";
      let idx = 0;
      let char = "";

      while (idx<code.length){
          // get current char
          char = code[idx];
          // get words in quotations
          if (["\"","\'"].includes(char)) {
              if (char_buffer) {
                  segments.push(char_buffer);
                  char_buffer = "";
              }
              let n = 1;
              while (code[idx+n] != char) {
                  n += 1;
              }
              segments.push("\'"+code.slice(idx + 1,idx + n)+"\'");
              idx += n;
          // get single qrys or ws
          }else if (this.cmdAndQryRepresentation.includes(char) || this._IsDivider(char)) {
              if (char_buffer) {
                  segments.push(char_buffer);
                  char_buffer = "";
              }
              segments.push(char);
          // get 3-char qrys or cmds
          }else if (this.cmdAndQryRepresentation.includes(code.slice(idx,idx+3).toUpperCase())) {
              if (char_buffer) {
                  segments.push(char_buffer);
                  char_buffer = "";
              }
              segments.push(code.slice(idx,idx+3).toUpperCase());
              idx += 2;
          // get &-codes
          }else if (char === "&") {
              if (char_buffer) {
                  segments.push(char_buffer);
                  char_buffer = "";
              }
              segments.push(QRY.QRY_SYMBOLS[code.slice(idx+1,idx+4).toUpperCase()]);
              idx += 3;
          // fill char buffer otherwise
          }else{
              char_buffer += char;
          }
          idx += 1;
      }
      // final char buffer push
      if (char_buffer) {
          segments.push(char_buffer);
      }
      // delete multiple consecutive whitespaces
      return this._ShrinkWhitespace(segments);
    };

    // _GetBoundConstructor
    TextSerializer.prototype._GetBoundConstructor = function(cmd, obj) {
        // check if cmd takes list input
        let takesList = QRY_CMDS_W_LIST_INPUT.includes(QRY.QRY_SYMBOLS[cmd]);
        let takesSingleOrList = QRY_CMDS_W_SINGLE_OR_LIST_INPUT.includes(QRY.QRY_SYMBOLS[cmd]);
        let takesMix = QRY_CMDS_W_MIXED_INPUT.includes(QRY.QRY_SYMBOLS[cmd]);

        // convert string to fit method names, i.e. GET -> Get
        let k = cmd[0].toUpperCase() + cmd.slice(1).toLowerCase();

        // break if non-chainable
        if (!(Object.keys(obj.__proto__.__proto__).includes(k))){ /*should work similar to obj.hasOwnProperty(cmd)*/
            throw new Error("Object has no bound method "+k+"!");
        }

        // construct function
        let func;
        if (takesList) {
            func = args => obj[k](args);
        }else if (takesMix) {
            func = args => obj[k](args[0], args.slice(1));
        }else if (takesSingleOrList){
            func = function (args) {
                if (args.length>1){
                    return obj[k](args);
                }else{
                    return obj[k](args[0]);
                }
            }
        }else{
            func = args => obj[k](...args);
        }

        return func;
    };

    // _GetBaseConstructor
    TextSerializer.prototype._GetBaseConstructor = function(cmd) {
        //return this.combinedConstructors.get(cmd);

        let k = cmd.toUpperCase();
        
        // check if cmd takes list input
        let takesList = QRY_CMDS_W_LIST_INPUT.includes(QRY.QRY_SYMBOLS[k]);
        let takesSingleOrList = QRY_CMDS_W_SINGLE_OR_LIST_INPUT.includes(QRY.QRY_SYMBOLS[k]);
        let takesMix = QRY_CMDS_W_MIXED_INPUT.includes(QRY.QRY_SYMBOLS[k]);

        //construct function
        let constructor = this.combinedConstructors.get(k);

        let func;
        if (takesList) {
            func = args => constructor(args);
        }else if (takesMix) {
            func = args => constructor(args);
        }else if (takesSingleOrList){
            func = function (args) {
                if (args.length>1){
                    return constructor(args);
                }else{
                    return constructor(args[0]);
                }
            }
        }else{
            func = args => constructor(args);
        }

        return func;
    };

    // _ConvertSegmentToFunction
    TextSerializer.prototype._ConvertSegmentToFunction = function(seg, res) {
        /*
        *   Converts segment symbol to function if possible. I.e. "!" -> Cls()
        * */
        if (this._IsCmdOrQry(seg)) {
            if (this._IsQry(seg)){
                seg = SYMBOLS_2_QRY_DICT[seg];
            }
            let cmd = seg;
            let isBoundCmd;
            let func;
            try {
                func = this._GetBoundConstructor(cmd, res[res.length-1]);
                isBoundCmd = true;
            } catch {
                func = this._GetBaseConstructor(cmd);
                isBoundCmd = false;
            }
            return [func, isBoundCmd];
        }else{
            throw new Error("Segment "+seg+" is not convertible to a JSEOQ function!")
        }
    };

    // _BalanceSteps
    // TextSerializer.prototype._BalanceSteps = function(parsingList){
    //     /*
    //     *   Closes unclosed step_in parsing cmds
    //     * */
    //     let toClose = 0;
    //     let seg;
    //     for (let idx in parsingList) {
    //         seg = parsingList[idx];
    //         if (seg === PARSING_CMDS.STEP_IN) {
    //             toClose += 1;
    //         }else if (seg === PARSING_CMDS.STEP_OUT) {
    //             toClose -= 1;
    //         }
    //     }
    //     for (let closing in Array(toClose)) {
    //         parsingList.push(PARSING_CMDS.STEP_OUT);
    //     }
    //     return parsingList;
    // };

    // _StripOuterQuotations
    TextSerializer.prototype._StripOuterQuotations = function(code) {
        return code.replace(/^'+|'+$/g, '');
    };

    // _StripOuterWhitespace
    TextSerializer.prototype._StripOuterWhitespace = function(code) {
        return code.trim();
    };

    // _SeparateCodes
    TextSerializer.prototype._SeparateCodes = function(code){
        let codes = code;
        // split codes
        for (let idx = 0; idx<EXPRESSION_DIVIDERS.length-1; idx++){
            codes = codes.split(EXPRESSION_DIVIDERS[idx]).join(EXPRESSION_DIVIDERS[idx+1]);
        }
        codes = codes.split(EXPRESSION_DIVIDERS[EXPRESSION_DIVIDERS.length-1]);
        // strip ws
        let cleaned_codes = [];
        for (let idx in codes) {
            if (codes[idx]){
                cleaned_codes.push(this._StripOuterWhitespace(codes[idx]))
            }
        }
        return cleaned_codes;
    };

    // _GetParsingList
    TextSerializer.prototype._GetParsingList = function(segments){
        /*
        *   Creates Array of segments and parsing commands.
        *   Contains the main logic to identify EOQ syntax.
        * */
        // init array for the result
        let parsingList = [];

        // init buffer & control variables
        let lastSeg = null;
        let nextSeg = null;
        let seg;
        let cmdDividerSeen = false;
        let stepInSinceCmdDivider = 0; // flat counter, keeps track of stepins since cmd divider
        let stepInSinceQryStart = []; // list counter, keeps track of stepins since subqry start
        let expectedStoppingSymbols = []; // keeps track of expected symbols to end subqry

        // variables for error handling
        let segmentsCopy = JSON.parse(JSON.stringify(segments)); // creating a deep copy

        while(segments.length){
            seg = segments.shift();
            nextSeg = segments? segments[0] : null;

            if (this._IsStarterSymbol(seg)){
                if (this._IsArgument(lastSeg)){
                    parsingList.push(PARSING_CMDS.STEP_OUT);
                    if (stepInSinceQryStart.length){
                        stepInSinceQryStart[stepInSinceQryStart.length-1] = Math.max(
                            stepInSinceQryStart[stepInSinceQryStart.length-1]-1,0);
                    }else if (stepInSinceCmdDivider) {
                        stepInSinceCmdDivider = Math.max(stepInSinceCmdDivider-1,0);
                    }
                }
                // keep track of subqueries
                stepInSinceQryStart.push(1);
                expectedStoppingSymbols.push(STOPPING_SYMBOL_DICT[seg]);
                // handle difference between argument2subqry and cmd2subqry by shifting the expected stepout
                if (this._IsCmdOrQry(lastSeg) && !this._IsStarterSymbol(lastSeg)){
                    try {
                        stepInSinceQryStart[stepInSinceQryStart.length-1] += 1
                        stepInSinceQryStart[stepInSinceQryStart.length-2] -= 1
                    }catch{
                        // pass
                    }
                }
                // construct parsing list
                parsingList.push(seg);
                parsingList.push(PARSING_CMDS.STEP_IN);

            }else if (this._IsCmdOrQry(seg)){
                if (parsingList.length
                    && !this._IsDivider(lastSeg)
                    && !this._IsStarterSymbol(lastSeg)
                    && !this._IsStopperSymbol(lastSeg)){
                    // stepout rule for chained cmds and qrys
                    // is disabled on first cmd (therefore "if parsingList")
                    parsingList.push(PARSING_CMDS.STEP_OUT);
                    if (stepInSinceQryStart.length){
                        stepInSinceQryStart[stepInSinceQryStart.length-1] = Math.max(
                            stepInSinceQryStart[stepInSinceQryStart.length-1]-1,0);
                    }else if (stepInSinceCmdDivider) {
                        stepInSinceCmdDivider = Math.max(stepInSinceCmdDivider-1,0);
                    }
                }

                if (this._IsCmdDivider(lastSeg) && this._IsCmd(seg)){
                    // stepout rule for divided base cmds
                    parsingList.push(PARSING_CMDS.STEP_OUT);
                    stepInSinceCmdDivider = Math.max(stepInSinceCmdDivider-1,0);
                }

                // construct parsing list
                parsingList.push(seg);
                parsingList.push(PARSING_CMDS.STEP_IN);

                if (this._IsCmd(seg)){
                    // reset cmd divider flag to disable step balancing when first divider is seen
                    cmdDividerSeen = false;
                }

                if (stepInSinceQryStart.length){
                    // count step ins within subqry
                    stepInSinceQryStart[stepInSinceQryStart.length-1] += 1;
                }else if (cmdDividerSeen){
                    // count step ins within separated cmd args
                    stepInSinceCmdDivider += 1;
                }

            }else if (this._IsCmdDivider(seg)){
                if (!cmdDividerSeen){
                    cmdDividerSeen = true;
                } else {
                    while (cmdDividerSeen && stepInSinceCmdDivider){
                        // balancing step outs
                        parsingList.push(PARSING_CMDS.STEP_OUT);
                        stepInSinceCmdDivider -= 1;
                    }
                    parsingList.push(seg)
                }

            // }else if (this._IsQryDivider(seg)){
            //     if (stepInSinceQryStart.length){
            //         // reset step-ins since subqry to 1 if qry divider met
            //         let stepIns = stepInSinceQryStart.pop();
            //         while (stepIns - 1){
            //             parsingList.push(PARSING_CMDS.STEP_OUT);
            //             stepIns -= 1;
            //         }
            //         stepInSinceQryStart.push(1);
            //         parsingList.push(seg);
            //     }

            }else if (this._IsStopperSymbol(seg)){
                if (!expectedStoppingSymbols.length){
                    // found stopping symbol without corresponding start symbol
                    let faultyIdx = segmentsCopy.length - segments.length;
                    let errorMsg = "Solving of code failed at segment "+ faultyIdx.toString() + "\n";
                    errorMsg += "Unexpected stopping symbol " + seg + "\n";
                    errorMsg += "..." + segmentsCopy.slice(faultyIdx-ERROR_MSG_VIEW_DISTANCE,faultyIdx).join(",");
                    errorMsg += "-->" + segmentsCopy[faultyIdx] + "<--";
                    errorMsg += segmentsCopy.slice(faultyIdx+1,faultyIdx+1+ERROR_MSG_VIEW_DISTANCE).join(",") + "...\n";
                    throw new Error(errorMsg);
                } else if (seg === expectedStoppingSymbols[expectedStoppingSymbols.length-1]) {
                    // correct stopping symbol found
                    if (stepInSinceQryStart){
                        let stepIns = stepInSinceQryStart.pop();
                        while (stepIns) {
                            parsingList.push(PARSING_CMDS.STEP_OUT);
                            stepIns -= 1;
                        }
                    }
                    expectedStoppingSymbols.pop();
                } else {
                    // wrong stopping symbol
                    let faultyIdx = segmentsCopy.length - segments.length - 1;
                    let errorMsg = "Solving of code failed at segment "+ faultyIdx.toString() + "\n";
                    errorMsg += "Expected " + expectedStoppingSymbols[expectedStoppingSymbols.length-1];
                    errorMsg += ", got " + seg + "\n";
                    errorMsg += "..." + segmentsCopy.slice(faultyIdx-ERROR_MSG_VIEW_DISTANCE,faultyIdx).join(",");
                    errorMsg += "-->" + segmentsCopy[faultyIdx] + "<--";
                    errorMsg += segmentsCopy.slice(faultyIdx+1,faultyIdx+1+ERROR_MSG_VIEW_DISTANCE).join(",") + "...\n";
                    throw new Error(errorMsg);
                }

            }else{
                // add argument to parsing list
                parsingList.push(seg);
            }

            lastSeg = seg;

        }// end while

        if (expectedStoppingSymbols.length){
            // ended parsing list creation without closing all subqrys -> throw error
            let errorMsg = "Solving of code failed at end.\n";
            errorMsg += "Expected " + expectedStoppingSymbols[expectedStoppingSymbols.length-1];
            errorMsg += " but reached end of code!\n";
            throw new Error(errorMsg);
        }

        return parsingList;
    };

    // _SolveParsingList
    TextSerializer.prototype._SolveParsingList = function(parsingList){
        /*
        *   parses segments to actual constructors
        * */
        let res = []
        let cmd;
        let isBoundCmd=false;
        let seg = null;
        let debugCounter = [];
        let lastSeg;

        while (parsingList.length){
            lastSeg = seg;
            seg = parsingList.shift();

            if (this._IsCmdOrQry(seg)){
                if (this._debugMode){
                    debugCounter.push(seg);
                }
                if (this._IsQryDivider(lastSeg) || this._IsCmdDivider(lastSeg)){
                    [cmd, isBoundCmd] = this._ConvertSegmentToFunction(seg, null);
                }else{
                    [cmd, isBoundCmd] = this._ConvertSegmentToFunction(seg, res);
                }

            }else if (seg===PARSING_CMDS.STEP_IN){
                if (this._debugMode){
                    console.log("stepping in after "+(isBoundCmd?"bound ":"")+debugCounter[debugCounter.length-1]);
                }
                let res_ = this._SolveParsingList(parsingList);
                res_ = this._Unwrap(res_);
                if (res.length && isBoundCmd){
                    res[res.length-1] = cmd(res_);
                }else if (res.length){
                    res.push(cmd(res_));
                }else{
                    res = [cmd(res_)];
                }

            }else if (seg===PARSING_CMDS.STEP_OUT){
                if (this._debugMode){
                    console.log("stepping out, returning ["+res.join(",")+"]");
                }
                return res;
            }else if (!this._IsQryDivider(seg) && !this._IsCmdDivider(seg)){
                res.push(this._HandlePrimitives(seg));
            }
        }

        if (this._debugMode){
            console.log("stepping out, returning ["+res.join(",")+"]");
        }

        return res;
    };

    // _ConstructCompound
    TextSerializer.prototype._ConstructCompound = function(commandList){
        /*
        *   combines multiple cmds to a cmp object
        * */
        let res = new CMD.Cmp();
        let cmdLiteral;
        let func;
        let args;
        for (let idx in commandList) {
            let cmd = commandList[idx];
            try{
                res.a.push(cmd);
                // get bound cmd for cmp
                // cmdLiteral = cmd[0].cmd.toLowerCase();
                // cmdLiteral = cmdLiteral[0].toUpperCase() + cmdLiteral.slice(1);
                // //func = res[cmdLiteral];
                // // get content
                // args = cmd[0].a;
                // if (!Array.isArray(args)){
                //     args = [args];
                // }
                // // construct
                // res = res[cmdLiteral](...args);
            }catch{
                let errorMsg = "Solving of code failed.\n";
                errorMsg += "Could non add command #" + (idx+1).toString() + " \'" + cmdLiteral + "\' to Compound.\n";
                throw new Error(errorMsg);
            }
        }
        return res;
    };

    TextSerializer.prototype.Des = function(code) {
        /*
        *   DES takes a textual representation EOQ code and constructs the cmd/qry chain
        * */
        let results = [];
        let codes = this._SeparateCodes(code);
        for (let idx in codes){
            code = codes[idx];
            // split code into segments
            let segments = this._GetSegments(code);
            // inject parsing cmds
            let parsingList = this._GetParsingList(segments);
            if (this._debugMode){
                console.log("PARSINGLIST: "+parsingList.join(","));
            }
            // deep copy parsing list for error handling
            let parsingListCopy = JSON.parse(JSON.stringify(parsingList));
            // solve
            try {
                let command = this._SolveParsingList(parsingList);
                results = results.concat(command);
            }catch(e) {
                // solving failed
                let faultyIdx = parsingListCopy.length - Math.max(1, parsingList.length);
                let errorMsg = "Solving of code failed at segment " + faultyIdx.toString() + "\n";
                errorMsg += "..." + parsingListCopy.slice(faultyIdx-ERROR_MSG_VIEW_DISTANCE,faultyIdx).join(",");
                errorMsg += "-->" + parsingListCopy[faultyIdx] + "<--";
                errorMsg += parsingListCopy.slice(faultyIdx+1,faultyIdx+1+ERROR_MSG_VIEW_DISTANCE).join(",") + "...\n";
                errorMsg += "<pre>"+e.toString()+"</pre>";
                errorMsg += "<pre>"+e.stack.toString()+"</pre>";
                throw new Error(errorMsg);
            }
        }

        if (results.length === 1){
            return results[0];
        }else{
            return this._ConstructCompound(results);
        }
    };

    return {
        TextSerializer : TextSerializer
    };
})());