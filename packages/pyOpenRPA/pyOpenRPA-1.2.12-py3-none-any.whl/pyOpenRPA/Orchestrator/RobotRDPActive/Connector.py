#Import parent folder to import current / other packages
from pyOpenRPA.Robot import UIDesktop #Lib to access RDP window
from . import ConnectorExceptions # Exceptions classes
import os #os for process run
import uuid #temp id for Template.rdp
import tempfile #Temporary location
import subprocess
from . import Clipboard # Clipboard functions get/set
import keyboard # Keyboard functions
import time
import random # random integers
from win32api import GetSystemMetrics # Get Screen rect
import pyautogui # for hotkey operations
# System variables for recovery scenario
gRecoveryWindowRDPRetryCountInt = 3 # Retry iteration count is RDP window is not responsible
gRecoveryWindowRDPRetryIntervalSecInt = 3 # Retry interval for reconnect

gRecoveryWindowRUNRetryCountInt = 3 # Retry iteration count is RUN window is not responsible
gRecoveryWindowRUNRetryIntervalSecInt = 3 # Retry interval for retry

gRecoveryCMDResponsibleRetryCountInt = 3 # Retry iteration count is CMD is not responsible
gRecoveryCMDResponsibleRetryIntervalSecInt = 3 # Retry interval for retry

gKeyboardHotkeyDelaySecFloat = 0.6 # Const for delay - important for work with RDP!!!!

#Connect to RDP session
"""
{
    "Host": "", #Host address
    "Port": "", #RDP Port
    "Login": "", # Login
    "Password": "", #Password
    "Screen": {
        "Resolution":"FullScreen", #"640x480" or "1680x1050" or "FullScreen". If Resolution not exists set full screen
        "FlagUseAllMonitors": False, # True or False
        "DepthBit":"" #"32" or "24" or "16" or "15"
    }
}
"""
def Session(inRDPSessionConfiguration, inScreenSize550x350Bool = False):
    #RDPConnector.SessionConnect(mConfiguration)
    #RDPConnector.LoginPassSet("111.222.222.111","ww","dd")
    (lRDPFile, lSessionHex) = SessionConfigurationCreate(inRDPSessionConfiguration)
    #Set session hex in globalDict
    inRDPSessionConfiguration["SessionHex"] = lSessionHex
    #Set login/password
    SessionLoginPasswordSet(inRDPSessionConfiguration["Host"],inRDPSessionConfiguration["Login"],inRDPSessionConfiguration["Password"])
    #Start session
    SessionRDPStart(lRDPFile, inScreenSize550x350Bool= inScreenSize550x350Bool)
    #Remove temp file
    time.sleep(4) #Delete file after some delay - one way to delete and run the RDP before because RDP is not read file in one moment
    os.remove(lRDPFile) # delete the temp rdp
    # Set the result 
    return inRDPSessionConfiguration
#Add login/ password to the windows credentials to run RDP
def SessionLoginPasswordSet(inHost, inLogin, inPassword):
    #Clear old login/password if it exists
    #os.system(f"cmdkey /delete:TERMSRV/{inHost}") #Dont need to delete because new user password will clear the previous creds
    #Set login password for host
    os.system(f'cmdkey /generic:TERMSRV/{inHost} /user:{inLogin} /pass:"{inPassword}"')
    return None
#Create current .rdp file with settings
#Return (full path to file, session hex)
def SessionConfigurationCreate(inConfiguration):
    #RobotRDPActive folder path
    lFileFullPath=__file__
    lFileFullPath = lFileFullPath.replace("/","\\")
    lRobotRDPActiveFolderPath = "\\".join(lFileFullPath.split("\\")[:-1])
    #Full path to Template.rdp file
    lRDPTemplateFileFullPath = os.path.join(lRobotRDPActiveFolderPath, "Template.rdp")
    #Open template file (.rdp encoding is USC-2 LE BOM = UTF-16 LE) http://qaru.site/questions/7156020/python-writing-a-ucs-2-little-endian-utf-16-le-file-with-bom
    lRDPTemplateFileContent = open(lRDPTemplateFileFullPath, "r", encoding="utf-16-le").read()
    #Prepare host:port
    lHostPort=inConfiguration['Host']
    if 'Port' in inConfiguration:
        if inConfiguration['Port']:
            lHostPort=f"{lHostPort}:{inConfiguration['Port']}"
    # Generate parameter for .rdp "drivestoredirect:s:C:\;"
    lDriveStoreDirectStr = ""
    for lItem in inConfiguration['SharedDriveList']:
        lDriveStoreDirectStr+=f"{lItem.upper()}:\\;" # Attention - all drives must be only in upper case!!!
    #Replace {Width}, {Height}, {BitDepth}, {HostPort}, {Login} {redirectclipboard}
    lRedirectClipboardStr = "1" if inConfiguration.get('RedirectClipboardBool',True) == True else "0"
    lRDPTemplateFileContent = lRDPTemplateFileContent.replace("{Width}", str(inConfiguration.get('Screen',{}).get("Width",1680)))
    lRDPTemplateFileContent = lRDPTemplateFileContent.replace("{Height}", str(inConfiguration.get('Screen',{}).get("Height",1050)))
    lRDPTemplateFileContent = lRDPTemplateFileContent.replace("{BitDepth}", inConfiguration.get('Screen',{}).get("DepthBit","32"))
    lRDPTemplateFileContent = lRDPTemplateFileContent.replace("{HostPort}", lHostPort)
    lRDPTemplateFileContent = lRDPTemplateFileContent.replace("{Login}", inConfiguration['Login'])
    lRDPTemplateFileContent = lRDPTemplateFileContent.replace("{SharedDriveList}", lDriveStoreDirectStr)
    lRDPTemplateFileContent = lRDPTemplateFileContent.replace("{redirectclipboard}", lRedirectClipboardStr)
    #Save template to temp file
    lRDPCurrentFileFullPath = os.path.join(tempfile.gettempdir(), f"{uuid.uuid4().hex}.rdp")
    open(lRDPCurrentFileFullPath, "w", encoding="utf-16-le").write(lRDPTemplateFileContent)
    #Return .rdp full path
    return (lRDPCurrentFileFullPath, (lRDPCurrentFileFullPath.split("\\")[-1])[0:-4])
#RDPSessionStart
def SessionRDPStart(inRDPFilePath, inScreenSize550x350Bool = False):
    #Disable certificate warning
    lCMDString = 'reg add "HKEY_CURRENT_USER\\Software\\Microsoft\\Terminal Server Client" /v "AuthenticationLevelOverride" /t "REG_DWORD" /d 0 /f'
    os.system(lCMDString)
    #run rdp session
    lItemArgs = [inRDPFilePath]
    subprocess.Popen(lItemArgs, shell=True)
    #Wait for UAC unknown publisher exists
    lRDPFileName = (inRDPFilePath.split("\\")[-1])[0:-4]
    lWaitResult = UIDesktop.UIOSelectorsSecs_WaitAppear_List(
        [
            [{"title": "Подключение к удаленному рабочему столу", "class_name": "#32770", "backend": "win32"},
             {"title": "Боль&ше не выводить запрос о подключениях к этому компьютеру", "friendly_class_name": "CheckBox"}],
            [{"title": "Remote Desktop Connection", "class_name": "#32770", "backend": "win32"},
             {"title": "D&on't ask me again for connections to this computer",
              "friendly_class_name": "CheckBox"}],
            [{"title_re": f"{lRDPFileName}.*",
              "class_name": "TscShellContainerClass", "backend": "win32"},{"depth_start":3, "depth_end": 3, "class_name":"UIMainClass"}]
        ],
        30
    )    
    #Enable certificate warning
    lCMDString = 'reg add "HKEY_CURRENT_USER\\Software\\Microsoft\\Terminal Server Client" /v "AuthenticationLevelOverride" /t "REG_DWORD" /d 2 /f'
    os.system(lCMDString)
    #Click if 0 is appear (RUS)
    if 0 in lWaitResult:
        #Check the box do not retry
        UIDesktop.UIOSelector_Get_UIO([{"title": "Подключение к удаленному рабочему столу", "backend": "win32"},
             {"title": "Боль&ше не выводить запрос о подключениях к этому компьютеру", "friendly_class_name": "CheckBox"}]).check()
        #Go to connection
        UIDesktop.UIOSelector_Get_UIO([{"title": "Подключение к удаленному рабочему столу", "backend": "win32"},
             {"title":"Подкл&ючить", "class_name":"Button"}]).click()
        lWaitResult = UIDesktop.UIOSelectorsSecs_WaitAppear_List(
            [
                [{"title_re": f"{lRDPFileName}.*",
                  "class_name": "TscShellContainerClass", "backend": "win32"}]
            ],
            30
        )
    # Click if 1 is appear (ENG)
    if 1 in lWaitResult:
        # Check the box do not retry
        UIDesktop.UIOSelector_Get_UIO([{"title": "Remote Desktop Connection", "class_name": "#32770", "backend": "win32"},
             {"title": "D&on't ask me again for connections to this computer",
              "friendly_class_name": "CheckBox"}]).check()
        # Go to connection
        UIDesktop.UIOSelector_Get_UIO([{"title": "Remote Desktop Connection", "class_name": "#32770", "backend": "win32"},
                                       {"title": "Co&nnect", "class_name": "Button"}]).click()
        lWaitResult = UIDesktop.UIOSelectorsSecs_WaitAppear_List(
            [
                [{"title_re": f"{lRDPFileName}.*",
                  "class_name": "TscShellContainerClass", "backend": "win32"}]
            ],
            30
        )
    # Raise exception if RDP is not active
    if len(lWaitResult) == 0:
        raise ConnectorExceptions.SessionWindowNotExistError("Error when initialize the RDP session - No RDP windows has appreared!")
    time.sleep(3) # Wait for init
    if inScreenSize550x350Bool: SessionScreenSize_X_Y_W_H(inSessionHex = lRDPFileName, inXInt = 10, inYInt = 10, inWInt = 550, inHInt = 350) #Prepare little window
    return None

#Set fullscreen for app
def SessionScreenFull(inSessionHex, inLogger = None, inRDPConfigurationItem = None):
    ########################################
    lWindowRDPRetryIterator = 0 # Retry iterator if RDP window is not active
    lRDPConfigurationItem = inRDPConfigurationItem # Get the RDP configuration item
    lL = inLogger # Get the logger instance
    lRDPWindow = None # Init the variable
    while lWindowRDPRetryIterator<gRecoveryWindowRDPRetryCountInt: # Loop iteration to connect to RDP
        try: # Try to get RDP window
            lRDPWindow = UIDesktop.UIOSelector_Get_UIO([{"title_re": f"{inSessionHex}.*", "backend": "win32"}])
            lWindowRDPRetryIterator = gRecoveryWindowRDPRetryCountInt # Set last iterator to turn off the loop
            # RDP window has been detected - go to set focus and maximize
            lRDPWindow.set_focus()
            lRDPWindow.maximize()
            if not SessionIsFullScreen(inSessionHex):
                lRDPWindow.type_keys("^%{BREAK}")
                time.sleep(0.5)
        except Exception as e: # RDP window is not exist - try to reconnect
            if lL: lL.warning(f"RDP::SessionScreenFull: RDP window is not exist - try sleep {gRecoveryWindowRDPRetryIntervalSecInt}[s.] and then to reconnect. SessionHex: {inSessionHex}. Current retry iterator is {lWindowRDPRetryIterator}")
            if lRDPConfigurationItem:
                time.sleep(gRecoveryWindowRDPRetryIntervalSecInt)  # Before try to reconnect sleep
                # Try to reconnect the RDP
                SessionClose(inSessionHexStr=inSessionHex) # Close the
                Session(lRDPConfigurationItem) # Create RDP session
                inSessionHex = lRDPConfigurationItem["SessionHex"] # Get new session hex after reconnect
                SystemRDPWarningClickOk()  # Click all warning messages
                lWindowRDPRetryIterator = lWindowRDPRetryIterator + 1 # increase the iterator
                if lWindowRDPRetryIterator >= gRecoveryWindowRDPRetryCountInt:  # Raise the error if retry count is over
                    if lL: lL.warning(f"RDP::SessionScreenFull: Retry count is over. Raise the error. SessionHex: {inSessionHex}.")  # Log the info
                    raise ConnectorExceptions.SessionWindowNotExistError()  # raise the error
            else:
                if lL: lL.warning(f"RDP::SessionScreenFull: Has no RDP configuration item - don't reconnect. Raise the error. SessionHex: {inSessionHex}") # Log the info
                raise ConnectorExceptions.SessionWindowNotExistError() # raise the error
    return None

# Set the screen size
def SessionScreenSize_X_Y_W_H(inSessionHex, inXInt, inYInt, inWInt, inHInt):
    lDoBool = True
    while lDoBool:
        #Prepare little window
        try:
            lRDPWindow = UIDesktop.UIOSelector_Get_UIO([{"title_re": f"{inSessionHex}.*", "backend": "win32"}])
        except Exception as e:
            return None
        try:
            lRDPWindow.set_focus()
            if SessionIsFullScreen(inSessionHex):
                lRDPWindow.type_keys("^%{BREAK}")
            time.sleep(0.5)
            lRDPWindow.restore()
            time.sleep(0.5)
            lRDPWindow.move_window(inXInt,inYInt,inWInt,inHInt)
        except Exception as e:
            time.sleep(1)
        else:
            lDoBool = False
    return None

# Set Little window of the session
def SessionScreen100x550(inSessionHex):
    SessionScreenSize_X_Y_W_H(inSessionHex = inSessionHex, inXInt = 10, inYInt = 10, inWInt = 550, inHInt = 100)
    return None
# Session - close window
def SessionClose(inSessionHexStr):
    #Close window
    try:
        UIDesktop.UIOSelector_Get_UIO([{"title_re": f"{inSessionHexStr}.*", "backend": "win32"}]).close()
    except Exception as e:
        pass
#Type command in CMD
# inSessionHex - SessionHex to catch window
# inModeStr "LISTEN", "CROSSCHECK", "RUN"
#   "LISTEN" - Get result of the cmd command in result TODO get home script
#   "CROSSCHECK" - Check if the command was successufully sent TODO get home script
#   "RUN" - Run without crosscheck and get clipboard
# return {
#   "OutStr": <> # Result string
#   "IsResponsibleBool": True|False # Flag is RDP is responsible - works only when inModeStr = CROSSCHECK
# }
# example Connector.SessionCMDRun("4d1e48f3ff6c45cc810ea25d8adbeb50","start notepad", "RUN")
def SessionCMDRun(inSessionHex,inCMDCommandStr = "echo 1", inModeStr="CROSSCHECK", inClipboardTimeoutSec = 5, inLogger=None, inRDPConfigurationItem=None):
    lL = inLogger # Init the logger
    # Init the result dict
    lResult = {"OutStr": None,"IsResponsibleBool":True}
    SessionScreenFull(inSessionHex, inLogger=lL, inRDPConfigurationItem=inRDPConfigurationItem) # Enter full screen mode with recovery scenario
    time.sleep(2)
    # Run CMD operations
    lResult = SystemCMDRun(inSessionHexStr = inRDPConfigurationItem["SessionHex"], inCMDCommandStr = inCMDCommandStr, inModeStr = inModeStr, inClipboardTimeoutSec = inClipboardTimeoutSec, inLogger=lL)
    # Exit fullscreen mode
    SessionScreenSize_X_Y_W_H(inSessionHex=inSessionHex, inXInt=10, inYInt=10, inWInt=550,
                              inHInt=350)  # Prepare little window
    return lResult
# Check if session is in Full screen mode
# Return True - is in fullscreen
# example print(Connector.SessionIsFullScreen(""))
def SessionIsFullScreen(inSessionHexStr):
    #Default resul
    lResult = False
    lWeight = GetSystemMetrics(0)
    lHeight = GetSystemMetrics(1)
    #Get window screen
    try:
        lRectangle = UIDesktop.UIOSelector_Get_UIO([{"title_re": f"{inSessionHexStr}.*", "backend": "win32"}]).rectangle()
    except Exception as e:
        return lResult
    # Get Height/Weight
    lSessionWeight = lRectangle.right - lRectangle.left
    lSessionHeight = lRectangle.bottom - lRectangle.top
    #Case fullscreen
    if lSessionHeight == lHeight and lSessionWeight == lWeight:
        lResult = True
    return lResult
    
# Check if session is in minimized screen mode
# Return True - is in minimized
# example print(Connector.SessionIsFullScreen(""))
def SessionIsMinimizedScreen(inSessionHexStr):
    #Default result
    lResult = False
    #Get window screen
    try:
        lResult = UIDesktop.UIOSelector_Get_UIO([{"title_re": f"{inSessionHexStr}.*", "backend": "win32"}]).is_minimized()
    except Exception as e:
        pass
    return lResult
# Check if RDP session is responsible (check with random combination in cmd)
# Attention - function will be work fine if RDP will be in full screen mode!!! (see def SessionScreenFull)
# Return True - is responsible; False - is not responsible
#Type command in CMD
# inFlagDoCrossCheck: True - Do check that CMD is executed (the text response will not be available)
# inModeStr "LISTEN", "CROSSCHECK", "RUN"
#   "LISTEN" - Get result of the cmd command in result TODO get home script
#   "CROSSCHECK" - Check if the command was successufully sent TODO get home script
#   "RUN" - Run without crosscheck and get clipboard
# inClipboardTimeoutSec # Second for wait when clipboard will changed
# return {
#   "OutStr": <> # Result string
#   "IsResponsibleBool": True|False # Flag is RDP is responsible - works only when inModeStr = CROSSCHECK
# }
# example Connector.SessionCMDRun("4d1e48f3ff6c45cc810ea25d8adbeb50","start notepad", "RUN")
def SystemCMDRun(inSessionHexStr, inCMDCommandStr = "echo 1", inModeStr="CROSSCHECK", inClipboardTimeoutSec = 5, inLogger = None):
    lRDPWindow = None # Init the UI object
    try:
        lRDPWindow = UIDesktop.UIOSelector_Get_UIO([{"title_re": f"{inSessionHexStr}.*", "backend": "win32"}])
    except Exception as e:
        raise ConnectorExceptions.SessionWindowNotExistError() # Raise error of gui window
    lL = inLogger # Alias for logger
    lResult = {"OutStr": None,"IsResponsibleBool":True} # Init the result dict
    lClipboardTextOld = str(random.randrange(999,9999999))  # Set random text to clipboard (for check purposes that clipboard text has been changed)
    Clipboard.TextSet(lClipboardTextOld)
    lCrosscheckKeyStr = str(random.randrange(999,9999999))
    lRecoveryCMDResponsibleRetryIteratorInt = 0  # Init the retry iterator
    lCommandIsTooBigBool = False
    lCMDPostFixStr = ""  # Case default "RUN"
    while lRecoveryCMDResponsibleRetryIteratorInt<gRecoveryCMDResponsibleRetryCountInt: # loop for retry
        # # # # # # # # # # # # # OPEN WINDOW RUN # # # # # # # # # # # # # # #
        lRecoveryWindowRUNRetryIteratorInt = 0  # Init the retry iterator
        while lRecoveryWindowRUNRetryIteratorInt<gRecoveryWindowRUNRetryCountInt: # loop for retry
            if inModeStr == "CROSSCHECK":
                #lCMDPostFixStr = f"& (echo {lCrosscheckKeyStr} | clip)"
                lCMDPostFixStr = f"| (echo {lCrosscheckKeyStr} | clip)" # Bugfix async set clipboard data
            elif inModeStr == "LISTEN":
                lCMDPostFixStr = f"| clip"
            Clipboard.TextSet("") # Clear the clipboard
            KeyboardHotkey("win","r") # win+r
            time.sleep(gKeyboardHotkeyDelaySecFloat)
            KeyboardHotkey("ctrl","a") # Select all
            KeyboardHotkey("ctrl","a") # Select all Bugfix - need double ctrl A because some OS reset selestion when ctrl A in RUN window
            #time.sleep(gKeyboardHotkeyDelaySecFloat)
            keyboard.send("backspace")  # Delete selected all
            time.sleep(gKeyboardHotkeyDelaySecFloat)  # Wait for RUN window will appear ctrl+a+backspace is async - so we need some timeout...
            lInputStr = f"cmd /c ({inCMDCommandStr}) {lCMDPostFixStr}" # Generate the output string for RUN window
            if len(lInputStr) <= 259:
                keyboard.write(lInputStr, delay=0.05) # Write new text
            else:
                if lL: lL.warning(
                    f"RDP.SystemCMDRun: ATTENTION! Your command is too big for the RUN window (len is {len(lInputStr)}). Orchestrator will send this command to the new cmd window. ")
                lInputStr = "cmd"
                lCommandIsTooBigBool = True
                keyboard.write(lInputStr, delay=0.05) # Write cmd
            time.sleep(gKeyboardHotkeyDelaySecFloat)
            # Check if autocomplete
            # # # # # # #
            KeyboardHotkey("ctrl", "c")  # Copy data
            # Check the clipboard
            lClipboardStr = Clipboard.TextGet() # Get text from clipboard
            time.sleep(gKeyboardHotkeyDelaySecFloat)
            #lL.debug(f"Clipboard text when check autocomplete:'{lClipboardStr}'")
            if lClipboardStr != "": # Send backspace if
                time.sleep(gKeyboardHotkeyDelaySecFloat)
                keyboard.send("backspace")  # Delete selected all
            # # # # # # # #
            KeyboardHotkey("ctrl","a") # Select all
            KeyboardHotkey("ctrl","c") # Copy data
            # Check the clipboard
            lClipboardWaitTimeStartSec = time.time()
            lClipboardStr = Clipboard.TextGet() # Get text from clipboard
            while lClipboardStr != lInputStr and (time.time() - lClipboardWaitTimeStartSec) <= inClipboardTimeoutSec:
                lClipboardStr = Clipboard.TextGet() # Get text from clipboard
                time.sleep(0.5) # wait some time for the next operation
            if lClipboardStr == lInputStr:  # Cross check the clipboard data and input string
                lRecoveryWindowRUNRetryIteratorInt = gRecoveryWindowRUNRetryCountInt # Set final count to block the loop
            else: # Failed - wait and retry
                if lL: lL.warning(f"RDP::SystemCMDRun: RUN window (win+r) doesn't appear. Wait for {gRecoveryWindowRUNRetryIntervalSecInt}[s.] and retry. Current retry iterator is {lRecoveryWindowRUNRetryIteratorInt}. CMD Str: {lInputStr}") # Log the error
                lRecoveryWindowRUNRetryIteratorInt = lRecoveryWindowRUNRetryIteratorInt + 1  # Increment the iterator
                if lRecoveryWindowRUNRetryIteratorInt == gRecoveryWindowRUNRetryCountInt:
                    if lL: lL.warning(f"RDP::SystemCMDRun: RUN window (win+r) retry count is over. Raise the error. CMD Str: {lInputStr}")  # Log the error
                    raise ConnectorExceptions.RUNExistError() # Raise the error
                time.sleep(gRecoveryWindowRUNRetryIntervalSecInt) # wait for some seconds before new iteration
        # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # # # # # # # # # # # # # RUN CMD # # # # # # # # # # # # # # #
        if inModeStr == "LISTEN":  # if mode == LISTEN - set random number in clipboard
            Clipboard.TextSet(lClipboardTextOld) #
            time.sleep(0.5)  # wait some time for the next operation
        keyboard.press_and_release('enter') # Execute CMD
        time.sleep(1)
        if lCommandIsTooBigBool == True:
            # Case when string is tool big - call cmd and then type text into
            #keyboard.write("cmd")  # Open cmd
            #time.sleep(1)
            #keyboard.press_and_release('enter')  # Execute CMD
            keyboard.write(f"(({inCMDCommandStr}) {lCMDPostFixStr}) && exit", delay=0.05)  # send command
            time.sleep(1)
            keyboard.press_and_release('enter')  # Execute command
        if inModeStr == "CROSSCHECK" or inModeStr == "LISTEN": # Get OutStr (Case CROSSCHECK and LISTEN)
            lClipboardWaitTimeStartSec = time.time()
            lResult["OutStr"] = Clipboard.TextGet() # Get text from clipboard
            while lResult["OutStr"].startswith(lClipboardTextOld) and (time.time() - lClipboardWaitTimeStartSec) <= inClipboardTimeoutSec:
                lResult["OutStr"] = Clipboard.TextGet() # Get text from clipboard
                time.sleep(0.5) # wait some time for the next operation
            if lResult["OutStr"] == lClipboardTextOld: # If value hasn't been changed - retry send
                lRecoveryCMDResponsibleRetryIteratorInt = lRecoveryCMDResponsibleRetryIteratorInt + 1  # increment the iterator
                if lL: lL.warning(f"RDP::SystemCMDRun: CMD command doesn't been executed (no changes in clipboard data). Wait for {gRecoveryCMDResponsibleRetryIntervalSecInt}[s.] and retry from start window RUN. Current retry iterator is {lRecoveryCMDResponsibleRetryIteratorInt}. CMD Str: {lInputStr}, Clipboard data: {lResult['OutStr']}")  # Log the error
                if lRecoveryCMDResponsibleRetryIteratorInt >= gRecoveryCMDResponsibleRetryCountInt:  # raise the error if retry count is exceeded
                    if lL: lL.warning(f"RDP::SystemCMDRun: CMD command retry count is over. Raise the error.")  # Log the error
                    raise ConnectorExceptions.CMDResponsibleError()  # Raise the error
                time.sleep(gRecoveryCMDResponsibleRetryIntervalSecInt)  # wait for some seconds before new iteration
            else: # Data was recieved - do crosscheck
                if inModeStr == "CROSSCHECK":
                    if lResult["OutStr"] == f"{lCrosscheckKeyStr} \r\n\x00\x00\x00\x00\x00": # it is ok - do futher check
                        lResult["IsResponsibleBool"] = True
                        lRecoveryCMDResponsibleRetryIteratorInt = gRecoveryCMDResponsibleRetryCountInt  # turn off the iterator
                    else:
                        lResult["IsResponsibleBool"] = False
                        lRecoveryCMDResponsibleRetryIteratorInt = lRecoveryCMDResponsibleRetryIteratorInt + 1  # increment the iterator
                        if lL: lL.warning(f"RDP::SystemCMDRun: CMD command doesn't been executed (wrong clipboard data). Wait for {gRecoveryCMDResponsibleRetryIntervalSecInt}[s.] and retry from start window RUN. Current retry iterator is {lRecoveryCMDResponsibleRetryIteratorInt}. CMD Str: {lInputStr}, Clipboard data: {lResult['OutStr']}")  # Log the error
                        if lRecoveryCMDResponsibleRetryIteratorInt >= gRecoveryCMDResponsibleRetryCountInt:  # raise the error if retry count is exceeded
                            if lL: lL.warning(f"RDP::SystemCMDRun: CMD command retry count is over. Raise the error.")  # Log the error
                            raise ConnectorExceptions.CMDResponsibleError()  # Raise the error
                        time.sleep(gRecoveryCMDResponsibleRetryIntervalSecInt)  # wait for some seconds before new iteration
                else: # clipboard data has been changed but mode is not crosscheck - return success from function
                    lRecoveryCMDResponsibleRetryIteratorInt = gRecoveryCMDResponsibleRetryCountInt  # turn off the iterator
        else: # Success - no cross validation is aaplicable
            lRecoveryCMDResponsibleRetryIteratorInt = gRecoveryCMDResponsibleRetryCountInt  # turn off the iterator
        # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    return lResult # return the result
# Check if current RDP is responsible
def SystemRDPIsResponsible(inSessionHexStr):
    return SystemCMDRun(inSessionHexStr = inSessionHexStr, inCMDCommandStr = "echo 1", inModeStr="CROSSCHECK")["IsResponsibleBool"]
# Click OK on error messages
def SystemRDPWarningClickOk():
    # Try to click OK Error window in RUS version
    while UIDesktop.UIOSelector_Exist_Bool([{"title": "Подключение к удаленному рабочему столу", "class_name": "#32770", "backend": "win32"},
             {"title": "ОК", "class_name": "Button"}]):
        try:
            UIDesktop.UIOSelector_Get_UIO([{"title": "Подключение к удаленному рабочему столу", "class_name": "#32770", "backend": "win32"},
                 {"title": "ОК", "class_name": "Button"}]).click()
        except Exception as e:
            pass
    # Try to click OK Error window in ENG version
    while UIDesktop.UIOSelector_Exist_Bool([{"title": "Remote Desktop Connection", "class_name": "#32770", "backend": "win32"},
                 {"title": "OK", "class_name": "Button"}]):
        try:
            UIDesktop.UIOSelector_Get_UIO([{"title": "Remote Desktop Connection", "class_name": "#32770", "backend": "win32"},
                 {"title": "OK", "class_name": "Button"}]).click()
        except Exception as e:
            pass
# Bugfix with RDP work
def KeyboardHotkey(inModifierKeyStr,inKeyStr, inDelaySecFloat=gKeyboardHotkeyDelaySecFloat):
    keyboard.press(inModifierKeyStr)
    time.sleep(inDelaySecFloat)
    keyboard.send(inKeyStr)
    time.sleep(inDelaySecFloat)
    keyboard.release(inModifierKeyStr)
    time.sleep(inDelaySecFloat)