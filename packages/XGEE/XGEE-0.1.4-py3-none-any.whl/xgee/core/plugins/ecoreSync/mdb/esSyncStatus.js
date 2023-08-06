export default class ESSyncStatus{
    constructor(ecoreSync,eObject){
        this.ecoreSync=ecoreSync;
        this._initializedFeatures=new Set();
        this._eObject=eObject;        
    }

    setInitialized(...args)
    {
        //marks the supplied features as initialized
        var self=this;
        args.forEach(function(e){
            if((typeof e)=='string')
            {
                self._initializedFeatures.add(e);
            }
        });
    }

    isInitialized(...args)
    {
        var res=null;
        var self=this;
        if(args.length)
        {
            if(args.length==1)
            {
                res=self._initializedFeatures.has(args[0]);
            }
            else
            {
                res=args.map(function(e){
                    return self._initializedFeatures.has(e);
                }).reduce((p,c) => { return p && c }, true);
            }
        }
        return res;
    }



    isDangling(){
        //returns true if the eObject is not contained within another eObject
        var res=true;
        if(this._eObject.eContainer)
        {
            res=false;
        }
        return res;
    }

    hasInitializedFeatures(){
        return this._initializedFeatures.length > 0
    }

    getInitializedFeatures(){
        return Array.from(this._initializedFeatures);
    }


    getObject(){
        return this._eObject;
    }

    toConsole(){
        console.error('ECORESYNC STATUS OF #'+this.ecoreSync.rlookup(this._eObject))
        console.error('-------------------------------------------------')
        console.error('isDangling: '+this.isDangling())
        let features=this.getInitializedFeatures()
        console.error('features: '+features.join(','))
        console.error('-------------------------------------------------')
    }
}