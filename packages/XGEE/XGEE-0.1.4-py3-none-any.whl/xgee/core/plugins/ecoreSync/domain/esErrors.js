

export class UnknownObject extends Error{
    constructor(...args){
        super(...args)
        this.name='UnknownObject'
        //Error.captureStackTrace(this, UnknownObject)
    }
}

export class NoSuchFeature extends Error{
    constructor(...args){
        super(...args)
        this.name='NoSuchFeature'
        //Error.captureStackTrace(this, NoSuchFeature)
    }
}