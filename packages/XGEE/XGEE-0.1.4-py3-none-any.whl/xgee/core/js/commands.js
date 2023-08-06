function ESetCommand(ecoreSync,eObject,featureName,value) {
    jsa.CommandA.call(this);

    this.ecoreSync = ecoreSync;
    this.eObject = eObject;//eObject.isProxy?eObject.noproxy:eObject;
    this.featureName = featureName;
    this.newValue = (value&&value.isProxy)?value.noproxy:value;
    this.oldValue = null;

    this.name = 'Set '+featureName;// + ' to ' + value.toString();
    this.description = 'Changes the value of the feature '; //TODO: customize the description by saying which object was set to shich value
};

ESetCommand.prototype = Object.create(jsa.CommandA.prototype);

ESetCommand.prototype.Do = function() {
    let oldValue = this.eObject.get(this.featureName);
    this.oldValue = (oldValue&&oldValue.isProxy)?oldValue.noproxy:oldValue; //TODO: still necessary?
    //this.eObject.set(this.featureName,this.newValue);
    if(null==this.newValue) {
        this.ecoreSync.unset(this.eObject,this.featureName);
    } else {
        this.ecoreSync.set(this.eObject,this.featureName,this.newValue);
    }

    return this;
};

ESetCommand.prototype.Undo = function() {
    //this.eObject.set(this.featureName,this.oldValue);
    if(null==this.oldValue) {
        this.ecoreSync.unset(this.eObject,this.featureName);
    } else {
        this.ecoreSync.set(this.eObject,this.featureName,this.oldValue);
    }
    this.oldValue = null;

    return this;
};


function ERemoveCommand(ecoreSync,eObject,featureName,value) {
    jsa.CommandA.call(this);

    this.ecoreSync = ecoreSync;
    this.eObject = eObject;//eObject.isProxy?eObject.noproxy:eObject;
    this.featureName = featureName;
    this.valueToRemove = (value&&value.isProxy)?value.noproxy:value;
    this.oldIndex = null; //TODO: remember index of object

    this.name = 'Remove from '+featureName;// + ' to ' + value.toString();
    this.description = 'Removes a value from a feature.'; //TODO: customize the description by saying which object was set to shich value
};

ERemoveCommand.prototype = Object.create(jsa.CommandA.prototype);

ERemoveCommand.prototype.Do = function() {
    //TODO: get index
    this.ecoreSync.remove(this.eObject,this.featureName,this.valueToRemove);

    return this;
};

ERemoveCommand.prototype.Undo = function() {
    //TODO: restore index
    this.ecoreSync.add(this.eObject,this.featureName,this.valueToRemove);

    return this;
};




/* UpdateReferenceCommand */
function UpdateReferenceCommand(ecoreSync,eObject,featureName,value) {
    jsa.CommandA.call(this);

    this.ecoreSync = ecoreSync;
    this.eObject = eObject;
    this.featureName = featureName;
    this.newValue = value;
    this.oldValue = []; //is initialized later 

    this.name = 'Set '+featureName + ' to ' + value.length + 'new objects.';
    this.description = 'Changes the value of a reference feature with multiplicity > 1'; //TODO: customize the description by saying which object was set to shich value
};

UpdateReferenceCommand.prototype = Object.create(jsa.CommandA.prototype);

UpdateReferenceCommand.prototype.Do = function() {
    let self = this;
    return new Promise(function(resolve,reject) {
        self.ecoreSync.get(self.eObject,self.featureName).then(function(reference) {
            self.oldValue = reference;
            let removePromises = [];
            for(let i=0; i<self.oldValue.length; i++) {
                let v = self.oldValue[i];
                removePromises.push(self.ecoreSync.remove(self.eObject,self.featureName,v.isProxy?v.noproxy:v));
            }
            Promise.all(removePromises).then(function(unused) {
                let addPromises = [];
                for(let j=0; j<self.newValue.length; j++) {
                    let v = self.newValue[j];
                    addPromises.push(self.ecoreSync.add(self.eObject,self.featureName,v.isProxy?v.noproxy:v));
                }
                Promise.all(addPromises).then(function(unused) {
                    resolve(self);
                });
            }); 
        });
    });
};

UpdateReferenceCommand.prototype.Undo = function() {
    return new Promise(function(resolve,reject) {
        self.ecoreSync.get(self.eObject,self.featureName).then(function(reference) {
            self.oldValue = reference;
            let removePromises = [];
            for(let i=0; i<self.newValue.length; i++) {
                let v = self.newValue[i];
                removePromises.push(self.ecoreSync.remove(self.eObject,this.featureName,v.isProxy?v.noproxy:v));
            }
            Promises.all(removePromises).then(function(unused) {
                let addPromises = [];
                for(let j=0; j<self.oldValue.length; j++) {
                    let v = self.oldValue[j];
                    addPromises.push(self.ecoreSync.add(self.eObject,self.featureName,v.isProxy?v.noproxy:v));
                }
                Promises.all(addPromises).then(function(unused) {
                    self.oldValue = [];
                    resolve(self);
                });
            }); 
        });
    });
};
