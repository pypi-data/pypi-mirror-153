'''
Provides various eoq-related model functions
2020 Institute of Aircraft Systems, University of Stuttgart
'''

from eoq2 import Get,Set,Add,Rem,Clo,Crn,CloModes
from eoq2 import Qry,Pth
from eoq2.util import error
from eoq2.event import EvtTypes


def GetName(domain,item) -> str:
    """ Retrieves name for given item """
    return domain.Do(Get(Qry(item).Pth("name")))


def GetId(domain,item) -> str:
    """ Retrieves ID for given item """
    return domain.Do(Get(Qry(item).Pth("id")))


def EventLogger(evts,source):
    """ Creates EventLogger and handles logging """
    for evt in evts:
        if evt.evt == EvtTypes.CST:
            print("EVT: Status of call %d changed to %s" % (evt.a[0],evt.a[1]))
        elif evt.evt == EvtTypes.OUP:
            print("EVT: Output of call %d on channel %s: %s" % (evt.a[0],evt.a[1],evt.a[2]))
        elif evt.evt == EvtTypes.CVA:
            print("EVT: Result of call %d: %s" % (evt.a[0],evt.a[1]))
        elif evt.evt == EvtTypes.CHG:
            print("EVT: Change (%d): %s t: %s, f: %s, n: %s, [was: v:%s, o: %s, f:%s, i:%s] (tid:%d)" % (
                evt.a[0],evt.a[1],evt.a[2],evt.a[3],evt.a[4],evt.a[5],evt.a[6],evt.a[7],evt.a[8],evt.a[9]))
        elif evt.evt == EvtTypes.MSG:
            print("EVT: Message: %s" % evt.a)


def CreateNewModelResource(domain,outFile,outDir,modelRoot):
    """ Saves OAAM model resource to file """
    print('Saving OAAM model to %s...' % outFile,end='')
    try:
        outModel = domain.Do(Get(Qry(outDir).Pth('resources').Sel(Pth('name').Equ(outFile)).Idx(0)))
        print('Replaced existing %s' % outFile)
    except (IndexError,error.EoqError):
        outModel = domain.Do(Crn('http://www.eoq.de/workspacemdbmodel/v1.0','ModelResource',1))
        domain.Do(Set(Qry(outModel),'name',outFile))
        domain.Do(Add(Qry(outDir),'resources',outModel))
        print('Created new %s' % outFile)
    domain.Do(Rem(Qry(outModel),'contents',Qry(outModel).Pth('contents')))  # clear the contents
    domain.Do(Add(Qry(outModel),'contents',modelRoot))
    print('Saved.')
    return


def CloneModelResource(domain,tempFile,templateDir=None):
    """ Clones model resource from template """
    if templateDir:
        templateRoot = domain.Do(Get(Pth('subdirectories').Sel(Pth('name').Equ(templateDir)).Idx(0).Pth('resources')
                                     .Sel(Pth('name').Equ(tempFile)).Idx(0).Pth('contents').Idx(0)))  # workspace mdb
    else:
        templateRoot = domain.Do(Get(Pth('resources').Sel(Pth('name').Equ(tempFile)).Idx(0).Pth('contents').Idx(0)))
    return domain.Do(Clo(Qry(templateRoot),CloModes.FUL))
