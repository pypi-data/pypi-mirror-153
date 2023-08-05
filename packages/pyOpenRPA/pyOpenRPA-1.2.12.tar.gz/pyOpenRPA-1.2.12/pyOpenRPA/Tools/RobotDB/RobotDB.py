import subprocess
import json
import datetime
import time
import codecs
import os
import signal
import sys #Get input argument
import pdb
from . import Server
import logging
import copy
#from .Settings import Settings
import importlib
from importlib import util

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
#mGlobalDict = Settings.Settings(sys.argv[1])
Server.mGlobalDict = gSettingsDict

#Инициализация настроечных параметров
lDaemonActivityLogDict={} #Словарь отработанных активностей, ключ - кортеж (<activityType>, <datetime>, <processPath || processName>, <processArgs>)
lDaemonStartDateTime=datetime.datetime.now()

#Инициализация сервера
lThreadServer = Server.RobotDaemonServer("ServerThread", gSettingsDict)
lThreadServer.start()