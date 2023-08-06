'''
Annighoefer 2019
'''

from .model import *
from .error import EoqValueError,EoqParseError

from pyecore.ecore import EObject

import types
from urllib.parse import quote,unquote  #for escaping strings

class ValueParser:
    @staticmethod
    def ValueToString(value):
        if(value.type in (ValueTypesE.INT,ValueTypesE.FLOAT)):
            return str(value.v)
        elif(value.type == ValueTypesE.BOOL):
            if(value.v):
                return 'true'
            else:
                return 'false'
        elif(value.type == ValueTypesE.STRING):
            return "'%s'"%(quote(value.v))
        elif(value.type == ValueTypesE.OBJECTREF):
            return '#%d'%(value.v)
        elif(value.type == ValueTypesE.HISTORYREF):
            return '$%d'%(value.v)
        elif(value.type == ValueTypesE.OBJECT):
            return '#%s'%(str(value.v))
        elif(value.type == ValueTypesE.EMPTY):
            return '%'
        elif(value.type == ValueTypesE.LIST):
            substrs = []
            for v in value.v:
                substrs += [ValueParser.ValueToString(v)]
            return '[%s]'%(','.join(substrs))
        else:
            raise EoqValueError(1,'Cannot convert EOQ value %s string'%(type(value)),value)
    
    @staticmethod
    def StringToValue(valueStr):
        #definition of the parser states
        VALUE_START = 1
        VALUE = 2
        VALUE_END = 3
        #start of parsing
        rootValueContainer = ListValue() #initialize the value with an empty list
        currentValueContainer = rootValueContainer
        state = VALUE_START
        valueStart = 0;
        valueEnd = 0;
        valueType = None
        nOpenBrakets = 0
        
        n = len(valueStr)
        for i in range(n):
            c = valueStr[i]
            if(VALUE_START == state):
                valueStart = i
                valueEnd = i
                if(('0' <= c and c <= '9') or '-' == c):
                    valueType = ValueTypesE.INT
                    state = VALUE
                elif('.'==c):
                    valueType = ValueTypesE.FLOAT
                    state = VALUE
                elif('t'==c or 'f'==c):
                    valueType = ValueTypesE.BOOL
                    state = VALUE
                elif('#'==c):
                    valueStart = i+1
                    valueEnd = i+1
                    valueType = ValueTypesE.OBJECTREF
                    state = VALUE
                elif('\''==c):
                    valueStart = i+1
                    valueEnd = i+1
                    valueType = ValueTypesE.STRING
                    state = VALUE
                elif('%'==c):
                    valueStart = i+1
                    valueEnd = i+1
                    valueType = ValueTypesE.EMPTY
                    state = VALUE
                elif('$'==c):
                    valueStart = i+1
                    valueEnd = i+1
                    valueType = ValueTypesE.HISTORYREF
                    state = VALUE
                elif('['==c):
                    valueType = ValueTypesE.LIST
                    nOpenBrakets += 1
                    sublist = ListValue()
                    currentValueContainer.v.add(sublist)
                    currentValueContainer = sublist
                    state = VALUE_START
                elif(']'==c):
                    #nothing needs to be added because it has already been added
                    nOpenBrakets -= 1
                    currentValueContainer = currentValueContainer.eContainer()
                    state = VALUE_END
                else:
                    raise EoqParseError(10,'Unexpected character \'%c\' at %d'%(c,i),valueStr)
            elif(VALUE == state):
                if(']'==c):
                    currentValueContainer.v.add(ValueParser.__StringToPritiveValue(valueStr[valueStart:valueEnd+1],valueType))
                    nOpenBrakets -= 1
                    currentValueContainer = currentValueContainer.eContainer()
                    state = VALUE_END
                elif(','==c and nOpenBrakets>0):
                    #TODO evaluate the value
                    currentValueContainer.v.add(ValueParser.__StringToPritiveValue(valueStr[valueStart:valueEnd+1],valueType))
                    state = VALUE_START
                elif((ValueTypesE.INT==valueType or ValueTypesE.FLOAT==valueType) and ('0' <= c and c <= '9')):
                    valueEnd = i
                elif(ValueTypesE.OBJECTREF==valueType and ('0' <= c and c <= '9')):
                    valueEnd = i
                elif(ValueTypesE.HISTORYREF==valueType and (('0' <= c and c <= '9') or c == '-')):
                    valueEnd = i
                elif(ValueTypesE.INT==valueType and'.'==c):
                    valueEnd = i
                    valueType = ValueTypesE.FLOAT
                elif(ValueTypesE.BOOL==valueType and c.isalpha()):
                    valueEnd = i
                elif(ValueTypesE.STRING==valueType and '\''!=c):
                    valueEnd = i
                elif(ValueTypesE.STRING==valueType and '\''==c):
                    valueEnd = i-1 #necessary for empty string
                else:
                    raise EoqParseError(11,'Unexpected character \'%c\' at %d'%(c,i),valueStr)
            elif(VALUE_END==state):
                if(']'==c):
                    nOpenBrakets -= 1
                    currentValueContainer = currentValueContainer.eContainer()
                elif(','==c and nOpenBrakets>0):
                    state = VALUE_START
                else:
                    raise EoqParseError(12,'Unexpected character \'%c\' at %d'%(c,i),valueStr)
        
        if(nOpenBrakets>0):
            raise EoqParseError(13,'%d lists are not closed'%(nOpenBrakets),valueStr)
        
        #process the last value
        if(VALUE==state):
            currentValueContainer.v.add(ValueParser.__StringToPritiveValue(valueStr[valueStart:valueEnd+1],valueType))        
        
        return rootValueContainer.v[0]
    
    @staticmethod
    def __StringToPritiveValue(valueStr,valueType):
        value = None
        if(valueType == ValueTypesE.INT):
            value = IntValue()
            value.v = int(valueStr)
        elif(valueType == ValueTypesE.FLOAT):
            value = FloatValue()
            value.v = float(valueStr)
        elif(valueType == ValueTypesE.STRING):
            value = StringValue()
            value.v = unquote(valueStr)
        elif(valueType == ValueTypesE.BOOL):
            value = BoolValue()
            if('true' == valueStr):
                value.v = True
            elif('false' == valueStr):
                value.v = False
            else:
                raise EoqParseError(20,"Unsupported boolean value '%s'. Should be 'true' or 'false'."%(valueStr),valueStr)
        elif(valueType == ValueTypesE.OBJECTREF):
            value = ObjectRefValue()
            value.v = int(valueStr)
        elif(valueType == ValueTypesE.EMPTY):
            value = EmptyValue()
        elif(valueType == ValueTypesE.HISTORYREF):
            value = HistoryRefValue()
            value.v = int(valueStr)
        else:
            raise EoqParseError(21,"Unknown value type '%s'."%(ValueTypesE.to_string(valueType)),valueStr)
        return value
    
    @staticmethod
    def PythonToValue(pvalue):
        if(isinstance(pvalue,bool)): #int is instance of bool, therefore bool must be first.
            return BoolValue(v=pvalue)
        elif(isinstance(pvalue,int)):
            return IntValue(v=pvalue)
        elif(isinstance(pvalue,float)):
            return FloatValue(v=pvalue)
        elif(isinstance(pvalue,str)):
            return StringValue(v=pvalue)
        elif(isinstance(pvalue,ObjectRefValue)):
            return pvalue
        elif(isinstance(pvalue,HistoryRefValue)):
            return pvalue
        elif(isinstance(pvalue,types.FunctionType) or isinstance(pvalue,types.MethodType)):
            return OperationValue(v=pvalue)
        elif(isinstance(pvalue,EObject)):
            return ObjectValue(v=pvalue)
        elif(None == pvalue):
            return EmptyValue()
        elif(isinstance(pvalue,list)):
            value = ListValue()
            for v in pvalue:
                value.v.add(ValueParser.PythonToValue(v))
            return value
        else:
            raise EoqValueError(31,'Cannot convert python data type %s to EOQ value'%(type(pvalue).__name__),pvalue)
        
    @staticmethod
    def ValueToPython(value):
        if(value.type in (ValueTypesE.INT,ValueTypesE.FLOAT,ValueTypesE.BOOL,ValueTypesE.STRING,ValueTypesE.OBJECT)):
            return value.v
        elif(value.type in (ValueTypesE.OBJECTREF,ValueTypesE.HISTORYREF,ValueTypesE.OPERATION)):
            return value
        elif(value.type == ValueTypesE.OPERATION):
            return value.v
        elif(value.type == ValueTypesE.EMPTY):
            return None
        elif(value.type == ValueTypesE.LIST):
            pvalue = []
            for v in value.v:
                pvalue += [ValueParser.ValueToPython(v)]
            return pvalue
        else:
            raise EoqValueError(32,'Cannot convert EOQ value %s to python data type'%(type(value).__name__),value)
        
    @staticmethod
    def CloneValue(value):
        clonedValue = None
        if(value.type == ValueTypesE.LIST):
            clonedValue = ListValue()
            for v in value.v:
                clonedValue.v.add(ValueParser.CloneValue(v))
        elif(value.type == ValueTypesE.OBJECTREF):
            clonedValue = ObjectRefValue(v=value.v)
        elif(value.type == ValueTypesE.INT):
            clonedValue = IntValue(v=value.v)
        elif(value.type == ValueTypesE.STRING):
            clonedValue = StringValue(v=value.v)
        elif(value.type == ValueTypesE.FLOAT):
            clonedValue = FloatValue(v=value.v)
        elif(value.type == ValueTypesE.BOOL):
            clonedValue = BoolValue(v=value.v)
        elif(value.type == ValueTypesE.EMPTY):
            clonedValue = EmptyValue()
        elif(value.type == ValueTypesE.HISTORYREF):
            clonedValue = HistoryRefValue(v=value.v)
        elif(value.type == ValueTypesE.OPERATION):
            clonedValue = OperationValue(v=value.v)
        elif(value.type == ValueTypesE.OBJECT):
            clonedValue == ObjectValue(v=value.v)
        return clonedValue
        
                