import { Mutex } from '../../lib/libaux.js'

export default class TransactionObject{
    constructor(){
        //Mutex used for managing transactions on the graph object 
        this.mutex=new Mutex()
    }

    initializer(){
        //Mutex used for managing transactions on the graph object 
        this.mutex=new Mutex()
    }  

    async startTransaction(){
        var token=await this.mutex.lock()
        return token
    }

    async endTransaction(token){       
        var res=this.mutex.release(token)
        return res
    }

}