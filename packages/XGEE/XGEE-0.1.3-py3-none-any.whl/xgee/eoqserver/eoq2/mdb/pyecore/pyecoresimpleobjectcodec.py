'''
 Bjoern Annighoefer 2019
'''
from ..valuecodec import ValueCodec
from ...query.query import ObjSeg

   
#eObject encoders    

from pyecore.ecore import EObject

class PyEcoreSimpleObjectCodec(ValueCodec):
    def __init__(self):
        pass
    
    def Enc(self,v):
        if(isinstance(v,EObject)):
            return ObjSeg(v)
        else:
            return v
    def Dec(self,c):
        if(isinstance(c,ObjSeg)):
            return c.v
        else:
            return c
        