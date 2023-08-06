class EoqErrorTypes:
    SYN = 'SYN' #Syntax error
    SEM = 'SEM' #Semantic error
    CMD = 'CMD' #Command error
    QRY = 'QRY' #Query error
    IDX = 'IDX' #Index error, e.g. index does not exist
    TYP = 'TYP' #Type error, e.g. type mismatch
    ACC = 'ACC' #Access error, access denied
    VAL = 'VAL' #Validation error
    CER = 'CER' #Call error
    CAB = 'CAL' #Aborted
    
    
# BASIC ERROR CLASS
class EoqError(Exception):
    def __init__(self,info,msg,trace=""):
        self.info = info
        self.msg = msg
        self.trace = trace
        
    def __str__(self):
        return str(self.info)+"::"+self.msg+(("::TRACE:"+self.trace) if self.trace else "")
    
    
# SPECIALIZED ERROR CLASS
class EoqSynError(EoqError):
    def __init__(self,msg,trace=""):
        super().__init__(EoqErrorTypes.SYN, msg, trace)
        
class EoqSemError(EoqError):
    def __init__(self,msg,trace=""):
        super().__init__(EoqErrorTypes.SEM, msg, trace)
        
class EoqCallError(EoqError):
    def __init__(self,msg,trace=""):
        super().__init__(EoqErrorTypes.CER, msg, trace)
        
class EoqCallAborted(EoqError):
    def __init__(self,msg,trace=""):
        super().__init__(EoqErrorTypes.CAB, msg, trace)
