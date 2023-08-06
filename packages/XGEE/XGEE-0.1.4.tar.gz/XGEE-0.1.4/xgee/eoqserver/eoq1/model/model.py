"""Definition of meta model 'model'."""
from functools import partial
import pyecore.ecore as Ecore
from pyecore.ecore import *


name = 'model'
nsURI = 'http://www.eoq.de/model/v1.0'
nsPrefix = 'de.eoq'

eClass = EPackage(name=name, nsURI=nsURI, nsPrefix=nsPrefix)

eClassifiers = {}
getEClassifier = partial(Ecore.getEClassifier, searchspace=eClassifiers)
MetaModelSourcesE = EEnum('MetaModelSourcesE', literals=['BUILDIN', 'DYNAMIC'])

FileResourceTypesE = EEnum('FileResourceTypesE', literals=['MODEL', 'TEXT', 'RAW'])

SegmentTypesE = EEnum('SegmentTypesE', literals=[
                      'RESOURCE', 'PATH', 'ID', 'CLAZZ', 'INSTANCE', 'META', 'HISTORY', 'LISTOP', 'SELECTOR', 'INDEX'])

MetaSegmentIdentifiersE = EEnum('MetaSegmentIdentifiersE', literals=['CONTAINER', 'INDEX', 'TYPE', 'CLASS', 'CONTENTS', 'CLASSNAME', 'PACKAGE', 'PACKAGENAME', 'RESOURCE', 'RESOURCENAME', 'CONTAININGFEATURE', 'CONTAININGFEATURENAME',
                                                                     'FEATURES', 'FEATURENAMES', 'ATTRIBUTES', 'ATTRIBUTENAMES', 'REFERENCES', 'REFERENCENAMES', 'CONTAINMENTS', 'CONTAINMENTNAMES', 'ATTRIBUTEVALUES', 'FEATUREVALUES', 'REFERENCEVALUES', 'CONTAINMENTVALUES'])

IndexTypesE = EEnum('IndexTypesE', literals=['NUMBER', 'RANGE', 'ADD', 'REMOVE', 'FLATTEN'])

OperatorTypesE = EEnum('OperatorTypesE', literals=['EQUAL', 'NOTEQUAL', 'GREATER', 'LESS'])

ValueTypesE = EEnum('ValueTypesE', literals=[
                    'INT', 'FLOAT', 'BOOL', 'STRING', 'OBJECTREF', 'EMPTY', 'LIST', 'HISTORYREF', 'OPERATION', 'OBJECT', 'QUERY'])

ReturnMultiplicityTypeE = EEnum('ReturnMultiplicityTypeE', literals=[
                                'UNCHANGED', 'FLATTENED', 'FORCESINGLE'])

CommandTypesE = EEnum('CommandTypesE', literals=['HELLO', 'GOODBYE', 'SESSION', 'STATUS', 'CHANGES', 'RETRIEVE',
                                                 'CREATE', 'UPDATE', 'CLONE', 'UNDO', 'CALL', 'ASYNCCALL', 'CALLSTATUS', 'ABORTCALL', 'COMPOUND'])

CloneModesE = EEnum('CloneModesE', literals=['CLASS', 'ATTRIBUTES', 'FULL', 'DEEP'])

ResultTypesE = EEnum('ResultTypesE', literals=['OK', 'ERROR', 'COMPOUND_OK', 'COMPOUND_ERROR'])

CallStatusE = EEnum('CallStatusE', literals=[
                    'INITIALIZING', 'RUNNING', 'WAITING', 'FINISHED', 'ABORTED', 'ERROR'])

CallChannelTypesE = EEnum('CallChannelTypesE', literals=['OUT', 'IN', 'INTERACTIVE'])

ListOpSegmentTypesE = EEnum('ListOpSegmentTypesE', literals=['SIZE', 'FLATTEN'])

SegmentProcessingTypesE = EEnum('SegmentProcessingTypesE', literals=['RECURSIVE', 'LINEAR'])


Object = EDataType('Object', instanceClassName='None')


@abstract
class NamedElementA(EObject, metaclass=MetaEClass):

    name = EAttribute(eType=EString, derived=False, changeable=True, default_value='UNNAMED')

    def __init__(self, *, name=None, **kwargs):
        if kwargs:
            raise AttributeError('unexpected arguments: {}'.format(kwargs))

        super().__init__()

        if name is not None:
            self.name = name


class Metamodel(EObject, metaclass=MetaEClass):

    source = EAttribute(eType=MetaModelSourcesE, derived=False, changeable=True)
    name = EAttribute(eType=EString, derived=False, changeable=True)
    package = EReference(ordered=True, unique=True, containment=False)

    def __init__(self, *, source=None, package=None, name=None, **kwargs):
        if kwargs:
            raise AttributeError('unexpected arguments: {}'.format(kwargs))

        super().__init__()

        if source is not None:
            self.source = source

        if name is not None:
            self.name = name

        if package is not None:
            self.package = package


class CommandInfo(EObject, metaclass=MetaEClass):

    name = EAttribute(eType=EString, derived=False, changeable=True, iD=True)
    description = EAttribute(eType=EString, derived=False, changeable=True)
    parameters = EReference(ordered=True, unique=True, containment=True, upper=-1)
    results = EReference(ordered=True, unique=True, containment=True, upper=-1)

    def __init__(self, *, name=None, parameters=None, description=None, results=None, **kwargs):
        if kwargs:
            raise AttributeError('unexpected arguments: {}'.format(kwargs))

        super().__init__()

        if name is not None:
            self.name = name

        if description is not None:
            self.description = description

        if parameters:
            self.parameters.extend(parameters)

        if results:
            self.results.extend(results)


class Transaction(EObject, metaclass=MetaEClass):

    id = EAttribute(eType=EInt, derived=False, changeable=True, default_value=0)
    starttime = EAttribute(eType=EFloat, derived=False, changeable=True, default_value=0.0)
    endtime = EAttribute(eType=EFloat, derived=False, changeable=True, default_value=0.0)
    deadline = EAttribute(eType=EFloat, derived=False, changeable=True, default_value=0.0)
    maxDuration = EAttribute(eType=EFloat, derived=False, changeable=True, default_value=0.0)
    wasTimedOut = EAttribute(eType=EBoolean, derived=False, changeable=True, default_value=False)
    wasEnded = EAttribute(eType=EBoolean, derived=False, changeable=True)
    history = EReference(ordered=True, unique=True, containment=False, upper=-1)
    changes = EReference(ordered=True, unique=True, containment=False, upper=-1)

    def __init__(self, *, id=None, starttime=None, endtime=None, deadline=None, maxDuration=None, wasTimedOut=None, wasEnded=None, history=None, changes=None, **kwargs):
        if kwargs:
            raise AttributeError('unexpected arguments: {}'.format(kwargs))

        super().__init__()

        if id is not None:
            self.id = id

        if starttime is not None:
            self.starttime = starttime

        if endtime is not None:
            self.endtime = endtime

        if deadline is not None:
            self.deadline = deadline

        if maxDuration is not None:
            self.maxDuration = maxDuration

        if wasTimedOut is not None:
            self.wasTimedOut = wasTimedOut

        if wasEnded is not None:
            self.wasEnded = wasEnded

        if history:
            self.history.extend(history)

        if changes:
            self.changes.extend(changes)


class Change(EObject, metaclass=MetaEClass):

    changeId = EAttribute(eType=EInt, derived=False, changeable=True, default_value=0)
    sourceTranscallId = EAttribute(eType=EInt, derived=False, changeable=True, default_value=0)
    target = EReference(ordered=True, unique=True, containment=True)
    query = EReference(ordered=True, unique=True, containment=True)
    newValue = EReference(ordered=True, unique=True, containment=True)
    oldValue = EReference(ordered=True, unique=True, containment=True)

    def __init__(self, *, target=None, query=None, newValue=None, changeId=None, sourceTranscallId=None, oldValue=None, **kwargs):
        if kwargs:
            raise AttributeError('unexpected arguments: {}'.format(kwargs))

        super().__init__()

        if changeId is not None:
            self.changeId = changeId

        if sourceTranscallId is not None:
            self.sourceTranscallId = sourceTranscallId

        if target is not None:
            self.target = target

        if query is not None:
            self.query = query

        if newValue is not None:
            self.newValue = newValue

        if oldValue is not None:
            self.oldValue = oldValue


class ActionInfo(EObject, metaclass=MetaEClass):

    name = EAttribute(eType=EString, derived=False, changeable=True, iD=True)
    description = EAttribute(eType=EString, derived=False, changeable=True)
    details = EAttribute(eType=EString, derived=False, changeable=True)
    parameters = EReference(ordered=True, unique=True, containment=True, upper=-1)
    results = EReference(ordered=True, unique=True, containment=True, upper=-1)
    handler = EReference(ordered=True, unique=True, containment=False)

    def __init__(self, *, name=None, description=None, parameters=None, results=None, handler=None, details=None, **kwargs):
        if kwargs:
            raise AttributeError('unexpected arguments: {}'.format(kwargs))

        super().__init__()

        if name is not None:
            self.name = name

        if description is not None:
            self.description = description

        if details is not None:
            self.details = details

        if parameters:
            self.parameters.extend(parameters)

        if results:
            self.results.extend(results)

        if handler is not None:
            self.handler = handler


class ActionParameter(EObject, metaclass=MetaEClass):

    name = EAttribute(eType=EString, derived=False, changeable=True, iD=True)
    type = EAttribute(eType=EString, derived=False, changeable=True, default_value='String')
    lowerBound = EAttribute(eType=EInt, derived=False, changeable=True, default_value=1)
    upperBound = EAttribute(eType=EInt, derived=False, changeable=True, default_value=1)
    description = EAttribute(eType=EString, derived=False, changeable=True)
    default = EAttribute(eType=EString, derived=False, changeable=True)
    choices = EReference(ordered=True, unique=True, containment=True, upper=-1)

    def __init__(self, *, name=None, type=None, lowerBound=None, upperBound=None, description=None, default=None, choices=None, **kwargs):
        if kwargs:
            raise AttributeError('unexpected arguments: {}'.format(kwargs))

        super().__init__()

        if name is not None:
            self.name = name

        if type is not None:
            self.type = type

        if lowerBound is not None:
            self.lowerBound = lowerBound

        if upperBound is not None:
            self.upperBound = upperBound

        if description is not None:
            self.description = description

        if default is not None:
            self.default = default

        if choices:
            self.choices.extend(choices)


class Choice(EObject, metaclass=MetaEClass):

    value = EAttribute(eType=EString, derived=False, changeable=True, iD=True)

    def __init__(self, *, value=None, **kwargs):
        if kwargs:
            raise AttributeError('unexpected arguments: {}'.format(kwargs))

        super().__init__()

        if value is not None:
            self.value = value


@abstract
class ActionHandlerA(EObject, metaclass=MetaEClass):

    def __init__(self, **kwargs):
        if kwargs:
            raise AttributeError('unexpected arguments: {}'.format(kwargs))

        super().__init__()

    def Call(self, actionCall=None, transaction=None):

        raise NotImplementedError('operation Call(...) not yet implemented')

    def AsyncCall(self, actionCall=None, transaction=None):

        raise NotImplementedError('operation AsyncCall(...) not yet implemented')

    def CallStatus(self, actionCall=None, transaction=None):

        raise NotImplementedError('operation CallStatus(...) not yet implemented')

    def AbortCall(self, actionCall=None, transaction=None):

        raise NotImplementedError('operation AbortCall(...) not yet implemented')


class CommandParameter(EObject, metaclass=MetaEClass):

    name = EAttribute(eType=EString, derived=False, changeable=True, iD=True)
    type = EAttribute(eType=EString, derived=False, changeable=True, default_value='String')
    description = EAttribute(eType=EString, derived=False, changeable=True)
    example = EAttribute(eType=EString, derived=False, changeable=True)

    def __init__(self, *, name=None, type=None, description=None, example=None, **kwargs):
        if kwargs:
            raise AttributeError('unexpected arguments: {}'.format(kwargs))

        super().__init__()

        if name is not None:
            self.name = name

        if type is not None:
            self.type = type

        if description is not None:
            self.description = description

        if example is not None:
            self.example = example


class Query(EObject, metaclass=MetaEClass):

    segments = EReference(ordered=True, unique=True, containment=True, upper=-1)
    sourceClass = EReference(ordered=True, unique=True, containment=True)
    returnMultiplicity = EReference(ordered=True, unique=True, containment=True)

    def __init__(self, *, segments=None, sourceClass=None, returnMultiplicity=None, **kwargs):
        if kwargs:
            raise AttributeError('unexpected arguments: {}'.format(kwargs))

        super().__init__()

        if segments:
            self.segments.extend(segments)

        if sourceClass is not None:
            self.sourceClass = sourceClass

        if returnMultiplicity is not None:
            self.returnMultiplicity = returnMultiplicity


@abstract
class Segment(EObject, metaclass=MetaEClass):

    identifier = EAttribute(eType=EString, derived=False, changeable=True)
    selector = EReference(ordered=True, unique=True, containment=True)
    index = EReference(ordered=True, unique=True, containment=True)
    depth = EReference(ordered=True, unique=True, containment=True)

    def __init__(self, *, identifier=None, selector=None, index=None, depth=None, **kwargs):
        if kwargs:
            raise AttributeError('unexpected arguments: {}'.format(kwargs))

        super().__init__()

        if identifier is not None:
            self.identifier = identifier

        if selector is not None:
            self.selector = selector

        if index is not None:
            self.index = index

        if depth is not None:
            self.depth = depth


class Depth(EObject, metaclass=MetaEClass):

    value = EAttribute(eType=EInt, derived=False, changeable=True, default_value=1)

    def __init__(self, *, value=None, **kwargs):
        if kwargs:
            raise AttributeError('unexpected arguments: {}'.format(kwargs))

        super().__init__()

        if value is not None:
            self.value = value


@abstract
class Index(EObject, metaclass=MetaEClass):

    def __init__(self, **kwargs):
        if kwargs:
            raise AttributeError('unexpected arguments: {}'.format(kwargs))

        super().__init__()


class Selector(EObject, metaclass=MetaEClass):

    name = EAttribute(eType=EString, derived=False, changeable=True)
    value = EReference(ordered=True, unique=True, containment=False)
    operator = EReference(ordered=True, unique=True, containment=True)

    def __init__(self, *, name=None, value=None, operator=None, **kwargs):
        if kwargs:
            raise AttributeError('unexpected arguments: {}'.format(kwargs))

        super().__init__()

        if name is not None:
            self.name = name

        if value is not None:
            self.value = value

        if operator is not None:
            self.operator = operator


@abstract
class Operator(EObject, metaclass=MetaEClass):

    def __init__(self, **kwargs):
        if kwargs:
            raise AttributeError('unexpected arguments: {}'.format(kwargs))

        super().__init__()


@abstract
class Value(EObject, metaclass=MetaEClass):

    def __init__(self, **kwargs):
        if kwargs:
            raise AttributeError('unexpected arguments: {}'.format(kwargs))

        super().__init__()


class SourceClass(EObject, metaclass=MetaEClass):

    dontCare = EAttribute(eType=EBoolean, derived=False, changeable=True, default_value=True)
    name = EAttribute(eType=EString, derived=False, changeable=True, default_value='*')
    type = EReference(ordered=True, unique=True, containment=False)

    def __init__(self, *, dontCare=None, name=None, type=None, **kwargs):
        if kwargs:
            raise AttributeError('unexpected arguments: {}'.format(kwargs))

        super().__init__()

        if dontCare is not None:
            self.dontCare = dontCare

        if name is not None:
            self.name = name

        if type is not None:
            self.type = type


@abstract
class ReturnMultiplicity(EObject, metaclass=MetaEClass):

    def __init__(self, **kwargs):
        if kwargs:
            raise AttributeError('unexpected arguments: {}'.format(kwargs))

        super().__init__()


@abstract
class CommandA(EObject, metaclass=MetaEClass):

    def __init__(self, **kwargs):
        if kwargs:
            raise AttributeError('unexpected arguments: {}'.format(kwargs))

        super().__init__()


@abstract
class ResultA(EObject, metaclass=MetaEClass):

    transactionId = EAttribute(eType=EInt, derived=False, changeable=True, default_value=0)

    def __init__(self, *, transactionId=None, **kwargs):
        if kwargs:
            raise AttributeError('unexpected arguments: {}'.format(kwargs))

        super().__init__()

        if transactionId is not None:
            self.transactionId = transactionId


class ActionCall(EObject, metaclass=MetaEClass):

    callId = EAttribute(eType=EInt, derived=False, changeable=True, default_value=0)
    callStatus = EAttribute(eType=CallStatusE, derived=False, changeable=True,
                            default_value=CallStatusE.INITIALIZING)
    action = EAttribute(eType=EString, derived=False, changeable=True, iD=True)
    channels = EReference(ordered=True, unique=True, containment=True, upper=-1)
    args = EReference(ordered=True, unique=True, containment=True)
    handler = EReference(ordered=True, unique=True, containment=False)
    returnValues = EReference(ordered=True, unique=True, containment=True)

    def __init__(self, *, callId=None, callStatus=None, action=None, channels=None, args=None, handler=None, returnValues=None, **kwargs):
        if kwargs:
            raise AttributeError('unexpected arguments: {}'.format(kwargs))

        super().__init__()

        if callId is not None:
            self.callId = callId

        if callStatus is not None:
            self.callStatus = callStatus

        if action is not None:
            self.action = action

        if channels:
            self.channels.extend(channels)

        if args is not None:
            self.args = args

        if handler is not None:
            self.handler = handler

        if returnValues is not None:
            self.returnValues = returnValues


class CallChannel(EObject, metaclass=MetaEClass):

    type = EAttribute(eType=CallChannelTypesE, derived=False,
                      changeable=True, default_value=CallChannelTypesE.OUT)
    name = EAttribute(eType=EString, derived=False, changeable=True, iD=True)
    data = EReference(ordered=True, unique=True, containment=True, upper=-1)

    def __init__(self, *, type=None, name=None, data=None, **kwargs):
        if kwargs:
            raise AttributeError('unexpected arguments: {}'.format(kwargs))

        super().__init__()

        if type is not None:
            self.type = type

        if name is not None:
            self.name = name

        if data:
            self.data.extend(data)


class CallChannelData(EObject, metaclass=MetaEClass):

    date = EAttribute(eType=EString, derived=False, changeable=True)
    data = EAttribute(eType=EString, derived=False, changeable=True)

    def __init__(self, *, date=None, data=None, **kwargs):
        if kwargs:
            raise AttributeError('unexpected arguments: {}'.format(kwargs))

        super().__init__()

        if date is not None:
            self.date = date

        if data is not None:
            self.data = data


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


@abstract
class DomainA(NamedElementA):

    version = EAttribute(eType=EString, derived=False, changeable=True, default_value='UNKNOWN')
    transactionCount = EAttribute(eType=EInt, derived=False, changeable=True, default_value=0)
    changeCount = EAttribute(eType=EInt, derived=False, changeable=True, default_value=0)
    callCount = EAttribute(eType=EInt, derived=False, changeable=True, default_value=0)
    metamodels = EReference(ordered=True, unique=True, containment=True, upper=-1)
    transactions = EReference(ordered=True, unique=True, containment=True, upper=-1)
    commands = EReference(ordered=True, unique=True, containment=True, upper=-1)
    models = EReference(ordered=True, unique=True, containment=True, upper=-1)
    actions = EReference(ordered=True, unique=True, containment=False, upper=-1)
    currentTransaction = EReference(ordered=True, unique=True, containment=False)
    changes = EReference(ordered=True, unique=True, containment=True, upper=-1)
    actionCalls = EReference(ordered=True, unique=True, containment=True, upper=-1)

    def __init__(self, *, version=None, metamodels=None, transactions=None, commands=None, models=None, actions=None, currentTransaction=None, transactionCount=None, changeCount=None, changes=None, actionCalls=None, callCount=None, **kwargs):

        super().__init__(**kwargs)

        if version is not None:
            self.version = version

        if transactionCount is not None:
            self.transactionCount = transactionCount

        if changeCount is not None:
            self.changeCount = changeCount

        if callCount is not None:
            self.callCount = callCount

        if metamodels:
            self.metamodels.extend(metamodels)

        if transactions:
            self.transactions.extend(transactions)

        if commands:
            self.commands.extend(commands)

        if models:
            self.models.extend(models)

        if actions:
            self.actions.extend(actions)

        if currentTransaction is not None:
            self.currentTransaction = currentTransaction

        if changes:
            self.changes.extend(changes)

        if actionCalls:
            self.actionCalls.extend(actionCalls)

    def Do(self, command=None):

        raise NotImplementedError('operation Do(...) not yet implemented')


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


class NumberIndex(Index):

    type = EAttribute(eType=IndexTypesE, derived=False,
                      changeable=True, default_value=IndexTypesE.NUMBER)
    value = EAttribute(eType=EInt, derived=False, changeable=True, default_value=0)

    def __init__(self, *, type=None, value=None, **kwargs):

        super().__init__(**kwargs)

        if type is not None:
            self.type = type

        if value is not None:
            self.value = value


class RangeIndex(Index):

    type = EAttribute(eType=IndexTypesE, derived=False,
                      changeable=True, default_value=IndexTypesE.RANGE)
    lower = EAttribute(eType=EInt, derived=False, changeable=True, default_value=1)
    upper = EAttribute(eType=EInt, derived=False, changeable=True, default_value=0)

    def __init__(self, *, type=None, lower=None, upper=None, **kwargs):

        super().__init__(**kwargs)

        if type is not None:
            self.type = type

        if lower is not None:
            self.lower = lower

        if upper is not None:
            self.upper = upper


class AddIndex(Index):

    type = EAttribute(eType=IndexTypesE, derived=False,
                      changeable=True, default_value=IndexTypesE.ADD)

    def __init__(self, *, type=None, **kwargs):

        super().__init__(**kwargs)

        if type is not None:
            self.type = type


class RemoveIndex(Index):

    type = EAttribute(eType=IndexTypesE, derived=False,
                      changeable=True, default_value=IndexTypesE.REMOVE)

    def __init__(self, *, type=None, **kwargs):

        super().__init__(**kwargs)

        if type is not None:
            self.type = type


class FlattenIndex(Index):

    type = EAttribute(eType=IndexTypesE, derived=False, changeable=True,
                      default_value=IndexTypesE.FLATTEN)

    def __init__(self, *, type=None, **kwargs):

        super().__init__(**kwargs)

        if type is not None:
            self.type = type


class EqualOperator(Operator):

    type = EAttribute(eType=OperatorTypesE, derived=False,
                      changeable=True, default_value=OperatorTypesE.EQUAL)
    symbol = EAttribute(eType=EChar, derived=False, changeable=True, default_value='=')

    def __init__(self, *, type=None, symbol=None, **kwargs):

        super().__init__(**kwargs)

        if type is not None:
            self.type = type

        if symbol is not None:
            self.symbol = symbol


class NotEqualOperator(Operator):

    type = EAttribute(eType=OperatorTypesE, derived=False, changeable=True,
                      default_value=OperatorTypesE.NOTEQUAL)
    symbol = EAttribute(eType=EChar, derived=False, changeable=True, default_value='~')

    def __init__(self, *, type=None, symbol=None, **kwargs):

        super().__init__(**kwargs)

        if type is not None:
            self.type = type

        if symbol is not None:
            self.symbol = symbol


class GreaterOperator(Operator):

    type = EAttribute(eType=OperatorTypesE, derived=False, changeable=True,
                      default_value=OperatorTypesE.GREATER)
    symbol = EAttribute(eType=EChar, derived=False, changeable=True, default_value='>')

    def __init__(self, *, type=None, symbol=None, **kwargs):

        super().__init__(**kwargs)

        if type is not None:
            self.type = type

        if symbol is not None:
            self.symbol = symbol


class LessOperator(Operator):

    type = EAttribute(eType=OperatorTypesE, derived=False,
                      changeable=True, default_value=OperatorTypesE.LESS)
    symbol = EAttribute(eType=EChar, derived=False, changeable=True, default_value='<')

    def __init__(self, *, type=None, symbol=None, **kwargs):

        super().__init__(**kwargs)

        if type is not None:
            self.type = type

        if symbol is not None:
            self.symbol = symbol


class IntValue(Value):

    type = EAttribute(eType=ValueTypesE, derived=False,
                      changeable=True, default_value=ValueTypesE.INT)
    v = EAttribute(eType=EInt, derived=False, changeable=True)

    def __init__(self, *, type=None, v=None, **kwargs):

        super().__init__(**kwargs)

        if type is not None:
            self.type = type

        if v is not None:
            self.v = v


class FloatValue(Value):

    type = EAttribute(eType=ValueTypesE, derived=False,
                      changeable=True, default_value=ValueTypesE.FLOAT)
    v = EAttribute(eType=EFloat, derived=False, changeable=True)

    def __init__(self, *, type=None, v=None, **kwargs):

        super().__init__(**kwargs)

        if type is not None:
            self.type = type

        if v is not None:
            self.v = v


class BoolValue(Value):

    type = EAttribute(eType=ValueTypesE, derived=False,
                      changeable=True, default_value=ValueTypesE.BOOL)
    v = EAttribute(eType=EBoolean, derived=False, changeable=True)

    def __init__(self, *, type=None, v=None, **kwargs):

        super().__init__(**kwargs)

        if type is not None:
            self.type = type

        if v is not None:
            self.v = v


class StringValue(Value):

    type = EAttribute(eType=ValueTypesE, derived=False,
                      changeable=True, default_value=ValueTypesE.STRING)
    v = EAttribute(eType=EString, derived=False, changeable=True)

    def __init__(self, *, type=None, v=None, **kwargs):

        super().__init__(**kwargs)

        if type is not None:
            self.type = type

        if v is not None:
            self.v = v


class ObjectRefValue(Value):

    type = EAttribute(eType=ValueTypesE, derived=False, changeable=True,
                      default_value=ValueTypesE.OBJECTREF)
    v = EAttribute(eType=EInt, derived=False, changeable=True)

    def __init__(self, *, type=None, v=None, **kwargs):

        super().__init__(**kwargs)

        if type is not None:
            self.type = type

        if v is not None:
            self.v = v


class EmptyValue(Value):

    type = EAttribute(eType=ValueTypesE, derived=False,
                      changeable=True, default_value=ValueTypesE.EMPTY)
    v = EAttribute(eType=Object, derived=False, changeable=True)

    def __init__(self, *, type=None, v=None, **kwargs):

        super().__init__(**kwargs)

        if type is not None:
            self.type = type

        if v is not None:
            self.v = v


class ListValue(Value):

    type = EAttribute(eType=ValueTypesE, derived=False,
                      changeable=True, default_value=ValueTypesE.LIST)
    v = EReference(ordered=True, unique=True, containment=True, upper=-1)

    def __init__(self, *, v=None, type=None, **kwargs):

        super().__init__(**kwargs)

        if type is not None:
            self.type = type

        if v:
            self.v.extend(v)


class HistoryRefValue(Value):

    type = EAttribute(eType=ValueTypesE, derived=False, changeable=True,
                      default_value=ValueTypesE.HISTORYREF)
    v = EAttribute(eType=EInt, derived=False, changeable=True)

    def __init__(self, *, type=None, v=None, **kwargs):

        super().__init__(**kwargs)

        if type is not None:
            self.type = type

        if v is not None:
            self.v = v


class OperationValue(Value):

    type = EAttribute(eType=ValueTypesE, derived=False, changeable=True,
                      default_value=ValueTypesE.OPERATION)

    def __init__(self, *, type=None, **kwargs):

        super().__init__(**kwargs)

        if type is not None:
            self.type = type

    def v(self):

        raise NotImplementedError('operation v(...) not yet implemented')


class ObjectValue(Value):

    type = EAttribute(eType=ValueTypesE, derived=False,
                      changeable=True, default_value=ValueTypesE.OBJECT)
    v = EReference(ordered=True, unique=True, containment=False)

    def __init__(self, *, type=None, v=None, **kwargs):

        super().__init__(**kwargs)

        if type is not None:
            self.type = type

        if v is not None:
            self.v = v


class UnchangedReturnMuliplicity(ReturnMultiplicity):

    type = EAttribute(eType=ReturnMultiplicityTypeE, derived=False,
                      changeable=True, default_value=ReturnMultiplicityTypeE.UNCHANGED)
    symbol = EAttribute(eType=EChar, derived=False, changeable=True, default_value='*')

    def __init__(self, *, type=None, symbol=None, **kwargs):

        super().__init__(**kwargs)

        if type is not None:
            self.type = type

        if symbol is not None:
            self.symbol = symbol


class FlattenedReturnMultiplicity(ReturnMultiplicity):

    type = EAttribute(eType=ReturnMultiplicityTypeE, derived=False,
                      changeable=True, default_value=ReturnMultiplicityTypeE.FLATTENED)
    symbol = EAttribute(eType=EChar, derived=False, changeable=True, default_value='_')

    def __init__(self, *, type=None, symbol=None, **kwargs):

        super().__init__(**kwargs)

        if type is not None:
            self.type = type

        if symbol is not None:
            self.symbol = symbol


class ForceSingleReturnMultiplicity(ReturnMultiplicity):

    type = EAttribute(eType=ReturnMultiplicityTypeE, derived=False, changeable=True,
                      default_value=ReturnMultiplicityTypeE.FORCESINGLE)
    symbol = EAttribute(eType=EChar, derived=False, changeable=True, default_value='1')

    def __init__(self, *, type=None, symbol=None, **kwargs):

        super().__init__(**kwargs)

        if type is not None:
            self.type = type

        if symbol is not None:
            self.symbol = symbol


class HelloCommand(CommandA):
    """Grants access as a certain user to the domain. Returned is a session id."""
    type = EAttribute(eType=CommandTypesE, derived=False,
                      changeable=True, default_value=CommandTypesE.HELLO)
    identification = EReference(ordered=True, unique=True, containment=True)
    sessionId = EReference(ordered=True, unique=True, containment=True)

    def __init__(self, *, type=None, identification=None, sessionId=None, **kwargs):

        super().__init__(**kwargs)

        if type is not None:
            self.type = type

        if identification is not None:
            self.identification = identification

        if sessionId is not None:
            self.sessionId = sessionId


class GoodbyeCommand(CommandA):

    type = EAttribute(eType=CommandTypesE, derived=False, changeable=True,
                      default_value=CommandTypesE.GOODBYE)
    sessionId = EReference(ordered=True, unique=True, containment=True)

    def __init__(self, *, type=None, sessionId=None, **kwargs):

        super().__init__(**kwargs)

        if type is not None:
            self.type = type

        if sessionId is not None:
            self.sessionId = sessionId


class SessionCommand(CommandA):
    """When working as a user this should be the first command in a compound command to notify the domain about the session to be used. """
    type = EAttribute(eType=CommandTypesE, derived=False, changeable=True,
                      default_value=CommandTypesE.SESSION)
    sessionId = EReference(ordered=True, unique=True, containment=True)

    def __init__(self, *, type=None, sessionId=None, **kwargs):

        super().__init__(**kwargs)

        if type is not None:
            self.type = type

        if sessionId is not None:
            self.sessionId = sessionId


class StatusCommand(CommandA):

    type = EAttribute(eType=CommandTypesE, derived=False,
                      changeable=True, default_value=CommandTypesE.STATUS)

    def __init__(self, *, type=None, **kwargs):

        super().__init__(**kwargs)

        if type is not None:
            self.type = type


class ChangesCommand(CommandA):

    type = EAttribute(eType=CommandTypesE, derived=False, changeable=True,
                      default_value=CommandTypesE.CHANGES)
    earliestChangeId = EReference(ordered=True, unique=True, containment=True)

    def __init__(self, *, type=None, earliestChangeId=None, **kwargs):

        super().__init__(**kwargs)

        if type is not None:
            self.type = type

        if earliestChangeId is not None:
            self.earliestChangeId = earliestChangeId


class RetrieveCommand(CommandA):

    type = EAttribute(eType=CommandTypesE, derived=False, changeable=True,
                      default_value=CommandTypesE.RETRIEVE)
    target = EReference(ordered=True, unique=True, containment=True)
    query = EReference(ordered=True, unique=True, containment=False)

    def __init__(self, *, type=None, target=None, query=None, **kwargs):

        super().__init__(**kwargs)

        if type is not None:
            self.type = type

        if target is not None:
            self.target = target

        if query is not None:
            self.query = query


class CreateCommand(CommandA):

    type = EAttribute(eType=CommandTypesE, derived=False,
                      changeable=True, default_value=CommandTypesE.CREATE)
    packageNsUri = EReference(ordered=True, unique=True, containment=True)
    className = EReference(ordered=True, unique=True, containment=True)
    n = EReference(ordered=True, unique=True, containment=True)

    def __init__(self, *, type=None, packageNsUri=None, className=None, n=None, **kwargs):

        super().__init__(**kwargs)

        if type is not None:
            self.type = type

        if packageNsUri is not None:
            self.packageNsUri = packageNsUri

        if className is not None:
            self.className = className

        if n is not None:
            self.n = n


class UpdateCommand(CommandA):

    type = EAttribute(eType=CommandTypesE, derived=False,
                      changeable=True, default_value=CommandTypesE.UPDATE)
    target = EReference(ordered=True, unique=True, containment=True)
    query = EReference(ordered=True, unique=True, containment=True)
    value = EReference(ordered=True, unique=True, containment=True)

    def __init__(self, *, type=None, target=None, query=None, value=None, **kwargs):

        super().__init__(**kwargs)

        if type is not None:
            self.type = type

        if target is not None:
            self.target = target

        if query is not None:
            self.query = query

        if value is not None:
            self.value = value


class CloneCommand(CommandA):

    type = EAttribute(eType=CommandTypesE, derived=False,
                      changeable=True, default_value=CommandTypesE.CLONE)
    mode = EAttribute(eType=CloneModesE, derived=False, changeable=True)
    target = EReference(ordered=True, unique=True, containment=True)

    def __init__(self, *, type=None, target=None, mode=None, **kwargs):

        super().__init__(**kwargs)

        if type is not None:
            self.type = type

        if mode is not None:
            self.mode = mode

        if target is not None:
            self.target = target


class CallCommand(CommandA):

    type = EAttribute(eType=CommandTypesE, derived=False,
                      changeable=True, default_value=CommandTypesE.CALL)
    action = EReference(ordered=True, unique=True, containment=True)
    args = EReference(ordered=True, unique=True, containment=True)

    def __init__(self, *, type=None, action=None, args=None, **kwargs):

        super().__init__(**kwargs)

        if type is not None:
            self.type = type

        if action is not None:
            self.action = action

        if args is not None:
            self.args = args


class AsyncCallCommand(CommandA):

    type = EAttribute(eType=CommandTypesE, derived=False, changeable=True,
                      default_value=CommandTypesE.ASYNCCALL)
    action = EReference(ordered=True, unique=True, containment=True)
    args = EReference(ordered=True, unique=True, containment=True)

    def __init__(self, *, type=None, action=None, args=None, **kwargs):

        super().__init__(**kwargs)

        if type is not None:
            self.type = type

        if action is not None:
            self.action = action

        if args is not None:
            self.args = args


class CallStatusCommand(CommandA):

    type = EAttribute(eType=CommandTypesE, derived=False, changeable=True,
                      default_value=CommandTypesE.CALLSTATUS)
    callId = EReference(ordered=True, unique=True, containment=True)

    def __init__(self, *, type=None, callId=None, **kwargs):

        super().__init__(**kwargs)

        if type is not None:
            self.type = type

        if callId is not None:
            self.callId = callId


class AbortCallCommand(CommandA):

    type = EAttribute(eType=CommandTypesE, derived=False, changeable=True,
                      default_value=CommandTypesE.ABORTCALL)
    callId = EReference(ordered=True, unique=True, containment=True)

    def __init__(self, *, type=None, callId=None, **kwargs):

        super().__init__(**kwargs)

        if type is not None:
            self.type = type

        if callId is not None:
            self.callId = callId


class CompoundCommand(CommandA):
    """A sequence of commands executed within the same transaction and therefore being atomar."""
    type = EAttribute(eType=CommandTypesE, derived=False, changeable=True,
                      default_value=CommandTypesE.COMPOUND)
    commands = EReference(ordered=True, unique=True, containment=True, upper=-1)

    def __init__(self, *, commands=None, type=None, **kwargs):

        super().__init__(**kwargs)

        if type is not None:
            self.type = type

        if commands:
            self.commands.extend(commands)


class HelloResult(ResultA):

    type = EAttribute(eType=ResultTypesE, derived=False,
                      changeable=True, default_value=ResultTypesE.OK)
    commandType = EAttribute(eType=CommandTypesE, derived=False,
                             changeable=True, default_value=CommandTypesE.HELLO)
    sessionId = EAttribute(eType=EString, derived=False, changeable=True,
                           default_value='123456789ABCDEF')

    def __init__(self, *, type=None, commandType=None, sessionId=None, **kwargs):

        super().__init__(**kwargs)

        if type is not None:
            self.type = type

        if commandType is not None:
            self.commandType = commandType

        if sessionId is not None:
            self.sessionId = sessionId


class GoodbyeResult(ResultA):

    type = EAttribute(eType=ResultTypesE, derived=False,
                      changeable=True, default_value=ResultTypesE.OK)
    commandType = EAttribute(eType=CommandTypesE, derived=False,
                             changeable=True, default_value=CommandTypesE.GOODBYE)

    def __init__(self, *, type=None, commandType=None, **kwargs):

        super().__init__(**kwargs)

        if type is not None:
            self.type = type

        if commandType is not None:
            self.commandType = commandType


class SessionResult(ResultA):

    type = EAttribute(eType=ResultTypesE, derived=False,
                      changeable=True, default_value=ResultTypesE.OK)
    commandType = EAttribute(eType=CommandTypesE, derived=False,
                             changeable=True, default_value=CommandTypesE.SESSION)

    def __init__(self, *, type=None, commandType=None, **kwargs):

        super().__init__(**kwargs)

        if type is not None:
            self.type = type

        if commandType is not None:
            self.commandType = commandType


class StatusResult(ResultA):

    type = EAttribute(eType=ResultTypesE, derived=False,
                      changeable=True, default_value=ResultTypesE.OK)
    commandType = EAttribute(eType=CommandTypesE, derived=False,
                             changeable=True, default_value=CommandTypesE.STATUS)
    changeId = EAttribute(eType=EInt, derived=False, changeable=True, default_value=0)

    def __init__(self, *, type=None, commandType=None, changeId=None, **kwargs):

        super().__init__(**kwargs)

        if type is not None:
            self.type = type

        if commandType is not None:
            self.commandType = commandType

        if changeId is not None:
            self.changeId = changeId


class ChangesResult(ResultA):

    type = EAttribute(eType=ResultTypesE, derived=False,
                      changeable=True, default_value=ResultTypesE.OK)
    commandType = EAttribute(eType=CommandTypesE, derived=False,
                             changeable=True, default_value=CommandTypesE.CHANGES)
    changes = EReference(ordered=True, unique=True, containment=True)

    def __init__(self, *, type=None, commandType=None, changes=None, **kwargs):

        super().__init__(**kwargs)

        if type is not None:
            self.type = type

        if commandType is not None:
            self.commandType = commandType

        if changes is not None:
            self.changes = changes


class RetrieveResult(ResultA):

    type = EAttribute(eType=ResultTypesE, derived=False,
                      changeable=True, default_value=ResultTypesE.OK)
    commandType = EAttribute(eType=CommandTypesE, derived=False,
                             changeable=True, default_value=CommandTypesE.RETRIEVE)
    value = EReference(ordered=True, unique=True, containment=True)

    def __init__(self, *, type=None, commandType=None, value=None, **kwargs):

        super().__init__(**kwargs)

        if type is not None:
            self.type = type

        if commandType is not None:
            self.commandType = commandType

        if value is not None:
            self.value = value


class CreateResult(ResultA):

    type = EAttribute(eType=ResultTypesE, derived=False,
                      changeable=True, default_value=ResultTypesE.OK)
    commandType = EAttribute(eType=CommandTypesE, derived=False,
                             changeable=True, default_value=CommandTypesE.CREATE)
    value = EReference(ordered=True, unique=True, containment=True)

    def __init__(self, *, type=None, commandType=None, value=None, **kwargs):

        super().__init__(**kwargs)

        if type is not None:
            self.type = type

        if commandType is not None:
            self.commandType = commandType

        if value is not None:
            self.value = value


class UpdateResult(ResultA):

    type = EAttribute(eType=ResultTypesE, derived=False,
                      changeable=True, default_value=ResultTypesE.OK)
    commandType = EAttribute(eType=CommandTypesE, derived=False,
                             changeable=True, default_value=CommandTypesE.UPDATE)
    target = EReference(ordered=True, unique=True, containment=True)

    def __init__(self, *, type=None, commandType=None, target=None, **kwargs):

        super().__init__(**kwargs)

        if type is not None:
            self.type = type

        if commandType is not None:
            self.commandType = commandType

        if target is not None:
            self.target = target


class CloneResult(ResultA):

    type = EAttribute(eType=ResultTypesE, derived=False,
                      changeable=True, default_value=ResultTypesE.OK)
    commandType = EAttribute(eType=CommandTypesE, derived=False,
                             changeable=True, default_value=CommandTypesE.CLONE)
    value = EReference(ordered=True, unique=True, containment=True)

    def __init__(self, *, type=None, commandType=None, value=None, **kwargs):

        super().__init__(**kwargs)

        if type is not None:
            self.type = type

        if commandType is not None:
            self.commandType = commandType

        if value is not None:
            self.value = value


class CallResult(ResultA):

    type = EAttribute(eType=ResultTypesE, derived=False,
                      changeable=True, default_value=ResultTypesE.OK)
    commandType = EAttribute(eType=CommandTypesE, derived=False,
                             changeable=True, default_value=CommandTypesE.CALL)
    callId = EAttribute(eType=EInt, derived=False, changeable=True, default_value=0)
    returnValues = EReference(ordered=True, unique=True, containment=False)

    def __init__(self, *, type=None, commandType=None, callId=None, returnValues=None, **kwargs):

        super().__init__(**kwargs)

        if type is not None:
            self.type = type

        if commandType is not None:
            self.commandType = commandType

        if callId is not None:
            self.callId = callId

        if returnValues is not None:
            self.returnValues = returnValues


class AsyncCallResult(ResultA):

    type = EAttribute(eType=ResultTypesE, derived=False,
                      changeable=True, default_value=ResultTypesE.OK)
    commandType = EAttribute(eType=CommandTypesE, derived=False,
                             changeable=True, default_value=CommandTypesE.ASYNCCALL)
    callId = EAttribute(eType=EInt, derived=False, changeable=True, default_value=0)

    def __init__(self, *, type=None, commandType=None, callId=None, **kwargs):

        super().__init__(**kwargs)

        if type is not None:
            self.type = type

        if commandType is not None:
            self.commandType = commandType

        if callId is not None:
            self.callId = callId


class CallStatusResult(ResultA):

    type = EAttribute(eType=ResultTypesE, derived=False,
                      changeable=True, default_value=ResultTypesE.OK)
    commandType = EAttribute(eType=CommandTypesE, derived=False,
                             changeable=True, default_value=CommandTypesE.CALLSTATUS)
    callStatus = EAttribute(eType=CallStatusE, derived=False, changeable=True)
    callId = EAttribute(eType=EInt, derived=False, changeable=True, default_value=0)
    result = EReference(ordered=True, unique=True, containment=True)

    def __init__(self, *, type=None, commandType=None, callStatus=None, callId=None, result=None, **kwargs):

        super().__init__(**kwargs)

        if type is not None:
            self.type = type

        if commandType is not None:
            self.commandType = commandType

        if callStatus is not None:
            self.callStatus = callStatus

        if callId is not None:
            self.callId = callId

        if result is not None:
            self.result = result


class AbortCallResult(ResultA):

    type = EAttribute(eType=ResultTypesE, derived=False,
                      changeable=True, default_value=ResultTypesE.OK)
    commandType = EAttribute(eType=CommandTypesE, derived=False,
                             changeable=True, default_value=CommandTypesE.ABORTCALL)

    def __init__(self, *, type=None, commandType=None, **kwargs):

        super().__init__(**kwargs)

        if type is not None:
            self.type = type

        if commandType is not None:
            self.commandType = commandType


class ErrorResult(ResultA):

    type = EAttribute(eType=ResultTypesE, derived=False,
                      changeable=True, default_value=ResultTypesE.ERROR)
    commandType = EAttribute(eType=CommandTypesE, derived=False, changeable=True)
    code = EAttribute(eType=EInt, derived=False, changeable=True, default_value=0)
    message = EAttribute(eType=EString, derived=False, changeable=True)

    def __init__(self, *, type=None, commandType=None, code=None, message=None, **kwargs):

        super().__init__(**kwargs)

        if type is not None:
            self.type = type

        if commandType is not None:
            self.commandType = commandType

        if code is not None:
            self.code = code

        if message is not None:
            self.message = message


class CompoundResult(ResultA):

    type = EAttribute(eType=ResultTypesE, derived=False, changeable=True,
                      default_value=ResultTypesE.COMPOUND_OK)
    commandType = EAttribute(eType=CommandTypesE, derived=False,
                             changeable=True, default_value=CommandTypesE.COMPOUND)
    results = EReference(ordered=True, unique=True, containment=True, upper=-1)

    def __init__(self, *, type=None, commandType=None, results=None, **kwargs):

        super().__init__(**kwargs)

        if type is not None:
            self.type = type

        if commandType is not None:
            self.commandType = commandType

        if results:
            self.results.extend(results)


class QueryValue(Value):

    type = EAttribute(eType=ValueTypesE, derived=False,
                      changeable=True, default_value=ValueTypesE.QUERY)
    v = EReference(ordered=True, unique=True, containment=False)

    def __init__(self, *, type=None, v=None, **kwargs):

        super().__init__(**kwargs)

        if type is not None:
            self.type = type

        if v is not None:
            self.v = v


@abstract
class RecursiveSegmetA(Segment):

    processingType = EAttribute(eType=SegmentProcessingTypesE, derived=False,
                                changeable=True, default_value=SegmentProcessingTypesE.RECURSIVE)

    def __init__(self, *, processingType=None, **kwargs):

        super().__init__(**kwargs)

        if processingType is not None:
            self.processingType = processingType


@abstract
class LinearSegmetA(Segment):

    processingType = EAttribute(eType=SegmentProcessingTypesE, derived=False,
                                changeable=True, default_value=SegmentProcessingTypesE.LINEAR)

    def __init__(self, *, processingType=None, **kwargs):

        super().__init__(**kwargs)

        if processingType is not None:
            self.processingType = processingType


class Directory(NamedElementA, PathElementA):

    subdirectories = EReference(ordered=True, unique=True, containment=True, upper=-1)
    resources = EReference(ordered=True, unique=True, containment=True, upper=-1)

    def __init__(self, *, subdirectories=None, resources=None, **kwargs):

        super().__init__(**kwargs)

        if subdirectories:
            self.subdirectories.extend(subdirectories)

        if resources:
            self.resources.extend(resources)


class ModelResource(FileResourceA):

    type = EAttribute(eType=FileResourceTypesE, derived=False,
                      changeable=True, default_value=FileResourceTypesE.MODEL)
    isMetaModel = EAttribute(eType=EBoolean, derived=False,
                             changeable=True, upper=-1, default_value=False)
    isWritable = EAttribute(eType=EBoolean, derived=False,
                            changeable=True, upper=-1, default_value=True)
    contents = EReference(ordered=True, unique=True, containment=True, upper=-1)
    domain = EReference(ordered=True, unique=True, containment=False)

    def __init__(self, *, type=None, isMetaModel=None, isWritable=None, contents=None, domain=None, **kwargs):

        super().__init__(**kwargs)

        if type is not None:
            self.type = type

        if isMetaModel:
            self.isMetaModel.extend(isMetaModel)

        if isWritable:
            self.isWritable.extend(isWritable)

        if contents:
            self.contents.extend(contents)

        if domain is not None:
            self.domain = domain


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


class ResourceSegment(RecursiveSegmetA):

    type = EAttribute(eType=SegmentTypesE, derived=False, changeable=True,
                      default_value=SegmentTypesE.RESOURCE)
    startCharacter = EAttribute(eType=EChar, derived=False, changeable=True, default_value=':')

    def __init__(self, *, type=None, startCharacter=None, **kwargs):

        super().__init__(**kwargs)

        if type is not None:
            self.type = type

        if startCharacter is not None:
            self.startCharacter = startCharacter


class PathSegment(RecursiveSegmetA):

    type = EAttribute(eType=SegmentTypesE, derived=False,
                      changeable=True, default_value=SegmentTypesE.PATH)
    startCharacter = EAttribute(eType=EChar, derived=False, changeable=True, default_value='/')
    feature = EReference(ordered=True, unique=True, containment=False)

    def __init__(self, *, type=None, startCharacter=None, feature=None, **kwargs):

        super().__init__(**kwargs)

        if type is not None:
            self.type = type

        if startCharacter is not None:
            self.startCharacter = startCharacter

        if feature is not None:
            self.feature = feature


class ClassSegment(RecursiveSegmetA):

    startCharacter = EAttribute(eType=EChar, derived=False, changeable=True, default_value='$')
    type = EAttribute(eType=SegmentTypesE, derived=False,
                      changeable=True, default_value=SegmentTypesE.CLAZZ)
    clazz = EReference(ordered=True, unique=True, containment=False)

    def __init__(self, *, startCharacter=None, type=None, clazz=None, **kwargs):

        super().__init__(**kwargs)

        if startCharacter is not None:
            self.startCharacter = startCharacter

        if type is not None:
            self.type = type

        if clazz is not None:
            self.clazz = clazz


class InstanceOfSegment(RecursiveSegmetA):

    type = EAttribute(eType=SegmentTypesE, derived=False, changeable=True,
                      default_value=SegmentTypesE.INSTANCE)
    startCharacter = EAttribute(eType=EChar, derived=False, changeable=True, default_value='?')
    clazz = EReference(ordered=True, unique=True, containment=False)

    def __init__(self, *, type=None, startCharacter=None, clazz=None, **kwargs):

        super().__init__(**kwargs)

        if type is not None:
            self.type = type

        if startCharacter is not None:
            self.startCharacter = startCharacter

        if clazz is not None:
            self.clazz = clazz


class IdSegment(RecursiveSegmetA):

    type = EAttribute(eType=SegmentTypesE, derived=False,
                      changeable=True, default_value=SegmentTypesE.ID)
    startCharacter = EAttribute(eType=EChar, derived=False, changeable=True, default_value='#')
    element = EReference(ordered=True, unique=True, containment=False)

    def __init__(self, *, type=None, startCharacter=None, element=None, **kwargs):

        super().__init__(**kwargs)

        if type is not None:
            self.type = type

        if startCharacter is not None:
            self.startCharacter = startCharacter

        if element is not None:
            self.element = element


class MetaSegment(RecursiveSegmetA):

    type = EAttribute(eType=SegmentTypesE, derived=False,
                      changeable=True, default_value=SegmentTypesE.META)
    startCharacter = EAttribute(eType=EChar, derived=False, changeable=True, default_value='@')
    identifierType = EAttribute(eType=MetaSegmentIdentifiersE, derived=False, changeable=True)

    def __init__(self, *, type=None, startCharacter=None, identifierType=None, **kwargs):

        super().__init__(**kwargs)

        if type is not None:
            self.type = type

        if startCharacter is not None:
            self.startCharacter = startCharacter

        if identifierType is not None:
            self.identifierType = identifierType


class HistorySegment(RecursiveSegmetA):

    type = EAttribute(eType=SegmentTypesE, derived=False, changeable=True,
                      default_value=SegmentTypesE.HISTORY)
    startCharacter = EAttribute(eType=EChar, derived=False, changeable=True, default_value='!')
    element = EReference(ordered=True, unique=True, containment=False)

    def __init__(self, *, type=None, startCharacter=None, element=None, **kwargs):

        super().__init__(**kwargs)

        if type is not None:
            self.type = type

        if startCharacter is not None:
            self.startCharacter = startCharacter

        if element is not None:
            self.element = element


class ListOpSegment(LinearSegmetA):

    type = EAttribute(eType=SegmentTypesE, derived=False,
                      changeable=True, default_value=SegmentTypesE.LISTOP)
    startCharacter = EAttribute(eType=EChar, derived=False, changeable=True, default_value='.')
    identifierType = EAttribute(eType=ListOpSegmentTypesE, derived=False, changeable=True)

    def __init__(self, *, type=None, startCharacter=None, identifierType=None, **kwargs):

        super().__init__(**kwargs)

        if type is not None:
            self.type = type

        if startCharacter is not None:
            self.startCharacter = startCharacter

        if identifierType is not None:
            self.identifierType = identifierType


class SelectorSegment(RecursiveSegmetA):

    type = EAttribute(eType=SegmentTypesE, derived=False, changeable=True,
                      default_value=SegmentTypesE.SELECTOR)
    startCharacter = EAttribute(eType=EChar, derived=False, changeable=True, default_value='{')

    def __init__(self, *, type=None, startCharacter=None, **kwargs):

        super().__init__(**kwargs)

        if type is not None:
            self.type = type

        if startCharacter is not None:
            self.startCharacter = startCharacter


class IndexSegment(LinearSegmetA):

    type = EAttribute(eType=SegmentTypesE, derived=False,
                      changeable=True, default_value=SegmentTypesE.INDEX)
    startCharacter = EAttribute(eType=EChar, derived=False, changeable=True, default_value='[')

    def __init__(self, *, type=None, startCharacter=None, **kwargs):

        super().__init__(**kwargs)

        if type is not None:
            self.type = type

        if startCharacter is not None:
            self.startCharacter = startCharacter


@abstract
class LocalDomainA(DomainA, Directory, ActionHandlerA):

    baseDir = EAttribute(eType=EString, derived=False, changeable=True)
    baseDirAbs = EAttribute(eType=EString, derived=False, changeable=True)
    baseDirCwd = EAttribute(eType=EString, derived=False, changeable=True)

    def __init__(self, *, baseDir=None, baseDirAbs=None, baseDirCwd=None, **kwargs):

        super().__init__(**kwargs)

        if baseDir is not None:
            self.baseDir = baseDir

        if baseDirAbs is not None:
            self.baseDirAbs = baseDirAbs

        if baseDirCwd is not None:
            self.baseDirCwd = baseDirCwd
