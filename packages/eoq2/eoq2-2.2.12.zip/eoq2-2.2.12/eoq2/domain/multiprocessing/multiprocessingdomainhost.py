'''
 2019 Bjoern Annighoefer
'''

'''
    Server
'''

from ..domain import Domain
from ...serialization import JsonSerializer
from ...frame import FrameTypes,Frame
from ...event import EvtTypes

from multiprocessing import Queue
import queue # imported for using queue.Empty exception
   
import threading
import traceback

class MultiprocessingQueueDomainHost(Domain):
    def __init__(self,domain,callManager,serializer=JsonSerializer(),timeout=0.1,sessionId=None,callId=None):
        super().__init__()
        self.domain = domain
        self.callManager = callManager
        self.cmdQueue = Queue()
        self.resQueue = Queue()
        self.evtQueue = Queue()
        self.timeout = timeout
        self.sessionId = sessionId
        self.callId = callId
        
        self.serializer = serializer
        self.shallRun = True
        
        #listen to domain events
        self.domain.Observe(self.OnDomainEvent,context=self,sessionId=self.sessionId)
        
    def Start(self):
        self.listenerThread = threading.Thread(target=self.__RemoteCommandHandler, args=())
        self.listenerThread.start()
        
    def Join(self):
        self.domain.Unobserve(self.OnDomainEvent,context=self)
        self.shallRun = False
        self.listenerThread.join()
        
    def __RemoteCommandHandler(self):
        while self.shallRun:
            try:
                frameStr = self.cmdQueue.get(timeout=self.timeout)
                frames = self.serializer.Des(frameStr)
                outFrames = []
                for frame in frames:
                    if(frame.eoq==FrameTypes.CMD):
                        cmd = frame.dat
                        res = self.domain.RawDo(cmd,sessionId=self.sessionId)
                        frame.eoq = FrameTypes.RES
                        frame.dat = res
                        outFrames.append(frame)
                    elif(frame.eoq == FrameTypes.EVT):
                        evt = frame.dat
                        if(evt.evt == EvtTypes.OUP):
                            self.callManager.AddCallOutputRaw(evt.a[0],evt.a[1],evt.a[2])
                        elif(evt.evt == EvtTypes.CST):
                            callId = evt.a[0]
                            status = evt.a[1]
                            info = evt.a[2]
                            self.callManager.ChangeCallStatus(callId,status,info)
                        elif(evt.evt == EvtTypes.CVA):
                            self.callManager.SetCallValue(evt.a[0],evt.a[1])
                #send a cumulative answer
                if(len(outFrames)>0):
                    frameStr = self.serializer.Ser(outFrames)
                    self.resQueue.put(frameStr) 
                    
            except queue.Empty:
                continue
            except Exception as e:
                print("Error in MultiprocessingQueueDomainHost: %s"%(str(e)))
                traceback.print_exc()
        #thread ends here
            
    def OnDomainEvent(self,evts,source):
        outFrames = []
        for evt in evts:
            if(evt.evt in [EvtTypes.OUP,EvtTypes.CST,EvtTypes.CVA] and self.callId==evt.a[0]): #do not feedback own events
                continue
            outFrames.append(Frame(FrameTypes.EVT,0,evt))
        # if there are events, than forward them
        if(len(outFrames)>0):
            frameStr = self.serializer.Ser(outFrames)
            self.evtQueue.put(frameStr)