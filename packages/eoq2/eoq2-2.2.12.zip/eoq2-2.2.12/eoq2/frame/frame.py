'''
 An EOQ protocol communication frame
 Bjoern Annighoefer 2019
 '''

class FrameTypes:
        CMD = "CMD" #Command
        RES = "RES" #Result
        CHG = "CHG" #Change
        EVT = "EVT" #Event: Change, call output
        ERR = "ERR" #Error
        
class Frame:
    def __init__(self,ftype,uid,data,version=210):
        self.eoq = ftype
        self.ver = version
        self.uid = uid
        self.dat = data
        
        