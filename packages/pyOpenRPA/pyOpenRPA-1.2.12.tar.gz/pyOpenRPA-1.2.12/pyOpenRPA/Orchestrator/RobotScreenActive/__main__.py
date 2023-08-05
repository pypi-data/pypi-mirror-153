#Run example
#cd %~dp0..\..\Sources
#..\Resources\WPy64-3720\python-3.7.2.amd64\python.exe -m pyOpenRPA.Tools.RobotScreenActive
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
from pyOpenRPA.Tools.RobotScreenActive import Monitor
Monitor.CheckScreen()