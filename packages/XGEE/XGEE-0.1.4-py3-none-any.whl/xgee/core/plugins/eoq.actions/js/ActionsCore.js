// 2020 Bjoern Annighoefer

var ACTIONS = ACTIONS || {};

String.prototype.insertArray = function (findDict, startCharacter = "", endCharacter = "") {
    let replaceString = this;
    for (let key in findDict) {
        replaceString = replaceString.replace(startCharacter + key + endCharacter, findDict[key] + ' ' + startCharacter + key + endCharacter);
    }
    return replaceString;
};

Object.assign(ACTIONS, (function () {
    /* BA: Fetch actions might be removed later if loading becomes part of a common domain*/
    function FetchActions(domain) {
        return new Promise(function (resolve, reject) {
            let cmd = new eoq2.Gaa();
            domain.Do(cmd).then(function (val) {
                try {
                    let actions = [];
                    let nActions = val.length;
                    for (let i = 0; i < nActions; i++) {
                        let actionInfo = val[i];
                        let actionSegments = actionInfo[0].split("/");
                        let nSegments = actionSegments.length;
                        let actionName = actionSegments[nSegments - 1];
                        let categories = actionSegments.slice(0, nSegments - 1);
                        actions.push({
                            id: actionInfo[0],
                            name: actionName,
                            categories: categories,
                            description: actionInfo[3],
                            parameters: [],
                            results: [],
                            tags: actionInfo[4],
                        });
                        let argsInfos = actionInfo[1];
                        let nParameters = argsInfos.length;
                        for (let j = 0; j < nParameters; j++) {
                            let argsInfo = argsInfos[j];
                            actions[i].parameters.push({
                                name: argsInfo[0],
                                type: argsInfo[1],
                                upperBound: argsInfo[2],
                                lowerBound: argsInfo[3],
                                default: argsInfo[4],
                                description: argsInfo[5],
                                choices: []
                            });
                            let choicesInfos = argsInfo[6];
                            let nChoices = choicesInfos.length;
                            for (let k = 0; k < nChoices; k++) {
                                let choicesInfo = choicesInfos[k];
                                actions[i].parameters[j].choices.push({
                                    value: choicesInfo[0],
                                    description: choicesInfo[1]
                                });
                            }
                        }
                        let resultInfos = actionInfo[1];
                        let nResultParameters = resultInfos.length;
                        for (let j = 0; j < nResultParameters; j++) {
                            let resultInfo = resultInfos[j];
                            actions[i].results.push({
                                name: resultInfo[0],
                                type: resultInfo[1],
                                upperBound: resultInfo[2],
                                lowerBound: resultInfo[3],
                                description: resultInfo[4],
                                default: resultInfo[5]
                            });
                        }
                        resolve(actions);
                    }
                } catch (e) {
                    reject(new Error("Failed to retrieve action list:" + e.toString()));
                }
            });
        });
    };


    function ActionRunner(params) {
        this.domain = null;
        this.actionName = '';
        this.args = []; //no arguments by default
        this.refreshRate = 100; //ms
        this.data = null; //to be used in callbacks
        this.onFailedCallback = function (info) {
        };
        this.onStatusUpdateCallback = function (statusInfo) {
        };
        this.onRunCallback = function (info) {
        };
        this.onFinishedCallback = function (info) {
        };
        this.onAbortedCallback = function (info) {
        };
        this.onResultCallback = function (res) {
        };

        //initialized later
        this.callEventCallback = null;
        this.statusInfo = null;
        this.processStatus = {
            currentTask: 0,
            numTasks: 0,
            taskPercentage: 0,
            totalPercentage: 0,
            taskStack: [],
        }
        this.streamBuffer = "";

        //Copy params
        jsa.CopyParams(this, params)

        //internals
        this.callId = -1;
        this.pullTimout = null;

        return this;
    }

    ActionRunner.prototype.Run = function () { //starts the action execution
        //initialize the status
        this.statusInfo = {
            status: eoq2.action.CallStatus.INI, // TODO: is being overridden later on!
            output: "",
            progress: 0,
//            status : ""
        };
        this.processStatus.numTasks= 0;

        //register for any changes on actions befor running it
        let self = this;
        this.callEventCallback = function (evts, src) {
            self.OnCallEvent(evts, src);
        }

        this.domain.Observe(this.callEventCallback, [eoq2.event.EvtTypes.OUP, eoq2.event.EvtTypes.CST, eoq2.event.EvtTypes.CVA]);

        let cmd = new CMD.Cmp().Asc(this.actionName, this.args, ['autoobserve', true])//args are already an array

        this.domain.Do(cmd).then(function (val) {
            self.callId = val[0];
        }).catch(function (e) {
            self.onFailedCallback(e);
        });
    };

    ActionRunner.prototype.UnobserveCall = function () {

        this.domain.Unobserve(this.callEventCallback);
    };

    ActionRunner.prototype.__ParseActionOutput = function (newData) {
        let data = "";
        this.streamBuffer += newData;
        if (!this.streamBuffer.includes("\n"))
            return "";
        else {
            data = this.streamBuffer.substring(0, this.streamBuffer.indexOf("\n"));
            this.streamBuffer = this.streamBuffer.substring(this.streamBuffer.indexOf("\n") + 1);
        }
        if (data.includes("Started Task")) {
            this.processStatus.currentTask++;
            this.processStatus.taskPercentage = 0;
            if (this.processStatus.numTasks < this.processStatus.currentTask) {
                this.processStatus.numTasks = this.processStatus.currentTask;
            }
            const regex = /\[Started Task]\s*(.*)/gm;
            let m;
            while ((m = regex.exec(data)) !== null) {
                if (m.index === regex.lastIndex) {
                    regex.lastIndex++;
                }
                m.forEach((match, groupIndex) => {
                    if (groupIndex === 1) {
                        this.processStatus.currentTaskName = match;
                        this.statusInfo.callStatusStr = match;
                        this.processStatus.taskStack.append(match);

                    }
                });
            }
        } else if (data.includes("Ended Task")) {
            this.processStatus.taskPercentage = 100.;
            this.processStatus.taskStack.pop();
            this.statusInfo.callStatusStr = "Completed.";

        } else if (data.includes("Announced Tasks")) {
            const regex = /\[Announced Tasks]\s*(\d+)/gm;
            let m;
            while ((m = regex.exec(data)) !== null) {
                if (m.index === regex.lastIndex) {
                    regex.lastIndex++;
                }
                m.forEach((match, groupIndex) => {
                    if (groupIndex === 1) {
                        this.processStatus.numTasks += Number.parseInt(match);
                        console.log("added task number " + this.processStatus.numTasks);
                    }
                });
            }
        }
        if (!this.__FindProgressFromText(data)) {
            return this.__StyleActionOutput(data);
        } else {
            return "";
        }
    }
    ActionRunner.prototype.__CalculateProgress = function () {
        if (0 === this.processStatus.numTasks) { // no tasks announced, assuming legacy action
            return this.processStatus.taskPercentage;
        } else {
            return Math.ceil(((this.processStatus.currentTask - 1) / this.processStatus.numTasks) * 100. + this.processStatus.taskPercentage / this.processStatus.numTasks);
        }
    }

    ActionRunner.prototype.__StyleActionOutput = function (data) {
        let classes = "";
        if (data.includes("WARNING")) {
            classes = "action-warning";
        } else if (data.includes("FAILED")) {
            classes = "action-error";
        } else if (data.includes("SUCCESS")) {
            classes = "action-success";
        } else if (data.includes("INFO")) {
            classes = "action-info";
        } else if (data.includes("Started Task")) {
            classes = "action-info";
        }
        data = '<div class="' + classes + '">' + data + '</div>';
        let replacements = {
            'SAVED': '<i class="fas fa-save" title="SAVED"></i>',
            'DELETED': '<i class="fas fa-trash" title="DELETED"></i>',
            'CHANGED': '<i class="fas fa-edit" title="CHANGED"></i>',
            'CREATED': '<i class="fas fa-plus-square" title="CREATED"></i>',
            'SUCCESS': '<i class="fas fa-check-circle" title="SUCCESS"></i>',
            'FAILED': '<i class="fas fa-times-octagon" title="FAILED"></i>',
            'WARNING': '<i class="fas fa-exclamation-triangle" title="WARNING"></i>',
            'INFO': '<i class="fas fa-info-circle" title="INFO"></i>',
            'FOUND': '<i class="fas fa-search" title="FOUND"></i>',
        }
        return data.insertArray(replacements, "[", "]");
    }

    ActionRunner.prototype.__HandleCallOutput = function (evt) {
        let channel = evt.a[1];
        let data = evt.a[2];

        if (channel === "STDOUT") { // TODO: check that this if statement compares against STDOUT

            this.statusInfo.output += this.__ParseActionOutput(data);
            this.statusInfo.progress = this.__CalculateProgress();
        }
        this.onStatusUpdateCallback(this.statusInfo);
    }

    ActionRunner.prototype.OnCallEvent = function (evts, src) {
        for (let i = 0; i < evts.length; i++) {
            let evt = evts[i];
            let callId = evt.a[0]; //all registered event types have the call id in the first position
            if (callId == this.callId) { //only process events for the own call
                switch (evt.evt) {
                    case eoq2.event.EvtTypes.OUP:
                        this.__HandleCallOutput(evt);
                        break;
                    case eoq2.event.EvtTypes.CST: {
                        let status = evt.a[1];
                        let info = evt.a[2];

                        this.statusInfo.status = status;
                        this.onStatusUpdateCallback(this.statusInfo);

                        switch (status) {
                            case eoq2.action.CallStatus.RUN:
                                this.onRunCallback(info);
                                break;
                            case eoq2.action.CallStatus.FIN:
                                //stop listening to events
                                this.UnobserveCall();
                                this.onFinishedCallback(info);
                                break;
                            case eoq2.action.CallStatus.ABO:
                                this.UnobserveCall();
                                this.onAbortedCallback(info);
                                break;
                            case eoq2.action.CallStatus.ERR:
                                this.UnobserveCall();
                                this.onFailedCallback(info);
                                break;
                            default:
                                break; //nothing
                        }
                    }
                        break;
                    case eoq2.event.EvtTypes.CVA: {
                        let res = evt.a[1];
                        this.onResultCallback(res);
                    }
                        break;
                }
            }
        }
    }

    ActionRunner.prototype.__FindProgressFromText = function (text) {
        let progressStrs = text.match(/\s\d+\%/g);
        if (progressStrs) {
            let progressStr = progressStrs[progressStrs.length - 1]; //last element
            let progressNumberStr = progressStr.substring(1, progressStr.length - 1); //ommit the trailing %
            this.processStatus.taskPercentage = Number.parseInt(progressNumberStr);
            return true;
        }
        return false;
    }

    ActionRunner.prototype.Abort = function () {
        //var cmd = jseoq.CommandParser.StringToCommand("ABORTCALL "+this.callId);
        let cmd = new eoq2.Abc(this.callId);
        let self = this;
        this.domain.RawDo(cmd).then(function (res) {
            let val = eoq2.ResGetValue(res); //val is not used, but ResGetVal triggeres exception if cmd failed
            ;//nothing more to do the progress task will to the rest.
        }).catch(function (e) {
            self.onFailedCallback(e);
            throw e; //abort failed
        });
        return this;
    };


    return {
        FetchActions: FetchActions,
        ActionRunner: ActionRunner
    };

})());