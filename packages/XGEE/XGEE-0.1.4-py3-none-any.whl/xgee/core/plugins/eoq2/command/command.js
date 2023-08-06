/*
*
* 2019 Bjoern Annighoefer
*
* Modified 2020 Christian Mollière
*/

var eoq2 = eoq2 || {};
eoq2.command = eoq2.command || {};


Object.assign(eoq2.command,(function(){

    let CmdTypes = {
        //data related commmands
        GET  : 'GET' , //get cmd
        SET  : 'SET' , //set cmd value
        ADD  : 'ADD' , //add cmd value
        REM  : 'REM' , //remove cmd value
        MOV  : 'MOV' , //move cmd cmd
        CLO  : 'CLO' , //clone source target mode
        DEL  : 'DEL' , //delete cmd
        CRT  : 'CRT' , //create
        CRN  : 'CRN' , //create by name
        QRF  : 'QRF' , //querify
		ADC  : 'ADC' , //add constraint
		GAC  : 'GAC' , //get constraint
		VAL  : 'VAL' , //validate constraint
		RMC  : 'RMC' , //remove constraint

        //comparison and merge
        CPR : 'CPR', //compare/diff
        MRG : 'MRG', //merge 

        //meta model related commands
        GMM : 'GMM', //get meta models
        RMM : 'RMM', //register meta model
        UMM : 'UMM', //unregister meta model

        //maintenance related commands
        HEL  : 'HEL' , //hello
        GBY  : 'GBY' , //goodby
        SES  : 'SES' , //session
        STS  : 'STS' , //status
        CHG  : 'CHG' , //changes
        OBS  : 'OBS' , //observe
        UBS  : 'UBS' , //unobserve

        //Action related commands
        GAA  : 'GAA' , //get all actions
        CAL  : 'CAL' , //call
        ASC  : 'ASC' , //async Call
        ABC  : 'ABC' , //abort call
        CST  : 'CST' , //call status

        CMP : 'CMP', //compound
        MUT : 'MUT', //mute stop outputing results history only
        UMT : 'UMT', //unmute start outputing results
    };


    let CloModes = {
        CLS : 'CLS', //class: object only
        ATT : 'ATT', //attribute: class + attributes
        DEP : 'DEP', //deep: classes + attributes + containments
        FUL : 'FUL', //full: classes + attributes + containments + reference adaptation
    };


    function Cmd(t,args) {
        this.cmd = t;
        this.a = args;
    };
    Cmd.prototype.toString = function() {
        let cmdStr = this.cmd.toString();
        if(Array.isArray(this.a) && this.a.length > 0) {
            let args = [];
            for(let i=0;i<this.a.length;i++) {
                args.push(this.a[i]);
            }
            cmdStr += ' ' + args.join(' ');
        } else if(this.a) {
            cmdStr += ' ' + this.a.toString();
        }
        return cmdStr;
    };

    function Get(target) {
        Cmd.call(this,CmdTypes.GET, target);
    };
    Get.prototype = Object.create(Cmd.prototype);

    function Set(target,feature,value) {
        Cmd.call(this,CmdTypes.SET, [target,feature,value]);
    };
    Set.prototype = Object.create(Cmd.prototype);

    function Add(target,feature,value) {
        Cmd.call(this,CmdTypes.ADD, [target,feature,value])
    };
    Add.prototype = Object.create(Cmd.prototype);
        
    function Rem(target,feature,value) {
        Cmd.call(this,CmdTypes.REM, [target,feature,value])
    };
    Rem.prototype = Object.create(Cmd.prototype);
        
    function Mov(target,newIndex) {
        Cmd.call(this,CmdTypes.MOV, [target,newIndex])
    };
    Mov.prototype = Object.create(Cmd.prototype);
        
    function Clo(target,mode) {
        Cmd.call(this,CmdTypes.CLO,[target,mode])
    };
    Clo.prototype = Object.create(Cmd.prototype);
        
    function Crt(clazz,n,constructorArgs=[]) {
        Cmd.call(this,CmdTypes.CRT,[clazz,n,constructorArgs])
    };
    Crt.prototype = Object.create(Cmd.prototype);
        
    function Crn(package,name,n,constructorArgs=[]) {
        Cmd.call(this,CmdTypes.CRN,[package,name,n,constructorArgs])
    };
    Crn.prototype = Object.create(Cmd.prototype);

    function Qrf(target) {
        Cmd.call(this,CmdTypes.QRF,target)
    };
    Qrf.prototype = Object.create(Cmd.prototype);

    function Cpr(orig,changed,mode) {
        Cmd.call(this,CmdTypes.CPR,[orig,changed,mode]);
    };
    Cpr.prototype = Object.create(Cmd.prototype);

    function Mrg(orig,changed,mode) {
        Cmd.call(this,CmdTypes.MRG,[orig,changed,mode]);
    };
    Mrg.prototype = Object.create(Cmd.prototype);

    function Gmm() {
        Cmd.call(this,CmdTypes.GMM,null)
    };
    Gmm.prototype = Object.create(Cmd.prototype);

    function Rmm(metamodel) {
        Cmd.call(this,CmdTypes.RMM,metamodel)
    };
    Rmm.prototype = Object.create(Cmd.prototype);

    function Umm() {
        Cmd.call(this,CmdTypes.UMM,null)
    };
    Umm.prototype = Object.create(Cmd.prototype);
        
    function Sts() {
        Cmd.call(this,CmdTypes.STS,null)
    };
    Sts.prototype = Object.create(Cmd.prototype);

    function Hel(user,password) {
        Cmd.call(this,CmdTypes.HEL,[user,password])
    };
    Hel.prototype = Object.create(Cmd.prototype);

    function Ses(sessionId) {
        Cmd.call(this,CmdTypes.SES,sessionId)
    };
    Ses.prototype = Object.create(Cmd.prototype);

    function Gby(sessionId) {
        Cmd.call(this,CmdTypes.GBY,sessionId)
    };
    Gby.prototype = Object.create(Cmd.prototype);
        
    function Chg(latestChangeId,n) {
        Cmd.call(this,CmdTypes.CHG,[latestChangeId,n])
    };
    Chg.prototype = Object.create(Cmd.prototype);

    function Obs(eventType,eventKey) {
        Cmd.call(this,CmdTypes.OBS,[eventType,eventKey])
    };
    Obs.prototype = Object.create(Cmd.prototype);

    function Ubs(eventType,eventKey) {
        Cmd.call(this,CmdTypes.UBS,[eventType,eventKey])
    };
    Ubs.prototype = Object.create(Cmd.prototype);
        
    function Gaa() {
        Cmd.call(this,CmdTypes.GAA,null)
    };
    Gaa.prototype = Object.create(Cmd.prototype);
        
    function Cal(name,args=[],opts=[]) {
        Cmd.call(this,CmdTypes.CAL,[name,args,opts])
    };
    Cal.prototype = Object.create(Cmd.prototype);

    function Asc(name,args=[],opts=[]) {
        Cmd.call(this,CmdTypes.ASC,[name,args,opts])
    };
    Asc.prototype = Object.create(Cmd.prototype);
        
    function Abc(callId) {
        Cmd.call(this,CmdTypes.ABC,callId)
    };
    Abc.prototype = Object.create(Cmd.prototype);

    function Adc(constraintType,target,feature,law,name,annotation) {
        Cmd.call(this,CmdTypes.ADC, [constraintType,target,feature,law,name,annotation]);
    };
    Adc.prototype = Object.create(Cmd.prototype);

    function Gac() {
        Cmd.call(this,CmdTypes.GAC, null);
    };
    Gac.prototype = Object.create(Cmd.prototype);
	
    function Val() {
        Cmd.call(this,CmdTypes.VAL, null);
    };
    Val.prototype = Object.create(Cmd.prototype);
	
    function Rmc(target) {
        Cmd.call(this,CmdTypes.RMC, target);
    };
    Rmc.prototype = Object.create(Cmd.prototype);
	
	function Mut() {
        Cmd.call(this,CmdTypes.MUT,null)
    };
    Mut.prototype = Object.create(Cmd.prototype);

    function Umt() {
        Cmd.call(this,CmdTypes.UMT,null)
    };
    Umt.prototype = Object.create(Cmd.prototype);

    function Cmp(){
        Cmd.call(this,CmdTypes.CMP,[])
    };
    Cmp.prototype = Object.create(Cmd.prototype);
            
    Cmp.prototype.Get = function(target) {
        this.a.push(new Get(target));
        return this;
    };
        
    Cmp.prototype.Set = function(target,feature,value) {
        this.a.push(new Set(target,feature,value));
        return this;
    }

    Cmp.prototype.Add = function(target,feature,value) {
        this.a.push(new Add(target,feature,value));
        return this;
    };
    
    Cmp.prototype.Rem = function(target,feature,value) {
        this.a.push(new Rem(target,feature,value));
        return this
    };
    
    Cmp.prototype.Mov = function(target,newIndex) {
        this.a.push(new Mov(target,newIndex));
        return this;
    };
    
    Cmp.prototype.Clo = function(target,mode) {
        this.a.push(new Clo(target,mode));
        return this;
    };
    
    Cmp.prototype.Crt = function(clazz,n,constructorArgs=[]) {
        this.a.push(new Crt(clazz,n,constructorArgs));
        return this;
    };
    
    Cmp.prototype.Crn = function(package,name,n,constructorArgs=[]) {
        this.a.push(new Crn(package,name,n,constructorArgs));
        return this;
    };

    Cmp.prototype.Qrf = function(target) {
        this.a.push(new Qrf(target));
        return this;
    };

    Cmp.prototype.Cpr = function(orig,changed,mode) {
        this.a.push(new Cpr(orig,changed,mode));
        return this;
    };

    Cmp.prototype.Mrg = function(orig,changed,mode) {
        this.a.push(new Mrg(orig,changed,mode));
        return this;
    };    
    
    Cmp.prototype.Sts = function() {
        this.a.push(new Sts());
        return this;
    };

    Cmp.prototype.Gmm = function() {
        this.a.push(new Gmm());
        return this;
    };

    Cmp.prototype.Rmm = function(metamodel) {
        this.a.push(new Rmm(metamodel));
        return this;
    };

    Cmp.prototype.Umm = function(metamodel) {
        this.a.push(new Umm(metamodel));
        return this;
    };

    Cmp.prototype.Hel = function(user,password) {
        this.a.push(new Hel(user,password));
        return this;
    };

    Cmp.prototype.Ses = function(sessionId) {
        this.a.push(new Ses(sessionId));
        return this;
    };

    Cmp.prototype.Gby = function(sessionId) {
        this.a.push(new Gby(sessionId));
        return this;
    };
    
    Cmp.prototype.Chg = function(changeId,n) {
        this.a.push(new Chg(changeId,n));
        return this;
    };

    Cmp.prototype.Obs = function(eventType,eventKey) {
        this.a.push(new Obs(eventType,eventKey));
        return this;
    };

    Cmp.prototype.Ubs = function(eventType,eventKey) {
        this.a.push(new Ubs(eventType,eventKey));
        return this;
    };
    
    Cmp.prototype.Gaa = function() {
        this.a.push(new Gaa());
        return this;
    };
    
    Cmp.prototype.Cal = function(name,args=[],opts=[]) {
        this.a.push(new Cal(name,args,opts));
        return this;
    };
    
    Cmp.prototype.Asc = function(name,args=[],opts=[]) {
        this.a.push(new Asc(name,args,opts));
        return this;
    };
    
    Cmp.prototype.Abc = function(callId) {
        this.a.push(new Abc(callId));
        return this;
    };

    Cmp.prototype.Adc = function(constraintType,target,feature,law,name,annotation) {
        this.a.push(new Adc(constraintType,target,feature,law,name,annotation));
        return this;
    };

    Cmp.prototype.Gac = function() {
        this.a.push(new Gac());
        return this;
    };

    Cmp.prototype.Val = function() {
        this.a.push(new Val());
        return this;
    };

    Cmp.prototype.Rmc = function(target) {
        this.a.push(new Rmc(target));
        return this;
    };

    Cmp.prototype.Mut = function() {
        this.a.push(new Mut());
        return this;
    };

    Cmp.prototype.Umt = function() {
        this.a.push(new Umt());
        return this;
    };

   
    //Define the external interface
    return {
        Cmd : Cmd,
        Get : Get,
        Set : Set,
        Add : Add,
        Rem : Rem,
        Mov : Mov,
        Clo : Clo,
        Crt : Crt,
        Crn : Crn,
        Qrf : Qrf,
        Cpr : Cpr,
        Mrg : Mrg,
        Gmm : Gmm,
        Rmm : Rmm,
        Umm : Umm,
        Hel : Hel,
        Ses : Ses,
        Gby : Gby,
        Sts : Sts,
        Chg : Chg,
        Obs : Obs,
        Ubs : Ubs,
        Gaa : Gaa,
        Cal : Cal,
        Asc : Asc,
        Abc : Abc,
		Adc : Adc,
		Gac : Gac,
		Val : Val,
		Rmc : Rmc,
        Cmp : Cmp,
        Mut : Mut,
        Umt : Umt,
        CmdTypes : CmdTypes,
        CloModes : CloModes
    };

})());

//make it available on the lowest level
Object.assign(eoq2,eoq2.command);


// Check Object definitions
//console.log(Object.keys(eoq2.command));
//console.log(eoq2.command.Get);