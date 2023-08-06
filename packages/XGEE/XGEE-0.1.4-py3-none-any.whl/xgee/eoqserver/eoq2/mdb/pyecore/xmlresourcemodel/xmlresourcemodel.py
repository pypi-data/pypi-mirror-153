"""Definition of meta model 'xmlresourcemodel'."""
from functools import partial
import pyecore.ecore as Ecore
from pyecore.ecore import *


name = 'xmlresourcemodel'
nsURI = 'http://www.eoq.de/xmlresourcemodel/v1.0'
nsPrefix = 'de.eoq'

eClass = EPackage(name=name, nsURI=nsURI, nsPrefix=nsPrefix)

eClassifiers = {}
getEClassifier = partial(Ecore.getEClassifier, searchspace=eClassifiers)


class Document(EObject, metaclass=MetaEClass):

    name = EAttribute(eType=EString, derived=False, changeable=True)
    version = EAttribute(eType=EString, derived=False, changeable=True)
    standalone = EAttribute(eType=EString, derived=False, changeable=True)
    encoding = EAttribute(eType=EString, derived=False, changeable=True)
    rootelement = EReference(ordered=True, unique=True, containment=True)
    comments = EReference(ordered=True, unique=True, containment=True, upper=-1)

    def __init__(self, *, name=None, version=None, standalone=None, encoding=None, rootelement=None, comments=None, **kwargs):
        if kwargs:
            raise AttributeError('unexpected arguments: {}'.format(kwargs))

        super().__init__()

        if name is not None:
            self.name = name

        if version is not None:
            self.version = version

        if standalone is not None:
            self.standalone = standalone

        if encoding is not None:
            self.encoding = encoding

        if rootelement is not None:
            self.rootelement = rootelement

        if comments:
            self.comments.extend(comments)


class Element(EObject, metaclass=MetaEClass):

    name = EAttribute(eType=EString, derived=False, changeable=True)
    content = EAttribute(eType=EString, derived=False, changeable=True)
    attributes = EReference(ordered=True, unique=True, containment=True, upper=-1)
    subelements = EReference(ordered=True, unique=True, containment=True, upper=-1)

    def __init__(self, *, name=None, content=None, attributes=None, subelements=None, **kwargs):
        if kwargs:
            raise AttributeError('unexpected arguments: {}'.format(kwargs))

        super().__init__()

        if name is not None:
            self.name = name

        if content is not None:
            self.content = content

        if attributes:
            self.attributes.extend(attributes)

        if subelements:
            self.subelements.extend(subelements)


class Attribute(EObject, metaclass=MetaEClass):

    name = EAttribute(eType=EString, derived=False, changeable=True)
    value = EAttribute(eType=EString, derived=False, changeable=True)

    def __init__(self, *, name=None, value=None, **kwargs):
        if kwargs:
            raise AttributeError('unexpected arguments: {}'.format(kwargs))

        super().__init__()

        if name is not None:
            self.name = name

        if value is not None:
            self.value = value


@abstract
class CommentA(EObject, metaclass=MetaEClass):

    content = EAttribute(eType=EString, derived=False, changeable=True)

    def __init__(self, *, content=None, **kwargs):
        if kwargs:
            raise AttributeError('unexpected arguments: {}'.format(kwargs))

        super().__init__()

        if content is not None:
            self.content = content


class Comment(CommentA):

    def __init__(self, **kwargs):

        super().__init__(**kwargs)


class CData(CommentA):

    def __init__(self, **kwargs):

        super().__init__(**kwargs)
