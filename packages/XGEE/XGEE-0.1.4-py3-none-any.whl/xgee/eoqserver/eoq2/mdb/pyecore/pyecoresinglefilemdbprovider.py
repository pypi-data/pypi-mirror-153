'''
 Single Model MDB Provider
 Bjoern Annighoefer 2019
'''


from ...util import NoLogging
from ...event import MsgEvt,ChgTypes,EvtTypes
from .pyecoremdb import PyEcoreMdb

from pyecore.resources import ResourceSet, URI
from pyecore.ecore import EObject,EPackage

from timeit import default_timer
from threading import Timer
import traceback

class PyEcoreSingleFileMdbProvider():
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
        
        self.valueCodec = None #is set during coupling
        self.domain = None #is set during coupling
        self.mdb = None #is created later
        
        if(autoload):
            self.Load()
            
    def Close(self):
        #make sure any changes are saved
        #self.logger.Info("Closing single %s ..."%(self.modelfile)) #makes problems when main thread has ended already
        
        self.__StopDelayedSaving()
        self.__Save()
        
#     def Root(self):
#         return self.modelroot
    
#     def Class(self,packageName,className):
#         clazz = None
#         try:
#             pack = self.rset.metamodel_registry[packageName]
#             clazz = pack.getEClassifier(className)
#         except Exception as e:
#             raise EoqError(0,"Could not create class %s:%s: %s"%(packageName,className,str(e)))
#         return clazz
    
    def GetMdb(self):
        return self.mdb
        
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
            self.mdb = PyEcoreMdb(self.modelroot,self.rset.metamodel_registry)
        end = default_timer()
        self.logger.Info("ok (%f s)"%(end-start))
        
    def CoupleWithDomain(self,domain,valueCodec):
        self.domain = domain
        self.valueCodec = valueCodec
        self.domain.Observe(self.OnChange,[EvtTypes.CHG])
        
    ''' sync model changes with workspace '''
        
    def OnChange(self,evts,src):
        for evt in evts:
            chg = evt
#             ctype = chg.a[1]
            target = self.valueCodec.Dec(chg.a[2]) #reverse what the domain did to the element
#             feature = chg.a[3]
#             oldOwner = self.valueCodec.Dec(chg.a[6])
            if(isinstance(target,EObject)):
                self.__SetDirty()
            
#     def Save(self):
#         #stop the current save action 
#         self.__StopDelayedSaving()
#         if(self.isDirty):
#             if(self.saveTimeout > 0):
#                 self.__StartDelayedSaving()
#             else:
#                 self.__Save() #skip threading for a 0 timeout
    
    ''' Saving functions '''
    def __SetDirty(self):
        self.isDirty = True
        self.__InitSave()
                      
    def __InitSave(self):
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
            evts = []
            try:
                self.__SaveResource()
                evts.append(MsgEvt("SingleFileMdb","Saved %s."%(self.modelfile)))
            except Exception as e:
                evts.append(MsgEvt("SingleFileMdb","Failed to save %s: %s"%(self.modelfile,str(e))))
                traceback.print_exc()
            #notify observers
            self.domain.NotifyObservers(evts, self)
        
    def __SaveResource(self):
        self.logger.Info("Saving %s ..."%(self.modelfile))
        start = default_timer()
        self.modelresource.save()
        self.isDirty = False
        end = default_timer()
        self.logger.Info("ok (%f s)"%(end-start))
    
#     def SetObjectDirty(self,obj):
#         #quit any previous saving timeout, this prevents doing the save during heavy DB interactions
#         self.__StopDelayedSaving()
#         #mark it dirty
#         self.isDirty = True
    