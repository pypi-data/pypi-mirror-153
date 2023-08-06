'''
 Bjoern Annighoefer 2019
'''

from ..mdbaccessor import MdbAccessor
from ...command.command import CloModes
from ...util.error import EoqError

#Definition of pyecore based accessors
from pyecore.ecore import EPackage,EObject,EClass,EProxy,MetaEClass,\
    EClassifier
from pyecore.valuecontainer import EOrderedSet

import types
from itertools import chain


class PyEcoreMdbAccessor(MdbAccessor):
    def __init__(self,mdb=None,valueCodec=None):
        super().__init__()
        self.mdb = mdb #is necessary for creating classes by name
        self.vc = valueCodec
        ##make sure the root gets the primary encoding
        self.root = self.__ResolveAndEnc(self.mdb.Root())
        self.root_obj = self.mdb.Root()
        
        #tid
        self.latestTransactionId = 0
        
        #internal caching
        #self.allReferencesLut = {}
        
    def Lock(self):
        self.mdb.Lock()
    
    def Release(self):
        self.mdb.Release()
        
    ''' METAMODEL ACESSORS '''
   
    def GetAllMetamodels(self):
        ePackages = self.mdb.Metamodels()
        metamodels = [self.__ResolveAndEnc(m) for m in ePackages]
        return metamodels
     
    def RegisterMetamodel(self,package):
        ePackage = self.vc.Dec(package)
        self.mdb.AddMetamodel(None,ePackage) #name is retrieved internally from URI
        return True
    
    def UnregisterMetamodel(self,package):
        ePackage = self.vc.Dec(package)
        self.mdb.RemoveMetamodel(None,ePackage) #name is retrieved internally from URI
        return True

    ''' MODEL ACESSORS '''

    def GetRoot(self):
        root = self.mdb.Root()
        return self.__ResolveAndEnc(root)
        
    def Get(self,obj,feature):
        value = None
        eObj = self.vc.Dec(obj)
        eFeature = self.vc.Dec(feature)
        eValue = eObj.eGet(eFeature)
        #check if this was not a value but a method.
        if(isinstance(eValue,types.MethodType)): 
            eValue =  eValue()#call the method to get the values
        #convert any sets to lists
        if(isinstance(eValue, EOrderedSet) or 
           isinstance(eValue, set) or 
           isinstance(eValue, list)):
            value = self.__RemoveNullRefs([ self.__ResolveAndEnc(v) for v in eValue])
        else:
            value = self.__ResolveAndEnc(eValue)
        return value
    
    def Set(self,obj,feature,value):
        eObj = self.vc.Dec(obj)
        eFeature = self.vc.Dec(feature)
        oldEValue = eObj.eGet(eFeature)
        eValue = self.vc.Dec(value)
        oldValue = self.__ResolveAndEnc(oldEValue)
        #preserve the old values
        oldOwner = None
        oldFeature = None
        oldIndex = None
        eOldOwner = None
        if(isinstance(eValue, EObject)):
            eOldOwner = eValue.eContainer()
            if(eOldOwner):
                oldOwner = self.__ResolveAndEnc(eOldOwner)
                eOldFeature = eValue.eContainmentFeature()
                oldFeature = self.__ResolveAndEnc(eOldFeature)
                if(eOldFeature.many):
                    oldIndex = eOldOwner.eGet(eOldFeature).index(eValue)
        eObj.eSet(eFeature,eValue)
        return (oldValue,oldOwner,oldFeature,oldIndex)
    
    def Add(self,obj,feature,child):
        eObj = self.vc.Dec(obj)
        eFeature = self.vc.Dec(feature)
        eChild = self.vc.Dec(child)
        oldEValue = eObj.eGet(eFeature)
        #preserve the old values
        oldOwner = None
        oldFeature = None
        oldIndex = None
        eOldOwner = None
        if(isinstance(eChild, EObject)):
            eOldOwner = eChild.eContainer()
            if(eOldOwner):
                oldOwner = self.__ResolveAndEnc(eOldOwner)
                eOldFeature = eChild.eContainmentFeature()
                oldFeature = self.__ResolveAndEnc(eOldFeature)
                if(eOldFeature.many):
                    oldIndex = eOldOwner.eGet(eOldFeature).index(eChild)
        #this must happen before in order to copy the old value
        oldValue = [ self.__ResolveAndEnc(v) for v in oldEValue]
        #add the new child
        oldEValue.add(eChild)
        return (oldValue,oldOwner,oldFeature,oldIndex)
    
    def Remove(self,obj,feature,child):
        eObj = self.vc.Dec(obj)
        eFeature = self.vc.Dec(feature)
        eChild = self.vc.Dec(child)
        oldEValue = eObj.eGet(eFeature)
        #preserve the old values
        oldOwner = None
        oldFeature = None
        oldIndex = None
        eOldOwner = None
        if(isinstance(eChild, EObject)):
            eOldOwner = eChild.eContainer()
            if(eOldOwner):
                oldOwner = self.__ResolveAndEnc(eOldOwner)
                eOldFeature = eChild.eContainmentFeature()
                oldFeature = self.__ResolveAndEnc(eOldFeature)
                if(eOldFeature.many):
                    oldIndex = eOldOwner.eGet(eOldFeature).index(eChild)
        #this must happen before in order to copy the old value
        oldValue = [ self.__ResolveAndEnc(v) for v in oldEValue]
        #remove the child
        eChild = self.vc.Dec(child)
        oldEValue.remove(eChild)
        return (oldValue,oldOwner,oldFeature,oldIndex)
    
    def Move(self,obj,newIndex):
        eObj = self.vc.Dec(obj)
        eContainer = eObj.eContainer()
        eFeature = eObj.eContainmentFeature()
        
        oldEValue = eContainer.eGet(eFeature)
        #preserve the old values
        oldOwner = self.__ResolveAndEnc(eContainer)
        oldFeature = self.__ResolveAndEnc(eFeature)
        oldIndex = eContainer.eGet(eFeature).index(eObj)
        #this must happen before in order to copy the old value
        oldValue = [ self.__ResolveAndEnc(v) for v in oldEValue]
        
        #do the move if it makes sense
        if(newIndex!=oldIndex):
            oldEValue.pop(oldIndex)
            oldEValue.insert(newIndex,eObj)
        return (oldValue,oldOwner,oldFeature,oldIndex)
        
    
    def Clone(self, obj, mode):
        clone = None
        eObj = self.vc.Dec(obj)
        if(CloModes.CLS==mode):
            clone = self.__ECloneClass(eObj)
        elif(CloModes.ATT==mode):
            clone = self.__ECloneAttributes(eObj)
        elif(CloModes.FLT==mode):
            clone = self.__ECloneFlat(eObj)
        elif(CloModes.FUL==mode):
            clone = self.__ECloneFull(eObj)
        elif(CloModes.DEP==mode):
            clone = self.__ECloneDeep(eObj)
        return self.__ResolveAndEnc(clone)
    
    def Create(self, clazz,n,constructorArgs=[]):
        eClass = self.vc.Dec(clazz)
        eConstructorArgs = [self.vc.Dec(a) for a in constructorArgs] # necessary if this contains an eObject
        if(n==1):
            newObjects = self.__ResolveAndEnc(self.__CreateEClassInstance(eClass,eConstructorArgs))
        else:
            newObjects = [self.__ResolveAndEnc(self.__CreateEClassInstance(eClass,eConstructorArgs)) for i in range(n)]
        return newObjects
        
    def CreateByName(self,packageName,className,n,constructorArgs=[]):
        newObjects = None
        eConstructorArgs = [self.vc.Dec(a) for a in constructorArgs] # necessary if this contains an eObject
        try:
            eClass = self.__GetClassByName(packageName, className)
            if(n==1):
                newObjects = self.__ResolveAndEnc(self.__CreateEClassInstance(eClass,eConstructorArgs))
            else:
                newObjects = [self.__ResolveAndEnc(self.__CreateEClassInstance(eClass,eConstructorArgs)) for i in range(n)]
        except Exception as e:
            raise EoqError(0,"Could not create class %s:%s: %s"%(packageName,className,str(e)))
        return newObjects
    
    def GetClassByName(self,packageName,className):
        eClass = self.__GetClassByName(packageName, className)
        return self.__ResolveAndEnc(eClass)
    
    def AddConstraint(self,constraint):
        index = None
        eClass = self.__GetClassByName('http://www.example.org/constraintmodel', 'Constraint')
        eClass_instance = self.__CreateEClassInstance(eClass)
        eClass_instance.eSet('constraintType',constraint.constraintType)
        eClass_instance.eSet('name',constraint.name)
        eClass_instance.eSet('target',constraint.target)
        eClass_instance.eSet('feature',constraint.feature)
        eClass_instance.eSet('law',constraint.law)
        eClass_instance.eSet('annotation',constraint.annotation)
        for i in range(len(self.root_obj.eContents)):
            if self.root_obj.eContents[i].name == 'cdb.constraintmodel':
                index = i
        if not(index == None):
            self.root_obj.eContents[index].eContents[0].constraint.append(eClass_instance)
            print("Constraint is added")
        
    def RemoveConstraint(self,constraint):
        index = None
        eClass = self.__GetClassByName('http://www.example.org/constraintmodel', 'Constraint')
        eClass_instance = self.__CreateEClassInstance(eClass)
        eClass_instance.eSet('constraintType',constraint.constraintType)
        eClass_instance.eSet('name',constraint.name)
        eClass_instance.eSet('target',constraint.target)
        eClass_instance.eSet('feature',constraint.feature)
        eClass_instance.eSet('law',constraint.law)
        eClass_instance.eSet('annotation',constraint.annotation)
        for i in range(len(self.root_obj.eContents)):
            if self.root_obj.eContents[i].name == 'cdb.constraintmodel':
                index = i
        if not(index == None):
            for eobj in self.root_obj.eContents[index].eContents[0].eContents:
                if str(eobj.constraintType) == str(eClass_instance.constraintType) and eobj.name == eClass_instance.name and eobj.target == eClass_instance.target and eobj.feature == eClass_instance.feature and eobj.law == eClass_instance.law and eobj.annotation == eClass_instance.annotation:
                    eobj.delete()
            
    def CalculateSimilarityIndex(self, obj, old):
        '''
        Calculates a Similarity Index of all children of "old" with respect to "obj".
        "Obj" is from "new" with level n ...
        ... and "old" the corresponding object from "old" with level n+1
        Calls 4 Subfunctions: Name, Attributes, References, Index/Position
        which can award up to 0.25 points each -> Maximum: 1, Minimum 0
        '''
        allSI      = [] # stores the SI for each child of old
        allChanges = [] # stores changes for MergeRoutine to handle
        eObj    = self.vc.Dec(obj)
        typeObj = eObj.eClass.name
        childrenOld = self.GetAllChildrenOfType(old, typeObj)
        # print('# STARTING CSI FOR', obj, 'and', childrenOld)
        for childOld in childrenOld:
            # print('### CSI LOOP FOR', obj, 'and', childOld)
            childObj = self.vc.Dec(childOld)
            childType = childObj.eClass.name
            SI = 0.0
            changes = []
            ### 1 NAME
            dSIName = self.__SimilarityIndexName(obj, childOld)
            # print('### 1 NAME:', dSI)
            if not dSIName == 0.25:
                changes.append('N')
            ### 2 REFERENCES
            dSIRef = self.__SimilarityIndexReferences(obj, childOld)
            # print('### 2 REFERENCES:', dSI)
            if not dSIRef == 0.25:
                changes.append('R')
            # 3 ATTRIBUTES
            dSIAttr = self.__SimilarityIndexAttributes(obj, childOld)
            # print('### 3 ATTRIBUTES:', dSI)
            if not dSIAttr == 0.25:
                changes.append('A')
            # 4 INDEX
            dSIIndex = self.__SimilarityIndexPosition(obj, childOld)
            # print('### 4 INDEX:', dSI)
            if not dSIIndex == 0.25:
                changes.append('I')
            # append to SI array rounded
            SI = dSIName + dSIRef + dSIAttr + dSIIndex
            # print('### End of CSI Loop:', dSIName, dSIRef, dSIAttr, dSIIndex)
            allSI.append(round(SI, 2))
            allChanges.append(changes)
            # if SI >= 0.99: # we found an identical object, so no need to continue
            #     break
        # return all SI and the corresponding objects
        return [allSI, childrenOld, allChanges]

    ''' CLASS ACESSORS '''
    
    def Class(self,obj):
        eObj = self.vc.Dec(obj)
        res = self.__ResolveAndEnc(eObj.eClass)
        return res
    
    def ClassName(self,obj):
        eObj = self.vc.Dec(obj)
        res = eObj.eClass.name
        return res
    
    def Package(self,clazz):
        res = None
        eClass = self.vc.Dec(clazz)
        if(isinstance(eClass,EClassifier)):
            res = self.__ResolveAndEnc(eClass.eContainer())
        else:
            raise EoqError(0,"Package works only for class objects")
        return res
    
    def Supertypes(self,clazz):
        res = []
        eClass = self.vc.Dec(clazz)
        #find the root package
        if(isinstance(eClass,EClass)):
            res = [self.__ResolveAndEnc(s) for s in eClass.eSuperTypes]
        else:
            raise EoqError(0,"Supertypes works only for class objects")
        return res
    
    def AllSupertypes(self,clazz):
        res = []
        eClass = self.vc.Dec(clazz)
        #find the root package
        if(isinstance(eClass,EClass)):
            res = [self.__ResolveAndEnc(s) for s in eClass.eAllSuperTypes()]
        else:
            raise EoqError(0,"All Supertypes works only for class objects")
        return res
    
    def Implementers(self,clazz):
        res = []
        eClass = self.vc.Dec(clazz)
        if(isinstance(eClass,EClass)):
            #find the root package
            rootPackage = eClass.eContainer()
            container = rootPackage.eContainer()
            while(isinstance(container,EPackage)):
                rootPackage = container
                container = rootPackage.eContainer()
            #find the implementers 
            res = [self.__ResolveAndEnc(c) for c in rootPackage.eAllContents() if ((type(c) == EClass) and (eClass in c.eSuperTypes))]
        else:
            raise EoqError(0,"Implementers works only for class objects")
        return res
    
    def AllImplementers(self,clazz):
        res = []
        eClass = self.vc.Dec(clazz)
        if(isinstance(eClass,EClass)):
            #find the root package
            rootPackage = eClass.eContainer()
            container = rootPackage.eContainer()
            while(isinstance(container,EPackage)):
                rootPackage = container
                container = rootPackage.eContainer()
            #find the implementers 
            res = [self.__ResolveAndEnc(c) for c in rootPackage.eAllContents() if ((type(c) == EClass) and (eClass in c.eAllSuperTypes()))]
        else:
            raise EoqError(0,"All implementers works only for class objects")
        return res
    
    def GetParent(self,obj):
        res = self.__ResolveAndEnc(self.vc.Dec(obj).eContainer())
        return res
    
    def GetAllParents(self,obj):
        res = []
        eObj = self.vc.Dec(obj)
        parent = eObj.eContainer()
        while(parent):
            res.append(self.__ResolveAndEnc(parent))
            parent = parent.eContainer()
        res.reverse() #reverse from earliest anchestor to the child
        return res
    
    def GetAssociates(self,obj,root):
        eRes =  []
        eObj = self.vc.Dec(obj)
        eRoot = self.vc.Dec(root)
        
        allReferencesLut = {}
        
        eChildsOfRoot = eRoot.eAllContents()
        for eChild in eChildsOfRoot:
            eClass = eChild.eClass
            try: 
                #eReferences = self.allReferencesLut[eClass]
                eReferences = allReferencesLut[eClass]
            except KeyError:
                eReferences = [r for r in eChild.eClass.eAllReferences() if not r.containment]
                #self.allReferencesLut[eClass] = eReferences
                allReferencesLut[eClass] = eReferences
            for r in eReferences:
                if(isinstance(eObj,r.eType)):
                    rVal = eChild.eGet(r.name)
                    if r.upperBound==1: #single ref
                        #rObj = self.__ResolveProxyAndBuildInClasses(rVal)
                        rObj = self.mdb.ResolveProxy(rVal)
                        if(eObj == rObj):
                            eRes.append(eChild)
                    else:
                        rObjs = rVal
                        for rObj in rObjs:
                            #rObj = self.__ResolveProxyAndBuildInClasses(rObj)
                            rObj = self.mdb.ResolveProxy(rObj)
                            if(eObj == rObj):
                                eRes.append(eChild)                           
        return self.__RemoveNullRefs([self.__ResolveAndEnc(o) for o in eRes])
    
    def GetIndex(self,obj):
        eObj = self.vc.Dec(obj)
        res = 0
        f = eObj.eContainmentFeature()
        if(None==f or f.upperBound == 1):
            res = None ## denotes the index makes no sense for single object references
        else: #index must be determined by backwards search
            #this backward search seems not optimal
            containingIndex = 0 #Eoq indicies start at 0
            container = eObj.eContainer()
            for sibling in container.eGet(f):
                if(sibling==eObj):
                    res = containingIndex
                    break;
                containingIndex = containingIndex+1
        return res
    
    def GetContainingFeature(self,obj):
        eObj = self.vc.Dec(obj)
        res = None
        f = eObj.eContainmentFeature()
        if(f):
            res = self.__ResolveAndEnc(f)
        else:
            res = None
        return res
    
    #def IsObject(self,value,encoder):
    #    return isinstance(encoder.decode(value),EObject)
        
    
    def GetAllChildrenOfType(self,obj,clazz):
        res = []
        eObj = self.vc.Dec(obj)
        childs = eObj.eAllContents()
        searchlist = chain(iter([eObj]),childs)
        if(isinstance(clazz,str)):
            className = clazz
            res = [self.__ResolveAndEnc(e) for e in searchlist if self.__IsType(e,className)]
        else:
            eClass = self.vc.Dec(clazz)
            res = [self.__ResolveAndEnc(e) for e in searchlist if e.eClass == eClass]
        return res
    
    def GetAllChildrenInstanceOfClass(self,obj,clazz):
        res = []
        eObj = self.vc.Dec(obj)
        childs = eObj.eAllContents()
        searchlist = chain(iter([eObj]),childs)
        if(isinstance(clazz,str)):
            className = clazz
            res = [self.__ResolveAndEnc(e) for e in searchlist if self.__IsInstanceOf(e,className)]
        else:
            eClass = self.vc.Dec(clazz)
            res = [self.__ResolveAndEnc(e) for e in searchlist if isinstance(e, eClass)]
        return res
    
    def GetAllFeatures(self,obj):
        res = [self.__ResolveAndEnc(x) for x in self.vc.Dec(obj).eClass.eAllStructuralFeatures()]
        return res
    
    def GetAllFeatureNames(self,obj):
        res = [x.name for x in self.vc.Dec(obj).eClass.eAllStructuralFeatures()]
        return res
    
    def GetAllFeatureValues(self,obj):
        eObj = self.vc.Dec(obj)
        res = [((self.__ResolveAndEnc(eObj.eGet(x)) if (x.upperBound==1) else self.__RemoveNullRefs([self.__ResolveAndEnc(c) for c in eObj.eGet(x)])))  for x in eObj.eClass.eAllStructuralFeatures()]
        return res
    
    def GetAllAttributes(self,obj):
        eObj = self.vc.Dec(obj)
        res = [self.__ResolveAndEnc(x) for x in eObj.eClass.eAllAttributes()]
        return res
    
    def GetAllAttributeNames(self,obj):
        eObj = self.vc.Dec(obj)
        res = [x.name for x in eObj.eClass.eAllAttributes()]
        return res
    
    def GetAllAttributeValues(self,obj):
        eObj = self.vc.Dec(obj)
        attributes = [x for x in eObj.eClass.eAllAttributes()]
        res = [ self.__ResolveAndEnc(eObj.eGet(a)) if (a.upperBound==1) else [self.__ResolveAndEnc(c) for c in eObj.eGet(a)] for a in attributes]
        return res
    
    def GetAllReferences(self,obj):
        eObj = self.vc.Dec(obj)
        res = [self.__ResolveAndEnc(x) for x in eObj.eClass.eAllReferences()]
        return res
    
    def GetAllReferenceNames(self,obj):
        eObj = self.vc.Dec(obj)
        res = [x.name for x in eObj.eClass.eAllReferences()]
        return res
    
    def GetAllReferenceValues(self,obj):
        eObj = self.vc.Dec(obj)
        references = [x for x in eObj.eClass.eAllReferences()]
        res = [ self.__ResolveAndEnc(eObj.eGet(a)) if (a.upperBound==1) else self.__RemoveNullRefs([self.__ResolveAndEnc(c) for c in eObj.eGet(a)]) for a in references]
        return res
    
    def GetAllContainments(self,obj):
        eObj = self.vc.Dec(obj)
        res = [self.__ResolveAndEnc(x) for x in eObj.eClass.eAllReferences() if x.containment]
        return res
    
    def GetAllContainmentNames(self,obj):
        eObj = self.vc.Dec(obj)
        res = [x.name for x in eObj.eClass.eAllReferences() if x.containment]
        return res
    
    def GetAllContainmentValues(self,obj):
        eObj = self.vc.Dec(obj)
        containments = [x for x in eObj.eClass.eAllReferences() if x.containment]
        #res = [ [self.__ResolveAndEnc(c) for c in eObj.eGet(a)] for a in containments if (a.upperbound>1) else valueCodec(eObj.eGet(a))]
        res = [ (self.__ResolveAndEnc(eObj.eGet(a)) if (a.upperBound==1) else [self.__ResolveAndEnc(c) for c in eObj.eGet(a)]) for a in containments]  
        return res
    
    '''
        PRIVATE METHODS
    '''
   
    def _OnMdbEvents(self,evts,src):
        self.NotifyObservers(evts, src)
        
    def __GetClassByName(self,packageName,className):
        try:
            pack = self.mdb.GetMetamodel(packageName)
            eClass = pack.getEClassifier(className)
        except:
            raise EoqError(0,"Unknown package %s or class %s."%(packageName,className))
        return eClass
        
    def __CreateEClassInstance(self,eClass,constructorArgs=[]):
        eObj = None
        if(0<len(constructorArgs)):
            eObj = eClass(*constructorArgs)
        else:
            eObj = eClass()
        return eObj
   
    def __IsType(self,obj,className):
        return (obj.eClass.name==className)
   
    def __IsInstanceOf(self,obj,className):
        result = self.__IsType(obj,className)
        if(not result):
            for superType in obj.eClass.eAllSuperTypes():
                if(superType.name==className):
                    result = True
                    break
            if('EObject'==className):
                result = isinstance(obj,EObject)
        return result
    
    def __ECloneClass(self,eObj):
        clazz = eObj.eClass
        clone = clazz()
            
        return clone
    
    def __ECloneAttributes(self,eObj):
        clone = self.__ECloneClass(eObj)
        clazz = eObj.eClass
        attributes = clazz.eAllAttributes()
        for attribute in attributes:
            if(attribute.many):
                for attributeValue in eObj.eGet(attribute):
                    clone.eGet(attribute).add(attributeValue)
            else:
                clone.eSet(attribute,eObj.eGet(attribute))    
        return clone
    
    def __ECloneFlat(self,eObj):
        clone = self.__ECloneAttributes(eObj)
        clazz = eObj.eClass
        references = clazz.eAllReferences()
        for reference in references:
            if(not reference.containment):
                if(reference.many):
                    for refObj in eObj.eGet(reference):
                        clone.eGet(reference).add(refObj)
                else:
                    clone.eSet(reference,eObj.eGet(reference))
        return clone
    
    def __ECloneDeep(self,eObj,copyReferences=True):
        clone = self.__ECloneAttributes(eObj)
        clazz = eObj.eClass
        references = clazz.eAllReferences()
        for reference in references:
            if(reference.containment):
                if(reference.many):
                    for child in eObj.eGet(reference):
                        clonedChild = self.__ECloneDeep(child,copyReferences)
                        clone.eGet(reference).add(clonedChild)
                else:
                    child = eObj.eGet(reference)
                    if(child): #only clone non empty single containments
                        clonedChild = self.__ECloneDeep(child,copyReferences)
                        clone.eSet(reference,clonedChild)
            elif(copyReferences): #non containments
                if(reference.many):
                    for refObj in eObj.eGet(reference):
                        clone.eGet(reference).add(refObj)
                else:
                    clone.eSet(reference,eObj.eGet(reference))
            
        return clone
    
    def __ECloneFull(self,eObj):
        clone = self.__ECloneDeep(eObj,False)
        #clazz = eObj.eClass
        self.__ECloneFullReferenceUpdater(eObj,clone,eObj,clone)            
        return clone
    
    def __ECloneFullReferenceUpdater(self,eObj,clonedEObject,root,clone):
        clazz = eObj.eClass
        references = clazz.eAllReferences()
        for reference in references:
            if(reference.containment):
                if(reference.many):
                    nChilds = len(eObj.eGet(reference))
                    for i in range(nChilds):
                        child = eObj.eGet(reference)[i]
                        clonedChild = clonedEObject.eGet(reference)[i]
                        self.__ECloneFullReferenceUpdater(child, clonedChild, root, clone)
                else:
                    child = eObj.eGet(reference)
                    if(child): #only clone non empty single containments
                        clonedChild = clonedEObject.eGet(reference)
                        self.__ECloneFullReferenceUpdater(child, clonedChild, root, clone)
            else: #non containments
                if(reference.many):
                    for oldRef in eObj.eGet(reference):
                        newRef = self.__ECloneFullFindCorrespondingReference(oldRef,root,clone)
                        clonedEObject.eGet(reference).add(newRef)
                else:
                    oldRef = eObj.eGet(reference)
                    if(oldRef): #null references need no cloning
                        newRef = self.__ECloneFullFindCorrespondingReference(oldRef,root,clone)
                        clonedEObject.eSet(reference,newRef)
        return clone
    
    def __ECloneFullFindCorrespondingReference(self,oldRef,root,clone):
        newRef = oldRef
        if(self.__ECloneFullIsParentOf(oldRef,root)): #we only need an new reference if the root contains the referred object
            featurePath = self.__ECloneFullGetPathFromTo(root,oldRef)
            newRef = clone
            for p in featurePath: #p is a tuple (featureName, many, index)
                feature = p[0]
                if(p[1]): #many
                    index = p[2]
                    newRef = newRef.eGet(feature)[index]
                else: #single
                    newRef = newRef.eGet(feature)
        return newRef
    
    def __ECloneFullIsParentOf(self,child,possibleParent):
        if(child == possibleParent) :
            return True
        parent = child.eContainer()
        if(parent and isinstance(parent, EObject)):
            return self.__ECloneFullIsParentOf(parent, possibleParent)
        return False #has no parent any more, return false
    
    def __ECloneFullGetPathFromTo(self,anchestor,child):
        featurePath = []
        if(anchestor!=child):
            parent = child.eContainer()
            if(parent and isinstance(parent, EObject)):
                feature = child.eContainmentFeature()
                featureName = feature.name
                many = feature.many
                index = 0
                if(many):
                    index = parent.eGet(featureName).index(child)
                featurePath = [(featureName,many,index)]
                featurePath = self.__ECloneFullGetPathFromTo(anchestor,parent) + featurePath
        return featurePath #has no parent any more, return false
    
#     def __ResolveProxyAndBuildInClasses(self,obj): 
#         if(isinstance(obj, EProxy)):
#             try: #resolve can fail if files have been modified or objects been deleted before the proxy has been resolved
#                 obj.force_resolve()
#                 obj = obj._wrapped #remove the outer proxy
#             except Exception as e:
#                 traceback.print_exc()
#                 print("WARN: Unresolvable proxy found and removed")
#                 obj = None;     
#         if(isinstance(obj, (MetaEClass,type,types.ModuleType))): #this is necessary to mask compiled model instances
#             obj = obj.eClass
#         return obj
#     
    def __ResolveAndEnc(self,obj):
        return self.vc.Enc(self.mdb.ResolveProxy(obj))
    
    def __RemoveNullRefs(self,objs):
        return list(filter(None,objs))
    
    def __SimilarityIndexName(self, obj, childOld):
        dSI = 0.0
        eObj     = self.vc.Dec(obj)
        childObj = self.vc.Dec(childOld)
        # is there a name attribute and is it identical? SI += 0.25
        if hasattr(childObj,'name') and childObj.name:
            if childObj.name == eObj.name:
                dSI = 0.25
        # nameless objects need to get + 0.25 if eObj also has no name
        elif (not hasattr(childObj, 'name') or not childObj.name) and (not hasattr(eObj, 'name') or not eObj.name):
            dSI = 0.25
        return dSI


    def __SimilarityIndexReferences(self, obj, childOld):
        dSI = 0.0
        eObj     = self.vc.Dec(obj)
        childObj = self.vc.Dec(childOld)
        referencesObj          = self.GetAllReferences(obj)
        referenceNamesObj      = self.GetAllReferenceNames(obj)
        referenceValuesObj     = self.GetAllReferenceValues(obj)
        # collect the number of valid referenced objects (obj)
        nValidRefValues = 0
        for ref in referenceValuesObj:
            if isinstance(ref, list):
                if len(ref) > 0:
                    nValidRefValues += 1
            else:
                nValidRefValues += 1
        # collect the names of the referenced objects (childOld)
        referencesChildOld      = self.GetAllReferences(childOld)
        referenceNamesChildOld  = self.GetAllReferenceNames(childOld)
        referenceValuesChildOld = self.GetAllReferenceValues(childOld)
        # iterate all references of obj (from here on abbreviated by F)
        # print('-- SIRef: Old:', childOld, 'New:', obj)
        for refF, refNameF, refValueF in zip(referencesObj, referenceNamesObj, referenceValuesObj):
            # match the reference value
            # print('- Trying to match reference:', refNameF, 'with values:', refValueF)
            matchedReferenceName = False
            # iterate all references of childOld and find the corresponding reference
            for i, [refO, refNameO, refValueO] in enumerate(zip(referencesChildOld, referenceNamesChildOld, referenceValuesChildOld)):
                if refNameO == refNameF:
                    matchedReferenceName = True
                    # print('--- Matched:', refNameO, refValueO)
                    # now i is the index of the matched reference
                    break
            # everything needs to be in lists
            if not isinstance(referenceValuesObj[i], list):
                referenceValuesObj[i] = [referenceValuesObj[i]]
            if not isinstance(referenceValuesChildOld[i], list):
                referenceValuesChildOld[i] = [referenceValuesChildOld[i]]
            # if the reference is matched and both have referenced objects, ...
            # ... we can compare the referenced objects' names
            if (matchedReferenceName 
                and len(referenceValuesObj[i]) > 0 
                and len(referenceValuesChildOld[i]) > 0):
                matchcounter = 0
                for objF in referenceValuesObj[i]:
                    decObjF = self.vc.Dec(objF)
                    if hasattr(decObjF, 'name') and decObjF.name:
                        nameF = decObjF.name
                    else:
                        nameF = 'noname'
                    matchedReference = False
                    for j, objO in enumerate(referenceValuesChildOld[i]):
                        # decode and compare
                        decObjO = self.vc.Dec(objO)
                        if hasattr(decObjO, 'name') and decObjO.name:
                            nameO = decObjO.name
                        else:
                            nameO = 'noname'
                        # see if we matched the reference
                        if nameO == nameF:
                            matchedReference = True
                            break
                    if matchedReference:
                        # print('--- Matched objects.  ',
                        # 	'Reference:', refNameF, 'Old:', nameO, 'New:', nameF)
                        matchcounter += 1
                    else:
                        pass
                        # print('--- Unmatched objects.',
                        # 	'Reference:', refNameF, 'Old:', nameO, 'New:', nameF)
                # print('- End of object comparison. Matchcounter:', matchcounter,
                #     'number of objects from this reference:',
                #     len(referenceValuesObj[i]))
                dSI += (matchcounter/len(referenceValuesObj[i]))*0.25/nValidRefValues
        if not any(referenceValuesObj) and not any(referenceValuesChildOld):
            # if both do not have references -> they have identical references
            dSI = 0.25
        return round(dSI, 2)

    def __SimilarityIndexAttributes(self, obj, childOld):
        dSI = 0
        eObj     = self.vc.Dec(obj)
        childObj = self.vc.Dec(childOld)
        attributeNamesObj  = self.GetAllAttributeNames(obj)
        attributeValuesObj = self.GetAllAttributeValues(obj)
        if 'name' in attributeNamesObj:
            attributeValuesObj.pop(attributeNamesObj.index('name'))
            attributeNamesObj.remove('name')
        attributeNamesChildOld  = self.GetAllAttributeNames(childOld)
        attributeValuesChildOld = self.GetAllAttributeValues(childOld)
        if 'name' in attributeNamesChildOld:
            attributeValuesChildOld.pop(attributeNamesChildOld.index('name'))
            attributeNamesChildOld.remove('name')
        nAttrs = len(attributeNamesObj)
        for (nameF, valueF) in zip(attributeNamesObj, attributeValuesObj):
            for (nameO, valueO) in zip(attributeNamesChildOld, attributeValuesChildOld):
                found = False
                if nameF == nameO:
                    if valueF == valueO:
                        dSI += 0.25/nAttrs
                        found = True
                        break
        if not attributeNamesObj and not attributeNamesChildOld:
            # if both do not have attributes -> they have identical attributes
            dSI = 0.25
        return round(dSI, 2)

    def __SimilarityIndexPosition(self, obj, childOld):
        dSI = 0
        eObj     = self.vc.Dec(obj)
        childObj = self.vc.Dec(childOld)
        if self.GetIndex(childObj) == self.GetIndex(eObj):
            dSI += 0.25
        return dSI
    
