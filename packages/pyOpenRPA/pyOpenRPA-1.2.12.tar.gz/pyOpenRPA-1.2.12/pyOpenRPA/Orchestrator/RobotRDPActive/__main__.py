#Run example
#cd %~dp0..\..\Sources
#..\Resources\WPy64-3720\python-3.7.2.amd64\python.exe -m pyOpenRPA.Tools.RobotRDPActive "C:\Abs\Archive\scopeSrcUL\Settings.py"
#pause >nul
#Import parent folder to import current / other packages
#########################################################
import sys
import subprocess #start process async
import os #path, run, remove
import time #timer
import importlib
#lFolderPath = "\\".join(__file__.split("\\")[:-4])
lFolderPath = "/".join(__file__.split("/")[:-4])
sys.path.insert(0, lFolderPath)
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
#########################################################
from pyOpenRPA.Tools.RobotRDPActive import Connector
from pyOpenRPA.Tools.RobotRDPActive import Monitor
from pyOpenRPA.Tools.RobotRDPActive import Scheduler # Scheduler operations
#### Global error handler
try:
    #time.sleep()
    ######## Init the RDP List
    for lConfigurationItem in gSettingsDict["RDPList"]:
        lConfigurationItem["SessionIsWindowExistBool"]=False #Flag that session is not started
        lConfigurationItem["SessionIsWindowResponsibleBool"]=False #Flag that session is not started
        lConfigurationItem["SessionHex"]=" 77777sdfsdf77777dsfdfsf77777777" #Flag that session is not started
    ##########
    #Run monitor
    Scheduler.Scheduler(gSettingsDict["Scheduler"]) # Init & Run Scheduler
    Monitor.Monitor(gSettingsDict, 1)
except Exception as e:
    # Write in logger - warning
    gSettingsDict["Logger"].exception(f"!!! ATTENTION !!! Global error handler - look at code")
finally:
    #Close all thread from OrchestratorConnection
    gSettingsDict["OrchestratorConnectorTerminateAll"]()