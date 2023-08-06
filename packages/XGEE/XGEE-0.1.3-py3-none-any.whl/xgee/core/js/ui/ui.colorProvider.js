//  ColorProvider
//  Provides colors to tokens devided into namespaces and compared using a supplied token comparision function.
//  (C) 2019 Matthias Brunner

var colorProviders=[];

var ColorProvider=function(namespace,compareTokens)
{
    var self=this;
    //main colors of CYM(K)
    this.colorWheel=["00FFFF","0080FF","0000FF","8000FF","FF00FF","FF0080","FF0000","FF8000","FFFF00","80FF00","00FF00","00FF80"];
    this.colorWheelPos=0;
    this.knownTokens=[];
    this.namespace=namespace;
    this.compareTokens=compareTokens;
    this.getColor=function(token)
    {
        //check if token already has been given a color
        for(let i in self.knownTokens)
        {
            if(self.compareTokens(self.knownTokens[i].token,token))
            {
                return self.knownTokens[i].color;
            }
        }

        //token does not exist
        let newToken={token:token,color:self.colorWheel[self.colorWheelPos]};
        self.knownTokens.push(newToken);
        self.colorWheelPos+=1;
        if(self.colorWheelPos==self.colorWheel.length)
        {
            //color wheel wrap around
            self.colorWheelPos=0;
        }
        return newToken.color;
    };
    
    colorProviders.push(this);
}

function getColorProvider(namespace)
{
    for(let i in colorProviders)
    {
        if(colorProviders[i].namespace==namespace)
        {
            return colorProviders[i];
        }
    }
}