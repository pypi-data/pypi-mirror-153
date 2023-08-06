/*
*
* 2019 Bjoern Annighoefer
*/

var eoq2 = eoq2 || {};
eoq2.action = eoq2.action || {};

Object.assign(eoq2.action,(function() {

    var CallTypes = {
        SYN : 'SYN',
        ASY : 'ASY'
    };
    
    var CallStatus = {
        INI : 'INI', //initiated
        RUN : 'RUN', //running
        WAI : 'WAI', //waiting (e.g. for user input)
        ABO : 'ABO', //aborted
        ERR : 'ERR', //error
        FIN : 'FIN' //finished (sucesfully)
    };

    return {
        CallTypes : CallTypes,
        CallStatus : CallStatus
    };

})());