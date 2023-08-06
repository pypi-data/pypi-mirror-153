'''
 Bjoern Annighoefer 2019
'''

from ..event import EvtProvider

'''
 ACCESSORS
'''    

#Defintion of Accessor base class
class MdbAccessor(EvtProvider): 
    def Lock(self):
        pass
    
    def Release(self):
        pass
    
    ''' METAMODEL ACESSORS '''
   
    def GetAllMetamodels(self):
        pass
     
    def RegisterMetamodel(self,package):
        pass
    
    def UnregisterMetamodel(self,package):
        pass

    ''' MODEL ACESSORS '''
   
    def GetRoot(self):
        pass
    
    def Get(self,obj,feature):
        pass
    
    def Set(self,obj,feature,value):
        pass
    
    def GetParent(self,obj):
        pass
    
    def GetAllParents(self,obj):
        pass
    
    def GetAssociates(self,obj):
        pass
    
    def GetIndex(self,obj):
        pass
    
    def GetContainingFeature(self,obj):
        pass
        
    def Add(self,obj,feature,child):
        pass
        
    def Remove(self,obj,feature,child):
        pass
    
    def Move(self,obj,newIndex):
        pass

    def Clone(self,obj,mode):
        pass
    
    def Create(self,clazz,n,constructorArgs=[]):
        pass
    
    def CreateByName(self,packageName,className,n,constructorArgs=[]):
        pass
    
    def GetClassByName(self,packageName,className):
        pass
    
    def Class(self,obj):
        pass
    
    def ClassName(self,obj):
        pass
    
    ''' CLASS ACESSORS '''
   
    def Package(self,clazz):
        pass
    
    def Supertypes(self,clazz):
        pass
    
    def AllSupertypes(self,clazz):
        pass
    
    def Implementers(self,clazz):
        pass
    
    def AllImplementers(self,clazz):
        pass
    
    def GetAllChildrenOfType(self,obj,clazz):
        pass
    
    def GetAllChildrenInstanceOfClass(self,obj,clazz):
        pass
    
    def GetAllFeatures(self,obj):
        pass
    
    def GetAllFeatureNames(self,obj):
        pass
    
    def GetAllFeatureValues(self,obj):
        pass
    
    def GetAllAttributes(self,obj):
        pass
    
    def GetAllAttributeNames(self,obj):
        pass
    
    def GetAllAttributeValues(self,obj):
        pass
    
    def GetAllReferences(self,obj):
        pass
    
    def GetAllReferenceNames(self,obj):
        pass
    
    def GetAllReferenceValues(self,obj):
        pass
    
    def GetAllContainments(self,obj):
        pass
    
    def GetAllContainmentNames(self,obj):
        pass
    
    def GetAllContainmentValues(self,obj):
        pass
    
    
    

    
