'''
Example script demonstrating the use of the Essential Object Queries to read and modify ECORE models. 

Bjoern Annighoefer 2019
'''

#new imports
from ..query.query import Qry 
from ..command.command import Get, Set, Add, Rem, Mov, Clo, Crt, Crn, Sts, Chg, Gaa, Cal, Asc, Abc, Cmp, CloModes


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
    def __init__(self,domain):
        import csv
        self.elementIdLOT = {} #lookup table for elements ids
        self.elementLOT = {} #lookup table for elements
        self.idAttributeLOT = {} #lookup table id attributes
        self.dc = ';' #delimiter char
        self.qc = '"' #quote char
        self.sc = ',' #sub delimiter sign
        self.domain = domain
        self.quoting_state = csv.QUOTE_MINIMAL
        self.omit_empty_first_column = False
        self.csvWriter = None
        self.file = None

    # splits a string by the given delimiter. but respects quote characters (qc) 
    # for encapsulating strings containing the delimiter characters (dc)
    def _csvSplit(self,txt):
        import csv

        return list(csv.reader(txt, quotechar=self.qc, delimiter=self.dc,
                                    quoting=csv.QUOTE_ALL, skipinitialspace=True))

    def _tanslateArray(self,strArray,translationDictionary):
        n = len(strArray)
        for i in range(n):
            if strArray[i] in translationDictionary:
                strArray[i] = translationDictionary[strArray[i]]
        return strArray
    
    def _writeLine(self,lineArray):
        self.csvWriter.writerow(lineArray)

# obsolete as csvwriter handles this.
    #adds quote to a segment if it includes forbidden chars like a delimiter
#    def _csvOutputSegment(self,segmentTxt):
#
#        if(self.dc in segmentTxt or ' ' in segmentTxt):
#            return '%c%s%c'%(self.qc,segmentTxt,self.qc)
#        return segmentTxt #do nothing by default
    
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
        if idAttribute:
            idValue = self.eoq.Retrieve(element,'(EObject:1)/%s'%(idAttributeName))
            if idValue:
                if idValue in self.elementLOT:
                    existingElement = self.elementLOT[idValue]
                    print('WARNING: %s seems to have the non unique id %s. %s has the same id. Using the path instead.'%(element,idValue,existingElement))
                else:
                    newElementId = str(idValue)
                    self.elementLOT[newElementId] = element.v
        if newElementId is None:
            #no id available, so generate one by the path
            containerId = self.getContainerId(element)
            containedPath = self.getContainingPath(element,1)
            newElementId = "%s/%s"%(containerId,containedPath)
                
        self.elementIdLOT[element.v] = newElementId
        return newElementId
    
    def getContainerId(self,element):
        container = self.eoq.Retrieve(element,'(EObject:1)@CONTAINER')
        if container:
            return self.getElementId(container)
        return ''
    
    '''
    retrieves the path of an object
    depth is the number of anchestors to start from (use -1 to obtain the absolute path)
    '''
    def getContainingPath(self,obj,depth):
        path = self.eoq.Retrieve(obj,'(EObject:1)@CONTAININGFEATURENAME')
        index = self.eoq.Retrieve(obj,'(EObject:1)@INDEX')
        if index > 0:
            path += '[%d]'%(index)
                    
        depth = depth-1 #reduce depth if one level was resolved
        
        if depth: # depth is not 0
            container = self.eoq.Retrieve(obj,'(EObject:1)@CONTAINER')
            path = "%s/%s"%(self.getContainingPath(container,depth),path)
        
        return path

    def storeClass(self,package,clazz,root,ommitContainer,ommitContainingPath,attributeNameDictionary,classSectionBegin,classSectionEnd,ommitClassInfo):
        # clazzName = self.eoq.Retrieve(clazz,'(EClass:1)/name')
        clazzName = self.domain.Do(Get(Qry(clazz).Pth('name')))
        # allInstances = self.eoq.Retrieve(root,"(*:*)$%s"%(clazzName))
        # allInstances = self.domain.Do(Get(Qry(root).Sel(Qry().Equ(clazzName))))
        #allInstances = self.domain.Do(Get(Qry(root).Met('FEATUREVALUES').Sel(Qry(root).Met('FEATURENAMES').Equ(clazzName))))
        allInstances = self.domain.Do(Get(Qry(root).Cls(clazzName)))
        #print all attribute names
        if allInstances:
            #allAttributes = clazz.eAllAttributes()
            # ownAttributes = self.eoq.Retrieve(clazz,'(EClass:*)/eAttributes')
            ownAttributes = self.domain.Do(Get(Qry(clazz).Pth('eAttributes')))
            # superTypeAttributes = self.eoq.Retrieve(clazz,'(EClass:_)/eSuperTypes<-1>/eAttributes')
            #todo rekursiver supertype muss hier noch einmal überarbeitet werden
            superTypeAttributes = self.domain.Do(Get(Qry(clazz).Pth('eSuperTypes').Pth('eAttributes')))
            allAttributes = ownAttributes+superTypeAttributes
            #allReferences = clazz.eAllReferences()
            # todo hier muss der befehl noch einmal ausgearbeitet weden
            # ownNonContainingReferences = self.eoq.Retrieve(clazz,'(EClass:*)$EReference{containment=false}')
#            try:
            ownNonContainingReferences = self.domain.Do(Get(Qry(clazz).Cls('EReference').Sel(Qry().Pth('containment').Equ(False))))
#            except:
#                ownNonContainingReferences = []
            # superTypeNonContainingReferences = self.eoq.Retrieve(clazz,'(EClass:_)/eSuperTypes<-1>$EReference{containment=false}')
#            try:
            superTypeNonContainingReferences = self.domain.Do(Get(Qry(clazz).Pth('eSuperTypes').Cls('EReference').Sel(Qry().Pth('containment').Equ(False))))
#            except:
#                superTypeNonContainingReferences = []
            allNonContainingReferences = ownNonContainingReferences + superTypeNonContainingReferences

            # packageNsUri = self.eoq.Retrieve(package,'(EPackage:1)/nsURI')
            packageNsUri = self.domain.Do(Get(Qry(package).Pth('nsURI')))
            # className = self.eoq.Retrieve(clazz,'(EClass:1)/name')
            className = self.domain.Do(Get(Qry(clazz).Pth('name')))

            headerArray = []
            
            #print(classSectionBegin,end="",file=self.file)
            self._writeLine([classSectionBegin])
            if not ommitClassInfo:
                self._writeLine([packageNsUri,className])
            if not ommitContainer:
                headerArray.append("container")
                #print("container",end="",file=self.file)
            if not ommitContainingPath:
                headerArray.append("containedPath")
            #print("container%ccontainedPath"%(self.dc),end="",file=self.file)
            for attribute in allAttributes:
                # attributeName = self.eoq.Retrieve(attribute,'(EAttribute:1)/name')
                attributeName = self.domain.Do(Get(Qry(attribute).Pth('name')))
                headerArray.append(attributeName)
                #print("%c%s"%(self.dc,self._csvOutputSegment(attributeName)),end="",file=self.file)
            for reference in allNonContainingReferences:
                # referenceName = self.eoq.Retrieve(reference,'(EReference:1)/name')
                referenceName = self.domain.Do(Get(Qry(reference).Pth('name')))
                headerArray.append(referenceName)
                #print("%c%s"%(self.dc,self._csvOutputSegment(referenceName)),end="",file=self.file)
            #replace elements with names from the dictionary
            if attributeNameDictionary:
                headerArray = self._tanslateArray(headerArray,attributeNameDictionary)
            self._writeLine(headerArray)
            for instance in allInstances:
                lineArray = []
                if not ommitContainer:
                    lineArray.append(self.getContainerId(instance))
                if not ommitContainingPath:
#                     featureName = self.eoq.Retrieve(instance,'(EObject:1)@CONTAININGFEATURENAME')
#                     lineArray.append(featureName)
                    lineArray.append(self.getContainingPath(instance,1))
                #print('%s%c%s'%(self._csvOutputSegment(self.getContainerId(eoq,instance)),self.dc,self._csvOutputSegment(self.eoq.EoqPath(instance,1))),end="",file=self.file)
                for attribute in allAttributes:
                    # attributeName = self.eoq.Retrieve(attribute,'(EAttribute:1)/name')
                    attributeName = self.domain.Do(Get(Qry(attribute).Pth('name')))
                    # attributeValue = self.eoq.Retrieve(instance,'(%s:1)/%s'%(className,attributeName))
                    attributeValue = self.domain.Do(Get(Qry(instance).Pth(attributeName)))
                    attributeStr = str(attributeValue) if attributeValue else ''
                    lineArray.append(attributeStr)
                    #print('%c%s'%(self.dc,self._csvOutputSegment(attributeStr)),end="",file=self.file)
                for reference in allNonContainingReferences:
                    referenceName = self.eoq.Retrieve(reference,'(EReference:1)/name')
                    referedElements = self.eoq.Retrieve(instance,'(%s:*)/%s'%(className,referenceName))

                    elementIds = []
                    for element in referedElements:
                        elementIds.append(self.getElementId(element))

                if self.omit_empty_first_column and lineArray[0]: # send only lines that have a non empty first column
                    self._writeLine(lineArray)

            self._writeLine([classSectionEnd])

    def storePackage(self,package,root,ommitRootElement,ommitContainer,ommitContainingPath,attributeNameDictionary,
                     classSectionBegin,classSectionEnd,ommitClassInfo):
        #allClazzes = package.eClassifiers
        # allClazzes = self.eoq.Retrieve(package,'(EPackage:_)/eClassifiers$EClass{abstract=false}')
        allClasses = iter(self.domain.Do(Get(Qry(package).Pth('eClassifiers').Sel(Qry().Pth('abstract').Equ(False)))))
        if ommitRootElement:
            next(allClasses)
        for iClass in allClasses:
            self.storeClass(package,iClass,root,ommitContainer,ommitContainingPath,attributeNameDictionary,
                            classSectionBegin,classSectionEnd,ommitClassInfo)

            
        #look for subpackages
        # allSubpackages = self.eoq.Retrieve(package,'(EPackage:*)/eSubpackages')
        #allSubpackages = package.eSubpackages
        for subpackage in self.domain.Do(Get(Qry(package).Pth('eSubpackages'))):
            self.storePackage(subpackage,root,False,ommitContainer,ommitContainingPath,attributeNameDictionary,classSectionBegin,classSectionEnd,ommitClassInfo)
            
    def SaveAsCsv(self,modelRoot,filename,header='',ommitRootElement=False,ommitContainer=False,ommitContainingPath=False,
                  attributeNameDictionary={},classSectionBegin='',classSectionEnd='',ommitClassInfo=False):
       
        #reset members
        self.elementIdLOT = {}
        self.elementLOT = {}
        self.idAttributeLOT = {}
        
        # mainclass = self.eoq.Retrieve(modelRoot,'(*:1)/eClass')
        mainclass = self.domain.Do(Get(Qry(modelRoot).Pth('eClass')))
        mainclass = mainclass[0] if type(mainclass) == list else mainclass
        # mainpackage = self.eoq.Retrieve(mainclass,'(*:1)/ePackage')
        mainpackage = self.domain.Do(Get(Qry(mainclass).Pth('ePackage')))
        mainpackage = mainpackage[0] if type(mainpackage)==list else mainpackage
        
        self.startCsv(filename)
        for h in header:
            
            self._writeLine([h])
        self.storePackage(mainpackage,modelRoot,ommitRootElement,ommitContainer,ommitContainingPath,
                          attributeNameDictionary,classSectionBegin,classSectionEnd,ommitClassInfo)
        self.finish_csv()

    def startCsv(self, filename):
        import csv
        self.file = open(filename, 'w',newline='')
        # here we can add the correct delimiters
        self.csvWriter = csv.writer(self.file, delimiter=self.dc, lineterminator='\r\n',
                                    quotechar=self.qc, quoting=self.quoting_state)

    def finish_csv(self):
        self.file.close()
