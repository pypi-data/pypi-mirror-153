

'''
 Legacy support for old jseoq commands
 2019 Bjoern Annighoefer
'''

from ..util import EoqError
from ..command.command import CmdTypes,Cmd,Cal,Asc,CloModes
from ..command.result import ResTypes
from ..query.query import QrySegTypes,Qry,Seg


#import legacy stuff
from eoq1.model import CommandTypesE, ResultTypesE, ValueTypesE, SegmentTypesE, IndexTypesE, OperatorTypesE, ErrorResult, CompoundResult, HelloResult, GoodbyeResult, SessionResult, StatusResult, ChangesResult, RetrieveResult, UpdateResult, CreateResult, CloneResult, CallResult, AsyncCallResult, AbortCallResult, CallStatusResult, CloneModesE


def UpgradeCmd(legacyCmd):
    cloModeConversion = {}
    cloModeConversion[CloneModesE.CLASS] = CloModes.CLS
    cloModeConversion[CloneModesE.ATTRIBUTES] = CloModes.ATT
    cloModeConversion[CloneModesE.DEEP] = CloModes.DEP
    cloModeConversion[CloneModesE.FULL] = CloModes.FUL
    
 
    
    cmd = None
    if(legacyCmd.type == CommandTypesE.HELLO):
        cmd = Cmd(CmdTypes.HEL,[UpgradeVal(legacyCmd.user),UpgradeVal(legacyCmd.identification)])
    elif(legacyCmd.type == CommandTypesE.GOODBYE):
        cmd = Cmd(CmdTypes.GBY,[UpgradeVal(legacyCmd.sessionId)])
    elif(legacyCmd.type == CommandTypesE.SESSION):
        cmd = Cmd(CmdTypes.SES,[UpgradeVal(legacyCmd.sessionId)])
    elif(legacyCmd.type == CommandTypesE.STATUS):
        cmd = Cmd(CmdTypes.STS,[])
    elif(legacyCmd.type == CommandTypesE.CHANGES):
        cmd = Cmd(CmdTypes.CHG,[UpgradeVal(legacyCmd.earliestChangeId),0])
    elif(legacyCmd.type == CommandTypesE.RETRIEVE):
        cmd = Cmd(CmdTypes.GET,UpgradeQry(legacyCmd.target,legacyCmd.query))
    elif(legacyCmd.type == CommandTypesE.CREATE):
        cmd = Cmd(CmdTypes.CRN,[UpgradeVal(legacyCmd.packageNsUri),UpgradeVal(legacyCmd.className),UpgradeVal(legacyCmd.n)])
    elif(legacyCmd.type == CommandTypesE.UPDATE):
        cmd = Cmd(CmdTypes.SET,[UpgradeQry(legacyCmd.target,legacyCmd.query),UpgradeVal(legacyCmd.value)])
        #cmd = Cmd(CmdTypes.ADD,[legacyCmd.target,legacyCmd.value])
        #cmd = Cmd(CmdTypes.REM,[legacyCmd.target,legacyCmd.value])
    elif(legacyCmd.type == CommandTypesE.CLONE):
        cmd = Cmd(CmdTypes.CLO,[UpgradeVal(legacyCmd.target),cloModeConversion[legacyCmd.mode]])
    elif(legacyCmd.type == CommandTypesE.CALL):
        cmd = Cal(UpgradeVal(legacyCmd.action),UpgradeVal(legacyCmd.args))
    elif(legacyCmd.type == CommandTypesE.ASYNCCALL):
        cmd = Asc(UpgradeVal(legacyCmd.action),UpgradeVal(legacyCmd.args))
    elif(legacyCmd.type == CommandTypesE.CALLSTATUS):
        cmd = Cmd(CmdTypes.GBY,[UpgradeVal(legacyCmd.callId)])
    elif(legacyCmd.type == CommandTypesE.ABORTCALL):
        cmd = Cmd(CmdTypes.GBY,[UpgradeVal(legacyCmd.callId)])
    elif(legacyCmd.type == CommandTypesE.COMPOUND):
        subcommands = []
        for lsc in legacyCmd.commands:
            sc = UpgradeCmd(lsc) 
            subcommands.append(sc)
        
        cmd = Cmd(CmdTypes.CMP,subcommands)
    else:
        raise EoqError(0,'Unknown command type: '+legacyCmd.type)
    return cmd


def UpgradeQry(target,legacyQry):
    root = UpgradeVal(target)
    qry = Qry(root)
    for ls in legacyQry.segments:
        if(ls.type == SegmentTypesE.PATH):
            name = ls.identifier
            qry.Pth(name)
        elif(ls.type == SegmentTypesE.CLAZZ):
            name = ls.identifier
            qry.Cls(name)
        elif(ls.type == SegmentTypesE.INSTANCE):
            name = ls.identifier
            qry.Ino(name)
        elif(ls.type == SegmentTypesE.META):
            name = ls.identifier
            qry.Met(name)
        else:
            raise EoqError(0,"Unknown segment type: "+ls.type)
        

        #consider selectors 
        if(ls.selector):
            selector = ls.selector
            subqry = Qry()
            subqry.Pth(selector.name)
            if(selector.operator.type == OperatorTypesE.EQUAL):
                    subqry.Equ(UpgradeVal(selector.value))
            elif(selector.operator.type == OperatorTypesE.NOTEQUAL):
                    subqry.Neq(UpgradeVal(selector.value))
            elif(selector.operator.type == OperatorTypesE.GREATER):
                    subqry.Gre(UpgradeVal(selector.value))
            elif(selector.operator.type == OperatorTypesE.LESS):
                    subqry.Les(UpgradeVal(selector.value))
            else:
                raise EoqError(0,"Unknown operator in selector: %s"%(selector.operator))
            
            qry.Sel(subqry)
        

        #consider index
        if(ls.index):
            index = ls.index
            if(index.type == IndexTypesE.NUMBER):
                qry.Idx(index.value)
            else:
                raise EoqError(0,"Legacy conversion does not support index type: %s"%(index.type))
    return qry


def UpgradeVal(legacyVal):
    qry = None
    if(legacyVal.type == ValueTypesE.LIST):
        subqrys = []
        for sv in legacyVal.v:
            sq = UpgradeVal(sv)
            subqrys.append(sq)
        
        #qry = Seg(QrySegTypes.ARR,subqrys)
        qry = subqrys #is that translation correct?
    elif(legacyVal.type == ValueTypesE.INT):
        qry = legacyVal.v
    elif(legacyVal.type == ValueTypesE.FLOAT):
        qry = legacyVal.v
    elif(legacyVal.type == ValueTypesE.BOOL):
        qry = legacyVal.v
    elif(legacyVal.type == ValueTypesE.STRING):
        qry = legacyVal.v
    elif(legacyVal.type == ValueTypesE.OBJECTREF):
        qry = Seg(QrySegTypes.OBJ,legacyVal.v)
    elif(legacyVal.type == ValueTypesE.EMPTY):
        qry = None
    elif(legacyVal.type == ValueTypesE.HISTORYREF):
        qry = Seg(QrySegTypes.HIS,legacyVal.v)
    else:
        raise EoqError(0,"Unknown value type: %s"%(legacyVal.type))
    return qry


def DowngradeRes(res):
    legacyRes = None
    if(res.res == CmdTypes.CMP):
        legacyRes = CompoundResult()
        if(res.s == ResTypes.ERR):
            legacyRes.type = ResultTypesE.COMPOUND_ERROR #if a single command failed the full compound command is failed.
        else:
            for subresult in res.v:
                lsr = DowngradeRes(subresult)
                legacyRes.results.append(lsr)
        
    else: # single commands
        if(res.res == CmdTypes.HEL):
            legacyRes = HelloResult()
            legacyRes.sessionId = res.v
        elif(res.res == CmdTypes.GBY):
            legacyRes = GoodbyeResult()
        elif(res.res == CmdTypes.SES):
            legacyRes = SessionResult()
        elif(res.res == CmdTypes.STS):
            legacyRes = StatusResult()
            legacyRes.changeId = res.v
        elif(res.res == CmdTypes.CHG):
            legacyRes = ChangesResult()
            legacyRes.changes = DowngradeVal(res.v) #could be more complicated if changes format differs in future
        elif(res.res == CmdTypes.GET):
            legacyRes = RetrieveResult()
            legacyRes.value = DowngradeVal(res.v)
        elif(res.res == CmdTypes.CRN):
            legacyRes = CreateResult()
            legacyRes.value = DowngradeVal(res.v)
        elif(res.res == CmdTypes.SET):
            legacyRes = UpdateResult()
            legacyRes.target = DowngradeVal(res.v[0])
        elif(res.res == CmdTypes.ADD):
            legacyRes = UpdateResult()
            legacyRes.target = DowngradeVal(res.v[0])
        elif(res.res == CmdTypes.REM):
            legacyRes = UpdateResult()
            legacyRes.target = DowngradeVal(res.v[0])
        elif(res.res == CmdTypes.MOV):
            legacyRes = UpdateResult()
            legacyRes.target = DowngradeVal(res.v[0])
        elif(res.res == CmdTypes.CLO):
            legacyRes = CloneResult()
            legacyRes.value = DowngradeVal(res.v)
        elif(res.res == CmdTypes.CAL):
            legacyRes = CallResult()
            legacyRes.callId = 0 #res.v[0]
            legacyRes.returnValues = DowngradeVal(res.v) #skip the first entry
        elif(res.res == CmdTypes.ASC):
            legacyRes = AsyncCallResult()
            legacyRes.callId = res.v
        elif(res.res == CmdTypes.CST):
            legacyRes = CallStatusResult()
            legacyRes.callId = res.v[0]
            legacyRes.callStatus = res.v[1]
            legacyRes.result = DowngradeVal(res.v[1:]) #skip the first entry
        elif(res.res == CmdTypes.ABC):
            legacyRes = AbortCallResult()
        else:
            raise EoqError(0,"Unknown result type: %s"%(res.res))
        
        
        #check if an error happened then we must override the legacy result
        if(res.s == ResTypes.ERR):
            commandType = legacyRes.commandType
            legacyRes = ErrorResult()
            legacyRes.commandType = commandType
            legacyRes.code = 0
            legacyRes.message = res.v
         

        # copy the transaction id
        legacyRes.transactionId = res.n #works for all results
    return legacyRes


from eoq1.model import IntValue, FloatValue, BoolValue, StringValue, ObjectRefValue, HistoryRefValue, EmptyValue, ListValue

def DowngradeVal(qry):
    legacyVal = 0
    if(isinstance(qry,bool)): #bool must before int, because bool is also in int in Python
        legacyVal = BoolValue()
        legacyVal.v = qry
    elif(isinstance(qry,int)):
        legacyVal = IntValue()
        legacyVal.v=qry
    elif(isinstance(qry,float)):
        legacyVal = FloatValue()
        legacyVal.v = qry
    elif(isinstance(qry,str)):
        legacyVal = StringValue()
        legacyVal.v = qry
    elif(isinstance(qry,list)):
        legacyVal = ListValue()
        for sv in qry:
            legacyVal.v.append(DowngradeVal(sv))
        return legacyVal
    elif(None == qry):
        legacyVal = EmptyValue()
    elif(qry.qry == QrySegTypes.OBJ):
        legacyVal = ObjectRefValue()
        legacyVal.v = qry.v
    elif(qry.qry == QrySegTypes.HIS):
        value = HistoryRefValue()
        value.v = qry.v
    else:
        raise EoqError(0,'Cannot convert data type %s to legacy EOQ value: %s'%(type(qry).__name__,qry))
    return legacyVal

from ..domain import Domain
from ..serialization import TextSerializer
from ..util.logger import NoLogging,LogLevels

class LegacyDomain(Domain):
    def __init__(self,domain,serializer=TextSerializer(),logger=NoLogging()):
        self.domain = domain
        self.serializer = serializer
        self.logger = logger
        
    def RawDo(self,legCmd,sessionId=None): #sessionId is not used
        cmd = UpgradeCmd(legCmd)
        self.logger.PassivatableLog(LogLevels.INFO,lambda : "legacy conversion to: %s"%(self.serializer.serialize(cmd)))
        res = self.domain.RawDo(cmd)
        legRes = DowngradeRes(res)
        return legRes
    
from ..frame import FrameHandler,FrameTypes
from eoq1 import CommandParser,ResultParser

import traceback
    
class LegacyTextFrameHandler(FrameHandler):
    def __init__(self,domain,logger=NoLogging()):
        super().__init__()
        self.domain = domain
        self.logger = logger
        
    def Handle(self,frames,sessionId=None):
        for i in range(len(frames)):
            try:
                if(frames[i].eoq == FrameTypes.CMD):
                    cmdStr = frames[i].dat
                    cmd = CommandParser.StringToCommand(cmdStr)
                    res = self.domain.RawDo(cmd,sessionId)
                    resStr = ResultParser.ResultToString(res)
                    frames[i].dat = resStr
                    frames[i].eoq = FrameTypes.RES
                else: 
                    raise EoqError(0,"Can not handle frame type: %s"%(frames[i].eoq))
            except Exception as e:
                errorMsg = "Got invalid frame: %s"%(str(e))
                self.logger.Error(errorMsg)
                traceback.print_exc();
                #print("WARNING: %s"%(errorMsg))
                frames[i].eoq = FrameTypes.ERR
                frames[i].dat = errorMsg
        return frames


