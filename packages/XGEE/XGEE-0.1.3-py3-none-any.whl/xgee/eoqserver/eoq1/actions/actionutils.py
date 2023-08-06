'''
Created on 24.06.2019

@author: Annighoefer
'''

from .. import CommandParser,ResultParser

import datetime
from urllib.parse import quote,unquote  #for escaping strings

class ActionUtils:
    @staticmethod
    def OutputToChannel(callId,channelName,data,domain):
        callRef = None
        cmd = CommandParser.StringToCommand("RETRIEVE #0 /actionCalls{callId=%d}"%(callId))
        res = domain.Do(cmd)
        if(ResultParser.IsResultOk(res)):
            if(0<len(res.value.v)):
                callRef = res.value.v[0].v
        if(callRef): 
            channelRef = None         
            cmd = CommandParser.StringToCommand("RETRIEVE #%d /channels{name='%s'}"%(callRef,channelName))
            res = domain.Do(cmd)
            if(ResultParser.IsResultOk(res)):
                if(0<len(res.value.v)):
                    channelRef = res.value.v[0].v
            if(None==channelRef):
                cmd = CommandParser.StringToCommand("CREATE 'http://www.eoq.de/model/v1.0' 'CallChannel' 1\n"
                                                     "UPDATE $0 /name '%s'\n"
                                                     "UPDATE #%d /channels[+] $0"%(channelName,callRef))
                res = domain.Do(cmd)
                if(ResultParser.IsResultOk(res)):
                    channelRef = res.results[0].value.v
            if(channelRef):
                timeStamp =datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
                cmd = CommandParser.StringToCommand("CREATE 'http://www.eoq.de/model/v1.0' 'CallChannelData' 1\n"
                                                     "UPDATE $0 /date '%s'\n"
                                                     "UPDATE $0 /data '%s'\n"
                                                     "UPDATE #%d /data[+] $0"%(timeStamp,quote(data),channelRef))
                res = domain.Do(cmd)
        return 
    
    @staticmethod
    def SetCallStatus(callId,callStatus,domain):
        cmd = CommandParser.StringToCommand("RETRIEVE #0 /actionCalls{callId=%d}[0]\n"
                                             "UPDATE $0 /callStatus '%s'"%(callId,callStatus))
        domain.Do(cmd)
        return