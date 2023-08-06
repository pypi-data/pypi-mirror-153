"""Definition of meta model 'workspacemdbmodel'."""
from functools import partial
import pyecore.ecore as Ecore
from pyecore.ecore import *


name = 'workspacemdbmodel'
nsURI = 'http://www.eoq.de/workspacemdbmodel/v1.0'
nsPrefix = 'de.eoq'

eClass = EPackage(name=name, nsURI=nsURI, nsPrefix=nsPrefix)

eClassifiers = {}
getEClassifier = partial(Ecore.getEClassifier, searchspace=eClassifiers)
FileResourceTypesE = EEnum('FileResourceTypesE', literals=['MODEL', 'TEXT', 'RAW', 'XML'])


@abstract
class PathElementA(EObject, metaclass=MetaEClass):

    def __init__(self, **kwargs):
        if kwargs:
            raise AttributeError('unexpected arguments: {}'.format(kwargs))

        super().__init__()

    def actualPathAbs(self):

        raise NotImplementedError('operation actualPathAbs(...) not yet implemented')

    def actualPath(self):

        raise NotImplementedError('operation actualPath(...) not yet implemented')

    def actualPathCwd(self):

        raise NotImplementedError('operation actualPathCwd(...) not yet implemented')


class Directory(PathElementA):

    name = EAttribute(eType=EString, derived=False, changeable=True, default_value='.')
    subdirectories = EReference(ordered=True, unique=True, containment=True, upper=-1)
    resources = EReference(ordered=True, unique=True, containment=True, upper=-1)

    def __init__(self, *, subdirectories=None, resources=None, name=None, **kwargs):

        super().__init__(**kwargs)

        if name is not None:
            self.name = name

        if subdirectories:
            self.subdirectories.extend(subdirectories)

        if resources:
            self.resources.extend(resources)


@abstract
class FileResourceA(PathElementA):

    name = EAttribute(eType=EString, derived=False, changeable=True, default_value='newResource')
    isDirty = EAttribute(eType=EBoolean, derived=False, changeable=True)
    isLoaded = EAttribute(eType=EBoolean, derived=False, changeable=True, default_value=False)
    lastPersistentPath = EAttribute(eType=EString, derived=False, changeable=True)

    def __init__(self, *, name=None, isDirty=None, isLoaded=None, lastPersistentPath=None, **kwargs):

        super().__init__(**kwargs)

        if name is not None:
            self.name = name

        if isDirty is not None:
            self.isDirty = isDirty

        if isLoaded is not None:
            self.isLoaded = isLoaded

        if lastPersistentPath is not None:
            self.lastPersistentPath = lastPersistentPath


class Workspace(Directory):

    def __init__(self, **kwargs):

        super().__init__(**kwargs)


class ModelResource(FileResourceA):

    type = EAttribute(eType=FileResourceTypesE, derived=False,
                      changeable=True, default_value=FileResourceTypesE.MODEL)
    isMetaModel = EAttribute(eType=EBoolean, derived=False,
                             changeable=True, upper=-1, default_value=False)
    isWritable = EAttribute(eType=EBoolean, derived=False,
                            changeable=True, upper=-1, default_value=True)
    contents = EReference(ordered=True, unique=True, containment=True, upper=-1)

    def __init__(self, *, type=None, isMetaModel=None, isWritable=None, contents=None, **kwargs):

        super().__init__(**kwargs)

        if type is not None:
            self.type = type

        if isMetaModel:
            self.isMetaModel.extend(isMetaModel)

        if isWritable:
            self.isWritable.extend(isWritable)

        if contents:
            self.contents.extend(contents)


class TextResource(FileResourceA):

    type = EAttribute(eType=FileResourceTypesE, derived=False,
                      changeable=True, default_value=FileResourceTypesE.TEXT)
    lines = EAttribute(eType=EString, derived=False, changeable=True, upper=-1)

    def __init__(self, *, type=None, lines=None, **kwargs):

        super().__init__(**kwargs)

        if type is not None:
            self.type = type

        if lines:
            self.lines.extend(lines)


class RawResource(FileResourceA):

    type = EAttribute(eType=FileResourceTypesE, derived=False,
                      changeable=True, default_value=FileResourceTypesE.RAW)
    data = EAttribute(eType=EByte, derived=False, changeable=True, upper=-1)

    def __init__(self, *, type=None, data=None, **kwargs):

        super().__init__(**kwargs)

        if type is not None:
            self.type = type

        if data:
            self.data.extend(data)


class XmlResource(FileResourceA):

    type = EAttribute(eType=FileResourceTypesE, derived=False,
                      changeable=True, default_value=FileResourceTypesE.XML)
    lines = EAttribute(eType=EString, derived=False, changeable=True, upper=-1)
    document = EReference(ordered=True, unique=True, containment=True)

    def __init__(self, *, type=None, lines=None, document=None, **kwargs):

        super().__init__(**kwargs)

        if type is not None:
            self.type = type

        if lines:
            self.lines.extend(lines)

        if document is not None:
            self.document = document
