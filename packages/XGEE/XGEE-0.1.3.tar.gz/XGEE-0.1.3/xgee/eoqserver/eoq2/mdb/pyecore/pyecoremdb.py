from ..mdb import Mdb

from pyecore.ecore import EProxy,MetaEClass
import types
import traceback
from threading import Lock

class PyEcoreMdb(Mdb):
    def __init__(self,root,metamodelRegistry,provider=None):#must be the original meta model registry and allow for modifications
        super().__init__()
        self.root = root
        self.metamodelRegistry = metamodelRegistry
        self.provider = provider;
        self.lock = Lock()
        
    def Lock(self):
        self.lock.acquire()
            
    def Release(self):
        self.lock.release()
    
    def Root(self):
        return self.root
    
    def Metamodels(self):
        return [(p.eClass if(isinstance(p,types.ModuleType)) else p) for p in self.metamodelRegistry.values()]
            
    def AddMetamodel(self,name,metamodel): #name is neglegted since the namespace URI is the identifier in pyecore
        self.metamodelRegistry[metamodel.nsURI] = metamodel #metamodel is expected to be a EPackage
        
    def RemoveMetamodel(self,name,metamodel): #name is neglegted since the namespace URI is the identifier in pyecore
        self.metamodelRegistry.pop(metamodel.nsURI)
        
    def GetMetamodel(self,name):
        package = self.metamodelRegistry[name]
        if(isinstance(package,types.ModuleType)):
            #this happens for metamodels loaded by generated python code
            #in this case we must create a copy as a psydo EPackge
            package = package.eClass
        return package
    
    def ResolveProxy(self,proxy):
        obj = proxy
        if(isinstance(proxy, EProxy)):
            try: #resolve can fail if files have been modified or objects been deleted before the proxy has been resolved
                if self.provider: self.provider.Lock() #otherwise IDs can not be resolved
                proxy.force_resolve()
                if self.provider: self.provider.Release() #undo the connection before
                obj = proxy._wrapped #remove the outer proxy
            except Exception as e:
                traceback.print_exc()
                print("WARN: Unresolvable proxy found and removed")
                obj = None
        if(isinstance(proxy, (MetaEClass,type,types.ModuleType))): #this is necessary to mask compiled model instances
            obj = proxy.eClass
        return obj
