var jseoq = jseoq || {};
jseoq.ResultParser = (function() {
        
    function ResultToString(result) {
        var resultSegments = [];
        var seperator = ' ';
        if([jseoq.model.ResultTypesE.COMPOUND_OK, jseoq.model.ResultTypesE.COMPOUND_ERROR].includes(result.type)) {
            seperator = '\n';
            for(var i=0; i<result.results.length; i++) {
                resultSegments.push(this.ResultToString(result.results[i]));
            }
        } else {
            var statusStr = jseoq.model.ResultTypesE.to_string(result.type);
            resultSegments = resultSegments.concat([statusStr, result.transactionId.toString(), jseoq.model.CommandTypesE.to_string(result.commandType)]);
			if(result.type == jseoq.model.ResultTypesE.OK) {
				if(result.commandType == jseoq.model.CommandTypesE.HELLO) {
					resultSegments = resultSegments.concat([result.sessionId]);
			    } else if(result.commandType == jseoq.model.CommandTypesE.GOODBYE) {
					;
			    } else if(result.commandType == jseoq.model.CommandTypesE.SESSION) {
					;
			    } else if(result.commandType == jseoq.model.CommandTypesE.STATUS) {
			    	resultSegments = resultSegments.concat([result.changeId.toString()]);
			    } else if(result.commandType == jseoq.model.CommandTypesE.CHANGES) {
					resultSegments = resultSegments.concat([jseoq.ValueParser.ValueToString(result.changes)]);
				} else if(result.commandType == jseoq.model.CommandTypesE.RETRIEVE) {
					resultSegments = resultSegments.concat([jseoq.ValueParser.ValueToString(result.value)]);
                } else if(result.commandType == jseoq.model.CommandTypesE.CREATE) {
                    resultSegments = resultSegments.concat([jseoq.ValueParser.ValueToString(result.value)]);
                } else if(result.commandType == jseoq.model.CommandTypesE.UPDATE) {
                    resultSegments = resultSegments.concat([jseoq.ValueParser.ValueToString(result.target)]);
                } else if(result.commandType == jseoq.model.CommandTypesE.CLONE) {
                    resultSegments = resultSegments.concat([jseoq.ValueParser.ValueToString(result.value)]);
                } else if(result.commandType == jseoq.model.CommandTypesE.CALL) {
					resultSegments = resultSegments.concat([result.callId.toString(), jseoq.ValueParser.ValueToString(result.returnValues)]);
				} else if(result.commandType == jseoq.model.CommandTypesE.ASYNCCALL) {
			    	resultSegments = resultSegments.concat([result.callId.toString()]);
				} else if(result.commandType == jseoq.model.CommandTypesE.CALLSTATUS) {
					resultSegments = resultSegments.concat([result.callId.toString(), jseoq.model.CallStatusE.to_string(result.callStatus), jseoq.ValueParser.ValueToString(result.result)]);
				} else if(result.commandType == jseoq.model.CommandTypesE.ABORTCALL) {
			    	;
				}

            } else if(result.type == jseoq.model.ResultTypesE.ERROR) {
            	resultSegments = resultSegments.concat([result.code.toString(),"'"+result.message+"'"]);
            }
        }
        return resultSegments.join(seperator);
    };
    
    function StringToResult(resultStr) {
        var result = null;
        var resultLines = resultStr.split(/\r?\n/); //TODO: This will get problems if newlines are included in strings
        if(1 < resultLines.length) {
            result = new jseoq.model.CompoundResult();
            for(var i=0;i<resultLines.length;i++) {
				subResult = this.SingleStringLineToResult(resultLines[i])
            	result.results.push(subResult);
				if(subResult.type == jseoq.model.ResultTypesE.ERROR) {
					result.type = jseoq.model.ResultTypesE.COMPOUND_ERROR; //if a single command failed the full compound command is failed.
				}
            }
        } else {
        	result = this.SingleStringLineToResult(resultStr);
        }
        return result;
    };
    
    function SingleStringLineToResult(resultLine) {
        var result = null;
        var resultSegments = this.StringAtSpaceSplitter(resultLine);

        var nSegments = resultSegments.length
        if(jseoq.model.ResultTypesE.to_string(jseoq.model.ResultTypesE.OK) == resultSegments[0] && nSegments >= 3) {
        	if(jseoq.model.CommandTypesE.to_string(jseoq.model.CommandTypesE.HELLO) == resultSegments[2] && nSegments == 4) {
				result = new jseoq.model.HelloResult();
				result.transactionId = Number.parseInt(resultSegments[1]);
				result.sessionId = resultSegments[3];
        	} else if(jseoq.model.CommandTypesE.to_string(jseoq.model.CommandTypesE.GOODBYE) == resultSegments[2] && nSegments == 3) {
				result = new jseoq.model.GoodbyeResult();
				result.transactionId = Number.parseInt(resultSegments[1]);
        	} else if(jseoq.model.CommandTypesE.to_string(jseoq.model.CommandTypesE.SESSION) == resultSegments[2] && nSegments == 3) {
				result = new jseoq.model.SessionResult();
				result.transactionId = Number.parseInt(resultSegments[1]);
        	} else if(jseoq.model.CommandTypesE.to_string(jseoq.model.CommandTypesE.STATUS) == resultSegments[2] && nSegments == 4) {
				result = new jseoq.model.StatusResult();
				result.transactionId = Number.parseInt(resultSegments[1]);
				result.changeId = Number.parseInt(resultSegments[3]);
	        } else if(jseoq.model.CommandTypesE.to_string(jseoq.model.CommandTypesE.CHANGES) == resultSegments[2] && nSegments == 4) {
				result = new jseoq.model.ChangesResult();
				result.transactionId = Number.parseInt(resultSegments[1]);
				result.changes = jseoq.ValueParser.StringToValue(resultSegments[3]);
	        } else if(jseoq.model.CommandTypesE.to_string(jseoq.model.CommandTypesE.RETRIEVE) == resultSegments[2] && nSegments == 4) {
				result = new jseoq.model.RetrieveResult();
				result.transactionId = Number.parseInt(resultSegments[1])
				result.value = jseoq.ValueParser.StringToValue(resultSegments[3]);
			} else if(jseoq.model.CommandTypesE.to_string(jseoq.model.CommandTypesE.CREATE) == resultSegments[2] && nSegments == 4) {
				result = new jseoq.model.CreateResult();
				result.transactionId = Number.parseInt(resultSegments[1]);
				result.value = jseoq.ValueParser.StringToValue(resultSegments[3]);
			} else if(jseoq.model.CommandTypesE.to_string(jseoq.model.CommandTypesE.UPDATE) == resultSegments[2] && nSegments == 4) {
				result = new jseoq.model.UpdateResult();
				result.transactionId = Number.parseInt(resultSegments[1]);
				result.target = jseoq.ValueParser.StringToValue(resultSegments[3]);
			} else if(jseoq.model.CommandTypesE.to_string(jseoq.model.CommandTypesE.CLONE) == resultSegments[2] && nSegments == 4) {
				result = new jseoq.model.CloneResult();
				result.transactionId = Number.parseInt(resultSegments[1]);
				result.value = jseoq.ValueParser.StringToValue(resultSegments[3]);
			} else if(jseoq.model.CommandTypesE.to_string(jseoq.model.CommandTypesE.CALL) == resultSegments[2] && nSegments == 5) {
				result = new jseoq.model.CallResult();
				result.transactionId = Number.parseInt(resultSegments[1]);
				result.callId = Number.parseInt(resultSegments[3]);
				result.returnValues = jseoq.ValueParser.StringToValue(resultSegments[4]);
			} else if(jseoq.model.CommandTypesE.to_string(jseoq.model.CommandTypesE.ASYNCCALL) == resultSegments[2] && nSegments == 4) {
				result = new jseoq.model.AsyncCallResult();
				result.transactionId = Number.parseInt(resultSegments[1]);
				result.callId = Number.parseInt(resultSegments[3]);
			} else if(jseoq.model.CommandTypesE.to_string(jseoq.model.CommandTypesE.CALLSTATUS) == resultSegments[2] && nSegments == 6) {
				result = new jseoq.model.CallStatusResult();
				result.transactionId = Number.parseInt(resultSegments[1]);
				result.callId = Number.parseInt(resultSegments[3]);
				result.callStatus = jseoq.model.CallStatusE.to_string(resultSegments[4]);
				result.result = jseoq.ValueParser.StringToValue(resultSegments[5]);
			} else if(jseoq.model.CommandTypesE.to_string(jseoq.model.CommandTypesE.ABORTCALL) == resultSegments[2] && nSegments == 3) {
				result = new jseoq.model.AbortCallResult();
				result.transactionId = Number.parseInt(resultSegments[1]);
			} else {
				throw new Error('Result string could not be split into segments: '+ resultLine);
			}
        } else if(jseoq.model.ResultTypesE.to_string(jseoq.model.ResultTypesE.ERROR) == resultSegments[0] && nSegments == 5) {
        	result = new jseoq.model.ErrorResult();
        	result.transactionId = Number.parseInt(resultSegments[1]);
        	result.commandType = jseoq.model.CommandTypesE[resultSegments[2]];
        	result.code = Number.parseInt(resultSegments[3]);
        	result.message = resultSegments[4];
        } else {
            throw new Error('Result string could not be split into segments: '+ resultLine);
        }
        return result;
    };
	
	function StringAtSpaceSplitter(txt) {
		//my own line splitter function because regex sucks
		var segments = [];
		var b = 0; //begin of segment
		var e = 0; //end of segment
		var state = 0 // 0: begin, 1: no open string, 2: open string
		var nOpenStrings = 0;
		for(var i=0;i<txt.length;i++) {
			if(state==0) {
				b = i;
				e = i;
				if(txt[i]=='\'') {
                    nOpenStrings++;
					state = 2;
				} else {
					state = 1;
				}
			} else if(state==1) {
				e = i;
				if(txt[i]==' ' && nOpenStrings==0) {
					segments.push(txt.substring(b,e));
					state = 0;
				} else if(txt[i]=='\'') {
					nOpenStrings++;
					state = 2; //open string
				} 
			} else if(state==2) {
				e = i;
				if(txt[i]=='\'') {
					nOpenStrings--;
					state = 1; //closed string
				} 
			}
		}
		if(nOpenStrings>0) {
			throw new Error('String has no ending. Missing a \': '+txt.substring(b,e+1));
		}
		segments.push(txt.substring(b,e+1));
		return segments;
	};

	function IsResultOk(result) {
		return (result.type == jseoq.model.ResultTypesE.OK ||
		   result.type == jseoq.model.ResultTypesE.COMPOUND_OK);
	};

	function IsResultNok(result) {
		return !IsResultOk(result);
	};
	
	function StringAtSpaceSplitter(txt) {
		//my own line splitter function because regex sucks
		var segments = [];
		var b = 0; //begin of segment
		var e = 0; //end of segment
		var state = 0 // 0: begin, 1: no open string, 2: open string
		var nOpenStrings = 0;
		for(var i=0;i<txt.length;i++) {
			if(state==0) {
				b = i;
				e = i;
				if(txt[i]=='\'') {
                    nOpenStrings++;
					state = 2;
				} else {
					state = 1;
				}
			} else if(state==1) {
				e = i;
				if(txt[i]==' ' && nOpenStrings==0) {
					segments.push(txt.substring(b,e));
					state = 0;
				} else if(txt[i]=='\'') {
					nOpenStrings++;
					state = 2; //open string
				} 
			} else if(state==2) {
				e = i;
				if(txt[i]=='\'') {
					nOpenStrings--;
					state = 1; //closed string
				} 
			}
		}
		if(nOpenStrings>0) {
			throw new Error('String has no ending. Missing a \': '+txt.substring(b,e+1));
		}
		segments.push(txt.substring(b,e+1));
		return segments;
	};

	/*Returns the message and code for falied results */
	function GetErrorString(result) {
		if(result.type==jseoq.model.ResultTypesE.COMPOUND_ERROR) {
			errorResult = result.results[result.results.length-1]; //it is always the last one that failed
			return errorResult.message+' ('+errorResult.code+')';
		}else if(result.type==jseoq.model.ResultTypesE.ERROR) {
			return result.message+' ('+result.code+')';
		}
		return '';
	}


	return {
		ResultToString : ResultToString,
		StringToResult : StringToResult,
		SingleStringLineToResult : SingleStringLineToResult,
		IsResultOk : IsResultOk,
		IsResultNok : IsResultNok,
		GetErrorString : GetErrorString,
		StringAtSpaceSplitter : StringAtSpaceSplitter
	}

})();