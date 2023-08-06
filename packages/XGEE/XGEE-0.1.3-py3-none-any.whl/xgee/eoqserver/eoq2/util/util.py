'''
2019 Bjoern Annighoefer
'''
from .error import EoqError

DATE_TIME_STR_FORMAT = "%m/%d/%Y %H:%M:%S"

'''
    A class indicating that nothing more to process here
'''
class Terminator:
    def __init__(self,v):
        self.v = v
    def __eq__(self, other):
        if(isinstance(other, Terminator)):
            return self.v == other.v
        else:
            return self.v == other

def Determinate(res):
    if(IsList(res)):
        res = [Determinate(r) for r in res]
    elif(isinstance(res, Terminator)):
        res = res.v
    return res

'''
    Operations on multiple objects, structures and lists
    
'''

def ApplyToAllElements(context,functor):
    res = None
    if(IsList(context)):
        res = [ApplyToAllElements(c,functor) for c in context]
    elif(isinstance(context, Terminator)):
        res = res
    else:
        res = functor(context)
    return res

#Applies and operation specified by the functor to all elements of arbitrary
#nested lists as long as they exhibit the same structure
# def ApplyToAllCorrespondingElements(a,b,functor):
#     res = None
#     if(IsList(a)):
#         res = [ApplyToAllCorrespondingElements(a[i],b[i],functor) for i in range(len(a))]
#     else:
#         res = functor(a,b) 
#     return res

def ApplyToAllElementsInA(a,b,functor):
    res = None
    if(IsList(a)):
        res = [ApplyToAllElementsInA(c,b,functor) for c in a]
    elif(isinstance(a, Terminator)):
        res = a
    else:
        res = functor(a,b)
    return res

def ApplyToAllElementsInB(a,b,functor):
    res = None
    if(IsList(b)):
        res = [ApplyToAllElementsInB(a,c,functor) for c in b]
    else:
        res = functor(a,b)
    return res

def ApplyToAllListsOfElementsInA(a,b,functor):
    res = None
    if(IsListOfObjects(a)):
        res = functor(a,b)
    else:
        res = [ApplyToAllListsOfElementsInA(c,b,functor) for c in a]
    return res

def ApplyToAllListsOfElementsInB(a,b,functor):
    res = None
    if(IsListOfObjects(b)):
        res = functor(a,b)
    else:
        res = [ApplyToAllListsOfElementsInB(a,c,functor) for c in b]
    return res

def ApplyToSimilarListsOfObjects(op1,op2,listVsListFunc,listVsStructFunc,structVsListOp,param=None):
    res = None
    if(IsListOfObjects(op1) and IsListOfObjects(op2)):
        res = listVsListFunc(op1,op2,param)
    elif(IsListOfObjects(op1)):
        res = listVsStructFunc(op1,op2,param)
    elif(IsListOfObjects(op2)):
        res = structVsListOp(op1,op2,param)
    elif(len(op1) == len(op2)):
        res = [ApplyToSimilarListsOfObjects(op1[i],op2[i],listVsListFunc,listVsStructFunc,structVsListOp,param) for i in range(len(op1))]
    else:
        raise EoqError(0,"Non comparable element list structures detected.")
    return res

def ApplyToSimilarElementStrutures(op1,op2,elemVsElemFunc,elemVsStruct,structVsElemOp,param=None):
    res = None
    if(IsNoList(op1) and IsNoList(op2)):
        res = elemVsElemFunc(op1,op2,param)
    elif(IsNoList(op1)):
        res = elemVsStruct(op1,op2,param)
    elif(IsNoList(op2)):
        res = structVsElemOp(op1,op2,param)
    elif(len(op1) == len(op2)):
        res = [ApplyToSimilarElementStrutures(op1[i],op2[i],elemVsElemFunc,elemVsStruct,structVsElemOp,param) for i in range(len(op1))]
    else:
        raise EoqError(0,"Non comparable element structures detected.")
    return res

def IsList(obj):
    return (isinstance(obj,list) and not isinstance(obj,str))

def IsNoList(obj):
    return (not isinstance(obj,list) or isinstance(obj,str))

def IsListOfObjects(obj):
    if(IsList(obj)):
        if(len(obj)==0): 
            return True
        for o in obj:
            if IsNoList(o):
                return True #any non list object make the search fail
    return False
    #return (IsList(obj) and (len(obj)==0 or IsNoList(obj[0])))

def ShowProgress(progress):
    print('Total progress: %d%%'%(progress))
    return
