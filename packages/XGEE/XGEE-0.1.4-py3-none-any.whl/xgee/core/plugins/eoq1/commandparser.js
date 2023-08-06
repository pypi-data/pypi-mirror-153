var jseoq = jseoq || {};
jseoq.CommandParser = (function() {

	function StringToCommand(commandStr) {
		//TODO: This is only a placeholder
		return commandStr;
	}; 
	
	function RetrieveCommand(target,query) {
        return this.RetrieveCommandStr(target,query); //queries are not parsed for now
	};
    
    function RetrieveCommandStr(target,queryStr) {
    	var command = new jseoq.model.RetrieveCommand();
    	command.target = target;
    	command.query = queryStr;
    	return command;
    };
    
    function CreateCommand(packageNsUri,className,n) {
        var command = new jseoq.model.CreateCommand();
		command.packageNsUri = new jseoq.model.StringValue();
		command.packageNsUri.v = packageNsUri;
		command.className = new jseoq.model.StringValue();
		command.className.v = className;
		command.n = new jseoq.model.IntValue();
		command.n.v;
        return command;
    };
    
    function UpdateCommand(target,query,value) {
        return this.UpdateCommandStr(target,query,value);
    };
    
    function UpdateCommandStr(target,queryStr,value) {
        var command = new jseoq.model.UpdateCommand();
        command.target = target;
        command.query = queryStr;
        command.value = value
        return command;
    };
    
    function CompoundCommand(subcommands) {
        var command = new jseoq.CompoundCommand();
        for(var i=0;i<subcommands.length;i++) {
            command.commands.push(subcommands[i]);
        }
        return command;
    };
    
    function CommandToString(command) {
        var commandSegments = [];
        var seperator = ' ';
        if(command.type == jseoq.model.CommandTypesE.COMPOUND) {
            seperator = '\n';
            for(var i=0;i<command.commands.length;i++) {
                commandSegments.push(this.CommandToString(command.commands[i]));
            }
        } else {
            var commandStr = jseoq.model.CommandTypesE.to_string(command.type);
            commandSegments.push(commandStr);
        	if(command.type == jseoq.model.CommandTypesE.HELLO) {
        		commandSegments = commandSegments.concat([jseoq.ValueParser.ValueToString(command.user), jseoq.ValueParser.ValueToString(command.identification)]);
        	} else if(command.type == jseoq.model.CommandTypesE.GOODBYE) {
        		commandSegments = commandSegments.concat([jseoq.ValueParser.ValueToString(command.sessionId)]);
        	} else if(command.type == jseoq.model.CommandTypesE.SESSION) {
        		commandSegments = commandSegments.concat([jseoq.ValueParser.ValueToString(command.sessionId)]);
        	} else if(command.type == jseoq.model.CommandTypesE.STATUS) {
        		;
        	} else if(command.type == jseoq.model.CommandTypesE.CHANGES) {
        		commandSegments = commandSegments.concat([jseoq.ValueParser.ValueToString(command.earliestChangeId)]);
        	} else if(command.type == jseoq.model.CommandTypesE.RETRIEVE) {
            	commandSegments = commandSegments.concat([jseoq.ValueParser.ValueToString(command.target),command.query]);
        	} else if(command.type == jseoq.model.CommandTypesE.CREATE) {
            	commandSegments = commandSegments.concat([jseoq.ValueParser.ValueToString(command.packageNsUri),jseoq.ValueParser.ValueToString(command.className),jseoq.ValueParser.ValueToString(command.n)]);
        	} else if(command.type == jseoq.model.CommandTypesE.UPDATE) {
            	commandSegments = commandSegments.concat([jseoq.ValueParser.ValueToString(command.target),command.query,jseoq.ValueParser.ValueToString(command.value)]);
        	} else if(command.type == jseoq.model.CommandTypesE.CLONE) {
            	commandSegments = commandSegments.concat([jseoq.ValueParser.ValueToString(command.target),jseoq.model.CloneModesE.to_string(command.mode)]);
            } else if(command.type == jseoq.model.CommandTypesE.CALL) {
        		commandSegments = commandSegments.concat([jseoq.ValueParser.ValueToString(command.action), jseoq.ValueParser.ValueToString(command.args)]);
            } else if(command.type == jseoq.model.CommandTypesE.ASYNCCALL) {
        		commandSegments = commandSegments.concat([jseoq.ValueParser.ValueToString(command.action), jseoq.ValueParser.ValueToString(command.args)]);
            } else if(command.type == jseoq.model.CommandTypesE.CALLSTATUS) {
        		commandSegments = commandSegments.concat([jseoq.ValueParser.ValueToString(command.callId)]);
            } else if(command.type == jseoq.model.CommandTypesE.ABORTCALL) {
        		commandSegments = commandSegments.concat([jseoq.ValueParser.ValueToString(command.callId)]);
            } else {
                throw new Error('Unknown command type: '+command.type);
            }
        }
        return commandSegments.join(seperator);
	};
	
    function StringToCommand(commandStr) {
        var command = null;
        var commandLines = commandStr.split(/\r?\n/); //TODO: This will get problems if newlines are included in strings
        if(1 < commandLines.length) {
            command = new jseoq.model.CompoundCommand();
            for(var i=0;i<commandLines.length;i++) {
                command.commands.push(this.SingleStringLineToCommand(commandLines[i]));
            }
        } else {
            command = this.SingleStringLineToCommand(commandStr);
        }
        return command;
    };
    
    function SingleStringLineToCommand(commandLine) {
        var command = null;
        var commandSegments = this.StringAtSpaceSplitter(commandLine);
        
        var nSegments = commandSegments.length
    	if(jseoq.model.CommandTypesE.to_string(jseoq.model.CommandTypesE.HELLO) == commandSegments[0] && nSegments == 3) {
	        command = new jseoq.model.HelloCommand();
	        command.user = jseoq.ValueParser.StringToValue(commandSegments[1]);
	        command.identification = jseoq.ValueParser.StringToValue(commandSegments[2]);
    	} else if(jseoq.model.CommandTypesE.to_string(jseoq.model.CommandTypesE.GOODBYE) == commandSegments[0] && nSegments == 2) {
	        command = new jseoq.model.GoodbyeCommand();
	        command.sessionId = jseoq.ValueParser.StringToValue(commandSegments[1]);
    	} else if(jseoq.model.CommandTypesE.to_string(jseoq.model.CommandTypesE.SESSION) == commandSegments[0] && nSegments == 2) {
	        command = new jseoq.model.SessionCommand();
	        command.sessionId = jseoq.ValueParser.StringToValue(commandSegments[1]);
    	} else if(jseoq.model.CommandTypesE.to_string(jseoq.model.CommandTypesE.STATUS) == commandSegments[0] && nSegments == 1) {
	        command = new jseoq.model.StatusCommand();
    	} else if(jseoq.model.CommandTypesE.to_string(jseoq.model.CommandTypesE.CHANGES) == commandSegments[0] && nSegments == 2) {
	        command = new jseoq.model.ChangesCommand();
	        command.earliestChangeId =jseoq.ValueParser.StringToValue(commandSegments[1]);
    	} else if(jseoq.model.CommandTypesE.to_string(jseoq.model.CommandTypesE.RETRIEVE) == commandSegments[0] && nSegments == 3) {
            command = new jseoq.model.RetrieveCommand();
            command.target = jseoq.ValueParser.StringToValue(commandSegments[1]);
            command.query = commandSegments[2];
        } else if(jseoq.model.CommandTypesE.to_string(jseoq.model.CommandTypesE.CREATE) == commandSegments[0] && nSegments == 4) {
            command = new jseoq.model.CreateCommand();
            command.packageNsUri = jseoq.ValueParser.StringToValue(commandSegments[1]);
            command.className = jseoq.ValueParser.StringToValue(commandSegments[2]);
            command.n = jseoq.ValueParser.StringToValue(commandSegments[3]);
        } else if(jseoq.model.CommandTypesE.to_string(jseoq.model.CommandTypesE.UPDATE) == commandSegments[0] && nSegments == 4) {
            command = new jseoq.model.UpdateCommand();
            command.target = jseoq.ValueParser.StringToValue(commandSegments[1]);
            command.query = commandSegments[2];
            command.value = jseoq.ValueParser.StringToValue(commandSegments[3]);
        } else if(jseoq.model.CommandTypesE.to_string(jseoq.model.CommandTypesE.CLONE) == commandSegments[0] && nSegments == 3) {
            command = new jseoq.model.CloneCommand();
            command.target = jseoq.ValueParser.StringToValue(commandSegments[1]);
            command.mode = jseoq.model.CloneModesE.from_string(commandSegments[2]);
        } else if(jseoq.model.CommandTypesE.to_string(jseoq.model.CommandTypesE.CALL) == commandSegments[0] && nSegments == 3) {
	        command = new jseoq.model.CallCommand();
	        command.action = jseoq.ValueParser.StringToValue(commandSegments[1]);
	        command.args = jseoq.ValueParser.StringToValue(commandSegments[2]);
        } else if(jseoq.model.CommandTypesE.to_string(jseoq.model.CommandTypesE.ASYNCCALL) == commandSegments[0] && nSegments == 3) {
	        command = new jseoq.model.AsyncCallCommand();
	        command.action = jseoq.ValueParser.StringToValue(commandSegments[1]);
	        command.args = jseoq.ValueParser.StringToValue(commandSegments[2]);
        } else if(jseoq.model.CommandTypesE.to_string(jseoq.model.CommandTypesE.CALLSTATUS) == commandSegments[0] && nSegments == 2) {
	        command = new jseoq.model.CallStatusCommand();
	        command.callId = jseoq.ValueParser.StringToValue(commandSegments[1]);
        } else if(jseoq.model.CommandTypesE.to_string(jseoq.model.CommandTypesE.ABORTCALL) == commandSegments[0] && nSegments == 2) {
	        command = new jseoq.model.AbortCallCommand();
	        command.callId = jseoq.ValueParser.StringToValue(commandSegments[1]);
        } else {
            throw new Error('Command string could not be split into segments: '+commandLine);
        }
        return command;
	};
	
	function CalcCommandHistoryLength(command) {
        var length = 0;
        if(command.type == jseoq.model.CommandTypesE.COMPOUND) {
            for(var i=0;i<command.commands.length;i++) {
				var subcommand = command.commands[i];
				length += this.CalcCommandHistoryLength(subcommand);
			}
		} else if([jseoq.model.CommandTypesE.RETRIEVE,jseoq.model.CommandTypesE.CREATE,jseoq.model.CommandTypesE.CALL].includes(command.type) ) {
			length = 1
		}
		return length;
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

	return {
		StringToCommand : StringToCommand,
		RetrieveCommand : RetrieveCommand,
		RetrieveCommandStr : RetrieveCommandStr,
		CreateCommand : CreateCommand,
		UpdateCommand : UpdateCommand,
		UpdateCommandStr : UpdateCommandStr,
		CompoundCommand : CompoundCommand,
		CommandToString : CommandToString,
		StringToCommand : StringToCommand,
		SingleStringLineToCommand : SingleStringLineToCommand,
		CalcCommandHistoryLength : CalcCommandHistoryLength,
		StringAtSpaceSplitter : StringAtSpaceSplitter
	}

})();