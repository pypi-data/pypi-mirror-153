'''
 2019 Bjoern Annighoefer
'''

'''
 CALL HANDLER
'''
    
class CallHandler:
    def __init__(self):
        pass
    
    def CanHandle(self,name,args,ctype):
        pass
        
    def HandleSync(self,name,callId,domain,args,opts,callManager):
        pass
    
    def HandleAsync(self,name,callId,domain,args,opts,callManager,sessionId=None):
        pass
    
    def InputToCall(self,callId,channelName,data):
        pass
    
    def AbortCall(self,callId):
        pass
    
    
class FunctionWrapperCallHandler(CallHandler):
    def __init__(self,fct):
        self.fct = fct
        
    def HandleSync(self,name,callId,domain,args,opts,callManager,sessionId=None):
        return self.fct(domain,*args)