var jseoq = jseoq || {};
jseoq.domains = jseoq.domains || {};

jseoq.domains.HttpPostDomain = (function() {
	//PRIVATE CLASSES
	function DefaultDomainLogger() {
		this.LogBegin = function(commandStr) {
			console.log('jseoq: Command: '+commandStr);
		}
		this.LogEnd = function(resultStr,timeEllapsed) {
			console.log('jseoq: Result: '+resultStr+' --> '+timeEllapsed+' ms ellapsed')
		}
	};

	function DefaultObjectCacheListener() {
		this.OnChange = function(objectList) {
			nObjects = objectList.length;
			console.log('jseoq: Object cache changed: '+nObjects+' in cache');
		};
	};

	//PUBLIC CLASS
	function HttpPostDomain(params) {
		jseoq.domains.Domain.call(this);
		this._url = 'http://localhost:8000/eoq.do';
		this._timeout = 0; //no timeout

		if(params.hasOwnProperty('url')) {
			this._url = params.url;
		} 
		if(params.hasOwnProperty('timeout')) {
			this._timeout = params.timeout;
		} 
		if(params.hasOwnProperty('logger')) {
			this.SetLogger(params.logger);
		} else {
			this.SetLogger(new DefaultDomainLogger());
		}
		if(params.hasOwnProperty('cachListener')) {
			this._cacheListener = params.cachListener;
		} else {
			this._cacheListener = new DefaultObjectCacheListener();
		} 
		
		return this;
	};

	HttpPostDomain.prototype = Object.create(jseoq.domains.Domain.prototype);

	HttpPostDomain.prototype.Do = function(command,successCallback,failCallback) {
		var self = this;
		this.DoSync(command).then(function(result) {
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
	
	HttpPostDomain.prototype.DoSync = function(command) {
		var startTime = new Date();
		var commandStr = jseoq.CommandParser.CommandToString(command);
		this._logger.LogBegin(commandStr);
		var thisDomain = this; //save the this pointer to access it within the callbacks
		return new Promise(function(resolve,reject) {
			var xhttp = new XMLHttpRequest();
			xhttp.onreadystatechange = function() {
				if (this.readyState == 4) {
					if(this.status == 200) {
						//var data = decodeURIComponent(this.responseText);
						var data = this.responseText;
						var endTime = new Date();
						thisDomain._logger.LogEnd(data,endTime-startTime);
						var result = new jseoq.model.ErrorResult();
						result.message = 'UNKNOWN ERROR';
						try {
							result = jseoq.ResultParser.StringToResult(data);
						} catch(e) {
							console.log(e.stack);
							result.message = e.toString();
						}
					} else {
						var endTime = new Date();
						var msg = 'ERROR ('+this.status+'): '+this.statusText;
						thisDomain._logger.LogEnd(msg,endTime-startTime);
						var result = new jseoq.model.ErrorResult();
						result.message = msg;
					}
					resolve(result);
				}
			};
			xhttp.open("POST", thisDomain._url, true);
			xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
			xhttp.send("command="+encodeURIComponent(commandStr)); 
		});
	};
	
	HttpPostDomain.prototype.ResultToJs = function(result) {
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

	return HttpPostDomain;
})();


