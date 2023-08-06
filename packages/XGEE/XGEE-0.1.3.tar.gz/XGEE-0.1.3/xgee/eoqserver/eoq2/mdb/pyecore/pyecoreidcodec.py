'''
 Bjoern Annighoefer 2019
'''
from ..valuecodec import ValueCodec
from ...query.query import ObjSeg
from ...util.error import EoqError

from pyecore.ecore import EObject,EEnumLiteral

class PyEcoreIdCodec(ValueCodec):
    def __init__(self):
        self.objectToIdLUT = {}
        self.idToObjectLUT = {}
        self.lastId = 0
        pass
    
    def Enc(self,v):
        #v = self.__ResolveProxyAndBuildInClasses(v)
        
        if(isinstance(v,EEnumLiteral)):
            return str(v)
        elif(isinstance(v,EObject)):
            idNb = 0
            try:
                idNb = self.objectToIdLUT[v]
            except:
                idNb = self.lastId
                self.objectToIdLUT[v] = idNb
                self.idToObjectLUT[idNb] = v
                self.lastId += 1 #root id starts now at 0 like all other indexes
            return ObjSeg(idNb)
        else:
            return v
    def Dec(self,c):
        if(isinstance(c,ObjSeg)):
            obj = None
            idNb = c.v
            try:
                obj = self.idToObjectLUT[idNb]
            except:
                raise EoqError(0,'Error id #%s is not a known object'%(idNb))
            return obj
        else:
            return c
        
    '''
     PRIVATE methods
    '''
       
#     def __ResolveProxyAndBuildInClasses(self,obj): 
#         if(isinstance(obj, EProxy)):
#             obj.force_resolve()
#             obj = obj._wrapped #remove the outer proxy
#         if(isinstance(obj, (MetaEClass,type,types.ModuleType))): #this is necessary to mask compiled model instances
#             obj = obj.eClass
#         return obj