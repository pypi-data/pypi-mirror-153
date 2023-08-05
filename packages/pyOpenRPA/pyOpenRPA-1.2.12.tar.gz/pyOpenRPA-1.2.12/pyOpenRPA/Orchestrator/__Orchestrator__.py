import subprocess, json, psutil, time, os, win32security, sys, base64, logging, ctypes, copy #Get input argument
import pickle
import inspect
import schedule
#from partd import Server

from . import Server
from . import Timer
from . import Processor
from . import BackwardCompatibility # Backward compatibility from v1.1.13
from . import Core
from . import Managers
from ..Tools import License
from subprocess import CREATE_NEW_CONSOLE
from .Utils import LoggerHandlerDumpLogList
from ..Tools import Debugger

# ATTENTION! HERE IS NO Relative import because it will be imported dynamically
# All function check the flag SessionIsWindowResponsibleBool == True else no cammand is processed
# All functions can return None, Bool or Dict { "IsSuccessful": True }
from .RobotRDPActive import CMDStr # Create CMD Strings
from .RobotRDPActive import Connector # RDP API

#from .Settings import Settings
import importlib
from importlib import util
import threading # Multi-threading for RobotRDPActive
from .RobotRDPActive import RobotRDPActive #Start robot rdp active
from .RobotScreenActive import Monitor #Start robot screen active
from . import SettingsTemplate # Settings template
import uuid # Generate uuid
import datetime # datetime
import math
import glob # search the files
import urllib

#Единый глобальный словарь (За основу взять из Settings.py)
gSettingsDict = None

# AGENT DEFS

def AgentActivityItemAdd(inHostNameStr, inUserStr, inActivityItemDict, inGSettings=None):
    """
    Add activity in AgentDict. Check if item is created

    :param inGSettings: Global settings dict (singleton)
    :param inHostNameStr: Agent host name
    :param inUserStr: User login, where agent is based
    :param inActivityItemDict: ActivityItem
    :return: GUID String of the ActivityItem - you can wait (sync or async) result by this guid!
    """

    inGSettings = GSettingsGet(inGSettings=inGSettings)  # Set the global settings
    lActivityItemDict = copy.deepcopy(inActivityItemDict)
    # Add GUIDStr if not exist
    lGUIDStr = None
    if "GUIDStr" not in lActivityItemDict:
        lGUIDStr = str(uuid.uuid4()) # generate new GUID
        lActivityItemDict["GUIDStr"] = lGUIDStr
    else: lGUIDStr = lActivityItemDict["GUIDStr"]
    # Add CreatedByDatetime
    lActivityItemDict["CreatedByDatetime"] = datetime.datetime.now()
    # Main alg
    lAgentDictItemKeyTurple = (inHostNameStr.upper(),inUserStr.upper())
    if lAgentDictItemKeyTurple not in inGSettings["AgentDict"]:
        inGSettings["AgentDict"][lAgentDictItemKeyTurple] = SettingsTemplate.__AgentDictItemCreate__()
    lThisAgentDict = inGSettings["AgentDict"][lAgentDictItemKeyTurple]
    lThisAgentDict["ActivityList"].append(lActivityItemDict)
    # Return the result
    return lGUIDStr


def AgentActivityItemExists(inHostNameStr, inUserStr, inGUIDStr, inGSettings = None):
    """
    Check by GUID if ActivityItem has exists in request list. If exist - the result response has not been recieved from the agent

    :param inGSettings: Global settings dict (singleton)
    :param inGUIDStr: GUID String of the ActivityItem
    :return: True - ActivityItem is exist in AgentDict ; False - else case
    """
    # Check if GUID is exists in dict - has been recieved
    inGSettings = GSettingsGet(inGSettings=inGSettings)  # Set the global settings
    # Main alg
    lAgentDictItemKeyTurple = (inHostNameStr.upper(),inUserStr.upper())
    lResultBool = False
    if lAgentDictItemKeyTurple in inGSettings["AgentDict"]:
        for lActivityItem in inGSettings["AgentDict"][lAgentDictItemKeyTurple]["ActivityList"]:
            if inGUIDStr == lActivityItem.get("GUIDStr",None):
                lResultBool = True
                break
    return lResultBool

def AgentActivityItemReturnExists(inGUIDStr, inGSettings = None):
    """
    Check by GUID if ActivityItem has been executed and result has come to the Orchestrator

    :param inGSettings: Global settings dict (singleton)
    :param inGUIDStr: GUID String of the ActivityItem - you can wait (sync or async) result by this guid!
    :return: True - result has been received from the Agent to orc; False - else case
    """

    inGSettings = GSettingsGet(inGSettings=inGSettings)  # Set the global settings
    # Check if GUID is exists in dict - has been recieved
    return inGUIDStr in inGSettings["AgentActivityReturnDict"]


def AgentActivityItemReturnGet(inGUIDStr, inCheckIntervalSecFloat = 0.5, inGSettings=None):
    """
    Work synchroniously! Wait while result will be recieved. Get the result of the ActivityItem execution on the Agent side. Before this please check by the def AgentActivityItemReturnExists that result has come to the Orchestrator

    !ATTENTION! Use only after Orchestrator initialization! Before orchestrator init exception will be raised.

    :param inGSettings: Global settings dict (singleton)
    :param inGUIDStr: GUID String of the ActivityItem - you can wait (sync or async) result by this guid!
    :param inCheckIntervalSecFloat: Interval in sec of the check Activity Item result
    :return: Result of the ActivityItem executed on the Agent side anr transmitted to the Orchestrator. IMPORTANT! ONLY JSON ENABLED Types CAN BE TRANSMITTED TO ORCHESTRATOR!
    """
    inGSettings = GSettingsGet(inGSettings=inGSettings)  # Set the global settings
    #Check if Orchestrator has been initialized - else raise exception
    if Core.IsOrchestratorInitialized(inGSettings=inGSettings) == True:
        # Wait while result will not come here
        while not AgentActivityItemReturnExists(inGSettings=inGSettings, inGUIDStr=inGUIDStr):
            time.sleep(inCheckIntervalSecFloat)
        # Return the result
        return inGSettings["AgentActivityReturnDict"][inGUIDStr]["Return"]
    else:
        raise Exception(f"__Orchestrator__.AgentActivityItemReturnGet !ATTENTION! Use this function only after Orchestrator initialization! Before orchestrator init exception will be raised.")

def AgentOSCMD(inHostNameStr, inUserStr, inCMDStr, inRunAsyncBool=True, inSendOutputToOrchestratorLogsBool=True, inCMDEncodingStr="cp1251", inGSettings=None, inCaptureBool=True):
    """
    Send CMD to OS thought the pyOpenRPA.Agent daemon. Result return to log + Orchestrator by the A2O connection

    :param inGSettings: Global settings dict (singleton)
    :param inHostNameStr: Agent host name in upper case (example "RPA01", "RPA_99" and so on). Active agent session you can see on the orchestrator dashboard as Orchestrator admin
    :param inUserStr: Agent user name in upper case (example "UserRPA"). Active agent session you can see on the orchestrator dashboard as Orchestrator admin
    :param inCMDStr: command to execute on the Agent session
    :param inRunAsyncBool: True - Agent processor don't wait execution; False - Agent processor wait cmd execution
    :param inSendOutputToOrchestratorLogsBool: True - catch cmd execution output and send it to the Orchestrator logs; Flase - else case; Default True
    :param inCMDEncodingStr: Set the encoding of the DOS window on the Agent server session. Windows is beautiful :) . Default is "cp1251" early was "cp866" - need test
    :param inCaptureBool: !ATTENTION! If you need to start absolutely encapsulated app - set this flag as False. If you set True - the app output will come to Agent
    :return: GUID String of the ActivityItem - you can wait (sync or async) result by this guid!
    """
    inGSettings = GSettingsGet(inGSettings=inGSettings)  # Set the global settings
    lActivityItemDict = {
        "Def":"OSCMD", # def alias (look pyOpeRPA.Agent gSettings["ProcessorDict"]["AliasDefDict"])
        "ArgList":[], # Args list
        "ArgDict":{"inCMDStr":inCMDStr,"inRunAsyncBool":inRunAsyncBool, "inSendOutputToOrchestratorLogsBool": inSendOutputToOrchestratorLogsBool, "inCMDEncodingStr": inCMDEncodingStr, "inCaptureBool":inCaptureBool}, # Args dictionary
        "ArgGSettings": "inGSettings", # Name of GSettings attribute: str (ArgDict) or index (for ArgList)
        "ArgLogger": None # Name of GSettings attribute: str (ArgDict) or index (for ArgList)
    }
    #Send item in AgentDict for the futher data transmition
    return AgentActivityItemAdd(inGSettings=inGSettings, inHostNameStr=inHostNameStr, inUserStr=inUserStr, inActivityItemDict=lActivityItemDict)

def AgentOSLogoff(inHostNameStr, inUserStr):
    """
    Logoff the agent user session

    :return: GUID String of the ActivityItem - you can wait (sync or async) result by this guid!
    """
    inGSettings = GSettingsGet()  # Set the global settings
    lCMDStr = "shutdown /l"
    lActivityItemDict = {
        "Def":"OSCMD", # def alias (look pyOpeRPA.Agent gSettings["ProcessorDict"]["AliasDefDict"])
        "ArgList":[], # Args list
        "ArgDict":{"inCMDStr":lCMDStr,"inRunAsyncBool":False, "inSendOutputToOrchestratorLogsBool": True, "inCMDEncodingStr": "cp1251"}, # Args dictionary
        "ArgGSettings": "inGSettings", # Name of GSettings attribute: str (ArgDict) or index (for ArgList)
        "ArgLogger": None # Name of GSettings attribute: str (ArgDict) or index (for ArgList)
    }
    #Send item in AgentDict for the futher data transmition
    return AgentActivityItemAdd(inGSettings=inGSettings, inHostNameStr=inHostNameStr, inUserStr=inUserStr, inActivityItemDict=lActivityItemDict)

def AgentOSFileSend(inHostNameStr, inUserStr, inOrchestratorFilePathStr, inAgentFilePathStr, inGSettings = None):
    """
   Send the file from the Orchestrator to Agent (synchroniously) pyOpenRPA.Agent daemon process (safe for JSON transmition).
   Work safety with big files
   Thread safe - you can call def even if you dont init the orchestrator - def will be executed later

    :param inGSettings: Global settings dict (singleton)
    :param inHostNameStr:
    :param inUserStr:
    :param inFilePathStr:
    :param inFileDataBytes:
    :return: GUID String of the ActivityItem - you can wait (sync or async) result by this guid!
    """

    inGSettings = GSettingsGet(inGSettings=inGSettings)  # Set the global settings
    # Check thread
    if  inGSettings["ServerDict"]["ServerThread"] is None:
        if inGSettings["Logger"]: inGSettings["Logger"].warning(f"AgentOSFileSend run before server init - activity will be append in the processor queue.")
        lResult = {
            "Def": AgentOSFileSend, # def link or def alias (look gSettings["Processor"]["AliasDefDict"])
            "ArgList": [],  # Args list
            "ArgDict": {"inHostNameStr":inHostNameStr, "inUserStr":inUserStr, "inOrchestratorFilePathStr":inOrchestratorFilePathStr, "inAgentFilePathStr": inAgentFilePathStr},  # Args dictionary
            "ArgGSettings": "inGSettings",  # Name of GSettings attribute: str (ArgDict) or index (for ArgList)
            "ArgLogger": None  # Name of GSettings attribute: str (ArgDict) or index (for ArgList)
        }
        inGSettings["ProcessorDict"]["ActivityList"].append(lResult)
    else: # In processor - do execution
        lActivityItemCheckIntervalSecFloat = inGSettings["ServerDict"]["AgentFileChunkCheckIntervalSecFloat"]

        # Get the chunk limit
        lChunkByteSizeInt = inGSettings["ServerDict"]["AgentFileChunkBytesSizeInt"]

        lL = inGSettings.get("Logger",None)

        # Open the file and get the size (in bytes)
        lFile = open(inOrchestratorFilePathStr,"rb")
        lFileSizeBytesInt = lFile.seek(0,2)
        lFile.seek(0)
        #import pdb
        #pdb.set_trace()
        lChunkCountInt = math.ceil(lFileSizeBytesInt/lChunkByteSizeInt)
        if lL: lL.info(f"O2A: Start to send binary file via chunks. Chunk count: {lChunkCountInt}, From (Orch side): {inOrchestratorFilePathStr}, To (Agent side): {inAgentFilePathStr}")
        for lChunkNumberInt in range(lChunkCountInt):
            # Read chunk
            lFileChunkBytes = lFile.read(lChunkByteSizeInt)
            # Convert to base64
            lFileChunkBase64Str = base64.b64encode(lFileChunkBytes).decode("utf-8")
            # Send chunk
            if lChunkNumberInt == 0:
                lActivityItemGUIDStr = AgentOSFileBinaryDataBase64StrCreate(inGSettings=inGSettings,inHostNameStr=inHostNameStr,
                                                     inUserStr=inUserStr,inFilePathStr=inAgentFilePathStr,
                                                     inFileDataBase64Str=lFileChunkBase64Str)
            else:
                lActivityItemGUIDStr = AgentOSFileBinaryDataBase64StrAppend(inGSettings=inGSettings, inHostNameStr=inHostNameStr,
                                                     inUserStr=inUserStr, inFilePathStr=inAgentFilePathStr,
                                                     inFileDataBase64Str=lFileChunkBase64Str)
            # Wait for the activity will be deleted
            while AgentActivityItemExists(inGSettings=inGSettings,inHostNameStr=inHostNameStr,inUserStr=inUserStr,inGUIDStr=lActivityItemGUIDStr):
                time.sleep(lActivityItemCheckIntervalSecFloat)
            if lL: lL.debug(
                    f"O2A: BINARY SEND: Current chunk index: {lChunkNumberInt}")
        if lL: lL.info(
            f"O2A: BINARY SEND: Transmition has been complete")
        # Close the file
        lFile.close()

def AgentOSFileBinaryDataBytesCreate(inHostNameStr, inUserStr, inFilePathStr, inFileDataBytes, inGSettings=None):
    """
    Create binary file by the base64 string by the pyOpenRPA.Agent daemon process (safe for JSON transmition)

    :param inGSettings: Global settings dict (singleton)
    :param inHostNameStr:
    :param inUserStr:
    :param inFilePathStr:
    :param inFileDataBytes:
    :return: GUID String of the ActivityItem - you can wait (sync or async) result by this guid!
    """
    inGSettings = GSettingsGet(inGSettings=inGSettings)  # Set the global settings
    lFileDataBase64Str = base64.b64encode(inFileDataBytes).decode("utf-8")
    lActivityItemDict = {
        "Def":"OSFileBinaryDataBase64StrCreate", # def alias (look pyOpeRPA.Agent gSettings["ProcessorDict"]["AliasDefDict"])
        "ArgList":[], # Args list
        "ArgDict":{"inFilePathStr":inFilePathStr,"inFileDataBase64Str":lFileDataBase64Str}, # Args dictionary
        "ArgGSettings": "inGSettings", # Name of GSettings attribute: str (ArgDict) or index (for ArgList)
        "ArgLogger": None # Name of GSettings attribute: str (ArgDict) or index (for ArgList)
    }
    #Send item in AgentDict for the futher data transmition
    return AgentActivityItemAdd(inGSettings=inGSettings, inHostNameStr=inHostNameStr, inUserStr=inUserStr, inActivityItemDict=lActivityItemDict)


def AgentOSFileBinaryDataBase64StrCreate(inHostNameStr, inUserStr, inFilePathStr, inFileDataBase64Str, inGSettings=None):
    """
    Create binary file by the base64 string by the pyOpenRPA.Agent daemon process (safe for JSON transmission)

    :param inGSettings: Global settings dict (singleton)
    :param inHostNameStr:
    :param inUserStr:
    :param inFilePathStr:
    :param inFileDataBase64Str:
    :return: GUID String of the ActivityItem - you can wait (sync or async) result by this guid!
    """
    inGSettings = GSettingsGet(inGSettings=inGSettings)  # Set the global settings
    lActivityItemDict = {
        "Def":"OSFileBinaryDataBase64StrCreate", # def alias (look pyOpeRPA.Agent gSettings["ProcessorDict"]["AliasDefDict"])
        "ArgList":[], # Args list
        "ArgDict":{"inFilePathStr":inFilePathStr,"inFileDataBase64Str":inFileDataBase64Str}, # Args dictionary
        "ArgGSettings": "inGSettings", # Name of GSettings attribute: str (ArgDict) or index (for ArgList)
        "ArgLogger": None # Name of GSettings attribute: str (ArgDict) or index (for ArgList)
    }
    #Send item in AgentDict for the futher data transmition
    return AgentActivityItemAdd(inGSettings=inGSettings, inHostNameStr=inHostNameStr, inUserStr=inUserStr, inActivityItemDict=lActivityItemDict)


def AgentOSFileBinaryDataBase64StrAppend(inHostNameStr, inUserStr, inFilePathStr, inFileDataBase64Str, inGSettings = None):
    """
    Append binary file by the base64 string by the pyOpenRPA.Agent daemon process (safe for JSON transmission)

    :param inGSettings: Global settings dict (singleton)
    :param inHostNameStr:
    :param inUserStr:
    :param inFilePathStr:
    :param inFileDataBase64Str:
    :return: GUID String of the ActivityItem - you can wait (sync or async) result by this guid!
    """
    inGSettings = GSettingsGet(inGSettings=inGSettings)  # Set the global settings
    lActivityItemDict = {
        "Def":"OSFileBinaryDataBase64StrAppend", # def alias (look pyOpeRPA.Agent gSettings["ProcessorDict"]["AliasDefDict"])
        "ArgList":[], # Args list
        "ArgDict":{"inFilePathStr":inFilePathStr,"inFileDataBase64Str":inFileDataBase64Str}, # Args dictionary
        "ArgGSettings": "inGSettings", # Name of GSettings attribute: str (ArgDict) or index (for ArgList)
        "ArgLogger": None # Name of GSettings attribute: str (ArgDict) or index (for ArgList)
    }
    #Send item in AgentDict for the futher data transmition
    return AgentActivityItemAdd(inGSettings=inGSettings, inHostNameStr=inHostNameStr, inUserStr=inUserStr, inActivityItemDict=lActivityItemDict)


# Send text file to Agent (string)
def AgentOSFileTextDataStrCreate(inHostNameStr, inUserStr, inFilePathStr, inFileDataStr, inEncodingStr = "utf-8",inGSettings=None):
    """
    Create text file by the string by the pyOpenRPA.Agent daemon process

    :param inGSettings: Global settings dict (singleton)
    :param inHostNameStr:
    :param inUserStr:
    :param inFilePathStr:
    :param inFileDataStr:
    :param inEncodingStr:
    :return: GUID String of the ActivityItem - you can wait (sync or async) result by this guid!
    """
    inGSettings = GSettingsGet(inGSettings=inGSettings)  # Set the global settings
    lActivityItemDict = {
        "Def":"OSFileTextDataStrCreate", # def alias (look pyOpeRPA.Agent gSettings["ProcessorDict"]["AliasDefDict"])
        "ArgList":[], # Args list
        "ArgDict":{"inFilePathStr":inFilePathStr,"inFileDataStr":inFileDataStr, "inEncodingStr": inEncodingStr}, # Args dictionary
        "ArgGSettings": "inGSettings", # Name of GSettings attribute: str (ArgDict) or index (for ArgList)
        "ArgLogger": None # Name of GSettings attribute: str (ArgDict) or index (for ArgList)
    }
    #Send item in AgentDict for the futher data transmition
    return AgentActivityItemAdd(inGSettings=inGSettings, inHostNameStr=inHostNameStr, inUserStr=inUserStr, inActivityItemDict=lActivityItemDict)

def AgentOSFileBinaryDataBase64StrReceive(inHostNameStr, inUserStr, inFilePathStr, inGSettings = None):
    """
    Read binary file and encode in base64 to transmit (safe for JSON transmition)

    :param inGSettings: Global settings dict (singleton)
    :param inHostNameStr:
    :param inUserStr:
    :param inFilePathStr: File path to read
    :return: GUID String of the ActivityItem - you can wait (sync or async) result by this guid!
    """
    inGSettings = GSettingsGet(inGSettings=inGSettings)  # Set the global settings
    lActivityItemDict = {
        "Def":"OSFileBinaryDataBase64StrReceive", # def alias (look pyOpeRPA.Agent gSettings["ProcessorDict"]["AliasDefDict"])
        "ArgList":[], # Args list
        "ArgDict":{"inFilePathStr":inFilePathStr}, # Args dictionary
        "ArgGSettings": "inGSettings", # Name of GSettings attribute: str (ArgDict) or index (for ArgList)
        "ArgLogger": None # Name of GSettings attribute: str (ArgDict) or index (for ArgList)
    }
    #Send item in AgentDict for the futher data transmition
    return AgentActivityItemAdd(inGSettings=inGSettings, inHostNameStr=inHostNameStr, inUserStr=inUserStr, inActivityItemDict=lActivityItemDict)


def AgentOSFileBinaryDataReceive(inHostNameStr, inUserStr, inFilePathStr):
    """
    Read binary file from agent (synchronious)

    :param inGSettings: Global settings dict (singleton)
    :param inHostNameStr:
    :param inUserStr:
    :param inFilePathStr: File path to read
    :return: file data bytes
    """
    lFileDataBytes = None
    inGSettings = GSettingsGet()  # Set the global settings
    # Check thread
    if  OrchestratorIsInited() == False:
        if inGSettings["Logger"]: inGSettings["Logger"].warning(f"AgentOSFileBinaryDataReceive run before orc init - activity will be append in the processor queue.")
        lResult = {
            "Def": AgentOSFileBinaryDataReceive, # def link or def alias (look gSettings["Processor"]["AliasDefDict"])
            "ArgList": [],  # Args list
            "ArgDict": {"inHostNameStr":inHostNameStr, "inUserStr":inUserStr, "inFilePathStr":inFilePathStr},  # Args dictionary
            "ArgGSettings": None,  # Name of GSettings attribute: str (ArgDict) or index (for ArgList)
            "ArgLogger": None  # Name of GSettings attribute: str (ArgDict) or index (for ArgList)
        }
        inGSettings["ProcessorDict"]["ActivityList"].append(lResult)
    else: # In processor - do execution
        lActivityItemDict = {
            "Def":"OSFileBinaryDataBase64StrReceive", # def alias (look pyOpeRPA.Agent gSettings["ProcessorDict"]["AliasDefDict"])
            "ArgList":[], # Args list
            "ArgDict":{"inFilePathStr":inFilePathStr}, # Args dictionary
            "ArgGSettings": "inGSettings", # Name of GSettings attribute: str (ArgDict) or index (for ArgList)
            "ArgLogger": None # Name of GSettings attribute: str (ArgDict) or index (for ArgList)
        }
        
        #Send item in AgentDict for the futher data transmition
        lGUIDStr = AgentActivityItemAdd(inGSettings=inGSettings, inHostNameStr=inHostNameStr, inUserStr=inUserStr, inActivityItemDict=lActivityItemDict)
        lFileBase64Str = AgentActivityItemReturnGet(inGUIDStr=lGUIDStr)
        if lFileBase64Str is not None: lFileDataBytes = base64.b64decode(lFileBase64Str)
        return lFileDataBytes

def AgentOSFileTextDataStrReceive(inHostNameStr, inUserStr, inFilePathStr, inEncodingStr="utf-8", inGSettings = None):
    """
    Read text file in the agent GUI session

    :param inGSettings: Global settings dict (singleton)
    :param inHostNameStr:
    :param inUserStr:
    :param inFilePathStr: File path to read
    :param inEncodingStr: Text file encoding. Default 'utf-8'
    :return: GUID String of the ActivityItem - you can wait (sync or async) result by this guid!
    """
    inGSettings = GSettingsGet(inGSettings=inGSettings)  # Set the global settings
    lActivityItemDict = {
        "Def":"OSFileTextDataStrReceive", # def alias (look pyOpeRPA.Agent gSettings["ProcessorDict"]["AliasDefDict"])
        "ArgList":[], # Args list
        "ArgDict":{"inFilePathStr":inFilePathStr, "inEncodingStr": inEncodingStr}, # Args dictionary
        "ArgGSettings": "inGSettings", # Name of GSettings attribute: str (ArgDict) or index (for ArgList)
        "ArgLogger": None # Name of GSettings attribute: str (ArgDict) or index (for ArgList)
    }
    #Send item in AgentDict for the futher data transmition
    return AgentActivityItemAdd(inGSettings=inGSettings, inHostNameStr=inHostNameStr, inUserStr=inUserStr, inActivityItemDict=lActivityItemDict)

def AgentProcessWOExeUpperUserListGet(inHostNameStr, inUserStr, inGSettings = None):
    """
    Return the process list only for the current user (where Agent is running) without .EXE in upper case. Can use in ActivityItem from Orchestrator to Agent

    :param inGSettings: Global settings dict (singleton)
    :param inHostNameStr:
    :param inUserStr:
    :return: GUID String of the ActivityItem - you can wait (sync or async) result by this guid!
    """
    inGSettings = GSettingsGet(inGSettings=inGSettings)  # Set the global settings
    lActivityItemDict = {
        "Def":"ProcessWOExeUpperUserListGet", # def alias (look pyOpeRPA.Agent gSettings["ProcessorDict"]["AliasDefDict"])
        "ArgList":[], # Args list
        "ArgDict":{}, # Args dictionary
        "ArgGSettings": "inGSettings", # Name of GSettings attribute: str (ArgDict) or index (for ArgList)
        "ArgLogger": None # Name of GSettings attribute: str (ArgDict) or index (for ArgList)
    }
    #Send item in AgentDict for the futher data transmition
    return AgentActivityItemAdd(inGSettings=inGSettings, inHostNameStr=inHostNameStr, inUserStr=inUserStr, inActivityItemDict=lActivityItemDict)

# OS DEFS

def OSLogoff():
    """
    Logoff the current orchestrator session
    :return:
    """
    os.system("shutdown /l")

def OSCredentialsVerify(inUserStr, inPasswordStr, inDomainStr=""): ##
    """
    Verify user credentials in windows. Return bool

    :param inUserStr:
    :param inPasswordStr:
    :param inDomainStr:
    :return: True - Credentials are actual; False - Credentials are not actual
    """
    try:
        hUser = win32security.LogonUser(
            inUserStr,inDomainStr, inPasswordStr,
            win32security.LOGON32_LOGON_NETWORK, win32security.LOGON32_PROVIDER_DEFAULT
        )
    except win32security.error:
        return False
    else:
        return True

def OSRemotePCRestart(inHostStr, inForceBool=True, inLogger = None):
    """
    Send signal via power shell to restart remote PC
    ATTENTION: Orchestrator user need to have restart right on the Remote machine to restart PC.

    :param inLogger: logger to log powershell result in logs
    :param inHostStr: PC hostname which you need to restart.
    :param inForceBool: True - send signal to force retart PC; False - else case
    :return:
    """
    if inLogger is None: inLogger = OrchestratorLoggerGet()
    lCMDStr = f"powershell -Command Restart-Computer -ComputerName {inHostStr}"
    if inForceBool == True: lCMDStr = lCMDStr + " -Force"
    OSCMD(inCMDStr=lCMDStr,inLogger=inLogger)

def OSCMD(inCMDStr, inRunAsyncBool=True, inLogger = None):
    """
    OS send command in shell locally

    :param inCMDStr:
    :param inRunAsyncBool:
    :param inLogger:
    :return: CMD result string
    """
    if inLogger is None: inLogger = OrchestratorLoggerGet()
    lResultStr = ""
    # New feature
    if inRunAsyncBool == True:
        inCMDStr = f"start {inCMDStr}"
    # Subdef to listen OS result
    def _CMDRunAndListenLogs(inCMDStr, inLogger):
        lResultStr = ""
        lOSCMDKeyStr = str(uuid.uuid4())[0:4].upper()
        lCMDProcess = subprocess.Popen(f'cmd /c {inCMDStr}', stdout=subprocess.PIPE, stderr=subprocess.STDOUT, creationflags=CREATE_NEW_CONSOLE)
        if inLogger:
            lListenBool = True
            inLogger.info(f"{lOSCMDKeyStr}: # # # # CMD Process has been STARTED # # # # ")
            inLogger.info(f"{lOSCMDKeyStr}: {inCMDStr}")
            while lListenBool:
                lOutputLineBytes = lCMDProcess.stdout.readline()
                if lOutputLineBytes == b"":
                    lListenBool = False
                lStr = lOutputLineBytes.decode('cp866')
                if lStr.endswith("\n"): lStr = lStr[:-1]
                inLogger.info(f"{lOSCMDKeyStr}: {lStr}")
                lResultStr+=lStr
            inLogger.info(f"{lOSCMDKeyStr}: # # # # CMD Process has been FINISHED # # # # ")
        return lResultStr
    # New call
    if inRunAsyncBool:
        lThread = threading.Thread(target=_CMDRunAndListenLogs, kwargs={"inCMDStr":inCMDStr, "inLogger":inLogger})
        lThread.start()
        lResultStr="ActivityList has been started in async mode - no output is available here."
    else:
        lResultStr = _CMDRunAndListenLogs(inCMDStr=inCMDStr, inLogger=inLogger)
    #lCMDCode = "cmd /c " + inCMDStr
    #subprocess.Popen(lCMDCode)
    #lResultCMDRun = 1  # os.system(lCMDCode)
    return lResultStr

def OrchestratorRestart(inGSettings=None):
    """
    Orchestrator restart

    :param inGSettings: Global settings dict (singleton)
    """
    inGSettings = GSettingsGet(inGSettings=inGSettings)  # Set the global settings
    OrchestratorSessionSave(inGSettings=inGSettings) # Dump RDP List in file json
    if inGSettings is not None:
        lL = inGSettings["Logger"]
        if lL: lL.info(f"Do restart")
    # Restart session
    os.execl(sys.executable, os.path.abspath(__file__), *sys.argv)
    sys.exit(0)

def OrchestratorLoggerGet() -> logging.Logger:
    """
    Get the logger from the Orchestrator

    :return:
    """
    return GSettingsGet().get("Logger",None)


def OrchestratorScheduleGet() -> schedule:
    """
    Get the schedule (schedule.readthedocs.io) from the Orchestrator

    Fro example you can use:

    .. code-block:: python
        # One schedule threaded
        Orchestrator.OrchestratorScheduleGet().every(5).seconds.do(lProcess.StatusCheckStart)

        #New schedule thread # See def description Orchestrator.OrchestratorThreadStart
        Orchestrator.OrchestratorScheduleGet().every(5).seconds.do(Orchestrator.OrchestratorThreadStart,lProcess.StatusCheckStart)

    :return: schedule module. Example see here https://schedule.readthedocs.io/en/stable/examples.html
    """
    if GSettingsGet().get("SchedulerDict",{}).get("Schedule",None) is None:
        GSettingsGet()["SchedulerDict"]["Schedule"]=schedule
    return GSettingsGet().get("SchedulerDict",{}).get("Schedule",None)

def OrchestratorThreadStart(inDef, *inArgList, **inArgDict):
    """
    Execute def in new thread and pass some args with list and dict types

    :param inDef: Python Def
    :param inArgList: args as list
    :param inArgDict: args as dict
    :return: threading.Thread object
    """
    lDefThread = threading.Thread(target=inDef,args=inArgList,kwargs=inArgDict)
    lDefThread.start()
    return lDefThread

def OrchestratorIsAdmin():
    """
    Check if Orchestrator process is running as administrator

    :return: True - run as administrator; False - not as administrator
    """
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def OrchestratorIsInited() -> bool:
    """Check if Orchestrator initial actions were processed

    :return: True - orc is already inited; False - else
    :rtype: bool
    """    

    return Core.IsOrchestratorInitialized(inGSettings=GSettingsGet())

def OrchestratorInitWait() -> None:
    """Wait thread while orc will process initial action. 
    ATTENTION: DO NOT CALL THIS DEF IN THREAD WHERE ORCHESTRATOR MUST BE INITIALIZED - INFINITE LOOP
    """
    lIntervalSecFloat = 0.5
    while not OrchestratorIsInited():
        time.sleep(lIntervalSecFloat)
    

def OrchestratorRerunAsAdmin():
    """
    Check if not admin - then rerun orchestrator as administrator

    :return: True - run as administrator; False - not as administrator
    """
    if not OrchestratorIsAdmin():
        # Re-run the program with admin rights
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
    else:
        print(f"!SKIPPED! Already run as administrator!")

def OrchestratorPySearchInit(inGlobPatternStr, inDefStr = None, inDefArgNameGSettingsStr = None, inAsyncInitBool = False):
    """
    Search the py files by the glob and do the safe init (in try except). Also add inited module in sys.modules as imported (module name = file name without extension).
    You can init CP in async way!
    .. code-block:: python

        # USAGE VAR 1 (without the def  auto call)
        # Autoinit control panels starts with CP_
        Orchestrator.OrchestratorPySearchInit(inGlobPatternStr="ControlPanel\\CP_*.py")

        # USAGE VAR 2 (with the def auto call) - for the backward compatibility CP for the Orchestrator ver. < 1.2.7
        # Autoinit control panels starts with CP_
        Orchestrator.OrchestratorPySearchInit(inGlobPatternStr="ControlPanel\\CP_*.py", inDefStr="SettingsUpdate", inDefArgNameGSettingsStr="inGSettings")

        # INFO: The code above will replace the code below
        ## !!! For Relative import !!! CP Version Check
        try:
            sys.path.insert(0,os.path.abspath(os.path.join(r"")))
            from ControlPanel import CP_VersionCheck
            CP_VersionCheck.SettingsUpdate(inGSettings=gSettings)
        except Exception as e:
            gSettings["Logger"].exception(f"Exception when init CP. See below.")


    :param inGlobPatternStr: example"..\\*\\*\\*X64*.cmd"
    :param inDefStr: OPTIONAL The string name of the def. For backward compatibility if you need to auto call some def from initialized module
    :param inDefArgNameGSettingsStr: OPTIONAL The name of the GSettings argument in def (if exists)
    :param inAsyncInitBool: OPTIONAL True - init py modules in many threads - parallel execution. False (default) - sequence execution
    :return: { "ModuleNameStr":{"PyPathStr": "", "Module": ...},  ...}
    """

    # # # # # # # #
    def __execute__(inResultDict, inPyPathItemStr, inDefStr = None, inDefArgNameGSettingsStr = None):
        try:
            lPyPathItemStr = inPyPathItemStr
            lModuleNameStr = os.path.basename(lPyPathItemStr)[0:-3]
            lTechSpecification = importlib.util.spec_from_file_location(lModuleNameStr, lPyPathItemStr)
            lTechModuleFromSpec = importlib.util.module_from_spec(lTechSpecification)
            sys.modules[lModuleNameStr] = lTechModuleFromSpec  # Add initialized module in sys - python will not init this module enought
            lTechSpecificationModuleLoader = lTechSpecification.loader.exec_module(lTechModuleFromSpec)
            lItemDict = {"ModuleNameStr": lModuleNameStr, "PyPathStr": lPyPathItemStr, "Module": lTechModuleFromSpec}
            if lL: lL.info(f"Py module {lModuleNameStr} has been successfully initialized.")
            inResultDict[lModuleNameStr]=lItemDict
            # Backward compatibility to call def with gsettings when init
            if inDefStr is not None and inDefStr is not "":
                lDef = getattr(lTechModuleFromSpec, inDefStr)
                lArgDict = {}
                if inDefArgNameGSettingsStr is not None and inDefArgNameGSettingsStr is not "":
                    lArgDict = {inDefArgNameGSettingsStr:GSettingsGet()}
                lDef(**lArgDict)
        except Exception as e:
            if lL: lL.exception(f"Exception when init the .py file {os.path.abspath(lPyPathItemStr)}")
    # # # # # # # #

    lResultDict = {}

    lPyPathStrList = glob.glob(inGlobPatternStr) # get the file list
    lL = OrchestratorLoggerGet() # get the logger
    for lPyPathItemStr in lPyPathStrList:
        if inAsyncInitBool == True:
            # ASYNC EXECUTION
            lThreadInit = threading.Thread(target=__execute__,kwargs={
                "inResultDict":lResultDict, "inPyPathItemStr": lPyPathItemStr, 
                "inDefStr": inDefStr, "inDefArgNameGSettingsStr": inDefArgNameGSettingsStr}, daemon=True)
            lThreadInit.start()
        else:
            # SYNC EXECUTION
            __execute__(inResultDict=lResultDict, inPyPathItemStr=lPyPathItemStr, inDefStr = inDefStr, inDefArgNameGSettingsStr = inDefArgNameGSettingsStr)
    return lResultDict

def OrchestratorSessionSave(inGSettings=None):
    """
    Orchestrator session save in file
    (from version 1.2.7)
        _SessionLast_GSettings.pickle (binary)

    (above the version 1.2.7)
        _SessionLast_RDPList.json (encoding = "utf-8")
        _SessionLast_StorageDict.pickle (binary)

    :param inGSettings: Global settings dict (singleton)
    :return: True every time
    """
    inGSettings = GSettingsGet(inGSettings=inGSettings)  # Set the global settings
    lL = inGSettings["Logger"]
    try:
        # Dump RDP List in file json
        #lFile = open("_SessionLast_RDPList.json", "w", encoding="utf-8")
        #lFile.write(json.dumps(inGSettings["RobotRDPActive"]["RDPList"]))  # dump json to file
        #lFile.close()  # Close the file
        #if inGSettings is not None:
        #    if lL: lL.info(
        #        f"Orchestrator has dump the RDP list before the restart.")
        ## _SessionLast_StorageDict.pickle (binary)
        #if "StorageDict" in inGSettings:
        #    with open('_SessionLast_StorageDict.pickle', 'wb') as lFile:
        #        pickle.dump(inGSettings["StorageDict"], lFile)
        #        if lL: lL.info(
        #            f"Orchestrator has dump the StorageDict before the restart.")

        #SessionLast
        lDumpDict = {"StorageDict":inGSettings["StorageDict"], "ManagersProcessDict":inGSettings["ManagersProcessDict"],
                     "RobotRDPActive":{"RDPList": inGSettings["RobotRDPActive"]["RDPList"]}}
        with open('_SessionLast_GSettings.pickle', 'wb') as lFile:
            pickle.dump(lDumpDict, lFile)
            if lL: lL.info(
                f"Orchestrator has dump the GSettings (new dump mode from v1.2.7) before the restart.")

    except Exception as e:
        if lL: lL.exception(f"Exception when dump data before restart the Orchestrator")
    return True

def OrchestratorSessionRestore(inGSettings=None):
    """
    Check _SessioLast... files in working directory. if exist - load into gsettings
    (from version 1.2.7)
        _SessionLast_GSettings.pickle (binary)

    (above the version 1.2.7)
        _SessionLast_RDPList.json (encoding = "utf-8")
        _SessionLast_StorageDict.pickle (binary)

    :param inGSettings: Global settings dict (singleton)
    :return:
    """
    inGSettings = GSettingsGet(inGSettings=inGSettings)  # Set the global settings
    lL = inGSettings.get("Logger",None)
    # _SessionLast_RDPList.json (encoding = "utf-8")
    if os.path.exists("_SessionLast_RDPList.json"):
        lFile = open("_SessionLast_RDPList.json", "r", encoding="utf-8")
        lSessionLastRDPList = json.loads(lFile.read())
        lFile.close()  # Close the file
        os.remove("_SessionLast_RDPList.json")  # remove the temp file
        inGSettings["RobotRDPActive"]["RDPList"] = lSessionLastRDPList  # Set the last session dict
        if lL: lL.warning(f"RDP Session List was restored from previous Orchestrator session")
    # _SessionLast_StorageDict.pickle (binary)
    if os.path.exists("_SessionLast_StorageDict.pickle"):
        if "StorageDict" not in inGSettings:
            inGSettings["StorageDict"] = {}
        with open('_SessionLast_StorageDict.pickle', 'rb') as lFile:
            lStorageDictDumpDict = pickle.load(lFile)
            Server.__ComplexDictMerge2to1Overwrite__(in1Dict=inGSettings["StorageDict"],
                                                     in2Dict=lStorageDictDumpDict)  # Merge dict 2 into dict 1
            if lL: lL.warning(f"StorageDict was restored from previous Orchestrator session")
        os.remove("_SessionLast_StorageDict.pickle")  # remove the temp file
    # _SessionLast_Gsettings.pickle (binary)
    if os.path.exists("_SessionLast_GSettings.pickle"):
        if "StorageDict" not in inGSettings:
            inGSettings["StorageDict"] = {}
        if "ManagersProcessDict" not in inGSettings:
            inGSettings["ManagersProcessDict"] = {}
        with open('_SessionLast_GSettings.pickle', 'rb') as lFile:
            lStorageDictDumpDict = pickle.load(lFile)
            Server.__ComplexDictMerge2to1Overwrite__(in1Dict=inGSettings,
                                                     in2Dict=lStorageDictDumpDict)  # Merge dict 2 into dict 1
            if lL: lL.warning(f"GSettings was restored from previous Orchestrator session")
        os.remove("_SessionLast_GSettings.pickle")  # remove the temp file

def UACKeyListCheck(inRequest, inRoleKeyList) -> bool:
    """
    Check is client is has access for the key list

    :param inRequest: request handler (from http.server import BaseHTTPRequestHandler)
    :param inRoleKeyList:
    :return: bool
    """
    return inRequest.UACClientCheck(inRoleKeyList=inRoleKeyList)

def UACUserDictGet(inRequest) -> dict:
    """
    Return user UAC hierarchy dict of the inRequest object. Empty dict - superuser access

    :param inRequest: request handler (from http.server import BaseHTTPRequestHandler)
    :return: user UAC hierarchy dict
    """
    return inRequest.UserRoleHierarchyGet() # get the Hierarchy

def UACUpdate(inADLoginStr, inADStr="", inADIsDefaultBool=True, inURLList=None, inRoleHierarchyAllowedDict=None, inGSettings = None):
    """
    Update user access (UAC)

    :param inGSettings: Global settings dict (singleton)
    :param inADLoginStr:
    :param inADStr:
    :param inADIsDefaultBool:
    :param inURLList:
    :param inRoleHierarchyAllowedDict:
    """
    inGSettings = GSettingsGet(inGSettings=inGSettings)  # Set the global settings
    lUserTurple = (inADStr.upper(),inADLoginStr.upper()) # Create turple key for inGSettings["ServerDict"]["AccessUsers"]["RuleDomainUserDict"]
    if inURLList is None: inURLList = [] # Check if None
    if inRoleHierarchyAllowedDict is None: inRoleHierarchyAllowedDict = {} # Check if None
    # Get the old URLList
    try:
        inURLList += inGSettings["ServerDict"]["AccessUsers"]["RuleDomainUserDict"][lUserTurple]["MethodMatchURLBeforeList"]
    except:
        pass
    # Check RoleHierarchyAllowedDict in gSettings for the old role hierarchy - include in result.
    if lUserTurple in inGSettings["ServerDict"]["AccessUsers"]["RuleDomainUserDict"] and "RoleHierarchyAllowedDict" in inGSettings["ServerDict"]["AccessUsers"]["RuleDomainUserDict"][lUserTurple]:
        lRoleHierarchyAllowedOLDDict = inGSettings["ServerDict"]["AccessUsers"]["RuleDomainUserDict"][lUserTurple]["RoleHierarchyAllowedDict"]
        Server.__ComplexDictMerge2to1__(in1Dict=inRoleHierarchyAllowedDict, in2Dict=lRoleHierarchyAllowedOLDDict) # Merge dict 2 into dict 1

    # Create Access item
    lRuleDomainUserDict = {
        "MethodMatchURLBeforeList": inURLList,
        "RoleHierarchyAllowedDict": inRoleHierarchyAllowedDict
    }
    # Case add domain + user
    inGSettings["ServerDict"]["AccessUsers"]["RuleDomainUserDict"].update({(inADStr.upper(),inADLoginStr.upper()):lRuleDomainUserDict})
    if inADIsDefaultBool:
        # Case add default domain + user
        inGSettings["ServerDict"]["AccessUsers"]["RuleDomainUserDict"].update({("",inADLoginStr.upper()):lRuleDomainUserDict})

def UACSuperTokenUpdate(inSuperTokenStr, inGSettings=None):
    """
    Add supertoken for the all access (it is need for the robot communication without human)

    :param inGSettings: Global settings dict (singleton)
    :param inSuperTokenStr:
    """
    inGSettings = GSettingsGet(inGSettings=inGSettings)  # Set the global settings
    lLoginStr = "SUPERTOKEN"
    UACUpdate(inGSettings=inGSettings, inADLoginStr=lLoginStr)
    inGSettings["ServerDict"]["AccessUsers"]["AuthTokensDict"].update(
        {inSuperTokenStr:{"User":lLoginStr, "Domain":"", "TokenDatetime":  datetime.datetime.now(), "FlagDoNotExpire":True}}
    )

# # # # # # # # # # # # # # # # # # # # # # #
# OrchestratorWeb defs
# # # # # # # # # # # # # # # # # # # # # # #

def WebURLIndexChange(inURLIndexStr:str ="/"):
    """Change the index page of the orchestrator if you dont want the '/' (main) path

    :param inURLIndexStr: New url for the index page of the orchestrator, defaults to "/"
    :type inURLIndexStr: str, optional
    """
    GSettingsGet()["ServerDict"]["URLIndexStr"] = inURLIndexStr

def WebURLConnectDef(inMethodStr, inURLStr, inMatchTypeStr, inDef, inContentTypeStr="application/octet-stream", inGSettings = None, inUACBool = None):
    """
     Connect URL to DEF
        "inMethodStr":"GET|POST",
        "inURLStr": "/index", #URL of the request
        "inMatchTypeStr": "", #"BeginWith|Contains|Equal|EqualCase",
        "inContentTypeStr": "", #HTTP Content-type
        "inDef": None #Function with str result

    :param inGSettings: Global settings dict (singleton)
    :param inMethodStr: "GET|POST",
    :param inURLStr: example "/index", #URL of the request
    :param inMatchTypeStr: #"BeginWith|Contains|Equal|EqualCase",
    :param inDef: def arg allowed list: 2:[inRequest, inGSettings], 1: [inRequest], 0: []
    :param inContentTypeStr: default: "application/octet-stream"
    :param inUACBool: default: None; True - check user access before do this URL item. None - get Server flag if ask user
    """
    inGSettings = GSettingsGet(inGSettings=inGSettings)  # Set the global settings
    lURLItemDict = {
        "Method": inMethodStr.upper(),
        "URL": inURLStr,  # URL of the request
        "MatchType": inMatchTypeStr,  # "BeginWith|Contains|Equal|EqualCase",
        # "ResponseFilePath": "", #Absolute or relative path
        #"ResponseFolderPath": "C:\Abs\Archive\scopeSrcUL\OpenRPA\Orchestrator\Settings",
        # Absolute or relative path
        "ResponseContentType": inContentTypeStr, #HTTP Content-type
        "ResponseDefRequestGlobal": inDef, #Function with str result
        "UACBool": inUACBool
    }
    inGSettings["ServerDict"]["URLList"].append(lURLItemDict)


def WebURLConnectFolder(inMethodStr, inURLStr, inMatchTypeStr, inFolderPathStr, inGSettings = None, inUACBool = None, inUseCacheBool= False):
    """
    Connect URL to Folder
        "inMethodStr":"GET|POST",
        "inURLStr": "/Folder/", #URL of the request
        "inMatchTypeStr": "", #"BeginWith|Contains|Equal|EqualCase",
        "inFolderPathStr": "", #Absolute or relative path
        "inUACBool"

    :param inGSettings: Global settings dict (singleton)
    :param inMethodStr:
    :param inURLStr:
    :param inMatchTypeStr:
    :param inFolderPathStr:
    :param inUACBool: default: None; True - check user access before do this URL item. None - get Server flag if ask user
    :param inUseCacheBool: True - cache this page - dont open ever
    """
    inGSettings = GSettingsGet(inGSettings=inGSettings)  # Set the global settings
    # Check if last symbol is "/" - append if not exist
    lFolderPathStr = os.path.abspath(inFolderPathStr)
    if lFolderPathStr[-1]!="/":lFolderPathStr+="/"
    # Prepare URLItem
    lURLItemDict = {
        "Method": inMethodStr.upper(),
        "URL": inURLStr,  # URL of the request
        "MatchType": inMatchTypeStr,  # "BeginWith|Contains|Equal|EqualCase",
        # "ResponseFilePath": "", #Absolute or relative path
        "ResponseFolderPath": lFolderPathStr, # Absolute or relative path
        "ResponseContentType": None, #HTTP Content-type
        #"ResponseDefRequestGlobal": inDef #Function with str result
        "UACBool": inUACBool,
        "UseCacheBool": inUseCacheBool
    }
    inGSettings["ServerDict"]["URLList"].append(lURLItemDict)


def WebURLConnectFile(inMethodStr, inURLStr, inMatchTypeStr, inFilePathStr, inContentTypeStr=None, inGSettings = None, inUACBool = None, inUseCacheBool = False):
    """
    Connect URL to File
        "inMethodStr":"GET|POST",
        "inURLStr": "/index", #URL of the request
        "inMatchTypeStr": "", #"BeginWith|Contains|Equal|EqualCase",
        "inFolderPathStr": "", #Absolute or relative path

    :param inGSettings: Global settings dict (singleton)
    :param inMethodStr:
    :param inURLStr:
    :param inMatchTypeStr:
    :param inFilePathStr:
    :param inContentTypeStr: If none - autodetect
    :param inUACBool: default: None; True - check user access before do this URL item. None - get Server flag if ask user
    :param inUseCacheBool: True - cache this page - dont open ever
    """
    inGSettings = GSettingsGet(inGSettings=inGSettings)  # Set the global settings
    lURLItemDict = {
        "Method": inMethodStr.upper(),
        "URL": inURLStr,  # URL of the request
        "MatchType": inMatchTypeStr,  # "BeginWith|Contains|Equal|EqualCase",
        "ResponseFilePath": os.path.abspath(inFilePathStr), #Absolute or relative path
        #"ResponseFolderPath": os.path.abspath(inFilePathStr), # Absolute or relative path
        "ResponseContentType": inContentTypeStr, #HTTP Content-type
        #"ResponseDefRequestGlobal": inDef #Function with str result
        "UACBool":inUACBool,
        "UseCacheBool": inUseCacheBool
    }
    inGSettings["ServerDict"]["URLList"].append(lURLItemDict)

def WebListenCreate(inServerKeyStr="Default", inAddressStr="", inPortInt=80, inCertFilePEMPathStr=None, inKeyFilePathStr=None, inGSettings = None):
    """
    Create listen interface for the web server

    :param inGSettings:  Global settings dict (singleton)
    :param inAddressStr: IP interface to listen
    :param inPortInt: Port int to listen for HTTP default is 80; for HTTPS default is 443
    :param inCertFilePEMPathStr: Path to .pem (base 64) certificate. Required for SSL connection. ATTENTION - do not use certificate with password
    :param inKeyFilePathStr: Path to the private key file
    :return: 
    """
    inGSettings = GSettingsGet(inGSettings=inGSettings)  # Set the global settings
    inGSettings["ServerDict"]["ListenDict"][inServerKeyStr]={
        "AddressStr":inAddressStr,
        "PortInt":inPortInt,
        "CertFilePEMPathStr":inCertFilePEMPathStr,
        "KeyFilePathStr":inKeyFilePathStr,
        "ServerInstance": None
    }


def WebCPUpdate(inCPKeyStr, inHTMLRenderDef=None, inJSONGeneratorDef=None, inJSInitGeneratorDef=None, inGSettings = None):
    """
    Add control panel HTML, JSON generator or JS when page init

    :param inGSettings: Global settings dict (singleton)
    :param inCPKeyStr:
    :param inHTMLRenderDef:
    :param inJSONGeneratorDef:
    :param inJSInitGeneratorDef:
    """
    lCPManager = Managers.ControlPanel(inControlPanelNameStr=inCPKeyStr, inRefreshHTMLJinja2TemplatePathStr=None)
    # CASE HTMLRender
    if inHTMLRenderDef is not None: lCPManager.mBackwardCompatibilityHTMLDef = inHTMLRenderDef
    # CASE JSONGenerator
    if inJSONGeneratorDef is not None: lCPManager.mBackwardCompatibilityJSONDef = inJSONGeneratorDef
    # CASE JSInitGeneratorDef
    if inJSInitGeneratorDef is not None: lCPManager.mBackwardCompatibilityJSDef = inJSInitGeneratorDef


def WebAuditMessageCreate(inRequest=None, inOperationCodeStr="-", inMessageStr="-"):
    """
    Create message string with request user details (IP, Login etc...). Very actual for IT security in big company.

    .. code-block:: python

        # USAGE
        from pyOpenRPA import Orchestrator

        lWebAuditMessageStr = Orchestrator.WebAuditMessageCreate(
            inRequest = lRequest,
            inOperationCodeStr = "OP_CODE_1",
            inMessageStr="Success"):

        # Log the WebAudit message
        lLogger.info(lWebAuditMessageStr)

    :param inRequest: HTTP request handler. Optional if call def from request thread
    :param inOperationCodeStr: operation code in string format (actual for IT audit in control panels)
    :param inMessageStr: additional message after
    :return: format "WebAudit :: DOMAIN\\USER@101.121.123.12 :: operation code :: message"
    """
    try:
        if inRequest is None: inRequest = WebRequestGet()
        lClientIPStr = inRequest.client_address[0]
        lUserDict = WebUserInfoGet(inRequest=inRequest)
        lDomainUpperStr = lUserDict["DomainUpperStr"]
        lUserLoginStr = lUserDict["UserNameUpperStr"]
        lResultStr = f"WebAudit :: {lDomainUpperStr}\\\\{lUserLoginStr}@{lClientIPStr} :: {inOperationCodeStr} :: {inMessageStr}"
    except Exception as e:
        print(str(e)) # Has no logger - must be dead alg branch
        lResultStr = inMessageStr
    return lResultStr

def WebRequestParseBodyBytes(inRequest=None):
    """
    Extract the body in bytes from the request

    :param inRequest: inRequest from the server. Optional if call def from request thread
    :return: Bytes or None
    """
    if inRequest is None: inRequest = WebRequestGet()
    lBodyBytes=None
    if inRequest.headers.get('Content-Length') is not None:
        lInputByteArrayLength = int(inRequest.headers.get('Content-Length'))
        lBodyBytes = inRequest.rfile.read(lInputByteArrayLength)
    return lBodyBytes

def WebRequestParseBodyStr(inRequest=None):
    """
    Extract the body in str from the request

    :param inRequest: inRequest from the server. Optional if call def from request thread
    :return: str or None
    """
    if inRequest is None: inRequest = WebRequestGet()
    return WebRequestParseBodyBytes(inRequest=inRequest).decode('utf-8')

def WebRequestParseBodyJSON(inRequest=None):
    """
    Extract the body in dict/list from the request

    :param inRequest: inRequest from the server. Optional if call def from request thread
    :return: dict or list
    """
    if inRequest is None: inRequest = WebRequestGet()
    return json.loads(WebRequestParseBodyStr(inRequest=inRequest))

def WebRequestParsePath(inRequest=None):
    """
    Parse the request - extract the url. Example: /pyOpenRPA/Debugging/DefHelper/...

    :param inRequest: inRequest from the server. Optional if call def from request thread
    :return: Str, Example: /pyOpenRPA/Debugging/DefHelper/...
    """
    if inRequest is None: inRequest = WebRequestGet()
    return urllib.parse.unquote(inRequest.path)

def WebRequestParseFile(inRequest=None):
    """
    Parse the request - extract the file (name, body in bytes)

    :param inRequest: inRequest from the server. Optional if call def from request thread
    :return: (FileNameStr, FileBodyBytes) or (None, None)
    """
    if inRequest is None: inRequest = WebRequestGet()
    lResultTurple=(None,None)
    if inRequest.headers.get('Content-Length') is not None:
        lInputByteArray = WebRequestParseBodyBytes(inRequest=inRequest)
        #print(f"BODY:ftInputByteArrayl")
        # Extract bytes data
        lBoundaryStr = str(inRequest.headers.get('Content-Type'))
        lBoundaryStr = lBoundaryStr[lBoundaryStr.index("boundary=")+9:] # get the boundary key #print(LBoundoryStr)
        lSplit = lInputByteArray.split('\r\n\r\n')
        lDelimiterRNRNIndex = lInputByteArray.index(b'\r\n\r\n') #print(LSplit) # Get file name
        lSplit0 = lInputByteArray[:lDelimiterRNRNIndex].split(b'\r\n')[1]
        lFileNameBytes = lSplit0[lSplit0.index(b'filename="')+10:-1]
        lFileNameStr = lFileNameBytes.decode("utf-8")
        # File data bytes
        lFileDataBytes = lInputByteArray[lDelimiterRNRNIndex+4:]
        lFileDataBytes = lFileDataBytes[:lFileDataBytes.index(b"\r\n--"+lBoundaryStr.encode("utf-8"))]
        lResultTurple = (lFileNameStr, lFileDataBytes)

    return lResultTurple

def WebRequestResponseSend(inResponeStr, inRequest=None):
    """
    Send response for the request

    :param inRequest: inRequest from the server. Optional if call def from request thread
    :return:
    """
    if inRequest is None: inRequest = WebRequestGet()
    inRequest.OpenRPAResponseDict["Body"] = bytes(inResponeStr, "utf8")


def WebRequestGet():
    """
    Return the web request instance if current thread was created by web request from client. else return None

    """
    lCurrentThread = threading.current_thread()
    if hasattr(lCurrentThread, "request"):
        return lCurrentThread.request

def WebUserInfoGet(inRequest=None):
    """
    Return User info about request

    :param inRequest: inRequest from the server. Optional if call def from request thread
    :return: {"DomainUpperStr": "", "UserNameUpperStr": ""}
    """
    if inRequest is None: inRequest = WebRequestGet()
    lDomainUpperStr = inRequest.OpenRPA["Domain"].upper()
    lUserUpperStr = inRequest.OpenRPA["User"].upper()
    return {"DomainUpperStr": lDomainUpperStr, "UserNameUpperStr": lUserUpperStr}

def WebUserIsSuperToken(inRequest = None, inGSettings = None):
    """
    Return bool if request is authentificated with supetoken (token which is never expires)

    :param inRequest: inRequest from the server. Optional if call def from request thread
    :param inGSettings: Global settings dict (singleton)
    :return: bool True - is supertoken; False - is not supertoken
    """
    if inRequest is None: inRequest = WebRequestGet()
    inGSettings = GSettingsGet(inGSettings=inGSettings)  # Set the global settings
    lIsSuperTokenBool = False
    # Get Flag is supertoken (True|False)
    lIsSuperTokenBool = inGSettings.get("ServerDict", {}).get("AccessUsers", {}).get("AuthTokensDict", {}).get(inRequest.OpenRPA["AuthToken"], {}).get("FlagDoNotExpire", False)
    return lIsSuperTokenBool

def WebUserUACHierarchyGet(inRequest = None):
    """
    Return User UAC Hierarchy DICT Return {...}

    :param inRequest: inRequest from the server. Optional if call def from request thread
    :return: UAC Dict {}
    """
    if inRequest is None: inRequest = WebRequestGet()
    return inRequest.UserRoleHierarchyGet()


## GSettings defs

from . import SettingsTemplate

GSettings = SettingsTemplate.Create(inModeStr = "BASIC")
# Modules alias for pyOpenRPA.Orchestrator and pyOpenRPA.Orchestrator.__Orchestrator__
lCurrentModule = sys.modules[__name__]
if __name__ == "pyOpenRPA.Orchestrator" and "pyOpenRPA.Orchestrator.__Orchestrator__" not in sys.modules:
    sys.modules["pyOpenRPA.Orchestrator.__Orchestrator__"] = lCurrentModule
if __name__ == "pyOpenRPA.Orchestrator.__Orchestrator__" and "pyOpenRPA.Orchestrator" not in sys.modules:
    sys.modules["pyOpenRPA.Orchestrator"] = lCurrentModule

def GSettingsGet(inGSettings=None):
    """
    Get the GSettings from the singleton module.

    :param inGSettings: You can pass some GSettings to check if it equal to base gsettings. If not equal - def will merge it
    :return: GSettings
    """
    global GSettings # identify the global variable
    # Merge dictionaries if some new dictionary has come
    if inGSettings is not None and GSettings is not inGSettings:
        GSettings = Server.__ComplexDictMerge2to1Overwrite__(in1Dict = inGSettings, in2Dict = GSettings)
    return GSettings # Return the result

def GSettingsKeyListValueSet(inValue, inKeyList=None, inGSettings = None):
    """
    Set value in GSettings by the key list

    :param inGSettings: Global settings dict (singleton)
    :param inValue:
    :param inKeyList:
    :return: bool
    """
    inGSettings = GSettingsGet(inGSettings=inGSettings)  # Set the global settings
    if inKeyList is None: inKeyList = []
    lDict = inGSettings
    for lItem2 in inKeyList[:-1]:
        #Check if key - value exists
        if lItem2 in lDict:
            pass
        else:
            lDict[lItem2]={}
        lDict=lDict[lItem2]
    lDict[inKeyList[-1]] = inValue #Set value
    return True

def GSettingsKeyListValueGet(inKeyList=None, inGSettings = None):
    """
    Get the value from the GSettings by the key list

    :param inGSettings: Global settings dict (singleton)
    :param inKeyList:
    :return: value any type
    """
    inGSettings = GSettingsGet(inGSettings=inGSettings)  # Set the global settings
    if inKeyList is None: inKeyList = []
    lDict = inGSettings
    for lItem2 in inKeyList[:-1]:
        #Check if key - value exists
        if lItem2 in lDict:
            pass
        else:
            lDict[lItem2]={}
        lDict=lDict[lItem2]
    return lDict.get(inKeyList[-1],None)

def GSettingsKeyListValueAppend(inValue, inKeyList=None, inGSettings = None):
    """
    Append value in GSettings by the key list

    .. code-block:: python

        # USAGE
        from pyOpenRPA import Orchestrator

        Orchestrator.GSettingsKeyListValueAppend(
            inGSettings = gSettings,
            inValue = "NewValue",
            inKeyList=["NewKeyDict","NewKeyList"]):
        # result inGSettings: {
        #    ... another keys in gSettings ...,
        #    "NewKeyDict":{
        #        "NewKeyList":[
        #            "NewValue"
        #        ]
        #    }
        #}

    :param inGSettings: Global settings dict (singleton)
    :param inValue: Any value to be appended in gSettings Dict by the key list
    :param inKeyList: List of the nested keys (see example)
    :return: True every time
    """
    inGSettings = GSettingsGet(inGSettings=inGSettings)  # Set the global settings
    if inKeyList is None: inKeyList = []
    lDict = inGSettings
    for lItem2 in inKeyList[:-1]:
        #Check if key - value exists
        if lItem2 in lDict:
            pass
        else:
            lDict[lItem2]={}
        lDict=lDict[lItem2]
    lDict[inKeyList[-1]].append(inValue) #Set value
    return True

def GSettingsKeyListValueOperatorPlus(inValue, inKeyList=None, inGSettings = None):
    """
    Execute plus operation between 2 lists (1:inValue and 2:gSettings by the inKeyList)

    .. code-block:: python

        # USAGE
        from pyOpenRPA import Orchestrator

        Orchestrator.GSettingsKeyListValueOperatorPlus(
            inGSettings = gSettings,
            inValue = [1,2,3],
            inKeyList=["NewKeyDict","NewKeyList"]):
        # result inGSettings: {
        #    ... another keys in gSettings ...,
        #    "NewKeyDict":{
        #        "NewKeyList":[
        #            "NewValue",
        #            1,
        #            2,
        #            3
        #        ]
        #    }
        #}

    :param inGSettings: Global settings dict (singleton)
    :param inValue: List with values to be merged with list in gSettings
    :param inKeyList: List of the nested keys (see example)
    :return: True every time
    """
    inGSettings = GSettingsGet(inGSettings=inGSettings)  # Set the global settings
    if inKeyList is None: inKeyList = []
    lDict = inGSettings
    for lItem2 in inKeyList[:-1]:
        #Check if key - value exists
        if lItem2 in lDict:
            pass
        else:
            lDict[lItem2]={}
        lDict=lDict[lItem2]
    lDict[inKeyList[-1]] += inValue #Set value
    return True

def StorageRobotExists(inRobotNameStr):
    """
    Check if robot storage exists

    :param inRobotNameStr: Robot name (case sensitive)
    :return: True - robot storage exist; False - does not exist
    """
    return inRobotNameStr in GSettingsGet()["StorageDict"]

def StorageRobotGet(inRobotNameStr):
    """
    Get the robot storage by the robot name. If Robot storage is not exist - function will create it

    :param inRobotNameStr: Robot name (case sensitive)
    :return: Dict
    """
    if inRobotNameStr not in GSettingsGet()["StorageDict"]:
        GSettingsGet()["StorageDict"][inRobotNameStr]={}
    return GSettingsGet()["StorageDict"][inRobotNameStr]

def ProcessorAliasDefCreate(inDef, inAliasStr=None, inGSettings = None):
    """
    Create alias for def (can be used in ActivityItem in field Def)
    !WHEN DEF ALIAS IS REQUIRED! - Def alias is required when you try to call Python def from the Orchestrator WEB side (because you can't transmit Python def object out of the Python environment)
    Deprecated. See ActivityItemDefAliasCreate

    .. code-block:: python

        # USAGE
        from pyOpenRPA import Orchestrator

        def TestDef():
            pass
        lAliasStr = Orchestrator.ProcessorAliasDefCreate(
            inGSettings = gSettings,
            inDef = TestDef,
            inAliasStr="TestDefAlias")
        # Now you can call TestDef by the alias from var lAliasStr with help of ActivityItem (key Def = lAliasStr)

    :param inGSettings: Global settings dict (singleton)
    :param inDef: Def
    :param inAliasStr: String alias for associated def
    :return: str Alias string (Alias can be regenerated if previous alias was occupied)
    """
    return ActivityItemDefAliasCreate(inDef=inDef, inAliasStr=inAliasStr, inGSettings = inGSettings)

def ProcessorAliasDefUpdate(inDef, inAliasStr, inGSettings = None):
    """
    Update alias for def (can be used in ActivityItem in field Def).
    !WHEN DEF ALIAS IS REQUIRED! - Def alias is required when you try to call Python def from the Orchestrator WEB side (because you can't transmit Python def object out of the Python environment)
    Deprecated. See ActivityItemDefAliasUpdate

    .. code-block:: python

        # USAGE
        from pyOpenRPA import Orchestrator

        def TestDef():
            pass
        Orchestrator.ProcessorAliasDefUpdate(
            inGSettings = gSettings,
            inDef = TestDef,
            inAliasStr="TestDefAlias")
        # Now you can call TestDef by the alias "TestDefAlias" with help of ActivityItem (key Def = "TestDefAlias")

    :param inGSettings: Global settings dict (singleton)
    :param inDef: Def
    :param inAliasStr: String alias for associated def
    :return: str Alias string
    """
    return ActivityItemDefAliasUpdate(inDef=inDef, inAliasStr=inAliasStr, inGSettings = inGSettings)

# ActivityItem defs
def ActivityItemHelperDefList(inDefQueryStr=None):
    """
     Create list of the available Def names in activity item. You can use query def filter via arg inDefQueryStr

    :param inDefStr:
    :return: ["ActivityItemDefAliasUpdate", "ActivityItemDefAliasCreate", etc...]
    """
    lResultList = []
    if inDefQueryStr is not None: # do search alg
        for lKeyStr in GSettingsGet()["ProcessorDict"]["AliasDefDict"]:
            if inDefQueryStr.upper() in lKeyStr.upper():
                lResultList.append(lKeyStr)
    else:
        for lKeyStr in GSettingsGet()["ProcessorDict"]["AliasDefDict"]:
            lResultList.append(lKeyStr)
    return lResultList

def ActivityItemHelperDefAutofill(inDef):
    """
    Detect def by the name and prepare the activity item dict with values.

    :param inDef:
    :return:
    """
    lResultDict = {
        "Def": None,
        "ArgList": [],
        "ArgDict": {},
        "ArgGSettingsStr": None,
        "ArgLoggerStr": None
    }
    lResultDict["Def"] = inDef
    lGS = GSettingsGet()
    if inDef in lGS["ProcessorDict"]["AliasDefDict"]:
        lDefSignature = inspect.signature(lGS["ProcessorDict"]["AliasDefDict"][inDef])
        for lItemKeyStr in lDefSignature.parameters:
            lItemValue = lDefSignature.parameters[lItemKeyStr]
            # Check if arg name contains "GSetting" or "Logger"
            if "GSETTING" in lItemKeyStr.upper():
                lResultDict["ArgGSettingsStr"] = lItemKeyStr
            elif "LOGGER" in lItemKeyStr.upper():
                lResultDict["ArgLoggerStr"] = lItemKeyStr
            else:
                if lItemValue.default is inspect._empty:
                    lResultDict["ArgDict"][lItemKeyStr] = None
                else:
                    lResultDict["ArgDict"][lItemKeyStr] = lItemValue.default
    return lResultDict

def ActivityItemCreate(inDef, inArgList=None, inArgDict=None, inArgGSettingsStr=None, inArgLoggerStr=None, inGUIDStr = None, inThreadBool = False):
    """
    Create activity item. Activity item can be used as list item in ProcessorActivityItemAppend or in Processor.ActivityListExecute.

    .. code-block:: python

        # USAGE
        from pyOpenRPA import Orchestrator

        # EXAMPLE 1
        def TestDef(inArg1Str, inGSettings, inLogger):
            pass
        lActivityItem = Orchestrator.ActivityItemCreate(
            inDef = TestDef,
            inArgList=[],
            inArgDict={"inArg1Str": "ArgValueStr"},
            inArgGSettingsStr = "inGSettings",
            inArgLoggerStr = "inLogger")
        # lActivityItem:
        #   {
        #       "Def":TestDef,
        #       "ArgList":inArgList,
        #       "ArgDict":inArgDict,
        #       "ArgGSettings": "inArgGSettings",
        #       "ArgLogger": "inLogger"
        #   }

        # EXAMPLE 2
        def TestDef(inArg1Str):
            pass
        Orchestrator.ActivityItemDefAliasUpdate(
            inGSettings = gSettings,
            inDef = TestDef,
            inAliasStr="TestDefAlias")
        lActivityItem = Orchestrator.ActivityItemCreate(
            inDef = "TestDefAlias",
            inArgList=[],
            inArgDict={"inArg1Str": "ArgValueStr"},
            inArgGSettingsStr = None,
            inArgLoggerStr = None)
        # lActivityItem:
        #   {
        #       "Def":"TestDefAlias",
        #       "ArgList":inArgList,
        #       "ArgDict":inArgDict,
        #       "ArgGSettings": None,
        #       "ArgLogger": None
        #   }

    :param inDef: def link or def alias (look gSettings["Processor"]["AliasDefDict"])
    :param inArgList: Args list for the Def
    :param inArgDict: Args dict for the def
    :param inArgGSettingsStr: Name of def argument of the GSettings dict
    :param inArgLoggerStr: Name of def argument of the logging object
    :param inGUIDStr: GUID which you can specify. If None the GUID will be generated
    :param inThreadBool: True - execute ActivityItem in new thread; False - in processor thread
    :return: {}
    """
    # Work about GUID in Activity items
    if inGUIDStr is None:
        inGUIDStr = str(uuid.uuid4())  # generate new GUID
    if inArgList is None: inArgList=[]
    if inArgDict is None: inArgDict={}
    lActivityItemDict= {
        "Def":inDef, # def link or def alias (look gSettings["Processor"]["AliasDefDict"])
        "ArgList":inArgList, # Args list
        "ArgDict":inArgDict, # Args dictionary
        "ArgGSettings": inArgGSettingsStr, # Name of GSettings attribute: str (ArgDict) or index (for ArgList)
        "ArgLogger": inArgLoggerStr, # Name of GSettings attribute: str (ArgDict) or index (for ArgList)
        "GUIDStr": inGUIDStr,
        "ThreadBool": inThreadBool
    }
    return lActivityItemDict


def ActivityItemDefAliasCreate(inDef, inAliasStr=None, inGSettings = None):
    """
    Create alias for def (can be used in ActivityItem in field Def)
    !WHEN DEF ALIAS IS REQUIRED! - Def alias is required when you try to call Python def from the Orchestrator WEB side (because you can't transmit Python def object out of the Python environment)

    .. code-block:: python

        # USAGE
        from pyOpenRPA import Orchestrator

        def TestDef():
            pass
        lAliasStr = Orchestrator.ActivityItemDefAliasCreate(
            inGSettings = gSettings,
            inDef = TestDef,
            inAliasStr="TestDefAlias")
        # Now you can call TestDef by the alias from var lAliasStr with help of ActivityItem (key Def = lAliasStr)

    :param inGSettings: Global settings dict (singleton)
    :param inDef: Def
    :param inAliasStr: String alias for associated def
    :return: str Alias string (Alias can be regenerated if previous alias was occupied)
    """
    #TODO Pay attention - New alias can be used too - need to create more complex algorythm to create new alias!
    inGSettings = GSettingsGet(inGSettings=inGSettings)  # Set the global settings
    lL = inGSettings["Logger"]
    if inAliasStr is None: inAliasStr = str(inDef)
    # Check if key is not exists
    if inAliasStr in inGSettings["ProcessorDict"]["AliasDefDict"]:
        inAliasStr = str(inDef)
        if lL: lL.warning(f"Orchestrator.ProcessorAliasDefCreate: Alias {inAliasStr} already exists in alias dictionary. Another alias will be generated and returned")
    inGSettings["ProcessorDict"]["AliasDefDict"][inAliasStr] = inDef
    return inAliasStr

def ActivityItemDefAliasModulesLoad():
    """
    Load all def from sys.modules... in ActivityItem def alias dict

    :return: None
    """
    lL = OrchestratorLoggerGet()
    lL.info(f"ActivityItem aliases: start to load sys.modules")
    lSysModulesSnapshot = copy.copy(sys.modules) # Actual when start from jupyter
    for lModuleItemStr in lSysModulesSnapshot:
        lModuleItem = lSysModulesSnapshot[lModuleItemStr]
        for lDefItemStr in dir(lModuleItem):
            try:
                lDefItem = getattr(lModuleItem,lDefItemStr)
                if callable(lDefItem) and not lDefItemStr.startswith("_"):
                    ActivityItemDefAliasCreate(inDef=lDefItem, inAliasStr=f"{lModuleItemStr}.{lDefItemStr}")
            except ModuleNotFoundError:
                pass
    lL.info(f"ActivityItem aliases: finish to load sys.modules")

def ActivityItemDefAliasUpdate(inDef, inAliasStr, inGSettings = None):
    """
    Update alias for def (can be used in ActivityItem in field Def).
    !WHEN DEF ALIAS IS REQUIRED! - Def alias is required when you try to call Python def from the Orchestrator WEB side (because you can't transmit Python def object out of the Python environment)

    .. code-block:: python

        # USAGE
        from pyOpenRPA import Orchestrator

        def TestDef():
            pass
        Orchestrator.ActivityItemDefAliasUpdate(
            inGSettings = gSettings,
            inDef = TestDef,
            inAliasStr="TestDefAlias")
        # Now you can call TestDef by the alias "TestDefAlias" with help of ActivityItem (key Def = "TestDefAlias")

    :param inGSettings: Global settings dict (singleton)
    :param inDef: Def
    :param inAliasStr: String alias for associated def
    :return: str Alias string
    """
    inGSettings = GSettingsGet(inGSettings=inGSettings)  # Set the global settings
    if callable(inDef): inGSettings["ProcessorDict"]["AliasDefDict"][inAliasStr] = inDef
    else: raise Exception(f"pyOpenRPA Exception: You can't use Orchestrator.ActivityItemDefAliasUpdate with arg 'inDef' string value. inDef is '{inDef}', inAliasStr is '{inAliasStr}'")
    return inAliasStr



def ProcessorActivityItemCreate(inDef, inArgList=None, inArgDict=None, inArgGSettingsStr=None, inArgLoggerStr=None, inGUIDStr = None, inThreadBool = False):
    """
    Create activity item. Activity item can be used as list item in ProcessorActivityItemAppend or in Processor.ActivityListExecute.
    Deprecated. See ActivityItemCreate
    .. code-block:: python

        # USAGE
        from pyOpenRPA import Orchestrator

        # EXAMPLE 1
        def TestDef(inArg1Str, inGSettings, inLogger):
            pass
        lActivityItem = Orchestrator.ProcessorActivityItemCreate(
            inDef = TestDef,
            inArgList=[],
            inArgDict={"inArg1Str": "ArgValueStr"},
            inArgGSettingsStr = "inGSettings",
            inArgLoggerStr = "inLogger")
        # lActivityItem:
        #   {
        #       "Def":TestDef,
        #       "ArgList":inArgList,
        #       "ArgDict":inArgDict,
        #       "ArgGSettings": "inArgGSettings",
        #       "ArgLogger": "inLogger"
        #   }

        # EXAMPLE 2
        def TestDef(inArg1Str):
            pass
        Orchestrator.ProcessorAliasDefUpdate(
            inGSettings = gSettings,
            inDef = TestDef,
            inAliasStr="TestDefAlias")
        lActivityItem = Orchestrator.ProcessorActivityItemCreate(
            inDef = "TestDefAlias",
            inArgList=[],
            inArgDict={"inArg1Str": "ArgValueStr"},
            inArgGSettingsStr = None,
            inArgLoggerStr = None)
        # lActivityItem:
        #   {
        #       "Def":"TestDefAlias",
        #       "ArgList":inArgList,
        #       "ArgDict":inArgDict,
        #       "ArgGSettings": None,
        #       "ArgLogger": None
        #   }

    :param inDef: def link or def alias (look gSettings["Processor"]["AliasDefDict"])
    :param inArgList: Args list for the Def
    :param inArgDict: Args dict for the def
    :param inArgGSettingsStr: Name of def argument of the GSettings dict
    :param inArgLoggerStr: Name of def argument of the logging object
    :param inGUIDStr: GUID which you can specify. If None the GUID will be generated
    :param inThreadBool: True - execute ActivityItem in new thread; False - in processor thread
    :return: {}
    """
    return ActivityItemCreate(inDef=inDef, inArgList=inArgList, inArgDict=inArgDict, inArgGSettingsStr=inArgGSettingsStr, inArgLoggerStr=inArgLoggerStr,
                           inGUIDStr=inGUIDStr, inThreadBool=inThreadBool)

def ProcessorActivityItemAppend(inGSettings = None, inDef=None, inArgList=None, inArgDict=None, inArgGSettingsStr=None, inArgLoggerStr=None, inActivityItemDict=None):
    """
    Create and add activity item in processor queue.

    .. code-block:: python

        # USAGE
        from pyOpenRPA import Orchestrator

        # EXAMPLE 1
        def TestDef(inArg1Str, inGSettings, inLogger):
            pass
        lActivityItem = Orchestrator.ProcessorActivityItemAppend(
            inGSettings = gSettingsDict,
            inDef = TestDef,
            inArgList=[],
            inArgDict={"inArg1Str": "ArgValueStr"},
            inArgGSettingsStr = "inGSettings",
            inArgLoggerStr = "inLogger")
        # Activity have been already append in the processor queue

        # EXAMPLE 2
        def TestDef(inArg1Str):
            pass
        Orchestrator.ProcessorAliasDefUpdate(
            inGSettings = gSettings,
            inDef = TestDef,
            inAliasStr="TestDefAlias")
        lActivityItem = Orchestrator.ProcessorActivityItemCreate(
            inDef = "TestDefAlias",
            inArgList=[],
            inArgDict={"inArg1Str": "ArgValueStr"},
            inArgGSettingsStr = None,
            inArgLoggerStr = None)
        Orchestrator.ProcessorActivityItemAppend(
            inGSettings = gSettingsDict,
            inActivityItemDict = lActivityItem)
        # Activity have been already append in the processor queue

    :param inGSettings: Global settings dict (singleton)
    :param inDef: def link or def alias (look gSettings["Processor"]["AliasDefDict"])
    :param inArgList: Args list for the Def
    :param inArgDict: Args dict for the Def
    :param inArgGSettingsStr: Name of def argument of the GSettings dict
    :param inArgLoggerStr: Name of def argument of the logging object
    :param inActivityItemDict: Fill if you already have ActivityItemDict (don't fill inDef, inArgList, inArgDict, inArgGSettingsStr, inArgLoggerStr)
    :return ActivityItem GUIDStr
    """
    inGSettings = GSettingsGet(inGSettings=inGSettings)  # Set the global settings
    if inActivityItemDict is None:
        if inArgList is None: inArgList=[]
        if inArgDict is None: inArgDict={}
        if inDef is None: raise Exception(f"pyOpenRPA Exception: ProcessorActivityItemAppend need inDef arg if you dont use inActivityItemDict")
        lActivityList=[
            {
                "Def":inDef, # def link or def alias (look gSettings["Processor"]["AliasDefDict"])
                "ArgList":inArgList, # Args list
                "ArgDict":inArgDict, # Args dictionary
                "ArgGSettings": inArgGSettingsStr, # Name of GSettings attribute: str (ArgDict) or index (for ArgList)
                "ArgLogger": inArgLoggerStr # Name of GSettings attribute: str (ArgDict) or index (for ArgList)
            }
        ]
    else:
        lActivityList = [inActivityItemDict]
    # Work about GUID in Activity items
    lGUIDStr = None
    for lItemDict in lActivityList:
        # Add GUIDStr if not exist
        if "GUIDStr" not in lItemDict:
            lGUIDStr = str(uuid.uuid4())  # generate new GUID
            lItemDict["GUIDStr"] = lGUIDStr
    # Add activity list in ProcessorDict
    inGSettings["ProcessorDict"]["ActivityList"]+=lActivityList
    return lGUIDStr

## Process defs
def ProcessIsStarted(inProcessNameWOExeStr): # Check if process is started
    """
    Check if there is any running process that contains the given name processName.

    .. code-block:: python

        # USAGE
        from pyOpenRPA import Orchestrator

        lProcessIsStartedBool = Orchestrator.ProcessIsStarted(inProcessNameWOExeStr = "notepad")
        # lProcessIsStartedBool is True - notepad.exe is running on the Orchestrator machine

    :param inProcessNameWOExeStr: Process name WithOut (WO) '.exe' postfix. Example: "notepad" (not "notepad.exe")
    :return: True - process is running on the orchestrator machine; False - process is not running on the orchestrator machine
    """
    #Iterate over the all the running process
    for proc in psutil.process_iter():
        try:
            # Check if process name contains the given name string.
            if inProcessNameWOExeStr.lower() in proc.name().lower():
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return False

def ProcessStart(inPathStr, inArgList, inStopProcessNameWOExeStr=None):
    """
    Start process locally. Extra feature: Use inStopProcessNameWOExeStr to stop the execution if current process is running.

    .. code-block:: python

        # USAGE
        from pyOpenRPA import Orchestrator

        Orchestrator.ProcessStart(
            inPathStr = "notepad"
            inArgList = []
            inStopProcessNameWOExeStr = "notepad")
        # notepad.exe will be started if no notepad.exe is active on the machine

    :param inPathStr: Command to send in CMD
    :param inArgList: List of the arguments for the CMD command. Example: ["test.txt"]
    :param inStopProcessNameWOExeStr: Trigger: stop execution if process is running. Process name WithOut (WO) '.exe' postfix. Example: "notepad" (not "notepad.exe")
    :return: None - nothing is returned. If process will not start -exception will be raised
    """
    lStartProcessBool = True
    if inStopProcessNameWOExeStr is not None: #Check if process running
        lCheckTaskName = inStopProcessNameWOExeStr
        if len(lCheckTaskName)>4:
            if lCheckTaskName[-4:].upper() != ".EXE":
                lCheckTaskName = lCheckTaskName+".exe"
        else:
            lCheckTaskName = lCheckTaskName+".exe"
        #Check if process exist
        if not ProcessIsStarted(inProcessNameWOExeStr=lCheckTaskName): lStartProcessBool=True

    if lStartProcessBool == True: # Start if flag is true
        lItemArgs=[inPathStr]
        if inArgList is None: inArgList = [] # 2021 02 22 Minor fix default value
        lItemArgs.extend(inArgList)
        subprocess.Popen(lItemArgs,shell=True)

def ProcessStop(inProcessNameWOExeStr, inCloseForceBool, inUserNameStr = "%username%"):
    """
    Stop process on the orchestrator machine. You can set user session on the machine and set flag about to force close process.

    .. code-block:: python

        # USAGE
        from pyOpenRPA import Orchestrator

        Orchestrator.ProcessStop(
            inProcessNameWOExeStr = "notepad"
            inCloseForceBool = True
            inUserNameStr = "USER_99")
        # Will close process "notepad.exe" on the user session "USER_99" (!ATTENTION! if process not exists no exceptions will be raised)

    :param inProcessNameWOExeStr: Process name WithOut (WO) '.exe' postfix. Example: "notepad" (not "notepad.exe")
    :param inCloseForceBool: True - do force close. False - send signal to safe close (!ATTENTION! - Safe close works only in orchestrator session. Win OS doens't allow to send safe close signal between GUI sessions)
    :param inUserNameStr: User name which is has current process to close. Default value is close process on the Orchestrator session
    :return: None
    """
    # Support input arg if with .exe
    lProcessNameWExeStr = inProcessNameWOExeStr
    if len(lProcessNameWExeStr) > 4:
        if lProcessNameWExeStr[-4:].upper() != ".EXE":
            lProcessNameWExeStr = lProcessNameWExeStr + ".exe"
    else:
        lProcessNameWExeStr = lProcessNameWExeStr + ".exe"
    # Flag Force
    lActivityCloseCommand = 'taskkill /im ' + lProcessNameWExeStr
    if inCloseForceBool == True:
        lActivityCloseCommand += " /F"
    # None - all users, %username% - current user, another str - another user
    if inUserNameStr is not None:
        lActivityCloseCommand += f' /fi "username eq {inUserNameStr}"'
    # Kill process
    os.system(lActivityCloseCommand)

def ProcessListGet(inProcessNameWOExeList=None):
    """
    Return process list on the orchestrator machine sorted by Memory Usage. You can determine the list of the processes you are interested - def will return the list about it.

    .. code-block:: python

        # USAGE
        from pyOpenRPA import Orchestrator

        lProcessList = Orchestrator.ProcessListGet()
        # Return the list of the process on the machine.
        # !ATTENTION! RUn orchestrator as administrator to get all process list on the machine.

    :param inProcessNameWOExeList:
    :return: {
    "ProcessWOExeList": ["notepad","..."],
    "ProcessWOExeUpperList": ["NOTEPAD","..."],
    "ProcessDetailList": [
        {
            'pid': 412,
            'username': "DESKTOP\\USER",
            'name': 'notepad.exe',
            'vms': 13.77767775,
            'NameWOExeUpperStr': 'NOTEPAD',
            'NameWOExeStr': "'notepad'"},
        {...}]

    """
    if inProcessNameWOExeList is None: inProcessNameWOExeList = []
    lMapUPPERInput = {} # Mapping for processes WO exe
    lResult = {"ProcessWOExeList":[], "ProcessWOExeUpperList":[],"ProcessDetailList":[]}
    # Create updated list for quick check
    lProcessNameWOExeList = []
    for lItem in inProcessNameWOExeList:
        if lItem is not None:
            lProcessNameWOExeList.append(f"{lItem.upper()}.EXE")
            lMapUPPERInput[f"{lItem.upper()}.EXE"]= lItem
    # Iterate over the list
    for proc in psutil.process_iter():
        try:
            # Fetch process details as dict
            pinfo = proc.as_dict(attrs=['pid', 'name', 'username'])
            pinfo['vms'] = proc.memory_info().vms / (1024 * 1024)
            pinfo['NameWOExeUpperStr'] = pinfo['name'][:-4].upper()
            # Add if empty inProcessNameWOExeList or if process in inProcessNameWOExeList
            if len(lProcessNameWOExeList)==0 or pinfo['name'].upper() in lProcessNameWOExeList:
                try: # 2021 02 22 Minor fix if not admin rights
                    pinfo['NameWOExeStr'] = lMapUPPERInput[pinfo['name'].upper()]
                except Exception as e:
                    pinfo['NameWOExeStr'] = pinfo['name'][:-4]
                lResult["ProcessDetailList"].append(pinfo) # Append dict to list
                lResult["ProcessWOExeList"].append(pinfo['NameWOExeStr'])
                lResult["ProcessWOExeUpperList"].append(pinfo['NameWOExeUpperStr'])
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
           pass
    return lResult


def ProcessDefIntervalCall(inDef, inIntervalSecFloat, inIntervalAsyncBool=False, inDefArgList=None, inDefArgDict=None, inDefArgGSettingsNameStr=None, inDefArgLoggerNameStr=None, inExecuteInNewThreadBool=True, inLogger=None, inGSettings = None):
    """
    Use this procedure if you need to run periodically some def. Set def, args, interval and enjoy :)

    :param inGSettings: global settings
    :param inDef: def link, which will be called with interval inIntervalSecFloat
    :param inIntervalSecFloat: Interval in seconds between call
    :param inIntervalAsyncBool: False - wait interval before next call after the previous iteration result; True - wait interval after previous iteration call
    :param inDefArgList: List of the args in def. Default None (empty list)
    :param inDefArgDict: Dict of the args in def. Default None (empty dict)
    :param inDefArgGSettingsNameStr: Name of the GSettings arg name for def (optional)
    :param inDefArgLoggerNameStr: Name of the Logger arg name for def (optional). If Use - please check fill of the inLogger arg.
    :param inExecuteInNewThreadBool: True - create new thread for the periodic execution; False - execute in current thread. Default: True
    :param inLogger: logging def if some case is appear
    :return:
    """
    inGSettings = GSettingsGet(inGSettings=inGSettings)  # Set the global settings
    if inLogger is None: inLogger = OrchestratorLoggerGet()
    #Some edits on start
    if inDefArgDict is None: inDefArgDict = {}
    if inDefArgList is None: inDefArgList = []
    # Check if inDefArgLogger is set and inLogger is exist
    if inDefArgLoggerNameStr=="": inDefArgLoggerNameStr=None
    if inDefArgGSettingsNameStr=="": inDefArgGSettingsNameStr=None
    if inDefArgLoggerNameStr is not None and not inLogger:
        raise Exception(f"!ERROR! ProcessDefIntervalCall - You need to send logger in def because your def is require logger. Raise error!")

    # Check thread
    if not Core.IsProcessorThread(inGSettings=inGSettings):
        if inGSettings["Logger"]: inGSettings["Logger"].warning(f"__Orchestrator__.ProcessDefIntervalCall def was called not from processor queue - activity will be append in the processor queue.")
        lProcessorActivityDict = {
            "Def": ProcessDefIntervalCall, # def link or def alias (look gSettings["Processor"]["AliasDefDict"])
            "ArgList": [],  # Args list
            "ArgDict": {"inDef": inDef, "inIntervalSecFloat": inIntervalSecFloat,
                        "inIntervalAsyncBool":inIntervalAsyncBool, "inDefArgList": inDefArgList,
                        "inDefArgDict": inDefArgDict, "inDefArgGSettingsNameStr":inDefArgGSettingsNameStr,
                        "inDefArgLoggerNameStr": inDefArgLoggerNameStr, "inExecuteInNewThreadBool": inExecuteInNewThreadBool},  # Args dictionary
            "ArgGSettings": "inGSettings",  # Name of GSettings attribute: str (ArgDict) or index (for ArgList)
            "ArgLogger": "inLogger"  # Name of GSettings attribute: str (ArgDict) or index (for ArgList)
        }
        inGSettings["ProcessorDict"]["ActivityList"].append(lProcessorActivityDict)
    else:
        # Internal def to execute periodically
        def __Execute__(inGSettings, inDef, inIntervalSecFloat, inIntervalAsyncBool, inDefArgList, inDefArgDict, inLogger,  inDefArgGSettingsNameStr, inDefArgLoggerNameStr):
            if inLogger: inLogger.info(f"__Orchestrator__.ProcessDefIntervalCall: Interval execution has been started. Def: {str(inDef)}")
            # Prepare gSettings and logger args
            if inDefArgGSettingsNameStr is not None:
                inDefArgDict[inDefArgGSettingsNameStr] = inGSettings
            if inDefArgLoggerNameStr is not None:
                inDefArgDict[inDefArgLoggerNameStr] = inLogger
            while True:
                try:
                    # Call async if needed
                    if inIntervalAsyncBool == False:  # Case wait result then wait
                        inDef(*inDefArgList, **inDefArgDict)
                    else:  # Case dont wait result - run sleep then new iteration (use many threads)
                        lThread2 = threading.Thread(target=inDef,
                                                    args=inDefArgList,
                                                    kwargs=inDefArgDict)
                        lThread2.start()
                except Exception as e:
                    if inLogger: inLogger.exception(
                        f"ProcessDefIntervalCall: Interval call has been failed. Traceback is below. Code will sleep for the next call")
                # Sleep interval
                time.sleep(inIntervalSecFloat)

        # Check to call in new thread
        if inExecuteInNewThreadBool:
            lThread = threading.Thread(target=__Execute__,
                                       kwargs={"inGSettings":inGSettings, "inDef": inDef, "inIntervalSecFloat": inIntervalSecFloat,
                                               "inIntervalAsyncBool": inIntervalAsyncBool, "inDefArgList": inDefArgList,
                                               "inDefArgDict": inDefArgDict, "inLogger": inLogger,
                                               "inDefArgGSettingsNameStr":inDefArgGSettingsNameStr , "inDefArgLoggerNameStr":inDefArgLoggerNameStr})
            lThread.start()
        else:
            __Execute__(inGSettings=inGSettings, inDef=inDef, inIntervalSecFloat=inIntervalSecFloat, inIntervalAsyncBool=inIntervalAsyncBool,
                        inDefArgList=inDefArgList, inDefArgDict=inDefArgDict, inLogger=inLogger,
                        inDefArgGSettingsNameStr=inDefArgGSettingsNameStr , inDefArgLoggerNameStr=inDefArgLoggerNameStr)


# Python def - start module function
def PythonStart(inModulePathStr, inDefNameStr, inArgList=None, inArgDict=None, inLogger = None):
    """
    Import module and run def in the Orchestrator process.

    .. note::

        Import module will be each time when PythonStart def will be called.

    .. code-block:: python

        # USAGE
        from pyOpenRPA import Orchestrator

        Orchestrator.PythonStart(
            inModulePathStr="ModuleToCall.py", # inModulePathStr: Working Directory\\ModuleToCall.py
            inDefNameStr="TestDef")
        # Import module in Orchestrator process and call def "TestDef" from module "ModuleToCall.py"

    :param inModulePathStr: Absolute or relative (working directory of the orchestrator process) path to the importing module .py
    :param inDefNameStr: Def name in module
    :param inArgList: List of the arguments for callable def
    :param inArgDict: Dict of the named arguments for callable def
    :param inLogger: Logger instance to log some information when PythonStart def is running
    :return: None
    """
    if inLogger is None: inLogger = OrchestratorLoggerGet()
    if inArgList is None: inArgList=[]
    if inArgDict is None: inArgDict={}
    try:
        lModule=importlib.import_module(inModulePathStr) #Подключить модуль для вызова
        lFunction=getattr(lModule,inDefNameStr) #Найти функцию
        return lFunction(*inArgList,**inArgDict)
    except Exception as e:
        if inLogger: inLogger.exception("Loop activity error: module/function not founded")

# # # # # # # # # # # # # # # # # # # # # # #
# Scheduler
# # # # # # # # # # # # # # # # # # # # # # #

def SchedulerActivityTimeAddWeekly(inTimeHHMMStr="23:55:", inWeekdayList=None, inActivityList=None, inGSettings = None):
    """
    Add activity item list in scheduler. You can set weekday list and set time when launch. Activity list will be executed at planned time/day.

    .. code-block:: python

        # USAGE
        from pyOpenRPA import Orchestrator

        # EXAMPLE 1
        def TestDef(inArg1Str):
            pass
        lActivityItem = Orchestrator.ProcessorActivityItemCreate(
            inDef = TestDef,
            inArgList=[],
            inArgDict={"inArg1Str": "ArgValueStr"},
            inArgGSettingsStr = None,
            inArgLoggerStr = None)
        Orchestrator.SchedulerActivityTimeAddWeekly(
            inGSettings = gSettingsDict,
            inTimeHHMMStr = "04:34",
            inWeekdayList=[2,3,4],
            inActivityList = [lActivityItem])
        # Activity will be executed at 04:34 Wednesday (2), thursday (3), friday (4)

    :param inGSettings: Global settings dict (singleton)
    :param inTimeHHMMStr: Activation time from "00:00" to "23:59". Example: "05:29"
    :param inWeekdayList: Week day list to initiate activity list. Use int from 0 (monday) to 6 (sunday) as list items. Example: [0,1,2,3,4]. Default value is everyday ([0,1,2,3,4,5,6])
    :param inActivityList: Activity list structure
    :return: None
    """
    inGSettings = GSettingsGet(inGSettings=inGSettings)  # Set the global settings
    if inWeekdayList is None: inWeekdayList=[0,1,2,3,4,5,6]
    if inActivityList is None: inActivityList=[]
    Processor.__ActivityListVerify__(inActivityList=inActivityList) # DO VERIFICATION FOR THE inActivityList
    lActivityTimeItemDict = {
        "TimeHH:MMStr": inTimeHHMMStr,  # Time [HH:MM] to trigger activity
        "WeekdayList": inWeekdayList, # List of the weekday index when activity is applicable, Default [1,2,3,4,5,6,7]
        "ActivityList": inActivityList,
        "GUID": None  #    # Will be filled in Orchestrator automatically - is needed for detect activity completion
    }
    inGSettings["SchedulerDict"]["ActivityTimeList"].append(lActivityTimeItemDict)

# # # # # # # # # # # # # # # # # # # # # # #
# RDPSession
# # # # # # # # # # # # # # # # # # # # # # #

def RDPTemplateCreate(inLoginStr, inPasswordStr, inHostStr="127.0.0.1", inPortInt = 3389, inWidthPXInt = 1680,  inHeightPXInt = 1050,
                      inUseBothMonitorBool = False, inDepthBitInt = 32, inSharedDriveList=None, inRedirectClipboardBool=True):
    """
    Create RDP connect dict item/ Use it connect/reconnect (Orchestrator.RDPSessionConnect)

    .. code-block:: python

        # USAGE
        from pyOpenRPA import Orchestrator

        lRDPItemDict = Orchestrator.RDPTemplateCreate(
            inLoginStr = "USER_99",
            inPasswordStr = "USER_PASS_HERE",
            inHostStr="127.0.0.1",
            inPortInt = 3389,
            inWidthPXInt = 1680,
            inHeightPXInt = 1050,
            inUseBothMonitorBool = False,
            inDepthBitInt = 32,
            inSharedDriveList=None)
        #     lRDPTemplateDict= {  # Init the configuration item
        #         "Host": "127.0.0.1", "Port": "3389", "Login": "USER_99", "Password": "USER_PASS_HERE",
        #         "Screen": { "Width": 1680, "Height": 1050, "FlagUseAllMonitors": False, "DepthBit": "32" },
        #         "SharedDriveList": ["c"],
        #         "RedirectClipboardBool": True, # True - share clipboard to RDP; False - else
        #         ###### Will updated in program ############
        #         "SessionHex": "77777sdfsdf77777dsfdfsf77777777",  # Hex is created when robot runs, example ""
        #         "SessionIsWindowExistBool": False, "SessionIsWindowResponsibleBool": False, "SessionIsIgnoredBool": False
        #     }

    :param inLoginStr: User/Robot Login, example "USER_99"
    :param inPasswordStr: Password, example "USER_PASS_HERE"
    :param inHostStr: Host address, example "77.77.22.22"
    :param inPortInt: RDP Port, example "3389" (default)
    :param inWidthPXInt: Width of the remote desktop in pixels, example 1680
    :param inHeightPXInt: Height of the remote desktop in pixels, example 1050
    :param inUseBothMonitorBool: True - connect to the RDP with both monitors. False - else case
    :param inDepthBitInt: Remote desktop bitness. Available: 32 or 24 or 16 or 15, example 32
    :param inSharedDriveList: Host local disc to connect to the RDP session. Example: ["c", "d"]
    :param inRedirectClipboardBool: # True - share clipboard to RDP; False - else
    :return:
        {
            "Host": inHostStr,  # Host address, example "77.77.22.22"
            "Port": str(inPortInt),  # RDP Port, example "3389"
            "Login": inLoginStr,  # Login, example "test"
            "Password": inPasswordStr,  # Password, example "test"
            "Screen": {
                "Width": inWidthPXInt,  # Width of the remote desktop in pixels, example 1680
                "Height": inHeightPXInt,  # Height of the remote desktop in pixels, example 1050
                # "640x480" or "1680x1050" or "FullScreen". If Resolution not exists set full screen, example
                "FlagUseAllMonitors": inUseBothMonitorBool,  # True or False, example False
                "DepthBit": str(inDepthBitInt)  # "32" or "24" or "16" or "15", example "32"
            },
            "SharedDriveList": inSharedDriveList,  # List of the Root sesion hard drives, example ["c"]
            "RedirectClipboardBool": True, # True - share clipboard to RDP; False - else
            ###### Will updated in program ############
            "SessionHex": "77777sdfsdf77777dsfdfsf77777777",  # Hex is created when robot runs, example ""
            "SessionIsWindowExistBool": False,
            # Flag if the RDP window is exist, old name "FlagSessionIsActive". Check every n seconds , example False
            "SessionIsWindowResponsibleBool": False,
            # Flag if RDP window is responsible (recieve commands). Check every nn seconds. If window is Responsible - window is Exist too , example False
            "SessionIsIgnoredBool": False  # Flag to ignore RDP window False - dont ignore, True - ignore, example False
        }

    """
    if inSharedDriveList is None: inSharedDriveList = ["c"]
    if inPortInt is None: inPortInt = 3389
    if inRedirectClipboardBool is None: inRedirectClipboardBool = True
    lRDPTemplateDict= {  # Init the configuration item
        "Host": inHostStr,  # Host address, example "77.77.22.22"
        "Port": str(inPortInt),  # RDP Port, example "3389"
        "Login": inLoginStr,  # Login, example "test"
        "Password": inPasswordStr,  # Password, example "test"
        "Screen": {
            "Width": inWidthPXInt,  # Width of the remote desktop in pixels, example 1680
            "Height": inHeightPXInt,  # Height of the remote desktop in pixels, example 1050
            # "640x480" or "1680x1050" or "FullScreen". If Resolution not exists set full screen, example
            "FlagUseAllMonitors": inUseBothMonitorBool,  # True or False, example False
            "DepthBit": str(inDepthBitInt)  # "32" or "24" or "16" or "15", example "32"
        },
        "SharedDriveList": inSharedDriveList,  # List of the Root sesion hard drives, example ["c"],
        "RedirectClipboardBool": inRedirectClipboardBool, # True - share clipboard to RDP; False - else
        ###### Will updated in program ############
        "SessionHex": "77777sdfsdf77777dsfdfsf77777777",  # Hex is created when robot runs, example ""
        "SessionIsWindowExistBool": False,
        # Flag if the RDP window is exist, old name "FlagSessionIsActive". Check every n seconds , example False
        "SessionIsWindowResponsibleBool": False,
        # Flag if RDP window is responsible (recieve commands). Check every nn seconds. If window is Responsible - window is Exist too , example False
        "SessionIsIgnoredBool": False  # Flag to ignore RDP window False - dont ignore, True - ignore, example False
    }
    return lRDPTemplateDict

# TODO Search dublicates in GSettings RDPlist !
# Return list if dublicates
def RDPSessionDublicatesResolve(inGSettings):
    """
    DEVELOPING Search duplicates in GSettings RDPlist
    !def is developing!

    :param inGSettings: Global settings dict (singleton)
    :return:
    """
    pass
    #for lItemKeyStr in inGSettings["RobotRDPActive"]["RDPList"]:
    #   lItemDict = inGSettings["RobotRDPActive"]["RDPList"][lItemKeyStr]

def RDPSessionConnect(inRDPSessionKeyStr, inRDPTemplateDict=None, inHostStr=None, inPortStr=None, inLoginStr=None, inPasswordStr=None, inGSettings = None, inRedirectClipboardBool=True):
    """
    Create new RDPSession in RobotRDPActive. Attention - activity will be ignored if RDP key is already exists
     2 way of the use
    Var 1 (Main stream): inGSettings, inRDPSessionKeyStr, inRDPTemplateDict
    Var 2 (Backward compatibility): inGSettings, inRDPSessionKeyStr, inHostStr, inPortStr, inLoginStr, inPasswordStr

    .. code-block:: python

        # USAGE
        from pyOpenRPA import Orchestrator

        lRDPItemDict = Orchestrator.RDPTemplateCreate(
            inLoginStr = "USER_99",
            inPasswordStr = "USER_PASS_HERE", inHostStr="127.0.0.1", inPortInt = 3389, inWidthPXInt = 1680,
            inHeightPXInt = 1050, inUseBothMonitorBool = False, inDepthBitInt = 32, inSharedDriveList=None)
        Orchestrator.RDPSessionConnect(
            inGSettings = gSettings,
            inRDPSessionKeyStr = "RDPKey",
            inRDPTemplateDict = lRDPItemDict)
        # Orchestrator will create RDP session by the lRDPItemDict configuration

    :param inGSettings: Global settings dict (singleton)
    :param inRDPSessionKeyStr: RDP Session string key - need for the further identification
    :param inRDPTemplateDict: RDP configuration dict with settings (see def Orchestrator.RDPTemplateCreate)
    :param inHostStr: Backward compatibility from Orchestrator v 1.1.20. Use inRDPTemplateDict
    :param inPortStr: Backward compatibility from Orchestrator v 1.1.20. Use inRDPTemplateDict
    :param inLoginStr: Backward compatibility from Orchestrator v 1.1.20. Use inRDPTemplateDict
    :param inPasswordStr: Backward compatibility from Orchestrator v 1.1.20. Use inRDPTemplateDict
    :return: True every time :)
    """
    inGSettings = GSettingsGet(inGSettings=inGSettings)  # Set the global settings
    # Check thread
    if not Core.IsProcessorThread(inGSettings=inGSettings):
        if inGSettings["Logger"]: inGSettings["Logger"].warning(f"RDP def was called not from processor queue - activity will be append in the processor queue.")
        lResult = {
            "Def": RDPSessionConnect, # def link or def alias (look gSettings["Processor"]["AliasDefDict"])
            "ArgList": [],  # Args list
            "ArgDict": {"inRDPSessionKeyStr": inRDPSessionKeyStr, "inRDPTemplateDict":inRDPTemplateDict, "inHostStr": inHostStr, "inPortStr": inPortStr,
                    "inLoginStr": inLoginStr, "inPasswordStr": inPasswordStr, "inRedirectClipboardBool": inRedirectClipboardBool},  # Args dictionary
            "ArgGSettings": "inGSettings",  # Name of GSettings attribute: str (ArgDict) or index (for ArgList)
            "ArgLogger": None  # Name of GSettings attribute: str (ArgDict) or index (for ArgList)
        }
        inGSettings["ProcessorDict"]["ActivityList"].append(lResult)
    else: # In processor - do execution
        # Var 1 - if RDPTemplateDict is input
        lRDPConfigurationItem=inRDPTemplateDict
        # Var 2 - backward compatibility
        if lRDPConfigurationItem is None:
            lRDPConfigurationItem = RDPTemplateCreate(inLoginStr=inLoginStr, inPasswordStr=inPasswordStr,
                  inHostStr=inHostStr, inPortInt = int(inPortStr), inRedirectClipboardBool=inRedirectClipboardBool)            # ATTENTION - dont connect if RDP session is exist
        # Start the connect
        if inRDPSessionKeyStr not in inGSettings["RobotRDPActive"]["RDPList"]:
            inGSettings["RobotRDPActive"]["RDPList"][inRDPSessionKeyStr] = lRDPConfigurationItem # Add item in RDPList
            Connector.Session(lRDPConfigurationItem) # Create the RDP session
            Connector.SystemRDPWarningClickOk()  # Click all warning messages
        else:
            if inGSettings["Logger"]: inGSettings["Logger"].warning(f"RDP session was not created because it is alredy exists in the RDPList. Use RDPSessionReconnect if you want to update RDP configuration.")
    return True

def RDPSessionDisconnect(inRDPSessionKeyStr, inBreakTriggerProcessWOExeList = None, inGSettings = None):
    """
    Disconnect the RDP session and stop monitoring it.

    .. code-block:: python

        # USAGE
        from pyOpenRPA import Orchestrator

        Orchestrator.RDPSessionDisconnect(
            inGSettings = gSettings,
            inRDPSessionKeyStr = "RDPKey")
        # Orchestrator will disconnect RDP session and will stop to monitoring current RDP

    :param inGSettings: Global settings dict (singleton)
    :param inRDPSessionKeyStr: RDP Session string key - need for the further identification
    :param inBreakTriggerProcessWOExeList: List of the processes, which will stop the execution. Example ["notepad"]

        .. note::

        Orchestrator look processes on the current machine
    :return: True every time
    """
    inGSettings = GSettingsGet(inGSettings=inGSettings)  # Set the global settings
    if inBreakTriggerProcessWOExeList is None: inBreakTriggerProcessWOExeList = []
    # Check thread
    if not Core.IsProcessorThread(inGSettings=inGSettings):
        if inGSettings["Logger"]: inGSettings["Logger"].warning(f"RDP def was called not from processor queue - activity will be append in the processor queue.")
        lResult = {
            "Def": RDPSessionDisconnect, # def link or def alias (look gSettings["Processor"]["AliasDefDict"])
            "ArgList": [],  # Args list
            "ArgDict": {"inRDPSessionKeyStr": inRDPSessionKeyStr, "inBreakTriggerProcessWOExeList": inBreakTriggerProcessWOExeList },  # Args dictionary
            "ArgGSettings": "inGSettings",  # Name of GSettings attribute: str (ArgDict) or index (for ArgList)
            "ArgLogger": None  # Name of GSettings attribute: str (ArgDict) or index (for ArgList)
        }
        inGSettings["ProcessorDict"]["ActivityList"].append(lResult)
    else: # In processor - do execution
        lSessionHex = inGSettings["RobotRDPActive"]["RDPList"].get(inRDPSessionKeyStr,{}).get("SessionHex", None)
        if lSessionHex:
            lProcessListResult = {"ProcessWOExeList":[],"ProcessDetailList":[]}
            if len(inBreakTriggerProcessWOExeList) > 0:
                lProcessListResult = ProcessListGet(inProcessNameWOExeList=inBreakTriggerProcessWOExeList)  # Run the task manager monitor
            if len(lProcessListResult["ProcessWOExeList"]) == 0: # Start disconnect if no process exist
                inGSettings["RobotRDPActive"]["RDPList"].pop(inRDPSessionKeyStr,None)
                Connector.SessionClose(inSessionHexStr=lSessionHex)
                Connector.SystemRDPWarningClickOk()  # Click all warning messages
    return True

def RDPSessionReconnect(inRDPSessionKeyStr, inRDPTemplateDict=None, inGSettings = None):
    """
    Reconnect the RDP session

    .. code-block:: python

        # USAGE
        from pyOpenRPA import Orchestrator

        lRDPItemDict = Orchestrator.RDPTemplateCreate(
            inLoginStr = "USER_99",
            inPasswordStr = "USER_PASS_HERE", inHostStr="127.0.0.1", inPortInt = 3389, inWidthPXInt = 1680,
            inHeightPXInt = 1050, inUseBothMonitorBool = False, inDepthBitInt = 32, inSharedDriveList=None)
        Orchestrator.RDPSessionReconnect(
            inGSettings = gSettings,
            inRDPSessionKeyStr = "RDPKey",
            inRDPTemplateDict = inRDPTemplateDict)
        # Orchestrator will reconnect RDP session and will continue to monitoring current RDP

    :param inGSettings: Global settings dict (singleton)
    :param inRDPSessionKeyStr: RDP Session string key - need for the further identification
    :param inRDPTemplateDict: RDP configuration dict with settings (see def Orchestrator.RDPTemplateCreate)
    :return:
    """
    inGSettings = GSettingsGet(inGSettings=inGSettings)  # Set the global settings
    # Check thread
    if not Core.IsProcessorThread(inGSettings=inGSettings):
        if inGSettings["Logger"]: inGSettings["Logger"].warning(f"RDP def was called not from processor queue - activity will be append in the processor queue.")
        lResult = {
            "Def": RDPSessionReconnect, # def link or def alias (look gSettings["Processor"]["AliasDefDict"])
            "ArgList": [],  # Args list
            "ArgDict": {"inRDPSessionKeyStr": inRDPSessionKeyStr, "inRDPTemplateDict":inRDPTemplateDict },  # Args dictionary
            "ArgGSettings": "inGSettings",  # Name of GSettings attribute: str (ArgDict) or index (for ArgList)
            "ArgLogger": None  # Name of GSettings attribute: str (ArgDict) or index (for ArgList)
        }
        inGSettings["ProcessorDict"]["ActivityList"].append(lResult)
    else:
        lRDPConfigurationItem = inGSettings["RobotRDPActive"]["RDPList"][inRDPSessionKeyStr]
        RDPSessionDisconnect(inGSettings = inGSettings, inRDPSessionKeyStr=inRDPSessionKeyStr) # Disconnect the RDP 2021 02 22 minor fix by Ivan Maslov
        # Replace Configuration item if inRDPTemplateDict exists
        if inRDPTemplateDict is not None: lRDPConfigurationItem=inRDPTemplateDict
        # Add item in RDPList
        inGSettings["RobotRDPActive"]["RDPList"][inRDPSessionKeyStr] = lRDPConfigurationItem
        # Create the RDP session
        Connector.Session(lRDPConfigurationItem)
    return True

def RDPSessionMonitorStop(inRDPSessionKeyStr, inGSettings = None):
    """
    Stop monitoring the RDP session by the Orchestrator process. Current def don't kill RDP session - only stop to track it (it can give )

    .. code-block:: python

        # USAGE
        from pyOpenRPA import Orchestrator

        Orchestrator.RDPSessionMonitorStop(
            inGSettings = gSettings,
            inRDPSessionKeyStr = "RDPKey")
        # Orchestrator will stop the RDP monitoring

    :param inGSettings: Global settings dict (singleton)
    :param inRDPSessionKeyStr: RDP Session string key - need for the further identification
    :return: True every time :>
    """
    inGSettings = GSettingsGet(inGSettings=inGSettings)  # Set the global settings
    lResult = True
    inGSettings["RobotRDPActive"]["RDPList"].pop(inRDPSessionKeyStr,None) # Remove item from RDPList
    return lResult

def RDPSessionLogoff(inRDPSessionKeyStr, inBreakTriggerProcessWOExeList = None, inGSettings = None):
    """
    Logoff the RDP session from the Orchestrator process (close all apps in session when logoff)

    .. code-block:: python

        # USAGE
        from pyOpenRPA import Orchestrator

        Orchestrator.RDPSessionLogoff(
            inGSettings = gSettings,
            inRDPSessionKeyStr = "RDPKey",
            inBreakTriggerProcessWOExeList = ['Notepad'])
        # Orchestrator will logoff the RDP session

    :param inGSettings: Global settings dict (singleton)
    :param inRDPSessionKeyStr: RDP Session string key - need for the further identification
    :param inBreakTriggerProcessWOExeList: List of the processes, which will stop the execution. Example ["notepad"]
    :return: True - logoff is successful
    """
    inGSettings = GSettingsGet(inGSettings=inGSettings)  # Set the global settings
    if inBreakTriggerProcessWOExeList is None: inBreakTriggerProcessWOExeList = []
    lResult = True
    # Check thread
    if not Core.IsProcessorThread(inGSettings=inGSettings):
        if inGSettings["Logger"]: inGSettings["Logger"].warning(f"RDP def was called not from processor queue - activity will be append in the processor queue.")
        lResult = {
            "Def": RDPSessionLogoff, # def link or def alias (look gSettings["Processor"]["AliasDefDict"])
            "ArgList": [],  # Args list
            "ArgDict": {"inRDPSessionKeyStr": inRDPSessionKeyStr, "inBreakTriggerProcessWOExeList": inBreakTriggerProcessWOExeList },  # Args dictionary
            "ArgGSettings": "inGSettings",  # Name of GSettings attribute: str (ArgDict) or index (for ArgList)
            "ArgLogger": None  # Name of GSettings attribute: str (ArgDict) or index (for ArgList)
        }
        inGSettings["ProcessorDict"]["ActivityList"].append(lResult)
    else:
        lCMDStr = "shutdown -L" # CMD logoff command
        # Calculate the session Hex
        lSessionHex = inGSettings["RobotRDPActive"]["RDPList"].get(inRDPSessionKeyStr,{}).get("SessionHex", None)
        if lSessionHex:
            lProcessListResult = {"ProcessWOExeList":[],"ProcessDetailList":[]}
            if len(inBreakTriggerProcessWOExeList) > 0:
                lProcessListResult = ProcessListGet(inProcessNameWOExeList=inBreakTriggerProcessWOExeList)  # Run the task manager monitor
            if len(lProcessListResult["ProcessWOExeList"]) == 0: # Start logoff if no process exist
                # Run CMD - dont crosscheck because CMD dont return value to the clipboard when logoff
                Connector.SessionCMDRun(inSessionHex=lSessionHex, inCMDCommandStr=lCMDStr, inModeStr="RUN", inLogger=inGSettings["Logger"], inRDPConfigurationItem=inGSettings["RobotRDPActive"]["RDPList"][inRDPSessionKeyStr])
                inGSettings["RobotRDPActive"]["RDPList"].pop(inRDPSessionKeyStr,None) # Remove item from RDPList
    return lResult

def RDPSessionResponsibilityCheck(inRDPSessionKeyStr, inGSettings = None):
    """
    DEVELOPING, MAYBE NOT USEFUL Check RDP Session responsibility TODO NEED DEV + TEST

    :param inGSettings: Global settings dict (singleton)
    :param inRDPSessionKeyStr: RDP Session string key - need for the further identification
    :return: True every time
    """
    inGSettings = GSettingsGet(inGSettings=inGSettings)  # Set the global settings
    # Check thread
    if not Core.IsProcessorThread(inGSettings=inGSettings):
        if inGSettings["Logger"]: inGSettings["Logger"].warning(f"RDP def was called not from processor queue - activity will be append in the processor queue.")
        lResult = {
            "Def": RDPSessionResponsibilityCheck, # def link or def alias (look gSettings["Processor"]["AliasDefDict"])
            "ArgList": [],  # Args list
            "ArgDict": {"inRDPSessionKeyStr": inRDPSessionKeyStr },  # Args dictionary
            "ArgGSettings": "inGSettings",  # Name of GSettings attribute: str (ArgDict) or index (for ArgList)
            "ArgLogger": None  # Name of GSettings attribute: str (ArgDict) or index (for ArgList)
        }
        inGSettings["ProcessorDict"]["ActivityList"].append(lResult)
    else:
        lRDPConfigurationItem = inGSettings["RobotRDPActive"]["RDPList"][inRDPSessionKeyStr] # Get the alias
        # set the fullscreen
        # ATTENTION!!! Session hex can be updated!!!
        Connector.SessionScreenFull(inSessionHex=lRDPConfigurationItem["SessionHex"], inLogger=inGSettings["Logger"], inRDPConfigurationItem=inGSettings["RobotRDPActive"]["RDPList"][inRDPSessionKeyStr])
        time.sleep(1)
        # Check RDP responsibility
        lDoCheckResponsibilityBool = True
        lDoCheckResponsibilityCountMax = 20
        lDoCheckResponsibilityCountCurrent = 0
        while lDoCheckResponsibilityBool:
            # Check if counter is exceed - raise exception
            if lDoCheckResponsibilityCountCurrent >= lDoCheckResponsibilityCountMax:
                pass
                #raise ConnectorExceptions.SessionWindowNotResponsibleError("Error when initialize the RDP session - RDP window is not responding!")
            # Check responding
            lDoCheckResponsibilityBool = not Connector.SystemRDPIsResponsible(inSessionHexStr = lRDPConfigurationItem["SessionHex"])
            # Wait if is not responding
            if lDoCheckResponsibilityBool:
                time.sleep(3)
            # increase the couter
            lDoCheckResponsibilityCountCurrent+=1
    return True

def RDPSessionProcessStartIfNotRunning(inRDPSessionKeyStr, inProcessNameWEXEStr, inFilePathStr, inFlagGetAbsPathBool=True, inGSettings = None):
    """
    Start process in RDP if it is not running (check by the arg inProcessNameWEXEStr)

    .. code-block:: python

        # USAGE
        from pyOpenRPA import Orchestrator

        Orchestrator.RDPSessionProcessStartIfNotRunning(
            inGSettings = gSettings,
            inRDPSessionKeyStr = "RDPKey",
            inProcessNameWEXEStr = 'Notepad.exe',
            inFilePathStr = "path\\to\the\\executable\\file.exe"
            inFlagGetAbsPathBool = True)
        # Orchestrator will start the process in RDP session

    :param inGSettings: Global settings dict (singleton)
    :param inRDPSessionKeyStr: RDP Session string key - need for the further identification
    :param inProcessNameWEXEStr: Process name with extension (.exe). This arg allow to check the process is running. Example: "Notepad.exe"
    :param inFilePathStr: Path to run process if it is not running.
    :param inFlagGetAbsPathBool: True - get abs path from the relative path in inFilePathStr. False - else case
    :return: True every time :)
    """
    inGSettings = GSettingsGet(inGSettings=inGSettings)  # Set the global settings
    # Check thread
    lResult = True
    if not Core.IsProcessorThread(inGSettings=inGSettings):
        if inGSettings["Logger"]: inGSettings["Logger"].warning(f"RDP def was called not from processor queue - activity will be append in the processor queue.")
        lActivityItem = {
            "Def": RDPSessionProcessStartIfNotRunning, # def link or def alias (look gSettings["Processor"]["AliasDefDict"])
            "ArgList": [],  # Args list
            "ArgDict": {"inRDPSessionKeyStr": inRDPSessionKeyStr,  "inProcessNameWEXEStr": inProcessNameWEXEStr, "inFilePathStr": inFilePathStr, "inFlagGetAbsPathBool": inFlagGetAbsPathBool },  # Args dictionary
            "ArgGSettings": "inGSettings",  # Name of GSettings attribute: str (ArgDict) or index (for ArgList)
            "ArgLogger": None  # Name of GSettings attribute: str (ArgDict) or index (for ArgList)
        }
        inGSettings["ProcessorDict"]["ActivityList"].append(lActivityItem)
    else:
        lCMDStr = CMDStr.ProcessStartIfNotRunning(inProcessNameWEXEStr, inFilePathStr, inFlagGetAbsPath= inFlagGetAbsPathBool)
        # Calculate the session Hex
        lSessionHex = inGSettings["RobotRDPActive"]["RDPList"].get(inRDPSessionKeyStr,{}).get("SessionHex", None)
        # Run CMD
        if lSessionHex:
            Connector.SessionCMDRun(inSessionHex=lSessionHex, inCMDCommandStr=lCMDStr, inModeStr="CROSSCHECK", inLogger=inGSettings["Logger"],
                                    inRDPConfigurationItem=inGSettings["RobotRDPActive"]["RDPList"][inRDPSessionKeyStr])
    return lResult

def RDPSessionCMDRun(inRDPSessionKeyStr, inCMDStr, inModeStr="CROSSCHECK", inGSettings = None):
    """
    Send CMD command to the RDP session "RUN" window

    .. code-block:: python

        # USAGE
        from pyOpenRPA import Orchestrator

        lResultDict = Orchestrator.RDPSessionCMDRun(
            inGSettings = gSettings,
            inRDPSessionKeyStr = "RDPKey",
            inModeStr = 'LISTEN')
        # Orchestrator will send CMD to RDP and return the result (see return section)

    :param inGSettings: Global settings dict (singleton)
    :param inRDPSessionKeyStr: RDP Session string key - need for the further identification
    :param inCMDStr: Any CMD string
    :param inModeStr: Variants:
        "LISTEN" - Get result of the cmd command in result;
        "CROSSCHECK" - Check if the command was successfully sent
        "RUN" - Run without crosscheck and get clipboard
    :return: # OLD > True - CMD was executed successfully
         {
          "OutStr": <> # Result string
          "IsResponsibleBool": True|False # Flag is RDP is responsible - works only when inModeStr = CROSSCHECK
        }
    """
    inGSettings = GSettingsGet(inGSettings=inGSettings)  # Set the global settings
    lResult = {
        "OutStr": None,  # Result string
        "IsResponsibleBool": False  # Flag is RDP is responsible - works only when inModeStr = CROSSCHECK
    }
    # Check thread
    if not Core.IsProcessorThread(inGSettings=inGSettings):
        if inGSettings["Logger"]: inGSettings["Logger"].warning(f"RDP def was called not from processor queue - activity will be append in the processor queue.")
        lProcessorActivityDict = {
            "Def": RDPSessionCMDRun, # def link or def alias (look gSettings["Processor"]["AliasDefDict"])
            "ArgList": [],  # Args list
            "ArgDict": {"inRDPSessionKeyStr": inRDPSessionKeyStr,  "inCMDStr": inCMDStr, "inModeStr": inModeStr },  # Args dictionary
            "ArgGSettings": "inGSettings",  # Name of GSettings attribute: str (ArgDict) or index (for ArgList)
            "ArgLogger": None  # Name of GSettings attribute: str (ArgDict) or index (for ArgList)
        }
        inGSettings["ProcessorDict"]["ActivityList"].append(lProcessorActivityDict)
    else:
        #lResult = True
        # Calculate the session Hex
        lSessionHex = inGSettings["RobotRDPActive"]["RDPList"].get(inRDPSessionKeyStr,{}).get("SessionHex", None)
        # Run CMD
        if lSessionHex:
            lResult = Connector.SessionCMDRun(inSessionHex=lSessionHex, inCMDCommandStr=inCMDStr, inModeStr=inModeStr, inLogger=inGSettings["Logger"],
                                    inRDPConfigurationItem=inGSettings["RobotRDPActive"]["RDPList"][inRDPSessionKeyStr])
    return lResult

def RDPSessionProcessStop(inRDPSessionKeyStr, inProcessNameWEXEStr, inFlagForceCloseBool, inGSettings = None):
    """
    Send CMD command to the RDP session "RUN" window.

    .. code-block:: python

        # USAGE
        from pyOpenRPA import Orchestrator

        lResultDict = Orchestrator.RDPSessionProcessStop(
            inGSettings = gSettings,
            inRDPSessionKeyStr = "RDPKey",
            inProcessNameWEXEStr = 'notepad.exe',
            inFlagForceCloseBool = True)
        # Orchestrator will send CMD to RDP and return the result (see return section)

    :param inGSettings: Global settings dict (singleton)
    :param inRDPSessionKeyStr: RDP Session string key - need for the further identification
    :param inProcessNameWEXEStr: Process name to kill. Example: 'notepad.exe'
    :param inFlagForceCloseBool: True - force close the process. False - safe close the process
    :return: True every time
    """
    inGSettings = GSettingsGet(inGSettings=inGSettings)  # Set the global settings
    # Check thread
    if not Core.IsProcessorThread(inGSettings=inGSettings):
        if inGSettings["Logger"]: inGSettings["Logger"].warning(f"RDP def was called not from processor queue - activity will be append in the processor queue.")
        lResult = {
            "Def": RDPSessionProcessStop, # def link or def alias (look gSettings["Processor"]["AliasDefDict"])
            "ArgList": [],  # Args list
            "ArgDict": {"inRDPSessionKeyStr": inRDPSessionKeyStr,  "inProcessNameWEXEStr": inProcessNameWEXEStr, "inFlagForceCloseBool": inFlagForceCloseBool },  # Args dictionary
            "ArgGSettings": "inGSettings",  # Name of GSettings attribute: str (ArgDict) or index (for ArgList)
            "ArgLogger": None  # Name of GSettings attribute: str (ArgDict) or index (for ArgList)
        }
        inGSettings["ProcessorDict"]["ActivityList"].append(lResult)
    else:
        lResult = True
        lCMDStr = f'taskkill /im "{inProcessNameWEXEStr}" /fi "username eq %USERNAME%"'
        if inFlagForceCloseBool:
            lCMDStr+= " /F"
        # Calculate the session Hex
        lSessionHex = inGSettings["RobotRDPActive"]["RDPList"].get(inRDPSessionKeyStr,{}).get("SessionHex", None)
        # Run CMD
        if lSessionHex:
            Connector.SessionCMDRun(inSessionHex=lSessionHex, inCMDCommandStr=lCMDStr, inModeStr="CROSSCHECK", inLogger=inGSettings["Logger"], inRDPConfigurationItem=inGSettings["RobotRDPActive"]["RDPList"][inRDPSessionKeyStr])
    return lResult

def RDPSessionFileStoredSend(inRDPSessionKeyStr, inHostFilePathStr, inRDPFilePathStr, inGSettings = None):
    """
    Send file from Orchestrator session to the RDP session using shared drive in RDP (see RDP Configuration Dict, Shared drive)

    .. code-block:: python

        # USAGE
        from pyOpenRPA import Orchestrator

        lResultDict = Orchestrator.RDPSessionFileStoredSend(
            inGSettings = gSettings,
            inRDPSessionKeyStr = "RDPKey",
            inHostFilePathStr = "TESTDIR\\Test.py",
            inRDPFilePathStr = "C:\\RPA\\TESTDIR\\Test.py")
        # Orchestrator will send CMD to RDP and return the result (see return section)

    :param inGSettings: Global settings dict (singleton)
    :param inRDPSessionKeyStr: RDP Session string key - need for the further identification
    :param inHostFilePathStr: Relative or absolute path to the file location on the Orchestrator side. Example: "TESTDIR\\Test.py"
    :param inRDPFilePathStr: !Absolute! path to the destination file location on the RDP side. Example: "C:\\RPA\\TESTDIR\\Test.py"
    :return: True every time
    """
    inGSettings = GSettingsGet(inGSettings=inGSettings)  # Set the global settings
    # Check thread
    if not Core.IsProcessorThread(inGSettings=inGSettings):
        if inGSettings["Logger"]: inGSettings["Logger"].warning(f"RDP def was called not from processor queue - activity will be append in the processor queue.")
        lResult = {
            "Def": RDPSessionFileStoredSend, # def link or def alias (look gSettings["Processor"]["AliasDefDict"])
            "ArgList": [],  # Args list
            "ArgDict": {"inRDPSessionKeyStr": inRDPSessionKeyStr,  "inHostFilePathStr": inHostFilePathStr, "inRDPFilePathStr": inRDPFilePathStr },  # Args dictionary
            "ArgGSettings": "inGSettings",  # Name of GSettings attribute: str (ArgDict) or index (for ArgList)
            "ArgLogger": None  # Name of GSettings attribute: str (ArgDict) or index (for ArgList)
        }
        inGSettings["ProcessorDict"]["ActivityList"].append(lResult)
    else:
        lResult = True
        lCMDStr = CMDStr.FileStoredSend(inHostFilePath = inHostFilePathStr, inRDPFilePath = inRDPFilePathStr)
        # Calculate the session Hex
        lSessionHex = inGSettings["RobotRDPActive"]["RDPList"].get(inRDPSessionKeyStr, {}).get("SessionHex", None)
        #lSessionHex = inGlobalDict["RobotRDPActive"]["RDPList"][inRDPSessionKeyStr]["SessionHex"]
        # Run CMD
        if lSessionHex:
            Connector.SessionCMDRun(inSessionHex=lSessionHex, inCMDCommandStr=lCMDStr, inModeStr="LISTEN", inClipboardTimeoutSec = 120, inLogger=inGSettings["Logger"], inRDPConfigurationItem=inGSettings["RobotRDPActive"]["RDPList"][inRDPSessionKeyStr])
    return lResult

def RDPSessionFileStoredRecieve(inRDPSessionKeyStr, inRDPFilePathStr, inHostFilePathStr, inGSettings = None):
    """
    Recieve file from RDP session to the Orchestrator session using shared drive in RDP (see RDP Configuration Dict, Shared drive)

    .. code-block:: python

        # USAGE
        from pyOpenRPA import Orchestrator

        lResultDict = Orchestrator.RDPSessionFileStoredRecieve(
            inGSettings = gSettings,
            inRDPSessionKeyStr = "RDPKey",
            inHostFilePathStr = "TESTDIR\\Test.py",
            inRDPFilePathStr = "C:\\RPA\\TESTDIR\\Test.py")
        # Orchestrator will send CMD to RDP and return the result (see return section)

    :param inGSettings: Global settings dict (singleton)
    :param inRDPSessionKeyStr: RDP Session string key - need for the further identification
    :param inRDPFilePathStr: !Absolute! path to the destination file location on the RDP side. Example: "C:\\RPA\\TESTDIR\\Test.py"
    :param inHostFilePathStr: Relative or absolute path to the file location on the Orchestrator side. Example: "TESTDIR\\Test.py"
    :return: True every time
    """
    inGSettings = GSettingsGet(inGSettings=inGSettings)  # Set the global settings
    # Check thread
    if not Core.IsProcessorThread(inGSettings=inGSettings):
        if inGSettings["Logger"]: inGSettings["Logger"].warning(f"RDP def was called not from processor queue - activity will be append in the processor queue.")
        lResult = {
            "Def": RDPSessionFileStoredRecieve, # def link or def alias (look gSettings["Processor"]["AliasDefDict"])
            "ArgList": [],  # Args list
            "ArgDict": {"inRDPSessionKeyStr": inRDPSessionKeyStr, "inRDPFilePathStr": inRDPFilePathStr, "inHostFilePathStr": inHostFilePathStr },  # Args dictionary
            "ArgGSettings": "inGSettings",  # Name of GSettings attribute: str (ArgDict) or index (for ArgList)
            "ArgLogger": None  # Name of GSettings attribute: str (ArgDict) or index (for ArgList)
        }
        inGSettings["ProcessorDict"]["ActivityList"].append(lResult)
    else:
        lResult = True
        lCMDStr = CMDStr.FileStoredRecieve(inRDPFilePath = inRDPFilePathStr, inHostFilePath = inHostFilePathStr)
        # Calculate the session Hex
        lSessionHex = inGSettings["RobotRDPActive"]["RDPList"].get(inRDPSessionKeyStr,{}).get("SessionHex", None)
        # Run CMD
        if lSessionHex:
            Connector.SessionCMDRun(inSessionHex=lSessionHex, inCMDCommandStr=lCMDStr, inModeStr="LISTEN", inClipboardTimeoutSec = 120, inLogger=inGSettings["Logger"], inRDPConfigurationItem=inGSettings["RobotRDPActive"]["RDPList"][inRDPSessionKeyStr])
    return lResult

# # # # # # # # # # # # # # # # # # # # # # #
# # # # # Start orchestrator
# # # # # # # # # # # # # # # # # # # # # # #

def GSettingsAutocleaner(inGSettings=None):
    """
    HIDDEN Interval gSettings auto cleaner def to clear some garbage.

    :param inGSettings: Global settings dict (singleton)
    :return: None
    """
    inGSettings = GSettingsGet(inGSettings=inGSettings)  # Set the global settings
    while True:
        time.sleep(inGSettings["Autocleaner"]["IntervalSecFloat"])  # Wait for the next iteration
        lL = inGSettings["Logger"]
        lNowDatetime = datetime.datetime.now() # Get now time
        # Clean old items in Client > Session > TechnicalSessionGUIDCache
        lTechnicalSessionGUIDCacheNew = {}
        for lItemKeyStr in inGSettings["Client"]["Session"]["TechnicalSessionGUIDCache"]:
            lItemValue = inGSettings["Client"]["Session"]["TechnicalSessionGUIDCache"][lItemKeyStr]
            if (lNowDatetime - lItemValue["InitDatetime"]).total_seconds() < inGSettings["Client"]["Session"]["LifetimeSecFloat"]: # Add if lifetime is ok
                lTechnicalSessionGUIDCacheNew[lItemKeyStr]=lItemValue # Lifetime is ok - set
            else:
                if lL: lL.debug(f"Client > Session > TechnicalSessionGUIDCache > lItemKeyStr: Lifetime is expired. Remove from gSettings")  # Info
        inGSettings["Client"]["Session"]["TechnicalSessionGUIDCache"] = lTechnicalSessionGUIDCacheNew # Set updated Cache
        # Clean old items in AgentActivityReturnDict > GUIDStr > ReturnedByDatetime
        lTechnicalAgentActivityReturnDictNew = {}
        for lItemKeyStr in inGSettings["AgentActivityReturnDict"]:
            lItemValue = inGSettings["AgentActivityReturnDict"][lItemKeyStr]
            if (lNowDatetime - lItemValue["ReturnedByDatetime"]).total_seconds() < inGSettings["Autocleaner"]["AgentActivityReturnLifetimeSecFloat"]: # Add if lifetime is ok
                lTechnicalAgentActivityReturnDictNew[lItemKeyStr]=lItemValue # Lifetime is ok - set
            else:
                if lL: lL.debug(f"AgentActivityReturnDict lItemKeyStr: Lifetime is expired. Remove from gSettings")  # Info
        inGSettings["AgentActivityReturnDict"] = lTechnicalAgentActivityReturnDictNew # Set updated Cache
    # # # # # # # # # # # # # # # # # # # # # # # # # #

from .. import __version__ # Get version from the package

def Start(inDumpRestoreBool = True, inRunAsAdministratorBool = True):
    """
    Start the orchestrator threads execution

    :param inDumpRestoreBool: True - restore data from the dumo
    :param inRunAsAdministratorBool: True - rerun as admin if not
    :return:
    """
    Orchestrator(inDumpRestoreBool = True, inRunAsAdministratorBool = True)

def Orchestrator(inGSettings=None, inDumpRestoreBool = True, inRunAsAdministratorBool = True):
    """
    Main def to start orchestrator

    :param inGSettings:
    :param inDumpRestoreBool:
    :param inRunAsAdministratorBool:
    :return:
    """
    lL = inGSettings["Logger"]
    # https://stackoverflow.com/questions/130763/request-uac-elevation-from-within-a-python-script
    License.ConsoleVerify()
    if not OrchestratorIsAdmin() and inRunAsAdministratorBool==True:
        OrchestratorRerunAsAdmin()
    else:
        # Code of your program here
        inGSettings = GSettingsGet(inGSettings=inGSettings)  # Set the global settings
        #mGlobalDict = Settings.Settings(sys.argv[1])
        global gSettingsDict
        gSettingsDict = inGSettings # Alias for old name in alg
        inGSettings["VersionStr"] = __version__
        #Logger alias
        lL = gSettingsDict["Logger"]

        if lL: lL.info("Link the gSettings in submodules")  #Logging
        Processor.gSettingsDict = gSettingsDict
        Timer.gSettingsDict = gSettingsDict
        Timer.Processor.gSettingsDict = gSettingsDict
        Server.gSettingsDict = gSettingsDict
        Server.ProcessorOld.gSettingsDict = gSettingsDict # Backward compatibility

        #Backward compatibility - restore in Orc def if old def
        if inDumpRestoreBool == True:
            OrchestratorSessionRestore(inGSettings=inGSettings)

        # Init SettingsUpdate defs from file list (after RDP restore)
        lSettingsUpdateFilePathList = gSettingsDict.get("OrchestratorStart", {}).get("DefSettingsUpdatePathList",[])
        lSubmoduleFunctionName = "SettingsUpdate"
        lSettingsPath = "\\".join(os.path.join(os.getcwd(), __file__).split("\\")[:-1])
        for lModuleFilePathItem in lSettingsUpdateFilePathList:  # Import defs with try catch
            try:  # Try to init - go next if error and log in logger
                lModuleName = lModuleFilePathItem[0:-3]
                lFileFullPath = os.path.join(lSettingsPath, lModuleFilePathItem)
                lTechSpecification = importlib.util.spec_from_file_location(lModuleName, lFileFullPath)
                lTechModuleFromSpec = importlib.util.module_from_spec(lTechSpecification)
                lTechSpecificationModuleLoader = lTechSpecification.loader.exec_module(lTechModuleFromSpec)
                if lSubmoduleFunctionName in dir(lTechModuleFromSpec):
                    # Run SettingUpdate function in submodule
                    getattr(lTechModuleFromSpec, lSubmoduleFunctionName)(gSettingsDict)
            except Exception as e:
                if lL: lL.exception(f"Error when init .py file in orchestrator '{lModuleFilePathItem}'. Exception is below:")

        # Turn on backward compatibility
        BackwardCompatibility.Update(inGSettings= gSettingsDict)

        # Append Orchestrator def to ProcessorDictAlias
        lModule = sys.modules[__name__]
        lModuleDefList = dir(lModule)
        for lItemDefNameStr in lModuleDefList:
            # Dont append alias for defs Orchestrator and ___deprecated_orchestrator_start__
            if lItemDefNameStr not in ["Orchestrator", "___deprecated_orchestrator_start__"]:
                lItemDef = getattr(lModule,lItemDefNameStr)
                if callable(lItemDef): inGSettings["ProcessorDict"]["AliasDefDict"][lItemDefNameStr]=lItemDef

        #Load all defs from sys.modules
        ActivityItemDefAliasModulesLoad()

        #Инициализация настроечных параметров
        gSettingsDict["ServerDict"]["WorkingDirectoryPathStr"] = os.getcwd() # Set working directory in g settings

        #Инициализация сервера (инициализация всех интерфейсов)
        lListenDict = gSettingsDict.get("ServerDict",{}).get("ListenDict",{})
        for lItemKeyStr in lListenDict:
            lItemDict = lListenDict[lItemKeyStr]
            lThreadServer = Server.RobotDaemonServer(lItemKeyStr, gSettingsDict)
            lThreadServer.start()
            gSettingsDict["ServerDict"]["ServerThread"] = lThreadServer
            lItemDict["ServerInstance"] = lThreadServer

        # Init the RobotScreenActive in another thread
        lRobotScreenActiveThread = threading.Thread(target= Monitor.CheckScreen)
        lRobotScreenActiveThread.daemon = True # Run the thread in daemon mode.
        lRobotScreenActiveThread.start() # Start the thread execution.
        if lL: lL.info("Robot Screen active has been started")  #Logging

        # Init the RobotRDPActive in another thread
        lRobotRDPThreadControlDict = {"ThreadExecuteBool":True} # inThreadControlDict = {"ThreadExecuteBool":True}
        lRobotRDPActiveThread = threading.Thread(target= RobotRDPActive.RobotRDPActive, kwargs={"inGSettings":gSettingsDict, "inThreadControlDict":lRobotRDPThreadControlDict})
        lRobotRDPActiveThread.daemon = True # Run the thread in daemon mode.
        lRobotRDPActiveThread.start() # Start the thread execution.
        if lL: lL.info("Robot RDP active has been started")  #Logging



        # Init autocleaner in another thread
        lAutocleanerThread = threading.Thread(target= GSettingsAutocleaner, kwargs={"inGSettings":gSettingsDict})
        lAutocleanerThread.daemon = True # Run the thread in daemon mode.
        lAutocleanerThread.start() # Start the thread execution.
        if lL: lL.info("Autocleaner thread has been started")  #Logging

        # Set flag that orchestrator has been initialized
        inGSettings["HiddenIsOrchestratorInitializedBool"] = True

        # Orchestrator start activity
        if lL: lL.info("Orchestrator start activity run")  #Logging
        for lActivityItem in gSettingsDict["OrchestratorStart"]["ActivityList"]:
            # Processor.ActivityListOrDict(lActivityItem)
            Processor.ActivityListExecute(inGSettings=gSettingsDict,inActivityList=[BackwardCompatibility.v1_2_0_ProcessorOld2NewActivityDict(lActivityItem)])
        # Processor thread
        lProcessorThread = threading.Thread(target= Processor.ProcessorRunSync, kwargs={"inGSettings":gSettingsDict, "inRobotRDPThreadControlDict":lRobotRDPThreadControlDict})
        lProcessorThread.daemon = True # Run the thread in daemon mode.
        lProcessorThread.start() # Start the thread execution.
        if lL: lL.info("Processor has been started (ProcessorDict)")  #Logging

        # Processor monitor thread
        lProcessorMonitorThread = threading.Thread(target= Processor.ProcessorMonitorRunSync, kwargs={"inGSettings":gSettingsDict})
        lProcessorMonitorThread.daemon = True # Run the thread in daemon mode.
        lProcessorMonitorThread.start() # Start the thread execution.
        if lL: lL.info("Processor monitor has been started")  #Logging

        # Scheduler loop
        lSchedulerThread = threading.Thread(target= __deprecated_orchestrator_loop__)
        lSchedulerThread.daemon = True # Run the thread in daemon mode.
        lSchedulerThread.start() # Start the thread execution.
        if lL: lL.info("Scheduler (old) loop start")  #Logging

        # Schedule (new) loop
        lScheduleThread = threading.Thread(target= __schedule_loop__)
        lScheduleThread.daemon = True # Run the thread in daemon mode.
        lScheduleThread.start() # Start the thread execution.
        if lL: lL.info("Schedule module (new) loop start")  #Logging

        # Restore state for process
        for lProcessKeyTuple in inGSettings["ManagersProcessDict"]:
            lProcess = inGSettings["ManagersProcessDict"][lProcessKeyTuple]
            lProcess.StatusCheckIntervalRestore()
            lThread = threading.Thread(target= lProcess.StatusRestore)
            lThread.start()

        # Init debug thread (run if "init_dubug" file exists)
        Debugger.LiveDebugCheckThread(inGSettings=GSettingsGet())

def __schedule_loop__():
    while True:
        schedule.run_pending()
        time.sleep(3)

# Backward compatibility below to 1.2.7
def __deprecated_orchestrator_loop__():
    lL = OrchestratorLoggerGet()
    inGSettings = GSettingsGet()
    lDaemonLoopSeconds = gSettingsDict["SchedulerDict"]["CheckIntervalSecFloat"]
    lDaemonActivityLogDict = {}  # Словарь отработанных активностей, ключ - кортеж (<activityType>, <datetime>, <processPath || processName>, <processArgs>)
    lDaemonLastDateTime = datetime.datetime.now()
    gDaemonActivityLogDictRefreshSecInt = 10  # The second period for clear lDaemonActivityLogDict from old items
    gDaemonActivityLogDictLastTime = time.time()  # The second perioad for clean lDaemonActivityLogDict from old items
    while True:
        try:
            lCurrentDateTime = datetime.datetime.now()
            # Циклический обход правил
            lFlagSearchActivityType = True
            # Periodically clear the lDaemonActivityLogDict
            if time.time() - gDaemonActivityLogDictLastTime >= gDaemonActivityLogDictRefreshSecInt:
                gDaemonActivityLogDictLastTime = time.time()  # Update the time
                for lIndex, lItem in enumerate(lDaemonActivityLogDict):
                    if lItem["ActivityEndDateTime"] and lCurrentDateTime <= lItem["ActivityEndDateTime"]:
                        pass
                        # Activity is actual - do not delete now
                    else:
                        # remove the activity - not actual
                        lDaemonActivityLogDict.pop(lIndex, None)
            lIterationLastDateTime = lDaemonLastDateTime  # Get current datetime before iterator (need for iterate all activities in loop)
            # Iterate throught the activity list
            for lIndex, lItem in enumerate(gSettingsDict["SchedulerDict"]["ActivityTimeList"]):
                try:
                    # Prepare GUID of the activity
                    lGUID = None
                    if "GUID" in lItem and lItem["GUID"]:
                        lGUID = lItem["GUID"]
                    else:
                        lGUID = str(uuid.uuid4())
                        lItem["GUID"] = lGUID

                    # Проверка дней недели, в рамках которых можно запускать активность
                    lItemWeekdayList = lItem.get("WeekdayList", [0, 1, 2, 3, 4, 5, 6])
                    if lCurrentDateTime.weekday() in lItemWeekdayList:
                        if lFlagSearchActivityType:
                            #######################################################################
                            # Branch 1 - if has TimeHH:MM
                            #######################################################################
                            if "TimeHH:MMStr" in lItem:
                                # Вид активности - запуск процесса
                                # Сформировать временной штамп, относительно которого надо будет проверять время
                                # часовой пояс пока не учитываем
                                lActivityDateTime = datetime.datetime.strptime(lItem["TimeHH:MMStr"], "%H:%M")
                                lActivityDateTime = lActivityDateTime.replace(year=lCurrentDateTime.year,
                                                                              month=lCurrentDateTime.month,
                                                                              day=lCurrentDateTime.day)
                                # Убедиться в том, что время наступило
                                if (
                                        lActivityDateTime >= lDaemonLastDateTime and
                                        lCurrentDateTime >= lActivityDateTime):
                                    # Log info about activity
                                    if lL: lL.info(
                                        f"Scheduler:: Activity list is started in new thread. Parameters are not available to see.")  # Logging
                                    # Do the activity
                                    lThread = threading.Thread(target=Processor.ActivityListExecute,
                                                               kwargs={"inGSettings": inGSettings,
                                                                       "inActivityList": lItem["ActivityList"]})
                                    lThread.start()
                                    lIterationLastDateTime = datetime.datetime.now()  # Set the new datetime for the new processor activity
                except Exception as e:
                    if lL: lL.exception(
                        f"Scheduler: Exception has been catched in Scheduler module when activity time item was initialising. ActivityTimeItem is {lItem}")
            lDaemonLastDateTime = lIterationLastDateTime  # Set the new datetime for the new processor activity
            # Уснуть до следующего прогона
            time.sleep(lDaemonLoopSeconds)
        except Exception as e:
            if lL: lL.exception(f"Scheduler: Exception has been catched in Scheduler module. Global error")

# Backward compatibility below to 1.2.0
def __deprecated_orchestrator_start__():
    lSubmoduleFunctionName = "Settings"
    lFileFullPath = sys.argv[1]
    lModuleName = (lFileFullPath.split("\\")[-1])[0:-3]
    lTechSpecification = importlib.util.spec_from_file_location(lModuleName, lFileFullPath)
    lTechModuleFromSpec = importlib.util.module_from_spec(lTechSpecification)
    lTechSpecificationModuleLoader = lTechSpecification.loader.exec_module(lTechModuleFromSpec)
    gSettingsDict = None
    if lSubmoduleFunctionName in dir(lTechModuleFromSpec):
        # Run SettingUpdate function in submodule
        gSettingsDict = getattr(lTechModuleFromSpec, lSubmoduleFunctionName)()
    #################################################
    Orchestrator(inGSettings=gSettingsDict) # Call the orchestrator
