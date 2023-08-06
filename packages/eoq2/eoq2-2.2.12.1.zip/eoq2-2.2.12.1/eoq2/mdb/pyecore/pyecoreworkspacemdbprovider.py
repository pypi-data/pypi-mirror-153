"""
 Workspace MDB Provider
 Bjoern Annighoefer 2019
"""
# todo: catch permission errors when renaming a folder in which is a file opened or the folder is open in the explorer!!!
# todo: the web surface does not recognize when to folders are named the same name -> on explorer side it is recognized
# todo: better printout when something happens -> make paths better readable etc
# todo: the funktionszuweisung part of the event handler should be reworked to get it nicer to read
# todo: there is a known issue that when a newly created file is deleted before it is loaded, it gets recreated again
#       after it has been deleted. Recreate issue: via Web surface create .oaam file and immediately delete it in the explorer

from ...util import NoLogging
from ...event import MsgEvt,ChgTypes,EvtTypes
from .pyecoremdb import PyEcoreMdb

from .workspacemdbmodel import Workspace,ModelResource,Directory,FileResourceTypesE,PathElementA,FileResourceA,XmlResource
from .xmlresourcemodel import Document,Element,Attribute

from pyecore.resources import ResourceSet, URI
from pyecore.ecore import EPackage,EObject


from eoq2 import Cmp, Set, Add
import os
import platform
import shutil
import glob
import time
import xml.etree.ElementTree
import xml.dom.minidom
from pathlib import Path
from timeit import default_timer
from threading import Timer
import traceback

# try importing for watchdog functions
try:
    from watchdog.observers import Observer
    from watchdog.events import PatternMatchingEventHandler, FileSystemEvent, FileCreatedEvent
except ImportError:
    raise ImportError("Could not import Element from watchdog.\nPlease install the watchdog library.")


import pyecore.behavior as behavior  # We need to import the 'behavior' package

# Ugly global necessary for the path methods 
PROVIDER_INSTANCE = None


#Implement methods
@PathElementA.behavior
def actualPath(self):
    path = None
    if(PROVIDER_INSTANCE):
        path = PROVIDER_INSTANCE.GetElementPath(self)
    return path

@PathElementA.behavior
def actualPathAbs(self):
    path = None
    if(PROVIDER_INSTANCE):
        path = PROVIDER_INSTANCE.GetAbsElementPath(self)
    return path

@PathElementA.behavior
def actualPathCwd(self):
    path = None
    if(PROVIDER_INSTANCE):
        path = PROVIDER_INSTANCE.GetElementPath(self)
    return path

# intended for saving changes for later, but file system changes must be checked immediately in order to prevent unwanted situations
# class WorkspaceChgTypes:
#     RESOURCE_ADD = "RESOURCE_ADD"
#     RESOURCE_MOV = "RESOURCE_MOV"
#     RESOURCE_DEL = "RESOURCE_DEL"
#     DIRECTORY_ADD = "DIRECTORY_ADD"
#     DIRECTORY_MOV = "DIRECTORY_MOV"
#     DIRECTORY_DEL = "DIRECTORY_DEL"
        
        
class PyEcoreWorkspaceMdbProvider():
    def __init__(self,baseDir,metaDir=['./.meta'],saveTimeout=10.0,logger=NoLogging(),autoload=True,trackFileChanges=False):
        super().__init__()

        self.baseDir = os.path.normpath(baseDir)
        self.baseDirAbs = os.path.join(os.getcwd(),self.baseDir)
        self.baseDirUri = URI(self.baseDir) 
        self.rset = ResourceSet()
        self.modelResourceLut = {}  #a look-up table between eResources and ModelResource objects
        self.eResourceLut = {}  #a look-up table between ModelResource and eResources objects
        self.eResourcesConnected = False
        self.metaDir = metaDir  #the directory that contains model definitions
        
        self.logger = logger
        
        self.modelroot = Workspace(name='.')  #clone behavior of the old localdomain
        self.lastPersistentPaths = {}  # dir or resources -> path
        self.dirtyResources = []  #stores all modified resources, such that they can be saved
        self.deletedResources = {}  #stores all resources marked for deletion
        self.dirtyObjects = []  #stores all objects that have been modified in order to do not mark them twice
        self.saveTimeout = saveTimeout  #This time is waited for any model modifications and than autosafe is called
        self.saveTimer = None
        self.trackFileChanges = trackFileChanges
        
        self.knownModelExtensions = ['ecore']  #this is used to identify the model files to be loaded. ecore files are known as model files by default.
        self.knownXmlExtensions = ['xml']
        
        self.valueCodec = None  # is set during coupling
        self.domain = None  # is set during coupling
        self.mdb = None  # is created later

        self.exchangeChangeEventsList = []  # this list exchanges events between the eoq and the watchdog to prevent them to trigger each other it has the
                                            # structure that the event is given in a tuple: (string_to_identify_event_type, path_of_changed_element)

        self.modifiedEventSkipList = []
        self.__observer = None
        if(self.trackFileChanges):
            self.logger.Info("File change tracking enabled.")
            self.__observer = Observer()  # create observer for watchdog library
        
        if(autoload):
            self.Load()
            
        #register this as an singelton
        global PROVIDER_INSTANCE
        PROVIDER_INSTANCE = self
        
        
    def Close(self):
        #make sure any changes are saved
        #self.logger.Info("Closing workspace MDB ...") #makes problems when main thread has ended already

        self.__StopDelayedSaving()
        self.__SaveAllDirtyResources()

        #todo: there is a problem with the del which has to be investigated
        if(self.trackFileChanges):
            self.__observer.stop()
            self.__observer.join(10)  # wait until the watchdog observing thread terminates or exceeded timeout
            
        self.logger.Info("ok")
        
    def GetMdb(self):
        return self.mdb
    
    def Load(self):
        self.logger.Info("Loading workspace MDB for %s (meta=%s)..."%(self.baseDir,self.metaDir))
        start = default_timer()
        self.__LoadMetaModels()
        self.__LoadResourceTree()
        end = default_timer()
        self.mdb = PyEcoreMdb(self.modelroot,self.rset.metamodel_registry,self)
        self.logger.Info("Workspace MDB ready after %f s"%(end-start))
    
    def CoupleWithDomain(self,domain,valueCodec):
        self.domain = domain
        self.valueCodec = valueCodec
        self.domain.Observe(self.OnChange,[EvtTypes.CHG])

        # create the observer to track changes made on the workspace
        if(self.trackFileChanges):
            my_event_handler = self.__CreateCustomEventHandlerForWatchdog()  # create custom event handler which is imported from separate file
            self.__observer.schedule(my_event_handler, self.baseDir, recursive=True)  # set up observer
            self.__observer.start()  # start watchdog to observe workspace
            self.logger.Info("Watchdog initialized and ready!")
        
    ''' sync model changes with workspace '''
        
    def OnChange(self,evts,src):
        for evt in evts:

            chg = evt
            ctype = chg.a[1]
            target = self.valueCodec.Dec(chg.a[2]) #reverse what the domain did to the element
            feature = chg.a[3]
            oldOwner = self.valueCodec.Dec(chg.a[6])
            
            if(isinstance(target,FileResourceA)):
                if(ctype==ChgTypes.SET and "name"==feature):
                    # get name and check whether the renaming of the resource was made by the watchdog
                    newName = chg.a[4]
                    # check if actual path is not none so the renaming of a newly created object by creation in the ecoreeditor which
                    # obviously has no actual path throws no error
                    if target.actualPath() is not None and self.__IsEventInEventsExchangeList(Path(self.baseDir,target.actualPathAbs()),"rename"):
                        self.__RemoveEventFromEventsExchangeList(Path(self.baseDir,target.actualPath()),newName)
                        self.logger.Info(f"Renaming Resource to '{newName}' made by the Watchdog recognized!")
                    else:
                        # rename action
                        self.__RenameResource(target,newName)
                else: #handle any other resource change like an object change
                    self.__SetObjectDirty(target)
                    self.__SetObjectDirty(oldOwner)
            elif(isinstance(target,Directory)):
                # directories might be renamed or deleted or new resources/subdirs added or deleted
                if(ctype==ChgTypes.SET and "name"==feature ):
                    # resource renamed
                    newName = chg.a[4]
                    # check whether the event caused by a change, the watchdog made on the eoq
                    # evaluate if the actual path of the target is not None to prevent an error when a newly created object, which is not added
                    # to the eoq, is renamed.
                    if target.actualPath() is not None and self.__IsEventInEventsExchangeList(Path(self.baseDir,target.actualPath()),"rename"):
                        self.__RemoveEventFromEventsExchangeList(Path(self.baseDir,target.actualPath()),"rename")
                        self.logger.Info(f"Renaming directory to '{newName}' made by the Watchdog recognized!")
                    else:
                        self.__RenameDirectory(target,newName)
                elif(ctype==ChgTypes.ADD and "resources"==feature):
                    # new resource
                    resource = self.valueCodec.Dec(chg.a[4])
                    # check if change was made by watchdog
                    if self.__IsEventInEventsExchangeList(Path(self.baseDir,target.actualPath(),resource.name),"create"):
                        self.__RemoveEventFromEventsExchangeList(Path(self.baseDir,target.actualPath(),resource.name),"create")
                        self.logger.Info(f"Creation of file '{resource.name}' made by the Watchdog recognized!")
                    else:
                        if(oldOwner):
                            self.__MoveResource(resource)
                        else:
                            # make entry in events exchange list so the watchdog knows that the change was made by the eoq
                            self.__AddEventToEventsExchangeList(Path(self.baseDir,target.actualPath(),resource.name),"create")
                            self.__AddResource(target,resource)
                elif(ctype==ChgTypes.REM and "resources"==feature):
                    # resource deleted
                    resource = self.valueCodec.Dec(chg.a[4])
                    # check if change was made by the watchdog
                    if self.__IsEventInEventsExchangeList(Path(self.baseDir,target.actualPath(),resource.name),"delete"):
                        self.__RemoveEventFromEventsExchangeList(Path(self.baseDir,target.actualPath(),resource.name),"delete")
                        self.logger.Info(f"Deletion of file '{resource.name}' made by the Watchdog recognized!")
                    else:
                        self.__DeleteResource(resource)
                elif(ctype==ChgTypes.ADD and "subdirectories"==feature):
                    # new directory
                    directory = self.valueCodec.Dec(chg.a[4])
                    if(oldOwner):
                        self.__MoveDirectory(directory)
                    else:
                        # check whether the event is because of a change from the watchdog
                        if self.__IsEventInEventsExchangeList(Path(self.baseDir,directory.actualPath()),"create"):
                            self.__RemoveEventFromEventsExchangeList(Path(self.baseDir,directory.actualPath()),"create")
                            self.logger.Info(f"Creation of directory '{directory.name}' made by the Watchdog recognized!")
                        else:
                            self.__AddDirectory(target,directory)
                elif(ctype==ChgTypes.REM and "subdirectories"==feature):
                    # directory deleted
                    directory = self.valueCodec.Dec(chg.a[4])
                    # get directory of deleted directory relative to the base dir and make it
                    # relative to the base dir with the naming convention of the eoq
                    absolutePathDeletedDir = self.__GetLastPersitentPath(directory)
                    # check if dir deletion is made by the watchdog
                    if self.__IsEventInEventsExchangeList(Path(absolutePathDeletedDir),"delete"):
                        self.__RemoveEventFromEventsExchangeList(Path(absolutePathDeletedDir),"delete")
                        self.logger.Info(f"Deletion of directory '{directory.name}' made by the Watchdog recognized!")
                    else:
                        self.__DeleteDirectory(directory)
            elif(isinstance(target,EObject)):
                self.__SetObjectDirty(target)
                self.__SetObjectDirty(oldOwner)
            elif(ctype==ChgTypes.ADC or ctype==ChgTypes.RMC):
                index = None
                for i in range(len(self.mdb.Root().eContents)):
                    if self.mdb.Root().eContents[i].name == 'cdb.constraintmodel':
                        index = i
                if not(index == None):
                    self.__SetObjectDirty(self.mdb.Root().eContents[index].eContents[0])
                
    ''' resource sync functions '''
       
    def __AddResource(self,dir,resource):
        if(dir): #otherwise there is no need to move the resource
            try:
                #move the file 
                newPath = self.GetAbsElementPath(resource)
                if(newPath): #if this is false, then the resource was added to a directory not attached to the workspace
                    #create placeholder file
                    open(newPath, 'w').close()
                    self.__SetLastPersistentPath(resource, newPath)
                    self.__SetResourceDirty(resource)
                    #update the pyecore URI
                    if(resource.type == FileResourceTypesE.MODEL):
                        eResource = self.rset.create_resource(newPath)
                        self.__LinkModelResourceAndEResource(resource,eResource)
                    #inform about action
                    newRelPath = os.path.relpath(newPath,self.baseDir)
                    self.logger.Info("Added resource %s."%(newRelPath))
            except Exception as e:
                self.logger.Error("Failed to add resource: %s"%(str(e)))
                traceback.print_exc()            
                   
    def __RenameResource(self,resource,newName):
        lastPersistentPath = self.__GetLastPersitentPath(resource)
        if(lastPersistentPath): #otherwise this is a new resource and needs no renaming
            oldPath = lastPersistentPath
            filePath, oldName = os.path.split(oldPath)
            if(newName!=oldName):
                try:
                    # create entry in the events exchange list to tell watchdog that the PyEoq created the file
                    self.__AddEventToEventsExchangeList(Path(filePath,newName), "rename")
                    # move the file
                    newPath = os.path.join(filePath,newName)
                    os.rename(oldPath,newPath) 
                    self.__RefreshResourceOrDirectoryPath(resource)
                    # inform about action
                    oldRelPath = os.path.relpath(oldPath,self.baseDir)
                    newRelPath = os.path.relpath(newPath,self.baseDir)
                    self.logger.Info("Renamed resource %s to %s."%(oldRelPath,newRelPath))
                except FileExistsError:
                    # remove entry from the exchange events list if the renaming could not be made
                    if self.__IsEventInEventsExchangeList(Path(filePath,newName), "rename"):
                        self.__RemoveEventFromEventsExchangeList(Path(filePath,newName), "rename")
                    self.logger.Error(f"Failed to rename resource '{oldName}' to '{newName}.\n"
                                      f"A file with this name already exists in '{filePath}'.")
                except Exception as e:
                    # remove entry from the exchange events list if the renaming could not be made
                    if self.__IsEventInEventsExchangeList(Path(filePath,newName), "rename"):
                        self.__RemoveEventFromEventsExchangeList(Path(filePath,newName), "rename")
                    self.logger.Error("Failed to rename resource: %s"%(str(e)))
                    traceback.print_exc()
                
    def __MoveResource(self,resource):
        lastPersistentPath = self.__GetLastPersitentPath(resource)
        if(lastPersistentPath): #otherwise there is no need to move the resource
            oldPath = lastPersistentPath
            newPath = self.GetAbsElementPath(resource)
            if(newPath!=oldPath):
                try:
                    #move the file 
                    os.rename(oldPath,newPath) 
                    self.__RefreshResourceOrDirectoryPath(resource)
                    #inform about action
                    oldRelPath = os.path.relpath(oldPath,self.baseDir)
                    newRelPath = os.path.relpath(newPath,self.baseDir)
                    self.logger.Info("Moved resource %s to %s."%(oldRelPath,newRelPath))
                except Exception as e:
                    self.logger.Error("Failed to moved resource: %s"%(str(e)))
                    traceback.print_exc()
                
    def __DeleteResource(self,resource):
        lastPersistentPath = self.__GetLastPersitentPath(resource)
        if(lastPersistentPath):
            try:
                # add deletion to eventsExchangeList
                self.__AddEventToEventsExchangeList(Path(lastPersistentPath),"delete")
                oldPath = lastPersistentPath
                #delete resource
                os.remove(oldPath)
                self.__DeleteResourceOrDirectoryPath(resource)
                #inform about action
                oldRelPath = os.path.relpath(oldPath,self.baseDir)
                self.logger.Info("Deleted resource %s."%(oldRelPath))
            except Exception as e:
                self.logger.Info("Failed to delete resource %s."%(str(e)))
                traceback.print_exc()
                
    ''' directory sync functions '''
    def __AddDirectory(self,parent,directory):
        if(parent): #otherwise there is no need to move the resource
            try:
                newPath = self.GetAbsElementPath(directory)
                if(newPath): #if this is false, then the dir was added to a directory not attached to the workspace
                    # create  in the events exchange list to tell watchdog that the PyEoq created the directory
                    self.__AddEventToEventsExchangeList(Path(newPath), "create")
                    #create new dir file
                    os.mkdir(newPath)
                    self.__SetLastPersistentPath(directory, newPath)
                    #recursively consider all contained resources and subdirs 
                    for res in directory.resources:
                        self.__AddResource(directory, res)
                    for subdir in directory.subdirectories:
                        self.__AddDirectory(directory, subdir)
                    # inform about action
                    newRelPath = os.path.relpath(newPath,self.baseDir)
                    self.logger.Info("Added directory %s."%(newRelPath))
            except Exception as e:
                # remove entry for add directory from events exchange list when it has been created and new path exists
                if (newPath):
                    self.__RemoveEventFromEventsExchangeList(Path(newPath), "create")
                self.logger.Error("Failed to add directory: %s"%(str(e)))
                traceback.print_exc() 
                
    
    def __RenameDirectory(self,directory,newName):
        lastPersistentPath = self.__GetLastPersitentPath(directory)
        if(lastPersistentPath): #otherwise this is a new resource and needs no renaming
            oldPath = lastPersistentPath
            filePath, oldName = os.path.split(oldPath)
            if(newName!=oldName):
                try:
                    newPath = os.path.join(filePath,newName)
                    # make entry into eventsExchangeList to inform watchdog about changes
                    self.__AddEventToEventsExchangeList(Path(newPath),'rename')
                    #create the new dir
                    os.rename(oldPath,newPath) 
                    self.__RefreshResourceOrDirectoryPath(directory)
                    #inform about action
                    oldRelPath = os.path.relpath(oldPath,self.baseDir)
                    newRelPath = os.path.relpath(newPath,self.baseDir)
                    self.logger.Info("Renamed directory %s to %s."%(oldRelPath,newRelPath))
                except Exception as e:
                    # remove entry from events exchange list because change has not been made
                    if self.__IsEventInEventsExchangeList(Path(newPath),'rename'):
                        self.__RemoveEventFromEventsExchangeList(Path(newPath),'rename')

                    self.logger.Error("Failed to rename directory: %s"%(str(e)))
                    traceback.print_exc() 
                    
    def __MoveDirectory(self,directory):
        lastPersistentPath = self.__GetLastPersitentPath(directory)
        if(lastPersistentPath): #otherwise there is no need to move the directory
            oldPath = lastPersistentPath
            newPath = self.GetAbsElementPath(directory)
            if(newPath!=oldPath):
                try:
                    #move the directory 
                    shutil.move(oldPath,newPath) 
                    self.__RefreshResourceOrDirectoryPath(directory)
                    #inform about action
                    oldRelPath = os.path.relpath(oldPath,self.baseDir)
                    newRelPath = os.path.relpath(newPath,self.baseDir)
                    self.logger.Info("Moved directory %s to %s."%(oldRelPath,newRelPath))
                except Exception as e:
                    self.logger.Error("Failed to move directory: %s"%(str(e)))
                    traceback.print_exc()
                
    def __DeleteDirectory(self,directory):
        lastPersistentPath = self.__GetLastPersitentPath(directory)
        if(lastPersistentPath):
            try:
                # add entry to events exchange list to show watchdog that change is made by eoq
                self.__AddEventToEventsExchangeList(Path(self.__GetLastPersitentPath(directory)), "delete")
                oldPath = lastPersistentPath
                #delete resource
                shutil.rmtree(oldPath)
                self.__DeleteResourceOrDirectoryPath(directory)
                #inform about action
                oldRelPath = os.path.relpath(oldPath,self.baseDir)
                self.logger.Info("Deleted directory %s."%(oldRelPath))
            except Exception as e:
                self.logger.Info("Failed to delete directory %s."%(str(e)))
                traceback.print_exc()
                
    ''' Generic path functions '''
                
    def __RefreshResourceOrDirectoryPath(self,element):
        newPath = self.GetAbsElementPath(element)
        if(newPath):
            self.__SetLastPersistentPath(element, newPath)
            if(isinstance(element, ModelResource)):  
                #update the pyecore URI
                newUri = URI(newPath)
                eResource = self.__GetEResourceForModelResource(element)
                eResource.uri = newUri
            elif(isinstance(element, Directory)):
                #update contained elements
                for subres in element.resources:
                    self.__RefreshResourceOrDirectoryPath(subres)
                for subdir in element.subdirectories:
                    self.__RefreshResourceOrDirectoryPath(subdir)
                    
    def __DeleteResourceOrDirectoryPath(self,element):
        self.__DeleteLastPeristentPath(element)
        if(isinstance(element, FileResourceA)):  
            self.__SetResourceClean(element)
            if(element.type == FileResourceTypesE.MODEL):
                self.__UnlinkModelResourceAndEResource(element)
        elif(isinstance(element, Directory)):
            #update contained elements
            for subres in element.resources:
                self.__DeleteResourceOrDirectoryPath(subres)
            for subdir in element.subdirectories:
                self.__DeleteResourceOrDirectoryPath(subdir)
                
    def GetElementPath(self,directory):
        workspaceFound = False #indicates if the element is attached correctly somewhere below the root
        path = directory.name
        if(isinstance(directory,Workspace)):
            return path
        parent = directory.eContainer()
        while(isinstance(parent,Directory)):
            path = os.path.join(parent.name,path)
            if(isinstance(parent,Workspace)):
                workspaceFound = True
                break #exit because there should not be an element further down.
            parent = parent.eContainer()
        if(workspaceFound):
            return path
        else:
            return None
    
    def GetAbsElementPath(self,directory):
        path = self.GetElementPath(directory)
        if(path):
            path = path[2:]
            return os.path.join(self.baseDirAbs,path)
        else:
            return None
     
    def __SetObjectDirty(self,obj):
        if(obj): 
            #find the resource object and mark it dirty
            if(obj in self.dirtyObjects):
                return  # quit here if object is already marked as dirty.
            self.dirtyObjects.append(obj)
            resource = self.__GetResourceForObject(obj)
            self.__SetResourceDirty(resource)
       
    ''' Last persistent path functions '''     
    def __GetLastPersitentPath(self,dirOrResource):
        lastPersistentPath = None
        try:
            lastPersistentPath = self.lastPersistentPaths[dirOrResource]
        except KeyError:
            lastPersistentPath = None
        return lastPersistentPath
    
    def __SetLastPersistentPath(self,dirOrResource,lastPersistentPath):
        self.lastPersistentPaths[dirOrResource] = lastPersistentPath
        
    def __DeleteLastPeristentPath(self,dirOrResource):
        try:
            self.lastPersistentPaths.pop(dirOrResource)
        except:
            pass  # fail silent if element does not has no path so far
    
    ''' Saving functions '''
    def __InitSave(self):
        #stop the current save action 
        self.__StopDelayedSaving()
        if(0<len(self.dirtyResources)):
            if(self.saveTimeout > 0):
                self.__StartDelayedSaving()
            else:
                self.__SaveAllDirtyResources() #skip threading for a 0 timeout
        
    
    def __StartDelayedSaving(self):
        self.saveTimer = Timer(self.saveTimeout,self.__DelayedSaving)
        self.saveTimer.start()
        
    def __StopDelayedSaving(self):
        if(self.saveTimer):
            self.saveTimer.cancel()
            self.saveTimer = None
            
    def __DelayedSaving(self):
        self.__SaveAllDirtyResources()
        self.saveTimer = None
        
    def __SaveAllDirtyResources(self):
        #self.Lock()
        self.mdb.Lock()
        evts = []
        self.__ConnectAllEResources()  # necessary for model resources
        for resource in self.dirtyResources:
            try:
                # add entry to the modified event list to ensure the resource wont get reloaded
                self.AddFileEventToSkipList(FileSystemEvent(self.__GetLastPersitentPath(resource)),2)
                self.__SaveResource(resource)
                evts.append(MsgEvt("WorkspaceMdb","Saved %s."%(resource.name)))
            except Exception as e:
                evts.append(MsgEvt("WorkspaceMdb","Failed to save %s: %s"%(resource.name,str(e))))
                traceback.print_exc()
        self.__DisconnectAllEResources()  # necessary for model resources

        self.dirtyResources.clear()
        self.dirtyObjects.clear()
        
        #notify observers
        self.domain.NotifyObservers(evts, self)
        #self.Release()
        self.mdb.Release()
    
    ''' resource handling functions '''

    def __SetResourceDirty(self,resource):
        if(resource and resource not in self.dirtyResources):
            self.dirtyResources.append(resource)
            self.__InitSave()
            
    def __SetResourceClean(self,resource):
        try:
            self.dirtyResources.remove(resource)
        except:
            pass  # do nothing if the resource was never marked as dirty
 
    def __GetResourceForObject(self,obj):
        container = obj
        while container and not isinstance(container, FileResourceA):
            container = container.eContainer()
        return container
         
    def __LoadMetaModels(self):
        #look for existing meta models and load them on them
        for mp in self.metaDir:
            metadir = mp
            if(not os.path.isabs(mp)):
                metadir = os.path.join(self.baseDir,mp)
            searchString = os.path.join(metadir+'/*.ecore')
            modeldefinitions = glob.glob(searchString)
            for md in modeldefinitions:
                self.__LoadMetaModelResource(md)
        return


    def __LoadModelContents(self,resourceFile):
        resource = self.rset.get_resource(resourceFile)
        return list(resource.contents) #make a copy of the list contents


    def __LoadMetaModelResource(self,resourceFile):
        modelContents = self.__LoadModelContents(resourceFile)
        gcmRoot = modelContents[0]
        self.rset.metamodel_registry[gcmRoot.nsURI] = gcmRoot
        # register all possible subpackages
        for child in gcmRoot.eAllContents():
            if(isinstance(child,EPackage)):
                self.rset.metamodel_registry[child.nsURI] = child
        #remember the file extension, which is the file name (without extension) of the model file
        metaModelFileName = os.path.basename(resourceFile)
        modelExtension = os.path.splitext(metaModelFileName)[0]
        self.knownModelExtensions += [modelExtension]
        #return the root
        return modelContents
                        
            
    def __LoadResourceTree(self):
        (directories,modelfiles) = self.__ScanForFilesAndDirectories()

        #create directories (this includes empty ones)
        for dirpath in directories:
            directory = self.__GetOrCreateDir(dirpath)
        
        #create model files
        for modelfile in modelfiles:
            head,tail = os.path.split(modelfile)
            directory = self.__GetOrCreateDir(head)
            resource = self.__LoadResource(modelfile)
            if(resource): #check if loading succeeded
                resource.name = tail
                directory.resources.add(resource)
    
    
    def __GetOrCreateDir(self,path):
        relPath = os.path.relpath(path, self.baseDirAbs)
        directory = self.modelroot
        if(relPath and relPath != '.'): #only proceed for non empty strings
            segments = relPath.split(os.path.sep)
            for segment in segments: 
                subdirexists = False
                for subdir in directory.subdirectories:
                    if(subdir.name == segment):
                        directory = subdir
                        subdirexists = True
                        break
                if(not subdirexists):
                    newsubdir = Directory(name=segment)
                    self.__SetLastPersistentPath(newsubdir, path)
                    directory.subdirectories.add(newsubdir)
                    directory = newsubdir
        return directory


    def __ScanForFilesAndDirectories(self):
        directories = []
        modelFiles = []
        for root, dirs, files in os.walk(self.baseDirAbs, topdown=True):
            for d in dirs:
#                 relativeRoot = os.path.relpath(root, self.baseDir)
                path = os.path.join(root,d)
                directories.append(path)
            for f in files:
#                 for extension in self.knownModelExtensions:
#                     if(f.endswith('.%s'%(extension))):
#                         relativeRoot = os.path.relpath(root, self.baseDir)
                        path = os.path.join(root,f)
                        modelFiles.append(path)
        return (directories,modelFiles)
    
    def __LoadResource(self,path):
        resource = None
        try:
            extension = os.path.splitext(path)[1].replace('.','') #remove the point in the extension
            self.logger.Info("Loading %s ..."%(path))
            start = default_timer() 
            if(extension in self.knownModelExtensions):
                resource = self.__LoadModelResource(path)
            elif(extension in self.knownXmlExtensions):
                resource = self.__LoadXmlResource(path)
            #check if a handler was found
            if(resource):
                self.__SetLastPersistentPath(resource, path)
                end = default_timer()
                self.logger.Info("ok (%f s)"%(end-start))
            else:
                self.logger.Info("skipped: Unknown format.")
        except Exception as e:
            self.logger.Info("failed: %s"%(str(e)))
        return resource
      
    def __LoadModelResource(self,path):
        resource = ModelResource()
        eResource = self.rset.get_resource(path)
        for content in eResource.contents:
            resource.contents.add(content)
        #register the resource in the lookup table
        self.__LinkModelResourceAndEResource(resource,eResource)
        #re-add the contents to the resource object because the containment removes it
        #is not necessary any more since the content will be re-added when saved or resolving proxies
#         for content in resource.contents:
#             eResource.append(content)
        return resource
    
    def __LoadXmlResource(self,path):
        resource = XmlResource()
        #parse input-xml
        xmlparse = xml.etree.ElementTree
        tree = xmlparse.parse(path)
        root = tree.getroot()
        ldfile = Document(name=resource.name, version="1.0")
        rootelement = Element(name=root.tag, content=root.text.strip())
        resource.document = ldfile
        resource.document.rootelement = rootelement
        for attr in root.attrib:
            newAttr = Attribute(name=attr, value=root.attrib[attr])
            rootelement.attributes.add(newAttr)
        # find first layer
        for element in root:
            if(element.text == None):
                element.text = ""
            #find all subclasses within first layer
            self.__FindChildElements(element, rootelement)
        return resource           
    
    def __FindChildElements(self, element, parent):
        if(element.text == None):
            element.text = ""
        newChild = Element(name = element.tag, content = element.text.strip())
        parent.subelements.add(newChild)
        #create attribute class for each attribute
        for attr in element.attrib:
            newAttr = Attribute(name = attr, value = element.attrib[attr])
            newChild.attributes.add(newAttr)
        #find all child elements
        for child in element:
            self.__FindChildElements(child, newChild)
        return parent
              
    def __SaveResource(self,resource):
        actualPath = self.__GetLastPersitentPath(resource)
        if(actualPath):
            actualRelPath = os.path.relpath(actualPath, self.baseDirAbs)
            self.logger.Info("Saving %s ..."%(actualRelPath))
            start = default_timer()
            if(resource.type == FileResourceTypesE.MODEL): 
                eResource = self.__GetEResourceForModelResource(resource)
                eResource.save()
            elif(resource.type == FileResourceTypesE.XML):
                tree = self.__SaveXmlResource(resource)
                with open(actualPath, "w") as f:
                    #comment: replace is not necessary
                    f.write(tree.replace('<?xml version="1.0" ?>',
                                         '<?xml version="1.0" encoding="utf-8"?>'))  
            elif(resource.type == FileResourceTypesE.TEXT):
                pass
            elif(resource.type == FileResourceTypesE.RAW):
                pass
            #self.__SetLastPersistentPath(resource, actualPath)
            end = default_timer()
            self.logger.Info("ok (%f s)"%(end-start))
        else:
            self.logger.Info("Saving %s skipped,because it is not attached to the workspace."%(resource.name))
        
    def __SaveXmlResource(self, resource):
        ET = xml.etree.ElementTree
        parser = xml.dom.minidom
        #get root element
        rootElement = resource.document.rootelement
        rootTag = ET.Element(rootElement.name)
        rootTag.text = rootElement.content
        #get attributes
        for attrib in rootElement.attributes:
                rootTag.set(attrib.name, attrib.value)
        #find all elements in root
        self.__FindSubElements(ET, rootTag, rootElement)
        #create output string
        xmlstr = parser.parseString(ET.tostring(rootTag)).toprettyxml(indent = "   ")
        return xmlstr   

    def __FindSubElements(self,ET, parentTag, Element):
        for subelement in Element.subelements:
            #add to parent
            subTag = ET.SubElement(parentTag, subelement.name)
            subTag.text = subelement.content
            #get attributes
            for attrib in subelement.attributes:
                subTag.set(attrib.name, attrib.value)
            # find (sub)subelement
            self.__FindSubElements(ET, subTag, subelement)

        
    ''' Special methods for model resources '''
    
    
    def __LinkModelResourceAndEResource(self, modelResource, eResource):
        self.modelResourceLut[eResource] = modelResource
        self.eResourceLut[modelResource] = eResource
        
    def __UnlinkModelResourceAndEResource(self, modelResource):
        try:
            eResource = self.eResourceLut.pop(modelResource)
            self.modelResourceLut.pop(eResource)
        except Exception as e:
            self.logger.Warn("Unlink model resource and eResource failed: %s"%(str(e)))
            
    def __GetModelResourceForEResource(self, eResource):
        try:
            return self.modelResourceLut[eResource]
        except:
            return None
        
    def __GetEResourceForModelResource(self,modelResource):
        try:
            return self.eResourceLut[modelResource]
        except:
            return None
        
    def __ConnectAllEResources(self):
        if(not self.eResourcesConnected):
            #self.eResourceLock.acquire()
            for resourceUri in self.rset.resources:
                resource = self.rset.resources[resourceUri]
                modelResource = self.__GetModelResourceForEResource(resource)
                if(modelResource):
                    for content in resource.contents:
                        resource.remove(content)
                    for content in modelResource.contents:
                        resource.append(content)
                        #modelResource.contents.discard(content)
                    #HACK1: elements must be removed from the Resource in order to make save work
                    modelResource.contents.clear()
            self.eResourcesConnected = True
        
    def __DisconnectAllEResources(self):
        if(self.eResourcesConnected):
            #self.eResourceLock.release()
            for resourceUri in self.rset.resources:
                resource = self.rset.resources[resourceUri]
                modelResource = self.__GetModelResourceForEResource(resource)
                if(modelResource):
                    #HACK2: now read the content
                    for content in resource.contents:
                        modelResource.contents.add(content)
                    #HACK3: content must be re-added to the resource because eResource() wont work otherwise
                    #not needed any more
#                     for content in modelResource.contents:
#                         resource.append(content)
            self.eResourcesConnected = False

    def __CreateCustomEventHandlerForWatchdog(self):
        """Function to create a custom event handler for the watchdog used to track the workspace changes corresponding to .oaam files"""

        def OnCreated(event:FileSystemEvent, pathObject=None):
            # - use path object for the element paths as translator to also support non windows platforms
            #   this if also supports the recursively calling of the OnCreated function with an pathobject
            # - the case when elementPathObject is none is when a copy into the workspace happened and OnCreated event
            #   is thrown for a subfolder whose parent folder has not been created eg. treated in an event.
            #   So the onCreated function gets manually called for this parent folder to create it in advance

            self.logger.Debug('Watchdog: OnCreated')
            if event is None:
                elementPathObject = pathObject
            else:
                elementPathObject = Path(event.src_path)

            # check if the element is known and set element type for later use in the domain command
            elementTypeInEoq = self.__CheckForKnownFile(elementPathObject)
            if not elementTypeInEoq:
                # skip if the file ending is unknown
                return
            # check if element is dir and was already created because previous event of a creation of a child dir caused
            # the creation of this dir. In this case the function is not further needed and can be skipped
            elif elementPathObject.is_dir() and self.__GetHashId(elementPathObject) is not False and \
                    not self.__IsEventInEventsExchangeList(elementPathObject, "create"):
                self.logger.Info(f"Watchdog: Event for creation {str(elementPathObject.absolute())} recognized. Dir already exists. "
                                 f"Skipping event")
                return

            # check if creation was done by the eoq and log if the creation was made by the eoq
            elif self.__CheckAndRemoveFromEventsExchangeList(elementPathObject, "create"):
                return
            else:
                # add the change which has to be made to the change list so there is no interference with the eoq trying
                # to add this folder/file to the file system
                self.__AddEventToEventsExchangeList(elementPathObject, "create")

                # add the skip of the modified event if the event is caused by a file and dont add teh skip event if the
                # onodified function has been called by an other function than the watchdog and when the operating
                # system is mac os
                if elementPathObject.is_file() and event is not None and\
                        "Darwin" not in platform.platform(aliased=True, terse=True):
                    self.AddFileEventToSkipList(event,1)

            # get the parent dir hash ID so it is possible to add the newly created element to it
            parentDirPathObject = elementPathObject.parent
            parentDirHash = self.__GetHashId(parentDirPathObject)

            # if it is not possible to get the parentDirHash, recursively call the OnCreated function
            # (when a onCreated event was thrown for an ).
            # This prevents an  error, when an OnCreation event is thrown for a child dir but the event
            # for its parent dir has not been thrown or worked on, by creating the parent folder in the Eoq in advance.
            if parentDirHash is False:
                self.logger.Info(f"Watchdog: Parent dir '{str(parentDirPathObject.name)}' of '{str(elementPathObject.absolute())}'"
                                 f" does not exist in the Eoq. Recursively calling function OnCreated of the watchdog "
                                 f"to create the parent dir in the Eoq.")
                OnCreated(None,parentDirPathObject)

                # get the parent Dir Hash again
                parentDirHash = self.__GetHashId(parentDirPathObject)

            metaDirAbsPath = self.__GetMetaDirAbsPath()

            # perform changes on the Eoq
            if elementPathObject.is_dir():
                self.__LoadDirFromFileSystem(elementPathObject, parentDirHash)
            # when ecore files are added new files can be added to the eoq, this will be done here
            elif elementPathObject.suffix == ".ecore" and str(parentDirPathObject.absolute()) in metaDirAbsPath:
                # remove entry from list to prevent the exchangeChangeEvents-list to fill up with artifacts or any
                # confusion when the eoq tries to read out an entry out of this list
                self.__LoadMetaModelFromFileSystem(elementPathObject, parentDirPathObject)
            else:
                self.__LoadResourceFromFileSystem(elementPathObject, parentDirPathObject)


        def OnMoved(event:FileSystemEvent):
            self.logger.Debug('Watchdog: OnMoved')
            # get some general information about the object involved in the process
            oldPathToObjectPathElement = Path(event.src_path)
            newPathToObjectPathElement = Path(event.dest_path)
            newNameOfObject = newPathToObjectPathElement.name
            oldNameOfObject = oldPathToObjectPathElement.name
            srcParentDirPathObject = oldPathToObjectPathElement.parent
            destParentDirPathObject = newPathToObjectPathElement.parent

            # this prevents an infinity loop when an revoke of a illegal file suffix renaming made in the explorer
            # was reverted by the watchdog
            if self.__IsEventInEventsExchangeList(newPathToObjectPathElement, 'watchdog_rename'):
                self.__RemoveEventFromEventsExchangeList(newPathToObjectPathElement, 'watchdog_rename')
                self.logger.Info('Watchdog: ok')
                return

            elementTypeInEoq = self.__CheckForKnownFile(oldPathToObjectPathElement)
            if not elementTypeInEoq:
                # check if the file was renamed to a known file suffix and revert the changes
                if newPathToObjectPathElement.suffix[1:] in self.knownXmlExtensions+self.knownModelExtensions:
                    self.logger.Info(f"Watchdog: File {str(oldPathToObjectPathElement.absolute())} was renamed to a file extension, known in"
                                     f" the eoq. Revoking changes...")
                    try:
                        # log changes so the watchdog does not reverte thoose since from his side of view a .oaam file gets illegaly renamed
                        self.__AddEventToEventsExchangeList(oldPathToObjectPathElement, 'watchdog_rename')
                        os.rename(str(newPathToObjectPathElement.absolute()), str(oldPathToObjectPathElement.absolute()))
                    except Exception as e:
                        self.logger.Info("Watchdog: Failed to undo illegal renaming of file %s in the eoq %s."%(str(oldPathToObjectPathElement.absolute()), str(e)))
                        traceback.print_exc()

                    return

                # only add this when the os is windows since there are no onmodified events thrown for this on mac
                if "Darwin" not in platform.platform(aliased=True, terse=True):
                    self.AddFileEventToSkipList(FileSystemEvent(event.dest_path),2)
                return


            ## catch case in which the element is just renamed
            if srcParentDirPathObject.absolute() == destParentDirPathObject.absolute():

                # catch case when a illegal renaming of a file extension happened
                # used != instead of 'is not' because equality and not identity is checked
                if newPathToObjectPathElement.suffix != oldPathToObjectPathElement.suffix:

                    # check whether the changes have been made by the ecoreEditor and delete the event from the event exchange queue
                    # also suffix changes in the eoq are not allowed
                    if self.__CheckAndRemoveFromEventsExchangeList(newPathToObjectPathElement, 'rename'):

                        # add the change which is to be made to the change list so there is no interference with the eoq
                        self.__AddEventToEventsExchangeList(oldPathToObjectPathElement, 'rename')

                        # perform changes
                        self.__RenameResourceOrDir(newPathToObjectPathElement, oldNameOfObject)

                    # add entry to Events exchange list so watchdog does not track the changes itself made
                    self.__AddEventToEventsExchangeList(oldPathToObjectPathElement, 'watchdog_rename')

                    self.logger.Info(f"Watchdog: Illegal renaming of file '{str(oldPathToObjectPathElement.absolute())}' detected. Revoking....")

                    # only add to skip eent list if system is windows
                    if "Darwin" not in platform.platform(aliased=True, terse=True):
                        self.AddFileEventToSkipList(event,1)

                    # undo changes in the explorer
                    os.rename(str(newPathToObjectPathElement),str(oldPathToObjectPathElement))
                    return

                # .ecore is no resource and a renaming should not be done so this is prevented here and changes are reverted
                if oldPathToObjectPathElement.suffix == '.ecore':
                    self.logger.Info(f"Watchdog: Illegal renaming of {str(oldPathToObjectPathElement.absolute())} file detected. Revoking....")
                    # prevent watchdog from reverting changes
                    self.__AddEventToEventsExchangeList(oldPathToObjectPathElement, 'watchdog_rename')
                    os.rename(newPathToObjectPathElement,oldPathToObjectPathElement)
                    return

                # check whether changes have been made by the eoq and return if that is the case
                if self.__CheckAndRemoveFromEventsExchangeList(newPathToObjectPathElement, 'rename'):
                    return

                # make entry in the modifiedqueue to prevent onmodified events to appear for this event, this is done with a synthetic event
                # with the dest_path which is only checked for, if a skip of the onModified event is checked
                # only add to skip list if the os is not mac os
                if not event.is_directory and "Darwin" not in platform.platform(aliased=True, terse=True):
                    self.AddFileEventToSkipList(FileSystemEvent(event.dest_path), 1)

                # add the change which is to be made to the change list so there is no interference with the eoq trying
                # to add this folder to the domain
                self.__AddEventToEventsExchangeList(newPathToObjectPathElement, "rename")
                self.__RenameResourceOrDir(oldPathToObjectPathElement, newNameOfObject)
                return

            # on Windows Platforms the moving of a folder is tracked by the Watchdog with a combination of delete and
            # create events. The only time a OnMoved event is thrown is when a folder or its parent folder is renamed.
            # Renaming its parent folder needs no extra action on the folder itself and this gets caught in here.
            # On OSX there is no combination of delete and create but instead a move event when a folder/file is moved.
            if "Darwin" not in platform.platform(aliased=True, terse=True) and event.is_directory:
                self.logger.Info(f"Watchdog: Moving of '{oldNameOfObject}' from '{str(srcParentDirPathObject)}' to "
                                 f"'{str(destParentDirPathObject)}' detected. No action needed since the moving of one of"
                                 f" its parent folders triggered this event.")
                return

        ## catch case in which the file/folder is moved to another folder, only on mac/linux available s. comment above
            # this catches the case when the Folder/file is moved to an other folder
            elif (newPathToObjectPathElement.exists() and oldPathToObjectPathElement.exists())\
                    or self.__ParentWasMoved(oldPathToObjectPathElement,newPathToObjectPathElement):
                #todo: check if the movement has been made by the eoq is not included. Needs implementation when moving
                #      in the eoq is possible

                # make movement to a create delete sequence to fit mac behavior of watchdog to windows eg make
                # logfiles look the same
                OnDeleted(None, oldPathToObjectPathElement)
                OnCreated(None, newPathToObjectPathElement)

            # catch case when multiply folders are copied
            else:
                elementHash = self.__GetHashId(oldPathToObjectPathElement)
                resource = self.valueCodec.Dec(elementHash)
                self.__SetLastPersistentPath(resource, str(newPathToObjectPathElement.absolute()))
                self.logger.Info(f"Watchdog: Parent folder of {newNameOfObject} renamed. No action needed")

        def OnDeleted(event:FileSystemEvent, pathObject=None):
            self.logger.Debug('Watchdog: OnDeleted')
            # This event behaves different on OSX and Windows when a parent folder is deleted: on windows there is just
            # an event for the deletion of the parent folder. On OSX there is an event for every deleted subfolder in the
            # parent folder. This is caught with an existence check on the parent folder later in this function.

            # make function reusable with a path object
            if event is None:
                elementPathObject = pathObject
            else:
                elementPathObject = Path(event.src_path)

            elementTypeInEoq = self.__CheckForKnownFile(elementPathObject)
            if not elementTypeInEoq:
                return

            # on mac os the modification of an event via an editor is achieved via a create and delete sequence.
            # therefore this sequence will be detected here and treated as an onModified event and the onCreated
            # event will be deleted
            # this sequence should only be searched on files and events which where thrown by the eoq
            if "Darwin" in platform.platform(aliased=True, terse=True) and not elementPathObject.is_dir()\
                    and not event is None:
                evt = self.__observer.event_queue.queue[0]
                if evt[0].src_path == event.src_path and type(evt[0]) is FileCreatedEvent:
                    self.__observer.event_queue.get()
                    OnModified(None, elementPathObject)
                    return

            # check if deletion was made by the eoq
            if self.__CheckAndRemoveFromEventsExchangeList(elementPathObject, 'delete'):
                return

            parentDirPathObject = elementPathObject.parent
            parentDirHash = self.__GetHashId(parentDirPathObject)

            metaDirAbsPath = self.__GetMetaDirAbsPath()

            # perform changes on the local sever domain simply reverting the steps which where made on creation of this
            # elements at server startup
            if elementPathObject.suffix == ".ecore" and str(parentDirPathObject.absolute()) in metaDirAbsPath:
                # delete event from events exchange list since the deletion of the ecore causes no events which could
                # be tracked by the pyeoq
                self.__UnloadMetaModel(elementPathObject)

            elif elementPathObject.name in self.metaDir:
                # get all files which are .ecore Files on top level of the deleted meta folder and unregister them since  only .ecore Files
                # on top level are registerd to track the corresponding models
                elementHash = self.__GetHashId(elementPathObject)
                elementObject = self.valueCodec.Dec(elementHash)

                # get all .ecore files which where contained in the top of the deleted directory and unload them
                for resource in elementObject.resources:
                    if resource.name[-6:] == ".ecore":
                        # convert path so it is absolute to the workspace directory
                        resourceAbsolutePath = self.__GetLastPersitentPath(resource)
                        resourcePathObject = Path(self.baseDir +'\\' +os.path.relpath(resourceAbsolutePath, self.baseDir))
                        self.__UnloadMetaModel(resourcePathObject)

                # unregister Folder and other files in it
                self.__UnloadResourceOrDir(elementPathObject, elementTypeInEoq)

            # in this case the resource is file or dir the procedure of deleting is the same
            else:
                # this case ist just needed for mac since there is no event for deleted subfiles on windows
                if parentDirHash is False:
                    self.logger.Info(
                        f"Watchdog: Parent dir of '{str(elementPathObject)}' already deleted. Performing no changes on the Eoq.")
                else:
                    self.__UnloadResourceOrDir(elementPathObject,elementTypeInEoq)

        def OnModified(event:FileSystemEvent, modifiedObjectPathObject=None):
            self.logger.Debug('Watchdog: OnModified')
            # catch resources which have been changed outside of the ecoreeditor during server runtime
            if event is not None:
                modifiedObjectPathObject = Path(event.src_path)

            # only reload objects corresponding to which fullfill the following conditions:
            # - they are Files, this is tested with event.is_directory and a check if a file ending exists because when the folder is
            # deleted, there is no check if it was a flder with is_file
            # - they are known in the pyeoq via an fitting .ecore file
            # - the corresponding event should not be skipped
            if not modifiedObjectPathObject.is_dir() and not modifiedObjectPathObject.suffix == ""\
                    and self.__CheckForKnownFile(modifiedObjectPathObject,silent=True) and not self.CheckForAndSkipOnModified(event):
                self.logger.Info(f"Watchdog: Modification of File {str(modifiedObjectPathObject.absolute())} detected")
                self.__ReloadResource(modifiedObjectPathObject)


        def OnAnyEvent(event:FileSystemEvent):
            self.logger.Debug('Watchdog: OnAnyEvent')
            if event.event_type == 'modified' and not event.is_directory:
                # onModified events often appear twice for one event so the redundant event gets filtered out here
                time.sleep(0.002)  # wait if eventually a redundant event is occurring
                eventQueueCopy = list(self.__observer.event_queue.queue)
                # search if there is a on modified event which is the same as the current event and delete it from the eventqueue
                for element in eventQueueCopy:
                    if element[0].event_type == 'modified' and element[0].src_path == event.src_path:
                        self.__observer.event_queue.get()
            return

        #### function defininitions are over and the main part of the event handler starts ####

        # add signs so the extensions can be processed in the patternMatchingEventHandler
        fileExtensionsToTrack = ["*"]+["*."+extension for extension in self.knownModelExtensions+self.knownXmlExtensions]

        # set up pattern matching event handler with ignoring temporary files and DS_Store of mac
        # todo: here is a problem when i want all folders to be checked but only specific files
        myEventHandler = PatternMatchingEventHandler(patterns=fileExtensionsToTrack, ignore_patterns=["*.DS_Store", "*.tmp", "*.TMP"],
                                                   case_sensitive=True, ignore_directories=False)

        # pass functions to specific events of the watchdog
        myEventHandler.on_created = OnCreated
        myEventHandler.on_moved = OnMoved
        myEventHandler.on_deleted = OnDeleted
        myEventHandler.on_modified = OnModified
        myEventHandler.on_any_event = OnAnyEvent

        return myEventHandler

    #### useful utility functions are starting here ####
    def __GetHashId(self, srcPath:Path):
        # get the elements of the path and delete the known working directory
        splitPathToObjectTuple = (srcPath.parts)[1:]

        # get the directory of the modelroot
        directory = self.modelroot

        # differentiate between source directory hash, hash of file and hash of dir wanted
        if len(splitPathToObjectTuple) == 0:
            return self.valueCodec.Enc(directory)
        elif "." in splitPathToObjectTuple[-1]:
            file = splitPathToObjectTuple[-1]
            splitPathToObjectTuple = splitPathToObjectTuple[:-1]
        else:
            file = None

        # find the parent object hash in the eoq when splitPathToObjectTuple is at least one element long.
        # Otherwise the root element is the parent object
        if len(splitPathToObjectTuple) >= 1:
            # this try expands the function so it is possible to check if a element exists in the eoq with this function
                # get the directory of the parent folder of the created object by iterate through a part of the
                # array not containing the root element or the destination object
                for element in splitPathToObjectTuple:
                    subdirexists = False
                    for subdir in directory.subdirectories:
                        if subdir.name == element:
                            directory = subdir
                            subdirexists = True
                            break
                    if not subdirexists:
                        return False

        # just return the current workspace as Hash, because there is no subfolder in the path
        if file is None:
            return self.valueCodec.Enc(directory)
        else:
            # get the corresponding resource object of the searched resource and return the object hash
            for resource in directory.resources:
                if resource.name == file:
                    return self.valueCodec.Enc(resource)
            return False

    def __AddEventToEventsExchangeList(self, pathObject:Path, eventId:str):
        '''This function adds an element to the events exchange list so the eoq and the watchdog can communicate about the events they caused'''
        self.exchangeChangeEventsList.append((eventId, pathObject.absolute()))

    def __RemoveEventFromEventsExchangeList(self, pathObject:Path, eventId:str) -> bool:
        if (eventId,pathObject.absolute()) in self.exchangeChangeEventsList:
            self.exchangeChangeEventsList.remove((eventId,pathObject.absolute()))
            return True
        else:
            return False

    def __IsEventInEventsExchangeList(self,pathObject:Path,identifierString:str) -> bool:
        '''Checks if the path element combined with id string is in the events exchange list'''
        for element in self.exchangeChangeEventsList:
            if element[0] == identifierString and element[1].resolve() == pathObject.resolve():
                return True
        return False

    def __CheckAndRemoveFromEventsExchangeList(self, pathObject:Path, identifierString:str, silent=False) -> bool:
        if self.__IsEventInEventsExchangeList(pathObject, identifierString):
            self.__RemoveEventFromEventsExchangeList(pathObject, identifierString)
            if not silent:
                self.logger.Info(f"Watchdog: {identifierString} of {str(pathObject.absolute())} recognized. Skipping Event")
            return True
        else:
            if not silent:
                self.logger.Info(f"Watchdog: {identifierString} of {str(pathObject.absolute())} detected.")
                return False

    def __GetMetaDirAbsPath(self) -> list:
        '''Takes all meta directories and returns all as absolute path strings in an array'''
        metaDirAbsPath = []
        for metaDir in self.metaDir:
            if not os.path.isabs(metaDir):
                metaDirAbsPath.append(os.path.join(self.baseDirAbs, metaDir))
            else:
                metaDirAbsPath.append(metaDir)
        return metaDirAbsPath

    def __LoadMetaModelFromFileSystem(self, elementPathObject:Path, parentDirPathObject=None):
        if parentDirPathObject is None:
            parentDirPathObject = elementPathObject.parent

        # load the ecore model from the files system as normal resource
        self.__LoadResourceFromFileSystem(elementPathObject)

        self.__LoadMetaModelResource(str(elementPathObject.absolute()))

        trackedEnding = str(elementPathObject.name[:-6])

        self.logger.Info(f"Watchdog: Meta Model {elementPathObject} registered.")
        self.logger.Info(f"Watchdog: Scanning and loading {trackedEnding}-Files.")

        # now checking which files have the "new" registered ending and include them into the pyeoq
        # get all the files which are in the workspace
        (directories, modelfiles) = self.__ScanForFilesAndDirectories()

        # counter for later printout and information
        registeredFilesNumber = 0
        notRegisteredFilesNumber = 0

        for element in modelfiles.copy():
            # only work on files which have the now available file ending
            if element[len(element)-len(trackedEnding):] == trackedEnding:

                # configure the filepaths etc for the new file to register
                newFoundFilePathObject = Path(os.path.relpath(element, self.baseDirAbs[:-len(self.baseDir)]))
                newFoundFileParentPathObject = newFoundFilePathObject.parent
                newFoundFileParentDirhash = self.__GetHashId(newFoundFileParentPathObject)

                # add the change which is to be made to the change list so there is no interference with the eoq trying
                # to add this folder/file to the file system
                self.__AddEventToEventsExchangeList(newFoundFilePathObject, "create")

                # uses the function which is also used during the start of the server to ensure compatibility of the changes
                resource = self.__LoadResource(element)

                # check if loading succeeded
                if (resource):
                    resource.name = str(newFoundFilePathObject.name)
                    # get the eoq hash for the loaded resource so it is possible to append the created model to the folder
                    # in the eoq. This is needed to be done with a domain.Do since only those are tracked by the EcoreEditor
                    objectHash = self.valueCodec.Enc(resource)
                    self.domain.Do(Add(newFoundFileParentDirhash, 'resources', objectHash))
                    registeredFilesNumber += 1
                else:
                    self.logger.Info(f"Watchdog: loading of created File '{str(newFoundFilePathObject.name)}' failed. Skipping file.")
                    # remove entry in the events exchange list so there is no confusion and leftover artifact
                    self.__RemoveEventFromEventsExchangeList(elementPathObject, "create")
                    notRegisteredFilesNumber += 1

        self.logger.Info(f"Watchdog: {notRegisteredFilesNumber+registeredFilesNumber} {trackedEnding}-Files found after registering. "
                         f"{registeredFilesNumber} loaded into the Workspace. {notRegisteredFilesNumber} could not be loaded.")

    def __UnloadMetaModel(self, elementPathObject:Path):
        self.logger.Info(f"Watchdog: Unloading {str(elementPathObject.absolute())}")
        start = default_timer()

        # unload meta model as resource
        self.__UnloadResourceOrDir(elementPathObject, 'resources')

        # get the file ending which has to be untracked
        untrackedEnding = str(elementPathObject.name[:-6])

        # reverting changes made during loading the meta model
        self.knownModelExtensions.remove(untrackedEnding)
        modelContents = self.__LoadModelContents(str(elementPathObject.absolute()))
        gcmRoot = modelContents[0]

        # unregister all subpackages belonging to the deleted ecore file
        for child in gcmRoot.eAllContents():
            if (isinstance(child, EPackage)):
                self.rset.metamodel_registry.pop(child.nsURI)
        # unregister meta model file itselve
        self.rset.metamodel_registry.pop(gcmRoot.nsURI)

        end = default_timer()
        self.logger.Info("ok (%f s)"%(end-start))
        self.logger.Info(f"Watchdog: Unloading files corresponding with the deleted meta model")

        # get all the files which are in the workspace
        (directories, modelfiles) = self.__ScanForFilesAndDirectories()

        for element in modelfiles.copy():
            # only work on files which have the now available file ending
            if element[len(element)-len(untrackedEnding):] == untrackedEnding:
                fileToUnloadPathObject = Path(os.path.relpath(element, self.baseDirAbs[:-len(self.baseDir)]))
                self.__UnloadResourceOrDir(fileToUnloadPathObject, 'resources')


        self.logger.Info(f"Watchdog: All files corresponding to {str(elementPathObject.absolute())} unregistered")

    def __LoadResourceFromFileSystem(self, elementPathObject:Path, parentDirPathObject=None):
        # make function usable without parent dir path object
        if parentDirPathObject is None:
            parentDirPathObject = elementPathObject.parent

        self.logger.Info(f"Watchdog: New created file '{str(elementPathObject.name)}' in '{parentDirPathObject.absolute()} detected.'")

        # uses the function which is also used during the start of the server to ensure compatibility of the changes with the eoq and support
        # loading known xml files and known model files
        resource = self.__LoadResource(str(elementPathObject.absolute()))

        # check if loading succeeded
        if (resource):
            resource.name = str(elementPathObject.name)
            # get the eoq hash for the loaded resource so it is possible to append the created model to the folder
            # in the eoq. This is needed to be done with a domain.Do since only those are tracked by the EcoreEditor
            objectHash = self.valueCodec.Enc(resource)
            parentDirHash = self.__GetHashId(parentDirPathObject)
            self.domain.Do(Add(parentDirHash, 'resources', objectHash))
        else:
            self.logger.Info(f"Watchdog: loading of created File '{str(elementPathObject.name)}' failed. Skipping file.")
            # remove entry in the events exchange list so there is no confusion and leftover artifact
            self.__RemoveEventFromEventsExchangeList(elementPathObject, "create")

    def __LoadDirFromFileSystem(self, elementPathObject:Path, parentDirHash):
        # imitate the loading function for directories on server startup to ensure compatibility of the changes
        createdDirectory = Directory(name=str(elementPathObject.name))
        self.__SetLastPersistentPath(createdDirectory, str(elementPathObject.absolute()))

        # the creation of the hash and the operation on the domain is needed so the ecoreeditor is informed
        # about the changes
        directoryHash = self.valueCodec.Enc(createdDirectory)
        self.domain.Do(Add(parentDirHash, 'subdirectories', directoryHash))

    def __UnloadResourceOrDir(self, elementPathObject:Path, elementTypeInEoq=None):
        '''Unload a resource from the eoq without deleting it. Used for the Watchdog'''
        if not elementPathObject.suffix == "":  #this is there to have consistency in the output, with the output when the server starts
            self.logger.Info(f"Watchdog: Unloading {str(elementPathObject.absolute())}....")
        start = default_timer()
        deletedObjectHash = self.__GetHashId(elementPathObject)

        # option to just unload resource locally if the eoq requires no change for example when the parent folder in the
        # eoq is already moved
        # get hashes for later operation on the eoq
        parentDirPathObject = elementPathObject.parent
        parentDirHash = self.__GetHashId(parentDirPathObject)
        # add event to exchange events list so the eoq knows that the change has been made by the Watchdog
        self.__AddEventToEventsExchangeList(elementPathObject, "delete")
        # perform changes on the domain
        self.domain.Do(Cmp().Rem(parentDirHash, elementTypeInEoq, deletedObjectHash))
        try:
            resource = self.valueCodec.Dec(deletedObjectHash)
            self.__DeleteResourceOrDirectoryPath(resource)
            end = default_timer()
            if not elementPathObject.suffix == "":  # this is there to have consistency in the output, with the output when the server starts
                self.logger.Info("ok (%f s)"%(end-start))
        except Exception as e:
            self.logger.Info("Watchdog: Failed to delete resource in the eoq %s."%(str(e)))
            traceback.print_exc()

    def __RenameResourceOrDir(self, elementPathObject:Path, name):
        # get hash id to undo renaming
        objectHash = self.__GetHashId(elementPathObject)

        # perform changes on the eoq
        self.domain.Do(Set(objectHash, 'name', name))

        # refresh path of object in the eoq
        renamedObjectEObject = self.valueCodec.Dec(objectHash)
        self.__RefreshResourceOrDirectoryPath(renamedObjectEObject)

    def __ReloadResource(self, resourcePathObject:Path):
        resourcePath = str(resourcePathObject.absolute())
        if resourcePathObject.suffix[1:] in self.knownModelExtensions:
            resource = self.valueCodec.Dec(self.__GetHashId(resourcePathObject))
            eResource = self.__GetEResourceForModelResource(resource)
            try:
                self.logger.Info("Watchdog: Reloading %s ..." % resourcePath)
                start = default_timer()
                # delete eResource and clean up connection to the resource
                self.__DeleteLastPeristentPath(eResource)
                self.__UnlinkModelResourceAndEResource(resource)
                self.rset.remove_resource(eResource)
                # load new eResource
                newEResource = self.rset.get_resource(resourcePath)
                # swap content
                resource.contents[0] = newEResource.contents[0]
                # register the resource in the lookup table
                self.__LinkModelResourceAndEResource(resource, newEResource)
                self.__SetLastPersistentPath(newEResource, resourcePath)
                # read the contents to the resource object because the containment removes it
                for content in resource.contents:
                    eResource.append(content)
                end = default_timer()
                self.logger.Info("ok (%f s)"%(end-start))
            except Exception as e:
                self.logger.Info("failed: %s"%(str(e)))
        elif resourcePathObject.suffix[1:] in self.knownXmlExtensions:
            resource = self.valueCodec.Dec(self.__GetHashId(resourcePathObject))
            try:
                self.logger.Info("Watchdog: Reloading %s ..." % resourcePath)
                start = default_timer()
                # parse input-xml
                xmlparse = xml.etree.ElementTree
                tree = xmlparse.parse(resourcePath)
                root = tree.getroot()
                ldfile = Document(name=resource.name, version="1.0")
                rootelement = Element(name=root.tag, content=root.text.strip())
                resource.document = ldfile
                resource.document.rootelement = rootelement
                for attr in root.attrib:
                    newAttr = Attribute(name=attr, value=root.attrib[attr])
                    rootelement.attributes.add(newAttr)
                # find first layer
                for element in root:
                    if (element.text == None):
                        element.text = ""
                    # find all subclasses within first layer
                    self.__FindChildElements(element, rootelement)
                end = default_timer()
                self.logger.Info("ok (%f s)"%(end-start))
            except Exception as e:
                self.logger.Info("failed: %s"%(str(e)))

        else:
            self.logger.Info(f"skipped Reloading {resourcePath}: Unknown format.")

    def __CheckForKnownFile(self,elementPathObject:Path, silent = False):
        # check what for element was changed and set a element type so the deletion command can be used for all elements
        if not elementPathObject.suffix:
            elementTypeInEoq = "subdirectories"
        elif elementPathObject.suffix[1:] in self.knownModelExtensions+self.knownXmlExtensions:
            elementTypeInEoq = 'resources'
        else:
            if not silent:
                self.logger.Info(f"The Object '{str(elementPathObject.absolute())}' has no equivalent on the eoq. "
                                 "No action has been performed on the Eoq.")
            return False
        return elementTypeInEoq

    def __ParentWasMoved(self, oldElementPathObject: Path, newElementPathObject: Path) -> bool:
        """ This function decides whether a one of the parent folders of the File/Folder was renamed or was moved
        to another folder """
        workspacePathObject = Path(self.baseDir)
        splitOldPath = list(oldElementPathObject.relative_to(workspacePathObject.parent).parts)
        splitNewPath = list(newElementPathObject.relative_to(workspacePathObject.parent).parts)

        # get the first element from top down in which the two paths differ to check if thoose exist. If both exist the
        # file/folder was just moved. If the old one does not exist, one of hte parent folders was renamed
        for oldPathElement, newPathElement in zip(reversed(splitOldPath), reversed(splitNewPath)):
            if oldPathElement != newPathElement:
                oldDifferentPathObject = oldElementPathObject
                newDifferentPathObject = newElementPathObject
                while oldDifferentPathObject.name != oldPathElement:
                    oldDifferentPathObject = oldDifferentPathObject.parent
                while newDifferentPathObject.name != newPathElement:
                    newDifferentPathObject = newDifferentPathObject.parent
                return newDifferentPathObject.exists() and oldDifferentPathObject.exists()
                pass
            pass
        pass

    def CheckForAndSkipOnModified(self,event:FileSystemEvent) -> bool:
        """Check if the event source path is already marked to skip in the skip list and decrement the skip counter if this is true"""
        for [eventToSkip, timesToSkip] in self.modifiedEventSkipList.copy():
            if eventToSkip.src_path == event.src_path or str(Path(event.src_path).absolute()) == eventToSkip.src_path:
                self.modifiedEventSkipList.remove([eventToSkip, timesToSkip])
                if timesToSkip > 1:
                    self.AddFileEventToSkipList(eventToSkip,timesToSkip-1)
                    return True
                elif timesToSkip == 1:
                    return True
                else:
                    print('Error in the CheckForAndSkipOnModified function of the watchdog. An entry has the'
                          'value 0 for times to skip.')
        return False
    
    def AddFileEventToSkipList(self,fileEvent,n):
        if(self.trackFileChanges):
            self.modifiedEventSkipList.append([fileEvent,n])
            
    def Lock(self):
        self.__ConnectAllEResources()
        #self.mdb.Lock()

    def Release(self):
        self.__DisconnectAllEResources()
        #self.mdb.Release()
