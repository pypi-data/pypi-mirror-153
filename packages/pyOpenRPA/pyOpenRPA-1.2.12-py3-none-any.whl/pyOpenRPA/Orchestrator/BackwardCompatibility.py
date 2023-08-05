# Def to check inGSettings and update structure to the backward compatibility
# !!! ATTENTION: Backward compatibility has been started from v1.1.13 !!!
# So you can use config of the orchestrator 1.1.13 in new Orchestrator versions and all will be ok :) (hope it's true)
import win32security, json, datetime, time, copy
import schedule
# # # # # # # # # # # # # # # # # # #
# Backward compatibility Web defs up to v1.2.0
# # # # # # # # # # # # # # # # # # #

# UserAccess get rights hierarchy dict in json
def v1_2_0_UserRoleHierarchyGet(inRequest,inGlobalDict):
    inResponseDict = inRequest.OpenRPAResponseDict
    # Create result JSON
    lResultDict = inRequest.OpenRPA["DefUserRoleHierarchyGet"]() # Get the User Role Hierarchy list
    # Send message back to client
    message = json.dumps(lResultDict)
    # Write content as utf-8 data
    inResponseDict["Body"] = bytes(message, "utf8")

from inspect import signature # For detect count of def args
# /Orchestrator/RobotRDPActive/ControlPanelDictGet
def v1_2_0_RobotRDPActive_ControlPanelDictGet(inRequest,inGlobalDict):
    inResponseDict = inRequest.OpenRPAResponseDict
    lResultDict = {
        "DataList":[
            # {"SessionKeyStr":"", "SessionHexStr": "", "IsFullScreenBool": False, "IsIgnoredBool": False}
        ]
    }
    # Iterate throught the RDP List
    for lRDPSessionKeyStrItem in inGlobalDict["RobotRDPActive"]["RDPList"]:
        lRDPConfiguration = inGlobalDict["RobotRDPActive"]["RDPList"][lRDPSessionKeyStrItem] # Get the configuration dict
        lDataItemDict = {"SessionKeyStr":"", "SessionHexStr": "", "IsFullScreenBool": False, "IsIgnoredBool": False} # Template
        lDataItemDict["SessionKeyStr"] = lRDPSessionKeyStrItem # Session key str
        lDataItemDict["SessionHexStr"] = lRDPConfiguration["SessionHex"] # Session Hex
        lDataItemDict["IsFullScreenBool"] = True if lRDPSessionKeyStrItem == inGlobalDict["RobotRDPActive"]["FullScreenRDPSessionKeyStr"] else False # Check  the full screen for rdp window
        lDataItemDict["IsIgnoredBool"] = lRDPConfiguration["SessionIsIgnoredBool"] # Is ignored
        lResultDict["DataList"].append(lDataItemDict)
    # Send message back to client
    message = json.dumps(lResultDict)
    # Write content as utf-8 data
    inResponseDict["Body"] = bytes(message, "utf8")

# def to check control panels for selected session
def v1_2_0_Monitor_ControlPanelDictGet_SessionCheckInit(inRequest,inGlobalDict):
    lL = inGlobalDict["Logger"]  # Alias for logger
    lLifetimeSecFloat = inGlobalDict["Client"]["Session"]["LifetimeSecFloat"]
    lLifetimeRequestSecFloat = inGlobalDict["Client"]["Session"]["LifetimeRequestSecFloat"]
    lControlPanelRefreshIntervalSecFloat = inGlobalDict["Client"]["Session"]["ControlPanelRefreshIntervalSecFloat"]
    lCookieSessionGUIDStr = None  # generate the new GUID
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # Technicaldef - interval check control panels + check actuality of the session by the datetime
    def TechnicalCheck():
        lItemValue = inGlobalDict["Client"]["Session"]["TechnicalSessionGUIDCache"][lCookieSessionGUIDStr]
        # Lifetime is ok - check control panel
        lDatasetCurrentBytes = v1_2_0_Monitor_ControlPanelDictGet(inRequest,inGlobalDict) # Call the control panel
        if lDatasetCurrentBytes != lItemValue["DatasetLast"]["ControlPanel"]["Data"]: # Check if dataset is changed
            lItemValue["DatasetLast"]["ControlPanel"]["Data"] = lDatasetCurrentBytes # Set new datset
            lItemValue["DatasetLast"]["ControlPanel"]["ReturnBool"] = True # Set flag to return the data
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # Technicaldef - Create new session struct
    def TechnicalSessionNew(inSessionGUIDStr):
        lCookieSessionGUIDStr = inSessionGUIDStr  # Generate the new GUID
        lSessionNew = { # Session with some GUID str. On client session guid stored in cookie "SessionGUIDStr"
            "InitDatetime": datetime.datetime.now(), # Datetime when session GUID was created
            "DatasetLast": {
                "ControlPanel": {
                    "Data": None, # Struct to check with new iterations. None if starts
                    "ReturnBool": False # flag to return, close request and return data as json
                }
            },
            "ClientRequestHandler": inRequest, # Last client request handler
            "UserADStr": inRequest.OpenRPA["User"], # User, who connect. None if user is not exists
            "DomainADStr": inRequest.OpenRPA["Domain"], # Domain of the user who connect. None if user is not exists
        }
        inGlobalDict["Client"]["Session"]["TechnicalSessionGUIDCache"][lCookieSessionGUIDStr] = lSessionNew # Set new session in dict
        inRequest.OpenRPAResponseDict["SetCookies"]["SessionGUIDStr"] = lCookieSessionGUIDStr # Set SessionGUIDStr in cookies
        if lL: lL.info(f"New session GUID is created. GUID {lCookieSessionGUIDStr}")
        return lCookieSessionGUIDStr
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    lCreateNewSessionBool = False # Flag to create new session structure
    # step 1 - get cookie SessionGUIDStr
    lSessionGUIDStr = inRequest.headers.get("SessionGUIDStr", None)
    if lSessionGUIDStr is not None: # Check if GUID session is ok
        #inRequest.OpenRPAResponseDict["StatusCode"] = 301
        #inRequest.OpenRPAResponseDict["Headers"]["Location"] = "/"
        #if lL: lL.info(f"GUID is detected - send HTTP 301 to refresh page")
        lCookieSessionGUIDStr = lSessionGUIDStr # Get the existing GUID
        if lSessionGUIDStr not in inGlobalDict["Client"]["Session"]["TechnicalSessionGUIDCache"]:
            lCookieSessionGUIDStr= TechnicalSessionNew(inSessionGUIDStr = lSessionGUIDStr) # Create new session
        else: # Update the datetime of the request session
            inGlobalDict["Client"]["Session"]["TechnicalSessionGUIDCache"][lCookieSessionGUIDStr]["InitDatetime"]=datetime.datetime.now()
    else:
        lCookieSessionGUIDStr = TechnicalSessionNew(inSessionGUIDStr = lSessionGUIDStr) # Create new session
    # Init the RobotRDPActive in another thread
    #lThreadCheckCPInterval = threading.Thread(target=TechnicalIntervalCheck)
    #lThreadCheckCPInterval.daemon = True  # Run the thread in daemon mode.
    #lThreadCheckCPInterval.start()  # Start the thread execution.

    # Step 2 - interval check if data is exist
    lTimeStartSecFloat = time.time()
    lDoWhileBool = True # Flag to iterate throught the lifetime of the request
    while lDoWhileBool:
        #print(lTechnicalSessionGUIDCache)
        #print(lCookieSessionGUIDStr)
        if lCookieSessionGUIDStr in inGlobalDict["Client"]["Session"]["TechnicalSessionGUIDCache"]:
            lItemValue = inGlobalDict["Client"]["Session"]["TechnicalSessionGUIDCache"][lCookieSessionGUIDStr]
            if (time.time() - lTimeStartSecFloat) >= lLifetimeRequestSecFloat: # Check if lifetime client request is over or has no key
                if lL: lL.debug(f"Client request lifetime is over")
                lDoWhileBool = False # Stop the iterations
            if lDoWhileBool:
                TechnicalCheck() # Calculate the CP
                if lItemValue["DatasetLast"]["ControlPanel"]["ReturnBool"] == True: # Return data if data flag it True
                    lDatasetCurrentBytes = lItemValue["DatasetLast"]["ControlPanel"]["Data"]  # Set new dataset
                    inResponseDict = inRequest.OpenRPAResponseDict
                    inResponseDict["Body"] = lDatasetCurrentBytes
                    lItemValue["DatasetLast"]["ControlPanel"]["ReturnBool"] = False  # Set flag that data was returned
                    lDoWhileBool = False  # Stop the iterations
        else:
            lCookieSessionGUIDStr = TechnicalSessionNew(inSessionGUIDStr = lCookieSessionGUIDStr) # Create new session
        if lDoWhileBool:  # Sleep if we wait hte next iteration
            time.sleep(lControlPanelRefreshIntervalSecFloat)  # Sleep to the next iteration

def v1_2_0_Monitor_ControlPanelDictGet(inRequest,inGlobalDict):
    inResponseDict = inRequest.OpenRPAResponseDict
    lL = inGlobalDict["Logger"] # Alias for logger
    # Create result JSON
    lResultJSON = {"RenderRobotList": [], "RenderRDPList": []}
    lRenderFunctionsRobotList = inGlobalDict["ControlPanelDict"]["RobotList"]
    for lItem in lRenderFunctionsRobotList:
        lUACBool = True # Check if render function is applicable User Access Rights (UAC)
        if inGlobalDict["Server"]["AccessUsers"]["FlagCredentialsAsk"] is True:
            lUserRights = inGlobalDict["Server"]["AccessUsers"]["RuleDomainUserDict"][(inRequest.OpenRPA["Domain"].upper(),inRequest.OpenRPA["User"].upper())]
            if len(lUserRights["ControlPanelKeyAllowedList"]) > 0 and lItem["KeyStr"] not in lUserRights["ControlPanelKeyAllowedList"]:
                lUACBool = False # UAC Check is not passed - False for user
        if lUACBool: # Run function if UAC is TRUE
            # Выполнить вызов и записать результат
            # Call def (inRequest, inGSettings) or def (inGSettings)
            lItemResultDict = None
            lDEFSignature = signature(lItem["RenderFunction"]) # Get signature of the def
            lDEFARGLen = len(lDEFSignature.parameters.keys()) # get count of the def args
            try:
                if lDEFARGLen == 1: # def (inGSettings)
                    lItemResultDict = lItem["RenderFunction"](inGlobalDict)
                elif lDEFARGLen == 2: # def (inRequest, inGSettings)
                    lItemResultDict = lItem["RenderFunction"](inRequest, inGlobalDict)
                elif lDEFARGLen == 0: # def ()
                    lItemResultDict = lItem["RenderFunction"]()
                # RunFunction
                lResultJSON["RenderRobotList"].append(lItemResultDict)
            except Exception as e:
                if lL: lL.exception(f"Error in control panel. CP item {lItem}. Exception is below")
    # Iterate throught the RDP list
    for lRDPSessionKeyStrItem in inGlobalDict["RobotRDPActive"]["RDPList"]:
        lRDPConfiguration = inGlobalDict["RobotRDPActive"]["RDPList"][
            lRDPSessionKeyStrItem]  # Get the configuration dict
        lDataItemDict = {"SessionKeyStr": "", "SessionHexStr": "", "IsFullScreenBool": False,
                         "IsIgnoredBool": False}  # Template
        lDataItemDict["SessionKeyStr"] = lRDPSessionKeyStrItem  # Session key str
        lDataItemDict["SessionHexStr"] = lRDPConfiguration["SessionHex"]  # Session Hex
        lDataItemDict["IsFullScreenBool"] = True if lRDPSessionKeyStrItem == inGlobalDict["RobotRDPActive"][
            "FullScreenRDPSessionKeyStr"] else False  # Check  the full screen for rdp window
        lDataItemDict["IsIgnoredBool"] = lRDPConfiguration["SessionIsIgnoredBool"]  # Is ignored
        lResultJSON["RenderRDPList"].append(lDataItemDict)
    # Send message back to client
    message = json.dumps(lResultJSON)
    # Write content as utf-8 data
    #inResponseDict["Body"] = bytes(message, "utf8")
    return bytes(message, "utf8")


from . import __Orchestrator__ # For user defs



# v1.2.0 Def for old procesor to new processor
# Return new activity for the new processor
def v1_2_0_ProcessorOld2NewActivityDict(inActivityOld):
    if inActivityOld["Type"] == "WindowsLogon":
        lResult = {
            "Def": __Orchestrator__.OSCredentialsVerify, # def link or def alias (look gSettings["Processor"]["AliasDefDict"])
            "ArgList":[], # Args list
            "ArgDict":{"inUserStr": inActivityOld["User"],"inPasswordStr":inActivityOld["Password"],"inDomainStr":inActivityOld["Domain"]}, # Args dictionary
            "ArgGSettings": None,  # Name of GSettings attribute: str (ArgDict) or index (for ArgList)
            "ArgLogger": None  # Name of GSettings attribute: str (ArgDict) or index (for ArgList)
        }
    elif inActivityOld["Type"] == "GlobalDictKeyListValueGet":
        lResult = {
            "Def": __Orchestrator__.GSettingsKeyListValueGet, # def link or def alias (look gSettings["Processor"]["AliasDefDict"])
            "ArgList":[], # Args list
            "ArgDict":{"inKeyList": inActivityOld["KeyList"]}, # Args dictionary
            "ArgGSettings": "inGSettings",  # Name of GSettings attribute: str (ArgDict) or index (for ArgList)
            "ArgLogger": None  # Name of GSettings attribute: str (ArgDict) or index (for ArgList)
        }
    elif inActivityOld["Type"] == "CMDStart":
        lResult = {
            "Def": __Orchestrator__.OSCMD, # def link or def alias (look gSettings["Processor"]["AliasDefDict"])
            "ArgList": [],  # Args list
            "ArgDict": {"inCMDStr": inActivityOld["Command"]},  # Args dictionary
            "ArgGSettings": None,  # Name of GSettings attribute: str (ArgDict) or index (for ArgList)
            "ArgLogger": "inLogger"  # Name of GSettings attribute: str (ArgDict) or index (for ArgList)
        }
    elif inActivityOld["Type"] == "OrchestratorRestart":
        lResult = {
            "Def": __Orchestrator__.OrchestratorRestart, # def link or def alias (look gSettings["Processor"]["AliasDefDict"])
            "ArgList": [],  # Args list
            "ArgDict": {},  # Args dictionary
            "ArgGSettings": "inGSettings",  # Name of GSettings attribute: str (ArgDict) or index (for ArgList)
            "ArgLogger": None  # Name of GSettings attribute: str (ArgDict) or index (for ArgList)
        }
    elif inActivityOld["Type"] == "OrchestratorSessionSave":
        lResult = {
            "Def": __Orchestrator__.OrchestratorSessionSave,
            # def link or def alias (look gSettings["Processor"]["AliasDefDict"])
            "ArgList": [],  # Args list
            "ArgDict": {},  # Args dictionary
            "ArgGSettings": "inGSettings",  # Name of GSettings attribute: str (ArgDict) or index (for ArgList)
            "ArgLogger": None  # Name of GSettings attribute: str (ArgDict) or index (for ArgList)
        }
    elif inActivityOld["Type"] == "GlobalDictKeyListValueSet":
        lResult = {
            "Def": __Orchestrator__.GSettingsKeyListValueSet, # def link or def alias (look gSettings["Processor"]["AliasDefDict"])
            "ArgList": [],  # Args list
            "ArgDict": {"inKeyList": inActivityOld["KeyList"], "inValue": inActivityOld["Value"]},  # Args dictionary
            "ArgGSettings": "inGSettings",  # Name of GSettings attribute: str (ArgDict) or index (for ArgList)
            "ArgLogger": None  # Name of GSettings attribute: str (ArgDict) or index (for ArgList)
        }
    elif inActivityOld["Type"] == "GlobalDictKeyListValueAppend":
        lResult = {
            "Def": __Orchestrator__.GSettingsKeyListValueAppend, # def link or def alias (look gSettings["Processor"]["AliasDefDict"])
            "ArgList": [],  # Args list
            "ArgDict": {"inKeyList": inActivityOld["KeyList"], "inValue": inActivityOld["Value"]},  # Args dictionary
            "ArgGSettings": "inGSettings",  # Name of GSettings attribute: str (ArgDict) or index (for ArgList)
            "ArgLogger": None  # Name of GSettings attribute: str (ArgDict) or index (for ArgList)
        }
    elif inActivityOld["Type"] == "GlobalDictKeyListValueOperator+":
        lResult = {
            "Def": __Orchestrator__.GSettingsKeyListValueOperatorPlus, # def link or def alias (look gSettings["Processor"]["AliasDefDict"])
            "ArgList": [],  # Args list
            "ArgDict": {"inKeyList": inActivityOld["KeyList"], "inValue": inActivityOld["Value"]},  # Args dictionary
            "ArgGSettings": "inGSettings",  # Name of GSettings attribute: str (ArgDict) or index (for ArgList)
            "ArgLogger": None  # Name of GSettings attribute: str (ArgDict) or index (for ArgList)
        }
    elif inActivityOld["Type"] == "ProcessStart":
        lResult = {
            "Def": __Orchestrator__.ProcessStart, # def link or def alias (look gSettings["Processor"]["AliasDefDict"])
            "ArgList": [],  # Args list
            "ArgDict": {"inPathStr": inActivityOld["Path"], "inArgList": inActivityOld["ArgList"]},  # Args dictionary
            "ArgGSettings": None,  # Name of GSettings attribute: str (ArgDict) or index (for ArgList)
            "ArgLogger": None  # Name of GSettings attribute: str (ArgDict) or index (for ArgList)
        }
    elif inActivityOld["Type"] == "ProcessStartIfTurnedOff":
        lResult = {
            "Def": __Orchestrator__.ProcessStart, # def link or def alias (look gSettings["Processor"]["AliasDefDict"])
            "ArgList": [],  # Args list
            "ArgDict": {"inPathStr": inActivityOld["Path"], "inArgList": inActivityOld["ArgList"], "inStopProcessNameWOExeStr": inActivityOld["CheckTaskName"]},  # Args dictionary
            "ArgGSettings": None,  # Name of GSettings attribute: str (ArgDict) or index (for ArgList)
            "ArgLogger": None  # Name of GSettings attribute: str (ArgDict) or index (for ArgList)
        }
    elif inActivityOld["Type"] == "ProcessStop":
        lResult = {
            "Def": __Orchestrator__.ProcessStop, # def link or def alias (look gSettings["Processor"]["AliasDefDict"])
            "ArgList": [],  # Args list
            "ArgDict": {"inProcessNameWOExeStr": inActivityOld["Name"], "inCloseForceBool": inActivityOld["FlagForce"], "inUserNameStr": inActivityOld["User"]},  # Args dictionary
            "ArgGSettings": None,  # Name of GSettings attribute: str (ArgDict) or index (for ArgList)
            "ArgLogger": None  # Name of GSettings attribute: str (ArgDict) or index (for ArgList)
        }
    elif inActivityOld["Type"] == "PythonStart":
        lResult = {
            "Def": __Orchestrator__.PythonStart, # def link or def alias (look gSettings["Processor"]["AliasDefDict"])
            "ArgList": [],  # Args list
            "ArgDict": {"inModulePathStr": inActivityOld["ModuleName"], "inDefNameStr": inActivityOld["FunctionName"], "inArgList": inActivityOld["ArgList"],
                    "inArgDict": inActivityOld["ArgDict"] },  # Args dictionary
            "ArgGSettings": None,  # Name of GSettings attribute: str (ArgDict) or index (for ArgList)
            "ArgLogger": "inLogger"  # Name of GSettings attribute: str (ArgDict) or index (for ArgList)
        }
    else:
        raise Exception(f"BackwardCompatibility up to v1.2.0, old processor: No type {inActivityOld['Type']} has been found in old processor.")
    return lResult # return the result


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # HERE IS THE MAIN DEF WHICH IS LAUNCHES WHEN START # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
def Update(inGSettings):
    lL = inGSettings["Logger"] # Alias for logger
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # v1.1.13 to v1.1.14
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    if "Autocleaner" not in inGSettings: # Add "Autocleaner" structure
        inGSettings["Autocleaner"] = { # Some gurbage is collecting in g settings. So you can configure autocleaner to periodically clear gSettings
            "IntervalSecFloat": 7200.0, # Sec float to periodically clear gsettings
        }
        if lL: lL.warning(f"Backward compatibility (v1.1.13 to v1.1.14): Add default 'Autocleaner' structure") # Log about compatibility
    if "Client" not in inGSettings: # Add "Client" structure
        inGSettings["Client"] = { # Settings about client web orchestrator
            "Session":{ # Settings about web session. Session algorythms works only for special requests (URL in ServerSettings)
                "LifetimeSecFloat": 600.0, # Client Session lifetime in seconds. after this time server will forget about this client session
                "LifetimeRequestSecFloat": 120.0, # 1 client request lifetime in server in seconds
                "ControlPanelRefreshIntervalSecFloat": 1.5, # Interval to refresh control panels for session,
                "TechnicalSessionGUIDCache": { # TEchnical cache. Fills when web browser is requesting
                    #"SessionGUIDStr":{ # Session with some GUID str. On client session guid stored in cookie "SessionGUIDStr"
                    #    "InitDatetime": None, # Datetime when session GUID was created
                    #    "DatasetLast": {
                    #        "ControlPanel": {
                    #            "Data": None, # Struct to check with new iterations. None if starts
                    #            "ReturnBool": False # flag to return, close request and return data as json
                    #        }
                    #    },
                    #    "ClientRequestHandler": None, # Last client request handler
                    #    "UserADStr": None, # User, who connect. None if user is not exists
                    #    "DomainADStr": None, # Domain of the user who connect. None if user is not exists
                    #}
                }
            }
        }
        if lL: lL.warning(f"Backward compatibility (v1.1.13 to v1.1.14): Add default 'Client' structure")  # Log about compatibility
    if "Server" in inGSettings and "RequestTimeoutSecFloat" not in inGSettings["Server"]: # Add Server > "RequestTimeoutSecFloat" property
        inGSettings["Server"]["RequestTimeoutSecFloat"] = 300 # Time to handle request in seconds
        if lL: lL.warning(
            f"Backward compatibility (v1.1.13 to v1.1.14): Add default 'Server' > 'RequestTimeoutSecFloat' property")  # Log about compatibility
    if "DefSettingsUpdatePathList" not in inGSettings["OrchestratorStart"]:  # Add OrchestratorStart > "DefSettingsUpdatePathList" property
        inGSettings["OrchestratorStart"]["DefSettingsUpdatePathList"] = []  # List of the .py files which should be loaded before init the algorythms
        if lL: lL.warning(f"Backward compatibility (v1.1.13 to v1.1.14): Add default 'OrchestratorStart' > 'DefSettingsUpdatePathList' property list")  # Log about compatibility
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # v1.1.20 to v1.2.0
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # Update Structure gSettings["Processor"]
    from . import SettingsTemplate
    if "DumpLogListRefreshIntervalSecFloat" not in inGSettings["Client"]:  # Create new ProcessorDict structure
        inGSettings["Client"].update({
            "DumpLogListRefreshIntervalSecFloat": 3.0,  # Duration between updates for the Client
            "DumpLogListCountInt": 100,  # Set the max row for the dump
            "DumpLogList": [],  # Will be filled automatically
            "DumpLogListHashStr": None,  # Will be filled automatically
        })
        if lL: lL.warning(f"Backward compatibility (v1.1.20 to v1.2.0): Create new attribute 'Client > DumpLog... with default parameters'")  # Log about compatibility
    if "Processor" in inGSettings: # Check if Processor exist
        # Update Logger
        if lL is not None:
            SettingsTemplate.LoggerDumpLogHandlerAdd(inLogger=lL, inGSettingsClientDict=inGSettings["Client"])
            if lL: lL.warning(f"Backward compatibility (v1.1.20 to v1.2.0): Add web dump log in logger as handler")  # Log about compatibility
        del inGSettings["Processor"] # Remove the key
        if lL: lL.warning(f"Backward compatibility (v1.1.20 to v1.2.0): Remove old structure 'Processor'")  # Log about compatibility
    if "ProcessorDict" not in inGSettings: # Create new ProcessorDict structure
        inGSettings["ProcessorDict"]={
            "ActivityList": [  # List of the activities
                # {
                #    "Def":"DefAliasTest", # def link or def alias (look gSettings["Processor"]["AliasDefDict"])
                #    "ArgList":[1,2,3], # Args list
                #    "ArgDict":{"ttt":1,"222":2,"dsd":3} # Args dictionary
                #    "ArgGSettings": # Name of GSettings attribute: str (ArgDict) or index (for ArgList)
                # },
            ],
            "AliasDefDict": {} , # Storage for def with Str alias. To use it see pyOpenRPA.Orchestrator.ControlPanel
            "CheckIntervalSecFloat": 1.0,  # Interval for check gSettings in ProcessorDict > ActivityList
            "ExecuteBool": True,  # Flag to execute thread processor
            "ThreadIdInt": None # Fill thread id when processor will be inited
        }
        if lL: lL.warning(f"Backward compatibility (v1.1.20 to v1.2.0): Create new structure 'ProcessorDict'")  # Log about compatibility
    if "VersionStr" not in inGSettings:  # Create new ProcessorDict structure
        inGSettings["VersionStr"] = None
        if lL: lL.warning(f"Backward compatibility (v1.1.20 to v1.2.0): Create new attribute 'VersionStr'")  # Log about compatibility
    if "AgentDict" not in inGSettings:  # Create new AgentDict structure
        inGSettings["AgentDict"]= {}
        if lL: lL.warning(
            f"Backward compatibility (v1.1.20 to v1.2.0): Create new attribute 'AgentDict'")  # Log about compatibility
    # Alg to convert UAC ControlPanelAllawedList to UACClient hierarchy
    # if inGSettings["Server"]["AccessUsers"]["FlagCredentialsAsk"] is True:
    #    lUserRights = inGSettings["Server"]["AccessUsers"]["RuleDomainUserDict"][(inRequest.OpenRPA["Domain"].upper(), inRequest.OpenRPA["User"].upper())]
    #    if len(lUserRights["ControlPanelKeyAllowedList"]) > 0 and lItem["KeyStr"] not in lUserRights["ControlPanelKeyAllowedList"]:
    #        lUACBool = False # UAC Check is not passed - False for user
    # # Convert to UACClient dict
    if "Server" in inGSettings:
        # Check if Server is active > convert to ServerDict
        inGSettings["ServerDict"] = inGSettings["Server"]
        if lL: lL.warning(
            f"Backward compatibility (v1.1.20 to v1.2.0): Convert Server to ServerDict")  # Log about compatibility
        # Remove old structure Scheduler
        del inGSettings["Server"]
        lShowWarnBool = False
        lRuleDomainUserDeepCopyDict = copy.deepcopy(inGSettings["ServerDict"]["AccessUsers"]["RuleDomainUserDict"])
        for lItemKeyTurple in lRuleDomainUserDeepCopyDict:
            lDomainUpperStr = lItemKeyTurple[0]
            lUserUpperStr = lItemKeyTurple[1]
            lItemDict = lRuleDomainUserDeepCopyDict[lItemKeyTurple]
            if "ControlPanelKeyAllowedList" in lItemDict:
                lShowWarnBool = True
                if len(lItemDict["ControlPanelKeyAllowedList"])>0:
                    lUACClientDict = {"pyOpenRPADict": {"CPKeyDict": {}}}
                else:
                    lUACClientDict = {}
                for lAllowedKeyItemStr in lItemDict["ControlPanelKeyAllowedList"]:
                    lUACClientDict["pyOpenRPADict"]["CPKeyDict"][lAllowedKeyItemStr]=True # Convert
                # Send update UACDict for user by the list
                __Orchestrator__.UACUpdate(inGSettings=inGSettings,inADLoginStr=lUserUpperStr, inADStr=lDomainUpperStr, inRoleHierarchyAllowedDict=lUACClientDict)
                # remove "ControlPanelKeyAllowedList" - will be removed in __Orchestrator__.UACUpdate
                #del inGSettings["ServerDict"]["AccessUsers"]["RuleDomainUserDict"][lItemKeyTurple]["ControlPanelKeyAllowedList"]
        if lShowWarnBool: # Show only 1 warning per all run
            if lL: lL.warning(f"Backward compatibility (v1.1.20 to v1.2.0): Convert CP allowed list to UAC Client hierarchy (consolidated)")  # Log about compatibility
    # Check if ControlPanelDict is active > convert to CPDict
    if "ControlPanelDict" in inGSettings:
        if "CPDict" not in inGSettings: inGSettings["CPDict"]={}
        for lItemDict in inGSettings["ControlPanelDict"]["RobotList"]:
            inGSettings["CPDict"][lItemDict["KeyStr"]]={"HTMLRenderDef":lItemDict["RenderFunction"], "JSONGeneratorDef":None, "JSInitGeneratorDef":None}
        # Remove old structure ControlPanel
        del inGSettings["ControlPanelDict"]
        if lL: lL.warning(f"Backward compatibility (v1.1.20 to v1.2.0): Convert ControlPanelDict to CPDict")  # Log about compatibility
    # Check if Scheduler is active > convert to SchedulerDict
    if "Scheduler" in inGSettings:
        if "SchedulerDict" not in inGSettings: inGSettings["SchedulerDict"]={ "CheckIntervalSecFloat": 5.0, "ActivityTimeList":[]}
        if "ActivityTimeCheckLoopSeconds" in inGSettings["Scheduler"]:
            inGSettings["SchedulerDict"]["CheckIntervalSecFloat"] = inGSettings["Scheduler"]["ActivityTimeCheckLoopSeconds"]
        for lItemDict in inGSettings["Scheduler"]["ActivityTimeList"]:
            # Append to the new struct if this is not periodic ("TimeHH:MMStart"and "TimeHH:MMStop")
            if "TimeHH:MMStart" not in lItemDict and "TimeHH:MMStop" not in lItemDict:
                lItemDict["ActivityList"]=[v1_2_0_ProcessorOld2NewActivityDict(inActivityOld=lItemDict["Activity"])]
                del lItemDict["Activity"]
                inGSettings["SchedulerDict"]["ActivityTimeList"].append(lItemDict)
        # Remove old structure Scheduler
        del inGSettings["Scheduler"]
        if lL: lL.warning(f"Backward compatibility (v1.1.20 to v1.2.0): Convert Scheduler to SchedulerDict with new features")  # Log about compatibility
    # # Convert to Storage to StorageDict
    if "Storage" in inGSettings:
        # Check if Server is active > convert to ServerDict
        inGSettings["StorageDict"] = inGSettings["Storage"]
        if lL: lL.warning(
            f"Backward compatibility (v1.2.1 to v1.2.2): Convert Storage to StorageDict")  # Log about compatibility
        # Remove old structure Scheduler
        del inGSettings["Storage"]
    # Add new key WarningExecutionMoreThanSecFloat in ProcessorDict
    if "WarningExecutionMoreThanSecFloat" not in inGSettings["ProcessorDict"]:
        inGSettings["ProcessorDict"]["WarningExecutionMoreThanSecFloat"] = 60.0
        if lL: lL.warning(
            f"Backward compatibility (v1.2.1 to v1.2.2): Add key WarningExecutionMoreThanSecFloat in ProcessorDict")  # Log about compatibility
    # Add new key AgentActivityLifetimeSecFloat, AgentConnectionLifetimeSecFloat, AgentLoopSleepSecFloat in ProcessorDict > ServerDict
    if "AgentActivityLifetimeSecFloat" not in inGSettings["ServerDict"]:
        inGSettings["ServerDict"]["AgentActivityLifetimeSecFloat"] = 1200.0
        inGSettings["ServerDict"]["AgentConnectionLifetimeSecFloat"] = 300.0
        inGSettings["ServerDict"]["AgentLoopSleepSecFloat"] = 2.0
        if lL: lL.warning(
            f"Backward compatibility (v1.2.1 to v1.2.2): Add key AgentActivityLifetimeSecFloat, AgentConnectionLifetimeSecFloat, AgentLoopSleepSecFloat in ProcessorDict > ServerDict")  # Log about compatibility
    # Add new key RecoveryDict in ProcessorDict > RobotRDPActive
    if "RecoveryDict" not in inGSettings["RobotRDPActive"]:
        inGSettings["RobotRDPActive"]["RecoveryDict"] = {
            "CatchPeriodSecFloat": 1200, # Catch last 10 minutes
            "TriggerCountInt": 10, # Activate trigger if for the period orch will catch the reconnect RDP n times
            "DoDict": {
                "OSRemotePCRestart": True # Do powershell remote restart
            },
            "__StatisticsDict__": {
                # RDPSessionKeyStr : [time.time(), time.time()],
            }
        }
        if lL: lL.warning(
            f"Backward compatibility (v1.2.1 to v1.2.2): Add new key RecoveryDict in ProcessorDict > RobotRDPActive")  # Log about compatibility
    # Add new key ServerDict > ListenDict
    if "ListenDict" not in inGSettings["ServerDict"]:
        lPortInt = inGSettings.get("ServerDict",{}).get("ListenPort",80)
        inGSettings["ServerDict"]["ListenDict"] = {
            "Default": {
                "AddressStr": "",
                "PortInt": lPortInt,
                "CertFilePEMPathStr": None,
                "KeyFilePathStr": None,
                "ServerInstance": None
            }
        }
        if lL: lL.warning(
            f"Backward compatibility (v1.2.2 to v1.2.3):  Add new key ServerDict > ListenDict. Transfer port from ServerDict > ListenPort")  # Log about compatibility
    # Add new key
    #"ServerDict": {
    #    "AgentFileChunkBytesSizeInt": 50000000,  # size of the each chunk for the agent transmition
    #    "AgentFileChunkCheckIntervalSecFloat": 0.2,  # The interval for check last activity item was successfully sent
    if "AgentFileChunkBytesSizeInt" not in inGSettings["ServerDict"]:
        inGSettings["ServerDict"]["AgentFileChunkBytesSizeInt"]= 50000000
        if lL: lL.warning(
            f"Backward compatibility (v1.2.3 to v1.2.4):  Add new key ServerDict > AgentFileChunkBytesSizeInt")  # Log about compatibility
    if "AgentFileChunkCheckIntervalSecFloat" not in inGSettings["ServerDict"]:
        inGSettings["ServerDict"]["AgentFileChunkCheckIntervalSecFloat"]= 0.2
        if lL: lL.warning(
            f"Backward compatibility (v1.2.3 to v1.2.4):  Add new key ServerDict > AgentFileChunkCheckIntervalSecFloat")  # Log about compatibility
    if "ServerThread" not in inGSettings["ServerDict"]:
        inGSettings["ServerDict"]["ServerThread"]= None
        if lL: lL.warning(
            f"Backward compatibility (v1.2.3 to v1.2.4):  Add new key ServerDict > ServerThread")  # Log about compatibility
    if "AgentLimitLogSizeBytesInt" not in inGSettings["ServerDict"]:
        inGSettings["ServerDict"]["AgentLimitLogSizeBytesInt"] = 300
        if lL: lL.warning(
            f"Backward compatibility (v1.2.3 to v1.2.4):  Add new key ServerDict > AgentLimitLogSizeBytesInt")  # Log about compatibility
    # Remove ControlPanelDict and CPDict > go to ServerDict > ControlPanelDict
    if "ControlPanelDict" in inGSettings:
        del inGSettings["ControlPanelDict"]
        if lL: lL.warning(
            f"Backward compatibility (v1.2.4 to v1.2.7):  Remove old key: ControlPanelDict")  # Log about compatibility
    if "CPDict" in inGSettings:
        for lCPKeyStr in inGSettings["CPDict"]:
            lCPItemDict = inGSettings["CPDict"][lCPKeyStr]
            __Orchestrator__.WebCPUpdate(inCPKeyStr=lCPKeyStr,inHTMLRenderDef=lCPItemDict["HTMLRenderDef"],
                                         inJSONGeneratorDef=lCPItemDict["JSONGeneratorDef"],
                                         inJSInitGeneratorDef=lCPItemDict["JSInitGeneratorDef"])
        del inGSettings["CPDict"]
        if lL: lL.warning(
            f"Backward compatibility (v1.2.4 to v1.2.7):  Remove old key: CPDict")  # Log about compatibility
    if "ControlPanelDict" not in inGSettings["ServerDict"]:
        inGSettings["ServerDict"]["ControlPanelDict"]={}
        if lL: lL.warning(
            f"Backward compatibility (v1.2.4 to v1.2.7):  Create new key: ServerDict > ControlPanelDict")  # Log about compatibility
    # ManagersProcessDict
    if "ManagersProcessDict" not in inGSettings:
        inGSettings["ManagersProcessDict"]={}
        if lL: lL.warning(
            f"Backward compatibility (v1.2.4 to v1.2.7):  Create new key: ManagersProcessDict")  # Log about compatibility
    # Check "SchedulerDict": {   "Schedule": schedule,  # https://schedule.readthedocs.io/en/stable/examples.html
    if inGSettings.get("SchedulerDict",{}).get("Schedule",None) is None:
        inGSettings["SchedulerDict"]["Schedule"] = schedule
        if lL: lL.warning(f"Backward compatibility (v1.2.4 to v1.2.7):  Create new module schedule (schedule.readthedocs.io)")  # Log about compatibility
    # ManagersGitDict
    if "ManagersGitDict" not in inGSettings:
        inGSettings["ManagersGitDict"]={}
        if lL: lL.warning(
            f"Backward compatibility (v1.2.4 to v1.2.7):  Create new key: ManagersGitDict")  # Log about compatibility
    # ProcessorDict > ActivityItemNowDict
    if "ActivityItemNowDict" not in inGSettings["ProcessorDict"]:
        inGSettings["ProcessorDict"]["ActivityItemNowDict"]=None
        if lL: lL.warning(
            f"Backward compatibility (v1.2.4 to v1.2.7):  Create new key: ProcessorDict > ActivityItemNowDict")  # Log about compatibility

    # # "UACBool": True # True - check user access before do this URL item
    for lURLItemDict in inGSettings["ServerDict"]["URLList"]:
        if "UACBool" not in lURLItemDict:
            lURLItemDict["UACBool"]=None
        if lL: lL.warning(
            f"Backward compatibility (v1.2.4 to v1.2.7):  ServerDict > URLList > item: add UACBool = None")  # Log about compatibility

    # "URLIndexStr"
    if "URLIndexStr" not in inGSettings["ServerDict"]:
        inGSettings["ServerDict"]["URLIndexStr"] = "/"
    if lL: lL.warning(
        f"Backward compatibility (v1.2.11 to v1.2.12):  ServerDict > URLIndexStr: add URLIndexStr = /")  # Log about compatibility