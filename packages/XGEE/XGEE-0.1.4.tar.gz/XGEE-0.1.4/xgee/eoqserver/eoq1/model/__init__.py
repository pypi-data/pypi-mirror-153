from pyecore.resources import global_registry
from .model import getEClassifier, eClassifiers
from .model import name, nsURI, nsPrefix, eClass
from .model import NamedElementA, DomainA, Metamodel, MetaModelSourcesE, CommandInfo, Transaction, Change, ActionInfo, ActionParameter, Choice, ActionHandlerA, CommandParameter, LocalDomainA, Directory, FileResourceA, FileResourceTypesE, ModelResource, TextResource, RawResource, Query, Segment, SegmentTypesE, ResourceSegment, PathSegment, ClassSegment, InstanceOfSegment, IdSegment, MetaSegment, MetaSegmentIdentifiersE, HistorySegment, Depth, Index, IndexTypesE, NumberIndex, RangeIndex, AddIndex, RemoveIndex, FlattenIndex, Selector, Operator, OperatorTypesE, EqualOperator, NotEqualOperator, GreaterOperator, LessOperator, Value, ValueTypesE, IntValue, FloatValue, BoolValue, StringValue, ObjectRefValue, EmptyValue, ListValue, HistoryRefValue, OperationValue, ObjectValue, SourceClass, ReturnMultiplicity, ReturnMultiplicityTypeE, UnchangedReturnMuliplicity, FlattenedReturnMultiplicity, ForceSingleReturnMultiplicity, CommandA, CommandTypesE, HelloCommand, GoodbyeCommand, SessionCommand, StatusCommand, ChangesCommand, RetrieveCommand, CreateCommand, UpdateCommand, CloneModesE, CloneCommand, CallCommand, AsyncCallCommand, CallStatusCommand, AbortCallCommand, CompoundCommand, ResultA, ResultTypesE, HelloResult, GoodbyeResult, SessionResult, StatusResult, ChangesResult, RetrieveResult, CreateResult, UpdateResult, CloneResult, CallResult, AsyncCallResult, CallStatusResult, AbortCallResult, ErrorResult, CompoundResult, CallStatusE, Object, ActionCall, CallChannel, CallChannelData, CallChannelTypesE, QueryValue, ListOpSegment, ListOpSegmentTypesE, RecursiveSegmetA, LinearSegmetA, SegmentProcessingTypesE, SelectorSegment, IndexSegment, PathElementA

from pyecore.ecore import EObject

from . import model

__all__ = ['NamedElementA', 'DomainA', 'Metamodel', 'MetaModelSourcesE', 'CommandInfo', 'Transaction', 'Change', 'ActionInfo', 'ActionParameter', 'Choice', 'ActionHandlerA', 'CommandParameter', 'LocalDomainA', 'Directory', 'FileResourceA', 'FileResourceTypesE', 'ModelResource', 'TextResource', 'RawResource', 'Query', 'Segment', 'SegmentTypesE', 'ResourceSegment', 'PathSegment', 'ClassSegment', 'InstanceOfSegment', 'IdSegment', 'MetaSegment', 'MetaSegmentIdentifiersE', 'HistorySegment', 'Depth', 'Index', 'IndexTypesE', 'NumberIndex', 'RangeIndex', 'AddIndex', 'RemoveIndex', 'FlattenIndex', 'Selector', 'Operator', 'OperatorTypesE', 'EqualOperator', 'NotEqualOperator', 'GreaterOperator', 'LessOperator', 'Value', 'ValueTypesE', 'IntValue', 'FloatValue', 'BoolValue', 'StringValue', 'ObjectRefValue', 'EmptyValue', 'ListValue', 'HistoryRefValue', 'OperationValue', 'ObjectValue', 'SourceClass', 'ReturnMultiplicity', 'ReturnMultiplicityTypeE',
           'UnchangedReturnMuliplicity', 'FlattenedReturnMultiplicity', 'ForceSingleReturnMultiplicity', 'CommandA', 'CommandTypesE', 'HelloCommand', 'GoodbyeCommand', 'SessionCommand', 'StatusCommand', 'ChangesCommand', 'RetrieveCommand', 'CreateCommand', 'UpdateCommand', 'CloneModesE', 'CloneCommand', 'CallCommand', 'AsyncCallCommand', 'CallStatusCommand', 'AbortCallCommand', 'CompoundCommand', 'ResultA', 'ResultTypesE', 'HelloResult', 'GoodbyeResult', 'SessionResult', 'StatusResult', 'ChangesResult', 'RetrieveResult', 'CreateResult', 'UpdateResult', 'CloneResult', 'CallResult', 'AsyncCallResult', 'CallStatusResult', 'AbortCallResult', 'ErrorResult', 'CompoundResult', 'CallStatusE', 'Object', 'ActionCall', 'CallChannel', 'CallChannelData', 'CallChannelTypesE', 'QueryValue', 'ListOpSegment', 'ListOpSegmentTypesE', 'RecursiveSegmetA', 'LinearSegmetA', 'SegmentProcessingTypesE', 'SelectorSegment', 'IndexSegment', 'PathElementA']

eSubpackages = []
eSuperPackage = None
model.eSubpackages = eSubpackages
model.eSuperPackage = eSuperPackage

DomainA.metamodels.eType = Metamodel
DomainA.transactions.eType = Transaction
DomainA.commands.eType = CommandInfo
DomainA.models.eType = EObject
DomainA.actions.eType = ActionInfo
DomainA.currentTransaction.eType = Transaction
DomainA.changes.eType = Change
DomainA.actionCalls.eType = ActionCall
Metamodel.package.eType = EObject
CommandInfo.parameters.eType = CommandParameter
CommandInfo.results.eType = CommandParameter
Transaction.history.eType = Value
Transaction.changes.eType = Change
Change.target.eType = Value
Change.query.eType = Query
Change.newValue.eType = Value
Change.oldValue.eType = Value
ActionInfo.parameters.eType = ActionParameter
ActionInfo.results.eType = ActionParameter
ActionInfo.handler.eType = ActionHandlerA
ActionParameter.choices.eType = Choice
Directory.subdirectories.eType = Directory
Directory.resources.eType = FileResourceA
ModelResource.contents.eType = EObject
ModelResource.domain.eType = LocalDomainA
Query.segments.eType = Segment
Query.sourceClass.eType = SourceClass
Query.returnMultiplicity.eType = ReturnMultiplicity
Segment.selector.eType = Selector
Segment.index.eType = Index
Segment.depth.eType = Depth
PathSegment.feature.eType = EObject
ClassSegment.clazz.eType = EObject
InstanceOfSegment.clazz.eType = EObject
IdSegment.element.eType = EObject
HistorySegment.element.eType = EObject
Selector.value.eType = Value
Selector.operator.eType = Operator
ListValue.v.eType = Value
ObjectValue.v.eType = EObject
SourceClass.type.eType = EObject
HelloCommand.identification.eType = Value
HelloCommand.sessionId.eType = Value
GoodbyeCommand.sessionId.eType = Value
SessionCommand.sessionId.eType = Value
ChangesCommand.earliestChangeId.eType = Value
RetrieveCommand.target.eType = Value
RetrieveCommand.query.eType = Query
CreateCommand.packageNsUri.eType = Value
CreateCommand.className.eType = Value
CreateCommand.n.eType = Value
UpdateCommand.target.eType = Value
UpdateCommand.query.eType = Query
UpdateCommand.value.eType = Value
CloneCommand.target.eType = Value
CallCommand.action.eType = Value
CallCommand.args.eType = ListValue
AsyncCallCommand.action.eType = Value
AsyncCallCommand.args.eType = ListValue
CallStatusCommand.callId.eType = Value
AbortCallCommand.callId.eType = Value
CompoundCommand.commands.eType = CommandA
ChangesResult.changes.eType = ListValue
RetrieveResult.value.eType = Value
CreateResult.value.eType = Value
UpdateResult.target.eType = Value
CloneResult.value.eType = Value
CallResult.returnValues.eType = Value
CallStatusResult.result.eType = Value
CompoundResult.results.eType = ResultA
ActionCall.channels.eType = CallChannel
ActionCall.args.eType = Value
ActionCall.handler.eType = ActionHandlerA
ActionCall.returnValues.eType = Value
CallChannel.data.eType = CallChannelData
QueryValue.v.eType = Query

otherClassifiers = [MetaModelSourcesE, FileResourceTypesE, SegmentTypesE, MetaSegmentIdentifiersE, IndexTypesE, OperatorTypesE, ValueTypesE,
                    ReturnMultiplicityTypeE, CommandTypesE, CloneModesE, ResultTypesE, CallStatusE, Object, CallChannelTypesE, ListOpSegmentTypesE, SegmentProcessingTypesE]

for classif in otherClassifiers:
    eClassifiers[classif.name] = classif
    classif.ePackage = eClass

for classif in eClassifiers.values():
    eClass.eClassifiers.append(classif.eClass)

for subpack in eSubpackages:
    eClass.eSubpackages.append(subpack.eClass)

register_packages = [model] + eSubpackages
for pack in register_packages:
    global_registry[pack.nsURI] = pack
