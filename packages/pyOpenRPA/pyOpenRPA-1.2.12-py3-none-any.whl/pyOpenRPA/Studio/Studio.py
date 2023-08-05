from http.server import BaseHTTPRequestHandler, HTTPServer
import pdb
import pywinauto
import json
import subprocess
import zlib
import os
import sys
import traceback
from . import RobotConnector
from . import JSONNormalize
from ..Tools import Usage
import importlib
#Единый глобальный словарь (За основу взять из Settings.py)
global gSettingsDict
#Call Settings function from argv[1] file
################################################
lSubmoduleFunctionName = "Settings"
lFileFullPath = sys.argv[1]
lModuleName = (lFileFullPath.split("\\")[-1])[0:-3]
lTechSpecification = importlib.util.spec_from_file_location(lModuleName, lFileFullPath)
lTechModuleFromSpec = importlib.util.module_from_spec(lTechSpecification)
lTechSpecificationModuleLoader = lTechSpecification.loader.exec_module(lTechModuleFromSpec)
gSettingsDict = None
if lSubmoduleFunctionName in dir(lTechModuleFromSpec):
    # Run SettingUpdate function in submodule
    gSettingsDict = getattr(lTechModuleFromSpec, lSubmoduleFunctionName)()
#################################################
RobotConnector.mGlobalDict = gSettingsDict
#Init the robot
RobotConnector.UIDesktop.Utils.ProcessBitness.SettingsInit(gSettingsDict["ProcessBitness"])

# HTTP Studio web server class
class testHTTPServer_RequestHandler(BaseHTTPRequestHandler):
    #ResponseContentTypeFile
    def SendResponseContentTypeFile(self,inContentType,inFilePath):
        # Send response status code
        self.send_response(200)
        # Send headers
        self.send_header('Content-type',inContentType)
        self.end_headers()
        lFileObject = open(inFilePath, "rb") 
        # Write content as utf-8 data
        self.wfile.write(lFileObject.read())
        #Закрыть файловый объект
        lFileObject.close()        
    # GET
    def do_GET(self):
        lStudioFolder = "\\".join(__file__.split("\\")[:-1])
        #Мост между файлом и http запросом (новый формат)
        if self.path == "/":
            self.SendResponseContentTypeFile('text/html', os.path.join(lStudioFolder, "Web\\Index.xhtml"))
        #Мост между файлом и http запросом (новый формат)
        if self.path == '/3rdParty/Semantic-UI-CSS-master/semantic.min.css':
            self.SendResponseContentTypeFile('text/css', os.path.join(lStudioFolder, "..\\Resources\\Web\\Semantic-UI-CSS-master\\semantic.min.css"))
        #Мост между файлом и http запросом (новый формат)
        if self.path == '/3rdParty/Semantic-UI-CSS-master/semantic.min.js':
            self.SendResponseContentTypeFile('application/javascript', os.path.join(lStudioFolder, "..\\Resources\\Web\\Semantic-UI-CSS-master\\semantic.min.js"))
        #Мост между файлом и http запросом (новый формат)
        if self.path == '/3rdParty/jQuery/jquery-3.1.1.min.js':
            self.SendResponseContentTypeFile('application/javascript', os.path.join(lStudioFolder, "..\\Resources\\Web\\jQuery\\jquery-3.1.1.min.js"))
        #Мост между файлом и http запросом (новый формат)
        if self.path == '/3rdParty/Google/LatoItalic.css':
            self.SendResponseContentTypeFile('font/css', os.path.join(lStudioFolder, "..\\Resources\\Web\\Google\\LatoItalic.css"))
        #Мост между файлом и http запросом (новый формат)
        if self.path == '/3rdParty/Semantic-UI-CSS-master/themes/default/assets/fonts/icons.woff2':
            self.SendResponseContentTypeFile('font/woff2', os.path.join(lStudioFolder, "..\\Resources\\Web\\Semantic-UI-CSS-master\\themes\\default\\assets\\fonts\\icons.woff2"))
        #Мост между файлом и http запросом (новый формат)
        if self.path == '/favicon.ico':
            self.SendResponseContentTypeFile('image/x-icon', os.path.join(lStudioFolder, "Web\\favicon.ico"))
		#Мост между файлом и http запросом (новый формат)
        if self.path == '/pyOpenRPA_logo.png':
            self.SendResponseContentTypeFile('image/png', os.path.join(lStudioFolder, "..\\Resources\\Web\\pyOpenRPA_logo.png"))
    # POST
    def do_POST(self):
        #Restart studio
        if self.path == '/RestartStudio':
            #self.shutdown()
			# Send response status code
            self.send_response(200)
            # Send headers
            self.send_header('Content-type','application/json')
            self.end_headers()
            message = json.dumps({"Result":"Restart is in progress!"})
            # Write content as utf-8 data
            self.wfile.write(bytes(message, "utf8"))
            os.execl(sys.executable,os.path.abspath(__file__),*sys.argv)
            sys.exit(0)
        if self.path == '/GUIAction':
            #Обернуть в try, чтобы вернуть ответ, что сообщение не может быть обработано
            #   pdb.set_trace()
            # Send response status code
            self.send_response(200)
            # Send headers
            self.send_header('Content-type','application/json')
            self.end_headers()
            try:
                #ReadRequest
                lInputByteArrayLength = int(self.headers.get('Content-Length'))
                lInputByteArray=self.rfile.read(lInputByteArrayLength)
                #Превращение массива байт в объект
                lInputObject=json.loads(lInputByteArray.decode('utf8'))
                # Send message back to client
                #{'functionName':'', 'argsArray':[]}
                #pdb.set_trace()
                lRequestObject=lInputObject
                #Отправить команду роботу
                lResponseObject=RobotConnector.ActivityRun(lRequestObject)
                #Normalize JSON before send in response
                lResponseObject=JSONNormalize.JSONNormalizeDictList(lResponseObject)
                #Dump DICT LIST in JSON
                message = json.dumps(lResponseObject)
            except Exception as e:
                #Установить флаг ошибки
                lProcessResponse={"Result":None}
                lProcessResponse["ErrorFlag"]=True
                #Зафиксировать traceback
                lProcessResponse["ErrorTraceback"]=traceback.format_exc()
                #Зафиксировать Error message
                lProcessResponse["ErrorMessage"]=str(e)
                #lProcessResponse["ErrorArgs"]=str(e.args)
                message = json.dumps(lProcessResponse)     
            finally:
                # Write content as utf-8 data
                self.wfile.write(bytes(message, "utf8"))
        if self.path == '/GUIActionList':
            #ReadRequest
            lInputByteArrayLength = int(self.headers.get('Content-Length'))
            lInputByteArray=self.rfile.read(lInputByteArrayLength)
            #Превращение массива байт в объект
            lInputObject=json.loads(lInputByteArray.decode('utf8'))
            # Send response status code
            self.send_response(200)
            # Send headers
            self.send_header('Content-type','application/json')
            self.end_headers()
            # Send message back to client
            #{'functionName':'', 'argsArray':[]}
            lRequestObject=lInputObject
            lOutputObject=[]
            #pdb.set_trace()
            lResponseObject=RobotConnector.ActivityListRun(lRequestObject)
            #Сформировать текстовый ответ
            message = json.dumps(lResponseObject)
            # Write content as utf-8 data
            self.wfile.write(bytes(message, "utf8")) 
        return
    
def run():
    inServerAddress = "";
    inPort = gSettingsDict["Server"]["ListenPort"];
    # Server settings
    # Choose port 8080, for port 80, which is normally used for a http server, you need root access
    server_address = (inServerAddress, inPort)
    httpd = HTTPServer(server_address, testHTTPServer_RequestHandler)
    # Logging
    gSettingsDict["Logger"].info(f"Server init. Listen URL: {inServerAddress}, Listen port: {inPort}")
    # Запуск адреса в браузере
    os.system(f"explorer http://127.0.0.1:{str(inPort)}")
    Usage.Process(inComponentStr="Studio")
    httpd.serve_forever()
run()
