import pdb
import json
import subprocess
import zlib
import os
from . import ProcessCommunicator
import importlib
import traceback
import logging
import sys
import datetime
import struct
import shutil
from pyOpenRPA.Robot import UIDesktop
global gSettingsDict
####################################
#Info: Main module of the Robot app (OpenRPA - Robot)
####################################

#Usage:
#Here you can run some activity or list of activities

#After import this module you can use the folowing functions:
#ActivityRun(inActivitySpecificationDict): outActivityResultDict - function - run activity (function or procedure)
#ActivityRunJSON(inActivitySpecificationDictJSON): outActivityResultDictJSON
#ActivityListRun(inActivitySpecificationDictList): outActivityResultDictList - function - run list of activities (function or procedure)
#ActivityListRunJSON(inActivitySpecificationDictListJSON): outActivityResultDictListJSON

#Naming:
#Activity - some action/list of actions
#Module - Any *.py file, which consist of area specific functions
#Argument

#inActivitySpecificationDict:
#{
#   ModuleName: <"GUI"|..., str>,
#   ActivityName: <Function or procedure name in module, str>,
#   ArgumentList: [<Argument 1, any type>, ...] - optional,
#   ArgumentDict: {<Argument 1 name, str>:<Argument 1 value, any type>, ...} - optional
#}

#outActivityResultDict:
#{
#   ActivitySpecificationDict: {
#       ModuleName: <"GUI"|..., str>,
#       ActivityName: <Function or procedure name in module, str>,
#       ArgumentList: [<Argument 1, any type>, ...] - optional,
#       ArgumentDict: {<Argument 1 name, str>: <Argument 1 value, any type>, ...} - optional
#   },
#   ErrorFlag: <Boolean flag - Activity result has error (true) or not (false), boolean>,
#   ErrorMessage: <Error message, str> - required if ErrorFlag is true,
#   ErrorTraceback: <Error traceback log, str> - required if ErrorFlag is true,
#   Result: <Result, returned from the Activity, int, str, boolean, list, dict> - required if ErrorFlag is false
#}

####################
#Section: Activity
####################
def ActivityRun(inActivitySpecificationDict):
    lResponseObject = {}
    #Выполнить отправку в модуль UIDesktop, если ModuleName == "UIDesktop"
    if inActivitySpecificationDict["ModuleName"] == "UIDesktop":
        if "ArgumentList" not in inActivitySpecificationDict:
            inActivitySpecificationDict["ArgumentList"]=[]
        if "ArgumentDict" not in inActivitySpecificationDict:
            inActivitySpecificationDict["ArgumentDict"]={}
        #Run the activity
        try:
            #Найти функцию
            lFunction=getattr(UIDesktop,inActivitySpecificationDict["ActivityName"])
            #Выполнить вызов и записать результат
            lResponseObject["Result"]=lFunction(*inActivitySpecificationDict["ArgumentList"],**inActivitySpecificationDict["ArgumentDict"])
        except Exception as e:
            #Установить флаг ошибки и передать тело ошибки
            lResponseObject["ErrorFlag"]=True
            lResponseObject["ErrorMessage"]=str(e)
            lResponseObject["ErrorTraceback"]=traceback.format_exc()
    #Остальные модули подключать и выполнять здесь
    else:
        lArgumentList=[]
        if "ArgumentList" in inActivitySpecificationDict:
            lArgumentList=inActivitySpecificationDict["ArgumentList"]
        lArgumentDict={}
        if "ArgumentDict" in inActivitySpecificationDict:
            lArgumentDict=inActivitySpecificationDict["ArgumentDict"]
        #Подготовить результирующую структуру
        lResponseObject={"ActivitySpecificationDict":inActivitySpecificationDict,"ErrorFlag":False}
        try:
            #Подключить модуль для вызова
            lModule=importlib.import_module(inActivitySpecificationDict["ModuleName"])
            #Найти функцию
            lFunction=getattr(lModule,inActivitySpecificationDict["ActivityName"])
            #Выполнить вызов и записать результат
            lResponseObject["Result"]=lFunction(*lArgumentList,**lArgumentDict)
        except Exception as e:
            #Установить флаг ошибки и передать тело ошибки
            lResponseObject["ErrorFlag"]=True
            lResponseObject["ErrorMessage"]=str(e)
            lResponseObject["ErrorTraceback"]=traceback.format_exc()
    return lResponseObject
#########################################################
#Run list of activities
#########################################################
def ActivityListRun(inActivitySpecificationDictList):
    lResult=[]
    for lItem in inActivitySpecificationDictList:
        lResult.append(ActivityRun(lItem))
    return lResult