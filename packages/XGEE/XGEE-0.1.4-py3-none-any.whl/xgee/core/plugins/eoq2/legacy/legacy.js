/*
* Legacy support for old jseoq commands
* 2019 Björn Annighöfer
*/

var eoq2 = eoq2 || {}
eoq2.legacy = eoq2.legacy || {}

Object.assign(eoq2.legacy,(function(){

    /**
     * 
     * jseoq1 legacy layer
     */

    /*
    Is useless, because object-oriented commands were never implemented on the js side of jseoq1
    function UpgradeCmd(legacyCmd) {
        let cmd = null;
        if(legacyCmd.type == jseoq.model.CommandTypesE.HELLO) {
            cmd = new eoq2.Cmd(eoq2.CmdTypes.HEL,[legacyCmd.user,legacyCmd.identification]);
        } else if(legacyCmd.type == jseoq.model.CommandTypesE.GOODBYE) {
            cmd = new eoq2.Cmd(eoq2.CmdTypes.GBY,[legacyCmd.sessionId]);
        } else if(legacyCmd.type == jseoq.model.CommandTypesE.SESSION) {
            cmd = new eoq2.Cmd(eoq2.CmdTypes.SES,[legacyCmd.sessionId]);
        } else if(legacyCmd.type == jseoq.model.CommandTypesE.STATUS) {
            cmd = new eoq2.Cmd(eoq2.CmdTypes.STS,[]);
        } else if(legacyCmd.type == jseoq.model.CommandTypesE.CHANGES) {
            cmd = new eoq2.Cmd(eoq2.CmdTypes.CHG,[legacyCmd.earliestChangeId]);
        } else if(legacyCmd.type == jseoq.model.CommandTypesE.RETRIEVE) {
            cmd = new eoq2.Cmd(eoq2.CmdTypes.GET,UpgradeQry(legacyCmd.target,legacyCmd.query));
        } else if(legacyCmd.type == jseoq.model.CommandTypesE.CREATE) {
            cmd = new eoq2.Cmd(eoq2.CmdTypes.CRT,[legacyCmd.packageNsUri,legacyCmd.className,UpgradeVal(legacyCmd.n)]);
        } else if(legacyCmd.type == jseoq.model.CommandTypesE.UPDATE) {
            cmd = new eoq2.Cmd(eoq2.CmdTypes.SET,[UpgradeQry(legacyCmd.target,legacyCmd.query),UpgradeVal(legacyCmd.value)]);
            //cmd = new eoq2.Cmd(eoq2.CmdTypes.ADD,[legacyCmd.target,legacyCmd.value]);
            //cmd = new eoq2.Cmd(eoq2.CmdTypes.REM,[legacyCmd.target,legacyCmd.value]);
        } else if(legacyCmd.type == jseoq.model.CommandTypesE.CLONE) {
            cmd = new eoq2.Cmd(eoq2.CmdTypes.CLO,[UpgradeVal(legacyCmd.target),legacyCmd.mode]);
        } else if(legacyCmd.type == jseoq.model.CommandTypesE.CALL) {
            cmd = new eoq2.Cmd(eoq2.CmdTypes.CAL,[legacyCmd.action].concat(UpgradeValue(legacyCmd.args)));
        } else if(legacyCmd.type == jseoq.model.CommandTypesE.ASYNCCALL) {
            cmd = new eoq2.Cmd(eoq2.CmdTypes.ASC,[legacyCmd.action].concat(UpgradeValue(legacyCmd.args)));
        } else if(legacyCmd.type == jseoq.model.CommandTypesE.CALLSTATUS) {
            cmd = new eoq2.Cmd(eoq2.CmdTypes.GBY,[legacyCmd.callId]);
        } else if(legacyCmd.type == jseoq.model.CommandTypesE.ABORTCALL) {
            cmd = new eoq2.Cmd(eoq2.CmdTypes.GBY,[legacyCmd.callId]);
        } else if(legacyCmd.type == jseoq.model.CommandTypesE.COMPOUND) {
            subcommands = [];
            for(let i=0; i<legacyCmd.commands.length; i++) {
                let lsc = legacyCmd.commands[i];
                let sc = UpgradeCmd(lsc) ;
                subcommands.push(sc);
            }
            cmd = new eoq2.Cmd(eoq2.CmdTypes.CMP,subcommands)
        } else {
            throw new Error('Unknown command type: '+legacyCmd.type);
        }
        return cmd;
    }

    function UpgradeQry(target,legacyQry) {
        let root = UpgradeVal(target);

        let qry = new eoq2.Qry(root);
        for(let i=0; i<legacyQry.segments; i++) {
            let ls = legacyQry.segments[i];
            if(ls.type == jseoq.model.SegmentTypesS.PATH) {
                let name = ls.identifier;
                qry.Pth(name);
            } else if(ls.type == jseoq.model.SegmentTypesE.CLAZZ){
                let name = ls.identifier;
                qry.Cls(name);
            } else if(ls.type == jseoq.model.SegmentTypesE.INSTANCE) {
                let name = ls.identifier;
                qry.Iio(name);
            } else if(ls.type == jseoq.model.SegmentTypesE.META) {
                let name = ls.identifier;
                qry.Met(name);
            } else {
                throw Error("Unknown segment type: "+ls.type);
            }

            //consider selectors 
            if(ls.selector) {
                let selector = ls.selector;
                subqry = new eoq2.Qry();
                subqry.Pth(selector.name);
                switch(selector.operator.type) {
                    case jseoq.model.OperatorTypesE.EQUAL:
                        subqry.Equ(UpgradeVal(selector.value));
                        break;
                    case jseoq.model.OperatorTypesE.NOTEQUAL:
                            subqry.Neq(UpgradeVal(selector.value));
                            break;
                    case jseoq.model.OperatorTypesE.GREATER:
                            subqry.Gre(UpgradeVal(selector.value));
                            break;
                    case jseoq.model.OperatorTypesE.LESS:
                            subqry.Les(UpgradeVal(selector.value));
                            break;
                    default:
                        throw new Error("Unknown operator in selector: "+selector.operator);
                }
                qry.Sel(subqry);
            }

            //consider index
            if(ls.index) {
                let index = ls.index;
                switch(index.type) {
                    case jseoq.model.IndexTypesE.NUMBER:
                        qry.Idx(index.value);
                    default:
                        throw new Error("Legacy conversion does not support index type: "+index.type);
                }
            }
        }

        return qry;
    }

    function UpgradeVal(legacyVal) {
        let qry = null;

        if(legacyVal.type == jseoq.model.ValueTypesE.LIST) {
            let subqrys = [];
            for(let i=0;i<legacyVal.v.length;i++) {
                let sv = legacyVal.v[i];
                let sq = UpgradeVal(sv);
                subqrys.push(sq);
            }
            //qry = new eoq2.Seg(eoq2.QrySegTypes.ARR,subqrys);
            qry = subqrys; //is that translation correct?
        } else if(legacyVal.type == jseoq.model.ValueTypesE.INT) {
            qry = legacyVal.v;
        } else if(legacyVal.type == jseoq.model.ValueTypesE.FLOAT) {
            qry = legacyVal.v;
        } else if(legacyVal.type == jseoq.model.ValueTypesE.BOOL) {
            qry = legacyVal.v;
        } else if(legacyVal.type == jseoq.model.ValueTypesE.STRING) {
            qry = legacyVal.v;
        } else if(legacyVal.type == jseoq.model.ValueTypesE.OBJECTREF) {
            qry = new eoq2.Seg(eoq2.QrySegTypes.OBJ,legacyVal.v);
        } else if(legacyVal.type == jseoq.model.ValueTypesE.EMPTY) {
            qry = null;
        } else if(legacyVal.type == jseoq.model.ValueTypesE.HISTORYREF) {
            qry = new eoq2.Seg(eoq2.QrySegTypes.HIS,legacyVal.v);
        } else {
            throw Error("Unknown value type: "+legacyVal.type);
        }
        return qry;
    }

    

    function DowngradeRes(res) {
        let legacyRes = null;
        if(res.res == eoq2.CmdTypes.CMP) {
            legacyRes = new jseoq.model.CompoundResult();
            if(res.s == eoq2.ResTypes.ERR) {
                legacyRes.type = jseoq.model.ResultTypesE.COMPOUND_ERROR; //if a single command failed the full compound command is failed.
            }
            for(let i=0;i<res.v.length;i++) {
                subresult = res.v[i];
                lsr = DowngradeRes(subresult);
                legacyRes.results.push(lsr);
            }
        } else { // single commands
            if(res.res == eoq2.CmdTypes.HEL) {
				legacyRes = new jseoq.model.HelloResult();
				legacyRes.sessionId = res.v;
        	} else if(res.res == eoq2.CmdTypes.GBY) {
				legacyRes = new jseoq.model.GoodbyeResult();
        	} else if(res.res == eoq2.CmdTypes.SES) {
				legacyRes = new jseoq.model.SessionResult();
        	} else if(res.res == eoq2.CmdTypes.STA) {
				legacyRes = new jseoq.model.StatusResult();
				legacyRes.changeId = res.v;
	        } else if(res.res == eoq2.CmdTypes.CHG) {
				legacyRes = new jseoq.model.ChangesResult();
				legacyRes.changes = DowngradeVal(res.v); //could be more complicated if changes format differs in future
	        } else if(res.res == eoq2.CmdTypes.GET) {
				legacyRes = new jseoq.model.RetrieveResult();
				legacyRes.value = DowngradeVal(res.v);
			} else if(res.res == eoq2.CmdTypes.CRT) {
				legacyRes = new jseoq.model.CreateResult();
				legacyRes.value = DowngradeVal(res.v);
			} else if(res.res == eoq2.CmdTypes.SET) {
				legacyRes = new jseoq.model.UpdateResult();
				legacyRes.target = DowngradeVal(res.v);
			} else if(res.res == eoq2.CmdTypes.CLO) {
				legacyRes = new jseoq.model.CloneResult();
				legacyRes.value = DowngradeVal(res.v);
			} else if(res.res == eoq2.CmdTypes.CAL) {
				legacyRes = new jseoq.model.CallResult();
				legacyRes.callId = res.v[0];
				legacyRes.returnValues = DowngradeVal(res.v.slice(1)); //skip the first entry
			} else if(res.res == eoq2.CmdTypes.ASC) {
				legacyRes = new jseoq.model.AsyncCallResult();
				legacyRes.callId = res.v;
			} else if(res.res == eoq2.CmdTypes.CST) {
				legacyRes = new jseoq.model.CallStatusResult();
				legacyRes.callId = res.v[0];
				legacyRes.callStatus = res.v[1];
				legacyRes.result = DowngradeVal(res.v.slice(1)); //skip the first entry
			} else if(res.res == eoq2.CmdTypes.ABC) {
				legacyRes = new jseoq.model.AbortCallResult();
			} else {
				throw new Error("Unknown result type: " + res.res);
			}
            
            //check if an error happened then we must override the legacy result
            if(res.s == eoq2.ResTypes.ERR) {
                let commandType = legacyRes.commandType;
                legacyRes = new jseoq.model.ErrorResult();
                legacyRes.commandType = commandType;
                legacyRes.code = 0;
                legacyRes.message = res.v;
            } 

            // copy the transaction id
            legacyRes.transactionId = res.n; //works for all results
        }
        return legacyRes;
    }


    function DowngradeVal(qry) {
    	let legacyVal = 0;
        if(typeof qry == "number" && Number.isInteger(qry)) {
            legacyVal = new jseoq.model.IntValue();
            legacyVal.v=qry;
        } else if(typeof qry == "number") {
        	legacyVal = new jseoq.model.FloatValue();
        	legacyVal.v = qry;
        } else if(typeof qry == "boolean") {
        	legacyVal = new jseoq.model.BoolValue();
        	legacyVal.v = qry;
        } else if(typeof qry == "string") {
        	legacyVal = new jseoq.model.StringValue();
        	legacyVal.v = qry;
        } else if(qry.qry == eoq2.QrySegTypes.OBJ) {
            legacyVal = new jseoq.model.ObjectRefValue();
        	legacyVal.v = qry.v;
        } else if(qry.qty == eoq2.QrySegTypes.HIS) {
        	value = new jseoq.model.HistoryRefValue();
            value.v = qry.v;
        } else if(null == qry) {
        	legacyVal = new jseoq.model.EmptyValue();
        } else if(qry instanceof Array) {
            legacyVal = new jseoq.model.ListValue();
            for(var i=0;i<qry.length;i++) {
                legacyVal.v.push(DowngradeVal(qry[i]));
            }
            return legacyVal;
        } else {
            throw Error('Cannot convert data type '+(typeof qry)+' to legacy EOQ value: '+qry);
        }
        return legacyVal;
    };
    */

    var jseoq1version = 100;


    function Jseoq1LegacyDomain(domain) {
        this.domain = domain;
        this._url = domain.url;
    }

    Jseoq1LegacyDomain.prototype = Object.create(jseoq.domains.Domain.prototype);

    Jseoq1LegacyDomain.prototype.Do = function(legacyCmd,successCallback=null,failCallback=null) {
        var self = this;
		this.DoSync(legacyCmd).then(function(result) {
			if(jseoq.ResultParser.IsResultOk(result)) {
				jsResult = self.ResultToJs(result);
				successCallback(jsResult);
				return;
			} else {
				jsResult = self.ResultToJs(result);
				failCallback(jsResult);
				return;
			} 
		});
		return this;
    };

    Jseoq1LegacyDomain.prototype.DoSync = function(legacyCmd) {
        let self = this;
        return new Promise(function(resolve,reject) {
            //let cmd = UpgradeCmd(legacyCmd);
            let legacyCmdStr = jseoq.CommandParser.CommandToString(legacyCmd);
            self.domain.RawDo(legacyCmdStr,jseoq1version).then(function(legacyResStr){
                legacyRes = null;
                try {
                    legacyRes = jseoq.ResultParser.StringToResult(legacyResStr);
                } catch(e) {
                    legacyRes = new jseoq.model.ErrorResult();
					legacyRes.message = e.toString();
                }
                resolve(legacyRes);
            });
        });
    };

    Jseoq1LegacyDomain.prototype.ResultToJs = function(result) {
		var jsObjects = null;
		if(result.commandType == jseoq.model.CommandTypesE.COMPOUND) {
			var jsObjects = [];
			for(var i=0;i<result.results.length;i++) {
				var jsValue = this.ResultToJs(result.results[i]);
				jsObjects.push(jsValue);
			}
		} else { // not compound command
			if(jseoq.ResultParser.IsResultOk(result)) {
				if(result.commandType == jseoq.model.CommandTypesE.RETRIEVE) {
					jsObjects = [true,result.transactionId,jseoq.ValueParser.ValueToJs(result.value)];
				} else if(result.commandType == jseoq.model.CommandTypesE.CREATE) {
					jsObjects = [true,result.transactionId,jseoq.ValueParser.ValueToJs(result.value)];
				} else if(result.commandType == jseoq.model.CommandTypesE.UPDATE) {
					jsObjects = [true,result.transactionId,jseoq.ValueParser.ValueToJs(result.target)];
				} else if(result.commandType == jseoq.model.CommandTypesE.CHANGES) {
					jsObjects = [true,jseoq.ValueParser.ValueToJs(result.changes)];
				}
			} else { //error
				jsObjects = [false,result.code, result.message];
			}
		}
		return jsObjects;
	};



    return {
        Jseoq1LegacyDomain : Jseoq1LegacyDomain
    };
})());