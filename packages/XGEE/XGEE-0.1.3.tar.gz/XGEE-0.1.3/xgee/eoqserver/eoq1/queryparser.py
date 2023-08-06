'''
	Author Bjoern Annighoefer Mar 2019
'''

from .error import EoqParseError
from .model import *

### CONSTANTS

#context constants
CONTEXT_TYPE_DONTCARE = 1 #Don't check the class type
CONTEXT_TYPE_EXPLICIT = 2 #Check the class type

#return multiplicity

CONTEXT_MULTIPLICITY_UNCHANGED = 1 #always return a list
CONTEXT_MULTIPLICITY_FLATTENED = 2 #always return a list of depth 1
CONTEXT_MULTIPLICITY_FORCESINGLE = 3 #always return a single object

#segment type constants
SEGTYPE_PATH = 2
SEGTYPE_CLASS = 3
SEGTYPE_INSTANCE = 4
SEGTYPE_ID = 5
SEGTYPE_META = 6
SEGTYPE_RESOURCE = 7
SEGTYPE_HISTORY = 8
SEGTYPE_LISTOP = 9

#selector types
SELTYPE_EQUAL = 1 #=
SELTYPE_DIFFERENT = 2 #~
SELTYPE_GREATER = 3 #>
SELTYPE_SMALLER = 4 #<

#selector value types
VALTYPE_INT = 1
VALTYPE_BOOL = 2
VALTYPE_FLOAT = 3
VALTYPE_STRING = 4
VALTYPE_ID = 5
VALTYPE_HISTORY = 6
VALTYPE_UNSET = 7

INDTYPE_NUMBER = 1 #1,2,3,4,5,6
INDTYPE_RANGE = 2 #1:3,:
INDTYPE_APPEND = 3 #+ (add after the last element. Only valid for add operations)
INDTYPE_REMOVE = 4 #- (remove element from array or unset attribute or reference)

################ MAIN CLASS ###############

class QueryParser:
	@staticmethod
	def __ResolveSegment(queryStr,segInfo):
		identifier = queryStr[segInfo['identifierStart']:segInfo['identifierEnd']+1]
		
		segment = None
		if(SEGTYPE_PATH==segInfo['type']):
			segment = PathSegment()
		elif(SEGTYPE_CLASS==segInfo['type']):
			segment = ClassSegment()
		elif(SEGTYPE_INSTANCE==segInfo['type']):
			segment = InstanceOfSegment()
		elif(SEGTYPE_ID==segInfo['type']):
			segment = IdSegment()
		elif(SEGTYPE_HISTORY==segInfo['type']):
			segment = HistorySegment()
		elif(SEGTYPE_META==segInfo['type']):
			if(identifier in MetaSegmentIdentifiersE):
				segment = MetaSegment()
				segment.identifierType = MetaSegmentIdentifiersE.from_string(identifier)
			else: 
				raise EoqParseError('ERROR(META_IDENTIFIER)',"Unknown meta segment: %s"%(identifier),queryStr)
		elif(SEGTYPE_LISTOP==segInfo['type']):
			if(identifier in ListOpSegmentTypesE):
				segment = ListOpSegment()
				segment.identifierType = ListOpSegmentTypesE.from_string(identifier)
			else: 
				raise EoqParseError('ERROR(LISTOP_IDENTIFIER)',"Unknown list operation: %s"%(identifier),queryStr)
		elif(SEGTYPE_RESOURCE==segInfo['type']):
			segment = ResourceSegment()
		else:
			raise EoqParseError('ERROR(SEGMENT_TYPE)',"Unknown segment type %d"%(segInfo['type']),queryStr)

		segment.identifier = identifier
		
		#check for correct identifier values
		
		if(segInfo['hasSelector']):
			segment.selector = Selector()
			segment.selector.name = queryStr[segInfo['selectorStart']:segInfo['selectorEnd']+1]
			## Get the value an comperator
			valueStr = queryStr[segInfo['valueStart']:segInfo['valueEnd']+1]
			if(VALTYPE_INT == segInfo['valueType'] or VALTYPE_FLOAT == segInfo['valueType'] or VALTYPE_STRING == segInfo['valueType']):
				if(SELTYPE_EQUAL == segInfo['selectorType']):
					segment.selector.operator = EqualOperator()
				elif(SELTYPE_DIFFERENT == segInfo['selectorType']):
					segment.selector.operator = NotEqualOperator()
				elif(SELTYPE_GREATER == segInfo['selectorType']):
					segment.selector.operator = GreaterOperator()
				elif(SELTYPE_SMALLER == segInfo['selectorType']):
					segment.selector.operator = LessOperator()
				else:
					raise EoqParseError("ERROR: Unknown comperator %d"%(segInfo['selectorType']),queryStr)
				#set the selector
				if(VALTYPE_INT == segInfo['valueType']):
					segment.selector.value = IntValue(v=int(valueStr))
				elif(VALTYPE_FLOAT == segInfo['valueType']):
					segment.selector.value = FloatValue(v=float(valueStr))
				elif(VALTYPE_STRING == segInfo['valueType']):
					segment.selector.value = StringValue(v=valueStr)
				
			elif(VALTYPE_BOOL == segInfo['valueType'] or VALTYPE_ID == segInfo['valueType'] or VALTYPE_HISTORY == segInfo['valueType'] or VALTYPE_UNSET == segInfo['valueType']):
				if(SELTYPE_EQUAL == segInfo['selectorType']):
					segment.selector.operator = EqualOperator()
				elif(SELTYPE_DIFFERENT == segInfo['selectorType']):
					segment.selector.operator = NotEqualOperator()
				elif(SELTYPE_GREATER == segInfo['selectorType']):
					raise EoqParseError(1,"Unsupported comperator > (%d)"%(segInfo['selectorType']),queryStr)
				elif(SELTYPE_SMALLER == segInfo['selectorType']):
					raise EoqParseError(2,"Unsupported comperator < (%d)"%(segInfo['selectorType']),queryStr)
				
				if(VALTYPE_BOOL == segInfo['valueType']):
					segment.selector.value = BoolValue()
					if('true' == valueStr):
						segment.selector.value.v = True
					elif('false' == valueStr):
						segment.selector.value.v = False
					else:
						raise EoqParseError(3,"Unsupported boolean value '%s'. Should be 'true' or 'false'."%(valueStr),queryStr)
					
				elif(VALTYPE_ID == segInfo['valueType']):
					segment.selector.value = ObjectRefValue(v=int(valueStr))
					
				elif(VALTYPE_HISTORY == segInfo['valueType']):
					segment.selector.value = HistoryRefValue(v=int(valueStr))
				
				elif(VALTYPE_UNSET == segInfo['valueType']):
					segment.selector.value = EmptyValue()
				
		#evaluate depth
		#depth = 1 #default depth for segments
		if(segInfo['hasDepth']):
			segment.depth = Depth()
			segment.depth.value = int(queryStr[segInfo['depthStart']:segInfo['depthEnd']+1])
# 		else:
# 			if(SEGTYPE_CLASS==segInfo['type']) or (SEGTYPE_INSTANCE==segInfo['type']):
# 				segment.depth = Depth()
# 				segment.depth.value = 1 #default depth for class recovery is infinity
			
		#consider the index
		if(segInfo['hasIndex']):
			indexStr = queryStr[segInfo['indexStart']:segInfo['indexEnd']+1]
			if(INDTYPE_NUMBER==segInfo['indexType']):
				segment.index = NumberIndex()
				segment.index.value = int(indexStr)
			elif(INDTYPE_RANGE==segInfo['indexType']):
				lowerUpper = indexStr.split(':')
				segment.index = RangeIndex()
				if(2 == len(lowerUpper)):
					segment.index.lower = int(lowerUpper[0])
					segment.index.upper = int(lowerUpper[1])
				elif(1==len(lowerUpper) and ':' == indexStr[0]):
					segment.index.lower = 1
					segment.index.upper = int(lowerUpper[0])
				elif(1==len(lowerUpper) and ':' == indexStr[-1]):
					segment.index.lower = int(lowerUpper[0])
					segment.index.upper = 0 #last element
				else:
					raise EoqParseError(4,"Bad index string '%s'. Possible is [2],[2:4],[+],[-]"%(indexStr),queryStr)
			elif(INDTYPE_APPEND==segInfo['indexType']):
				segment.index = AddIndex()
			elif(INDTYPE_REMOVE==segInfo['indexType']):
				segment.index = RemoveIndex()
			else:
				#Should never go here
				raise EoqParseError(5,"ERROR: Unsupported index type %d."%(segInfo['indexType']),queryStr)
		return segment
	
	@staticmethod
	def __RetrieveSourceClass(queryStr,contextInfo):
		sourceClass = None
		sourceClassName = queryStr[contextInfo['nameStart']:contextInfo['nameEnd']+1]
		if(not '*' == sourceClassName):
			sourceClass = SourceClass()
			sourceClass.name = sourceClassName
			sourceClass.dontCare = False
		return sourceClass
	
	@staticmethod
	def __RetrieveReturnMultiplicity(queryStr,contextInfo):
		returnMultiplicity = None
		if(contextInfo['contextMultiplicity'] == CONTEXT_MULTIPLICITY_FORCESINGLE):
			returnMultiplicity = ForceSingleReturnMultiplicity()
		elif(contextInfo['contextMultiplicity'] == CONTEXT_MULTIPLICITY_UNCHANGED):
			returnMultiplicity = UnchangedReturnMuliplicity()
		elif(contextInfo['contextMultiplicity'] == CONTEXT_MULTIPLICITY_FLATTENED):
			returnMultiplicity = FlattenedReturnMultiplicity()
		return returnMultiplicity

	@staticmethod
	def StringToQuery(queryStr):
		query = Query()
		
		contextInfo = {}
		segInfo = {}
		
		#definition of states for queryStr parser
		#state constants
		START = 1
		CONTEXT_CLASS_START = 2
		CONTEXT_CLASS = 3
		
		CONTEXT_MULTIPLICITY_START = 4
		CONTEXT_MULTIPLICITY = 5
		
		PATH_START = 6
		IDENTIFIER_START = 7
		IDENTIFIER = 8
		DEPTH_START = 9
		DEPTH = 10
		SELECTOR_START = 11
		SELECTOR = 12
		VALUE_START = 13
		VALUE = 14
		INDEX_START = 15
		INDEX = 16
		
		state = START
		
		#query context information
		contextInfo['contextType'] = CONTEXT_TYPE_DONTCARE
		contextInfo['contextClass'] = None
		contextInfo['contextMultiplicity'] = CONTEXT_MULTIPLICITY_UNCHANGED
		
		contextInfo['nameStart'] = 0
		contextInfo['nameEnd'] = 0
		
		#properties of a segment
		segInfo['type'] = 0
		segInfo['hasDepth'] = False
		segInfo['hasSelector'] = False
		segInfo['hasIndex'] = False
		
		#variables for parsing
		segInfo['identifierStart'] = 0
		segInfo['identifierEnd'] = 0
		segInfo['depthStart'] = 0
		segInfo['depthEnd'] = 0
		segInfo['selectorType'] = 0
		segInfo['selectorStart'] = 0
		segInfo['selectorEnd'] = 0
		segInfo['valueType'] = 0
		segInfo['valueStart'] = 0
		segInfo['valueEnd'] = 0
		segInfo['indexType'] = 0
		segInfo['indexStart'] = 0
		segInfo['indexEnd'] = 0
		
		n = len(queryStr)
		
		for i in range(n):
			c = queryStr[i]
			if(START == state):
				if('(' == c):
					contextInfo['nameStart'] = i+1
					state = CONTEXT_CLASS_START
				elif('/' == c):
					segInfo['type'] = SEGTYPE_PATH
					segInfo['identifierStart'] = i+1
					state = IDENTIFIER_START
				elif('$' == c):
					segInfo['type'] = SEGTYPE_CLASS
					segInfo['identifierStart'] = i+1
					state = IDENTIFIER_START
				elif('#' == c):
					segInfo['type'] = SEGTYPE_ID
					segInfo['identifierStart'] = i+1
					state = IDENTIFIER_START
				elif('?' == c):
					segInfo['type'] = SEGTYPE_INSTANCE
					segInfo['identifierStart'] = i+1
					state = IDENTIFIER_START
				elif('@' == c):
					segInfo['type'] = SEGTYPE_META
					segInfo['identifierStart'] = i+1
					state = IDENTIFIER_START
				elif(':' == c):
					segInfo['type'] = SEGTYPE_RESOURCE
					segInfo['identifierStart'] = i+1
					state = IDENTIFIER_START
				elif('!' == c):
					segInfo['type'] = SEGTYPE_HISTORY
					segInfo['identifierStart'] = i+1
					state = IDENTIFIER_START
				elif('.' == c):
					segInfo['type'] = SEGTYPE_LISTOP
					segInfo['identifierStart'] = i+1
					state = IDENTIFIER_START
				else:
					raise EoqParseError(10,'Unexpected character \'%c\' at %d'%(c,i),queryStr)
			elif(CONTEXT_CLASS_START == state):
				if(c.isalpha() or '*'==c):
					contextInfo['nameEnd'] = i
					state = CONTEXT_CLASS
				else:
					raise EoqParseError(11,'Unexpected character \'%c\' at %d'%(c,i),queryStr)
			elif(CONTEXT_CLASS == state):
				if(c.isalpha() or c.isdigit() or '*'==c):
					contextInfo['nameEnd'] = i
					state = CONTEXT_CLASS
				elif(':'==c):
					#contextInfo = self.__EvaluateContext(root,queryStr,contextInfo)
					sourceClass = QueryParser.__RetrieveSourceClass(queryStr,contextInfo)
					query.sourceClass = sourceClass
					state = CONTEXT_MULTIPLICITY_START
				elif(')'==c):
					#contextInfo['contextMultiplicity'] = CONTEXT_MULTIPLICITY_UNCHANGED
					sourceClass = QueryParser.__RetrieveSourceClass(queryStr,contextInfo)
					query.sourceClass = sourceClass
					state = PATH_START
				else:
					raise EoqParseError(12,'Unexpected character \'%c\' at %d'%(c,i),queryStr)
			elif(CONTEXT_MULTIPLICITY_START == state):
				if('1'==c):
					contextInfo['contextMultiplicity'] = CONTEXT_MULTIPLICITY_FORCESINGLE
					state = CONTEXT_MULTIPLICITY
				elif('_'==c):
					contextInfo['contextMultiplicity'] = CONTEXT_MULTIPLICITY_FLATTENED
					state = CONTEXT_MULTIPLICITY
				elif('*'==c):
					contextInfo['contextMultiplicity'] = CONTEXT_MULTIPLICITY_UNCHANGED
					state = CONTEXT_MULTIPLICITY
				else:
					raise EoqParseError(13,'Unexpected character \'%c\' at %d'%(c,i),queryStr)
			elif(CONTEXT_MULTIPLICITY == state):
				if(')'==c):
					returnMultiplicity = QueryParser.__RetrieveReturnMultiplicity(queryStr,contextInfo)
					query.returnMultiplicity = returnMultiplicity
					state = PATH_START
				else:
					raise EoqParseError(14,'Unexpected character \'%c\' at %d'%(c,i),queryStr)
			elif(PATH_START == state):
				if('/' == c):
					segInfo['type'] = SEGTYPE_PATH
					segInfo['identifierStart'] = i+1
					state = IDENTIFIER_START
				elif('$' == c):
					segInfo['type'] = SEGTYPE_CLASS
					segInfo['identifierStart'] = i+1
					state = IDENTIFIER_START
				elif('#' == c):
					segInfo['type'] = SEGTYPE_ID
					segInfo['identifierStart'] = i+1
					state = IDENTIFIER_START
				elif('?' == c):
					segInfo['type'] = SEGTYPE_INSTANCE
					segInfo['identifierStart'] = i+1
					state = IDENTIFIER_START
				elif('@' == c):
					segInfo['type'] = SEGTYPE_META
					segInfo['identifierStart'] = i+1
					state = IDENTIFIER_START
				elif(':' == c):
					segInfo['type'] = SEGTYPE_RESOURCE
					segInfo['identifierStart'] = i+1
					state = IDENTIFIER_START
				elif('!' == c):
					segInfo['type'] = SEGTYPE_HISTORY
					segInfo['identifierStart'] = i+1
					state = IDENTIFIER_START
				elif('.' == c):
					segInfo['type'] = SEGTYPE_LISTOP
					segInfo['identifierStart'] = i+1
					state = IDENTIFIER_START
				else:
					raise EoqParseError(15,'Unexpected character \'%c\' at %d'%(c,i),queryStr)
			
			elif(IDENTIFIER_START == state):
				#reset segment properties
				segInfo['hasDepth'] = False
				segInfo['hasSelector'] = False
				segInfo['hasIndex'] = False
				if(SEGTYPE_RESOURCE == segInfo['type']):
					if(c.isalpha() or '_' == c or '.' == c):
						segInfo['identifierEnd'] = i
						state = IDENTIFIER
					else:
						raise EoqParseError(16,'Unexpected character \'%c\' at %d'%(c,i),queryStr)
				else:
					if(c.isalpha() or '_' == c):
						segInfo['identifierEnd'] = i
						state = IDENTIFIER
					else:
						raise EoqParseError(16,'Unexpected character \'%c\' at %d'%(c,i),queryStr)
			elif(IDENTIFIER == state):
				if(c.isalpha() or '_' == c  or ('0' <= c and c <= '9') or '\\' == c):
					segInfo['identifierEnd'] = i
				elif(SEGTYPE_RESOURCE == segInfo['type'] and '.'==c): #special case of reverse path to container
					segInfo['identifierEnd'] = i
				elif('{'==c):
					segInfo['hasSelector'] = True
					segInfo['selectorStart'] = i+1
					state = SELECTOR_START
				elif('['==c):
					segInfo['hasIndex'] = True
					segInfo['indexStart'] = i+1
					state = INDEX_START
				elif('<'==c):
					segInfo['hasDepth'] = True
					segInfo['depthStart'] = i+1
					state = DEPTH_START
				elif('/' == c):
					segment = QueryParser.__ResolveSegment(queryStr,segInfo)
					query.segments.add(segment)
					segInfo['type'] = SEGTYPE_PATH
					segInfo['identifierStart'] = i+1
					state = IDENTIFIER_START
				elif('$' == c):
					segment = QueryParser.__ResolveSegment(queryStr,segInfo)
					query.segments.add(segment)
					segInfo['type'] = SEGTYPE_CLASS
					segInfo['identifierStart'] = i+1
					state = IDENTIFIER_START
				elif('?' == c):
					segment = QueryParser.__ResolveSegment(queryStr,segInfo)
					query.segments.add(segment)
					segInfo['type'] = SEGTYPE_INSTANCE
					segInfo['identifierStart'] = i+1
					state = IDENTIFIER_START
				elif('#' == c):
					segment = QueryParser.__ResolveSegment(queryStr,segInfo)
					query.segments.add(segment)
					segInfo['type'] = SEGTYPE_ID
					segInfo['identifierStart'] = i+1
					state = IDENTIFIER_START
				elif('@' == c):
					segment = QueryParser.__ResolveSegment(queryStr,segInfo)
					query.segments.add(segment)
					segInfo['type'] = SEGTYPE_META
					segInfo['identifierStart'] = i+1
					state = IDENTIFIER_START
				elif('!' == c):
					segment = QueryParser.__ResolveSegment(queryStr,segInfo)
					query.segments.add(segment)
					segInfo['type'] = SEGTYPE_HISTORY
					segInfo['identifierStart'] = i+1
					state = IDENTIFIER_START
				elif('.' == c):
					segment = QueryParser.__ResolveSegment(queryStr,segInfo)
					query.segments.add(segment)
					segInfo['type'] = SEGTYPE_LISTOP
					segInfo['identifierStart'] = i+1
					state = IDENTIFIER_START
# 				elif(':' == c): # There can not be a second resource
# 					segInfo['type'] = SEGTYPE_RESOURCE
# 					segInfo['identifierStart'] = i+1
# 					state = IDENTIFIER_START
				else:
					raise EoqParseError(17,'Unexpected character \'%c\' at %d'%(c,i),queryStr)
			elif(DEPTH_START == state):
				if(('0' <= c and c <= '9') or '-' == c):
					segInfo['depthEnd'] = i
					state = DEPTH
				else:
					raise EoqParseError(18,'Unexpected character \'%c\' at %d'%(c,i),queryStr)
			elif(DEPTH == state):
				if('0' <= c and c <= '9'):
					segInfo['depthEnd'] = i
				elif('>'==c):
					state = IDENTIFIER
				else:
					raise EoqParseError(19,'Unexpected character \'%c\' at %d'%(c,i),queryStr)
			elif(SELECTOR_START == state):
				if(c.isalpha()):
					segInfo['selectorEnd'] = i
					state = SELECTOR
				else:
					raise EoqParseError(20,'Unexpected character \'%c\' at %d'%(c,i),queryStr)
			elif(SELECTOR == state):
				if(c.isalpha()):
					segInfo['selectorEnd'] = i
				elif('='==c):
					segInfo['selectorType'] = SELTYPE_EQUAL
					segInfo['valueStart'] = i+1
					state = VALUE_START
				elif('~'==c):
					segInfo['selectorType'] = SELTYPE_DIFFERENT
					segInfo['valueStart'] = i+1
					state = VALUE_START
				elif('>'==c):
					segInfo['selectorType'] = SELTYPE_GREATER
					segInfo['valueStart'] = i+1
					state = VALUE_START
				elif('<'==c):
					segInfo['selectorType'] = SELTYPE_SMALLER
					segInfo['valueStart'] = i+1
					state = VALUE_START
				else:
					raise EoqParseError(22,'Unexpected character \'%c\' at %d'%(c,i),queryStr)
			elif(VALUE_START == state):
				if(('0' <= c and c <= '9') or '-' == c):
					segInfo['valueEnd'] = i
					segInfo['valueType'] = VALTYPE_INT
					state = VALUE
				elif('.'==c):
					segInfo['valueEnd'] = i
					segInfo['valueType'] = VALTYPE_FLOAT
					state = VALUE
				elif('t'==c or 'f'==c):
					segInfo['valueEnd'] = i
					segInfo['valueType'] = VALTYPE_BOOL
					state = VALUE
				elif('#'==c):
					segInfo['valueStart'] = i+1
					segInfo['valueEnd'] = i+1
					segInfo['valueType'] = VALTYPE_ID
					state = VALUE
				elif('$'==c):
					segInfo['valueStart'] = i+1
					segInfo['valueEnd'] = i+1
					segInfo['valueType'] = VALTYPE_HISTORY
					state = VALUE
				elif('\''==c):
					segInfo['valueStart'] = i+1
					segInfo['valueEnd'] = i+1
					segInfo['valueType'] = VALTYPE_STRING
					state = VALUE
				elif('%'==c):
					segInfo['valueStart'] = i
					segInfo['valueEnd'] = i
					segInfo['valueType'] = VALTYPE_UNSET
					state = VALUE
				else:
					raise EoqParseError(23,'Unexpected character \'%c\' at %d'%(c,i),queryStr)
			elif(VALUE == state):
				if('}'==c):
					state = IDENTIFIER
				elif(VALTYPE_INT==segInfo['valueType'] and ('0' <= c and c <= '9')):
					segInfo['valueEnd'] = i
				elif(VALTYPE_ID==segInfo['valueType'] and ('0' <= c and c <= '9')):
					segInfo['valueEnd'] = i
				elif(VALTYPE_HISTORY==segInfo['valueType'] and ('0' <= c and c <= '9')):
					segInfo['valueEnd'] = i
				elif(VALTYPE_INT==segInfo['valueType'] and'.'==c):
					segInfo['valueEnd'] = i
					segInfo['valueType'] = VALTYPE_FLOAT
				elif(VALTYPE_BOOL==segInfo['valueType'] and c.isalpha()):
					segInfo['valueEnd'] = i
				elif(VALTYPE_STRING==segInfo['valueType'] and '\''!=c):
					segInfo['valueEnd'] = i
				elif(VALTYPE_STRING==segInfo['valueType'] and '\''==c):
					segInfo['valueEnd'] = i-1 # not necessary, but a statement is required
				else:
					raise EoqParseError(24,'Unexpected character \'%c\' at %d'%(c,i),queryStr)
			elif(INDEX_START == state):
				if('0' <= c and c <= '9'):
					segInfo['indexEnd'] = i
					segInfo['indexType'] = INDTYPE_NUMBER
					state = INDEX
				elif('+' == c):
					segInfo['indexEnd'] = i
					segInfo['indexType'] = INDTYPE_APPEND
					state = INDEX
				elif('-' == c):
					segInfo['indexEnd'] = i
					segInfo['indexType'] = INDTYPE_REMOVE
					state = INDEX
				elif(':' == c):
					segInfo['indexEnd'] = i
					segInfo['indexType'] = INDTYPE_RANGE
					state = INDEX
				else:
					raise EoqParseError(25,'Unexpected character \'%c\' at %d'%(c,i),queryStr)
			elif(INDEX == state):
				if('0' <= c and c <= '9') and (INDTYPE_NUMBER == segInfo['indexType'] or INDTYPE_RANGE == segInfo['indexType']):
					segInfo['indexEnd'] = i
				elif(':' == c) and (INDTYPE_NUMBER == segInfo['indexType'] or INDTYPE_RANGE == segInfo['indexType']):
					segInfo['indexEnd'] = i
					segInfo['indexType'] = INDTYPE_RANGE
					state = INDEX
				elif(']'==c):
					state = IDENTIFIER
				else:
					raise EoqParseError(26,'Unexpected character \'%c\' at %d'%(c,i),queryStr)
		
		#evaluate last segment
		segment = QueryParser.__ResolveSegment(queryStr,segInfo)
		query.segments.add(segment)
		#result = lastSegmentHandler(root,queryStr,segInfo)
		return query
	
	@staticmethod
	def QueryToString(query):
		queryStr = ''
		if(query.sourceClass or query.returnMultiplicity):
			sourceClassName = ('*' if(not query.sourceClass or query.sourceClass.dontCare) else query.sourceClass.name)
			multiplicityChar = ('*' if(not query.returnMultiplicity) else query.returnMultiplicity.symbol)
			queryStr += '(%s:%c)'%(sourceClassName,multiplicityChar)
		for segment in query.segments:
			queryStr += '%c%s'%(segment.startCharacter,segment.identifier)
			if(segment.selector):
				selector = segment.selector
				value = selector.value
				valueStr = ''
				if(value.type == ValueTypesE.INT):
					valueStr = str(value.v)
				elif(value.type == ValueTypesE.FLOAT):
					valueStr = str(value.v)
				elif(value.type == ValueTypesE.BOOL):
					valueStr = ('true' if value.v else 'false')
				elif(value.type == ValueTypesE.STRING):
					valueStr = '\'%s\''%(value.v)
				elif(value.type == ValueTypesE.OBJECTREF):
					valueStr = '#%d'%(value.v)
				elif(value.type == ValueTypesE.HISTORYREF):
					valueStr = '$%d'%(value.v)
				elif(value.type == ValueTypesE.EMPTY):
					valueStr = '#'
				queryStr += '{%s%c%s}'%(selector.name,selector.operator.symbol,valueStr)
			if(segment.index):
				index = segment.index
				if(index.type == IndexTypesE.NUMBER):
					queryStr += '[%d]'%(index.value)
				elif(index.type == IndexTypesE.RANGE):
					queryStr += '[%d:%d]'%(index.lower,index.upper)
				elif(index.type == IndexTypesE.ADD):
					queryStr += '[+]'
				elif(index.type == IndexTypesE.REMOVE):
					queryStr += '[-]'
			if(segment.depth):
				queryStr += '<%d>'%(segment.depth.value)
		return queryStr