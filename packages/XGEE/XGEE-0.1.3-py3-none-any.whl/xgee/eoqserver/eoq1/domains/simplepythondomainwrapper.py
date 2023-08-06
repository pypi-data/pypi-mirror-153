'''
Created on 24.03.2019

Wrapper class that enables the use of EOQ domains without 
using commands. Primarily this was written to keep old EOQ examples operational.

@author: Annighoefer
'''

from ..model import ObjectRefValue,CommandA,DomainA
from .. import ValueParser
from .. import QueryParser
from .. import CommandParser
from .. import ResultParser
from ..error import EoqGeneralError

class SimplePythonDomainWrapper():
    def __init__(self,domain : DomainA):
        self.domain = domain
        
    def Do(self,command : CommandA):
        return self.domain.Do(command)

    def Retrieve(self,ptarget,queryStr):
        if(None==ptarget):
            ptarget = ObjectRefValue(v=0)
        target = ValueParser.PythonToValue(ptarget)
        query = QueryParser.StringToQuery(queryStr)
        command = CommandParser.RetrieveCommand(target, query)
        result = self.domain.Do(command)
        if(ResultParser.IsResultNok(result)):
            raise EoqGeneralError(result.code,result.message)
        return ValueParser.ValueToPython(result.value)
    
    def Create(self,packageNsUri,className,n=1):
        command = CommandParser.CreateCommand(packageNsUri, className, n)
        result = self.domain.Do(command)
        if(ResultParser.IsResultNok(result)):
            raise EoqGeneralError(result.code,result.message)
        return ValueParser.ValueToPython(result.value)
    
    def Update(self,ptarget,queryStr,pvalue):
        if(None==ptarget):
            ptarget = ObjectRefValue(v=0)
        target = ValueParser.PythonToValue(ptarget)
        query = QueryParser.StringToQuery(queryStr)
        value = ValueParser.PythonToValue(pvalue)
        command = CommandParser.UpdateCommand(target, query, value)
        result = self.domain.Do(command)
        if(ResultParser.IsResultNok(result)):
            raise EoqGeneralError(result.code,result.message)
        return ValueParser.ValueToPython(result.target)
    
    def Clone(self,ptarget,cloneOp='FULL'):
        if(None==ptarget):
            ptarget = ObjectRefValue(v=0)
        target = ValueParser.PythonToValue(ptarget)
        cmdStr = "CLONE #%d %s"%(target.v,cloneOp)
        cmd = CommandParser.StringToCommand(cmdStr)
        result = self.domain.Do(cmd)
        if(ResultParser.IsResultNok(result)):
            raise EoqGeneralError(result.code,result.message)
        return ValueParser.ValueToPython(result.value)
       
   
