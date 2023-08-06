'''
 Bjoern Annighoefer 2019
'''

#Abstract definition of a domain
class Mdb:     
    def Root(self):
        pass
    
    def Metamodels(self):
        pass
    
    def AddMetamodel(self,name,metamodel):
        pass
        
    def RemoveMetamodel(self,name,metamodel):
        pass
        
    def GetMetamodel(self,name):
        pass
    
    def ResolveProxy(self,proxy):
        pass
    
    def Close(self):
        pass
    
    