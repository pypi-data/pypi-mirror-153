var jseoq = jseoq || {};
jseoq.model = (function() {
	//generated from EClass NamedElementA
	function NamedElementA() {
		//super constructors
		//attributes
	    this.name = 'UNNAMED'; //
		return this;
	};
	
	//generated from EClass DomainA
	function DomainA() {
		//super constructors
		jseoq.model.NamedElementA.call(this);
		//attributes
	    this.version = 'UNKNOWN'; //
	    this.transactionCount =  0; //       
	    this.changeCount =  0; //       
	    this.callCount =  0; //       
	    this.metamodels = []; //Metamodel
	    this.transactions = []; //Transaction
	    this.commands = []; //CommandInfo
	    this.models = []; //EObject
	    this.actions = []; //ActionInfo
	    this.currentTransaction = null; //Transaction
	    this.changes = []; //Change
	    this.actionCalls = []; //ActionCall
		return this;
	};
	DomainA.prototype = Object.create(NamedElementA);
	
	//generated from EClass Metamodel
	function Metamodel() {
		//super constructors
		//attributes
	    this.source = 0;
	    this.name = ''; //
	    this.package = null; //EObject
		return this;
	};
	
//generated from EEnum MetaModelSourcesE
	var MetaModelSourcesE = {
		BUILDIN : 0,
		DYNAMIC : 1,
		to_string : function(id) {
			for(literal in this) {
				if(this[literal] == id) {
					return literal;
				}
			}
			return null;
		},
		from_string : function(literal) {
			return this[literal];
		}
	};
	
	//generated from EClass CommandInfo
	function CommandInfo() {
		//super constructors
		//attributes
	    this.name = ''; //
	    this.description = ''; //
	    this.parameters = []; //CommandParameter
	    this.results = []; //CommandParameter
		return this;
	};
	
	//generated from EClass Transaction
	function Transaction() {
		//super constructors
		//attributes
	    this.id =  0; //       
	    this.starttime = 0.0; //
	    this.endtime = 0.0; //
	    this.deadline = 0.0; //
	    this.maxDuration = 0.0; //
	    this.wasTimedOut =  false; //  
	    this.wasEnded =  false; //  
	    this.history = []; //Value
	    this.changes = []; //Change
		return this;
	};
	
	//generated from EClass Change
	function Change() {
		//super constructors
		//attributes
	    this.changeId =  0; //       
	    this.sourceTranscallId =  0; //       
	    this.target = null; //Value
	    this.query = null; //Query
	    this.newValue = null; //Value
	    this.oldValue = null; //Value
		return this;
	};
	
	//generated from EClass ActionInfo
	function ActionInfo() {
		//super constructors
		//attributes
	    this.name = ''; //
	    this.description = ''; //
	    this.details = ''; //
	    this.parameters = []; //ActionParameter
	    this.results = []; //ActionParameter
	    this.handler = null; //ActionHandlerA
		return this;
	};
	
	//generated from EClass ActionParameter
	function ActionParameter() {
		//super constructors
		//attributes
	    this.name = ''; //
	    this.type = 'String'; //
	    this.lowerBound =  1; //       
	    this.upperBound =  1; //       
	    this.description = ''; //
	    this.default = ''; //
	    this.choices = []; //Choice
		return this;
	};
	
	//generated from EClass Choice
	function Choice() {
		//super constructors
		//attributes
	    this.value = ''; //
		return this;
	};
	
	//generated from EClass ActionHandlerA
	function ActionHandlerA() {
		//super constructors
		//attributes
		return this;
	};
	
	//generated from EClass CommandParameter
	function CommandParameter() {
		//super constructors
		//attributes
	    this.name = ''; //
	    this.type = 'String'; //
	    this.description = ''; //
	    this.example = ''; //
		return this;
	};
	
	//generated from EClass LocalDomainA
	function LocalDomainA() {
		//super constructors
		jseoq.model.DomainA.call(this);
		jseoq.model.Directory.call(this);
		jseoq.model.ActionHandlerA.call(this);
		//attributes
		return this;
	};
	LocalDomainA.prototype = Object.create(DomainA);
	LocalDomainA.prototype = Object.create(Directory);
	LocalDomainA.prototype = Object.create(ActionHandlerA);
	
	//generated from EClass Directory
	function Directory() {
		//super constructors
		jseoq.model.NamedElementA.call(this);
		//attributes
	    this.subdirectories = []; //Directory
	    this.resources = []; //FileResourceA
		return this;
	};
	Directory.prototype = Object.create(NamedElementA);
	
	//generated from EClass FileResourceA
	function FileResourceA() {
		//super constructors
		//attributes
	    this.name = ''; //
	    this.isDirty =  false; //  
	    this.isLoaded =  false; //  
	    this.lastPersistentPath = ''; //
		return this;
	};
	
//generated from EEnum FileResourceTypesE
	var FileResourceTypesE = {
		MODEL : 0,
		TEXT : 1,
		RAW : 2,
		to_string : function(id) {
			for(literal in this) {
				if(this[literal] == id) {
					return literal;
				}
			}
			return null;
		},
		from_string : function(literal) {
			return this[literal];
		}
	};
	
	//generated from EClass ModelResource
	function ModelResource() {
		//super constructors
		jseoq.model.FileResourceA.call(this);
		//attributes
	    this.type = jseoq.model.FileResourceTypesE.MODEL;
	    this.isMetaModel =  false; //  
	    this.isWritable =  true; //  
	    this.contents = []; //EObject
	    this.domain = null; //LocalDomainA
		return this;
	};
	ModelResource.prototype = Object.create(FileResourceA);
	
	//generated from EClass TextResource
	function TextResource() {
		//super constructors
		jseoq.model.FileResourceA.call(this);
		//attributes
	    this.type = jseoq.model.FileResourceTypesE.TEXT;
	    this.lines = ''; //
		return this;
	};
	TextResource.prototype = Object.create(FileResourceA);
	
	//generated from EClass RawResource
	function RawResource() {
		//super constructors
		jseoq.model.FileResourceA.call(this);
		//attributes
	    this.type = jseoq.model.FileResourceTypesE.RAW;
	    this.data =  0; //
		return this;
	};
	RawResource.prototype = Object.create(FileResourceA);
	
	//generated from EClass Query
	function Query() {
		//super constructors
		//attributes
	    this.segments = []; //Segment
	    this.sourceClass = null; //SourceClass
	    this.returnMultiplicity = null; //ReturnMultiplicity
		return this;
	};
	
	//generated from EClass Segment
	function Segment() {
		//super constructors
		//attributes
	    this.identifier = ''; //
	    this.selector = null; //Selector
	    this.index = null; //Index
	    this.depth = null; //Depth
		return this;
	};
	
//generated from EEnum SegmentTypesE
	var SegmentTypesE = {
		RESOURCE : 0,
		PATH : 1,
		ID : 2,
		CLAZZ : 3,
		INSTANCE : 4,
		META : 5,
		HISTORY : 6,
		LISTOP : 7,
		SELECTOR : 8,
		INDEX : 9,
		to_string : function(id) {
			for(literal in this) {
				if(this[literal] == id) {
					return literal;
				}
			}
			return null;
		},
		from_string : function(literal) {
			return this[literal];
		}
	};
	
	//generated from EClass ResourceSegment
	function ResourceSegment() {
		//super constructors
		jseoq.model.RecursiveSegmetA.call(this);
		//attributes
	    this.type = jseoq.model.SegmentTypesE.RESOURCE;
	    this.startCharacter =  ':'; //
		return this;
	};
	ResourceSegment.prototype = Object.create(RecursiveSegmetA);
	
	//generated from EClass PathSegment
	function PathSegment() {
		//super constructors
		jseoq.model.RecursiveSegmetA.call(this);
		//attributes
	    this.type = jseoq.model.SegmentTypesE.PATH;
	    this.startCharacter =  '/'; //
	    this.feature = null; //EObject
		return this;
	};
	PathSegment.prototype = Object.create(RecursiveSegmetA);
	
	//generated from EClass ClassSegment
	function ClassSegment() {
		//super constructors
		jseoq.model.RecursiveSegmetA.call(this);
		//attributes
	    this.startCharacter =  '$'; //
	    this.type = jseoq.model.SegmentTypesE.CLAZZ;
	    this.clazz = null; //EObject
		return this;
	};
	ClassSegment.prototype = Object.create(RecursiveSegmetA);
	
	//generated from EClass InstanceOfSegment
	function InstanceOfSegment() {
		//super constructors
		jseoq.model.RecursiveSegmetA.call(this);
		//attributes
	    this.type = jseoq.model.SegmentTypesE.INSTANCE;
	    this.startCharacter =  '?'; //
	    this.clazz = null; //EObject
		return this;
	};
	InstanceOfSegment.prototype = Object.create(RecursiveSegmetA);
	
	//generated from EClass IdSegment
	function IdSegment() {
		//super constructors
		jseoq.model.RecursiveSegmetA.call(this);
		//attributes
	    this.type = jseoq.model.SegmentTypesE.ID;
	    this.startCharacter =  '#'; //
	    this.element = null; //EObject
		return this;
	};
	IdSegment.prototype = Object.create(RecursiveSegmetA);
	
	//generated from EClass MetaSegment
	function MetaSegment() {
		//super constructors
		jseoq.model.RecursiveSegmetA.call(this);
		//attributes
	    this.type = jseoq.model.SegmentTypesE.META;
	    this.startCharacter =  '@'; //
	    this.identifierType = 0;
		return this;
	};
	MetaSegment.prototype = Object.create(RecursiveSegmetA);
	
//generated from EEnum MetaSegmentIdentifiersE
	var MetaSegmentIdentifiersE = {
		CONTAINER : 0,
		INDEX : 1,
		TYPE : 2,
		CLASS : 3,
		CONTENTS : 4,
		CLASSNAME : 5,
		PACKAGE : 6,
		PACKAGENAME : 7,
		RESOURCE : 8,
		RESOURCENAME : 9,
		CONTAININGFEATURE : 10,
		CONTAININGFEATURENAME : 11,
		FEATURES : 12,
		FEATURENAMES : 13,
		ATTRIBUTES : 14,
		ATTRIBUTENAMES : 15,
		REFERENCES : 16,
		REFERENCENAMES : 17,
		CONTAINMENTS : 18,
		CONTAINMENTNAMES : 19,
		ATTRIBUTEVALUES : 20,
		FEATUREVALUES : 21,
		REFERENCEVALUES : 22,
		CONTAINMENTVALUES : 23,
		to_string : function(id) {
			for(literal in this) {
				if(this[literal] == id) {
					return literal;
				}
			}
			return null;
		},
		from_string : function(literal) {
			return this[literal];
		}
	};
	
	//generated from EClass HistorySegment
	function HistorySegment() {
		//super constructors
		jseoq.model.RecursiveSegmetA.call(this);
		//attributes
	    this.type = jseoq.model.SegmentTypesE.HISTORY;
	    this.startCharacter =  '!'; //
	    this.element = null; //EObject
		return this;
	};
	HistorySegment.prototype = Object.create(RecursiveSegmetA);
	
	//generated from EClass Depth
	function Depth() {
		//super constructors
		//attributes
	    this.value =  1; //       
		return this;
	};
	
	//generated from EClass Index
	function Index() {
		//super constructors
		//attributes
		return this;
	};
	
//generated from EEnum IndexTypesE
	var IndexTypesE = {
		NUMBER : 0,
		RANGE : 1,
		ADD : 2,
		REMOVE : 3,
		FLATTEN : 4,
		to_string : function(id) {
			for(literal in this) {
				if(this[literal] == id) {
					return literal;
				}
			}
			return null;
		},
		from_string : function(literal) {
			return this[literal];
		}
	};
	
	//generated from EClass NumberIndex
	function NumberIndex() {
		//super constructors
		jseoq.model.Index.call(this);
		//attributes
	    this.type = jseoq.model.IndexTypesE.NUMBER;
	    this.value =  0; //       
		return this;
	};
	NumberIndex.prototype = Object.create(Index);
	
	//generated from EClass RangeIndex
	function RangeIndex() {
		//super constructors
		jseoq.model.Index.call(this);
		//attributes
	    this.type = jseoq.model.IndexTypesE.RANGE;
	    this.lower =  1; //       
	    this.upper =  0; //       
		return this;
	};
	RangeIndex.prototype = Object.create(Index);
	
	//generated from EClass AddIndex
	function AddIndex() {
		//super constructors
		jseoq.model.Index.call(this);
		//attributes
	    this.type = jseoq.model.IndexTypesE.ADD;
		return this;
	};
	AddIndex.prototype = Object.create(Index);
	
	//generated from EClass RemoveIndex
	function RemoveIndex() {
		//super constructors
		jseoq.model.Index.call(this);
		//attributes
	    this.type = jseoq.model.IndexTypesE.REMOVE;
		return this;
	};
	RemoveIndex.prototype = Object.create(Index);
	
	//generated from EClass FlattenIndex
	function FlattenIndex() {
		//super constructors
		jseoq.model.Index.call(this);
		//attributes
	    this.type = jseoq.model.IndexTypesE.FLATTEN;
		return this;
	};
	FlattenIndex.prototype = Object.create(Index);
	
	//generated from EClass Selector
	function Selector() {
		//super constructors
		//attributes
	    this.name = ''; //
	    this.value = null; //Value
	    this.operator = null; //Operator
		return this;
	};
	
	//generated from EClass Operator
	function Operator() {
		//super constructors
		//attributes
		return this;
	};
	
//generated from EEnum OperatorTypesE
	var OperatorTypesE = {
		EQUAL : 0,
		NOTEQUAL : 1,
		GREATER : 2,
		LESS : 3,
		to_string : function(id) {
			for(literal in this) {
				if(this[literal] == id) {
					return literal;
				}
			}
			return null;
		},
		from_string : function(literal) {
			return this[literal];
		}
	};
	
	//generated from EClass EqualOperator
	function EqualOperator() {
		//super constructors
		jseoq.model.Operator.call(this);
		//attributes
	    this.type = jseoq.model.OperatorTypesE.EQUAL;
	    this.symbol =  '='; //
		return this;
	};
	EqualOperator.prototype = Object.create(Operator);
	
	//generated from EClass NotEqualOperator
	function NotEqualOperator() {
		//super constructors
		jseoq.model.Operator.call(this);
		//attributes
	    this.type = jseoq.model.OperatorTypesE.NOTEQUAL;
	    this.symbol =  '~'; //
		return this;
	};
	NotEqualOperator.prototype = Object.create(Operator);
	
	//generated from EClass GreaterOperator
	function GreaterOperator() {
		//super constructors
		jseoq.model.Operator.call(this);
		//attributes
	    this.type = jseoq.model.OperatorTypesE.GREATER;
	    this.symbol =  '>'; //
		return this;
	};
	GreaterOperator.prototype = Object.create(Operator);
	
	//generated from EClass LessOperator
	function LessOperator() {
		//super constructors
		jseoq.model.Operator.call(this);
		//attributes
	    this.type = jseoq.model.OperatorTypesE.LESS;
	    this.symbol =  '<'; //
		return this;
	};
	LessOperator.prototype = Object.create(Operator);
	
	//generated from EClass Value
	function Value() {
		//super constructors
		//attributes
		return this;
	};
	
//generated from EEnum ValueTypesE
	var ValueTypesE = {
		INT : 0,
		FLOAT : 1,
		BOOL : 2,
		STRING : 3,
		OBJECTREF : 4,
		EMPTY : 5,
		LIST : 6,
		HISTORYREF : 7,
		OPERATION : 8,
		OBJECT : 9,
		QUERY : 10,
		to_string : function(id) {
			for(literal in this) {
				if(this[literal] == id) {
					return literal;
				}
			}
			return null;
		},
		from_string : function(literal) {
			return this[literal];
		}
	};
	
	//generated from EClass IntValue
	function IntValue() {
		//super constructors
		jseoq.model.Value.call(this);
		//attributes
	    this.type = jseoq.model.ValueTypesE.INT;
	    this.v =  0; //       
		return this;
	};
	IntValue.prototype = Object.create(Value);
	
	//generated from EClass FloatValue
	function FloatValue() {
		//super constructors
		jseoq.model.Value.call(this);
		//attributes
	    this.type = jseoq.model.ValueTypesE.FLOAT;
	    this.v = 0; //
		return this;
	};
	FloatValue.prototype = Object.create(Value);
	
	//generated from EClass BoolValue
	function BoolValue() {
		//super constructors
		jseoq.model.Value.call(this);
		//attributes
	    this.type = jseoq.model.ValueTypesE.BOOL;
	    this.v =  false; //  
		return this;
	};
	BoolValue.prototype = Object.create(Value);
	
	//generated from EClass StringValue
	function StringValue() {
		//super constructors
		jseoq.model.Value.call(this);
		//attributes
	    this.type = jseoq.model.ValueTypesE.STRING;
	    this.v = ''; //
		return this;
	};
	StringValue.prototype = Object.create(Value);
	
	//generated from EClass ObjectRefValue
	function ObjectRefValue() {
		//super constructors
		jseoq.model.Value.call(this);
		//attributes
	    this.type = jseoq.model.ValueTypesE.OBJECTREF;
	    this.v =  0; //       
		return this;
	};
	ObjectRefValue.prototype = Object.create(Value);
	
	//generated from EClass EmptyValue
	function EmptyValue() {
		//super constructors
		jseoq.model.Value.call(this);
		//attributes
	    this.type = jseoq.model.ValueTypesE.EMPTY;
	    this.v = null //	
		return this;
	};
	EmptyValue.prototype = Object.create(Value);
	
	//generated from EClass ListValue
	function ListValue() {
		//super constructors
		jseoq.model.Value.call(this);
		//attributes
	    this.type = jseoq.model.ValueTypesE.LIST;
	    this.v = []; //Value
		return this;
	};
	ListValue.prototype = Object.create(Value);
	
	//generated from EClass HistoryRefValue
	function HistoryRefValue() {
		//super constructors
		jseoq.model.Value.call(this);
		//attributes
	    this.type = jseoq.model.ValueTypesE.HISTORYREF;
	    this.v =  0; //       
		return this;
	};
	HistoryRefValue.prototype = Object.create(Value);
	
	//generated from EClass OperationValue
	function OperationValue() {
		//super constructors
		jseoq.model.Value.call(this);
		//attributes
	    this.type = jseoq.model.ValueTypesE.OPERATION;
		return this;
	};
	OperationValue.prototype = Object.create(Value);
	
	//generated from EClass ObjectValue
	function ObjectValue() {
		//super constructors
		jseoq.model.Value.call(this);
		//attributes
	    this.type = jseoq.model.ValueTypesE.OBJECT;
	    this.v = null; //EObject
		return this;
	};
	ObjectValue.prototype = Object.create(Value);
	
	//generated from EClass SourceClass
	function SourceClass() {
		//super constructors
		//attributes
	    this.dontCare =  true; //  
	    this.name = '*'; //
	    this.type = null; //EObject
		return this;
	};
	
	//generated from EClass ReturnMultiplicity
	function ReturnMultiplicity() {
		//super constructors
		//attributes
		return this;
	};
	
//generated from EEnum ReturnMultiplicityTypeE
	var ReturnMultiplicityTypeE = {
		UNCHANGED : 0,
		FLATTENED : 1,
		FORCESINGLE : 2,
		to_string : function(id) {
			for(literal in this) {
				if(this[literal] == id) {
					return literal;
				}
			}
			return null;
		},
		from_string : function(literal) {
			return this[literal];
		}
	};
	
	//generated from EClass UnchangedReturnMuliplicity
	function UnchangedReturnMuliplicity() {
		//super constructors
		jseoq.model.ReturnMultiplicity.call(this);
		//attributes
	    this.type = jseoq.model.ReturnMultiplicityTypeE.UNCHANGED;
	    this.symbol =  '*'; //
		return this;
	};
	UnchangedReturnMuliplicity.prototype = Object.create(ReturnMultiplicity);
	
	//generated from EClass FlattenedReturnMultiplicity
	function FlattenedReturnMultiplicity() {
		//super constructors
		jseoq.model.ReturnMultiplicity.call(this);
		//attributes
	    this.type = jseoq.model.ReturnMultiplicityTypeE.FLATTENED;
	    this.symbol =  '_'; //
		return this;
	};
	FlattenedReturnMultiplicity.prototype = Object.create(ReturnMultiplicity);
	
	//generated from EClass ForceSingleReturnMultiplicity
	function ForceSingleReturnMultiplicity() {
		//super constructors
		jseoq.model.ReturnMultiplicity.call(this);
		//attributes
	    this.type = jseoq.model.ReturnMultiplicityTypeE.FORCESINGLE;
	    this.symbol =  '1'; //
		return this;
	};
	ForceSingleReturnMultiplicity.prototype = Object.create(ReturnMultiplicity);
	
	//generated from EClass CommandA
	function CommandA() {
		//super constructors
		//attributes
		return this;
	};
	
//generated from EEnum CommandTypesE
	var CommandTypesE = {
		HELLO : 0,
		GOODBYE : 1,
		SESSION : 2,
		STATUS : 3,
		CHANGES : 4,
		RETRIEVE : 5,
		CREATE : 6,
		UPDATE : 7,
		CLONE : 8,
		UNDO : 9,
		CALL : 10,
		ASYNCCALL : 11,
		CALLSTATUS : 12,
		ABORTCALL : 13,
		COMPOUND : 14,
		to_string : function(id) {
			for(literal in this) {
				if(this[literal] == id) {
					return literal;
				}
			}
			return null;
		},
		from_string : function(literal) {
			return this[literal];
		}
	};
	
	//generated from EClass HelloCommand
	function HelloCommand() {
		//super constructors
		jseoq.model.CommandA.call(this);
		//attributes
	    this.type = jseoq.model.CommandTypesE.HELLO;
	    this.identification = null; //Value
	    this.sessionId = null; //Value
		return this;
	};
	HelloCommand.prototype = Object.create(CommandA);
	
	//generated from EClass GoodbyeCommand
	function GoodbyeCommand() {
		//super constructors
		jseoq.model.CommandA.call(this);
		//attributes
	    this.type = jseoq.model.CommandTypesE.GOODBYE;
	    this.sessionId = null; //Value
		return this;
	};
	GoodbyeCommand.prototype = Object.create(CommandA);
	
	//generated from EClass SessionCommand
	function SessionCommand() {
		//super constructors
		jseoq.model.CommandA.call(this);
		//attributes
	    this.type = jseoq.model.CommandTypesE.SESSION;
	    this.sessionId = null; //Value
		return this;
	};
	SessionCommand.prototype = Object.create(CommandA);
	
	//generated from EClass StatusCommand
	function StatusCommand() {
		//super constructors
		jseoq.model.CommandA.call(this);
		//attributes
	    this.type = jseoq.model.CommandTypesE.STATUS;
		return this;
	};
	StatusCommand.prototype = Object.create(CommandA);
	
	//generated from EClass ChangesCommand
	function ChangesCommand() {
		//super constructors
		jseoq.model.CommandA.call(this);
		//attributes
	    this.type = jseoq.model.CommandTypesE.CHANGES;
	    this.earliestChangeId = null; //Value
		return this;
	};
	ChangesCommand.prototype = Object.create(CommandA);
	
	//generated from EClass RetrieveCommand
	function RetrieveCommand() {
		//super constructors
		jseoq.model.CommandA.call(this);
		//attributes
	    this.type = jseoq.model.CommandTypesE.RETRIEVE;
	    this.target = null; //Value
	    this.query = null; //Query
		return this;
	};
	RetrieveCommand.prototype = Object.create(CommandA);
	
	//generated from EClass CreateCommand
	function CreateCommand() {
		//super constructors
		jseoq.model.CommandA.call(this);
		//attributes
	    this.type = jseoq.model.CommandTypesE.CREATE;
	    this.packageNsUri = null; //Value
	    this.className = null; //Value
	    this.n = null; //Value
		return this;
	};
	CreateCommand.prototype = Object.create(CommandA);
	
	//generated from EClass UpdateCommand
	function UpdateCommand() {
		//super constructors
		jseoq.model.CommandA.call(this);
		//attributes
	    this.type = jseoq.model.CommandTypesE.UPDATE;
	    this.target = null; //Value
	    this.query = null; //Query
	    this.value = null; //Value
		return this;
	};
	UpdateCommand.prototype = Object.create(CommandA);
	
//generated from EEnum CloneModesE
	var CloneModesE = {
		CLASS : 0,
		ATTRIBUTES : 1,
		FULL : 2,
		DEEP : 3,
		to_string : function(id) {
			for(literal in this) {
				if(this[literal] == id) {
					return literal;
				}
			}
			return null;
		},
		from_string : function(literal) {
			return this[literal];
		}
	};
	
	//generated from EClass CloneCommand
	function CloneCommand() {
		//super constructors
		jseoq.model.CommandA.call(this);
		//attributes
	    this.type = jseoq.model.CommandTypesE.CLONE;
	    this.mode = 0;
	    this.target = null; //Value
		return this;
	};
	CloneCommand.prototype = Object.create(CommandA);
	
	//generated from EClass CallCommand
	function CallCommand() {
		//super constructors
		jseoq.model.CommandA.call(this);
		//attributes
	    this.type = jseoq.model.CommandTypesE.CALL;
	    this.action = null; //Value
	    this.args = null; //ListValue
		return this;
	};
	CallCommand.prototype = Object.create(CommandA);
	
	//generated from EClass AsyncCallCommand
	function AsyncCallCommand() {
		//super constructors
		jseoq.model.CommandA.call(this);
		//attributes
	    this.type = jseoq.model.CommandTypesE.ASYNCCALL;
	    this.action = null; //Value
	    this.args = null; //ListValue
		return this;
	};
	AsyncCallCommand.prototype = Object.create(CommandA);
	
	//generated from EClass CallStatusCommand
	function CallStatusCommand() {
		//super constructors
		jseoq.model.CommandA.call(this);
		//attributes
	    this.type = jseoq.model.CommandTypesE.CALLSTATUS;
	    this.callId = null; //Value
		return this;
	};
	CallStatusCommand.prototype = Object.create(CommandA);
	
	//generated from EClass AbortCallCommand
	function AbortCallCommand() {
		//super constructors
		jseoq.model.CommandA.call(this);
		//attributes
	    this.type = jseoq.model.CommandTypesE.ABORTCALL;
	    this.callId = null; //Value
		return this;
	};
	AbortCallCommand.prototype = Object.create(CommandA);
	
	//generated from EClass CompoundCommand
	function CompoundCommand() {
		//super constructors
		jseoq.model.CommandA.call(this);
		//attributes
	    this.type = jseoq.model.CommandTypesE.COMPOUND;
	    this.commands = []; //CommandA
		return this;
	};
	CompoundCommand.prototype = Object.create(CommandA);
	
	//generated from EClass ResultA
	function ResultA() {
		//super constructors
		//attributes
	    this.transactionId =  0; //       
		return this;
	};
	
//generated from EEnum ResultTypesE
	var ResultTypesE = {
		OK : 0,
		ERROR : 1,
		COMPOUND_OK : 2,
		COMPOUND_ERROR : 3,
		to_string : function(id) {
			for(literal in this) {
				if(this[literal] == id) {
					return literal;
				}
			}
			return null;
		},
		from_string : function(literal) {
			return this[literal];
		}
	};
	
	//generated from EClass HelloResult
	function HelloResult() {
		//super constructors
		jseoq.model.ResultA.call(this);
		//attributes
	    this.type = jseoq.model.ResultTypesE.OK;
	    this.commandType = jseoq.model.CommandTypesE.HELLO;
	    this.sessionId = '123456789ABCDEF'; //
		return this;
	};
	HelloResult.prototype = Object.create(ResultA);
	
	//generated from EClass GoodbyeResult
	function GoodbyeResult() {
		//super constructors
		jseoq.model.ResultA.call(this);
		//attributes
	    this.type = jseoq.model.ResultTypesE.OK;
	    this.commandType = jseoq.model.CommandTypesE.GOODBYE;
		return this;
	};
	GoodbyeResult.prototype = Object.create(ResultA);
	
	//generated from EClass SessionResult
	function SessionResult() {
		//super constructors
		jseoq.model.ResultA.call(this);
		//attributes
	    this.type = jseoq.model.ResultTypesE.OK;
	    this.commandType = jseoq.model.CommandTypesE.SESSION;
		return this;
	};
	SessionResult.prototype = Object.create(ResultA);
	
	//generated from EClass StatusResult
	function StatusResult() {
		//super constructors
		jseoq.model.ResultA.call(this);
		//attributes
	    this.type = jseoq.model.ResultTypesE.OK;
	    this.commandType = jseoq.model.CommandTypesE.STATUS;
	    this.changeId =  0; //       
		return this;
	};
	StatusResult.prototype = Object.create(ResultA);
	
	//generated from EClass ChangesResult
	function ChangesResult() {
		//super constructors
		jseoq.model.ResultA.call(this);
		//attributes
	    this.type = jseoq.model.ResultTypesE.OK;
	    this.commandType = jseoq.model.CommandTypesE.CHANGES;
	    this.changes = null; //ListValue
		return this;
	};
	ChangesResult.prototype = Object.create(ResultA);
	
	//generated from EClass RetrieveResult
	function RetrieveResult() {
		//super constructors
		jseoq.model.ResultA.call(this);
		//attributes
	    this.type = jseoq.model.ResultTypesE.OK;
	    this.commandType = jseoq.model.CommandTypesE.RETRIEVE;
	    this.value = null; //Value
		return this;
	};
	RetrieveResult.prototype = Object.create(ResultA);
	
	//generated from EClass CreateResult
	function CreateResult() {
		//super constructors
		jseoq.model.ResultA.call(this);
		//attributes
	    this.type = jseoq.model.ResultTypesE.OK;
	    this.commandType = jseoq.model.CommandTypesE.CREATE;
	    this.value = null; //Value
		return this;
	};
	CreateResult.prototype = Object.create(ResultA);
	
	//generated from EClass UpdateResult
	function UpdateResult() {
		//super constructors
		jseoq.model.ResultA.call(this);
		//attributes
	    this.type = jseoq.model.ResultTypesE.OK;
	    this.commandType = jseoq.model.CommandTypesE.UPDATE;
	    this.target = null; //Value
		return this;
	};
	UpdateResult.prototype = Object.create(ResultA);
	
	//generated from EClass CloneResult
	function CloneResult() {
		//super constructors
		jseoq.model.ResultA.call(this);
		//attributes
	    this.type = jseoq.model.ResultTypesE.OK;
	    this.commandType = jseoq.model.CommandTypesE.CLONE;
	    this.value = null; //Value
		return this;
	};
	CloneResult.prototype = Object.create(ResultA);
	
	//generated from EClass CallResult
	function CallResult() {
		//super constructors
		jseoq.model.ResultA.call(this);
		//attributes
	    this.type = jseoq.model.ResultTypesE.OK;
	    this.commandType = jseoq.model.CommandTypesE.CALL;
	    this.callId =  0; //       
	    this.returnValues = null; //Value
		return this;
	};
	CallResult.prototype = Object.create(ResultA);
	
	//generated from EClass AsyncCallResult
	function AsyncCallResult() {
		//super constructors
		jseoq.model.ResultA.call(this);
		//attributes
	    this.type = jseoq.model.ResultTypesE.OK;
	    this.commandType = jseoq.model.CommandTypesE.ASYNCCALL;
	    this.callId =  0; //       
		return this;
	};
	AsyncCallResult.prototype = Object.create(ResultA);
	
	//generated from EClass CallStatusResult
	function CallStatusResult() {
		//super constructors
		jseoq.model.ResultA.call(this);
		//attributes
	    this.type = jseoq.model.ResultTypesE.OK;
	    this.commandType = jseoq.model.CommandTypesE.CALLSTATUS;
	    this.callStatus = 0;
	    this.callId =  0; //       
	    this.result = null; //Value
		return this;
	};
	CallStatusResult.prototype = Object.create(ResultA);
	
	//generated from EClass AbortCallResult
	function AbortCallResult() {
		//super constructors
		jseoq.model.ResultA.call(this);
		//attributes
	    this.type = jseoq.model.ResultTypesE.OK;
	    this.commandType = jseoq.model.CommandTypesE.ABORTCALL;
		return this;
	};
	AbortCallResult.prototype = Object.create(ResultA);
	
	//generated from EClass ErrorResult
	function ErrorResult() {
		//super constructors
		jseoq.model.ResultA.call(this);
		//attributes
	    this.type = jseoq.model.ResultTypesE.ERROR;
	    this.commandType = 0;
	    this.code =  0; //       
	    this.message = ''; //
		return this;
	};
	ErrorResult.prototype = Object.create(ResultA);
	
	//generated from EClass CompoundResult
	function CompoundResult() {
		//super constructors
		jseoq.model.ResultA.call(this);
		//attributes
	    this.type = jseoq.model.ResultTypesE.COMPOUND_OK;
	    this.commandType = jseoq.model.CommandTypesE.COMPOUND;
	    this.results = []; //ResultA
		return this;
	};
	CompoundResult.prototype = Object.create(ResultA);
	
//generated from EEnum CallStatusE
	var CallStatusE = {
		INITIALIZING : 0,
		RUNNING : 1,
		WAITING : 2,
		FINISHED : 3,
		ABORTED : 4,
		ERROR : 5,
		to_string : function(id) {
			for(literal in this) {
				if(this[literal] == id) {
					return literal;
				}
			}
			return null;
		},
		from_string : function(literal) {
			return this[literal];
		}
	};
	
	
	//generated from EClass ActionCall
	function ActionCall() {
		//super constructors
		//attributes
	    this.callId =  0; //       
	    this.callStatus = jseoq.model.CallStatusE.INITIALIZING;
	    this.action = ''; //
	    this.channels = []; //CallChannel
	    this.args = null; //Value
	    this.handler = null; //ActionHandlerA
	    this.returnValues = null; //Value
		return this;
	};
	
	//generated from EClass CallChannel
	function CallChannel() {
		//super constructors
		//attributes
	    this.type = jseoq.model.CallChannelTypesE.OUT;
	    this.name = ''; //
	    this.data = []; //CallChannelData
		return this;
	};
	
	//generated from EClass CallChannelData
	function CallChannelData() {
		//super constructors
		//attributes
	    this.date = ''; //
	    this.data = ''; //
		return this;
	};
	
//generated from EEnum CallChannelTypesE
	var CallChannelTypesE = {
		OUT : 0,
		IN : 1,
		INTERACTIVE : 2,
		to_string : function(id) {
			for(literal in this) {
				if(this[literal] == id) {
					return literal;
				}
			}
			return null;
		},
		from_string : function(literal) {
			return this[literal];
		}
	};
	
	//generated from EClass QueryValue
	function QueryValue() {
		//super constructors
		jseoq.model.Value.call(this);
		//attributes
	    this.type = jseoq.model.ValueTypesE.QUERY;
	    this.v = null; //Query
		return this;
	};
	QueryValue.prototype = Object.create(Value);
	
	//generated from EClass ListOpSegment
	function ListOpSegment() {
		//super constructors
		jseoq.model.LinearSegmetA.call(this);
		//attributes
	    this.type = jseoq.model.SegmentTypesE.LISTOP;
	    this.startCharacter =  '.'; //
	    this.identifierType = 0;
		return this;
	};
	ListOpSegment.prototype = Object.create(LinearSegmetA);
	
//generated from EEnum ListOpSegmentTypesE
	var ListOpSegmentTypesE = {
		SIZE : 0,
		FLATTEN : 1,
		to_string : function(id) {
			for(literal in this) {
				if(this[literal] == id) {
					return literal;
				}
			}
			return null;
		},
		from_string : function(literal) {
			return this[literal];
		}
	};
	
	//generated from EClass RecursiveSegmetA
	function RecursiveSegmetA() {
		//super constructors
		jseoq.model.Segment.call(this);
		//attributes
	    this.processingType = jseoq.model.SegmentProcessingTypesE.RECURSIVE;
		return this;
	};
	RecursiveSegmetA.prototype = Object.create(Segment);
	
	//generated from EClass LinearSegmetA
	function LinearSegmetA() {
		//super constructors
		jseoq.model.Segment.call(this);
		//attributes
	    this.processingType = jseoq.model.SegmentProcessingTypesE.LINEAR;
		return this;
	};
	LinearSegmetA.prototype = Object.create(Segment);
	
//generated from EEnum SegmentProcessingTypesE
	var SegmentProcessingTypesE = {
		RECURSIVE : 0,
		LINEAR : 1,
		to_string : function(id) {
			for(literal in this) {
				if(this[literal] == id) {
					return literal;
				}
			}
			return null;
		},
		from_string : function(literal) {
			return this[literal];
		}
	};
	
	//generated from EClass SelectorSegment
	function SelectorSegment() {
		//super constructors
		jseoq.model.RecursiveSegmetA.call(this);
		//attributes
	    this.type = jseoq.model.SegmentTypesE.SELECTOR;
	    this.startCharacter =  '{'; //
		return this;
	};
	SelectorSegment.prototype = Object.create(RecursiveSegmetA);
	
	//generated from EClass IndexSegment
	function IndexSegment() {
		//super constructors
		jseoq.model.LinearSegmetA.call(this);
		//attributes
	    this.type = jseoq.model.SegmentTypesE.INDEX;
	    this.startCharacter =  '['; //
		return this;
	};
	IndexSegment.prototype = Object.create(LinearSegmetA);
	

	return {
		NamedElementA : NamedElementA,
		DomainA : DomainA,
		Metamodel : Metamodel,
		MetaModelSourcesE : MetaModelSourcesE,
		CommandInfo : CommandInfo,
		Transaction : Transaction,
		Change : Change,
		ActionInfo : ActionInfo,
		ActionParameter : ActionParameter,
		Choice : Choice,
		ActionHandlerA : ActionHandlerA,
		CommandParameter : CommandParameter,
		LocalDomainA : LocalDomainA,
		Directory : Directory,
		FileResourceA : FileResourceA,
		FileResourceTypesE : FileResourceTypesE,
		ModelResource : ModelResource,
		TextResource : TextResource,
		RawResource : RawResource,
		Query : Query,
		Segment : Segment,
		SegmentTypesE : SegmentTypesE,
		ResourceSegment : ResourceSegment,
		PathSegment : PathSegment,
		ClassSegment : ClassSegment,
		InstanceOfSegment : InstanceOfSegment,
		IdSegment : IdSegment,
		MetaSegment : MetaSegment,
		MetaSegmentIdentifiersE : MetaSegmentIdentifiersE,
		HistorySegment : HistorySegment,
		Depth : Depth,
		Index : Index,
		IndexTypesE : IndexTypesE,
		NumberIndex : NumberIndex,
		RangeIndex : RangeIndex,
		AddIndex : AddIndex,
		RemoveIndex : RemoveIndex,
		FlattenIndex : FlattenIndex,
		Selector : Selector,
		Operator : Operator,
		OperatorTypesE : OperatorTypesE,
		EqualOperator : EqualOperator,
		NotEqualOperator : NotEqualOperator,
		GreaterOperator : GreaterOperator,
		LessOperator : LessOperator,
		Value : Value,
		ValueTypesE : ValueTypesE,
		IntValue : IntValue,
		FloatValue : FloatValue,
		BoolValue : BoolValue,
		StringValue : StringValue,
		ObjectRefValue : ObjectRefValue,
		EmptyValue : EmptyValue,
		ListValue : ListValue,
		HistoryRefValue : HistoryRefValue,
		OperationValue : OperationValue,
		ObjectValue : ObjectValue,
		SourceClass : SourceClass,
		ReturnMultiplicity : ReturnMultiplicity,
		ReturnMultiplicityTypeE : ReturnMultiplicityTypeE,
		UnchangedReturnMuliplicity : UnchangedReturnMuliplicity,
		FlattenedReturnMultiplicity : FlattenedReturnMultiplicity,
		ForceSingleReturnMultiplicity : ForceSingleReturnMultiplicity,
		CommandA : CommandA,
		CommandTypesE : CommandTypesE,
		HelloCommand : HelloCommand,
		GoodbyeCommand : GoodbyeCommand,
		SessionCommand : SessionCommand,
		StatusCommand : StatusCommand,
		ChangesCommand : ChangesCommand,
		RetrieveCommand : RetrieveCommand,
		CreateCommand : CreateCommand,
		UpdateCommand : UpdateCommand,
		CloneModesE : CloneModesE,
		CloneCommand : CloneCommand,
		CallCommand : CallCommand,
		AsyncCallCommand : AsyncCallCommand,
		CallStatusCommand : CallStatusCommand,
		AbortCallCommand : AbortCallCommand,
		CompoundCommand : CompoundCommand,
		ResultA : ResultA,
		ResultTypesE : ResultTypesE,
		HelloResult : HelloResult,
		GoodbyeResult : GoodbyeResult,
		SessionResult : SessionResult,
		StatusResult : StatusResult,
		ChangesResult : ChangesResult,
		RetrieveResult : RetrieveResult,
		CreateResult : CreateResult,
		UpdateResult : UpdateResult,
		CloneResult : CloneResult,
		CallResult : CallResult,
		AsyncCallResult : AsyncCallResult,
		CallStatusResult : CallStatusResult,
		AbortCallResult : AbortCallResult,
		ErrorResult : ErrorResult,
		CompoundResult : CompoundResult,
		CallStatusE : CallStatusE,
		Object : Object,
		ActionCall : ActionCall,
		CallChannel : CallChannel,
		CallChannelData : CallChannelData,
		CallChannelTypesE : CallChannelTypesE,
		QueryValue : QueryValue,
		ListOpSegment : ListOpSegment,
		ListOpSegmentTypesE : ListOpSegmentTypesE,
		RecursiveSegmetA : RecursiveSegmetA,
		LinearSegmetA : LinearSegmetA,
		SegmentProcessingTypesE : SegmentProcessingTypesE,
		SelectorSegment : SelectorSegment,
		IndexSegment : IndexSegment
	};
})();
