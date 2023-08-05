#     inRequest.OpenRPA = {}
#     inRequest.OpenRPA["AuthToken"] = None
#     inRequest.OpenRPA["Domain"] = None
#     inRequest.OpenRPA["User"] = None

# lResponseDict = {"Headers": {}, "SetCookies": {}, "Body": b"", "StatusCode": None}
# self.OpenRPAResponseDict = lResponseDict

from http.server import BaseHTTPRequestHandler, HTTPServer
from socketserver import ThreadingMixIn
import threading
import json
from threading import Thread
import inspect
from . import Processor # Add new processor
from . import ProcessorOld # Support old processor - deprecated defs only for backward compatibility
import urllib.parse # decode URL in string
import importlib
import pdb
import base64
import uuid
import datetime
import os #for path operations
from http import cookies
global gSettingsDict
from . import ServerSettings
from . import __Orchestrator__
import copy
import mimetypes
mimetypes.add_type("font/woff2",".woff2")

gCacheDict = {}


# Tool to merge complex dictionaries
def __ComplexDictMerge2to1__(in1Dict, in2Dict):
    lPathList=None
    if lPathList is None: lPathList = []
    for lKeyStr in in2Dict:
        if lKeyStr in in1Dict:
            if isinstance(in1Dict[lKeyStr], dict) and isinstance(in2Dict[lKeyStr], dict):
                __ComplexDictMerge2to1__(in1Dict[lKeyStr], in2Dict[lKeyStr])
            elif in1Dict[lKeyStr] == in2Dict[lKeyStr]:
                pass  # same leaf value
            else:
                raise Exception('Conflict at %s' % '.'.join(lPathList + [str(lKeyStr)]))
        else:
            in1Dict[lKeyStr] = in2Dict[lKeyStr]
    return in1Dict

# Tool to merge complex dictionaries - no exceptions, just overwrite dict 2 in dict 1
def __ComplexDictMerge2to1Overwrite__(in1Dict, in2Dict):
    """
    Merge in2Dict in in1Dict. In conflict override and get value from dict 2

    :param in1Dict: Source dict. Save the link (structure)
    :param in2Dict: New data dict
    :return: Merged dict 1
    """
    lPathList=None
    if lPathList is None: lPathList = []
    for lKeyStr in in2Dict:
        if lKeyStr in in1Dict:
            if isinstance(in1Dict[lKeyStr], dict) and isinstance(in2Dict[lKeyStr], dict):
                __ComplexDictMerge2to1Overwrite__(in1Dict[lKeyStr], in2Dict[lKeyStr])
            else:
                in1Dict[lKeyStr] = in2Dict[lKeyStr]
        else:
            in1Dict[lKeyStr] = in2Dict[lKeyStr]
    return in1Dict

#Authenticate function ()
# return dict
# {
#   "Domain": "", #Empty if Auth is not success
#   "User": "" #Empty if Auth is not success
# }
def AuthenticateVerify(inRequest):
    lResult={"Domain": "", "User": ""}
    ######################################
    #Way 1 - try to find AuthToken
    lCookies = cookies.SimpleCookie(inRequest.headers.get("Cookie", ""))
    #pdb.set_trace()
    if "AuthToken" in lCookies:
        lCookieAuthToken = lCookies.get("AuthToken", "").value
        if lCookieAuthToken:
            #Find AuthToken in GlobalDict
            if lCookieAuthToken in gSettingsDict.get("ServerDict", {}).get("AccessUsers", {}).get("AuthTokensDict", {}):
                #Auth Token Has Been Founded
                lResult["Domain"] = gSettingsDict["ServerDict"]["AccessUsers"]["AuthTokensDict"][lCookieAuthToken]["Domain"]
                lResult["User"] = gSettingsDict["ServerDict"]["AccessUsers"]["AuthTokensDict"][lCookieAuthToken]["User"]
                #Set auth token
                inRequest.OpenRPA["AuthToken"] = lCookieAuthToken
                inRequest.OpenRPA["Domain"] = lResult["Domain"]
                inRequest.OpenRPA["User"] = lResult["User"]
                #Exit earlier
                return lResult
    ######################################
    #Way 2 - try to logon
    lHeaderAuthorization = inRequest.headers.get("Authorization", "").split(" ")
    if len(lHeaderAuthorization) == 2:
        llHeaderAuthorizationDecodedUserPasswordList = base64.b64decode(lHeaderAuthorization[1]).decode("utf-8").split(
            ":")
        lUser = llHeaderAuthorizationDecodedUserPasswordList[0]
        lPassword = llHeaderAuthorizationDecodedUserPasswordList[1]
        lDomain = ""
        if "\\" in lUser:
            lDomain = lUser.split("\\")[0]
            lUser = lUser.split("\\")[1]
        lLogonBool = __Orchestrator__.OSCredentialsVerify(inUserStr=lUser, inPasswordStr=lPassword, inDomainStr=lDomain)
        #Check result
        if lLogonBool:
            lResult["Domain"] = lDomain
            lResult["User"] = lUser
            #Create token
            lAuthToken=str(uuid.uuid1())
            gSettingsDict["ServerDict"]["AccessUsers"]["AuthTokensDict"][lAuthToken] = {}
            gSettingsDict["ServerDict"]["AccessUsers"]["AuthTokensDict"][lAuthToken]["Domain"] = lResult["Domain"]
            gSettingsDict["ServerDict"]["AccessUsers"]["AuthTokensDict"][lAuthToken]["User"] = lResult["User"]
            gSettingsDict["ServerDict"]["AccessUsers"]["AuthTokensDict"][lAuthToken]["FlagDoNotExpire"] = False
            gSettingsDict["ServerDict"]["AccessUsers"]["AuthTokensDict"][lAuthToken]["TokenDatetime"] = datetime.datetime.now()
            #Set-cookie
            inRequest.OpenRPA["AuthToken"] = lAuthToken
            inRequest.OpenRPA["Domain"] = lResult["Domain"]
            inRequest.OpenRPA["User"] = lResult["User"]
            inRequest.OpenRPASetCookie = {}
            #New engine of server
            inRequest.OpenRPAResponseDict["SetCookies"]["AuthToken"] = lAuthToken
            #inRequest.OpenRPAResponse["Set-Cookie"]=[]lResult["Set-Cookie"] = lAuthToken
            #pdb.set_trace()
            #inRequest.send_header("Set-Cookie:", f"AuthToken={lAuthToken}")
    ######################################
    return lResult
def AuthenticateBlock(inRequest):
    # Send response status code
    inRequest.send_response(401)
    # Send headers
    inRequest.send_header('Content-type', 'text/html')
    inRequest.send_header('WWW-Authenticate', 'Basic')  # Always ask login pass
    inRequest.end_headers()
    # Write content as utf-8 data
    inRequest.wfile.write(bytes("", "utf8"))
#Check access before execute the action
#return bool True - go execute, False - dont execute
def UserAccessCheckBefore(inMethod, inRequest):
    # Help def - Get access flag from dict
    #pdb.set_trace()
    def HelpGetFlag(inAccessRuleItem, inRequest, inGlobalDict, inAuthenticateDict):
        if "FlagAccess" in inAccessRuleItem:
            return inAccessRuleItem["FlagAccess"]
        elif "FlagAccessDefRequestGlobalAuthenticate" in inAccessRuleItem:
            return inAccessRuleItem["FlagAccessDefRequestGlobalAuthenticate"](inRequest, inGlobalDict,
                                                                              inAuthenticateDict)
    ##########################################
    inMethod=inMethod.upper()
    #Prepare result false
    lResult = False
    lAuthToken = inRequest.OpenRPA["AuthToken"]
    #go next if user is identified
    lUserDict = None
    if lAuthToken:
        lUserDict = gSettingsDict["ServerDict"]["AccessUsers"]["AuthTokensDict"][lAuthToken]
    #pdb.set_trace()
    ########################################
    ########################################
    #Check general before rule (without User domain)
    #Check rules
    inRuleMatchURLList = gSettingsDict.get("ServerDict", {}).get("AccessUsers", {}).get("RuleMethodMatchURLBeforeList", [])
    for lAccessRuleItem in inRuleMatchURLList:
        #Go next execution if flag is false
        if not lResult:
            #Check if Method is identical
            if lAccessRuleItem["Method"].upper() == inMethod:
                #check Match type variant: BeginWith
                if lAccessRuleItem["MatchType"].upper() == "BEGINWITH":
                    lURLPath = inRequest.path
                    lURLPath = lURLPath.upper()
                    if lURLPath.startswith(lAccessRuleItem["URL"].upper()):
                        lResult = HelpGetFlag(lAccessRuleItem, inRequest, gSettingsDict, lUserDict)
                # check Match type variant: Contains
                elif lAccessRuleItem["MatchType"].upper() == "CONTAINS":
                    lURLPath = inRequest.path
                    lURLPath = lURLPath.upper()
                    if lURLPath.contains(lAccessRuleItem["URL"].upper()):
                        lResult = HelpGetFlag(lAccessRuleItem, inRequest, gSettingsDict, lUserDict)
                # check Match type variant: Equal
                elif lAccessRuleItem["MatchType"].upper() == "EQUAL":
                    if lAccessRuleItem["URL"].upper() == inRequest.path.upper():
                        lResult = HelpGetFlag(lAccessRuleItem, inRequest, gSettingsDict, lUserDict)
                # check Match type variant: EqualCase
                elif lAccessRuleItem["MatchType"].upper() == "EQUALCASE":
                    if lAccessRuleItem["URL"] == inRequest.path:
                        lResult = HelpGetFlag(lAccessRuleItem, inRequest, gSettingsDict, lUserDict)
    #########################################
    #########################################
    #Do check if lResult is false
    if not lResult:
        #Check access by User Domain
        #Check rules to find first appicable
        #Check rules
        lMethodMatchURLList = gSettingsDict.get("ServerDict", {}).get("AccessUsers", {}).get("RuleDomainUserDict", {}).get((lUserDict["Domain"].upper(), lUserDict["User"].upper()), {}).get("MethodMatchURLBeforeList", [])
        if len(lMethodMatchURLList) > 0:
            for lAccessRuleItem in lMethodMatchURLList:
                #Go next execution if flag is false
                if not lResult:
                    #Check if Method is identical
                    if lAccessRuleItem["Method"].upper() == inMethod:
                        #check Match type variant: BeginWith
                        if lAccessRuleItem["MatchType"].upper() == "BEGINWITH":
                            lURLPath = inRequest.path
                            lURLPath = lURLPath.upper()
                            if lURLPath.startswith(lAccessRuleItem["URL"].upper()):
                                lResult = HelpGetFlag(lAccessRuleItem, inRequest, gSettingsDict, lUserDict)
                        #check Match type variant: Contains
                        elif lAccessRuleItem["MatchType"].upper() == "CONTAINS":
                            lURLPath = inRequest.path
                            lURLPath = lURLPath.upper()
                            if lURLPath.contains(lAccessRuleItem["URL"].upper()):
                                lResult = HelpGetFlag(lAccessRuleItem, inRequest, gSettingsDict, lUserDict)
                        # check Match type variant: Equal
                        elif lAccessRuleItem["MatchType"].upper() == "EQUAL":
                            if lAccessRuleItem["URL"].upper() == inRequest.path.upper():
                                lResult = HelpGetFlag(lAccessRuleItem, inRequest, gSettingsDict, lUserDict)
                        # check Match type variant: EqualCase
                        elif lAccessRuleItem["MatchType"].upper() == "EQUALCASE":
                            if lAccessRuleItem["URL"] == inRequest.path:
                                lResult = HelpGetFlag(lAccessRuleItem, inRequest, gSettingsDict, lUserDict)
        else:
            return True
    #####################################
    #####################################
    #Return lResult
    return lResult
# HTTPRequestHandler class
class testHTTPServer_RequestHandler(BaseHTTPRequestHandler):
    # Def to check User Role access grants
    def UACClientCheck(self, inRoleKeyList): # Alias
        return self.UserRoleAccessAsk(inRoleKeyList=inRoleKeyList)
    def UserRoleAccessAsk(self, inRoleKeyList):
        lResult = True # Init flag
        lRoleHierarchyDict = self.UserRoleHierarchyGet() # get the Hierarchy
        # Try to get value from key list
        lKeyValue = lRoleHierarchyDict # Init the base
        for lItem in inRoleKeyList:
            if type(lKeyValue) is dict:
                if lItem in lKeyValue: # Has key
                    lKeyValue = lKeyValue[lItem] # Get the value and go to the next loop iteration
                else: # Else branch - true or false
                    if len(lKeyValue)>0: # False - if Dict has some elements
                        lResult = False # Set the False Flag
                    else:
                        lResult = True # Set the True flag
                    break # Stop the loop
            else: # Has element with no detalization - return True
                lResult = True # Set the flag
                break # Close the loop
        return lResult # Return the result

    # Def to get hierarchy of the current user roles
    # if return {} - all is available
    def UserRoleHierarchyGet(self):
        lDomainUpperStr = self.OpenRPA["Domain"].upper()
        lUserUpperStr = self.OpenRPA["User"].upper()
        return gSettingsDict.get("ServerDict", {}).get("AccessUsers", {}).get("RuleDomainUserDict", {}).get((lDomainUpperStr, lUserUpperStr), {}).get("RoleHierarchyAllowedDict", {})

    #Tech def
    #return {"headers":[],"body":"","statuscode":111}
    def URLItemCheckDo(self, inURLItem, inMethod, inOnlyFlagUACBool = False):
        ###############################
        #Tech sub def - do item
        ################################
        def URLItemDo(inURLItem,inRequest,inGlobalDict):
            global gCacheDict
            inResponseDict = inRequest.OpenRPAResponseDict
            inResponseDict["Headers"]["Content-type"]= None
            #Set status code 200
            inResponseDict["StatusCode"] = 200
            #Content-type
            if "ResponseContentType" in inURLItem:
                inResponseDict["Headers"]["Content-type"] = inURLItem["ResponseContentType"]
            #If file path is set
            if "ResponseFilePath" in inURLItem:
                # Check cache
                if inURLItem.get("UseCacheBool",False) == True:
                    if inURLItem["ResponseFilePath"] in gCacheDict:
                        # Write content as utf-8 data
                        inResponseDict["Body"] = gCacheDict[inURLItem["ResponseFilePath"]]
                    else:
                        lFileObject = open(inURLItem["ResponseFilePath"], "rb")
                        # Write content as utf-8 data
                        gCacheDict[inURLItem["ResponseFilePath"]] = lFileObject.read()
                        inResponseDict["Body"] = gCacheDict[inURLItem["ResponseFilePath"]]
                        # Закрыть файловый объект
                        lFileObject.close()
                else:
                    lFileObject = open(inURLItem["ResponseFilePath"], "rb")
                    # Write content as utf-8 data
                    inResponseDict["Body"] = lFileObject.read()
                    # Закрыть файловый объект
                    lFileObject.close()
                # detect MIME type if none
                if inResponseDict["Headers"]["Content-type"] is None:
                    inResponseDict["Headers"]["Content-type"]= mimetypes.guess_type(inURLItem["ResponseFilePath"])[0]
            #If function is set
            if "ResponseDefRequestGlobal" in inURLItem:
                lDef = inURLItem["ResponseDefRequestGlobal"]
                lDefSignature = inspect.signature(lDef)
                if len(lDefSignature.parameters) == 2:
                    inURLItem["ResponseDefRequestGlobal"](inRequest, inGlobalDict)
                elif len(lDefSignature.parameters) == 1:
                    inURLItem["ResponseDefRequestGlobal"](inRequest)
                else:
                    inURLItem["ResponseDefRequestGlobal"]()                
            if "ResponseFolderPath" in inURLItem:

                #lRequestPath = inRequest.path
                lRequestPath = urllib.parse.unquote(inRequest.path)
                if inURLItem["URL"][-1]!="/": inURLItem["URL"]+= "/" # Fix for settings
                lFilePathSecondPart = lRequestPath.replace(inURLItem["URL"],"")
                lFilePath = os.path.join(inURLItem["ResponseFolderPath"],lFilePathSecondPart)
                #print(f"File full path {lFilePath}")
                #Check if file exist
                if os.path.exists(lFilePath) and os.path.isfile(lFilePath):
                    # Check cache
                    if inURLItem.get("UseCacheBool",False) == True:
                        if lFilePath in gCacheDict:
                            # Write content as utf-8 data
                            inResponseDict["Body"] = gCacheDict[lFilePath]
                        else:
                            lFileObject = open(lFilePath, "rb")
                            # Write content as utf-8 data
                            gCacheDict[lFilePath] = lFileObject.read()
                            inResponseDict["Body"] = gCacheDict[lFilePath]
                            # Закрыть файловый объект
                            lFileObject.close()
                    else:
                        lFileObject = open(lFilePath, "rb")
                        # Write content as utf-8 data
                        inResponseDict["Body"] = lFileObject.read()
                        # Закрыть файловый объект
                        lFileObject.close()
                    # detect MIME type if none
                    if inResponseDict["Headers"]["Content-type"] is None:
                        inResponseDict["Headers"]["Content-type"]= mimetypes.guess_type(lFilePath)[0]
            # If No content-type
            if inResponseDict["Headers"]["Content-type"] is None:
                inResponseDict["Headers"]["Content-type"]= "application/octet-stream"
        ##############################################
        # UAC Check 
        if inOnlyFlagUACBool == True and inURLItem.get("UACBool",None) in [None, True]:
            return False
        if inURLItem["Method"].upper() == inMethod.upper():
            # check Match type variant: BeginWith
            if inURLItem["MatchType"].upper() == "BEGINWITH":
                lURLPath = urllib.parse.unquote(self.path)
                lURLPath = lURLPath.upper()
                if lURLPath.startswith(inURLItem["URL"].upper()):
                    URLItemDo(inURLItem, self, gSettingsDict)
                    return True
            # check Match type variant: Contains
            elif inURLItem["MatchType"].upper() == "CONTAINS":
                lURLPath = urllib.parse.unquote(self.path)
                lURLPath = lURLPath.upper()
                if lURLPath.contains(inURLItem["URL"].upper()):
                    URLItemDo(inURLItem, self, gSettingsDict)
                    return True
            # check Match type variant: Equal
            elif inURLItem["MatchType"].upper() == "EQUAL":
                if inURLItem["URL"].upper() == urllib.parse.unquote(self.path).upper():
                    URLItemDo(inURLItem, self, gSettingsDict)
                    return True
            # check Match type variant: EqualNoParam
            elif inURLItem["MatchType"].upper() == "EQUALNOPARAM":
                if inURLItem["URL"].upper() == urllib.parse.unquote(self.path).upper().split("?")[0]:
                    URLItemDo(inURLItem, self, gSettingsDict)
                    return True
            # check Match type variant: EqualCase
            elif inURLItem["MatchType"].upper() == "EQUALCASE":
                if inURLItem["URL"] == urllib.parse.unquote(self.path):
                    URLItemDo(inURLItem, self, gSettingsDict)
                    return True
        return False
    #ResponseContentTypeFile
    def SendResponseContentTypeFile(self, inContentType, inFilePath):
        # Send response status code
        self.send_response(200)
        # Send headers
        self.send_header('Content-type', inContentType)
        #Check if var exist
        if hasattr(self, "OpenRPASetCookie"):
            self.send_header("Set-Cookie", f"AuthToken={self.OpenRPA['AuthToken']}")
        self.end_headers()
        lFileObject = open(inFilePath, "rb") 
        # Write content as utf-8 data
        self.wfile.write(lFileObject.read())
        #Закрыть файловый объект
        lFileObject.close()
    # ResponseContentTypeFile
    def ResponseDictSend(self):
        lL = gSettingsDict["Logger"]
        inResponseDict = self.OpenRPAResponseDict
        # Send response status code
        self.send_response(inResponseDict["StatusCode"])
        # Send headers
        for lItemKey, lItemValue in inResponseDict["Headers"].items():
            self.send_header(lItemKey, lItemValue)
        # Send headers: Set-Cookie
        for lItemKey, lItemValue in inResponseDict["SetCookies"].items():
            self.send_header("Set-Cookie", f"{lItemKey}={lItemValue}")
        #Close headers section in response
        try:
            self.end_headers()
            # Write content as utf-8 data
            self.wfile.write(inResponseDict["Body"])
        except (ConnectionResetError, ConnectionAbortedError) as e:
            if lL: lL.warning(f"SERVER: Connection was forcibly closed by the client side - OK for the network interactions (ConnectionResetError: [WinError 10054] or ConnectionAbortedError: [WinError 10053])")

    def do_GET(self):
        try:
            threading.current_thread().request = self
            self.OpenRPA = {}
            self.OpenRPA["AuthToken"] = None
            self.OpenRPA["Domain"] = None
            self.OpenRPA["User"] = None
            self.OpenRPA["DefUserRoleAccessAsk"]=self.UserRoleAccessAsk # Alias for def
            self.OpenRPA["DefUserRoleHierarchyGet"]=self.UserRoleHierarchyGet # Alias for def
            # Prepare result dict
            lResponseDict = {"Headers": {}, "SetCookies": {}, "Body": b"", "StatusCode": None}
            self.OpenRPAResponseDict = lResponseDict
            ############################
            #First - all with Flag UACBool
            ############################
            for lURLItem in gSettingsDict["ServerDict"]["URLList"]:
                #Check if all condition are applied
                lFlagURLIsApplied=False
                lFlagURLIsApplied=self.URLItemCheckDo(inURLItem=lURLItem, inMethod="GET", inOnlyFlagUACBool=True)
                if lFlagURLIsApplied:
                    self.ResponseDictSend()
                    return
            #####################################
            #Do authentication
            #Check if authentication is turned on
            #####################################
            lFlagAccessUserBlock=False
            lAuthenticateDict = {"Domain": "", "User": ""}
            if gSettingsDict.get("ServerDict", {}).get("AccessUsers", {}).get("FlagCredentialsAsk", False):
                lAuthenticateDict = AuthenticateVerify(self)
                if not lAuthenticateDict["User"]:
                    lFlagAccessUserBlock=True
            # Logging
            # gSettingsDict["Logger"].info(f"HTTP request /. Domain: {lAuthenticateDict['Domain']}, User: {lAuthenticateDict['User']}")
            if lFlagAccessUserBlock:
                AuthenticateBlock(self)
            #####################################
            else:
                #Check the user access (if flag)
                ####################################
                lFlagUserAccess = True
                #If need user authentication
                if gSettingsDict.get("ServerDict", {}).get("AccessUsers", {}).get("FlagCredentialsAsk", False):
                    lFlagUserAccess = UserAccessCheckBefore("GET", self)
                ######################################
                if lFlagUserAccess:
                    lOrchestratorFolder = "\\".join(__file__.split("\\")[:-1])
                    ############################
                    #New server engine (url from global dict (URLList))
                    ############################
                    for lURLItem in gSettingsDict["ServerDict"]["URLList"]:
                        #Check if all condition are applied
                        lFlagURLIsApplied=False
                        lFlagURLIsApplied=self.URLItemCheckDo(lURLItem, "GET")
                        if lFlagURLIsApplied:
                            self.ResponseDictSend()
                            return
                    #Monitor
                    if self.path == '/Monitor/JSONDaemonListGet':
                        # Send response status code
                        self.send_response(200)
                        # Send headers
                        self.send_header('Content-type','application/json')
                        self.end_headers()
                        # Send message back to client
                        message = json.dumps(gSettingsDict)
                        # Write content as utf-8 data
                        self.wfile.write(bytes(message, "utf8"))
                    #Filemanager function
                    if self.path.lower().startswith('/filemanager/'):
                        lFileURL=self.path[13:]
                        # check if file in FileURL - File Path Mapping Dict
                        if lFileURL.lower() in gSettingsDict["FileManager"]["FileURLFilePathDict"]:
                            self.SendResponseContentTypeFile('application/octet-stream', gSettingsDict["FileManager"]["FileURLFilePathDict"][lFileURL])

                    # Index page
                    elif self.path == gSettingsDict["ServerDict"]["URLIndexStr"]:
                        lURLItemDict = {
                            "Method":"GET", 
                            "URL": gSettingsDict["ServerDict"]["URLIndexStr"], 
                            "MatchType": "EqualCase", 
                            "ResponseFilePath": os.path.join(lOrchestratorFolder, "Web\\Index.xhtml"), 
                            "ResponseContentType": "text/html"}
                        #Check if all condition are applied
                        lFlagURLIsApplied=False
                        lFlagURLIsApplied=self.URLItemCheckDo(lURLItemDict, "GET")
                        if lFlagURLIsApplied:
                            self.ResponseDictSend()
                            return
                else:
                    #Set access denied code
                    # Send response status code
                    self.send_response(403)
                    # Send headers
                    self.end_headers()
        except Exception as e:
            lL = gSettingsDict["Logger"]
            if lL: lL.exception(f"Server.do_GET: Global error handler - look traceback below.")
    # POST
    def do_POST(self):
        try:
            threading.current_thread().request = self
            lL = gSettingsDict["Logger"]
            self.OpenRPA = {}
            self.OpenRPA["AuthToken"] = None
            self.OpenRPA["Domain"] = None
            self.OpenRPA["User"] = None
            self.OpenRPA["DefUserRoleAccessAsk"]=self.UserRoleAccessAsk # Alias for def
            self.OpenRPA["DefUserRoleHierarchyGet"]=self.UserRoleHierarchyGet # Alias for def
            # Prepare result dict
            #pdb.set_trace()
            lResponseDict = {"Headers": {}, "SetCookies":{}, "Body": b"", "StatusCode": None}
            self.OpenRPAResponseDict = lResponseDict
            ############################
            #First - all with Flag UACBool
            ############################
            for lURLItem in gSettingsDict["ServerDict"]["URLList"]:
                #Check if all condition are applied
                lFlagURLIsApplied=False
                lFlagURLIsApplied=self.URLItemCheckDo(inURLItem=lURLItem, inMethod="POST", inOnlyFlagUACBool=True)
                if lFlagURLIsApplied:
                    self.ResponseDictSend()
                    return
            #####################################
            #Do authentication
            #Check if authentication is turned on
            #####################################
            lFlagAccessUserBlock=False
            lAuthenticateDict = {"Domain": "", "User": ""}
            lIsSuperToken = False # Is supertoken
            if gSettingsDict.get("ServerDict", {}).get("AccessUsers", {}).get("FlagCredentialsAsk", False):
                lAuthenticateDict = AuthenticateVerify(self)
                # Get Flag is supertoken (True|False)
                lIsSuperToken = gSettingsDict.get("ServerDict", {}).get("AccessUsers", {}).get("AuthTokensDict", {}).get(self.OpenRPA["AuthToken"], {}).get("FlagDoNotExpire", False)
                if not lAuthenticateDict["User"]:
                    lFlagAccessUserBlock=True
            if lFlagAccessUserBlock:
                AuthenticateBlock(self)
            #####################################
            else:
                #Check the user access (if flag)
                ####################################
                lFlagUserAccess = True
                #If need user authentication
                if gSettingsDict.get("ServerDict", {}).get("AccessUsers", {}).get("FlagCredentialsAsk", False):
                    lFlagUserAccess = UserAccessCheckBefore("POST", self)
                ######################################
                if lFlagUserAccess:
                    lOrchestratorFolder = "\\".join(__file__.split("\\")[:-1])
                    ############################
                    #New server engine (url from global dict (URLList))
                    ############################
                    for lURLItem in gSettingsDict["ServerDict"]["URLList"]:
                        #Check if all condition are applied
                        lFlagURLIsApplied=False
                        lFlagURLIsApplied=self.URLItemCheckDo(lURLItem, "POST")
                        if lFlagURLIsApplied:
                            self.ResponseDictSend()
                            return
                    #Централизованная функция получения запросов/отправки
                    if self.path == '/Utils/Processor':
                        #ReadRequest
                        lInputObject={}
                        if self.headers.get('Content-Length') is not None:
                            lInputByteArrayLength = int(self.headers.get('Content-Length'))
                            lInputByteArray=self.rfile.read(lInputByteArrayLength)
                            #Превращение массива байт в объект
                            lInputObject=json.loads(lInputByteArray.decode('utf8'))
                        # Send response status code
                        self.send_response(200)
                        # Send headers
                        self.send_header('Content-type','application/json')
                        self.end_headers()
                        # Logging info about processor activity if not SuperToken ()
                        if not lIsSuperToken:
                            lActivityTypeListStr = ""
                            try:
                                if type(lInputObject) is list:
                                    for lActivityItem in lInputObject:
                                        lActivityTypeListStr+=f"{lActivityItem['Type']}; "
                                else:
                                    lActivityTypeListStr += f"{lInputObject['Type']}"
                            except Exception as e:
                                lActivityTypeListStr = "Has some error with Activity Type read"
                            if lL: lL.info(f"Server:: !ATTENTION! /Utils/Processor will be deprecated in future. Use /pyOpenRPA/Processor or /pyOpenRPA/ActivityListExecute. User activity from web. Domain: {self.OpenRPA['Domain']}, Username: {self.OpenRPA['User']}, ActivityType: {lActivityTypeListStr}")
                        # Send message back to client
                        message = json.dumps(ProcessorOld.ActivityListOrDict(lInputObject))
                        # Write content as utf-8 data
                        self.wfile.write(bytes(message, "utf8"))
                    return
                else:
                    #Set access denied code
                    # Send response status code
                    self.send_response(403)
                    # Send headers
                    self.end_headers()
                    return
        except Exception as e:
            lL = gSettingsDict["Logger"]
            if lL: lL.exception(f"Server.do_POST: Global error handler - look traceback below.")
    #Logging
    #!Turn it on to stop print in console
    #def log_message(self, format, *args):
    #    return
class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    daemon_threads = True
    """Handle requests in a separate thread."""
    def finish_request(self, request, client_address):
        request.settimeout(gSettingsDict["ServerDict"]["RequestTimeoutSecFloat"])
        # "super" can not be used because BaseServer is not created from object
        HTTPServer.finish_request(self, request, client_address)
#inGlobalDict
# "JSONConfigurationDict":<JSON>
import ssl
class RobotDaemonServer(Thread):
    def __init__(self,name,inGlobalDict):
        Thread.__init__(self)
        self.name = name
        # Update the global dict
        ServerSettings.SettingsUpdate(inGlobalDict)
    def run(self):
        lL = gSettingsDict.get("Logger",None)
        try:
            lServerDict = gSettingsDict["ServerDict"]["ListenDict"][self.name]
            lAddressStr=lServerDict["AddressStr"]
            lPortInt=lServerDict["PortInt"]
            lCertFilePathStr = lServerDict["CertFilePEMPathStr"]
            lKeyFilePathStr = lServerDict["KeyFilePathStr"]
            if lCertFilePathStr == "": lCertFilePathStr = None
            if lKeyFilePathStr == "": lKeyFilePathStr = None
            # Server settings
            # Choose port 8080, for port 80, which is normally used for a http server, you need root access
            server_address = (lAddressStr, lPortInt)
            #httpd = HTTPServer(server_address, testHTTPServer_RequestHandler)
            #httpd.serve_forever()
            httpd = ThreadedHTTPServer(server_address, testHTTPServer_RequestHandler)
            if lCertFilePathStr is not None:
                if lKeyFilePathStr is not None:
                    httpd.socket = ssl.wrap_socket(httpd.socket, server_side=True, certfile=lCertFilePathStr, keyfile=lKeyFilePathStr)
                else:
                    httpd.socket = ssl.wrap_socket(httpd.socket, server_side=True, certfile=lCertFilePathStr)
                if lL: lL.info(f"Web Server init (with SSL). Name: {self.name}, Listen URL: {lAddressStr}, Listen port: {lPortInt}, Cert path: {lCertFilePathStr}")
            else:
                if lL: lL.info(f"Web Server init. Name: {self.name}, Listen URL: {lAddressStr}, Listen port: {lPortInt}")
            #print('Starting server, use <Ctrl-C> to stop')
            httpd.serve_forever()
        except Exception as e:
            if lL: lL.exception(f"Web Server execution exception")
