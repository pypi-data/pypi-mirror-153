from ..mdb import DomainA,CommandA
from pyeoq import ResultParser,CommandParser


from urllib.parse import urlencode
from http.client import HTTPConnection

class RemoteHttpDomain(DomainA):
    
    connection = None
    timeout = 1
    
    def __init__(self, host, port=8000, timeout=1, **kwargs):
        
        self.connection = HTTPConnection(host, port=port)
        
        self.timeout = timeout
        super().__init__(**kwargs)
        self.name = 'RemoteHTTPDomain'
        
        
        
        
    def Do(self, command):
            
        if isinstance(command,CommandA):
            command = CommandParser.CommandToString(command)
        elif not type(command) == str:
            raise TypeError("Argument must be either a string or an instance of CommandA.")
            
        commandStr = urlencode({'command':command})
        
        res = self._post_request(commandStr)
        
        return res
    
    def _post_request(self,commandStr):
        
        self.connection.request("POST", "/eoq.do", commandStr)
        response = self.connection.getresponse()
        resultStr = response.read().decode('utf-8')
        res = ResultParser.StringToResult(resultStr)
        return res