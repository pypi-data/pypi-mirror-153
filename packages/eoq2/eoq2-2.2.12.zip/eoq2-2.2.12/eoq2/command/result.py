'''
 Command result
 
'''
from ..util.error import EoqError
from .command import CmdTypes

class ResTypes:
    OKY = 'OKY'
    ERR = 'ERR'

class Res:
    def __init__(self,commandType,status,value,transactionId=0,changeId=0):
        self.res = commandType #correspondes to the command that this result comes from
        self.s = status #status
        self.v = value #result of the executed command (error text in case of error, subresult array in case of a compound command)
        self.n = transactionId
        self.c = changeId
        
    def GetValue(self):
        return ResGetValue(self)
    
    
def ResGetValue(res):
    val = None
    if(ResTypes.ERR==res.s):
        raise EoqError(0,res.v)
    if(CmdTypes.CMP==res.res):
        val = [sr.v for sr in res.v]
    else: 
        val = res.v
    return val