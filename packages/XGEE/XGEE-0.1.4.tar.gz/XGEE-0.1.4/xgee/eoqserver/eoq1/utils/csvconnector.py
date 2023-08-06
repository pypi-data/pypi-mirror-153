'''
Example script demonstrating the use of the Essential Object Queries to read and modify ECORE models. 

Bjoern Annighoefer 2018
'''
from ..model import DomainA
from ..domains import SimplePythonDomainWrapper

import fileinput

#ERROR HANLDERS
class EoqCsvError(Exception):
    pass

class EoqCsvReadError(EoqCsvError):
    def __init__(self, errortype, message, eoqstring):
        self.errortype = errortype
        self.message = message
        self.eoqstring = eoqstring
        
           
#MAIN CLASS
class CsvConnector: 
    def __init__(self,eoq : DomainA):
        self.elementIdLOT = {} #lookup table for elements ids
        self.elementLOT = {} #lookup table for elements
        self.idAttributeLOT = {} #lookup table id attributes
        self.dc = ';' #delimiter char
        self.qc = '"' #quote char
        self.sc = ',' #sub delimiter sign
        self.eoqOriginal = eoq
        self.eoq = SimplePythonDomainWrapper(eoq) #Hack to ensure backwards compatibility. TODO: Change to command interface later
     
    # splits a string by the given delimiter. but respects quote characters (qc) 
    # for encapsulating strings containing the delimiter characters (dc)
    def _csvSplit(self,txt):
        QUOTE_START = 1
        DELIM_START = 2
        state = DELIM_START
        b = 0 #begin of current substring
        e = 0 #end of current substring
        
        segments = []
        
        n = len(txt)
        for i in range(n):
            c = txt[i]
            if(DELIM_START == state):
                if(self.dc == c):
                    segment = txt[b:e]
                    segments.append(segment)
                    b = i+1
                elif(self.qc == c):
                    b = i+1
                    state = QUOTE_START
                else:
                    e = i+1
            elif(QUOTE_START == state):
                if(self.qc == c):
                    state = DELIM_START
                else:
                    e = i+1
        
        if(QUOTE_START == state):
            raise EoqCsvReadError('CVS split','Unbalanced quote starting at position %d.'%(b),txt)
        
        segment = txt[b:n]
        segments.append(segment)
    
        return segments;
    
    def _tanslateArray(self,strArray,translationDictionary):
        n = len(strArray)
        for i in range(n):
            if strArray[i] in translationDictionary:
                strArray[i] = translationDictionary[strArray[i]]
        return strArray
    
    def _writeLine(self,lineArray,dc,file):
        n = len(lineArray)
        if(n>0):
            print(self._csvOutputSegment(lineArray[0]),end="",file=self.file)
        for i in range(1,n):
            print("%c%s"%(dc,self._csvOutputSegment(lineArray[i])),end="",file=self.file)
        print("",file=self.file)
            
    
    #adds quote to a segment if it includes forbidden chars like a delimiter
    def _csvOutputSegment(self,segmentTxt):
        if(self.dc in segmentTxt or ' ' in segmentTxt):
            return '%c%s%c'%(self.qc,segmentTxt,self.qc)
        return segmentTxt #do nothing by default
    
    def getIdAttribute(self,element):
        idAttribute = None
        #clazz = element.eClass
        clazz = self.eoq.Retrieve(element,'(EObject:1)/eClass')
        if(clazz in self.idAttributeLOT):
            idAttribute = self.idAttributeLOT[clazz]
        else:
            idAttribute = self.eoq.Retrieve(clazz,'(EClass:1)/eAttributes{iD=true}')
            if(None == idAttribute):
                idAttribute = self.eoq.Retrieve(clazz,'(EClass:_)/eSuperTypes<-1>/eAttributes{iD=true}')
                if(len(idAttribute)>0):
                    idAttribute = idAttribute[0] #take only the first one. Multiple id attributes are not supported.
        self.idAttributeLOT[clazz] = idAttribute
        return idAttribute
          
    #return an element id
    def getElementId(self,element):
        if(element.v in self.elementIdLOT):
            return self.elementIdLOT[element.v]
        
        newElementId = None
        idAttribute = self.getIdAttribute(element);
        idAttributeName = self.eoq.Retrieve(idAttribute,'(EAttribute:1)/name')
        if(idAttribute):
            idValue = self.eoq.Retrieve(element,'(EObject:1)/%s'%(idAttributeName))
            if(idValue):
                if(idValue in self.elementLOT):
                    existingElement = self.elementLOT[idValue]
                    print('WARNING: %s seems to have the non unique id %s. %s has the same id. Using the path instead.'%(element,idValue,existingElement))
                else:
                    newElementId = str(idValue)
                    self.elementLOT[newElementId] = element.v
        if(None == newElementId):
            #no id available, so generate one by the path
            containerId = self.getContainerId(element)
            containedPath = self.getContainingPath(element,1)
            newElementId = "%s/%s"%(containerId,containedPath)
                
        self.elementIdLOT[element.v] = newElementId
        return newElementId
    
    def getContainerId(self,element):
        container = self.eoq.Retrieve(element,'(EObject:1)@CONTAINER')
        if(container):
            return self.getElementId(container)
        return ''
    
        '''
    retrieves the path of an object
    depth is the number of anchestors to start from (use -1 to obtain the absolute path)
    '''
    def getContainingPath(self,obj,depth):
        path = self.eoq.Retrieve(obj,'(EObject:1)@CONTAININGFEATURENAME')
        index = self.eoq.Retrieve(obj,'(EObject:1)@INDEX')
        if(index>0):
            path += '[%d]'%(index)
                    
        depth = depth-1 #reduce depth if one level was resolved
        
        if(depth!=0):
            container = self.eoq.Retrieve(obj,'(EObject:1)@CONTAINER')
            path = "%s/%s"%(self.getContainingPath(container,depth),path)
        
        return path

    def storeClass(self,package,clazz,gcmRoot,ommitContainer,ommitContainingPath,attributeNameDictionary,classSectionBegin,classSectionEnd,ommitClassInfo):
        clazzName = self.eoq.Retrieve(clazz,'(EClass:1)/name')
        allInstances = self.eoq.Retrieve(gcmRoot,"(*:*)$%s"%(clazzName))
        #print all attribute names
        if(0 < len(allInstances)):
            #allAttributes = clazz.eAllAttributes()
            ownAttributes = self.eoq.Retrieve(clazz,'(EClass:*)/eAttributes')
            superTypeAttributes = self.eoq.Retrieve(clazz,'(EClass:_)/eSuperTypes<-1>/eAttributes')
            allAttributes = ownAttributes+superTypeAttributes
            #allReferences = clazz.eAllReferences()
            ownNonContainingReferences = self.eoq.Retrieve(clazz,'(EClass:*)$EReference{containment=false}')
            superTypeNonContainingReferences = self.eoq.Retrieve(clazz,'(EClass:_)/eSuperTypes<-1>$EReference{containment=false}') 
            allNonContainingReferences = ownNonContainingReferences + superTypeNonContainingReferences

            packageNsUri = self.eoq.Retrieve(package,'(EPackage:1)/nsURI')
            className = self.eoq.Retrieve(clazz,'(EClass:1)/name')
            
            headerArray = []
            
            print(classSectionBegin,end="",file=self.file)
            if(False==ommitClassInfo):
                print("#%c%s%c%s"%(self.dc,self._csvOutputSegment(packageNsUri),self.dc,self._csvOutputSegment(className)),file=self.file)
            if(False==ommitContainer):
                headerArray.append("container")
                #print("container",end="",file=self.file)
            if(False==ommitContainingPath):
                headerArray.append("containedPath")
            #print("container%ccontainedPath"%(self.dc),end="",file=self.file)
            for attribute in allAttributes:
                attributeName = self.eoq.Retrieve(attribute,'(EAttribute:1)/name')
                headerArray.append(attributeName)
                #print("%c%s"%(self.dc,self._csvOutputSegment(attributeName)),end="",file=self.file)
            for reference in allNonContainingReferences:
                referenceName = self.eoq.Retrieve(reference,'(EReference:1)/name')
                headerArray.append(referenceName)
                #print("%c%s"%(self.dc,self._csvOutputSegment(referenceName)),end="",file=self.file)
            #replace elements with names from the dictionary
            if(len(attributeNameDictionary)>0):
                headerArray = self._tanslateArray(headerArray,attributeNameDictionary)
            self._writeLine(headerArray,self.dc,self.file)
            #print("",file=self.file)
            #print all values
            for instance in allInstances:
                lineArray = []
                if(False==ommitContainer):
                    lineArray.append(self.getContainerId(instance))
                    #print("container",end="",file=self.file)
                if(False==ommitContainingPath):
#                     featureName = self.eoq.Retrieve(instance,'(EObject:1)@CONTAININGFEATURENAME')
#                     lineArray.append(featureName)
                    lineArray.append(self.getContainingPath(instance,1))
                #print('%s%c%s'%(self._csvOutputSegment(self.getContainerId(eoq,instance)),self.dc,self._csvOutputSegment(self.eoq.EoqPath(instance,1))),end="",file=self.file)
                for attribute in allAttributes:
                    attributeName = self.eoq.Retrieve(attribute,'(EAttribute:1)/name')
                    attributeValue = self.eoq.Retrieve(instance,'(%s:1)/%s'%(className,attributeName))
                    attributeStr = ''
                    if(None!=attributeValue):
                        attributeStr = str(attributeValue)
                    lineArray.append(attributeStr)
                    #print('%c%s'%(self.dc,self._csvOutputSegment(attributeStr)),end="",file=self.file)
                for reference in allNonContainingReferences:
                    referenceString = ''
                    referenceName = self.eoq.Retrieve(reference,'(EReference:1)/name')
                    referedElements = self.eoq.Retrieve(instance,'(%s:*)/%s'%(className,referenceName))
                    if(not isinstance(referedElements,list)):
                        referedElements = [referedElements]
                    nReferedElements = len(referedElements)
                    if(nReferedElements>0 and referedElements[0]):
                        referenceString += self.getElementId(referedElements[0])
                    for i in range(1,nReferedElements):
                        referenceString += self.sc+self.getElementId(referedElements[i])
                    lineArray.append(referenceString)
                    #print('%c%s'%(self.dc,self._csvOutputSegment(referenceString)),end="",file=self.file)
                self._writeLine(lineArray,self.dc,self.file)
                #print('',file=self.file)
            print(classSectionEnd,end="",file=self.file)
        

    def storePackage(self,package,gcmRoot,ommitRootElement,ommitContainer,ommitContainingPath,attributeNameDictionary,classSectionBegin,classSectionEnd,ommitClassInfo):
        #allClazzes = package.eClassifiers
        allClazzes = self.eoq.Retrieve(package,'(EPackage:_)/eClassifiers$EClass{abstract=false}')
        i = 0
        for clazz in allClazzes:
            if(i==0 and ommitRootElement):
                i += 1
            else:
                self.storeClass(package,clazz,gcmRoot,ommitContainer,ommitContainingPath,attributeNameDictionary,classSectionBegin,classSectionEnd,ommitClassInfo)
                i +=1
            
        #look for subpackages
        allSubpackages = self.eoq.Retrieve(package,'(EPackage:*)/eSubpackages')
        #allSubpackages = package.eSubpackages
        for subpackage in allSubpackages:
            self.storePackage(subpackage, gcmRoot,False,ommitContainer,ommitContainingPath,attributeNameDictionary,classSectionBegin,classSectionEnd,ommitClassInfo)
            
    def SaveAsCsv(self,modelRoot,filename,header='',ommitRootElement=False,ommitContainer=False,ommitContainingPath=False,attributeNameDictionary={},classSectionBegin='',classSectionEnd='',ommitClassInfo=False):
       
        #reset members
        self.elementIdLOT = {}
        self.elementLOT = {}
        self.idAttributeLOT = {}
        
        mainclass = self.eoq.Retrieve(modelRoot,'(*:1)/eClass')
        mainpackage = self.eoq.Retrieve(mainclass,'(*:1)/ePackage')
        
        with open(filename, 'w') as self.file:
            print(header,end="",file=self.file)
            self.storePackage(mainpackage,modelRoot,ommitRootElement,ommitContainer,ommitContainingPath,attributeNameDictionary,classSectionBegin,classSectionEnd,ommitClassInfo)
            
    def LoadFromCsv(self,filename):
        
        #CONSTANTS
        CLASS_OR_ELEMENT_LINE = 1
        FEATURE_LINE = 2
        
        #reset members
        self.elementIdLOT = {}
        self.elementLOT = {}
        self.idAttributeLOT = {}
        
        #the return value
        gcmRoot = None
        
        with fileinput.input(files=(filename)) as f:
            packageNsUri = None
            classname = None
            allAttributeNames = []
            allAttributeDataTypes = []
            
            
            featureColumns = []
            attributeColumns = []
            attributeColumnIndicies = []
            attributeColumnsType = []
            attributeDataTypeTranslators = []
            nonContainingReferenceColumns = []
            nonContainingReferenceColumnIndicies = []
            nFeatureColumns = 0
            clazz = None
            idAttribute = None
            idAttributeName = None
            
            state = CLASS_OR_ELEMENT_LINE
            
            n = 1;
            
            tmpElementInfos = []
            
            for line in f:
                #remove line endings
                #line = lineEndRemoverRe.sub(line,'')
                line = line.splitlines()[0]
                
                #create all classes 
                if(CLASS_OR_ELEMENT_LINE==state):
                    if('#'==line[0]):
                        segments = self._csvSplit(line)
                        if(3!=len(segments)):
                            raise EoqCsvReadError('LoadFromCsv 1','Found invalid package or class identifier in line %d'%(n),line)
                        packageNsUri = segments[1]
                        classname = segments[2]
                        dummyElement = self.eoq.Create(packageNsUri,classname) #this element is only for test purposes and to obtain the class information
                        if(None==dummyElement):
                            raise EoqCsvReadError('LoadFromCsv 2','Could not create instance of class %s from package %s line %d'%(classname,packageNsUri,n),line)
                        clazz = self.eoq.Retrieve(dummyElement,'(EObject:1)/eClass')
                        ownAttributes = self.eoq.Retrieve(clazz,'(EClass:*)/eAttributes')
                        superTypeAttributes = self.eoq.Retrieve(clazz,'(EClass:_)/eSuperTypes<-1>/eAttributes')
                        
                        allAttributes = ownAttributes+superTypeAttributes
                        allAttributeNames = self.eoq.Retrieve(allAttributes,'(*:*)/name')
                        allAttributeDataTypes = self.eoq.Retrieve(allAttributes,'(*:*)/eType/name')
                        ownNonContainingReferenceNames = self.eoq.Retrieve(clazz,'(EClass:*)$EReference{containment=false}/name')
                        superTypeNonContainingReferenceNames = self.eoq.Retrieve(clazz,'(EClass:*)/eSuperTypes<-1>$EReference{containment=false}/name')
                        allNonContainingReferenceNames = ownNonContainingReferenceNames+superTypeNonContainingReferenceNames
                        
                        idAttributes = self.eoq.Retrieve(allAttributes,'(*:_)$EAttribute{iD=true}')
                        if(len(idAttributes)==1):
                            idAttribute = idAttributes[0]
                            idAttributeName = self.eoq.Retrieve(idAttribute,'(EAttribute:1)/name')
                        
                        state = FEATURE_LINE
                    else:
                        #valueStrs = line.split(';')
                        valueStrs = self._csvSplit(line)
                        nValues = len(valueStrs)
                        if(nValues!=nFeatureColumns):
                            raise EoqCsvReadError('LoadFromCsv 2','Found %d valueStrs but expected %d in line %d'%(nValues,nFeatureColumns,n),line)
                        containerId = valueStrs[0]
                        containingPath = valueStrs[1]
                        element = self.eoq.Create(packageNsUri,classname)
                        
                        #obtain the elements id
                        elementId = '%s/%s'%(containerId,containingPath)
                        
                        #write attributes
                        j = 0
                        for i in attributeColumnIndicies:
                            if('' != valueStrs[i]): #Only store something, if a value is given
                                value = attributeDataTypeTranslators[j](valueStrs[i])
                                self.eoq.Update(element,'/%s'%(featureColumns[i]),value)
                                if(idAttributeName and idAttributeName==featureColumns[i]):
                                    if(valueStrs[i] in self.elementLOT):
                                        print('WARNING: Element %s seems to have a non-unique id %s. Using the path instead'%(element,valueStrs[i]))
                                    else:
                                        elementId = valueStrs[i]
                            j = j+1
                            
                        self.elementLOT[elementId] = element       
                                
                        #extract reference values 
                        referenceValues = []
                        for i in nonContainingReferenceColumnIndicies:
                            referenceValues.append(valueStrs[i])
                                
                        #split up containing path
                        containingReferenceIsMulti = False
                        containingReferenceIndex = -1
                        containingPathSegments = containingPath.split('[')
                        containingReferenceName = containingPathSegments[0]
                        if(1<len(containingPathSegments)):
                            containingReferenceIsMulti = True
                            containingPathSegments = containingPathSegments[1].split(']')
                            containingReferenceIndex = int(containingPathSegments[0])
                                                 
                        #store the new element and some additional information for later 
                        tmpElementInformation = {'elementId':elementId, 'containerId':containerId, 'containingPath':containingPath, 'referenceValues':referenceValues, 'containingReferenceName':containingReferenceName, 'containingReferenceIsMulti':containingReferenceIsMulti, 'containingReferenceIndex':containingReferenceIndex,'nonContainingReferenceColumns':nonContainingReferenceColumns}
                        tmpElementInfos.append(tmpElementInformation)   
                        
                elif(FEATURE_LINE==state):
                    #featureColumns = line.split(';')
                    featureColumns = self._csvSplit(line)
                    nFeatureColumns = len(featureColumns)
                    if(2>nFeatureColumns):
                        raise EoqCsvReadError('LoadFromCsv 3','Line %d has %columns, but the minimum is 2'%(n,nFeatureColumns),line)
                    attributeColumns = []
                    attributeColumnIndicies = []
                    attributeColumnsType = []
                    attributeDataTypeTranslators = []
                    nonContainingReferenceColumns = []
                    nonContainingReferenceColumnIndicies = []
                    for i in range(nFeatureColumns):
                        if(featureColumns[i] in allAttributeNames):
                            j = allAttributeNames.index(featureColumns[i])
                            attributeColumns.append(f)
                            attributeColumnIndicies.append(i)
                            attributeColumnsType.append(allAttributeDataTypes[j])
                            attributeDataType = allAttributeDataTypes[j]
                            #create converter functions
                            if('EBoolean'==attributeDataType):
                                dataTypeConverter = lambda s: True
                            elif('EString'==attributeDataType):
                                dataTypeConverter = lambda s: str(s)
                            elif('EDouble'==attributeDataType):
                                dataTypeConverter = lambda s: float(s)
                            elif('EFloat'==attributeDataType):
                                dataTypeConverter = lambda s: float(s)
                            elif('EInt'==attributeDataType):
                                dataTypeConverter = lambda s: int(s)
                            elif('EDate'==attributeDataType):
                                dataTypeConverter = lambda s: str(s)
                            else:
                                dataTypeConverter = lambda s: str(s)
                            #else:
                            #    raise EoqCsvReadError('LoadFromCsv 5','Attribute %s of class %s has an unsupported data type:%s'%(featureColumns[i],classname,attributeDataType),line)
                            attributeDataTypeTranslators.append(dataTypeConverter)
                        elif(featureColumns[i] in allNonContainingReferenceNames):
                            nonContainingReferenceColumns.append(featureColumns[i])
                            nonContainingReferenceColumnIndicies.append(i)
                            
                    state = CLASS_OR_ELEMENT_LINE
                n = n+1;    
                
            #elements must be sorted by their containment
            elementInformationSortKey = lambda x: x['containerId']+'/'+x['containingReferenceName']+'%10.d'%(x['containingReferenceIndex'])
            tmpElementInfos.sort(key=elementInformationSortKey)
                
            #resolve all references
            for elementInfo in tmpElementInfos:
                elementId = elementInfo['elementId']
                containerId = elementInfo['containerId']
                #containingPath = elementInfo['containingPath']
                containingReferenceName = elementInfo['containingReferenceName']
                containingReferenceIsMulti = elementInfo['containingReferenceIsMulti']
                nonContainingReferenceColumns = elementInfo['nonContainingReferenceColumns']
                referenceValues = elementInfo['referenceValues']
                #get the element
                element = self.elementLOT[elementId]
                
                #establish the containment
                if('' == containerId and ''== containingReferenceName):
                    gcmRoot = element
                else:
                    father = None
                    if('' == containerId):
                        father = gcmRoot
                    else:
                        father = self.elementLOT[containerId]
                    if(None==father):
                        raise EoqCsvReadError('LoadFromCsv 4','Element %s has a not resolvable container id %s'%(elementId,containerId),containerId)
                    if(containingReferenceIsMulti):
                        self.eoq.Update(father,'/%s[+]'%(containingReferenceName),element) #can use plus, because elements are sorted in the right order    
                    else:
                        self.eoq.Update(father,'/%s'%(containingReferenceName),element)             
                
                #resolve all other references
                nNonContainingReferences=len(nonContainingReferenceColumns)
                for i in range(nNonContainingReferences):
                    nonContainingReferenceName = nonContainingReferenceColumns[i]
                    if(''!=referenceValues[i]):
                        referredElementIds = referenceValues[i].split(',')
                        if(1<len(referredElementIds)):
                            for referredElementId in referredElementIds:
                                referredElement = self.elementLOT[referredElementId]
                                self.eoq.Update(element,'/%s[+]'%(nonContainingReferenceName),referredElement)
                        else:
                            referredElement = self.elementLOT[referredElementIds[0]]
                            self.eoq.Update(element,'/%s'%(nonContainingReferenceName),referredElement)
                            
        return gcmRoot
            
                
            
            
        
        


