from pyecore.resources import global_registry
from .constraintmodel import getEClassifier, eClassifiers
from .constraintmodel import name, nsURI, nsPrefix, eClass
from .constraintmodel import Constraint, ConstraintTypeEnum


from . import constraintmodel

__all__ = ['Constraint', 'ConstraintTypeEnum']

eSubpackages = []
eSuperPackage = None
constraintmodel.eSubpackages = eSubpackages
constraintmodel.eSuperPackage = eSuperPackage


otherClassifiers = [ConstraintTypeEnum]

for classif in otherClassifiers:
    eClassifiers[classif.name] = classif
    classif.ePackage = eClass

for classif in eClassifiers.values():
    eClass.eClassifiers.append(classif.eClass)

for subpack in eSubpackages:
    eClass.eSubpackages.append(subpack.eClass)

register_packages = [constraintmodel] + eSubpackages
for pack in register_packages:
    global_registry[pack.nsURI] = pack
