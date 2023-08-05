import requests
#Logging
import os
import logging
import datetime
import copy
from .Utils import TimerRepeat # Timer which can repeating
mLogger=logging.getLogger("OrchestratorConnector")
#########################
mTimerList=[]
def IntervalTerminateAll():
    for lItem in mTimerList:
        lItem.stop()
#########################
# Создать файл логирования
# add filemode="w" to overwrite
if not os.path.exists("Reports"):
    os.makedirs("Reports")
##########################
# Подготовка логгера Robot
#########################
mLogger.setLevel(logging.INFO)
# create the logging file handler
mLoggerFH = logging.FileHandler("Reports\ReportOrchestratorConnector_" + datetime.datetime.now().strftime("%Y_%m_%d") + ".log")
mLoggerFormatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
mLoggerFH.setFormatter(mLoggerFormatter)
# add handler to logger object
mLogger.addHandler(mLoggerFH)
############################################
#Turn loggin level ERROR
def LoggerSetLevelError():
    mLogger.setLevel(logging.ERROR)
#from requests import async
import json
###################################
##Orchestrator integration module (safe use when orchestrator is turned off)
###################################
################################################################################
# Recieve data from orchestrator (synchronyous)
# Example:
# t=IntegrationOrchestrator.DataRecieveAsync(
#             RobotStorage=mGlobal["Storage"],
#             RobotStorageKey="R01_OrchestratorToRobot",
#             OrchestratorKeyList=["Storage", "R01_OrchestratorToRobot"],
#             OrchestratorProtocol="http",
#             OrchestratorHost="localhost",
#             OrchestratorPort=8081,
#             OrchestratorAuthToken="1992-04-03-0643-ru-b4ff-openrpa52zzz"
#         )
def DataReceiveSync(
        OrchestratorKeyList, OrchestratorProtocol="http",
        OrchestratorHost="localhost", OrchestratorPort=80, OrchestratorAuthToken=None
    ):
    lCookies = {}
    # Set auth token if authorization is needed
    if OrchestratorAuthToken:
        lCookies["AuthToken"] = OrchestratorAuthToken
    lURL = f'{OrchestratorProtocol}://{OrchestratorHost}:{OrchestratorPort}/Utils/Processor'
    lDataJSON = [{"Type": "GlobalDictKeyListValueGet", "KeyList": OrchestratorKeyList}]
    try:
        lResult = requests.post(lURL, json=lDataJSON, cookies=lCookies)
        lResultJSON = json.loads(lResult.text)
        return (True, lResultJSON[0]["Result"])  # (Flag response is ok, Data)
    except Exception:
        mLogger.warning(
            f"Orchestrator not responding. Def DataRecieveSync, OrchestratorKeyList: {str(OrchestratorKeyList)}, OrchestratorProtocol: {str(OrchestratorProtocol)}, OrchestratorHost: {str(OrchestratorHost)}, OrchestratorPort: {str(OrchestratorPort)}")
        return (False, None)  # (Flag response is not ok, Data None)
################################################################################
# Recieve data from orchestrator (asynchronyous)
# Example:
# t=IntegrationOrchestrator.DataRecieveAsync(
#             RobotStorage=mGlobal["Storage"],
#             RobotStorageKey="R01_OrchestratorToRobot",
#             OrchestratorKeyList=["Storage", "R01_OrchestratorToRobot"],
#             OrchestratorProtocol="http",
#             OrchestratorHost="localhost",
#             OrchestratorPort=8081,
#             OrchestratorAuthToken="1992-04-03-0643-ru-b4ff-openrpa52zzz"
#         )
def DataReceiveAsync(
        RobotStorage, RobotStorageKey, OrchestratorKeyList, OrchestratorProtocol="http",
        OrchestratorHost="localhost", OrchestratorPort=80, OrchestratorAuthToken=None
    ):
    from threading import Thread
    import uuid
    global mGlobalDict
    class ThreadAsync(Thread):
        def DataRecieveSync(self):
            lCookies = {}
            #Set auth token if authorization is needed
            if OrchestratorAuthToken:
                lCookies["AuthToken"] = OrchestratorAuthToken
            lURL = f'{OrchestratorProtocol}://{OrchestratorHost}:{OrchestratorPort}/Utils/Processor'
            lDataJSON = [{"Type": "GlobalDictKeyListValueGet", "KeyList": OrchestratorKeyList}]
            try:
                lResult = requests.post(lURL, json=lDataJSON, cookies = lCookies)
                lResultJSON = json.loads(lResult.text)
                return (True,lResultJSON[0]["Result"]) #(Flag response is ok, Data)
            except Exception:
                mLogger.warning(
                    f"Orchestrator not responding. Def DataRecieveAsync, OrchestratorKeyList: {str(OrchestratorKeyList)}, OrchestratorProtocol: {str(OrchestratorProtocol)}, OrchestratorHost: {str(OrchestratorHost)}, OrchestratorPort: {str(OrchestratorPort)}")
                return (False,None) #(Flag response is not ok, Data None)
        # Thread init
        def __init__(self, name):
            Thread.__init__(self)
            self.name = name
        #Thread start
        def run(self):
            (lFlagResponseOK,lResponseData) = self.DataRecieveSync()
            if lFlagResponseOK:
                RobotStorage[RobotStorageKey] = lResponseData
    ThreadObject = ThreadAsync(f"ThreadAsync{str(uuid.uuid1())}")
    ThreadObject.start()
    return True
################################################################################
#IntervalDataRecieveAsync - Periodic recieve data from orchestrator and update storage
def IntervalDataReceiveAsync(*args, **kwargs):
    lInterval=3
    #Delete index 0 from args
    lArgs=copy.copy(args)
    if len(lArgs)>0:
        lInterval = lArgs[0]
        lArgs = lArgs[1:]
    #Delete Interval from kwargs
    lKwargs = copy.copy(kwargs)
    if "Interval" in lKwargs:
        lInterval = lKwargs["Interval"]
        del lKwargs["Interval"]
    lTimer = TimerRepeat.TimerRepeat(lInterval, DataReceiveAsync, lArgs, lKwargs)
    lTimer.start()
    #Add timer to general list to stop this when needed
    mTimerList.append(lTimer)
    return lTimer
################################################################################
###################################
################################
###################################
################################################################################
# Send data from orchestrator (synchronyous)
# Example:
# t=IntegrationOrchestrator.DataSendSync(
#             RobotValue="Value",
#             OrchestratorKeyList=["Storage", "R01_OrchestratorToRobot"],
#             OrchestratorProtocol="http",
#             OrchestratorHost="localhost",
#             OrchestratorPort=8081,
#             OrchestratorAuthToken="1992-04-03-0643-ru-b4ff-openrpa52zzz"
#         )
def DataSendSync(
        RobotValue, OrchestratorKeyList, OrchestratorProtocol="http",
        OrchestratorHost="localhost", OrchestratorPort=80, OrchestratorAuthToken=None
    ):
    lCookies = {}
    # Set auth token if authorization is needed
    if OrchestratorAuthToken:
        lCookies["AuthToken"] = OrchestratorAuthToken
    lURL = f'{OrchestratorProtocol}://{OrchestratorHost}:{OrchestratorPort}/Utils/Processor'
    lDataJSON = [{"Type": "GlobalDictKeyListValueSet", "KeyList": OrchestratorKeyList, "Value": RobotValue}]
    try:
        lResult = requests.post(lURL, json=lDataJSON, cookies=lCookies)
        lResultJSON = json.loads(lResult.text)
        return (True, lResultJSON[0]["Result"])  # (Flag response is ok, Data)
    except Exception:
        mLogger.warning(
            f"Orchestrator not responding. Def: DataSendSync, RobotValue: {str(RobotValue)}, OrchestratorKeyList: {str(OrchestratorKeyList)}, OrchestratorProtocol: {str(OrchestratorProtocol)}, OrchestratorHost: {str(OrchestratorHost)}, OrchestratorPort: {str(OrchestratorPort)}")
        return (False, None)  # (Flag response is not ok, Data None)
################################################################################
# Send data from orchestrator (asynchronyous)
# Example:
# t=IntegrationOrchestrator.DataSendAsync(
#             RobotStorage=mGlobal["Storage"],
#             RobotStorageKey="R01_OrchestratorToRobot",
#             OrchestratorKeyList=["Storage", "R01_OrchestratorToRobot"],
#             OrchestratorProtocol="http",
#             OrchestratorHost="localhost",
#             OrchestratorPort=8081,
#             OrchestratorAuthToken="1992-04-03-0643-ru-b4ff-openrpa52zzz"
#         )
def DataSendAsync(
        RobotStorage, RobotStorageKey, OrchestratorKeyList, OrchestratorProtocol="http",
        OrchestratorHost="localhost", OrchestratorPort=80, OrchestratorAuthToken=None
    ):
    from threading import Thread
    import uuid
    global mGlobalDict
    class ThreadAsync(Thread):
        def DataSendSync(self):
            RobotValue = RobotStorage[RobotStorageKey]
            lCookies = {}
            # Set auth token if authorization is needed
            if OrchestratorAuthToken:
                lCookies["AuthToken"] = OrchestratorAuthToken
            lURL = f'{OrchestratorProtocol}://{OrchestratorHost}:{OrchestratorPort}/Utils/Processor'
            lDataJSON = [{"Type": "GlobalDictKeyListValueSet", "KeyList": OrchestratorKeyList, "Value": RobotValue}]
            try:
                lResult = requests.post(lURL, json=lDataJSON, cookies=lCookies)
                lResultJSON = json.loads(lResult.text)
                return (True, lResultJSON[0]["Result"])  # (Flag response is ok, Data)
            except Exception:
                mLogger.warning(
                    f"Orchestrator not responding. Def: DataSendAsync, RobotValue: {str(RobotValue)}, OrchestratorKeyList: {str(OrchestratorKeyList)}, OrchestratorProtocol: {str(OrchestratorProtocol)}, OrchestratorHost: {str(OrchestratorHost)}, OrchestratorPort: {str(OrchestratorPort)}")
                return (False, None)  # (Flag response is not ok, Data None)
        # Thread init
        def __init__(self, name):
            Thread.__init__(self)
            self.name = name
        #Thread start
        def run(self):
            self.DataSendSync()
    ThreadObject = ThreadAsync(f"ThreadAsync{str(uuid.uuid1())}")
    ThreadObject.start()
    return True
################################################################################
#IntervalDataSendAsync - Periodic send data from robot to orchestrator
def IntervalDataSendAsync(*args,**kwargs):
    lInterval=3
    #Delete index 0 from args
    lArgs=copy.copy(args)
    if len(lArgs)>0:
        lInterval = lArgs[0]
        lArgs = lArgs[1:]
    #Delete Interval from kwargs
    lKwargs = copy.copy(kwargs)
    if "Interval" in lKwargs:
        lInterval = lKwargs["Interval"]
        del lKwargs["Interval"]
    lTimer = TimerRepeat.TimerRepeat(lInterval, DataSendAsync, lArgs, lKwargs)
    lTimer.start()
    #Add timer to general list to stop this when needed
    mTimerList.append(lTimer)
    return lTimer
################################################################################
###################################
################################
###################################
################################################################################
# Check if RobotStorage[Key] Value has been changed > then send data + reset to orchestrator (asynchronyous) timeout 2 seconds
# Example:
# t=IntegrationOrchestrator.DataSendResetAsync(
#             RobotStorage=mGlobal["Storage"],
#             RobotStorageKey="R01_OrchestratorToRobot",
#             RobotResetValue="Test",
#             OrchestratorKeyList=["Storage", "R01_OrchestratorToRobot"],
#             OrchestratorProtocol="http",
#             OrchestratorHost="localhost",
#             OrchestratorPort=8081,
#             OrchestratorAuthToken="1992-04-03-0643-ru-b4ff-openrpa52zzz"
#         )
def DataSendResetAsync(
        RobotStorage, RobotStorageKey, RobotResetValue, OrchestratorKeyList, OrchestratorProtocol="http",
        OrchestratorHost="localhost", OrchestratorPort=80, OrchestratorAuthToken=None
    ):
    #Do operations if data not equal to ResetValue
    if RobotStorage[RobotStorageKey] != RobotResetValue:
        #Get value
        lRobotValue = copy.deepcopy(RobotStorage[RobotStorageKey])
        #Reset value
        RobotStorage[RobotStorageKey] = copy.deepcopy(RobotResetValue)
        #Send data (retry while data will be transferred completele)
        from threading import Thread
        import uuid
        import time
        global mGlobalDict
        class ThreadAsync(Thread):
            def DataSendSync(self):
                RobotValue = lRobotValue
                lCookies = {}
                # Set auth token if authorization is needed
                if OrchestratorAuthToken:
                    lCookies["AuthToken"] = OrchestratorAuthToken
                lURL = f'{OrchestratorProtocol}://{OrchestratorHost}:{OrchestratorPort}/Utils/Processor'
                lDataJSON = [{"Type": "GlobalDictKeyListValueSet", "KeyList": OrchestratorKeyList, "Value": RobotValue}]
                lFlagDataTransmit = False
                while not lFlagDataTransmit:
                    try:
                        lResult = requests.post(lURL, json=lDataJSON, cookies=lCookies)
                        lResultJSON = json.loads(lResult.text)
                        lFlagDataTransmit = True
                    except Exception:
                        mLogger.warning(
                            f"Orchestrator not responding - will retry to send update. Timeout 2 seconds. Def: DataSendResetAsync, RobotValue: {str(RobotValue)}, OrchestratorKeyList: {str(OrchestratorKeyList)}, OrchestratorProtocol: {str(OrchestratorProtocol)}, OrchestratorHost: {str(OrchestratorHost)}, OrchestratorPort: {str(OrchestratorPort)}")
                        time.sleep(2) #Timout for next loop
                return (True,True) # Only True can be returned
            # Thread init
            def __init__(self, name):
                Thread.__init__(self)
                self.name = name
            # Thread start
            def run(self):
                self.DataSendSync()
        ThreadObject = ThreadAsync(f"ThreadAsync{str(uuid.uuid1())}")
        ThreadObject.start()
        return True
    return True
################################################################################
################################################################################
#IntervalDataSendResetAsync - Periodic check changed and send + reset data from robot to orchestrator
def IntervalDataSendResetAsync(*args,**kwargs):
    lInterval=3
    #Delete index 0 from args
    lArgs=copy.copy(args)
    if len(lArgs)>0:
        lInterval = lArgs[0]
        lArgs = lArgs[1:]
    #Delete Interval from kwargs
    lKwargs = copy.copy(kwargs)
    if "Interval" in lKwargs:
        lInterval = lKwargs["Interval"]
        del lKwargs["Interval"]
    lTimer = TimerRepeat.TimerRepeat(lInterval, DataSendResetAsync, lArgs, lKwargs)
    lTimer.start()
    #Add timer to general list to stop this when needed
    mTimerList.append(lTimer)
    return lTimer
################################################################################
# Check changes in orchestrator - then replace in RobotStorage if not equeal. Has no timeout because You can use function IntervalDataReceiveResetAsync (asynchronyous)
#Next iteration do not rewrite value until new change has come from orchestrator
# Example:
# t=IntegrationOrchestrator.DataRecieveAsync(
#             RobotStorage=mGlobal["Storage"],
#             RobotStorageKey="R01_OrchestratorToRobot",
#             RobotResetValue={"Test":"Test"},
#             OrchestratorKeyList=["Storage", "R01_OrchestratorToRobot"],
#             OrchestratorProtocol="http",
#             OrchestratorHost="localhost",
#             OrchestratorPort=8081,
#             OrchestratorAuthToken="1992-04-03-0643-ru-b4ff-openrpa52zzz"
#         )
def DataReceiveResetAsync(
        RobotStorage, RobotStorageKey, RobotResetValue, OrchestratorKeyList, OrchestratorProtocol="http",
        OrchestratorHost="localhost", OrchestratorPort=80, OrchestratorAuthToken=None
    ):
    from threading import Thread
    import uuid
    global mGlobalDict
    class ThreadAsync(Thread):
        def DataRecieveSync(self):
            lCookies = {}
            #Set auth token if authorization is needed
            if OrchestratorAuthToken:
                lCookies["AuthToken"] = OrchestratorAuthToken
            lURL = f'{OrchestratorProtocol}://{OrchestratorHost}:{OrchestratorPort}/Utils/Processor'
            lDataJSON = [
                {"Type": "GlobalDictKeyListValueGet", "KeyList": OrchestratorKeyList},
                {"Type": "GlobalDictKeyListValueSet", "KeyList": OrchestratorKeyList, "Value": RobotResetValue}
            ]
            try:
                lResult = requests.post(lURL, json=lDataJSON, cookies = lCookies)
                lResultJSON = json.loads(lResult.text)
                #Change data if it changes with ResetValue
                if lResultJSON[0]["Result"] != RobotResetValue:
                    return (True,lResultJSON[0]["Result"]) #(Flag data changes is ok, Data)
                else:
                    return (False, lResultJSON[0]["Result"])  # (Flag data changes is false - dont rewrite in RobotStorage, Data)
            except Exception:
                mLogger.warning(
                    f"Orchestrator not responding. Def DataReceiveResetAsync, RobotResetValue: {str(RobotResetValue)}, OrchestratorKeyList: {str(OrchestratorKeyList)}, OrchestratorProtocol: {str(OrchestratorProtocol)}, OrchestratorHost: {str(OrchestratorHost)}, OrchestratorPort: {str(OrchestratorPort)}")
                return (False,None) #(Flag response is not ok, Data None)
        # Thread init
        def __init__(self, name):
            Thread.__init__(self)
            self.name = name
        #Thread start
        def run(self):
            (lFlagResponseOK,lResponseData) = self.DataRecieveSync()
            if lFlagResponseOK:
                RobotStorage[RobotStorageKey] = lResponseData
    ThreadObject = ThreadAsync(f"ThreadAsync{str(uuid.uuid1())}")
    ThreadObject.start()
    return True
################################################################################
################################################################################
#IntervalDataReceiveResetAsync - Periodic receive + every time reset and check changed and reset data on robot storage
def IntervalDataReceiveResetAsync(*args,**kwargs):
    lInterval=3
    #Delete index 0 from args
    lArgs=copy.copy(args)
    if len(lArgs)>0:
        lInterval = lArgs[0]
        lArgs = lArgs[1:]
    #Delete Interval from kwargs
    lKwargs = copy.copy(kwargs)
    if "Interval" in lKwargs:
        lInterval = lKwargs["Interval"]
        del lKwargs["Interval"]
    # Reset the storage before start
    DataSendSync(
            RobotValue=lKwargs["RobotResetValue"],
            OrchestratorKeyList=lKwargs["OrchestratorKeyList"], OrchestratorProtocol=lKwargs["OrchestratorProtocol"],
            OrchestratorHost=lKwargs["OrchestratorHost"], OrchestratorPort=lKwargs["OrchestratorPort"],
            OrchestratorAuthToken=lKwargs["OrchestratorAuthToken"]
    )
    lTimer = TimerRepeat.TimerRepeat(lInterval, DataReceiveResetAsync, lArgs, lKwargs)
    lTimer.start()
    #Add timer to general list to stop this when needed
    mTimerList.append(lTimer)
    return lTimer
#################################################################################
#################################################################################
################################################################################
#ConfigurationInit - Get dict configuration and init interval functions
def ConfigurationInit(inConfigurationDict):
    for lItem in inConfigurationDict.keys():
        lFunction = globals()[lItem]
        #Iterate throught the nested list
        for lFunctionConfigurationDict in inConfigurationDict[lItem]:
            lFunction(**lFunctionConfigurationDict)
    return True