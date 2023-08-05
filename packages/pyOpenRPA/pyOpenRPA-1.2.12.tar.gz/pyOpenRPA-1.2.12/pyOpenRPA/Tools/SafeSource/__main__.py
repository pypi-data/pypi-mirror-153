#argv 0 = "RUN"/"CREATE"

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
from pyOpenRPA.Tools.SafeSource import DistrRun
from pyOpenRPA.Tools.SafeSource import DistrCreate
#Mode RUN
if sys.argv[1].upper() == "RUN":
    DistrRun.Run()
#Mode CREATE
if sys.argv[1].upper() == "CREATE":
    DistrCreate.Run()
    pass