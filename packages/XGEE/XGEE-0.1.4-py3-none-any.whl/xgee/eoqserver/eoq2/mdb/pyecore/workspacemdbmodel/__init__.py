from pyecore.resources import global_registry
from .workspacemdbmodel import getEClassifier, eClassifiers
from .workspacemdbmodel import name, nsURI, nsPrefix, eClass
from .workspacemdbmodel import PathElementA, Workspace, Directory, FileResourceA, FileResourceTypesE, ModelResource, TextResource, RawResource, XmlResource

from pyecore.ecore import EObject

from . import workspacemdbmodel

__all__ = ['PathElementA', 'Workspace', 'Directory', 'FileResourceA',
           'FileResourceTypesE', 'ModelResource', 'TextResource', 'RawResource', 'XmlResource']

eSubpackages = []
eSuperPackage = None
workspacemdbmodel.eSubpackages = eSubpackages
workspacemdbmodel.eSuperPackage = eSuperPackage

Directory.subdirectories.eType = Directory
Directory.resources.eType = FileResourceA
ModelResource.contents.eType = EObject
XmlResource.document.eType = EObject

otherClassifiers = [FileResourceTypesE]

for classif in otherClassifiers:
    eClassifiers[classif.name] = classif
    classif.ePackage = eClass

for classif in eClassifiers.values():
    eClass.eClassifiers.append(classif.eClass)

for subpack in eSubpackages:
    eClass.eSubpackages.append(subpack.eClass)

register_packages = [workspacemdbmodel] + eSubpackages
for pack in register_packages:
    global_registry[pack.nsURI] = pack
