#from pyOpenRPA.Orchestrator import Managers
from .. import __Orchestrator__
import os
import time

from pyOpenRPA import Orchestrator
class Process():
    """
    Manager process, which is need to be started / stopped / restarted

    With Process instance you can automate your process activity. Use schedule package to set interval when process should be active and when not.

    All defs in class are pickle safe! After orchestrator restart (if not the force stop of the orchestrator process) your instance with properties will be restored. But it not coverage the scheduler which is in __Orchestrator__ .
    After orc restart you need to reinit all schedule rules: Orchestrator.OrchestratorScheduleGet

    Process instance has the following statuses:
        - 0_STOPPED
        - 1_STOPPED_MANUAL
        - 2_STOP_SAFE
        - 3_STOP_SAFE_MANUAL
        - 4_STARTED
        - 5_STARTED_MANUAL

    .. code-block:: python
        # For the safe init class use ProcessInitSafe
        lProcess = Orchestrator.Managers.ProcessInitSafe(inAgentHostNameStr="PCNAME",inAgentUserNameStr="USER",
             inProcessNameWOExeStr="notepad",inStartCMDStr="notepad",inStopSafeTimeoutSecFloat=3)
        # Async way to run job
        lProcess.ScheduleStatusCheckEverySeconds(inIntervalSecondsInt=5)
        Orchestrator.OrchestratorScheduleGet().every(5).seconds.do(Orchestrator.OrchestratorThreadStart,
                                                                   lProcess.StartCheck)
        # OR (sync mode)
        Orchestrator.OrchestratorScheduleGet().every(5).seconds.do(lProcess.StartCheck)

    How to use StopSafe on the robot side

    .. code-block:: python
        from pyOpenRPA.Tools import StopSafe
        StopSafe.Init(inLogger=None)
        StopSafe.IsSafeStop() # True - WM_CLOSE SIGNAL has come. taskkill /im someprocess.exe
    """

    mAgentHostNameStr = None
    mAgentUserNameStr = None
    mStartPathStr = None
    mStartCMDStr = None
    mStartArgDict = None
    mStatusCheckIntervalSecFloat = None
    mProcessNameWOExeStr = None
    mStopSafeTimeoutSecFloat = None
    mStatusStr = None # 0_STOPPED 1_STOPPED_MANUAL 2_STOP_SAFE 3_STOP_SAFE_MANUAL 4_STARTED 5_STARTED_MANUAL

    # MST - Manual Stop Trigger
    mMSTdTSecFloat: float = None
    mMSTdNInt = None
    mMSTStartTimeList = []

    mAgentMuteBool = False # Mute any sends to agent while some action is perfomed

    mStatusSavedStr = None # Saved status to the further restore

    def MuteWait(self):
        """
        Internal def. Wait when class is apply to send new activities to the agent

        :return:
        """
        lIntervalSecFloat = 0.3
        while self.mAgentMuteBool == True:
            time.sleep(lIntervalSecFloat)
        return None

    def KeyTurpleGet(self):
        """
        Get the key turple of the current process

        """
        return (self.mAgentHostNameStr.upper(), self.mAgentUserNameStr.upper(), self.mProcessNameWOExeStr.upper())


    def __init__(self, inAgentHostNameStr, inAgentUserNameStr, inProcessNameWOExeStr, inStartPathStr=None, inStartCMDStr = None, inStopSafeTimeoutSecFloat=300, inStartArgDict=None, inStatusCheckIntervalSecFloat=30):
        """
        Init the class instance.
        !ATTENTION! Function can raise exception if process with the same (inAgentHostNameStr, inAgentUserNameStr, inProcessNameWOExeStr) is already exists in GSettings (can be restored from previous Orchestrator session). See ProcessInitSafe to sefaty init the instance or restore previous
        !ATTENTION! Schedule options you must

        :param inAgentHostNameStr: Agent hostname in any case. Required to identify Process
        :param inAgentUserNameStr: Agent user name in any case. Required to identify Process
        :param inProcessNameWOExeStr: The process name without extension .exe (the key of the Process instance). Any case - will be processed to the upper case
        :param inStartPathStr: Path to start process (.cmd/ .exe or something else). Path can be relative (from orc working directory) or absolute
        :param inStartCMDStr: CMD script to start program (if no start file is exists)
        :param inStopSafeTimeoutSecFloat: Time to wait for stop safe. After that do the stop force (if process is not stopped)
        """
        lGS = __Orchestrator__.GSettingsGet()
        # Check if Process is not exists in GSettings
        if (inAgentHostNameStr.upper(), inAgentUserNameStr.upper(), inProcessNameWOExeStr.upper()) not in lGS["ManagersProcessDict"]:
            self.mStartArgDict = inStartArgDict
            self.mAgentHostNameStr = inAgentHostNameStr
            self.mAgentUserNameStr = inAgentUserNameStr
            self.mStartPathStr = inStartPathStr
            self.mStartCMDStr = inStartCMDStr
            self.mProcessNameWOExeStr = inProcessNameWOExeStr
            self.mStopSafeTimeoutSecFloat = inStopSafeTimeoutSecFloat
            lGS["ManagersProcessDict"][(inAgentHostNameStr.upper(), inAgentUserNameStr.upper(), inProcessNameWOExeStr.upper())]=self
            lActivityDict = __Orchestrator__.ProcessorActivityItemCreate(inDef=self.StatusCheck,inArgList=[], inThreadBool=True)
            __Orchestrator__.ProcessorActivityItemAppend(inActivityItemDict=lActivityDict)
            if inStatusCheckIntervalSecFloat is not None: __Orchestrator__.OrchestratorScheduleGet().every(inStatusCheckIntervalSecFloat).seconds.do(Orchestrator.OrchestratorThreadStart,self.StatusCheck)
            self.mStatusCheckIntervalSecFloat = inStatusCheckIntervalSecFloat
        else: raise Exception(f"Managers.Process ({inAgentHostNameStr}, {inAgentUserNameStr}, {inProcessNameWOExeStr}): Can't init the Process instance because it already inited in early (see ProcessInitSafe)")

    def ManualStopTriggerSet(self, inMSTdTSecFloat: float, inMSTdNInt: int) -> None:
        """
        Set ManualStopTrigger (MST) to switch to STOPPED MANUAL if specified count of start fails will be catched in specified time period

        :param inMSTdTSecFloat: Time perios in seconds
        :param inMSTdNInt: Counts of the start tries
        :return: None
        """

        # MST - Manual Stop Trigger
        self.mMSTdTSecFloat = inMSTdTSecFloat
        self.mMSTdNInt = inMSTdNInt


    def ManualStopTriggerNewStart(self):
        """
        Log new start event. Check if it is applicable. Change status if ManualStop trigger criteria is applied

        :return: # 0_STOPPED 1_STOPPED_MANUAL 2_STOP_SAFE 3_STOP_SAFE_MANUAL 4_STARTED 5_STARTED_MANUAL
        """
        if self.mMSTdTSecFloat is not None and self.mMSTdNInt is not None:
            lTimeNowSecFloat  = time.time()
            self.mMSTStartTimeList.append(lTimeNowSecFloat) # Append current time to MST list
            # Remove old items from list
            lMSTStartTimeList = []
            for lTimeItemSecFloat in self.mMSTStartTimeList:
                ldTSecFloat = lTimeNowSecFloat - lTimeItemSecFloat
                # Move to the new list if dT less
                if ldTSecFloat < self.mMSTdTSecFloat: lMSTStartTimeList.append(lTimeItemSecFloat)
            self.mMSTStartTimeList = lMSTStartTimeList # Set new list
            # Check count in list
            if len(lMSTStartTimeList) > self.mMSTdNInt:
                self.mStatusStr = "1_STOPPED_MANUAL"
                # Log info about process
                lL = __Orchestrator__.OrchestratorLoggerGet()
                lL.info(f"Managers.Process ({self.mAgentHostNameStr}, {self.mAgentUserNameStr}, {self.mProcessNameWOExeStr}): ManualStopTrigger is activated. {self.mMSTdNInt} start tries in {self.mMSTdTSecFloat} sec.")
        return self.mStatusStr

    def ManualStopListClear(self) -> None:
        """
        Clear the last start tries list.

        :return: None
        """
        self.mMSTStartTimeList=[]

    def Manual2Auto(self) -> str:
        """
        Remove Manual flag from process (if exists) - it will allow the schedule operations via def StatusCheckStart(self):    def StatusCheckStorForce(self): def StatusCheckStopSafe(self):

        :return: Process status. See self.mStatusStr. 0_STOPPED 1_STOPPED_MANUAL 2_STOP_SAFE 3_STOP_SAFE_MANUAL 4_STARTED 5_STARTED_MANUAL
        """
        lLogBool = False
        if self.mStatusStr=="1_STOPPED_MANUAL": self.mStatusStr = "0_STOPPED"; lLogBool=True
        if self.mStatusStr=="3_STOP_SAFE_MANUAL": self.mStatusStr = "2_STOP_SAFE"; lLogBool=True
        if self.mStatusStr=="5_STARTED_MANUAL": self.mStatusStr = "4_STARTED"; lLogBool=True
        # Log info about process
        if lLogBool == True: self.StatusChangeLog()
        return self.mStatusStr

    def Start(self, inIsManualBool = True, inStartArgDict=None) -> str:
        """
        Manual/Auto start. Manual start will block scheduling execution. To return schedule execution use def Manual2Auto.
        Will not start if STOP SAFE is now and don't start auto is stopped manual now

        :param inIsManualBool: Default is True - Mark this operation as manual - StatusCheckStart/Stop will be blocked - only StatusCheck will be working. False - Auto operation
        :return: Process status. See self.mStatusStr. 0_STOPPED 1_STOPPED_MANUAL 2_STOP_SAFE 3_STOP_SAFE_MANUAL 4_STARTED 5_STARTED_MANUAL
        """
        if inIsManualBool == False: self.ManualStopTriggerNewStart() # Set the time
        if self.mStatusStr is not None and (self.mStatusStr == "1_STOPPED_MANUAL" or "STOP_SAFE" in self.mStatusStr) and inIsManualBool == False:
            lStr = f"Managers.Process ({self.mAgentHostNameStr}, {self.mAgentUserNameStr}, {self.mProcessNameWOExeStr}): Process will not start because of stopped manual or stop safe is now."
            __Orchestrator__.OrchestratorLoggerGet().warning(lStr)
            return self.mStatusStr
        # Send activity item to agent - wait result
        if self.mStartPathStr is not None: lCMDStr = os.path.abspath(self.mStartPathStr)
        elif self.mStartCMDStr is not None: lCMDStr = self.mStartCMDStr
        # Append args
        if inStartArgDict is not None: self.mStartArgDict = inStartArgDict
        if self.mStartArgDict is not None:
            for lItemKeyStr in self.mStartArgDict:
                lItemValueStr = self.mStartArgDict[lItemKeyStr]
                lCMDStr = f"{lCMDStr} {lItemKeyStr} {lItemValueStr}"
        #import pdb
        #pdb.set_trace()
        self.MuteWait()
        self.mAgentMuteBool=True
        lActivityItemStart = __Orchestrator__.ProcessorActivityItemCreate(inDef="OSCMD",
              inArgDict={"inCMDStr":lCMDStr,"inSendOutputToOrchestratorLogsBool":False, "inCaptureBool":False},
              inArgGSettingsStr="inGSettings")
        lGUIDStr = __Orchestrator__.AgentActivityItemAdd(inHostNameStr=self.mAgentHostNameStr,
                                                         inUserStr=self.mAgentUserNameStr,
                                                         inActivityItemDict=lActivityItemStart)
        lStartResult = __Orchestrator__.AgentActivityItemReturnGet(inGUIDStr=lGUIDStr)
        if inIsManualBool==True:
            self.mStatusStr = "5_STARTED_MANUAL"
        else:
            self.mStatusStr = "4_STARTED"
        # Log info about process
        self.StatusChangeLog()
        self.mAgentMuteBool = False
        return self.mStatusStr

    def StartCheck(self) -> str:
        """
        Start program if auto stopped (0_STOPPED).

        :return: Process status. See self.mStatusStr. 0_STOPPED 1_STOPPED_MANUAL 2_STOP_SAFE 3_STOP_SAFE_MANUAL 4_STARTED 5_STARTED_MANUAL
        """
        self.MuteWait()
        if self.mStatusStr == "0_STOPPED":
            self.Start(inIsManualBool=False)
        return self.mStatusStr

    def StopSafe(self, inIsManualBool = True, inStopSafeTimeoutSecFloat = None) -> str:
        """
        Manual/Auto stop safe. Stop safe is the operation which send signal to process to terminate own work (send term signal to process). Managers.Process wait for the mStopSafeTimeoutSecFloat seconds. After that, if process is not terminated - self will StopForce it.
        Manual stop safe will block scheduling execution. To return schedule execution use def Manual2Auto

        :param inIsManualBool: Default is True - Mark this operation as manual - StatusCheckStart/Stop will be blocked - only StatusCheck will be working. False - Auto operation
        :param inStopSafeTimeoutSecFloat: Default value goes from the instance. You can specify time is second to wait while safe stop. After that program will stop force
        :return: Process status. See self.mStatusStr. 0_STOPPED 1_STOPPED_MANUAL 2_STOP_SAFE 3_STOP_SAFE_MANUAL 4_STARTED 5_STARTED_MANUAL
        """
        if inStopSafeTimeoutSecFloat is None: inStopSafeTimeoutSecFloat = self.mStopSafeTimeoutSecFloat
        self.MuteWait()
        self.mAgentMuteBool=True
        # Send activity item to agent - wait result
        lCMDStr = f'taskkill /im "{self.mProcessNameWOExeStr}.exe" /fi "username eq %USERNAME%"'
        lActivityItemStart = __Orchestrator__.ProcessorActivityItemCreate(
            inDef="OSCMD",inArgDict={"inCMDStr": lCMDStr,"inSendOutputToOrchestratorLogsBool":False, "inCaptureBool": False},inArgGSettingsStr="inGSettings")
        lGUIDStr = __Orchestrator__.AgentActivityItemAdd(inHostNameStr=self.mAgentHostNameStr,
                                                         inUserStr=self.mAgentUserNameStr,
                                                         inActivityItemDict=lActivityItemStart)
        lStartResult = __Orchestrator__.AgentActivityItemReturnGet(inGUIDStr=lGUIDStr)
        if inIsManualBool==True:
            self.mStatusStr = "3_STOP_SAFE_MANUAL"
        else:
            self.mStatusStr = "2_STOP_SAFE"
        # Log info about process
        self.StatusChangeLog()
        # Interval check is stopped
        lTimeStartFloat = time.time()
        lIntervalCheckSafeStatusFLoat = 15.0
        while "SAFE" in self.mStatusStr and (time.time() - lTimeStartFloat) < inStopSafeTimeoutSecFloat:
            self.StatusCheck()
            if "SAFE" not in self.mStatusStr: break
            time.sleep(lIntervalCheckSafeStatusFLoat)
        if "SAFE" in  self.mStatusStr:
            # Log info about process
            lL = __Orchestrator__.OrchestratorLoggerGet()
            lL.info(f"Managers.Process ({self.mAgentHostNameStr}, {self.mAgentUserNameStr}, {self.mProcessNameWOExeStr}): Safe stop has been wait for {inStopSafeTimeoutSecFloat} sec. Now do the force stop.")
            self.StopForce(inIsManualBool=inIsManualBool,inMuteIgnoreBool=True)
        # Log info about process
        # self.StatusChangeLog() status check has already log status (see above)
        self.mAgentMuteBool = False
        return self.mStatusStr

    def StopSafeCheck(self, inStopSafeTimeoutSecFloat = None) -> str:
        """
        Stop safe program if auto started (4_STARTED).

        :param inStopSafeTimeoutSecFloat: Default value goes from the instance. You can specify time is second to wait while safe stop. After that program will stop force
        :return: Process status. See self.mStatusStr. 0_STOPPED 1_STOPPED_MANUAL 2_STOP_SAFE 3_STOP_SAFE_MANUAL 4_STARTED 5_STARTED_MANUAL
        """
        self.MuteWait()
        if self.mStatusStr == "4_STARTED":
            self.StopSafe(inIsManualBool=False, inStopSafeTimeoutSecFloat = inStopSafeTimeoutSecFloat)
        return self.mStatusStr

    def StopForce(self, inIsManualBool = True, inMuteIgnoreBool = False) -> str:
        """
        Manual/Auto stop force. Force stop don't wait process termination  - it just terminate process now.
        Manual stop safe will block scheduling execution. To return schedule execution use def Manual2Auto

        :param inIsManualBool: Default is True - Mark this operation as manual - StatusCheckStart/Stop will be blocked - only StatusCheck will be working. False - Auto operation
        :return: Process status. See self.mStatusStr. 0_STOPPED 1_STOPPED_MANUAL 2_STOP_SAFE 3_STOP_SAFE_MANUAL 4_STARTED 5_STARTED_MANUAL
        """
        if inMuteIgnoreBool == False: self.MuteWait()
        lMuteWorkBool = False
        if self.mAgentMuteBool==False: self.mAgentMuteBool=True; lMuteWorkBool=True
        # Send activity item to agent - wait result
        lCMDStr = f'taskkill /F /im "{self.mProcessNameWOExeStr}.exe" /fi "username eq %USERNAME%"'
        lActivityItemStart = __Orchestrator__.ProcessorActivityItemCreate(
            inDef="OSCMD",inArgDict={"inCMDStr": lCMDStr,"inSendOutputToOrchestratorLogsBool":False, "inCaptureBool": False},inArgGSettingsStr="inGSettings")
        lGUIDStr = __Orchestrator__.AgentActivityItemAdd(inHostNameStr=self.mAgentHostNameStr,
                                                         inUserStr=self.mAgentUserNameStr,
                                                         inActivityItemDict=lActivityItemStart)
        lStartResult = __Orchestrator__.AgentActivityItemReturnGet(inGUIDStr=lGUIDStr)
        if inIsManualBool==True:
            self.mStatusStr = "1_STOPPED_MANUAL"
        else:
            self.mStatusStr = "0_STOPPED"
        # Log info about process
        self.StatusChangeLog()
        if lMuteWorkBool == True:
            self.mAgentMuteBool=False
        return self.mStatusStr

    def StopForceCheck(self) -> str:
        """
        Stop force program if auto started (4_STARTED).

        :return: Process status. See self.mStatusStr. 0_STOPPED 1_STOPPED_MANUAL 2_STOP_SAFE 3_STOP_SAFE_MANUAL 4_STARTED 5_STARTED_MANUAL
        """
        self.MuteWait()
        if self.mStatusStr == "4_STARTED":
            self.StopForce(inIsManualBool=False)
        return self.mStatusStr

    def RestartSafe(self, inIsManualBool = True):
        """
        Manual/Auto restart safe. Restart safe is the operation which send signal to process to terminate own work (send term signal to process). Then it run process. Managers.Process wait for the mStopSafeTimeoutSecFloat seconds. After that, if process is not terminated - self will StopForce it.
        Manual stop safe will block scheduling execution. To return schedule execution use def Manual2Auto

        :param inIsManualBool: Default is True - Mark this operation as manual - StatusCheckStart/Stop will be blocked - only StatusCheck will be working. False - Auto operation
        :return: Process status. See self.mStatusStr. 0_STOPPED 1_STOPPED_MANUAL 2_STOP_SAFE 3_STOP_SAFE_MANUAL 4_STARTED 5_STARTED_MANUAL
        """
        self.StopSafe(inIsManualBool=inIsManualBool)
        return self.Start(inIsManualBool=inIsManualBool)

    def RestartForce(self, inIsManualBool = True):
        """
        Manual/Auto restart force. Force restart dont wait process termination  - it just terminate process now ant then start it.
        Manual restart will block scheduling execution. To return schedule execution use def Manual2Auto

        :param inIsManualBool: Default is True - Mark this operation as manual - StatusCheckStart/Stop will be blocked - only StatusCheck will be working. False - Auto operation
        :return: Process status. See self.mStatusStr. 0_STOPPED 1_STOPPED_MANUAL 2_STOP_SAFE 3_STOP_SAFE_MANUAL 4_STARTED 5_STARTED_MANUAL
        """
        self.StopForce(inIsManualBool=inIsManualBool)
        return self.Start(inIsManualBool=inIsManualBool)

    def StatusSave(self):
        """
        Save current status of the process. After that you can restore process activity. Work when orchestrator is restarted. Don't save "STOP_SAFE" status > "STOPPED"

        :return: Process status. See self.mStatusStr. 0_STOPPED 1_STOPPED_MANUAL 2_STOP_SAFE 3_STOP_SAFE_MANUAL 4_STARTED 5_STARTED_MANUAL
        """
        lWarnSafeBool = True
        if self.mStatusStr == "2_STOP_SAFE": self.mStatusSavedStr = "0_STOPPED"
        elif self.mStatusStr == "3_STOP_SAFE_MANUAL": self.mStatusSavedStr = "1_STOPPED_MANUAL"
        else: self.mStatusSavedStr = self.mStatusStr; lWarnSafeBool = False
        if lWarnSafeBool==True: __Orchestrator__.OrchestratorLoggerGet().warning(f"Managers.Process ({self.mAgentHostNameStr}, {self.mAgentUserNameStr}, {self.mProcessNameWOExeStr}): Safe status has been catched when safe > change saved status to stopped.")
        return self.mStatusStr


    def StatusCheckIntervalRestore(self):
        """Call from orchestrator when init
        """
        if self.mStatusCheckIntervalSecFloat is not None: 
            __Orchestrator__.OrchestratorLoggerGet().info(f"Managers.Process ({self.mAgentHostNameStr}, {self.mAgentUserNameStr}, {self.mProcessNameWOExeStr}): Restore schedule to StatusCheck in interval of {self.mStatusCheckIntervalSecFloat} sec.")
            __Orchestrator__.OrchestratorScheduleGet().every(self.mStatusCheckIntervalSecFloat).seconds.do(Orchestrator.OrchestratorThreadStart,self.StatusCheck)

    def StatusRestore(self):
        """
        Execute the StatusCheck, after that restore status to the saved state (see StatusSave). Work when orchestrator is restarted.

        :return: Process status. See self.mStatusStr. 0_STOPPED 1_STOPPED_MANUAL 2_STOP_SAFE 3_STOP_SAFE_MANUAL 4_STARTED 5_STARTED_MANUAL
        """
        self.StatusCheck() # check current status
        # Do some action
        if self.mStatusSavedStr != self.mStatusStr and self.mStatusSavedStr is not None:
            #lManualBool = False
            #if "MANUAL" in self.mStatusSavedStr:
            #    lManualBool = True
            if "STOPPED" in self.mStatusSavedStr and "STOPPED" not in self.mStatusStr:
                self.StopSafe(inIsManualBool=True)
            if "STARTED" in self.mStatusSavedStr and "STARTED" not in self.mStatusStr:
                self.Start(inIsManualBool=True)
            Orchestrator.OrchestratorLoggerGet().info(f"Managers.Process ({self.mAgentHostNameStr}, {self.mAgentUserNameStr}, {self.mProcessNameWOExeStr}): Status has been restored to {self.mStatusSavedStr}")
            self.mStatusStr = self.mStatusSavedStr
            self.mStatusSavedStr = None
        return self.mStatusStr

    def StatusChangeLog(self):
        """
        Lof information about status change

        :return:
        """
        # Log info about process
        lL = __Orchestrator__.OrchestratorLoggerGet()
        lL.info(f"Managers.Process ({self.mAgentHostNameStr}, {self.mAgentUserNameStr}, {self.mProcessNameWOExeStr}): Status has been changed to {self.mStatusStr})")


    def StatusCheck(self):
        """
        Check if process is alive. The def will save the manual flag is exists. Don't wait mute but set mute if it is not set.

        :return: Process status. See self.mStatusStr. 0_STOPPED 1_STOPPED_MANUAL 2_STOP_SAFE 3_STOP_SAFE_MANUAL 4_STARTED 5_STARTED_MANUAL
        """
        # Send activity item to agent - wait result
        lLogBool = False
        lActivityItemUserProcessList = __Orchestrator__.ProcessorActivityItemCreate(inDef="ProcessWOExeUpperUserListGet")
        #self.MuteWait()
        self.mAgentMuteBool=True
        lGUIDStr = __Orchestrator__.AgentActivityItemAdd(inHostNameStr=self.mAgentHostNameStr,inUserStr=self.mAgentUserNameStr,inActivityItemDict=lActivityItemUserProcessList)
        lUserProcessList = __Orchestrator__.AgentActivityItemReturnGet(inGUIDStr=lGUIDStr)
        if self.mProcessNameWOExeStr.upper() in lUserProcessList:
            if self.mStatusStr == "1_STOPPED_MANUAL": self.mStatusStr = "5_STARTED_MANUAL"; lLogBool=True
            if self.mStatusStr == "0_STOPPED": self.mStatusStr = "4_STARTED"; lLogBool=True
            if self.mStatusStr is None: self.mStatusStr = "4_STARTED"; lLogBool=True
        else:
            if self.mStatusStr == "2_STOP_SAFE": self.mStatusStr = "0_STOPPED"; lLogBool = True
            if self.mStatusStr == "3_STOP_SAFE_MANUAL": self.mStatusStr = "1_STOPPED_MANUAL"; lLogBool = True
            if self.mStatusStr == "5_STARTED_MANUAL": self.mStatusStr = "1_STOPPED_MANUAL"; lLogBool=True
            if self.mStatusStr == "4_STARTED": self.mStatusStr = "0_STOPPED"; lLogBool=True
            if self.mStatusStr is None: self.mStatusStr = "0_STOPPED"; lLogBool=True
        # Log info about process
        if lLogBool == True: self.StatusChangeLog()
        self.mAgentMuteBool = False
        return self.mStatusStr
    def StatusCheckStart(self):
        """
        Check process status and run it if auto stopped self.mStatusStr is "0_STOPPED"

        :return: Process status. See self.mStatusStr. 0_STOPPED 1_STOPPED_MANUAL 2_STOP_SAFE 3_STOP_SAFE_MANUAL 4_STARTED 5_STARTED_MANUAL
        """
        lStatusStr = self.StatusCheck()
        if lStatusStr == "0_STOPPED":
            self.Start(inIsManualBool=False)
        return self.mStatusStr
    def StatusCheckStopForce(self):
        """
        Check process status and auto stop force it if self.mStatusStr is 4_STARTED

        :return: Process status. See self.mStatusStr. 0_STOPPED 1_STOPPED_MANUAL 2_STOP_SAFE 3_STOP_SAFE_MANUAL 4_STARTED 5_STARTED_MANUAL
        """
        lStatusStr = self.StatusCheck()
        if lStatusStr == "4_STARTED":
            self.StopForce(inIsManualBool=False)
        return self.mStatusStr

    def StatusCheckStopSafe(self):
        """
        Check process status and auto stop safe it if self.mStatusStr is 4_STARTED

        :return:
        """
        lStatusStr = self.StatusCheck()
        if lStatusStr == "4_STARTED":
            self.StopSafe(inIsManualBool=False)
        return self.mStatusStr


def ProcessInitSafe(inAgentHostNameStr, inAgentUserNameStr, inProcessNameWOExeStr, inStartPathStr=None, inStartCMDStr = None, inStopSafeTimeoutSecFloat=300) -> Process:
    """
    Exception safe function. Check if process instance is not exists in GSettings (it can be after restart because Orchestrator restore objects from dump of the previous Orchestrator session)
    Return existing instance (if exists) or create new instance and return it.

    :param inAgentHostNameStr: Agent hostname in any case. Required to identify Process
    :param inAgentUserNameStr: Agent user name in any case. Required to identify Process
    :param inProcessNameWOExeStr: The process name without extension .exe (the key of the Process instance). Any case - will be processed to the upper case
    :param inStartPathStr: Path to start process (.cmd/ .exe or something else). Path can be relative (from orc working directory) or absolute
    :param inStartCMDStr: CMD script to start program (if no start file is exists)
    :param inStopSafeTimeoutSecFloat: Time to wait for stop safe. After that do the stop force (if process is not stopped)
    :return: Process instance
    """
    lProcess = ProcessGet(inAgentHostNameStr = inAgentHostNameStr, inAgentUserNameStr = inAgentUserNameStr, inProcessNameWOExeStr=inProcessNameWOExeStr)
    if lProcess is not None: return lProcess
    else: return Process(inAgentHostNameStr=inAgentHostNameStr,inAgentUserNameStr=inAgentUserNameStr,inProcessNameWOExeStr=inProcessNameWOExeStr,
                  inStartPathStr=inStartPathStr,inStartCMDStr=inStartCMDStr,inStopSafeTimeoutSecFloat=inStopSafeTimeoutSecFloat)

def ProcessExists(inAgentHostNameStr: str, inAgentUserNameStr: str, inProcessNameWOExeStr: str) -> bool:
    """
    Check if the Process instance is exists in GSettings by the (inAgentHostNameStr: str, inAgentUserNameStr: str, inProcessNameWOExeStr: str)

    :param inAgentHostNameStr: Agent hostname in any case. Required to identify Process
    :param inAgentUserNameStr: Agent user name in any case. Required to identify Process
    :param inProcessNameWOExeStr: The process name without extension .exe (the key of the Process instance). Any case - will be processed to the upper case
    :return: True - process exists in gsettings; False - else
    """
    return (inAgentHostNameStr.upper(), inAgentUserNameStr.upper(), inProcessNameWOExeStr.upper()) in __Orchestrator__.GSettingsGet()["ManagersProcessDict"]


def ProcessGet(inAgentHostNameStr: str, inAgentUserNameStr: str, inProcessNameWOExeStr: str) -> Process:
    """
    Return the process instance by the inProcessNameWOExeStr

    :param inAgentHostNameStr: Agent hostname in any case. Required to identify Process
    :param inAgentUserNameStr: Agent user name in any case. Required to identify Process
    :param inProcessNameWOExeStr: The process name without extension .exe (the key of the Process instance). Any case - will be processed to the upper case
    :return: Process instance (if exists) Else None
    """
    return __Orchestrator__.GSettingsGet()["ManagersProcessDict"].get((inAgentHostNameStr.upper(), inAgentUserNameStr.upper(), inProcessNameWOExeStr.upper()),None)

def ProcessStatusStrGet(inAgentHostNameStr: str, inAgentUserNameStr: str, inProcessNameWOExeStr: str) -> str:
    """
    Get the status of the Process instance.

    :param inAgentHostNameStr: Agent hostname in any case. Required to identify Process
    :param inAgentUserNameStr: Agent user name in any case. Required to identify Process
    :param inProcessNameWOExeStr: The process name without extension .exe (the key of the Process instance). Any case - will be processed to the upper case
    :return: Process status. See self.mStatusStr.
        Process instance has the following statuses:
        - 0_STOPPED
        - 1_STOPPED_MANUAL
        - 2_STOP_SAFE
        - 3_STOP_SAFE_MANUAL
        - 4_STARTED
        - 5_STARTED_MANUAL
        - None (if Process instance not exists)
    """
    lProcess = ProcessGet(inAgentHostNameStr = inAgentHostNameStr, inAgentUserNameStr = inAgentUserNameStr, inProcessNameWOExeStr=inProcessNameWOExeStr)
    if lProcess is not None: return lProcess.mStatusStr

def ProcessStart(inAgentHostNameStr: str, inAgentUserNameStr: str, inProcessNameWOExeStr: str, inIsManualBool: bool = True) -> str:
    """
    Manual/Auto start. Manual start will block scheduling execution. To return schedule execution use def Manual2Auto

    :param inAgentHostNameStr: Agent hostname in any case. Required to identify Process
    :param inAgentUserNameStr: Agent user name in any case. Required to identify Process
    :param inProcessNameWOExeStr: The process name without extension .exe (the key of the Process instance). Any case - will be processed to the upper case
    :param inIsManualBool: Default is True - Mark this operation as manual - StatusCheckStart/Stop will be blocked - only StatusCheck will be working. False - Auto operation
    :return: Process status. See self.mStatusStr.
        Process instance has the following statuses:
        - 0_STOPPED
        - 1_STOPPED_MANUAL
        - 2_STOP_SAFE
        - 3_STOP_SAFE_MANUAL
        - 4_STARTED
        - 5_STARTED_MANUAL
        - None (if Process instance not exists)
    """
    lProcess = ProcessGet(inAgentHostNameStr = inAgentHostNameStr, inAgentUserNameStr = inAgentUserNameStr, inProcessNameWOExeStr=inProcessNameWOExeStr)
    if lProcess is not None: return lProcess.Start(inIsManualBool=inIsManualBool)


def ProcessStopSafe(inAgentHostNameStr: str, inAgentUserNameStr: str, inProcessNameWOExeStr: str, inIsManualBool: bool = True, inStopSafeTimeoutSecFloat = None) -> str:
    """
    Manual/Auto stop safe. Stop safe is the operation which send signal to process to terminate own work (send term signal to process). Managers.Process wait for the mStopSafeTimeoutSecFloat seconds. After that, if process is not terminated - self will StopForce it.
    Manual stop safe will block scheduling execution. To return schedule execution use def Manual2Auto

    :param inAgentHostNameStr: Agent hostname in any case. Required to identify Process
    :param inAgentUserNameStr: Agent user name in any case. Required to identify Process
    :param inProcessNameWOExeStr: The process name without extension .exe (the key of the Process instance). Any case - will be processed to the upper case
    :param inIsManualBool: Default is True - Mark this operation as manual - StatusCheckStart/Stop will be blocked - only StatusCheck will be working. False - Auto operation
    :param inStopSafeTimeoutSecFloat: Default value goes from the instance. You can specify time is second to wait while safe stop. After that program will stop force
    :return: Process status. See self.mStatusStr.
        Process instance has the following statuses:
        - 0_STOPPED
        - 1_STOPPED_MANUAL
        - 2_STOP_SAFE
        - 3_STOP_SAFE_MANUAL
        - 4_STARTED
        - 5_STARTED_MANUAL
        - None (if Process instance not exists)
    """
    lProcess = ProcessGet(inAgentHostNameStr = inAgentHostNameStr, inAgentUserNameStr = inAgentUserNameStr, inProcessNameWOExeStr=inProcessNameWOExeStr)
    if lProcess is not None: return lProcess.StopSafe(inIsManualBool=inIsManualBool)

def ProcessStopForce(inAgentHostNameStr: str, inAgentUserNameStr: str, inProcessNameWOExeStr: str, inIsManualBool: bool = True) -> str:
    """
    Manual/Auto stop force. Force stop dont wait process termination  - it just terminate process now.
    Manual stop safe will block scheduling execution. To return schedule execution use def Manual2Auto

    :param inAgentHostNameStr: Agent hostname in any case. Required to identify Process
    :param inAgentUserNameStr: Agent user name in any case. Required to identify Process
    :param inProcessNameWOExeStr: The process name without extension .exe (the key of the Process instance). Any case - will be processed to the upper case
    :param inIsManualBool: Default is True - Mark this operation as manual - StatusCheckStart/Stop will be blocked - only StatusCheck will be working. False - Auto operation
    :return: Process status. See self.mStatusStr.
        Process instance has the following statuses:
        - 0_STOPPED
        - 1_STOPPED_MANUAL
        - 2_STOP_SAFE
        - 3_STOP_SAFE_MANUAL
        - 4_STARTED
        - 5_STARTED_MANUAL
        - None (if Process instance not exists)
    """
    lProcess = ProcessGet(inAgentHostNameStr = inAgentHostNameStr, inAgentUserNameStr = inAgentUserNameStr, inProcessNameWOExeStr=inProcessNameWOExeStr)
    if lProcess is not None: return lProcess.StopForce(inIsManualBool=inIsManualBool)

def ProcessStatusSave(inAgentHostNameStr: str, inAgentUserNameStr: str, inProcessNameWOExeStr: str):
    """
    Save current status of the process. After that you can restore process activity. Work when orchestrator is restarted. Don't save "STOP_SAFE" status > "STOPPED"

    :return: Process status. See self.mStatusStr. 0_STOPPED 1_STOPPED_MANUAL 2_STOP_SAFE 3_STOP_SAFE_MANUAL 4_STARTED 5_STARTED_MANUAL
    """
    lProcess = ProcessGet(inAgentHostNameStr=inAgentHostNameStr, inAgentUserNameStr=inAgentUserNameStr,
                          inProcessNameWOExeStr=inProcessNameWOExeStr)
    if lProcess is not None:
        lProcess.StatusSave()
        return lProcess.mStatusStr

def ProcessStatusRestore(inAgentHostNameStr: str, inAgentUserNameStr: str, inProcessNameWOExeStr: str):
    """
    Execute the StatusCheck, after that restore status to the saved state (see StatusSave). Work when orchestrator is restarted.

    :return: Process status. See self.mStatusStr. 0_STOPPED 1_STOPPED_MANUAL 2_STOP_SAFE 3_STOP_SAFE_MANUAL 4_STARTED 5_STARTED_MANUAL
    """
    lProcess = ProcessGet(inAgentHostNameStr=inAgentHostNameStr, inAgentUserNameStr=inAgentUserNameStr,
                          inProcessNameWOExeStr=inProcessNameWOExeStr)
    if lProcess is not None:
        lProcess.StatusRestore()
        return lProcess.mStatusStr

def ProcessStatusCheck(inAgentHostNameStr: str, inAgentUserNameStr: str, inProcessNameWOExeStr: str) -> str:
    """
    Check if process is alive. The def will save the manual flag is exists.

    :param inAgentHostNameStr: Agent hostname in any case. Required to identify Process
    :param inAgentUserNameStr: Agent user name in any case. Required to identify Process
    :param inProcessNameWOExeStr: The process name without extension .exe (the key of the Process instance). Any case - will be processed to the upper case
    :return: Process status. See self.mStatusStr.
        Process instance has the following statuses:
        - 0_STOPPED
        - 1_STOPPED_MANUAL
        - 2_STOP_SAFE
        - 3_STOP_SAFE_MANUAL
        - 4_STARTED
        - 5_STARTED_MANUAL
        - None (if Process instance not exists)
    """
    lProcess = ProcessGet(inAgentHostNameStr=inAgentHostNameStr, inAgentUserNameStr=inAgentUserNameStr,
                          inProcessNameWOExeStr=inProcessNameWOExeStr)
    if lProcess is not None:
        lProcess.StatusCheck()
        return lProcess.mStatusStr

def ProcessManual2Auto(inAgentHostNameStr: str, inAgentUserNameStr: str, inProcessNameWOExeStr: str) -> str:
    """
    Remove Manual flag from process (if exists) - it will allow the schedule operations via def StatusCheckStart(self):    def StatusCheckStorForce(self): def StatusCheckStopSafe(self):

    :param inAgentHostNameStr: Agent hostname in any case. Required to identify Process
    :param inAgentUserNameStr: Agent user name in any case. Required to identify Process
    :param inProcessNameWOExeStr: The process name without extension .exe (the key of the Process instance). Any case - will be processed to the upper case
    :return: Process status. See self.mStatusStr.
        Process instance has the following statuses:
        - 0_STOPPED
        - 1_STOPPED_MANUAL
        - 2_STOP_SAFE
        - 3_STOP_SAFE_MANUAL
        - 4_STARTED
        - 5_STARTED_MANUAL
        - None (if Process instance not exists)
    """
    lProcess = ProcessGet(inAgentHostNameStr=inAgentHostNameStr, inAgentUserNameStr=inAgentUserNameStr,
                          inProcessNameWOExeStr=inProcessNameWOExeStr)
    if lProcess is not None: return lProcess.Manual2Auto()

def ProcessManualStopTriggerSet(inAgentHostNameStr: str, inAgentUserNameStr: str, inProcessNameWOExeStr: str,  inMSTdTSecFloat: float, inMSTdNInt: int) -> None:
    """
    Remove Manual flag from process (if exists) - it will allow the schedule operations via def StatusCheckStart(self):    def StatusCheckStorForce(self): def StatusCheckStopSafe(self):

    :param inAgentHostNameStr: Agent hostname in any case. Required to identify Process
    :param inAgentUserNameStr: Agent user name in any case. Required to identify Process
    :param inProcessNameWOExeStr: The process name without extension .exe (the key of the Process instance). Any case - will be processed to the upper case
    :param inMSTdTSecFloat: Time periods in seconds
    :param inMSTdNInt: Counts of the start tries
    :return: None
    """
    lProcess = ProcessGet(inAgentHostNameStr=inAgentHostNameStr, inAgentUserNameStr=inAgentUserNameStr,
                          inProcessNameWOExeStr=inProcessNameWOExeStr)
    if lProcess is not None: lProcess.ManualStopTriggerSet(inMSTdTSecFloat = inMSTdTSecFloat, inMSTdNInt = inMSTdNInt)


def ProcessManualStopListClear(inAgentHostNameStr: str, inAgentUserNameStr: str, inProcessNameWOExeStr: str) -> None:
    """
    Clear the last start tries list.

    :param inAgentHostNameStr: Agent hostname in any case. Required to identify Process
    :param inAgentUserNameStr: Agent user name in any case. Required to identify Process
    :param inProcessNameWOExeStr: The process name without extension .exe (the key of the Process instance). Any case - will be processed to the upper case
    :return: None
    """
    lProcess = ProcessGet(inAgentHostNameStr=inAgentHostNameStr, inAgentUserNameStr=inAgentUserNameStr,
                          inProcessNameWOExeStr=inProcessNameWOExeStr)
    if lProcess is not None: lProcess.ManualStopListClear()

def ProcessScheduleStatusCheckEverySeconds(inAgentHostNameStr: str, inAgentUserNameStr: str, inProcessNameWOExeStr: str,inIntervalSecondsInt: int = 120):
    """
    Run status check every interval in second you specify.

    :param inAgentHostNameStr: Agent hostname in any case. Required to identify Process
    :param inAgentUserNameStr: Agent user name in any case. Required to identify Process
    :param inProcessNameWOExeStr: The process name without extension .exe (the key of the Process instance). Any case - will be processed to the upper case
    :param inIntervalSecondsInt: Interval in seconds. Default is 120
    :return: None
    """
    lProcess = ProcessGet(inAgentHostNameStr=inAgentHostNameStr, inAgentUserNameStr=inAgentUserNameStr,
                          inProcessNameWOExeStr=inProcessNameWOExeStr)
    # Check job in threaded way
    __Orchestrator__.OrchestratorScheduleGet().every(inIntervalSecondsInt).seconds.do(__Orchestrator__.OrchestratorThreadStart,lProcess.StatusCheck)