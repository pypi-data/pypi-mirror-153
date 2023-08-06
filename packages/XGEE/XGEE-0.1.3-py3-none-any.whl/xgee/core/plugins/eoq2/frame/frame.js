var eoq2 = eoq2 || {};
eoq2.frame = eoq2.frame || {};

Object.assign(eoq2.frame,(function(){
    var FrameTypes = {
        CMD : "CMD", //Command
        RES : "RES", //Result
        CHG : "CHG", //Change
        EVT : "EVT", //Event: Change, call output
        ERR : "ERR" //Error
    };

    function Frame(type,uid,data,version=eoq2.version) {
        this.eoq = type;
        this.ver = version; 
        this.uid = uid;
        this.dat = data;
    };

    return {
        FrameTypes : FrameTypes,
        Frame : Frame
    };

})());