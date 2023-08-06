#class Segtypes(Enum):
# Context free operations
from ..util.error import EoqSynError

# TODO implement CNS operator
# TODO implement RGX operator

class QrySegTypes:
    OBJ = 'OBJ' #object reference
    HIS = 'HIS' #history reference
    
    # Left only element-wise operations
    PTH = 'PTH' # path
    CLS = 'CLS' # class
    INO = 'INO' # instance of
    MET = 'MET' # meta
    NOT = 'NOT' # boolean not
    TRM = 'TRM' # terminate
    CNS = 'CNS' # constraint
    TRY = 'TRY' #try catch

    # Left only list-of-elements-wise operations
    IDX = 'IDX' # index
    SEL = 'SEL' # selector
    ARR = 'ARR' # outer array
    ZIP = 'ZIP' # inner array creation
    QRY = 'QRY' # cmd
    
    ANY = 'ANY' # at least one element from the right is found in the left --> Bool
    ALL = 'ALL' # all elements from the right are found in the left --> Bool
    
    # Left-vs-right element-wise operators
    EQU = 'EQU' # equal
    EQA = 'EQA' # equal any of the right elements
    NEQ = 'NEQ' # not equal
    LES = 'LES' # less
    GRE = 'GRE' # greater
    RGX = 'RGX' # regex (string only)
    
    ##generic operators
    ADD = 'ADD' # OR, addition,
    SUB = 'SUB' # XOR, subtraction,
    MUL = 'MUL' # AND, multiply,
    DIV = 'DIV' # NAND, divided,
    
    ##logic operator synonyms
    ORR = 'ORR' # OR synonym
    XOR = 'XOR' # XOR synonym
    AND = 'AND' # AND synonym
    NAD = 'NAD' # NAND synonym
    
    #Left-vs-right list-of-element-wise operators
    CSP = 'CSP' # cross product
    ITS = 'ITS' # intersection
    DIF = 'DIF' # set subtraction / relative complement
    UNI = 'UNI' # union
    CON = 'CON' # concut

#define a list of symbols for the textual representation
QRY_SYMBOLS = {
    'OBJ' : '#', 
    'HIS' : '$', 
    'PTH' : '/', 
    'CLS' : '!', 
    'INO' : '?',
    'MET' : '@',
    'NOT' : '&NOT',
    'TRM' : '&TRM',
    'CNS' : '&CNS',
    'TRY' : '&TRY',

    'IDX' : ':', 
    'SEL' : '{', 
    'ARR' : '[', 
    'ZIP' : '&ZIP',
    'QRY' : '(', 
    'ANY' : '&ANY',
    'ALL' : '&ALL', 
    'EQU' : '=',
    'EQA' : '&EQA',
    'NEQ' : '~', 
    'LES' : '<', 
    'GRE' : '>',
    'RGX' : '&RGX',
    'ADD' : '&ADD', 
    'SUB' : '&SUB', 
    'MUL' : '&MUL', 
    'DIV' : '&DIV', 
    'ORR' : '&ORR', 
    'XOR' : '&XOR', 
    'AND' : '&AND', 
    'NAD' : '&NAD', 
    'CSP' : '&CSP', 
    'ITS' : '^', 
    'DIF' : '\\',
    'UNI' : '_', 
    'CON' : '|'
}  
#free symbols: *`�;
#reserved symbols: {}()[]'"+-.,
        

# META OPERATORS 
# Use only three letters for meta operators

#element operators
class QryMetaSegTypes:
    CLS = 'CLASS' #class
    CLN = 'CLASSNAME' #class name
    CON = 'CONTAINER' #parent (container)
    PAR = 'PARENT' #parent (container)
    ALP = 'ALLPARENTS' #parent (container)
    ASO = 'ASSOCIATES' #ASSOCIATES(start=root) all elements refering to this one beginning at start. default is root
    IDX = 'INDEX' #index within its containment
    CFT = 'CONTAININGFEATURE' #the feature that contains the element
    FEA = 'FEATURES' #all features
    FEV = 'FEATUREVALUES' #all feature values
    FEN = 'FEATURENAMES' #all feature names
    ATT = 'ATTRIBUTES' #all attribute features
    ATN = 'ATTRIBUTENAMES' #all attribute feature names
    ATV = 'ATTRIBUTEVALUES' #all attribute feature values
    REF = 'REFERENCES' #all reference features
    REN = 'REFERENCENAMES' #all reference feature names
    REV = 'REFERENCEVALUES' #all reference feature values
    CNT = 'CONTAINMENTS' #all containment features
    CNV = 'CONTAINMENTVALUES' #all containment feature values
    CNN = 'CONTAINMENTNAMES' #all containment feature names
    
    #class operators
    PAC = 'PACKAGE' #class
    STY = 'SUPERTYPES' #directly inherited classes
    ALS = 'ALLSUPERTYPES' #all and also indirectly inherited classes
    IMP = 'IMPLEMENTERS' #all direct implementers of a class
    ALI = 'ALLIMPLEMENTERS' #all and also indirect implementers of a class  
    MMO = 'METAMODELS' #retrieve all metamodels
    
    #Control flow operators 
    IFF = 'IF' #if(condition,then,else);  #DEPRICATED
    TRY = 'TRY' #catch errors and return a default #NOT IMPLEMENTED
    
    
    #list operators
    LEN = 'SIZE' #size of a list #DEPRICATED
    
    #recursive operators
    REC = 'REPEAT' #REPEAT(<query>,depth) repeat a given query until no more results are found #NOT IMPLEMENTED
    
    
    
class QryIdxTypes:
    #structure operators
    FLT = 'FLATTEN' #flatten any sub list structure to a list #NOT IMPLEMENTED
    LEN = 'SIZE' #size of a list
    ASC = 'SORTASC' #sort ascending #NOT IMPLEMENTED
    DSC = 'SORTDSC' #sort descending #NOT IMPLEMENTED

        
class Seg:
    def __init__(self,stype,args):
        self.qry = stype
        self.v = args
        
    def __repr__(self):
        return QRY_SYMBOLS[self.qry]+str(self.v)
        
    def __eq__(self, other):
        if(isinstance(other, Seg)):
            return self.qry == other.qry and self.v == other.v
        else: 
            return False #can not be equal if it is a different type
        
class PthSeg(Seg):
    def __init__(self,name):
        super().__init__(QrySegTypes.PTH,name)
        
class SelSeg(Seg):
    def __init__(self,query):
        super().__init__(QrySegTypes.SEL,query)
        
    def __repr__(self):
        return '{'+str(self.v)+'}'
    
class ArrSeg(Seg):
    def __init__(self,query):
        super().__init__(QrySegTypes.ARR,query)
        
    def __repr__(self):
        return '['+str(self.v)+']'
    
class ObjSeg(Seg):
    def __init__(self,obj):
        super().__init__(QrySegTypes.OBJ,obj)
        
    def __lt__(self, other):
        return self.v < other.v
        
class Qry(Seg): #Essential object cmd 
    def __init__(self,root=None):
        if(None==root):
            super().__init__(QrySegTypes.QRY, []) #add the root to the list if it is given, otherwise add an empty list
        elif(isinstance(root,Seg)):
            super().__init__(QrySegTypes.QRY, [root])
        else:
            raise EoqSynError('If root is given it must be a query segment itself. No primitives or lists are allowed. Use Arr() to pack a list of elements.')
    def __repr__(self):
        queryStr = ''
        for seg in self.v:
            queryStr += str(seg)
        return '('+queryStr+')'
    
    def _(self,seg): #adds an existing segment
        self.v.append(seg)
    
    def Obj(self,v):
        self.v.append(ObjSeg(v))
        return self
    
    def His(self,v):
        self.v.append(Seg(QrySegTypes.HIS,v))
        return self
        
    def Pth(self,name):
        self.v.append(PthSeg(name))
        return self
    
    def Cls(self,clazz):
        self.v.append(Seg(QrySegTypes.CLS,clazz))
        return self
    
    def Ino(self,clazz):
        self.v.append(Seg(QrySegTypes.INO,clazz))
        return self
    
    def Met(self,name,args=[]):
        self.v.append(Seg(QrySegTypes.MET,[name]+args))
        return self
    
    def Not(self):
        self.v.append(Seg(QrySegTypes.NOT,None))
        return self
    
    def Trm(self,cond=None,default=None):
        self.v.append(Seg(QrySegTypes.TRM,[cond,default]))
        return self
        
    def Cns(self):
        self.v.append(Seg(QrySegTypes.CNS,None))
        return self
    
    def Try(self,query,default=None):
        self.v.append(Seg(QrySegTypes.TRY,[query,default]))
        return self
    
    def Idx(self,n):
        self.v.append(Seg(QrySegTypes.IDX,n))
        return self
    
    def Sel(self,query):
        self.v.append(SelSeg(query))
        return self
    
    def Arr(self,elements):
        self.v.append(ArrSeg(elements))
        return self

    def Zip(self,elements):
        self.v.append(Seg(QrySegTypes.ZIP,elements))
        return self
    
    def Any(self,query):
        self.v.append(Seg(QrySegTypes.ANY,query))
        return self
    
    def All(self,query):
        self.v.append(Seg(QrySegTypes.ALL,query))
        return self
    
    def Equ(self,query):
        self.v.append(Seg(QrySegTypes.EQU,query))
        return self
    
    def Eqa(self,query):
        self.v.append(Seg(QrySegTypes.EQA,query))
        return self
    
    def Neq(self,query):
        self.v.append(Seg(QrySegTypes.NEQ,query))
        return self
    
    def Les(self,query):
        self.v.append(Seg(QrySegTypes.LES,query))
        return self
    
    def Gre(self,query):
        self.v.append(Seg(QrySegTypes.GRE,query))
        return self
        
    def Rgx(self,query):
        self.v.append(Seg(QrySegTypes.RGX,query))
        return self
    
    def Rgx(self,query):
        self.v.append(Seg(QrySegTypes.RGX,query))
        return self
    
    def Add(self,query):
        self.v.append(Seg(QrySegTypes.ADD,query))
        return self
    
    def Sub(self,query):
        self.v.append(Seg(QrySegTypes.SUB,query))
        return self
    
    def Mul(self,query):
        self.v.append(Seg(QrySegTypes.MUL,query))
        return self
    
    def Div(self,query):
        self.v.append(Seg(QrySegTypes.DIV,query))
        return self
    
    def Orr(self,query):
        self.v.append(Seg(QrySegTypes.ORR,query))
        return self
    
    def Xor(self,query):
        self.v.append(Seg(QrySegTypes.XOR,query))
        return self
    
    def And(self,query):
        self.v.append(Seg(QrySegTypes.AND,query))
        return self
    
    def Nad(self,query):
        self.v.append(Seg(QrySegTypes.NAD,query))
        return self
    
    def Csp(self,query):
        self.v.append(Seg(QrySegTypes.CSP,query))
        return self
    
    def Its(self,query):
        self.v.append(Seg(QrySegTypes.ITS,query))
        return self
    
    def Dif(self,query):
        self.v.append(Seg(QrySegTypes.DIF,query))
        return self
    
    def Uni(self,query):
        self.v.append(Seg(QrySegTypes.UNI,query))
        return self
    
    def Con(self,query):
        self.v.append(Seg(QrySegTypes.CON,query))
        return self
    
''' Shortcuts to start queries '''
    
class Obj(Qry):
    def __init__(self,v):
        super().__init__()
        self.Obj(v)
        
class His(Qry):
    def __init__(self,v):
        super().__init__()
        self.His(v)

class Pth(Qry):
    def __init__(self,name):
        super().__init__()
        self.Pth(name)
    
class Cls(Qry):
    def __init__(self,clazz):
        super().__init__()
        self.Cls(clazz)
        
class Ino(Qry):
    def __init__(self,clazz):
        super().__init__()
        self.Ino(clazz)
        
class Try(Qry):
    def __init__(self,query,default):
        super().__init__()
        self.Try(query,default)
        
class Met(Qry):
    def __init__(self,name,args=[]):
        super().__init__()
        self.Met(name,args)
        
class Not(Qry):
    def __init__(self):
        super().__init__()
        self.Not()
        
class Cns(Qry):
    def __init__(self):
        super().__init__()
        self.Cns()
        
class Idx(Qry):
    def __init__(self,n):
        super().__init__()
        self.Idx(n)
        
class Sel(Qry):
    def __init__(self,query):
        super().__init__()
        self.Sel(query)
        
class Arr(Qry):
    def __init__(self,elements):
        super().__init__()
        self.Arr(elements)       
    
class Zip(Qry):
    def __init__(self,elements):
        super().__init__()
        self.Zip(elements)   
        
class Any(Qry):
    def __init__(self,select):
        super().__init__()
        self.Any(select)
        
class All(Qry):
    def __init__(self,select):
        super().__init__()
        self.All(select)
        
class Equ(Qry):
    def __init__(self,query):
        super().__init__()
        self.Equ(query)
        
class Eqa(Qry):
    def __init__(self,query):
        super().__init__()
        self.Eqa(query)
        
class Neq(Qry):
    def __init__(self,query):
        super().__init__()
        self.Neq(query)
        
class Les(Qry):
    def __init__(self,query):
        super().__init__()
        self.Les(query)
        
class Gre(Qry):
    def __init__(self,query):
        super().__init__()
        self.Gre(query)
        
class Rgx(Qry):
    def __init__(self,query):
        super().__init__()
        self.Rgx(query)        

def QrySegFactory(qry,v):
    if(QrySegTypes.OBJ==qry):
        return ObjSeg(v)
    else:
        return Seg(qry,v)

        
        

        
        
