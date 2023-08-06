/*
*
* 2019 Bjoern Annighoefer
*/

var jseoq2 = jseoq2 || {};
eoq2.domain = eoq2.domain || {};
eoq2.domain.remote = eoq2.domain.remote || {};

Object.assign(eoq2.domain.remote,(function(){

    /*
    * HttpPostDomain
    */

    function HttpPostDomain(params) {
        Domain.call(this);
        this.url = 'http://localhost:8000/eoq.do';
        this.timeout = 0; //no timeout

        if(params.hasOwnProperty('url')) {
            this.url = params.url;
        } 
        if(params.hasOwnProperty('timeout')) {
            this.timeout = params.timeout;
        } 
        if(params.hasOwnProperty('logger')) {
            this.SetLogger(params.logger);
        } else {
            this.SetLogger(new DefaultDomainLogger());
        }
        return this;
    };
    HttpPostDomain.prototype = Object.create(eoq2.domain.Domain.prototype);

    HttpPostDomain.prototype.Do = function(cmd) {
        let startTime = new Date();
        this.logger.LogBegin(cmd);
        let self = this; //save the this pointer to access it within the callbacks
        return new Promise(function(resolve,reject) {
            let xhttp = new XMLHttpRequest();
            xhttp.onreadystatechange = function() {
                if (this.readyState == 4) {
                    let res = null
                    if(this.status == 200) {
                        res = JSON.parse(this.responseText);
                        let endTime = new Date();
                        self.logger.LogEnd(res,endTime-startTime);
                    } else {
                        let endTime = new Date();
                        let msg = 'ERROR ('+this.status+'): '+this.statusText;
                        res = new eoq2.Res(cmd.cmd,eoq2.ResTypes.ERR,msg);
                        self.logger.LogEnd(res,endTime-startTime);
                        
                    }
                    resolve(res);
                }
            };
            xhttp.open("POST", self.url, true);
            xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
            xhttp.send("command="+JSON.stringify(cmd)); 
        });
    };

    return {
        HttpPostDomain : HttpPostDomain
    };
})());