import time

def RetryMark(inRDPSessionKeyStr, inGSettings):
    """
    Set mark that Orch will try to reconnect to RDP

    :param inRDPSessionKeyStr: RDP Session key string - to monitor retry count by the RDP Session key
    :param inGSettings: Orchestrator global settings dict (singleton)
    :return: None

    """

    lL = inGSettings.get("Logger", None) # Get the logger instance
    # Create List by the RDP Session key if not exists
    if inRDPSessionKeyStr not in inGSettings["RobotRDPActive"]["RecoveryDict"]["__StatisticsDict__"]:
        inGSettings["RobotRDPActive"]["RecoveryDict"]["__StatisticsDict__"][inRDPSessionKeyStr] = []
    inGSettings["RobotRDPActive"]["RecoveryDict"]["__StatisticsDict__"][inRDPSessionKeyStr].append(time.time())

def RetryIsTriggered(inRDPSessionKeyStr, inGSettings):
    """
    Check if you can need to init recovery mode for the RDP

    :param inRDPSessionKeyStr: RDP Session key string - to monitor retry count by the RDP Session key
    :param inGSettings: Orchestrator global settings dict (singleton)
    :return: True - Ready to start recovery mode - remotely restart PC; Falsew - else case
    """
    lTimeNowFloat = time.time()
    lResultBool = False
    if inRDPSessionKeyStr in inGSettings["RobotRDPActive"]["RecoveryDict"]["__StatisticsDict__"]:
        lTimeNewList = []
        lCatchCounterInt = 0
        for inTimeItemFloat in inGSettings["RobotRDPActive"]["RecoveryDict"]["__StatisticsDict__"][inRDPSessionKeyStr]:
            lTimeDeltaFloat = lTimeNowFloat - inTimeItemFloat
            # Remove item if very old
            if lTimeDeltaFloat < inGSettings["RobotRDPActive"]["RecoveryDict"]["CatchPeriodSecFloat"]:
                lTimeNewList.append(inTimeItemFloat)
                lCatchCounterInt = lCatchCounterInt+1
        # Set updated list
        inGSettings["RobotRDPActive"]["RecoveryDict"]["__StatisticsDict__"][inRDPSessionKeyStr] = lTimeNewList
        # Check if counter equal or more
        if lCatchCounterInt>= inGSettings["RobotRDPActive"]["RecoveryDict"]["TriggerCountInt"]:
            lResultBool = True
    return lResultBool

def RetryHostClear(inHostStr, inGSettings):
    """
    Clear retry stat by the host str

    :param inHostStr: PC host str to be cleared (search the RDPSession keys)
    :param inGSettings: Orchestrator global settings dict (singleton)
    :return:
    """

    for lRDPSessionKeyStr in inGSettings["RobotRDPActive"]["RDPList"]:
        lRDPDict = inGSettings["RobotRDPActive"]["RDPList"][lRDPSessionKeyStr]
        # Check if HOST in UPPER is equal
        if lRDPDict["Host"].upper() == inHostStr.upper():
            #Check if RDPSession key exist in stat
            if lRDPSessionKeyStr in inGSettings["RobotRDPActive"]["RecoveryDict"]["__StatisticsDict__"]:
                del inGSettings["RobotRDPActive"]["RecoveryDict"]["__StatisticsDict__"][lRDPSessionKeyStr]