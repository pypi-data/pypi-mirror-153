'''
 Bjoern Annighoefer 2019
'''
#define the default codec

from .valuecodec import ValueCodec

class NoCodec(ValueCodec):
    def __init__(self):
        pass
    
    def Enc(self,v):
        return v
    
    def Dec(self,c):
        return c
    