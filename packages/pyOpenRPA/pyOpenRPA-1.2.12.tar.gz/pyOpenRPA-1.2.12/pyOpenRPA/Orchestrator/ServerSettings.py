import json, os
import copy
from . import __Orchestrator__
#ControlPanelDict
from desktopmagic.screengrab_win32 import (
	getDisplayRects, saveScreenToBmp, saveRectToBmp, getScreenAsImage,
	getRectAsImage, getDisplaysAsImages)
from http import cookies
import uuid # generate UUID4
import time # sleep functions
import datetime # datetime functions
import threading # Multi-threading
from .Web import Basic
from ..Tools import Usage
from . import BackwardCompatibility # Support old up to 1.2.0 defs
from . import Processor
from . import SettingsTemplate

# # # # # # # # # # # #
# v 1.2.0 Functionallity
# # # # # # # # # # # #
# Generate JS when page init
def HiddenJSInitGenerate(inRequest, inGSettings):
    dUAC = inRequest.UACClientCheck # Alias.
    lUACCPTemplateKeyList=["pyOpenRPADict","CPKeyDict"]
    lL = inGSettings["Logger"] # Alias for logger
    lJSInitResultStr = ""
    lRenderFunctionsRobotDict = inGSettings["ServerDict"]["ControlPanelDict"]
    for lItemKeyStr in lRenderFunctionsRobotDict:
        lItemDict = lRenderFunctionsRobotDict[lItemKeyStr]
        lUACBool = dUAC(inRoleKeyList=lUACCPTemplateKeyList+[lItemKeyStr]) # Check if render function is applicable User Access Rights (UAC)
        if lItemKeyStr=="VersionCheck": lUACBool=True # For backward compatibility for the old fron version which not reload page when new orch version is comming
        if lUACBool: # Run function if UAC is TRUE
            # JSONGeneratorDef
            lJSInitResultStr = lJSInitResultStr + ";" + lItemDict.OnInitJSStr(inRequest=inRequest)
    return lJSInitResultStr

# Generate CP HTML + JSON
# Return {"Key":{"",""}}
def HiddenCPDictGenerate(inRequest, inGSettings):
    dUAC = inRequest.UACClientCheck # Alias.
    lUACCPTemplateKeyList=["pyOpenRPADict","CPKeyDict"]
    lL = inGSettings["Logger"] # Alias for logger
    # Create result JSON
    lCPDict = {}
    lRenderFunctionsRobotDict = inGSettings["ServerDict"]["ControlPanelDict"]
    for lItemKeyStr in lRenderFunctionsRobotDict:
        lItemDict = lRenderFunctionsRobotDict[lItemKeyStr]
        lUACBool = dUAC(inRoleKeyList=lUACCPTemplateKeyList+[lItemKeyStr]) # Check if render function is applicable User Access Rights (UAC)
        if lItemKeyStr=="VersionCheck": lUACBool=True # For backward compatibility for the old fron version which not reload page when new orch version is comming
        if lUACBool: # Run function if UAC is TRUE
            lCPItemDict = {"HTMLStr": None, "JSONDict":None}
            try:
                # HTML Render
                lCPItemDict["HTMLStr"] = lItemDict.OnRefreshHTMLStr(inRequest=inRequest)
                # JSONGeneratorDef
                lCPItemDict["JSONDict"] = lItemDict.OnRefreshJSONDict(inRequest=inRequest)
            except Exception as e:
                lL.exception(f"EXCEPTION WHEN HTML/ JSON RENDER")
            # Insert CPItemDict in result CPDict
            lCPDict[lItemKeyStr]=lCPItemDict
    return lCPDict

# Return {"Key":{"",""}}
def HiddenRDPDictGenerate(inRequest, inGSettings):
    dUAC = inRequest.UACClientCheck # Alias.
    lUACRDPTemplateKeyList=["pyOpenRPADict","RDPKeyDict"]
    lRDPDict = {"HandlebarsList":[]}
    # Iterate throught the RDP list
    for lRDPSessionKeyStrItem in inGSettings["RobotRDPActive"]["RDPList"]:
        # Check UAC
        if dUAC(inRoleKeyList=lUACRDPTemplateKeyList+[lRDPSessionKeyStrItem]):
            lRDPConfiguration = inGSettings["RobotRDPActive"]["RDPList"][
                lRDPSessionKeyStrItem]  # Get the configuration dict
            lDataItemDict = {"SessionKeyStr": "", "SessionHexStr": "", "IsFullScreenBool": False,
                             "IsIgnoredBool": False}  # Template
            lDataItemDict["SessionKeyStr"] = lRDPSessionKeyStrItem  # Session key str
            lDataItemDict["SessionHexStr"] = lRDPConfiguration["SessionHex"]  # Session Hex
            lDataItemDict["IsFullScreenBool"] = True if lRDPSessionKeyStrItem == inGSettings["RobotRDPActive"][
                "FullScreenRDPSessionKeyStr"] else False  # Check  the full screen for rdp window
            lDataItemDict["IsIgnoredBool"] = lRDPConfiguration["SessionIsIgnoredBool"]  # Is ignored
            lRDPDict[lDataItemDict["SessionKeyStr"]]=lDataItemDict
            lHandlebarsDataItemDict = copy.deepcopy(lDataItemDict)
            lHandlebarsDataItemDict["SessionKeyStr"]=lDataItemDict["SessionKeyStr"]
            lRDPDict["HandlebarsList"].append(lHandlebarsDataItemDict)
    return lRDPDict

# Return {"HostNameUpperStr;UserUpperStr":{"IsListenBool":True}, "HandlebarsList":[{"HostnameUpperStr":"","UserUpperStr":"","IsListenBool":True}]}
def HiddenAgentDictGenerate(inRequest, inGSettings):
    dUAC = inRequest.UACClientCheck # Alias.
    lUACAgentTemplateKeyList=["pyOpenRPADict","AgentKeyDict"]
    lAgentDict = {"HandlebarsList":[]}
    # Iterate throught the RDP list
    for lAgentItemKeyStrItem in inGSettings["AgentDict"]:
        # Check UAC
        lKeyStr = f"{lAgentItemKeyStrItem[0]};{lAgentItemKeyStrItem[1]}" # turple ("HostNameUpperStr","UserUpperStr") > Str "HostNameUpperStr;UserUpperStr"
        if dUAC(inRoleKeyList=lUACAgentTemplateKeyList+[lKeyStr]):
            lDataItemDict = inGSettings["AgentDict"][lAgentItemKeyStrItem]
            lDataItemAgentDict = copy.deepcopy(lDataItemDict)
            lDataItemAgentDict["ActivityList"] = []
            lAgentDict[lKeyStr]=lDataItemAgentDict
            lHandlebarsDataItemDict = copy.deepcopy(lDataItemDict)
            lHandlebarsDataItemDict["HostnameUpperStr"]=lAgentItemKeyStrItem[0]
            lHandlebarsDataItemDict["UserUpperStr"]=lAgentItemKeyStrItem[1]
            lHandlebarsDataItemDict["ActivityList"] = []
            lAgentDict["HandlebarsList"].append(lHandlebarsDataItemDict)
    return lAgentDict


#v1.2.0 Send data container to the client from the server
# /pyOpenRPA/ServerData return {"HashStr" , "ServerDataDict": {"CPKeyStr":{"HTMLStr":"", DataDict:{}}}}

# Client: mGlobal.pyOpenRPA.ServerDataHashStr
# Client: mGlobal.pyOpenRPA.ServerDataDict
def pyOpenRPA_ServerData(inRequest,inGSettings):

    # Extract the hash value from request
    lValueStr = None
    if inRequest.headers.get('Content-Length') is not None:
        lInputByteArrayLength = int(inRequest.headers.get('Content-Length'))
        lInputByteArray = inRequest.rfile.read(lInputByteArrayLength)
        # Превращение массива байт в объект
        lValueStr = (lInputByteArray.decode('utf8'))
    # Generate ServerDataDict
    lFlagDoGenerateBool = True
    while lFlagDoGenerateBool:
        lServerDataDict = {
            "CPDict": HiddenCPDictGenerate(inRequest=inRequest, inGSettings=inGSettings),
            "RDPDict": HiddenRDPDictGenerate(inRequest=inRequest, inGSettings=inGSettings),
            "AgentDict": HiddenAgentDictGenerate(inRequest=inRequest, inGSettings=inGSettings),
            "UserDict": {"UACClientDict": inRequest.OpenRPA["DefUserRoleHierarchyGet"](), "CWDPathStr": os.getcwd(), "VersionStr": inGSettings["VersionStr"]},
        }
        # Create JSON
        lServerDataDictJSONStr = json.dumps(lServerDataDict)
        # Generate hash
        lServerDataHashStr = str(hash(lServerDataDictJSONStr))
        if lValueStr!=lServerDataHashStr and lServerDataHashStr!= "" and lServerDataHashStr!= None: # Case if Hash is not equal
            lFlagDoGenerateBool = False
        else: # Case Hashes are equal
            time.sleep(inGSettings["Client"]["Session"]["ControlPanelRefreshIntervalSecFloat"])
    # Return the result if Hash is changed
    lResult = {"HashStr": lServerDataHashStr, "ServerDataDict": lServerDataDict}
    inResponseDict = inRequest.OpenRPAResponseDict
    # Send message back to client
    message = json.dumps(lResult)
    # Write content as utf-8 data
    inResponseDict["Body"] = bytes(message, "utf8")
    return lResult

# GET
# /pyOpenRPA/ServerJSInit return JavaScript to init on page
def pyOpenRPA_ServerJSInit(inRequest,inGSettings):
    lResultStr = HiddenJSInitGenerate(inRequest=inRequest, inGSettings=inGSettings)
    inResponseDict = inRequest.OpenRPAResponseDict
    if lResultStr is None:
        lResultStr = ""
    # Write content as utf-8 data
    inResponseDict["Body"] = bytes(lResultStr, "utf8")

#v1.2.0 Send data container to the client from the server
# /pyOpenRPA/ServerLog return {"HashStr" , "ServerLogList": ["row 1", "row 2"]}
# Client: mGlobal.pyOpenRPA.ServerLogListHashStr
# Client: mGlobal.pyOpenRPA.ServerLogList
def pyOpenRPA_ServerLog(inRequest,inGSDict):
    # Extract the hash value from request
    lValueStr = None
    if inRequest.headers.get('Content-Length') is not None:
        lInputByteArrayLength = int(inRequest.headers.get('Content-Length'))
        lInputByteArray = inRequest.rfile.read(lInputByteArrayLength)
        # Превращение массива байт в объект
        lValueStr = (lInputByteArray.decode('utf8'))
    # Generate ServerDataDict
    lFlagDoGenerateBool = True
    while lFlagDoGenerateBool:
        lServerLogList = inGSDict["Client"]["DumpLogList"]
        # Get hash
        lServerLogListHashStr = inGSDict["Client"]["DumpLogListHashStr"]
        if lValueStr!=lServerLogListHashStr and lServerLogListHashStr!= "" and lServerLogListHashStr!= None: # Case if Hash is not equal Fix because None can be obtained without JSON decode
            lFlagDoGenerateBool = False
        else: # Case Hashes are equal
            time.sleep(inGSDict["Client"]["DumpLogListRefreshIntervalSecFloat"])
    # Return the result if Hash is changed
    lResult = {"HashStr": lServerLogListHashStr, "ServerLogList": lServerLogList}
    inResponseDict = inRequest.OpenRPAResponseDict
    # Send message back to client
    message = json.dumps(lResult)
    # Write content as utf-8 data
    inResponseDict["Body"] = bytes(message, "utf8")
    return lResult

def pyOpenRPA_Screenshot(inRequest,inGlobalDict):
    # Get Screenshot
    def SaveScreenshot(inFilePath):
        # grab fullscreen
        # Save the entire virtual screen as a PNG
        lScreenshot = getScreenAsImage()
        lScreenshot.save('screenshot.png', format='png')
        # lScreenshot = ScreenshotSecondScreen.grab_screen()
        # save image file
        # lScreenshot.save('screenshot.png')
    # Сохранить файл на диск
    SaveScreenshot("Screenshot.png")
    lFileObject = open("Screenshot.png", "rb")
    # Write content as utf-8 data
    inRequest.OpenRPAResponseDict["Body"] = lFileObject.read()
    # Закрыть файловый объект
    lFileObject.close()
# Add activity item or activity list to the processor queue
# Body is Activity item or Activity List
def pyOpenRPA_Processor(inRequest, inGSettings):
    lL = inGSettings["Logger"]
    # Recieve the data
    lValueStr = None
    if inRequest.headers.get('Content-Length') is not None:
        lInputByteArrayLength = int(inRequest.headers.get('Content-Length'))
        lInputByteArray = inRequest.rfile.read(lInputByteArrayLength)
        # Превращение массива байт в объект
        lInput = json.loads(lInputByteArray.decode('utf8'))
    # If list - operator plus
    if type(lInput) is list:
        # Logging info about processor activity if not SuperToken ()
        if not __Orchestrator__.WebUserIsSuperToken(inRequest=inRequest, inGSettings=inGSettings):
            lActivityTypeListStr = ""
            try:
                for lActivityItem in lInput:
                    lActivityTypeListStr += f"{lActivityItem['Def']}; "
            except Exception as e:
                lActivityTypeListStr = "Has some error with Activity Type read"
            lWebAuditMessageStr = __Orchestrator__.WebAuditMessageCreate(inRequest=inRequest,inOperationCodeStr=lActivityTypeListStr, inMessageStr="pyOpenRPA_Processor")
            if lL: lL.info(lWebAuditMessageStr)
        # Separate into 2 lists - sync and async
        lSyncActvityList = []
        lAsyncActivityList = []
        for lActivityItem in lInput:
            if lInput.get("ThreadBool", False) == False:
                lSyncActvityList.append(lActivityItem)
            else:
                lAsyncActivityList.append(lActivityItem)
        # Sync: Append in list
        inGSettings["ProcessorDict"]["ActivityList"]+=lSyncActvityList
        # Async: go to run
        if len(lAsyncActivityList)>0:
            for lActivityItem in lAsyncActivityList:
                lActivityItemArgsDict = {"inGSettings":inGSettings,"inActivityList":[lActivityItem]}
                lThread = threading.Thread(target=Processor.ActivityListExecute, kwargs=lActivityItemArgsDict)
                lThread.start()
    else:
        # Logging info about processor activity if not SuperToken ()
        if not __Orchestrator__.WebUserIsSuperToken(inRequest=inRequest, inGSettings=inGSettings):
            lActivityTypeListStr = ""
            try:
                lActivityTypeListStr = lInput['Def']
            except Exception as e:
                lActivityTypeListStr = "Has some error with Activity Type read"
            lWebAuditMessageStr = __Orchestrator__.WebAuditMessageCreate(inRequest=inRequest,inOperationCodeStr=lActivityTypeListStr, inMessageStr="pyOpenRPA_Processor")
            if lL: lL.info(lWebAuditMessageStr)
        if lInput.get("ThreadBool",False) == False:
            # Append in list
            inGSettings["ProcessorDict"]["ActivityList"].append(lInput)
        else:
            lActivityItemArgsDict = {"inGSettings": inGSettings, "inActivityList": [lInput]}
            lThread = threading.Thread(target=Processor.ActivityListExecute, kwargs=lActivityItemArgsDict)
            lThread.start()
# Execute activity list
def pyOpenRPA_ActivityListExecute(inRequest, inGSettings):
    # Recieve the data
    lL = inGSettings["Logger"]
    lValueStr = None
    if inRequest.headers.get('Content-Length') is not None:
        lInputByteArrayLength = int(inRequest.headers.get('Content-Length'))
        lInputByteArray = inRequest.rfile.read(lInputByteArrayLength)
        # Превращение массива байт в объект
        lInput = json.loads(lInputByteArray.decode('utf8'))
    # If list - operator plus
    if type(lInput) is list:
        # Logging info about processor activity if not SuperToken ()
        if not __Orchestrator__.WebUserIsSuperToken(inRequest=inRequest, inGSettings=inGSettings):
            lActivityTypeListStr = ""
            try:
                for lActivityItem in lInput:
                    lActivityTypeListStr += f"{lActivityItem['Def']}; "
            except Exception as e:
                lActivityTypeListStr = "Has some error with Activity Type read"
            lWebAuditMessageStr = __Orchestrator__.WebAuditMessageCreate(inRequest=inRequest,inOperationCodeStr=lActivityTypeListStr, inMessageStr="pyOpenRPA_ActivityListExecute")
            if lL: lL.info(lWebAuditMessageStr)
        # Execution
        lResultList = Processor.ActivityListExecute(inGSettings = inGSettings, inActivityList = lInput)
        inRequest.OpenRPAResponseDict["Body"] = bytes(json.dumps(lResultList), "utf8")
    else:
        # Logging info about processor activity if not SuperToken ()
        if not __Orchestrator__.WebUserIsSuperToken(inRequest=inRequest, inGSettings=inGSettings):
            lActivityTypeListStr = ""
            try:
                lActivityTypeListStr = lInput['Def']
            except Exception as e:
                lActivityTypeListStr = "Has some error with Activity Type read"
            lWebAuditMessageStr = __Orchestrator__.WebAuditMessageCreate(inRequest=inRequest,
                                                                         inOperationCodeStr=lActivityTypeListStr,
                                                                         inMessageStr="pyOpenRPA_ActivityListExecute")
            if lL: lL.info(lWebAuditMessageStr)
        # Execution
        lResultList = Processor.ActivityListExecute(inGSettings = inGSettings, inActivityList = [lInput])
        inRequest.OpenRPAResponseDict["Body"] = bytes(json.dumps(lResultList[0]), "utf8")

# See docs in Agent (pyOpenRPA.Agent.O2A)
def pyOpenRPA_Agent_O2A(inRequest, inGSettings):
    lL = inGSettings["Logger"] # Alias
    lConnectionLifetimeSecFloat = inGSettings["ServerDict"]["AgentConnectionLifetimeSecFloat"] # 300.0 # 5 min * 60 sec 300.0
    lActivityItemLifetimeLimitSecFloat = inGSettings["ServerDict"]["AgentActivityLifetimeSecFloat"]
    lAgentLoopSleepSecFloat = inGSettings["ServerDict"]["AgentLoopSleepSecFloat"]
    lTimeStartFloat = time.time()
    # Recieve the data
    lValueStr = None
    if inRequest.headers.get('Content-Length') is not None:
        lInputByteArrayLength = int(inRequest.headers.get('Content-Length'))
        lInputByteArray = inRequest.rfile.read(lInputByteArrayLength)
        # Превращение массива байт в объект
        lInput = json.loads(lInputByteArray.decode('utf8'))
    # Check if item is created
    lAgentDictItemKeyTurple = (lInput["HostNameUpperStr"],lInput["UserUpperStr"])
    if lAgentDictItemKeyTurple not in inGSettings["AgentDict"]:
        inGSettings["AgentDict"][lAgentDictItemKeyTurple] = SettingsTemplate.__AgentDictItemCreate__()
    lThisAgentDict = inGSettings["AgentDict"][lAgentDictItemKeyTurple]
    lThisAgentDict["IsListenBool"]=True # Set is online
    lThisAgentDict["ConnectionCountInt"] += 1  # increment connection count
    # Test solution
    lDoLoopBool = True
    try:
        while lDoLoopBool:
            # Check if lifetime is over
            if time.time() - lTimeStartFloat > lConnectionLifetimeSecFloat: # Lifetime is over
                lThisAgentDict["IsListenBool"] = False  # Set is offline
                lDoLoopBool = False
            else: # Lifetime is good - do alg
                lThisAgentDict["IsListenBool"] = True  # Set is online
                lQueueList = lThisAgentDict["ActivityList"]
                if len(lQueueList)>0:# Do some operations if has queue items
                    # check if delta datetime is < than ActivityLifeTimeSecFloat
                    lActivityItem = lThisAgentDict["ActivityList"][0]
                    lActivityLifetimeSecFloat = (datetime.datetime.now() - lActivityItem["CreatedByDatetime"]).total_seconds()
                    # Check case if limit is expired - remove item
                    if lActivityLifetimeSecFloat > lActivityItemLifetimeLimitSecFloat:
                        lActivityItem = lThisAgentDict["ActivityList"].pop(0)
                    else:
                        lReturnActivityItemList = []
                        lReturnActivityItemDict = None
                        # If lInput['ActivityLastGUIDStr'] is '' > return 0 element for send in Agent
                        if lInput['ActivityLastGUIDStr'] == "":
                            lReturnActivityItemList=lQueueList # 2022 02 21 - Maslov Return list - not one item
                        else:
                            # go from the end - search element with GUIDStr
                            lForTriggerGetNextItem = False
                            for lForActivityItemDict in lQueueList:
                                if lForTriggerGetNextItem == True:
                                    lReturnActivityItemDict = lForActivityItemDict
                                    lReturnActivityItemList.append(lReturnActivityItemDict) # 2022 02 21 - Maslov Return list - not one item
                                    #break
                                if lForActivityItemDict['GUIDStr'] == lInput['ActivityLastGUIDStr']: lForTriggerGetNextItem = True
                            # CASE if GUID is not detected - return 0 element
                            if (len(lQueueList)==1 and lQueueList[0]['GUIDStr'] != lInput['ActivityLastGUIDStr']):
                                #lReturnActivityItemDict = lThisAgentDict["ActivityList"][0]
                                lReturnActivityItemList=lQueueList # 2022 02 21 - Maslov Return list - not one item
                        # Send QUEUE ITEM
                        if len(lReturnActivityItemList) > 0:
                            lReturnActivityItemList = copy.deepcopy(lReturnActivityItemList)
                            for lItemDict in lReturnActivityItemList:
                                if "CreatedByDatetime" in lItemDict:
                                    del lItemDict["CreatedByDatetime"]
                            inRequest.OpenRPAResponseDict["Body"] = bytes(json.dumps(lReturnActivityItemList), "utf8")
                            # Log full version if bytes size is less than limit . else short
                            lBodyLenInt = len(inRequest.OpenRPAResponseDict["Body"])
                            lAgentLimitLogSizeBytesInt = inGSettings["ServerDict"]["AgentLimitLogSizeBytesInt"]
                            if lL: lL.debug(f"ActivityItem to Agent ({lInput['HostNameUpperStr']}, {lInput['UserUpperStr']}): Item count: {len(lReturnActivityItemList)}, bytes size: {lBodyLenInt}")                            
                            lDoLoopBool = False # CLose the connection
                        else: # Nothing to send - sleep for the next iteration
                            time.sleep(lAgentLoopSleepSecFloat)
                else: # no queue item - sleep for the next iteration
                    time.sleep(lAgentLoopSleepSecFloat)
    except Exception as e:
        if lL: lL.exception("pyOpenRPA_Agent_O2A Exception!")
    lThisAgentDict["ConnectionCountInt"] -= 1  # Connection go to be closed - decrement the connection count

def pyOpenRPA_Debugging_HelperDefList(inRequest, inGSettings):
    # Parse query
    lResultDict = {
        "success": True,
        "results": []
    }
    # Get the path
    lPathSplitList = __Orchestrator__.WebRequestParsePath(inRequest=inRequest).split('/')
    lQueryStr = None
    if "HelperDefList" != lPathSplitList[-1] and "" != lPathSplitList[-1]: lQueryStr = lPathSplitList[-1]
    if lQueryStr != "" and lQueryStr is not None:
        lDefList = __Orchestrator__.ActivityItemHelperDefList(inDefQueryStr=lQueryStr)
        for lDefStr in lDefList:
            lResultDict["results"].append({"name": lDefStr, "value": lDefStr, "text": lDefStr})
    __Orchestrator__.WebRequestResponseSend(inRequest=inRequest, inResponeStr=json.dumps(lResultDict))

def pyOpenRPA_Debugging_HelperDefAutofill(inRequest, inGSettings):
    # Parse query
    # Get the path
    lPathSplitList = __Orchestrator__.WebRequestParsePath(inRequest=inRequest).split('/')
    lQueryStr = None
    if "HelperDefAutofill" != lPathSplitList[-1] and "" != lPathSplitList[-1]: lQueryStr = lPathSplitList[-1]
    lResultDict = __Orchestrator__.ActivityItemHelperDefAutofill(inDef = lQueryStr)
    __Orchestrator__.WebRequestResponseSend(inRequest=inRequest, inResponeStr=json.dumps(lResultDict))

# See docs in Agent (pyOpenRPA.Agent.A2O)
def pyOpenRPA_Agent_A2O(inRequest, inGSettings):
    lL = inGSettings["Logger"]
    # Recieve the data
    lValueStr = None
    if inRequest.headers.get('Content-Length') is not None:
        lInputByteArrayLength = int(inRequest.headers.get('Content-Length'))
        lInputByteArray = inRequest.rfile.read(lInputByteArrayLength)
        # Превращение массива байт в объект
        lInput = json.loads(lInputByteArray.decode('utf8'))
        lAgentDictItemKeyTurple = (lInput["HostNameUpperStr"], lInput["UserUpperStr"])
    if "LogList" in lInput:
        for lLogItemStr in lInput["LogList"]:
            inGSettings["Logger"].info(lLogItemStr)
    if "ActivityReturnDict" in lInput:
        for lActivityReturnItemKeyStr in lInput["ActivityReturnDict"]:
            lActivityReturnItemValue = lInput["ActivityReturnDict"][lActivityReturnItemKeyStr]
            # Create item in gSettings
            inGSettings["AgentActivityReturnDict"][lActivityReturnItemKeyStr]=SettingsTemplate.__AgentActivityReturnDictItemCreate__(inReturn=lActivityReturnItemValue)
            lLogStr = "x bytes"
            try:
                if lActivityReturnItemValue is not None:
                    lLogStr = f"{len(lActivityReturnItemValue)} bytes"
            except Exception as e:
                pass 
            if lL: lL.debug(f"SERVER: pyOpenRPA_Agent_A2O:: Has recieved result of the activity items from agent! ActivityItem GUID Str: {lActivityReturnItemKeyStr}; Return value len: {lLogStr}")
            # Delete the source activity item from AgentDict
            if lAgentDictItemKeyTurple in inGSettings["AgentDict"]:
                lAgentDictActivityListNew = []
                lAgentDict = inGSettings["AgentDict"][lAgentDictItemKeyTurple]
                for lActivityItem in lAgentDict["ActivityList"]:
                    if lActivityReturnItemKeyStr != lActivityItem.get("GUIDStr",None):
                        lAgentDictActivityListNew.append(lActivityItem)
                    else:
                        del lActivityItem
                        if lL: lL.debug(f"SERVER: pyOpenRPA_Agent_A2O:: Source activity item request was deleted from the orchestrator. ActivityItem GUID Str: {lActivityReturnItemKeyStr}")
                inGSettings["AgentDict"][lAgentDictItemKeyTurple]["ActivityList"] = lAgentDictActivityListNew
def SettingsUpdate(inGlobalConfiguration):
    import os
    import pyOpenRPA.Orchestrator
    lOrchestratorFolder = "\\".join(pyOpenRPA.Orchestrator.__file__.split("\\")[:-1])
    lURLList = \
        [ #List of available URLs with the orchestrator server
            #{
            #    "Method":"GET|POST",
            #    "URL": "/index", #URL of the request
            #    "MatchType": "", #"BeginWith|Contains|Equal|EqualCase",
            #    "ResponseFilePath": "", #Absolute or relative path
            #    "ResponseFolderPath": "", #Absolute or relative path
            #    "ResponseContentType": "", #HTTP Content-type
            #    "ResponseDefRequestGlobal": None #Function with str result
            #}
            #Orchestrator basic dependencies # Index page in server.py because of special settings
            {"Method":"GET", "URL": "/Index.js", "MatchType": "EqualCase", "ResponseFilePath": os.path.join(lOrchestratorFolder, "Web\\Index.js"), "ResponseContentType": "text/javascript"},
            {"Method":"GET", "URL": "/3rdParty/Semantic-UI-CSS-master/semantic.min.css", "MatchType": "EqualCase", "ResponseFilePath": os.path.join(lOrchestratorFolder, "..\\Resources\\Web\\Semantic-UI-CSS-master\\semantic.min.css"), "ResponseContentType": "text/css", "UACBool":False, "UseCacheBool": True},
            {"Method":"GET", "URL": "/3rdParty/Semantic-UI-CSS-master/semantic.min.js", "MatchType": "EqualCase", "ResponseFilePath": os.path.join(lOrchestratorFolder, "..\\Resources\\Web\\Semantic-UI-CSS-master\\semantic.min.js"), "ResponseContentType": "application/javascript", "UACBool":False, "UseCacheBool": True},
            {"Method":"GET", "URL": "/3rdParty/jQuery/jquery-3.1.1.min.js", "MatchType": "EqualCase", "ResponseFilePath": os.path.join(lOrchestratorFolder, "..\\Resources\\Web\\jQuery\\jquery-3.1.1.min.js"), "ResponseContentType": "application/javascript", "UACBool":False, "UseCacheBool": True},
            {"Method":"GET", "URL": "/3rdParty/Google/LatoItalic.css", "MatchType": "EqualCase", "ResponseFilePath": os.path.join(lOrchestratorFolder, "..\\Resources\\Web\\Google\\LatoItalic.css"), "ResponseContentType": "font/css", "UACBool":False, "UseCacheBool": True},
            {"Method":"GET", "URL": "/3rdParty/Semantic-UI-CSS-master/themes/default/assets/fonts/icons.woff2", "MatchType": "EqualCase", "ResponseFilePath": os.path.join(lOrchestratorFolder, "..\\Resources\\Web\\Semantic-UI-CSS-master\\themes\\default\\assets\\fonts\\icons.woff2"), "ResponseContentType": "font/woff2", "UACBool":False, "UseCacheBool": True},
            {"Method":"GET", "URL": "/themes/default/", "MatchType": "BeginWith", "ResponseFolderPath": os.path.join(lOrchestratorFolder, "..\\Resources\\Web\\Semantic-UI-CSS-master\\themes\\default"),"UACBool":False, "UseCacheBool": True},            
            {"Method":"GET", "URL": "/favicon.ico", "MatchType": "EqualCase", "ResponseFilePath": os.path.join(lOrchestratorFolder, "Web\\favicon.ico"), "ResponseContentType": "image/x-icon", "UACBool":False, "UseCacheBool": True},
            {"Method":"GET", "URL": "/3rdParty/Handlebars/handlebars-v4.1.2.js", "MatchType": "EqualCase", "ResponseFilePath": os.path.join(lOrchestratorFolder, "..\\Resources\\Web\\Handlebars\\handlebars-v4.1.2.js"), "ResponseContentType": "application/javascript", "UACBool":False, "UseCacheBool": True},
            {"Method": "GET", "URL": "/Monitor/ControlPanelDictGet", "MatchType": "Equal", "ResponseDefRequestGlobal": BackwardCompatibility.v1_2_0_Monitor_ControlPanelDictGet_SessionCheckInit, "ResponseContentType": "application/json"},
            {"Method": "GET", "URL": "/GetScreenshot", "MatchType": "BeginWith", "ResponseDefRequestGlobal": pyOpenRPA_Screenshot, "ResponseContentType": "image/png"},
            {"Method": "GET", "URL": "/pyOpenRPA_logo.png", "MatchType": "Equal", "ResponseFilePath": os.path.join(lOrchestratorFolder, "..\\Resources\\Web\\pyOpenRPA_logo.png"), "ResponseContentType": "image/png", "UACBool":False, "UseCacheBool": True},
            {"Method": "POST", "URL": "/Orchestrator/UserRoleHierarchyGet", "MatchType": "Equal","ResponseDefRequestGlobal": BackwardCompatibility.v1_2_0_UserRoleHierarchyGet, "ResponseContentType": "application/json"},
            # New way of the v.1.2.0 functionallity (all defs by the URL from /pyOpenRPA/...)
            {"Method": "POST", "URL": "/pyOpenRPA/ServerData", "MatchType": "Equal","ResponseDefRequestGlobal": pyOpenRPA_ServerData, "ResponseContentType": "application/json"},
            {"Method": "GET", "URL": "/pyOpenRPA/ServerJSInit", "MatchType": "Equal","ResponseDefRequestGlobal": pyOpenRPA_ServerJSInit, "ResponseContentType": "application/javascript"},
            {"Method": "POST", "URL": "/pyOpenRPA/ServerLog", "MatchType": "Equal","ResponseDefRequestGlobal": pyOpenRPA_ServerLog, "ResponseContentType": "application/json"},
            {"Method": "GET", "URL": "/pyOpenRPA/Screenshot", "MatchType": "BeginWith", "ResponseDefRequestGlobal": pyOpenRPA_Screenshot, "ResponseContentType": "image/png"},
            {"Method": "POST", "URL": "/pyOpenRPA/ProcessorQueueAdd", "MatchType": "Equal","ResponseDefRequestGlobal": pyOpenRPA_Processor, "ResponseContentType": "application/json"},
            {"Method": "POST", "URL": "/pyOpenRPA/ActivityListExecute", "MatchType": "Equal","ResponseDefRequestGlobal": pyOpenRPA_ActivityListExecute, "ResponseContentType": "application/json"},
            {"Method": "POST", "URL": "/pyOpenRPA/Agent/O2A", "MatchType": "Equal","ResponseDefRequestGlobal": pyOpenRPA_Agent_O2A, "ResponseContentType": "application/json"},
            {"Method": "POST", "URL": "/pyOpenRPA/Agent/A2O", "MatchType": "Equal","ResponseDefRequestGlobal": pyOpenRPA_Agent_A2O, "ResponseContentType": "application/json"},
            {"Method": "GET", "URL": "/pyOpenRPA/Debugging/HelperDefList/", "MatchType": "BeginWith","ResponseDefRequestGlobal": pyOpenRPA_Debugging_HelperDefList, "ResponseContentType": "application/json"},
            {"Method": "GET", "URL": "/pyOpenRPA/Debugging/HelperDefAutofill/", "MatchType": "BeginWith","ResponseDefRequestGlobal": pyOpenRPA_Debugging_HelperDefAutofill, "ResponseContentType": "application/json"},
    ]
    Usage.Process(inComponentStr="Orchestrator")
    inGlobalConfiguration["ServerDict"]["URLList"]=inGlobalConfiguration["ServerDict"]["URLList"]+lURLList
    return inGlobalConfiguration