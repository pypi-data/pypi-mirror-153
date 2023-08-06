'''
Annighoefer 2019
'''
import re

from .model import *
from .error import EoqParseError
from . import QueryParser
from . import ValueParser


class CommandParser:
    @staticmethod
    def RetrieveCommand(target,query):
        command = RetrieveCommand()
        command.target = target
        command.query = query
        return command
    
    @staticmethod
    def RetrieveCommandStr(target,queryStr):
        command = RetrieveCommand()
        command.target = target
        command.query = QueryParser.StringToQuery(queryStr)
        return command
    
    @staticmethod
    def CreateCommand(packageNsUri,className,n):
        command = CreateCommand()
        command.packageNsUri = StringValue(v=packageNsUri)
        command.className = StringValue(v=className)
        command.n = IntValue(v=n)
        return command
    
    @staticmethod
    def UpdateCommand(target,query,value):
        command = UpdateCommand()
        command.target = target
        command.query = query
        command.value = value
        return command
    
    @staticmethod
    def UpdateCommandStr(target,queryStr,value):
        command = UpdateCommand()
        command.target = target
        command.query = QueryParser.StringToQuery(queryStr)
        command.value = value
        return command
    
    @staticmethod
    def ChangesCommand(earliestChangeId):
        command = ChangesCommand()
        command.earliestChangeId = IntValue(v=earliestChangeId)
        return command
    
    @staticmethod
    def CompoundCommand(subcommands):
        command = CompoundCommand()
        for c in subcommands:
            command.commands.add(c)
        return command
    
    @staticmethod
    def CommandToString(command):
        commandSegments = []
        seperator = ' '
        if(command.type == CommandTypesE.COMPOUND):
            seperator = '\n'
            for c in command.commands:
                commandSegments += [CommandParser.CommandToString(c)]
        else:
            commandStr = CommandTypesE.to_string(command.type)
            commandSegments += [commandStr]
            if(command.type == CommandTypesE.HELLO):
                commandSegments += [ValueParser.ValueToString(command.user), ValueParser.ValueToString(command.identification)]
            elif(command.type == CommandTypesE.GOODBYE):
                commandSegments += [ValueParser.ValueToString(command.sessionId)]
            elif(command.type == CommandTypesE.SESSION):
                commandSegments += [ValueParser.ValueToString(command.sessionId)]
            elif(command.type == CommandTypesE.STATUS):
                pass
            elif(command.type == CommandTypesE.CHANGES):
                commandSegments += [ValueParser.ValueToString(command.earliestChangeId)]
            elif(command.type == CommandTypesE.RETRIEVE):
                commandSegments += [ValueParser.ValueToString(command.target),QueryParser.QueryToString(command.query)]
            elif(command.type == CommandTypesE.CREATE):
                commandSegments += [ValueParser.ValueToString(command.packageNsUri),ValueParser.ValueToString(command.className),ValueParser.ValueToString(command.n)]
            elif(command.type == CommandTypesE.UPDATE):
                commandSegments += [ValueParser.ValueToString(command.target),QueryParser.QueryToString(command.query),ValueParser.ValueToString(command.value)]
            elif(command.type == CommandTypesE.CALL):
                commandSegments += [ValueParser.ValueToString(command.action),ValueParser.ValueToString(command.args)]
            elif(command.type == CommandTypesE.CLONE):
                commandSegments += [ValueParser.ValueToString(command.target),CloneModesE.to_string(command.mode)]
            elif(command.type == CommandTypesE.ASYNCCALL):
                commandSegments += [ValueParser.ValueToString(command.action),ValueParser.ValueToString(command.args)]
            elif(command.type == CommandTypesE.CALLSTATUS):
                commandSegments += [ValueParser.ValueToString(command.callId)]
            elif(command.type == CommandTypesE.ABORTCALL):
                commandSegments += [ValueParser.ValueToString(command.callId)]
            else:
                pass
        return seperator.join(commandSegments)
    
    @staticmethod
    def StringToCommand(commandStr):
        command = None
        commandLines = commandStr.splitlines() #TODO: This will get problems if newlines are included in strings
        if(1 < len(commandLines)):
            command = CompoundCommand()
            for commandLine in commandLines:
                command.commands.add(CommandParser.SingleStringLineToCommand(commandLine))
        else:
            command = CommandParser.SingleStringLineToCommand(commandStr)
        return command
    
    @staticmethod
    def SingleStringLineToCommand(commandLine):
        command = None
        commandSegments = re.findall(r"[^'\s]\S*|'.+?'", commandLine) #special solution since strings can contain spaces
        #commandSegments = commandLine.split(' ')
        nSegments = len(commandSegments)
        if(CommandTypesE.to_string(CommandTypesE.HELLO) == commandSegments[0] and nSegments == 3):
            command = HelloCommand()
            command.user = ValueParser.StringToValue(commandSegments[1])
            command.identification = ValueParser.StringToValue(commandSegments[2])
        elif(CommandTypesE.to_string(CommandTypesE.GOODBYE) == commandSegments[0] and nSegments == 2):
            command = GoodbyeCommand()
            command.sessionId = ValueParser.StringToValue(commandSegments[1])
        elif(CommandTypesE.to_string(CommandTypesE.SESSION) == commandSegments[0] and nSegments == 2):
            command = SessionCommand()
            command.sessionId = ValueParser.StringToValue(commandSegments[1])
        elif(CommandTypesE.to_string(CommandTypesE.STATUS) == commandSegments[0] and nSegments == 1):
            command = StatusCommand()
        elif(CommandTypesE.to_string(CommandTypesE.CHANGES) == commandSegments[0] and nSegments == 2):
            command = ChangesCommand()
            command.earliestChangeId = ValueParser.StringToValue(commandSegments[1])
        elif(CommandTypesE.to_string(CommandTypesE.RETRIEVE) == commandSegments[0] and nSegments == 3):
            command = RetrieveCommand()
            command.target = ValueParser.StringToValue(commandSegments[1])
            command.query = QueryParser.StringToQuery(commandSegments[2])
        elif(CommandTypesE.to_string(CommandTypesE.CREATE) == commandSegments[0] and nSegments == 4):
            command = CreateCommand()
            command.packageNsUri = ValueParser.StringToValue(commandSegments[1])
            command.className = ValueParser.StringToValue(commandSegments[2])
            command.n = ValueParser.StringToValue(commandSegments[3])
        elif(CommandTypesE.to_string(CommandTypesE.UPDATE) == commandSegments[0] and nSegments == 4):
            command = UpdateCommand()
            command.target = ValueParser.StringToValue(commandSegments[1])
            command.query = QueryParser.StringToQuery(commandSegments[2])
            command.value = ValueParser.StringToValue(commandSegments[3])
        elif(CommandTypesE.to_string(CommandTypesE.CLONE) == commandSegments[0] and nSegments == 3):
            command = CloneCommand()
            command.target = ValueParser.StringToValue(commandSegments[1])
            command.mode = CloneModesE.from_string(commandSegments[2])
        elif(CommandTypesE.to_string(CommandTypesE.CALL) == commandSegments[0] and nSegments == 3):
            command = CallCommand()
            command.action = ValueParser.StringToValue(commandSegments[1])
            command.args = ValueParser.StringToValue(commandSegments[2])
        elif(CommandTypesE.to_string(CommandTypesE.ASYNCCALL) == commandSegments[0] and nSegments == 3):
            command = AsyncCallCommand()
            command.action = ValueParser.StringToValue(commandSegments[1])
            command.args = ValueParser.StringToValue(commandSegments[2])
        elif(CommandTypesE.to_string(CommandTypesE.CALLSTATUS) == commandSegments[0] and nSegments == 2):
            command = CallStatusCommand()
            command.callId = ValueParser.StringToValue(commandSegments[1])
        elif(CommandTypesE.to_string(CommandTypesE.ABORTCALL) == commandSegments[0] and nSegments == 2):
            command = AbortCallCommand()
            command.callId = ValueParser.StringToValue(commandSegments[1])
        
        else:
            raise EoqParseError(0,'Command string could not be split into segments',commandLine)
        return command
    
    @staticmethod
    def CalcCommandHistoryLength(command,until=-1):
        length = 0
        if(command.type == CommandTypesE.COMPOUND):
            for subcommand in command.commands:
                until -= 1
                if(until!=0):
                    length += CommandParser.CalcCommandHistoryLength(subcommand,until)
        elif(command.type in [CommandTypesE.RETRIEVE,CommandTypesE.CREATE,CommandTypesE.CALL] ):
            length = 1
        return length
    