
/*
*
* 2019 Bjoern Annighoefer
*
* Modified 2020 Christian Mollière
*/

var eoq2 = eoq2 || {};

Object.assign(eoq2,(function() {

    var version = 229; //the central version

    //define singletons to create cmds and queries
    var CMD = {
        Get : function(target) {return new eoq2.command.Get(target)},
        Set : function(target,feature,value) {return new eoq2.command.Set(target,feature,value)},
        Add : function(target,feature,value) {return new eoq2.command.Add(target,feature,value)},
        Rem : function(target,feature,value) {return new eoq2.command.Rem(target,feature,value)},
        Mov : function(target,newIndex) {return new eoq2.command.Mov(target,newIndex)},
        Clo : function(target,mode) {return new eoq2.command.Clo(target,mode)},
        Crt : function(clazz,n,constructorArgs=[]) {return new eoq2.command.Crt(clazz,n,constructorArgs)},
        Crn : function(package,name,n,constructorArgs=[]) {return new eoq2.command.Crn(package,name,n,constructorArgs)},
        Qrf : function(target) {return new eoq2.command.Qrf(target)},
        Cpr : function(orig,changed,mode) {return new eoq2.command.Cpr(orig,changed,mode)},
        Mrg : function(orig,changed,mode) {return new eoq2.command.Mrg(orig,changed,mode)},
        Hel : function(user,password) {return new eoq2.command.Hel(user,password)},
        Ses : function(sessionId) {return new eoq2.command.Ses(sessionId)},
        Gby : function(sessionId) {return new eoq2.command.Gby(sessionId)},
        Sts : function() {return new eoq2.command.Sts()},
        Gmm : function() {return new eoq2.command.Gmm()},
        Rmm : function(metamodel) {return new eoq2.command.Rmm(metamodel)},
        Umm : function(metamodel) {return new eoq2.command.Umm(metamodel)},
        Obs : function(eventType,eventKey) {return new eoq2.command.Obs(eventType,eventKey)},
        Ubs : function(eventType,eventKey) {return new eoq2.command.Ubs(eventType,eventKey)},
        Chg : function(changeId,n) {return new eoq2.command.Chg(changeId,n)},
        Gaa : function() {return new eoq2.command.Gaa()},
        Cal : function(name,args=[],opts=[]) {return new eoq2.command.Cal(name,args,opts)},
        Asc : function(name,args=[],opts=[]) {return new eoq2.command.Asc(name,args,opts)},
        Abc : function(callId) {return new eoq2.command.Abc(callId)},
		Adc : function(constraintType,target,feature,law,name,annotation) {return new eoq2.command.Adc(constraintType,target,feature,law,name,annotation)},
		Gac : function() {return new eoq2.command.Gac()},
		Val : function() {return new eoq2.command.Val()},
		Rmc : function(target) {return new eoq2.command.Rmc(target)},
        Cmp : function() {return new eoq2.command.Cmp()},
        Mut : function() {return new eoq2.command.Mut()},
        Umt : function() {return new eoq2.command.Umt()},
        CloModes : eoq2.command.CloModes,
        CmdTypes : eoq2.command.CmdTypes
    };
	
    var QRY = {
        Qry : function(root=null) {return new eoq2.query.Qry(root)}, //depricated?
        Obj : function(v) {return new eoq2.query.Obj(v)},
        His : function(v) {return new eoq2.query.His(v)},
        Pth : function(name) {return new eoq2.query.Pth(name)},
        Cls : function(name) {return new eoq2.query.Cls(name)},
        Ino : function(name) {return new eoq2.query.Ino(name)},
        Met : function(name,args=[]) {return new eoq2.query.Met(name,args)},
        Not : function() {return new eoq2.query.Not()},
        Trm : function(condition=null,def=null) {return new eoq2.query.Trm(condition,def)},
        Cns : function() {return new eoq2.query.Cns()},
        Try : function(query,def=null) {return new eoq2.query.Try(query,def)},
        Idx : function(n) {return new eoq2.query.Idx(n)},
        Arr : function(elements) {return new eoq2.query.Arr(elements)},
        Any : function(select) {return new eoq2.query.Any(select)},
        All : function(select) {return new eoq2.query.All(select)},
        Equ : function(operator) {return new eoq2.query.Equ(operator)},
        Eqa : function(operator) {return new eoq2.query.Eqa(operator)},
        Neq : function(operator) {return new eoq2.query.Neq(operator)},
        Les : function(operator) {return new eoq2.query.Les(operator)},
        Gre : function(operator) {return new eoq2.query.Gre(operator)},
        Rgx : function(operator) {return new eoq2.query.Rgx(operator)},
        QrySegTypes : eoq2.query.QrySegTypes,
        QRY_SYMBOLS : eoq2.query.QRY_SYMBOLS,
        QryMetaSegTypes: eoq2.query.QryMetaSegTypes,
    };

    return {
        version : version,
        CMD : CMD,
        QRY : QRY
    }
})());

//export the singletons to the gobal namespace
CMD = eoq2.CMD;
QRY = eoq2.QRY;


