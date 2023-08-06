// UUID Library
// (C) 2020 Matthias Brunner

class UUIDv4{
    constructor(){
        this._value=new Uint8Array(16);
        this._strVal=null;
        crypto.getRandomValues(this._value);
        this._value[6] = ( this._value[6] & 0b00001111 ) | 0b01000000 //4 MSB == 0100
        this._value[8] = (this._value[8] & 0b00111111) | 0b10000000; //2 MSB == 10
    }

    toString(){
        var str='';
        if(this._strVal==null)
        {
           
            this._value.forEach(function(val){
                str+=('00'+val.toString(16)).substr(-2);
            })
            const layout=[8,4,4,4];
            layout.forEach(function(pos,i){    
                let offset=pos;
                if(i>0) offset=layout.slice(0,i+1).reduce(function(p,c){ return p+c},0)+i             
                str=str.substr(0,offset)+'-'+str.substr(offset)
            })
            this._strVal=str;
        }
        else
        {
            str=this._strVal;
        }
        return str;
    }

    equals(other){
        return this.toString()==other.toString()
    }

}

class UUIDLib{
    constructor(){
        this.v4=UUIDv4
    }
}

const UUID=new UUIDLib();

export default UUID;