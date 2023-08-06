var jseoq = jseoq || {};
jseoq.domains = jseoq.domains || {};

jseoq.domains.BufferingDomain = (function() {
	function SingleCommandInfo(command,resolve) {
		this.command = command;
		this.resolve = resolve;
		this.startIndex = 0;
		this.len = 0;
	}
	
	function CommandStack() {
		this.singleCommandInfos = []; //SingleCommandInfo
	};
	
	function BufferingDomain(domain,waitTime) {
		this.domain = domain;
		this.waitTime = waitTime;
		this.currentCommandStack = new CommandStack();
        this.execTimeout = null;
        return this;
    };
    
    BufferingDomain.prototype = Object.create(jseoq.domains.Domain.prototype);

	BufferingDomain.prototype.DoSync = function(command) {
		return this.DoSyncBuffering(command);
	};

	BufferingDomain.prototype.Do = function(command,successCallback,failCallback) { //lagecy support
		return this.domain.Do(command,successCallback,failCallback);
	};

	BufferingDomain.prototype.DoSyncBuffering = function(command) {
		var self = this;
		return new Promise(function(resolve,reject) {
			var singleCommandInfo = new SingleCommandInfo(command,resolve);
			//append to stack. This should be an atomic operation
			self.currentCommandStack.singleCommandInfos.push(singleCommandInfo);

			if(null==self.execTimeout) {
				//var self = this;
				self.execTimeout = window.setTimeout(function() {
					self.DoSyncExec();
				},self.waitTime);
			}
		});
	};

	BufferingDomain.prototype.DoSyncExec = function() {
		var commandStack = this.currentCommandStack; //copy the current stack ...
		this.currentCommandStack = new CommandStack(); //... and reset it for the next commands 
		this.execTimeout = null; //delete timeout such that a new queue can be started
		//build the compound command
		var command = new jseoq.model.CompoundCommand();
		var nSingleCommands = commandStack.singleCommandInfos.length;
		var offset = 0;
		for(var i=0;i<nSingleCommands;i++) {
			var subcommand = commandStack.singleCommandInfos[i].command;
			var nSubcommands = 1;
			if (subcommand.type == jseoq.model.CommandTypesE.COMPOUND) {
				nSubcommands = subcommand.commands.length;
				for(var j=0;j<nSubcommands;j++) {
					command.commands.push(this.AdoptHistoryRefsCommand(subcommand.commands[j],offset));
				}
			} else {
				command.commands.push(this.AdoptHistoryRefsCommand(subcommand,offset));
			}
			commandStack.singleCommandInfos[i].len = nSubcommands;
			commandStack.singleCommandInfos[i].startIndex = offset;
			//offset+=nSubcommands;
			offset+=jseoq.CommandParser.CalcCommandHistoryLength(subcommand); //use function to take care of commands that do not add to history, i.e. UPDATE
		}
		this.domain.DoSync(command).then(function(result) {
			if(1==nSingleCommands) { //nothing to do, just forward the result
				commandStack.singleCommandInfos[0].resolve(result);
            } else { //if we go here, we need to decompose stacked results
                if(jseoq.ResultParser.IsResultOk(result)) {
                    for(var i=0;i<nSingleCommands;i++) {
                        var singleCommandInfo = commandStack.singleCommandInfos[i];
                        if(singleCommandInfo.len==1) { //individual command
                            singleCommandInfo.resolve(result.results[singleCommandInfo.startIndex]);
                        } else { //compound command
                            singleResult = new jseoq.model.CompoundResult();
                            for(var j=0;j<singleCommandInfo.len;j++) {
                                singleResult.results.push(result.results[singleCommandInfo.startIndex+j]);
                            }
                            singleCommandInfo.resolve(singleResult);
                        }
                    }
                } else { //else the failure case is more tricky because a decomposition is impossible so all stacked members get the same failure message
                    for(var i=0;i<nSingleCommands;i++) {
                        var singleCommandInfo = commandStack.singleCommandInfos[i];
                        singleCommandInfo.resolve(result);
                    } 
                }
			}
		});
    };

    BufferingDomain.prototype.AdoptHistoryRefsCommand = function(command,offset) {
        if(command.type == jseoq.model.CommandTypesE.COMPOUND) {
            for(var i=0;i<command.commands.length;i++) {
                this.AdoptHistoryRefsCommand(command.commands[i],offset);
            }
        } else if(command.type == jseoq.model.CommandTypesE.RETRIEVE) {
            this.AdoptHistoryRefsValue(command.target,offset);
        } else if(command.type == jseoq.model.CommandTypesE.UPDATE) {
            this.AdoptHistoryRefsValue(command.target,offset);
            this.AdoptHistoryRefsValue(command.value,offset);
        } else if(command.type == jseoq.model.CommandTypesE.CALL) {
            this.AdoptHistoryRefsValue(command.args,offset);
        } else if(command.type == jseoq.model.CommandTypesE.ASYNCCALL) {
            this.AdoptHistoryRefsValue(command.args,offset);
        }
        return command;
    };

    BufferingDomain.prototype.AdoptHistoryRefsValue = function(value,offset) {
        if(value.type == jseoq.model.ValueTypesE.LIST) {
            for(var i=0;i<value.v.length;i++) {
                this.AdoptHistoryRefsValue(value.v[i],offset);
            }
        } else if(value.type == jseoq.model.ValueTypesE.HISTORYREF) {
			if(value.v>=0) { //negative values need no adaptation
				value.v += offset;
			}
        }   
        return value;
    };
    
    BufferingDomain.prototype.SetLogger = function(logger) {
        this.domain.SetLogger(logger);
    };

    BufferingDomain.prototype.GetLogger = function() {
        return this.domain.GetLogger();
    };

	return BufferingDomain;
})();
