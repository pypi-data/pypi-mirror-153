from http.server import BaseHTTPRequestHandler, HTTPServer
from socketserver import ThreadingMixIn
import threading
import json
from threading import Thread
import importlib
import pdb
import base64
import uuid
import datetime
import os #for path operations
from http import cookies
global gSettingsDict
from . import ServerSettings
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
    inRequest.OpenRPA = {}
    inRequest.OpenRPA["AuthToken"] = None
    #pdb.set_trace()
    if "AuthToken" in lCookies:
        lCookieAuthToken = lCookies.get("AuthToken", "").value
        if lCookieAuthToken:
            #Find AuthToken in GlobalDict
            if lCookieAuthToken in gSettingsDict.get("Server", {}).get("AccessUsers", {}).get("AuthTokensDict", {}):
                #Auth Token Has Been Founded
                lResult["Domain"] = gSettingsDict["Server"]["AccessUsers"]["AuthTokensDict"][lCookieAuthToken]["Domain"]
                lResult["User"] = gSettingsDict["Server"]["AccessUsers"]["AuthTokensDict"][lCookieAuthToken]["User"]
                #Set auth token
                inRequest.OpenRPA["AuthToken"] = lCookieAuthToken
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
        #Try to logon - use processor
        lLogonResult = Processor.Activity(
            {
                "Type": "WindowsLogon",
                "Domain": lDomain,
                "User": lUser,
                "Password": lPassword
            }
        )
        #Check result
        if lLogonResult["Result"]:
            lResult["Domain"] = lLogonResult["Domain"]
            lResult["User"] = lLogonResult["User"]
            #Create token
            lAuthToken=str(uuid.uuid1())
            gSettingsDict["Server"]["AccessUsers"]["AuthTokensDict"][lAuthToken] = {}
            gSettingsDict["Server"]["AccessUsers"]["AuthTokensDict"][lAuthToken]["Domain"] = lResult["Domain"]
            gSettingsDict["Server"]["AccessUsers"]["AuthTokensDict"][lAuthToken]["User"] = lResult["User"]
            gSettingsDict["Server"]["AccessUsers"]["AuthTokensDict"][lAuthToken]["FlagDoNotExpire"] = False
            gSettingsDict["Server"]["AccessUsers"]["AuthTokensDict"][lAuthToken]["TokenDatetime"] = datetime.datetime.now()
            #Set-cookie
            inRequest.OpenRPA["AuthToken"] = lAuthToken
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
        lUserDict = gSettingsDict["Server"]["AccessUsers"]["AuthTokensDict"][lAuthToken]
    #pdb.set_trace()
    ########################################
    ########################################
    #Check general before rule (without User domain)
    #Check rules
    for lAccessRuleItem in gSettingsDict.get("Server", {}).get("AccessUsers", {}).get("RuleMethodMatchURLBeforeList", []):
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
        for lAccessRuleItem in gSettingsDict.get("Server", {}).get("AccessUsers", {}).get("RuleDomainUserDict", {}).get((lUserDict["Domain"].upper(), lUserDict["User"].upper()), {}).get("MethodMatchURLBeforeList", []):
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
    #####################################
    #####################################
    #Return lResult
    return lResult
# HTTPRequestHandler class
class testHTTPServer_RequestHandler(BaseHTTPRequestHandler):
    #Tech def
    #return {"headers":[],"body":"","statuscode":111}
    def URLItemCheckDo(self, inURLItem, inMethod):
        ###############################
        #Tech sub def - do item
        ################################
        def URLItemDo(inURLItem,inRequest,inGlobalDict):
            inResponseDict = inRequest.OpenRPAResponseDict
            #Set status code 200
            inResponseDict["StatusCode"] = 200
            #Content-type
            if "ResponseContentType" in inURLItem:
                inResponseDict["Headers"]["Content-type"] = inURLItem["ResponseContentType"]
            #If file path is set
            if "ResponseFilePath" in inURLItem:
                lFileObject = open(inURLItem["ResponseFilePath"], "rb")
                # Write content as utf-8 data
                inResponseDict["Body"] = lFileObject.read()
                # Закрыть файловый объект
                lFileObject.close()
            #If function is set
            if "ResponseDefRequestGlobal" in inURLItem:
                inURLItem["ResponseDefRequestGlobal"](inRequest, inGlobalDict)
            if "ResponseFolderPath" in inURLItem:
                lRequestPath = inRequest.path
                lFilePathSecondPart = lRequestPath.replace(inURLItem["URL"],"")
                lFilePath = os.path.join(inURLItem["ResponseFolderPath"],lFilePathSecondPart)
                #print(f"File full path {lFilePath}")
                #Check if file exist
                if os.path.exists(lFilePath) and os.path.isfile(lFilePath):
                    lFileObject = open(lFilePath, "rb")
                    # Write content as utf-8 data
                    inResponseDict["Body"] = lFileObject.read()
                    inResponseDict["ContentType"]= "application/octet-stream"
                    # Закрыть файловый объект
                    lFileObject.close()
        ##############################################
        if inURLItem["Method"].upper() == inMethod.upper():
            # check Match type variant: BeginWith
            if inURLItem["MatchType"].upper() == "BEGINWITH":
                lURLPath = self.path
                lURLPath = lURLPath.upper()
                if lURLPath.startswith(inURLItem["URL"].upper()):
                    URLItemDo(inURLItem, self, gSettingsDict)
                    return True
            # check Match type variant: Contains
            elif inURLItem["MatchType"].upper() == "CONTAINS":
                lURLPath = self.path
                lURLPath = lURLPath.upper()
                if lURLPath.contains(inURLItem["URL"].upper()):
                    URLItemDo(inURLItem, self, gSettingsDict)
                    return True
            # check Match type variant: Equal
            elif inURLItem["MatchType"].upper() == "EQUAL":
                if inURLItem["URL"].upper() == self.path.upper():
                    URLItemDo(inURLItem, self, gSettingsDict)
                    return True
            # check Match type variant: EqualCase
            elif inURLItem["MatchType"].upper() == "EQUALCASE":
                if inURLItem["URL"] == self.path:
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
        self.end_headers()
        # Write content as utf-8 data
        self.wfile.write(inResponseDict["Body"])
    def do_GET(self):
        # Prepare result dict
        lResponseDict = {"Headers": {}, "SetCookies": {}, "Body": b"", "StatusCode": None}
        self.OpenRPAResponseDict = lResponseDict
        #####################################
        #Do authentication
        #Check if authentication is turned on
        #####################################
        lFlagAccessUserBlock=False
        lAuthenticateDict = {"Domain": "", "User": ""}
        if gSettingsDict.get("Server", {}).get("AccessUsers", {}).get("FlagCredentialsAsk", False):
            lAuthenticateDict = AuthenticateVerify(self)
            if not lAuthenticateDict["User"]:
                lFlagAccessUserBlock=True
        # Logging
        gSettingsDict["Logger"].info(f"HTTP request /. Domain: {lAuthenticateDict['Domain']}, User: {lAuthenticateDict['User']}")
        if lFlagAccessUserBlock:
            AuthenticateBlock(self)
        #####################################
        else:
            #Check the user access (if flag)
            ####################################
            lFlagUserAccess = True
            #If need user authentication
            if gSettingsDict.get("Server", {}).get("AccessUsers", {}).get("FlagCredentialsAsk", False):
                lFlagUserAccess = UserAccessCheckBefore("GET", self)
            ######################################
            if lFlagUserAccess:
                lOrchestratorFolder = "\\".join(__file__.split("\\")[:-1])
                ############################
                #New server engine (url from global dict (URLList))
                ############################
                for lURLItem in gSettingsDict["Server"]["URLList"]:
                    #Check if all condition are applied
                    lFlagURLIsApplied=False
                    lFlagURLIsApplied=self.URLItemCheckDo(lURLItem, "GET")
                    if lFlagURLIsApplied:
                        self.ResponseDictSend()
                        return
            else:
                #Set access denied code
                # Send response status code
                self.send_response(403)
                # Send headers
                self.end_headers()
    # POST
    def do_POST(self):
        # Prepare result dict
        #pdb.set_trace()
        lResponseDict = {"Headers": {}, "SetCookies":{}, "Body": b"", "StatusCode": None}
        self.OpenRPAResponseDict = lResponseDict
        #####################################
        #Do authentication
        #Check if authentication is turned on
        #####################################
        lFlagAccessUserBlock=False
        lAuthenticateDict = {"Domain": "", "User": ""}
        if gSettingsDict.get("Server", {}).get("AccessUsers", {}).get("FlagCredentialsAsk", False):
            lAuthenticateDict = AuthenticateVerify(self)
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
            if gSettingsDict.get("Server", {}).get("AccessUsers", {}).get("FlagCredentialsAsk", False):
                lFlagUserAccess = UserAccessCheckBefore("POST", self)
            ######################################
            if lFlagUserAccess:
                lOrchestratorFolder = "\\".join(__file__.split("\\")[:-1])
                ############################
                #New server engine (url from global dict (URLList))
                ############################
                for lURLItem in gSettingsDict["Server"]["URLList"]:
                    #Check if all condition are applied
                    lFlagURLIsApplied=False
                    lFlagURLIsApplied=self.URLItemCheckDo(lURLItem, "POST")
                    if lFlagURLIsApplied:
                        self.ResponseDictSend()
                        return
                return
            else:
                #Set access denied code
                # Send response status code
                self.send_response(403)
                # Send headers
                self.end_headers()
                return
    #Logging
    #!Turn it on to stop print in console
    #def log_message(self, format, *args):
    #    return
class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    daemon_threads = True
    """Handle requests in a separate thread."""
    def finish_request(self, request, client_address):
        request.settimeout(30)
        # "super" can not be used because BaseServer is not created from object
        HTTPServer.finish_request(self, request, client_address)
#inGlobalDict
# "JSONConfigurationDict":<JSON>
class RobotDaemonServer(Thread):
    def __init__(self,name,inGlobalDict):
        Thread.__init__(self)
        self.name = name
        # Update the global dict
        ServerSettings.SettingsUpdate(gSettingsDict)
    def run(self):
        inServerAddress="";
        inPort = gSettingsDict["Server"]["ListenPort"];
        # Server settings
        # Choose port 8080, for port 80, which is normally used for a http server, you need root access
        server_address = (inServerAddress, inPort)
        #httpd = HTTPServer(server_address, testHTTPServer_RequestHandler)
        # Logging
        gSettingsDict["Logger"].info(f"Server init. Listen URL: {inServerAddress}, Listen port: {inPort}")
        #httpd.serve_forever()
        httpd = ThreadedHTTPServer(server_address, testHTTPServer_RequestHandler)
        #print('Starting server, use <Ctrl-C> to stop')
        httpd.serve_forever()
