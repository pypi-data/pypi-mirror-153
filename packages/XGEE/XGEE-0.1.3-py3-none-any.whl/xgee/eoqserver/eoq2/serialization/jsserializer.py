'''
 Bjoern Annighoefer 2019
'''

from .serializer import Serializer

from ..query.query import QrySegTypes
from ..command.command import CmdTypes
from ..util.error import EoqError



'''
Javascript Serializer   

'''

JS_PREFIX = "new eoq2."
   
class JsSerializer(Serializer):
    def __init__(self):
        self.cmdTranslators = {
            CmdTypes.GET : lambda o,p: p+"Get("+self._Ser(o.a,p)+")",
            CmdTypes.SET : lambda o,p: p+"Set("+",".join([self._Ser(a,p) for a in o.a])+")",
            CmdTypes.ADD : lambda o,p: p+"Add("+",".join([self._Ser(a,p) for a in o.a])+")",
            CmdTypes.REM : lambda o,p: p+"Rem("+",".join([self._Ser(a,p) for a in o.a])+")",
            CmdTypes.MOV : lambda o,p: p+"Mov("+",".join([self._Ser(a,p) for a in o.a])+")",
            CmdTypes.CLO : lambda o,p: p+"Clo("+",".join([self._Ser(a,p) for a in o.a])+")",
            CmdTypes.CRN : lambda o,p: p+"Crn("+",".join([self._Ser(a,p) for a in o.a])+")",
            CmdTypes.CRT : lambda o,p: p+"Crt("+",".join([self._Ser(a,p) for a in o.a])+")",
            CmdTypes.QRF : lambda o,p: p+"Qrf("+self._Ser(o.a,p)+")",
            CmdTypes.CPR : lambda o,p: p+"Cpr("+self._Ser(o.a[0],p)+","+self._Ser(o.a[1],p)+","+self._Ser(o.a[2],p)+")",
            CmdTypes.MRG : lambda o,p: p+"Mrg("+self._Ser(o.a[0],p)+","+self._Ser(o.a[1],p)+","+self._Ser(o.a[2],p)+")",
            CmdTypes.GMM : lambda o,p: p+"Gmm()",
            CmdTypes.RMM : lambda o,p: p+"Rmm("+self._Ser(o.a,p)+")",
            CmdTypes.UMM : lambda o,p: p+"Umm("+self._Ser(o.a,p)+")",
            CmdTypes.HEL : lambda o,p: p+"Hel("+self._Ser(o.a[0],p)+","+self._Ser(o.a[1],p)+")",
            CmdTypes.SES : lambda o,p: p+"Ses("+self._Ser(o.a,p)+")",
            CmdTypes.GBY : lambda o,p: p+"Gby("+self._Ser(o.a,p)+")",
            CmdTypes.STS : lambda o,p: p+"Sts()",
            CmdTypes.CHG : lambda o,p: p+"Chg("+",".join([self._Ser(a,p) for a in o.a])+")",
            CmdTypes.OBS : lambda o,p: p+"Obs("+self._Ser(o.a[0],p)+","+self._Ser(o.a[1],p)+")",
            CmdTypes.UBS : lambda o,p: p+"Ubs("+self._Ser(o.a[0],p)+","+self._Ser(o.a[1],p)+")",
            CmdTypes.GAA : lambda o,p: p+"Gaa()",
            CmdTypes.CAL : lambda o,p: p+"Cal("+self._Ser(o.a[0],p)+","+self._Ser(o.a[1:],p)+")",
            CmdTypes.ASC : lambda o,p: p+"Asc("+self._Ser(o.a[0],p)+","+self._Ser(o.a[1:],p)+")",
            CmdTypes.ABC : lambda o,p: p+"Abc("+self._Ser(o.a,p)+")",
            CmdTypes.ADC : lambda o,p: p+"Adc("+",".join([self._Ser(a,p) for a in o.a])+")",
            CmdTypes.GAC : lambda o,p: p+"Gac()",
            CmdTypes.VAL : lambda o,p: p+"Val()",
            CmdTypes.RMC : lambda o,p: p+"Rmc("+self._Ser(o.a,p)+")",
            CmdTypes.CST : lambda o,p: p+"Cst("+self._Ser(o.a,p)+")",
            CmdTypes.CMP : lambda o,p: p+"Cmp()."+".".join([self._Ser(a,"") for a in o.a]),
            CmdTypes.MUT : lambda o,p: p+"Mut()",
            CmdTypes.UMT : lambda o,p: p+"Umt()"
            }
        self.qryTranslators = {     
            QrySegTypes.OBJ : lambda o,p: "Obj("+self._Ser(o.v,p)+")",
            QrySegTypes.HIS : lambda o,p: "His("+self._Ser(o.v,p)+")",
            QrySegTypes.PTH : lambda o,p: "Pth("+self._Ser(o.v,p)+")",
            QrySegTypes.CLS : lambda o,p: "Cls("+self._Ser(o.v,p)+")",
            QrySegTypes.INO : lambda o,p: "Ino("+self._Ser(o.v,p)+")",
            QrySegTypes.MET : lambda o,p: "Met("+self._Ser(o.v[0],p)+(","+self._Ser(o.v[1:],p) if len(o.v)>1 else "")+")",
            QrySegTypes.NOT : lambda o,p: "Not()",
            QrySegTypes.TRM : lambda o,p: "Trm("+self._Ser(o.v[0],p)+","+self._Ser(o.v[1],p)+")",
            QrySegTypes.CNS : lambda o,p: "Cns()",
            QrySegTypes.TRY : lambda o,p: "Try("+self._Ser(o.v[0],p)+","+self._Ser(o.v[1],p)+")",
            QrySegTypes.IDX : lambda o,p: "Idx("+self._Ser(o.v,p)+")",
            QrySegTypes.SEL : lambda o,p: "Sel("+self._Ser(o.v,p)+")",
            QrySegTypes.ARR : lambda o,p: "Arr(["+",".join([self._Ser(a,p) for a in o.v])+"])",
            QrySegTypes.ZIP : lambda o,p: "Zip("+self._Ser(o.v,p)+")",
            QrySegTypes.QRY : lambda o,p: p+"Qry()."+".".join([self._Ser(a,p) for a in o.v]),
            QrySegTypes.ANY : lambda o,p: "Any("+self._Ser(o.v,p)+")",
            QrySegTypes.ALL : lambda o,p: "All("+self._Ser(o.v,p)+")",
            QrySegTypes.EQU : lambda o,p: "Equ("+self._Ser(o.v,p)+")",
            QrySegTypes.EQA : lambda o,p: "Eqa("+self._Ser(o.v,p)+")",
            QrySegTypes.NEQ : lambda o,p: "Neq("+self._Ser(o.v,p)+")",
            QrySegTypes.LES : lambda o,p: "Les("+self._Ser(o.v,p)+")",
            QrySegTypes.GRE : lambda o,p: "Gre("+self._Ser(o.v,p)+")",
            QrySegTypes.RGX : lambda o,p: "Rgx("+self._Ser(o.v,p)+")",
            QrySegTypes.ADD : lambda o,p: "Add("+self._Ser(o.v,p)+")",
            QrySegTypes.SUB : lambda o,p: "Sub("+self._Ser(o.v,p)+")",
            QrySegTypes.MUL : lambda o,p: "Mul("+self._Ser(o.v,p)+")",
            QrySegTypes.ORR : lambda o,p: "Orr("+self._Ser(o.v,p)+")",
            QrySegTypes.XOR : lambda o,p: "Xor("+self._Ser(o.v,p)+")",
            QrySegTypes.AND : lambda o,p: "And("+self._Ser(o.v,p)+")",
            QrySegTypes.NAD : lambda o,p: "Nad("+self._Ser(o.v,p)+")",
            QrySegTypes.DIV : lambda o,p: "Div("+self._Ser(o.v,p)+")",
            QrySegTypes.CSP : lambda o,p: "Csp("+self._Ser(o.v,p)+")",
            QrySegTypes.ITS : lambda o,p: "Its("+self._Ser(o.v,p)+")",
            QrySegTypes.DIF : lambda o,p: "Dif("+self._Ser(o.v,p)+")",
            QrySegTypes.UNI : lambda o,p: "Uni("+self._Ser(o.v,p)+")",
            QrySegTypes.CON : lambda o,p: "Con("+self._Ser(o.v,p)+")"
            }
        self.priTranslators = {
            #primitive types
            bool : lambda o,p: str(o),
            int : lambda o,p: str(o),
            float : lambda o,p: str(o),
            bool : lambda o,p: str(o),
            str : lambda o,p: "'"+o+"'",
            list : lambda o,p: "[%s]"%(",".join([self._Ser(x,p) for x in o])),
            type(None) : lambda o,p: str(o)
            }
        
    def Ser(self,val):
        return self._Ser(val,JS_PREFIX)
    
    def _Ser(self,val,p):
        try: 
            return self.cmdTranslators[val.cmd](val,p)
        except:
            try: 
                return self.qryTranslators[val.qry](val,JS_PREFIX)
            except:
                try:
                    return self.priTranslators[type(val)](val,JS_PREFIX)
                except:
                    raise EoqError(0,"Text serializer failed for %s"%(str(val)))
    
    def Des(self,code):
        pass