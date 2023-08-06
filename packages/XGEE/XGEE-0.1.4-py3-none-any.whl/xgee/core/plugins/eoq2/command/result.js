/*
 Command result
 2019 Bjoern Annighoefer
*/

var eoq2 = eoq2 || {};
eoq2.command = eoq2.command || {};

Object.assign(eoq2.command,(function(){
    var ResTypes = {
        OKY : 'OKY',
        ERR : 'ERR'
    };
   
    function Res(commandType,status,value,transactionId=0,changeId=0) {
        this.res = commandType; //correspondes to the command that this result comes from
        this.s = status; //status
        this.v = value; //result of the executed command (error text in case of error, subresult array in case of a compound command)
        this.n = transactionId;
        this.c = changeId;
    };
        
    Res.prototype.GetValue = function() {
        return ResGetValue(this);
    };

    function ResGetValue(res) {
        let val = null;
        if(ResTypes.ERR==res.s) {
            throw Error(res.v);
        }
        if(eoq2.command.CmdTypes.CMP==res.res) {
            val = [];
            for(let i=0;i<res.v.length;i++) {
                let sr = res.v[i];
                val.push(sr.v);
            }
        }
        else {
            val = res.v
        }
        return val;
    };

    return {
        ResTypes : ResTypes,
        Res : Res,
        ResGetValue : ResGetValue
    };
})());

//make it available on the lowest level
Object.assign(eoq2,eoq2.command);

