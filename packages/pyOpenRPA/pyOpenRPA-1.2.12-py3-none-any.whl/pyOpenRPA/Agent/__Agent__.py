import threading, socket, getpass, sys, uuid, subprocess, base64, psutil, getpass, time
from . import O2A, A2O # Data flow Orchestrator To Agent
from . import Processor # Processor Queue
from ..Tools import Usage
from ..Tools import License
from subprocess import CREATE_NEW_CONSOLE # Flag to create new process in another CMD
import os

gSettings = None

# Create binary file by the base64 string (safe for JSON transmition)
def OSFileBinaryDataBase64StrCreate(inFilePathStr, inFileDataBase64Str,inGSettings = None):
    """
    Create binary file by the base64 string (safe for JSON transmition)

    """
    lFile = open(inFilePathStr, "wb")
    lFile.write(base64.b64decode(inFileDataBase64Str))
    lFile.close()
    lL = inGSettings.get("Logger", None) if type(inGSettings) is dict else None
    lMessageStr = f"AGENT Binary file {inFilePathStr} has been created."
    if lL: lL.info(lMessageStr)
    A2O.LogListSend(inGSettings=inGSettings, inLogList=[lMessageStr])

# Append binary file by the base64 string (safe for JSON transmition)
def OSFileBinaryDataBase64StrAppend(inFilePathStr, inFileDataBase64Str,inGSettings = None):
    """
    Create binary file by the base64 string (safe for JSON transmition)

    """
    lFile = open(inFilePathStr, "ab")
    lFile.write(base64.b64decode(inFileDataBase64Str))
    lFile.close()
    lL = inGSettings.get("Logger", None) if type(inGSettings) is dict else None
    lMessageStr = f"AGENT Binary file {inFilePathStr} has been appended."
    if lL: lL.info(lMessageStr)
    A2O.LogListSend(inGSettings=inGSettings, inLogList=[lMessageStr])

# Create text file by the string
def OSFileTextDataStrCreate(inFilePathStr, inFileDataStr, inEncodingStr = "utf-8",inGSettings = None):
    """
    Create text file in the agent GUI session

    :param inFilePathStr: File abs path
    :param inFileDataStr: File data text content
    :param inEncodingStr:  Write file encoding
    :param inGSettings: global settings of the Agent (singleton)
    :return:
    """
    lFile = open(inFilePathStr, "w", encoding=inEncodingStr)
    lFile.write(inFileDataStr)
    lFile.close()
    lL = inGSettings.get("Logger", None) if type(inGSettings) is dict else None
    lMessageStr = f"AGENT Text file {inFilePathStr} has been created."
    if lL: lL.info(lMessageStr)
    A2O.LogListSend(inGSettings=inGSettings, inLogList=[lMessageStr])

def OSFileBinaryDataBase64StrReceive(inFilePathStr, inGSettings=None):
    """
    Read binary file and encode in base64 to transmit (safe for JSON transmition)

    :param inFilePathStr: File path to read
    :param inGSettings:  global settings of the Agent (singleton)
    :return: File content in string base64 format (use base64.b64decode to decode data). Return None if file is not exist
    """
    lL = inGSettings.get("Logger", None) if type(inGSettings) is dict else None
    lFileDataBase64Str = None
    if os.path.exists(inFilePathStr):
        lFile = open(inFilePathStr, "rb")
        lFileDataBytes = lFile.read()
        lFile.close()
        lFileDataBase64Str = base64.b64encode(lFileDataBytes).decode("utf-8")
        lMessageStr = f"OSFileBinaryDataBase64StrReceive: file {inFilePathStr} has been read"
        if lL: lL.debug(lMessageStr)
        #A2O.LogListSend(inGSettings=inGSettings, inLogList=[lMessageStr])
    else: 
        if lL: lL.debug(f"OSFileBinaryDataBase64StrReceive: file {inFilePathStr} is not exists - return None")
    return lFileDataBase64Str

def OSFileMTimeGet(inFilePathStr: str) -> float or None:
    """
    Read file modification time timestamp format (float)

    :param inFilePathStr: File path to read
    :return: timestamp (float) Return None if file is not exist
    """
    global gSettings
    lL = gSettings.get("Logger", None) if type(gSettings) is dict else None
    lFileMTimeFloat = None
    if os.path.exists(inFilePathStr):
        lFileMTimeFloat = os.path.getmtime(inFilePathStr)
        if lL: lL.debug(f"OSFileMTimeGet: file {inFilePathStr} has been read")
    else: 
        if lL: lL.debug(f"OSFileMTimeGet: file {inFilePathStr} is not exists - return None")
    return lFileMTimeFloat

def OSFileTextDataStrReceive(inFilePathStr, inEncodingStr="utf-8", inGSettings=None):
    """
    Read text file in the agent GUI session

    :param inFilePathStr: File abs path
    :param inEncodingStr:  Read file encoding. Default utf-8
    :param inGSettings: global settings of the Agent (singleton)
    :return: File text content in string format (use base64.b64decode to decode data). Return None if file is not exist
    """
    lFileDataStr = None
    lL = inGSettings.get("Logger", None) if type(inGSettings) is dict else None
    if os.path.exists(inFilePathStr):
        lFile = open(inFilePathStr, "r", encoding=inEncodingStr)
        lFileDataStr = lFile.read()
        lFile.close()
        lMessageStr = f"OSFileTextDataStrReceive: file {inFilePathStr} has been read"
        if lL: lL.info(lMessageStr)
        #A2O.LogListSend(inGSettings=inGSettings, inLogList=[lMessageStr])
    else:
        if lL: lL.info(f"OSFileTextDataStrReceive: file {inFilePathStr} is not exists - return None")
    return lFileDataStr

# Send CMD to OS. Result return to log + Orchestrator by the A2O connection
def OSCMD(inCMDStr, inRunAsyncBool=True, inGSettings = None, inSendOutputToOrchestratorLogsBool = True, inCMDEncodingStr = "cp1251", inCaptureBool = True):
    """
    Execute CMD on the Agent daemonic process

    :param inCMDStr: command to execute on the Agent session
    :param inRunAsyncBool: True - Agent processor don't wait execution; False - Agent processor wait cmd execution
    :param inGSettings: Agent global settings dict
    :param inSendOutputToOrchestratorLogsBool: True - catch cmd execution output and send it to the Orchestrator logs; Flase - else case; Default True
    :param inCMDEncodingStr: Set the encoding of the DOS window on the Agent server session. Windows is beautiful :) . Default is "cp1251" early was "cp866" - need test
    :param inCaptureBool: !ATTENTION! If you need to start absolutely encapsulated app - set this flag as False. If you set True - the app output will come to Agent
    :return:
    """
    lResultStr = ""
    # New feature
    if inSendOutputToOrchestratorLogsBool == False and inCaptureBool == False:
        inCMDStr = f"start {inCMDStr}"
    # Subdef to listen OS result
    def _CMDRunAndListenLogs(inCMDStr, inSendOutputToOrchestratorLogsBool, inCMDEncodingStr,  inGSettings = None, inCaptureBool = True):
        lL = inGSettings.get("Logger",None) if type(inGSettings) is dict else None
        lResultStr = ""
        lOSCMDKeyStr = str(uuid.uuid4())[0:4].upper()
        lCMDProcess = None
        if inCaptureBool == True:
            lCMDProcess = subprocess.Popen(f'cmd /c {inCMDStr}', stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        else:
            lCMDProcess = subprocess.Popen(f'cmd /c {inCMDStr}', stdout=None, stderr=None,
                                           creationflags=CREATE_NEW_CONSOLE)
        lListenBool = True
        lMessageStr = f"{lOSCMDKeyStr}: # # # # AGENT CMD Process has been STARTED # # # # "
        if lL: lL.info(lMessageStr)
        if inSendOutputToOrchestratorLogsBool == True:  # Capturing can be turned on!
            A2O.LogListSend(inGSettings=inGSettings,inLogList=[lMessageStr])
        lMessageStr = f"{lOSCMDKeyStr}: {inCMDStr}"
        if lL: lL.info(lMessageStr)
        if inSendOutputToOrchestratorLogsBool == True:  # Capturing can be turned on!
            A2O.LogListSend(inGSettings=inGSettings, inLogList=[lMessageStr])
        while lListenBool:
            #if inSendOutputToOrchestratorLogsBool == True: # Capturing can be turned on!
            if inCaptureBool == True: # Capturing can be turned on!
                lOutputLineBytes = lCMDProcess.stdout.readline()
                if lOutputLineBytes == b"":
                    lListenBool = False
                lStr = lOutputLineBytes.decode(inCMDEncodingStr) # was cp866, on win server don't work properly - set cp1251
                if lStr.endswith("\n"): lStr = lStr[:-1]
                lMessageStr = f"{lOSCMDKeyStr}: {lStr}"
                if lL: lL.info(lMessageStr)
                if inSendOutputToOrchestratorLogsBool == True:  # Capturing can be turned on!
                    A2O.LogListSend(inGSettings=inGSettings, inLogList=[lMessageStr])
                lResultStr+=lStr
            else: #Capturing is not turned on - wait until process will be closed
                lCMDProcessPoll = lCMDProcess.poll()
                if lCMDProcessPoll is None: # Process is alive - wait
                    time.sleep(2)
                else:
                    lListenBool = False
        lMessageStr = f"{lOSCMDKeyStr}: # # # # AGENT CMD Process has been FINISHED # # # # "
        if lL: lL.info(lMessageStr)
        if inSendOutputToOrchestratorLogsBool == True:  # Capturing can be turned on!
            A2O.LogListSend(inGSettings=inGSettings, inLogList=[lMessageStr])
        return lResultStr
    # New call
    if inRunAsyncBool:
        lThread = threading.Thread(target=_CMDRunAndListenLogs, kwargs={"inCMDStr":inCMDStr, "inGSettings":inGSettings, "inSendOutputToOrchestratorLogsBool":inSendOutputToOrchestratorLogsBool, "inCMDEncodingStr":inCMDEncodingStr, "inCaptureBool": inCaptureBool })
        lThread.start()
        lResultStr="ActivityList has been started in async mode - no output is available here."
    else:
        lResultStr = _CMDRunAndListenLogs(inCMDStr=inCMDStr, inGSettings=inGSettings, inSendOutputToOrchestratorLogsBool = inSendOutputToOrchestratorLogsBool, inCMDEncodingStr = inCMDEncodingStr, inCaptureBool=inCaptureBool)
    #lCMDCode = "cmd /c " + inCMDStr
    #subprocess.Popen(lCMDCode)
    #lResultCMDRun = 1  # os.system(lCMDCode)
    return lResultStr


def ProcessWOExeUpperUserListGet():
    """
    Return the process list only for the current user (where Agent is running) without .EXE in upper case. Can use in ActivityItem from Orchestrator to Agent

    :param inProcessNameWOExeList:
    :return: list of the agent user process in upper case without .EXE. Example ["NOTEPAD","..."],

    """
    lUserNameStr = getpass.getuser()
    lResult = []
    # Create updated list for quick check
    lProcessNameWOExeList = []
    # Iterate over the list
    for proc in psutil.process_iter():
        try:
            # Fetch process details as dict
            pinfo = proc.as_dict(attrs=['pid', 'name', 'username'])
            # Add if empty inProcessNameWOExeList or if process in inProcessNameWOExeList
            lUserNameWODomainStr = proc.username().split('\\')[-1]
            if lUserNameWODomainStr == lUserNameStr:
                lResult.append(pinfo['name'][:-4].upper())
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
           pass
    return lResult

# Main def
def Agent(inGSettings):
    License.ConsoleVerify()
    lL = inGSettings["Logger"]
    global gSettings
    gSettings = inGSettings
    # Append Orchestrator def to ProcessorDictAlias
    lModule = sys.modules[__name__]
    lModuleDefList = dir(lModule)
    for lItemDefNameStr in lModuleDefList:
        # Dont append alias for defs Agent
        if lItemDefNameStr not in ["Agent"]:
            lItemDef = getattr(lModule,lItemDefNameStr)
            if callable(lItemDef): inGSettings["ProcessorDict"]["AliasDefDict"][lItemDefNameStr]=lItemDef

    # Detect Machine host name and username
    inGSettings["AgentDict"]["HostNameUpperStr"] = socket.gethostname().upper()
    inGSettings["AgentDict"]["UserUpperStr"] = getpass.getuser().upper()

    # Processor thread
    lProcessorThread = threading.Thread(target= Processor.ProcessorRunSync, kwargs={"inGSettings":inGSettings})
    lProcessorThread.daemon = True # Run the thread in daemon mode.
    lProcessorThread.start() # Start the thread execution.
    if lL: lL.info("Processor has been started (ProcessorDict)")  #Logging

    # Start thread to wait data from Orchestrator (O2A)
    lO2AThread = threading.Thread(target=O2A.O2A_Loop, kwargs={"inGSettings":inGSettings})
    lO2AThread.start()
    Usage.Process(inComponentStr="Agent")
    
    
    # Send log that Agent has been started
    A2O.LogListSend(inGSettings=inGSettings, inLogList=[f'Host: {inGSettings["AgentDict"]["HostNameUpperStr"]}, User: {inGSettings["AgentDict"]["UserUpperStr"]}, Agent has been started.'])