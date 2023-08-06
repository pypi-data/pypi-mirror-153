'''
 Bjoern Annighoefer 2019
'''

from .serializer import Serializer

'''

JSON Serializer

'''
   
from ..frame.frame import Frame
from ..command.command import Cmd
from ..query.query import QrySegFactory
from ..command.result import Res
from ..event.event import Evt

import json

def JsonSerializeHook(obj):
    return obj.__dict__

def JsonDeserializeHook(dct):
        if "eoq" in dct:
            return Frame(dct["eoq"],dct["uid"],dct["dat"],version=dct["ver"])
        if "cmd" in dct:
            return Cmd(dct["cmd"],dct["a"])
        elif "qry" in dct: 
            return QrySegFactory(dct["qry"],dct["v"])
        elif "res" in dct:
            return Res(dct["res"],dct["s"],dct["v"],dct["n"],dct["c"])
        elif "evt" in dct:
            return Evt(dct["evt"],dct["k"],dct["a"])
        return dct


class JsonSerializer(Serializer):
    def __init__(self):
        pass

    def Ser(self, val):
        try:
            return json.dumps(val,default=JsonSerializeHook)
        except Exception as e:
            return "{error: '%s'"%(str(e))
    
    def Des(self,code):
        return json.loads(code,object_hook=JsonDeserializeHook)