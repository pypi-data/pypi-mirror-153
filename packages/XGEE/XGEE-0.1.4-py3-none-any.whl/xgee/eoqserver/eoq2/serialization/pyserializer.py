'''
 Bjoern Annighoefer 2019
'''

from .serializer import Serializer

from ..query.query import QrySegTypes
from ..command.command import CmdTypes
from ..util.error import EoqError



'''
TEXT Serializer   

'''

class PySerializer(Serializer):
    def __init__(self):
        self.cmdTranslators = {
            CmdTypes.GET : lambda o: "Get("+self.Ser(o.a)+")",
            CmdTypes.SET : lambda o: "Set("+",".join([self.Ser(a) for a in o.a])+")",
            CmdTypes.ADD : lambda o: "Add("+",".join([self.Ser(a) for a in o.a])+")",
            CmdTypes.REM : lambda o: "Rem("+",".join([self.Ser(a) for a in o.a])+")",
            CmdTypes.MOV : lambda o: "Mov("+",".join([self.Ser(a) for a in o.a])+")",
            CmdTypes.CLO : lambda o: "Clo("+",".join([self.Ser(a) for a in o.a])+")",
            CmdTypes.CRN : lambda o: "Crn("+",".join([self.Ser(a) for a in o.a])+")",
            CmdTypes.CRT : lambda o: "Crt("+",".join([self.Ser(a) for a in o.a])+")",
            CmdTypes.QRF : lambda o: "Qrf("+self.Ser(o.a)+")",
            CmdTypes.CPR : lambda o: "Cpr("+self.Ser(o.a[0])+","+self.Ser(o.a[1])+","+self.Ser(o.a[2])+")",
            CmdTypes.MRG : lambda o: "Mrg("+self.Ser(o.a[0])+","+self.Ser(o.a[1])+","+self.Ser(o.a[2])+")",
            CmdTypes.GMM : lambda o: "Gmm()",
            CmdTypes.RMM : lambda o: "Rmm("+self.Ser(o.a)+")",
            CmdTypes.UMM : lambda o: "Umm("+self.Ser(o.a)+")",
            CmdTypes.HEL : lambda o: "Hel("+self.Ser(o.a[0])+","+self.Ser(o.a[1])+")",
            CmdTypes.SES : lambda o: "Ses("+self.Ser(o.a)+")",
            CmdTypes.GBY : lambda o: "Gby("+self.Ser(o.a)+")",
            CmdTypes.STS : lambda o: "Sts()",
            CmdTypes.CHG : lambda o: "Chg("+",".join([self.Ser(a) for a in o.a])+")",
            CmdTypes.OBS : lambda o: "Obs("+self.Ser(o.a[0])+","+self.Ser(o.a[1])+")",
            CmdTypes.UBS : lambda o: "Ubs("+self.Ser(o.a[0])+","+self.Ser(o.a[1])+")",
            CmdTypes.GAA : lambda o: "Gaa()",
            CmdTypes.CAL : lambda o: "Cal("+self.Ser(o.a[0])+","+self.Ser(o.a[1:])+")",
            CmdTypes.ASC : lambda o: "Asc("+self.Ser(o.a[0])+","+self.Ser(o.a[1:])+")",
            CmdTypes.ABC : lambda o: "Abc("+self.Ser(o.a)+")",
            CmdTypes.CST : lambda o: "Cst("+self.Ser(o.a)+")",
            CmdTypes.CMP : lambda o: "Cmp()."+".".join([self.Ser(a) for a in o.a]),
            CmdTypes.MUT : lambda o: "Mut()",
            CmdTypes.UMT : lambda o: "Umt()"
            }
        self.qryTranslators = {
            QrySegTypes.OBJ : lambda o: "Obj("+self.Ser(o.v)+")",
            QrySegTypes.HIS : lambda o: "His("+self.Ser(o.v)+")",
            QrySegTypes.PTH : lambda o: "Pth("+self.Ser(o.v)+")",
            QrySegTypes.CLS : lambda o: "Cls("+self.Ser(o.v)+")",
            QrySegTypes.INO : lambda o: "Ino("+self.Ser(o.v)+")",
            QrySegTypes.MET : lambda o: "Met("+self.Ser(o.v[0]) + (","+self.Ser(o.v[1:]) if len(o.v)>1 else "")+")",
            QrySegTypes.NOT : lambda o: "Not()",
            QrySegTypes.TRM : lambda o: "Trm("+self.Ser(o.v[0])+","+self.Ser(o.v[1])+")",
            QrySegTypes.TRY : lambda o: "Try("+self.Ser(o.v[0])+","+self.Ser(o.v[1])+")",
            QrySegTypes.IDX : lambda o: "Idx("+self.Ser(o.v)+")",
            QrySegTypes.SEL : lambda o: "Sel("+self.Ser(o.v)+")",
            QrySegTypes.ARR : lambda o: "Arr(["+",".join([self.Ser(a) for a in o.v])+"])",
            QrySegTypes.ZIP : lambda o: "Zip("+self.Ser(o.v)+")",
            QrySegTypes.QRY : lambda o: "Qry()."+".".join([self.Ser(a) for a in o.v]),
            QrySegTypes.ANY : lambda o: "Any("+self.Ser(o.v)+")",
            QrySegTypes.ALL : lambda o: "All("+self.Ser(o.v)+")",
            QrySegTypes.EQU : lambda o: "Equ("+self.Ser(o.v)+")",
            QrySegTypes.EQA : lambda o: "Eqa("+self.Ser(o.v)+")",
            QrySegTypes.NEQ : lambda o: "Neq("+self.Ser(o.v)+")",
            QrySegTypes.LES : lambda o: "Les("+self.Ser(o.v)+")",
            QrySegTypes.GRE : lambda o: "Gre("+self.Ser(o.v)+")",
            QrySegTypes.RGX : lambda o: "Rgx("+self.Ser(o.v)+")",
            QrySegTypes.ADD : lambda o: "Add("+self.Ser(o.v)+")",
            QrySegTypes.SUB : lambda o: "Sub("+self.Ser(o.v)+")",
            QrySegTypes.MUL : lambda o: "Mul("+self.Ser(o.v)+")",
            QrySegTypes.DIV : lambda o: "Div("+self.Ser(o.v)+")",
            QrySegTypes.ORR : lambda o: "Orr("+self.Ser(o.v)+")",
            QrySegTypes.XOR : lambda o: "Xor("+self.Ser(o.v)+")",
            QrySegTypes.AND : lambda o: "And("+self.Ser(o.v)+")",
            QrySegTypes.NAD : lambda o: "Nad("+self.Ser(o.v)+")",
            QrySegTypes.CSP : lambda o: "Csp("+self.Ser(o.v)+")",
            QrySegTypes.ITS : lambda o: "Its("+self.Ser(o.v)+")",
            QrySegTypes.DIF : lambda o: "Dif("+self.Ser(o.v)+")",
            QrySegTypes.UNI : lambda o: "Uni("+self.Ser(o.v)+")",
            QrySegTypes.CON : lambda o: "Con("+self.Ser(o.v)+")"
            }
        self.priTranslators = {
            #primitive types
            bool : lambda o: str(o),
            int : lambda o: str(o),
            float : lambda o: str(o),
            bool : lambda o: str(o),
            str : lambda o: "'"+o+"'",
            list : lambda o: "[%s]"%(",".join([self.Ser(x) for x in o])),
            type(None) : lambda o: str(o)
            }

    def Ser(self,val):
        try:
            return self.cmdTranslators[val.cmd](val)
        except:
            try:
                return self.qryTranslators[val.qry](val)
            except:
                try:
                    return self.priTranslators[type(val)](val)
                except:
                    raise EoqError(0,"Text serializer failed for %s"%(str(val)))

    def Des(self,code):
        pass