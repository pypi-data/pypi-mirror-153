'''
Annighoefer 2019
'''
import re

from .model import *
from .error import EoqParseError
from . import QueryParser
from . import ValueParser


class ResultParser:  
    @staticmethod
    def ResultToString(result : ResultA):
        resultSegments = []
        seperator = ' '
        if(result.type in (ResultTypesE.COMPOUND_OK, ResultTypesE.COMPOUND_ERROR)):
            seperator = '\n'
            for r in result.results:
                resultSegments += [ResultParser.ResultToString(r)]
        else:
            statusStr = ResultTypesE.to_string(result.type)
            resultSegments += [statusStr, str(result.transactionId), CommandTypesE.to_string(result.commandType)]
            if(result.type == ResultTypesE.OK):
                if(result.commandType == CommandTypesE.HELLO):
                    resultSegments += [result.sessionId]
                elif(result.commandType == CommandTypesE.GOODBYE):
                    pass
                elif(result.commandType == CommandTypesE.SESSION):
                    pass
                elif(result.commandType == CommandTypesE.STATUS):
                    resultSegments += [str(result.changeId)]
                elif(result.commandType == CommandTypesE.CHANGES):
                    resultSegments += [ValueParser.ValueToString(result.changes)]
                elif(result.commandType == CommandTypesE.RETRIEVE):
                    resultSegments += [ValueParser.ValueToString(result.value)]
                elif(result.commandType == CommandTypesE.CREATE):
                    resultSegments += [ValueParser.ValueToString(result.value)]
                elif(result.commandType == CommandTypesE.UPDATE):
                    resultSegments += [ValueParser.ValueToString(result.target)]
                elif(result.commandType == CommandTypesE.CLONE):
                    resultSegments += [ValueParser.ValueToString(result.value)]
                elif(result.commandType == CommandTypesE.CALL):
                    resultSegments += [str(result.callId), ValueParser.ValueToString(result.returnValues)]
                elif(result.commandType == CommandTypesE.ASYNCCALL):
                    resultSegments += [str(result.callId)]
                elif(result.commandType == CommandTypesE.CALLSTATUS):
                    resultSegments += [str(result.callId), CallStatusE.to_string(result.callStatus), ValueParser.ValueToString(result.result)]
                elif(result.commandType == CommandTypesE.ABORTCALL):
                    pass
            elif(result.type == ResultTypesE.ERROR):
                resultSegments += [str(result.code),"'%s'"%(result.message)]
        return seperator.join(resultSegments)
    
    @staticmethod
    def StringToResult(resultStr):
        result = None
        resultLines = resultStr.splitlines() #TODO: This will get problems if newlines are included in strings
        if(1 < len(resultLines)):
            result = CompoundResult()
            for resultLine in resultLines:
                subResult = ResultParser.SingleStringLineToResult(resultLine)
                result.results.append(subResult)
                if(subResult.type == ResultTypesE.ERROR) :
                    result.type = ResultTypesE.COMPOUND_ERROR #if a single command failed the full compound command is failed.
        else :
            result = ResultParser.SingleStringLineToResult(resultStr)
        return result
    
    @staticmethod
    def SingleStringLineToResult(resultLine):
        result = None
        resultSegments = re.findall(r"[^'\s]\S*|'.+?'", resultLine)

        nSegments = len(resultSegments)
        if(ResultTypesE.to_string(ResultTypesE.OK) == resultSegments[0] and nSegments >= 3):
            if(CommandTypesE.to_string(CommandTypesE.HELLO) == resultSegments[2] and nSegments == 4):
                result = HelloResult()
                result.transactionId = int(resultSegments[1])
                result.sessionId = resultSegments[3]
            elif(CommandTypesE.to_string(CommandTypesE.GOODBYE) == resultSegments[2] and nSegments == 3):
                result = GoodbyeResult()
                result.transactionId = int(resultSegments[1])
            elif(CommandTypesE.to_string(CommandTypesE.SESSION) == resultSegments[2] and nSegments == 3):
                result = SessionResult()
                result.transactionId = int(resultSegments[1])
            elif(CommandTypesE.to_string(CommandTypesE.STATUS) == resultSegments[2] and nSegments == 4):
                result = StatusResult()
                result.transactionId = int(resultSegments[1])
                result.changeId = int(resultSegments[3])
            elif(CommandTypesE.to_string(CommandTypesE.CHANGES) == resultSegments[2] and nSegments == 4):
                result = ChangesResult()
                result.transactionId = int(resultSegments[1])
                result.changes = ValueParser.StringToValue(resultSegments[3])
            elif(CommandTypesE.to_string(CommandTypesE.RETRIEVE) == resultSegments[2] and nSegments == 4):
                result = RetrieveResult()
                result.transactionId = int(resultSegments[1])
                result.value = ValueParser.StringToValue(resultSegments[3])
            elif(CommandTypesE.to_string(CommandTypesE.CREATE) == resultSegments[2] and nSegments == 4):
                result = CreateResult()
                result.transactionId = int(resultSegments[1])
                result.value = ValueParser.StringToValue(resultSegments[3])
            elif(CommandTypesE.to_string(CommandTypesE.UPDATE) == resultSegments[2] and nSegments == 4):
                result = UpdateResult()
                result.transactionId = int(resultSegments[1])
                result.target = ValueParser.StringToValue(resultSegments[3])
            elif(CommandTypesE.to_string(CommandTypesE.CLONE) == resultSegments[2] and nSegments == 4):
                result = CloneResult()
                result.transactionId = int(resultSegments[1])
                result.value = ValueParser.StringToValue(resultSegments[3])
            elif(CommandTypesE.to_string(CommandTypesE.CALL) == resultSegments[2] and nSegments == 5):
                result = CallResult()
                result.transactionId = int(resultSegments[1])
                result.callId = int(resultSegments[3])
                result.returnValues = ValueParser.StringToValue(resultSegments[4])
            elif(CommandTypesE.to_string(CommandTypesE.ASYNCCALL) == resultSegments[2] and nSegments == 4):
                result = AsyncCallResult()
                result.transactionId = int(resultSegments[1])
                result.callId = int(resultSegments[3])
            elif(CommandTypesE.to_string(CommandTypesE.CALLSTATUS) == resultSegments[2] and nSegments == 6):
                result = CallStatusResult()
                result.transactionId = int(resultSegments[1])
                result.callId = int(resultSegments[3])
                result.callStatus = CallStatusE.to_string(resultSegments[4])
                result.result = ValueParser.StringToValue(resultSegments[5])
            elif(CommandTypesE.to_string(CommandTypesE.ABORTCALL) == resultSegments[2] and nSegments == 3):
                result = AbortCallResult()
                result.transactionId = int(resultSegments[1])
            else:
                raise EoqParseError(0,'Result string could not be split into segments',resultLine)
        elif(ResultTypesE.to_string(ResultTypesE.ERROR) == resultSegments[0] and nSegments == 5):
            result = ErrorResult()
            result.transactionId = int(resultSegments[1])
            result.commandType = CommandTypesE.from_string(resultSegments[2])
            result.code = int(resultSegments[3])
            result.message = resultSegments[4]
        else:
            raise EoqParseError(0,'Result string could not be split into segments: ',resultLine)
        return result
    
    @staticmethod
    def IsResultOk(result : ResultA)->bool:
        return (result.type == ResultTypesE.OK or result.type == ResultTypesE.COMPOUND_OK)
    
    @staticmethod
    def IsResultNok(result : ResultA)->bool:
        return (result.type == ResultTypesE.ERROR or result.type == ResultTypesE.COMPOUND_ERROR)