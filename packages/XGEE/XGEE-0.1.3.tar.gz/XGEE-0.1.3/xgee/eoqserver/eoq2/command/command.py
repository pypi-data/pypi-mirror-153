'''
 2019 Bjoern Annighoefer
'''

class CmdTypes:
    #data related commmands
    GET = 'GET' #get cmd
    SET = 'SET' #set cmd value
    ADD = 'ADD' #add cmd value
    REM = 'REM' #remove cmd value
    MOV = 'MOV' #move cmd cmd
    DEL = 'DEL' #delete cmd
    CLO = 'CLO' #clone source target mode
    CRT = 'CRT' #create by class
    CRN = 'CRN' #create by name
    QRF = 'QRF' #querify
    
    #comparison and merge
    CPR = 'CPR' #compare/diff
    MRG = 'MRG' #merge 
    
    #meta model related commands
    GMM = 'GMM' #get meta models
    RMM = 'RMM' #register meta model
    UMM = 'UMM' #unregister meta model
    
    #maintenance related commands
    HEL = 'HEL' #hello
    GBY = 'GBY' #goodbye
    SES = 'SES' #session
    STS = 'STS' #status
    CHG = 'CHG' #changes
    OBS = 'OBS' #observe
    UBS = 'UBS' #unobserve
    UDO = 'UDO' #undo
    RDO = 'RDO' #redo
    
    # Action related commands
    GAA = 'GAA' #get all actions
    CAL = 'CAL' #call
    ASC = 'ASC' #async Call
    ABC = 'ABC' #abort call
    CST = 'CST' #call status

    # Validation related commands
    ADC = "ADC"
    RMC = "RMC"
    VAL = "VAL"
    GAC = "GAC"
    
    CMP = 'CMP' #compound
    MUT = 'MUT' #mute stop outputing results history only
    UMT = 'UMT' #unmute start outputing results
    
    
class CloModes:
    CLS = 'CLS' #class: object only
    ATT = 'ATT' #attribute: class + attributes
    FLT = 'FLT' #deep: class + attributes + references
    DEP = 'DEP' #deep: classes + attributes + containments
    FUL = 'FUL' #full: classes + attributes + containments + reference adaptation

class MrgModes:
    STD = 'STD' #standard mode without additional information or output
    LST = 'LST' #list: creates a list with all commands
    LOG = 'LOG' #log: LST + creates a log file (info.log) with detailed information on every object
    DET = 'DET' #detailed: LOG + creates a file with all objects and their #1234 number

class Cmd:
    def __init__(self,t : str,args):
        self.cmd = t
        self.a = args
    def __repr__(self):
        cmdStr = str(self.cmd)
        if(type(self.a)==list and len(self.a) > 0):
            cmdStr += ' ' + ' '.join([str(arg) for arg in self.a])
        elif(self.a):
            cmdStr += ' ' + str(self.a)
        return cmdStr
        
class Get(Cmd):
    def __init__(self,target):
        super().__init__(CmdTypes.GET, target)
        
class Set(Cmd):
    def __init__(self,target,feature,value):
        super().__init__(CmdTypes.SET, [target,feature,value])
        
class Add(Cmd):
    def __init__(self,target,feature,value):
        super().__init__(CmdTypes.ADD, [target,feature,value])
        
class Rem(Cmd):
    def __init__(self,target,feature,value):
        super().__init__(CmdTypes.REM, [target,feature,value])
        
class Mov(Cmd):
    def __init__(self,target,newIndex):
        super().__init__(CmdTypes.MOV, [target,newIndex])
        
class Clo(Cmd):
    def __init__(self,target,original):
        super().__init__(CmdTypes.CLO,[target,original])
        
class Crt(Cmd):
    def __init__(self,clazz,n,constructorArgs=[]):
        super().__init__(CmdTypes.CRT,[clazz,n,constructorArgs])
        
class Crn(Cmd):
    def __init__(self,package,name,n,constructorArgs=[]):
        super().__init__(CmdTypes.CRN,[package,name,n,constructorArgs])
        
class Qrf(Cmd):
    def __init__(self,target):
        super().__init__(CmdTypes.QRF,target)
        
class Cpr(Cmd):
    def __init__(self,old,new,mode):
        super().__init__(CmdTypes.CPR,[old,new,mode])
        
class Mrg(Cmd):
    def __init__(self,old,new,mode):
        super().__init__(CmdTypes.MRG,[old,new,mode])

class Gmm(Cmd):
    def __init__(self):
        super().__init__(CmdTypes.GMM, None)
        
class Rmm(Cmd):
    def __init__(self,metamodel):
        super().__init__(CmdTypes.RMM, metamodel)
        
class Umm(Cmd):
    def __init__(self,metamodel):
        super().__init__(CmdTypes.UMM, metamodel)
        
class Hel(Cmd):
    def __init__(self,user,password):
        super().__init__(CmdTypes.HEL, [user, password])
        
class Ses(Cmd):
    def __init__(self,sessionId):
        super().__init__(CmdTypes.SES, sessionId)
        
class Gby(Cmd):
    def __init__(self,sessionId):
        super().__init__(CmdTypes.GBY, sessionId)
        
class Sts(Cmd):
    def __init__(self):
        super().__init__(CmdTypes.STS, None)
        
class Chg(Cmd):
    def __init__(self,latestChangeId,n):
        super().__init__(CmdTypes.CHG,[latestChangeId,n])
        
class Obs(Cmd):
    def __init__(self,eventType,eventKey):
        super().__init__(CmdTypes.OBS, [eventType,eventKey])
        
class Ubs(Cmd):
    def __init__(self,eventType,eventKey):
        super().__init__(CmdTypes.UBS, [eventType,eventKey])
        
class Gaa(Cmd):
    def __init__(self):
        super().__init__(CmdTypes.GAA,None)
        
class Cal(Cmd):
    def __init__(self,name,args=[],opts=[]):
        super().__init__(CmdTypes.CAL,[name,args,opts])
    
class Asc(Cmd):
    def __init__(self,name,args=[],opts=[]):
        super().__init__(CmdTypes.ASC,[name,args,opts])
        
class Abc(Cmd):
    def __init__(self,callId):
        super().__init__(CmdTypes.ABC,callId)

class Adc(Cmd):
    def __init__(self, constraintType, target, feature, law, name, annotation):
        super().__init__(CmdTypes.ADC,[constraintType, target, feature, law, name, annotation])

class Rmc(Cmd):
    def __init__(self, constraint):
        super().__init__(CmdTypes.RMC,constraint)

class Val(Cmd):
    def __init__(self, obj):
        super().__init__(CmdTypes.VAL, obj)

class Gac(Cmd):
    def __init__(self):
        super().__init__(CmdTypes.GAC, None)

class Mut(Cmd):
    def __init__(self):
        super().__init__(CmdTypes.MUT,None)
        
class Umt(Cmd):
    def __init__(self):
        super().__init__(CmdTypes.UMT,None)
        
class Cmp(Cmd):
    def __init__(self):
        super().__init__(CmdTypes.CMP,[])
        
    def Get(self,target):
        self.a.append(Get(target))
        return self
    
    def Set(self,target,feature,value):
        self.a.append(Set(target,feature,value))
        return self
    
    def Add(self,target,feature,value):
        self.a.append(Add(target,feature,value))
        return self
    
    def Rem(self,target,feature,value):
        self.a.append(Rem(target,feature,value))
        return self
    
    def Mov(self,target,newIndex):
        self.a.append(Mov(target,newIndex))
        return self
    
    def Clo(self,target,mode):
        self.a.append(Clo(target,mode))
        return self
    
    def Crt(self,clazz,n,constructorArgs=[]):
        self.a.append(Crt(clazz,n,constructorArgs))
        return self
    
    def Crn(self,package,name,n,constructorArgs=[]):
        self.a.append(Crn(package,name,n,constructorArgs))
        return self
    
    def Qrf(self,target):
        self.a.append(Qrf(target))
        return self
    
    def Mrg(self,old,new,mode):
        self.a.append(Mrg(old,new,mode))
        return self

    def Cpr(self,old,new,mode):
        self.a.append(Cpr(old,new,mode))
        return self
    
    def Gmm(self):
        self.a.append(Gmm())
        return self
    
    def Rmm(self,metamodel):
        self.a.append(Rmm(metamodel))
        return self
    
    def Umm(self,metamodel):
        self.a.append(Umm(metamodel))
        return self
    
    def Hel(self,user,password):
        self.a.append(Hel(user,password))
        return self
    
    def Ses(self,sessionId):
        self.a.append(Ses(sessionId))
        return self
    
    def Gby(self,sessionId):
        self.a.append(Gby(sessionId))
        return self
    
    def Sts(self):
        self.a.append(Sts())
        return self
    
    def Chg(self,changeId,n):
        self.a.append(Chg(changeId,n))
        return self
    
    def Obs(self,eventType,eventKey):
        self.a.append(Obs(eventType,eventKey))
        return self
    
    def Ubs(self,eventType,eventKey):
        self.a.append(Ubs(eventType,eventKey))
        return self
    
    def Gaa(self):
        self.a.append(Gaa())
        return self
    
    def Cal(self,name,args=[],opts=[]):
        self.a.append(Cal(name,args,opts))
        return self
    
    def Asc(self,name,args=[],opts=[]):
        self.a.append(Asc(name,args,opts))
        return self
    
    def Abc(self,callId):
        self.a.append(Abc(callId))
        return self

    def Adc(self,constraintType, target, feature, law, name, annotation):
        self.a.append(Adc(constraintType, target, feature, law, name, annotation))
        return self

    def Rmc(self,constraint):
        self.a.append(Rmc(constraint))
        return self

    def Val(self,obj):
        self.a.append(Val(obj))
        return self

    def Gac(self):
        self.a.append(Gac())
        return self
    
    def Mut(self):
        self.a.append(Mut())
        return self
    
    def Umt(self):
        self.a.append(Umt())
        return self
