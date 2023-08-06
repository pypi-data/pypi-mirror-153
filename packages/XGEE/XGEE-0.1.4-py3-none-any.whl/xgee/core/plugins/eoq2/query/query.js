/*
*
* 2019 Bjoern Annighoefer
*/

var eoq2 = eoq2 || {};
eoq2.query = eoq2.query || {};

Object.assign(eoq2.query,(function() {

    var QrySegTypes = {
        OBJ : 'OBJ' , //object reference
        HIS : 'HIS' , //history reference
    
        // Left only element-wise operations
        PTH : 'PTH' , // path
        CLS : 'CLS' , // class
        INO : 'INO', // is instance of 
        MET : 'MET' , //meta
        NOT : 'NOT', //Boolean not
        TRM : 'TRM', //terminate
        CNS : 'CNS', //Constraint of
        TRY : 'TRY', //try
        
        // Left only list-of-elements-wise operations
        IDX : 'IDX' , //index
        SEL : 'SEL' , // selector
        ARR : 'ARR' , // outer array
        ZIP : 'ZIP' , // inner array creation
        QRY : 'QRY' , // cmd

        ANY : 'ANY', //At least one element from the right is found in the left --> Bool
        ALL : 'ALL', //All elements from the right are found in the left --> Bool
        
        // Left-vs-right element-wise operators
        //DEP : '!' , // depth
        EQU : 'EQU' , //equal
        EQA : 'EQA' , //equal any of the right elements
        NEQ : 'NEQ' , //not equal
        LES : 'LES' , // less
        GRE : 'GRE' , // greater
        RGX : 'RGX' , // regex (string only)

        ADD : 'ADD' , //OR, addition, ?union?
        SUB : 'SUB' , //XOR, substraction, ?substract?
        MUL : 'MUL' , //AND, multiply, ?cross product?
        DIV : 'DIV' , //NAND, divided, ?intersection?

        // logic operator synonyms
        ORR : 'ORR' , //OR synonym
        XOR : 'XOR' , //XOR synonym
        AND : 'AND' , //AND synonym
        NAD : 'NAD' , //NAND synonym
        
        //Left-vs-right list-of-element-wise operators
        CSP : 'CSP' , //cross product
        ITS : 'ITS' , //intersection
        DIF : 'DIF' , //set subtraction / relative complement
        UNI : 'UNI' , //union
        CON : 'CON'  //concut
    };

    //define a list of symbols for the textual representation
   var QRY_SYMBOLS = {
       'OBJ' : '#',
       'HIS' : '$',
       'PTH' : '/',
       'CLS' : '!',
       'INO' : '?',
       'MET' : '@',
       'NOT' : '&NOT',
	   'CNS' : '&CNS',
       'TRM' : '&TRM',
       'TRY' : '&TRY',
       'IDX' : ':',
       'SEL' : '{',
       'ARR' : '[',
       'ZIP' : '&ZIP',
       'QRY' : '(',
       'ANY' : '&ANY',
       'ALL' : '&ALL',
       'EQU' : '=',
       'EQA' : '&EQA',
       'NEQ' : '~',
       'LES' : '<',
       'GRE' : '>',
       'RGX' : '&RGX',
       'ADD' : '&ADD',
       'SUB' : '&SUB',
       'MUL' : '&MUL',
       'DIV' : '&DIV',
       'ORR' : '&ORR',
       'XOR' : '&XOR',
       'AND' : '&AND',
       'NAD' : '&NAD',
       'CSP' : '&CSP',
       'ITS' : '^',
       'DIF' : '\\',
       'UNI' : '_',
       'CON' : '|'
   };

    var QryMetaSegTypes  = {
        CLS : 'CLASS' , //class
        CLN : 'CLASSNAME' , //class name
        PAR : 'CONTAINER' , //parent (container)
        PAR : 'PARENT', //parent (container)
        ALP : 'ALLPARENTS', //parent (container)
        ASO : 'ASSOCIATES', //ASSOCIATES(start=root) all elements refering to this one beginning at start. default is root
        IDX : 'INDEX' , //parent (container)
        FEA : 'FEATURES' , //all features
        FEV : 'FEATUREVALUES' , //all feature values
        FEN : 'FEATURENAMES' , //all feature names
        ATT : 'ATTRIBUTES' , //all attribute features
        ATN : 'ATTRIBUTENAMES' , //all attribute feature names
        ATV : 'ATTRIBUTEVALUES' , //all attribute feature values
        REF : 'REFERENCES' , //all reference features    
        REN : 'REFERENCENAMES' , //all reference feature names
        REV : 'REFERENCEVALUES' , //all reference feature values
        CNT : 'CONTAINMENTS' , //all containment features
        CNV : 'CONTAINMENTVALUES' , //all containment feature values
        CNN : 'CONTAINMENTNAMES' , //all containment feature names

        //class operators
        PAC : 'PACKAGE', //class
        STY : 'SUPERTYPES', //directly inherited classes
        ALS : 'ALLSUPERTYPES', //all and also indirectly inherited classes
        IMP : 'IMPLEMENTERS', //all direct implementers of a class
        ALI : 'ALLIMPLEMENTERS', //all and also indirect implementers of a class  
        MMO : 'METAMODELS', //retrieve all metamodels
        
        //Control flow operators 
        IFF : 'IF', //if(condition,then,else);  #DEPRICATED
        TRY : 'TRY', //catch errors and return a default #NOT IMPLEMENTED

        //list operators
        LEN : 'SIZE' , //size of a list
        ASC : 'SORTASC' , //sort ascending
        ASC : 'SORTDSC' , //sort descending

        //recursive operation
        REC : 'REPEAT', //REPEAT(<query>,depth) repeate a given query until no more results are found

        //structure operators
        FTT : 'FLATTEN' , //flatten any sub list structure 
    };

    var QryIdxTypes = {
        //structure operators
        FLT : 'FLATTEN' , //flatten any sub list structure to a list #NOT IMPLEMENTED
        LEN : 'SIZE' , //size of a list
        ASC : 'SORTASC' , //sort ascending #NOT IMPLEMENTED
        DSC : 'SORTDSC' , //sort descending #NOT IMPLEMENTED
    };

    function Seg(stype,args) {
        this.qry = stype
        this.v = args
    };
        
    Seg.prototype.toString = function() {
        return QRY_SYMBOLS[this.qry]+(this.v==null?'':this.v.toString());
    };
        
    function PthSeg(name) {
        Seg.call(this,QrySegTypes.PTH,name);
    };
    PthSeg.prototype = Object.create(Seg.prototype);
            
    function SelSeg(query) {
        Seg.call(this,QrySegTypes.SEL,query);
    };
    SelSeg.prototype = Object.create(Seg.prototype);
            
    SelSeg.prototype.toString = function() {
            return '{'+this.v.toString()+'}';
    };
        
    function ArrSeg(query) {
        Seg.call(this,QrySegTypes.ARR,query)
    };
    ArrSeg.prototype = Object.create(Seg.prototype);
            
    ArrSeg.prototype.toString = function() {
        return '['+this.v.toString()+']';
    };
        
    function ObjSeg(obj) {
        Seg.call(this,QrySegTypes.OBJ,obj);
    };
    
    ObjSeg.prototype = Object.create(Seg.prototype);
            
         
    /*
    * Qry - the main object to create any kind of complex queries by concatenation
    /*/
    function Qry(root=null) {
            if(root) {
                Seg.call(this,QrySegTypes.QRY, [root]);
            } else {
                Seg.call(this,QrySegTypes.QRY, []);
            }
    }; 

    Qry.prototype = Object.create(Seg.prototype);

    Qry.prototype.toString = function() {
        let queryStr = '';
        for(let i=0;i<this.v.length;i++) {
            let seg = this.v[i];
            queryStr += seg.toString();
        }
        return '('+queryStr+')';
    };
    
    Qry.prototype.Obj = function(v) {
        this.v.push(new ObjSeg(v))
        return this;
    };

    Qry.prototype.His = function(v) {
        this.v.push(new Seg(QrySegTypes.HIS,v))
        return this;
    };
        
    Qry.prototype.Pth = function(name) {
        this.v.push(new PthSeg(name));
        return this;
    };
        
    Qry.prototype.Cls = function(name) {
        this.v.push(new Seg(QrySegTypes.CLS,name));
        return this;
    };

    Qry.prototype.Ino = function(name) {
        this.v.push(new Seg(QrySegTypes.INO,name));
        return this;
    };

    Qry.prototype.Met = function(name,args=[]) {
        this.v.push(new Seg(QrySegTypes.MET,[name].concat(args)));
        return this;
    };

    Qry.prototype.Not = function() {
        this.v.push(new Seg(QrySegTypes.NOT,null));
        return this;
    };

    Qry.prototype.Trm = function(condition=null,def=null) {
        this.v.push(new Seg(QrySegTypes.TRM,[condition,def]));
        return this;
    };

    Qry.prototype.Cns = function() {
        this.v.push(new Seg(QrySegTypes.CNS,null));
		return this;
    };

    Qry.prototype.Try = function(query,def=null) {
        this.v.push(new Seg(QrySegTypes.TRY,[query,def]));
        return this;
    };

    Qry.prototype.Idx = function(name) {
        this.v.push(new Seg(QrySegTypes.IDX,name));
        return this;
    };

    Qry.prototype.Sel = function(query) {
        this.v.push(new SelSeg(query));
        return this;
    };

    Qry.prototype.Arr = function(elements) {
        this.v.push(new ArrSeg(elements));
        return this;
    };

    Qry.prototype.Zip = function(elements) {
        this.v.push(new Seg(QrySegTypes.ZIP,elements));
        return this;
    };

    Qry.prototype.Any = function(query) {
        this.v.push(new Seg(QrySegTypes.ANY,query));
        return this;
    };

    Qry.prototype.All = function(query) {
        this.v.push(new Seg(QrySegTypes.ALL,query));
        return this;
    };

    Qry.prototype.Equ = function(query) {
        this.v.push(new Seg(QrySegTypes.EQU,query));
        return this;
    };

    Qry.prototype.Eqa = function(query) {
        this.v.push(new Seg(QrySegTypes.EQA,query));
        return this;
    };

    Qry.prototype.Neq = function(query) {
        this.v.push(new Seg(QrySegTypes.NEQ,query));
        return this;
    };

    Qry.prototype.Les = function(query) {
        this.v.push(new Seg(QrySegTypes.LES,query));
        return this;
    };

    Qry.prototype.Gre = function(query) {
        this.v.push(new Seg(QrySegTypes.GRE,query));
        return this;
    };

    Qry.prototype.Rgx = function(query) {
        this.v.push(new Seg(QrySegTypes.RGX,query));
        return this;
    };

    Qry.prototype.Add = function(query) {
        this.v.push(new Seg(QrySegTypes.ADD,query));
        return this;
    };

    Qry.prototype.Sub = function(query) {
        this.v.push(new Seg(QrySegTypes.SUB,query));
        return this;
    };

    Qry.prototype.Mul = function(query) {
        this.v.push(new Seg(QrySegTypes.MUL,query));
        return this;
    };

    Qry.prototype.Div = function(query) {
        this.v.push(new Seg(QrySegTypes.DIV,query));
        return this;
    };

    Qry.prototype.Orr = function(query) {
        this.v.push(new Seg(QrySegTypes.ORR,query));
        return this;
    };

    Qry.prototype.Xor = function(query) {
        this.v.push(new Seg(QrySegTypes.XOR,query));
        return this;
    };

    Qry.prototype.And = function(query) {
        this.v.push(new Seg(QrySegTypes.AND,query));
        return this;
    };

    Qry.prototype.Nad = function(query) {
        this.v.push(new Seg(QrySegTypes.NAD,query));
        return this;
    };

    Qry.prototype.Csp = function(query) {
        this.v.push(new Seg(QrySegTypes.CSP,query));
        return this;
    };

    Qry.prototype.Its = function(query) {
        this.v.push(new Seg(QrySegTypes.ITS,query));
        return this;
    };

    Qry.prototype.Dif = function(query) {
        this.v.push(new Seg(QrySegTypes.DIF,query));
        return this;
    };

    Qry.prototype.Uni = function(query) {
        this.v.push(new Seg(QrySegTypes.UNI,query));
        return this;
    };

    Qry.prototype.Con = function(query) {
        this.v.push(new Seg(QrySegTypes.CON,query));
        return this;
    };

    function Obj(v) {
        Qry.call(this);
        this.Obj(v);
    };
    Obj.prototype = Object.create(Qry.prototype);

    function His(v) {
        Qry.call(this);
        this.His(v);
    };
    His.prototype = Object.create(Qry.prototype);

    function Pth(name) {
        Qry.call(this);
        this.Pth(name);
    };
    Pth.prototype = Object.create(Qry.prototype);

    function Cls(name) {
        Qry.call(this);
        this.Cls(name);
    };
    Cls.prototype = Object.create(Qry.prototype);

    function Ino(name) {
        Qry.call(this);
        this.Ino(name);
    };
    Ino.prototype = Object.create(Qry.prototype);

    function Try(query,def=null) {
        Qry.call(this);
        this.Try(query,def);
    };
    Try.prototype = Object.create(Qry.prototype);

    function Met(name,args=[]) {
        Qry.call(this);
        this.Met(name,args);
    };
    Met.prototype = Object.create(Qry.prototype);

    function Idx(n) {
        Qry.call(this);
        this.Idx(n);
    };
    Idx.prototype = Object.create(Qry.prototype);
        
    function Arr(elements) {
        Qry.call(this);
        this.Arr(elements);
    };
    Arr.prototype = Object.create(Qry.prototype);

    function Any(select) {
        Qry.call(this);
        this.Any(select);
    };
    Any.prototype = Object.create(Qry.prototype);

    function Equ(query) {
        Qry.call(this);
        this.Equ(query);
    };
    Equ.prototype = Object.create(Qry.prototype);

    function Eqa(query) {
        Qry.call(this);
        this.Eqa(query);
    };
    Eqa.prototype = Object.create(Qry.prototype);

    function Neq(query) {
        Qry.call(this);
        this.Neq(query);
    };
    Neq.prototype = Object.create(Qry.prototype);

    function Les(query) {
        Qry.call(this);
        this.Les(query);
    };
    Les.prototype = Object.create(Qry.prototype);

    function Gre(query) {
        Qry.call(this);
        this.Gre(query);
    };
    Gre.prototype = Object.create(Qry.prototype);

    function Rgx(query) {
        Qry.call(this);
        this.Rgx(query);
    };
    Rgx.prototype = Object.create(Qry.prototype);

    //Define the exported classes
    return {
        QrySegTypes : QrySegTypes,
        QRY_SYMBOLS : QRY_SYMBOLS,
        QryMetaSegTypes: QryMetaSegTypes,
        Seg : Seg,
        Qry : Qry,
        Obj : Obj,
        His : His,
        Pth : Pth,
        Cls : Cls,
        Ino : Ino,
        Try : Try,
        Met : Met,
        Idx : Idx,
        Arr : Arr,
        Any : Any,
        Equ : Equ,
        Eqa : Eqa,
        Neq : Neq,
        Les : Les,
        Gre : Gre,
        Rgx : Rgx
    };

})());

//make it available on the lowest level
Object.assign(eoq2,eoq2.query);