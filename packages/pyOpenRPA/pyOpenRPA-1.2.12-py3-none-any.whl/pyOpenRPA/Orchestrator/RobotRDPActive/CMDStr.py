import os # Get abs path of the file
# Create CMD str to run file if process.exe is not running
def ProcessStartIfNotRunning(inProcessName, inFilePath, inFlagGetAbsPath=True):
    lFileAbsPath = inFilePath
    if inFlagGetAbsPath:
        lFileAbsPath = os.path.abspath(inFilePath)
    lResult = f'tasklist /nh /fi "imagename eq {inProcessName}" | find /i "{inProcessName}" > nul || (start {lFileAbsPath})'
    return lResult
# Create CMD str to stop process
def ProcessStop(inProcessName, inFlagForceClose):
    lResult = f'taskkill /im "{inProcessName}" /fi "username eq %USERNAME%"'
    if inFlagForceClose:
        lResult+= " /F"
    return lResult
# Send file from Host to Session RDP using shared drive in RDP (force copy)
def FileStoredSend(inHostFilePath, inRDPFilePath):
    lHostFileAbsPath = os.path.join("\\\\tsclient", os.path.abspath(inHostFilePath).replace(":","")) # \\tsclient\C\path\to\file
    lHostRDPFileAbsPath = os.path.abspath(inRDPFilePath) # File location in RDP
    lResult = f'copy /Y "{lHostFileAbsPath}" "{lHostRDPFileAbsPath}"'
    return lResult
# Send file from Session RDP to Host using shared drive in RDP (force copy)
def FileStoredRecieve(inRDPFilePath, inHostFilePath):
    lHostFileAbsPath = os.path.join("\\\\tsclient", os.path.abspath(inHostFilePath).replace(":","")) # \\tsclient\C\path\to\file
    lHostRDPFileAbsPath = os.path.abspath(inRDPFilePath) # File location in RDP
    lResult = f'copy /Y "{lHostRDPFileAbsPath}" "{lHostFileAbsPath}"'
    return lResult