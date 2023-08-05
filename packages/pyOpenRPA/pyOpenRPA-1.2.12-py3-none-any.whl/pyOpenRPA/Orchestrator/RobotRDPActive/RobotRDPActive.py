from pyOpenRPA.Robot import UIDesktop
import os
import time # Time wait operations
from . import ConnectorExceptions # Exceptions classes
from . import Connector
from . import Processor # Module for process some functions on thr RDP
from . import Recovery
from .. import __Orchestrator__
# Main function
# inThreadControlDict = {"ThreadExecuteBool":True}
def RobotRDPActive(inGSettings, inThreadControlDict):
    # inGSettings = {
    # ... "RobotRDPActive": {} ...
    # }
    lL = inGSettings["Logger"] #Logger alias
    Processor.gSettings = inGSettings  # Set gSettings in processor module
    mGSettingsRDPActiveDict = inGSettings["RobotRDPActive"] # Get configuration from global dict settings
    # Global error handler
    try:
        ######## Init the RDP List
        lNewRDPList = {}
        for lRDPSessionKeyStrItem in mGSettingsRDPActiveDict["RDPList"]:
            lConfigurationItem = mGSettingsRDPActiveDict["RDPList"][lRDPSessionKeyStrItem]
            lAddToNewRDPDict = True
            if "SessionHex" not in lConfigurationItem: lAddToNewRDPDict = False # 2020.08.03 fix: Init the Session hex field. If no SessionHex - trash in structure - remove
            if lConfigurationItem["SessionHex"] is None or lConfigurationItem["SessionHex"] == "": # Minor fix - need for restore existed RDP sessions
                lConfigurationItem["SessionIsWindowExistBool"] = False  # Flag that session is not started
                lConfigurationItem["SessionIsWindowResponsibleBool"] = False  # Flag that session is not started
                lConfigurationItem["SessionHex"] = " 77777sdfsdf77777dsfdfsf77777777"  # Flag that session is not started
            if lAddToNewRDPDict:
                lNewRDPList[lRDPSessionKeyStrItem] = lConfigurationItem
        mGSettingsRDPActiveDict["RDPList"] = lNewRDPList # Update the structure
        ##########
        # Run monitor - main loop
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        inGlobalDict = mGSettingsRDPActiveDict # Compatibility
        inListUpdateTimeout = 1 # Compatibility
        lFlagWhile = True
        lResponsibilityCheckLastSec = time.time()  # Get current time for check interval
        while lFlagWhile:
            try:
                if inThreadControlDict["ThreadExecuteBool"] == True:
                    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
                    # Check RDP window is OK - reconnect if connection was lost
                    lUIOSelectorList = []
                    lRDPConfigurationDictList = []
                    lRDPSessionKeyList = []
                    # Prepare selectors list for check
                    for lRDPSessionKeyStrItem in inGlobalDict["RDPList"]:
                        lRDPSessionKeyList.append(lRDPSessionKeyStrItem)
                        lItem = inGlobalDict["RDPList"][lRDPSessionKeyStrItem]
                        lRDPConfigurationDictList.append(lItem) # Add RDP Configuration in list
                        lUIOSelectorList.append([{"title_re": f"{lItem['SessionHex']}.*", "backend": "win32"}])
                    # Run wait command
                    lRDPDissappearList = UIDesktop.UIOSelectorsSecs_WaitDisappear_List(lUIOSelectorList, inListUpdateTimeout)
                    for lItem in lRDPDissappearList: # Reconnect if connection was lost
                        lRDPSessionKeyStr = lRDPSessionKeyList[lItem]
                        lRDPConfigurationDict = lRDPConfigurationDictList[lItem] # Get RDP Configuration list
                        lRDPConfigurationDict["SessionIsWindowExistBool"] = False  # Set flag that session is disconnected
                        # Check if RDP window is not ignored
                        if not lRDPConfigurationDict["SessionIsIgnoredBool"]:
                            try:
                                Connector.Session(lRDPConfigurationDict, inScreenSize550x350Bool = True)
                                lRDPConfigurationDict["SessionIsWindowExistBool"] = True  # Flag that session is started
                                if lL: lL.info(f"Host: {lRDPConfigurationDict['Host']}, Login: {lRDPConfigurationDict['Login']}, SessionHex: {str(lRDPConfigurationDict['SessionHex'])}:: Session has been initialized!")  #Logging
                            # catch ConnectorExceptions.SessionWindowNotExistError
                            except ConnectorExceptions.SessionWindowNotExistError as e:
                                lRDPConfigurationDict["SessionIsWindowExistBool"] = False  # Set flag that session is disconnected
                                if lL: lL.warning(f"Host: {lRDPConfigurationDict['Host']}, Login: {lRDPConfigurationDict['Login']}, SessionHex: {str(lRDPConfigurationDict['SessionHex'])}:: Session is not exist! Mark the retry")  #Logging
                                # Recovery operations
                                Recovery.RetryMark(inRDPSessionKeyStr=lRDPSessionKeyStr,inGSettings=inGSettings)
                                if Recovery.RetryIsTriggered(inRDPSessionKeyStr=lRDPSessionKeyStr,inGSettings=inGSettings) == True:
                                    if lL: lL.warning(f"!ATTENTION! Host: {lRDPConfigurationDict['Host']}, Login: {lRDPConfigurationDict['Login']}; RDP is not responsible for many times - run recovery mode")
                                    Recovery.RetryHostClear(inHostStr=lRDPConfigurationDict['Host'],inGSettings=inGSettings) # Clear the stat about current host
                                    if inGSettings["RobotRDPActive"]["RecoveryDict"]["DoDict"]["OSRemotePCRestart"] == True:
                                        if lL: lL.warning(f"!ATTENTION! Host: {lRDPConfigurationDict['Host']}, Send signal to restart remote PC.")
                                        __Orchestrator__.OSRemotePCRestart(inLogger=lL,inHostStr=lRDPConfigurationDict['Host'],inForceBool=True)
                            # general exceptions
                            except Exception as e:
                                if lL: lL.exception(f"!!! ATTENTION !!! Unrecognized error")  #Logging
                                pass
                    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
                    Connector.SystemRDPWarningClickOk() # Click all warning messages
                    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
                    # Check if RDP session is full screen (if is not ignored)
                    if inGlobalDict["FullScreenRDPSessionKeyStr"] is not None:
                        lRDPSessionKeyStr = inGlobalDict["FullScreenRDPSessionKeyStr"] # Get the RDPSessionKeyStr
                        if lRDPSessionKeyStr in inGlobalDict["RDPList"]: # Session Key is in dict
                            lRDPConfigurationDict = inGlobalDict["RDPList"][lRDPSessionKeyStr]
                            #if not lRDPConfigurationDict["SessionIsIgnoredBool"]: # Session is not ignored
                            # Check if full screen
                            lIsFullScreenBool = Connector.SessionIsFullScreen(inSessionHexStr=lRDPConfigurationDict["SessionHex"])
                            if not lIsFullScreenBool: # If not the full screen
                                # Check all RDP window and minimize it
                                for lRDPSessionKeyStrItem in inGlobalDict["RDPList"]:
                                    lRDPConfigurationDictItem = inGlobalDict["RDPList"][lRDPSessionKeyStrItem]
                                    if Connector.SessionIsFullScreen(inSessionHexStr=lRDPConfigurationDictItem["SessionHex"]):
                                        if inThreadControlDict["ThreadExecuteBool"] == True: # TEST FEATURE BEFORE ONE THREAD INTEGRATION
                                            Connector.SessionScreenSize_X_Y_W_H(inSessionHex=lRDPConfigurationDictItem["SessionHex"], inXInt=10, inYInt=10,
                                                                      inWInt=550,
                                                                      inHInt=350)  # Prepare little window
                                # Set full screen for new window
                                if inThreadControlDict["ThreadExecuteBool"] == True: # TEST FEATURE BEFORE ONE THREAD INTEGRATION
                                    Connector.SessionScreenFull(inSessionHex=lRDPConfigurationDict["SessionHex"], inLogger= inGSettings["Logger"], inRDPConfigurationItem=inGlobalDict["RDPList"][lRDPSessionKeyStrItem])
                    else:
                        # Check all RDP window and minimize it
                        for lRDPSessionKeyStrItem in inGlobalDict["RDPList"]:
                            lRDPConfigurationDictItem = inGlobalDict["RDPList"][lRDPSessionKeyStrItem]
                            if Connector.SessionIsFullScreen(inSessionHexStr=lRDPConfigurationDictItem["SessionHex"]) or Connector.SessionIsMinimizedScreen(inSessionHexStr=lRDPConfigurationDictItem["SessionHex"]): # If window is minimized - restore # if window in full screen - resize
                                if inThreadControlDict["ThreadExecuteBool"] == True:  # TEST FEATURE BEFORE ONE THREAD INTEGRATION
                                    Connector.SessionScreenSize_X_Y_W_H(inSessionHex=lRDPConfigurationDictItem["SessionHex"],
                                                                    inXInt=10, inYInt=10,
                                                                    inWInt=550,
                                                                    inHInt=350)  # Prepare little window
                    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
                    # Iterate the activity list in robot RDP active
                    lActivityListNew = []
                    lActivityListOld = inGlobalDict["ActivityList"]
                    inGlobalDict["ActivityList"] = []
                    for lActivityItem in lActivityListOld:
                        lSubmoduleFunctionName = lActivityItem["DefNameStr"]
                        if lSubmoduleFunctionName in dir(Processor):
                            lActivityItemResult = None # init the variable
                            try: # try to run function from Processor.py
                                lActivityItemResult = getattr(Processor, lSubmoduleFunctionName)(
                                    *lActivityItem["ArgList"], **lActivityItem["ArgDict"])
                            except Exception as e:
                                if lL: lL.exception(f"RDP::main: Exception when run def in processor.py - activity will be ignored. Activity item: {lActivityItem}")  #Logging
                                lActivityItemResult = True # True - clear from repeat list
                            lActivityItemResultType = type(lActivityItemResult)
                            # Check if Result is bool
                            if lActivityItemResultType is bool:
                                if not lActivityItemResult:
                                    # Activity is not done - add to list (retry in future)
                                    lActivityListNew.append(lActivityItem)
                    inGlobalDict["ActivityList"] = lActivityListNew  # Override the value
                    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
            except RuntimeError as e:
                # case noGUI error passed - do nothing
                if lL: lL.warning(f"Host session has lost the GUI")  #Logging
            finally:
                # Wait for the next iteration
                time.sleep(0.7)
        # Scheduler.Scheduler(mGSettingsRDPActiveDict["Scheduler"])  # Init & Run Scheduler TODO remake in processor list
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        #Monitor.Monitor(mGSettingsRDPActiveDict, 1)
    except Exception as e:
        if lL: lL.exception(f"!!! ATTENTION !!! Global error handler - look at code")  #Logging