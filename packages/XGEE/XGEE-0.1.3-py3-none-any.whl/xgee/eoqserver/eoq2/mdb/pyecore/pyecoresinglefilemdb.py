'''
 Bjoern Annighoefer 2019
'''


from ..mdb import Mdb
from ...util import NoLogging,EoqError

from pyecore.resources import ResourceSet, URI
from pyecore.ecore import EPackage

from timeit import default_timer
from threading import Timer

class PyEcoreSingleFileMdb(Mdb):
    def __init__(self,modelfile,metamodelfile=None,saveTimeout=1.0,logger=NoLogging(),autoload=True):
        self.modelfile = modelfile
        self.metamodelfile = metamodelfile
        self.isLoaded = False
        self.rset = None
        self.modelroot = None
        
        self.logger = logger
        
        self.metamodelresource = None
        self.modelresource = None
        self.isDirty = False #indicates if the file needs to be saved
        self.saveTimeout = saveTimeout #This time is waited for any model modifications and than autosafe is called 
        self.saveTimer = None
        
        if(autoload):
            self.Load()
            
    def __del__(self):
        #make sure any changes are saved
        #self.logger.Info("Closing single %s ..."%(self.modelfile)) #makes problems when main thread has ended already
        
        self.__StopDelayedSaving()
        self.__Save()
        
    def Root(self):
        return self.modelroot
    
    def Class(self,packageName,className):
        clazz = None
        try:
            pack = self.rset.metamodel_registry[packageName]
            clazz = pack.getEClassifier(className)
        except Exception as e:
            raise EoqError(0,"Could not create class %s:%s: %s"%(packageName,className,str(e)))
        return clazz
        
    def Load(self,):
        self.logger.Info("Opening mdb for %s... "%(self.modelfile))
        start = default_timer()
        if(not self.isLoaded):
            self.rset = ResourceSet()
            if(self.metamodelfile):
                self.metamodelresource = self.rset.get_resource(URI(self.metamodelfile)) 
                metamodelroot = self.metamodelresource.contents[0]
                self.rset.metamodel_registry[metamodelroot.nsURI] = metamodelroot
                for child in metamodelroot.eAllContents():
                        if(isinstance(child,EPackage)):
                            self.rset.metamodel_registry[child.nsURI] = child
            self.modelresource = self.rset.get_resource(URI(self.modelfile)) 
            self.modelroot = self.modelresource.contents[0]  # We get the root (an EPackage here)
        end = default_timer()
        self.logger.Info("ok (%f s)"%(end-start))
            
    def Save(self):
        #stop the current save action 
        self.__StopDelayedSaving()
        if(self.isDirty):
            if(self.saveTimeout > 0):
                self.__StartDelayedSaving()
            else:
                self.__Save() #skip threading for a 0 timeout
        
    def __StartDelayedSaving(self):
        self.saveTimer = Timer(self.saveTimeout,self.__DelayedSaving)
        self.saveTimer.start()
        
    def __StopDelayedSaving(self):
        if(self.saveTimer):
            self.saveTimer.cancel()
            self.saveTimer = None
            
    def __DelayedSaving(self):
        self.__Save()
        self.saveTimer = None
        
    def __Save(self):
        if(self.isDirty):
            self.__SaveResource()
            self.isDirty = False
        
    def __SaveResource(self):
        self.logger.Info("Saving %s ..."%(self.modelfile))
        start = default_timer()
        self.modelresource.save()
        self.isDirty = False
        end = default_timer()
        self.logger.Info("ok (%f s)"%(end-start))
    
    def SetObjectDirty(self,obj):
        #quit any previous saving timeout, this prevents doing the save during heavy DB interactions
        self.__StopDelayedSaving()
        #mark it dirty
        self.isDirty = True
    