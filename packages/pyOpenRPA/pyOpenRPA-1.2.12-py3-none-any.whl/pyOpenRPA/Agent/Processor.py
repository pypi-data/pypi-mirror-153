# 1.2.0 - general processor - contains old orchestrator processor + RDPActive processor
import time, copy, threading
from . import A2O
# Run processor synchronious
def ProcessorRunSync(inGSettings):
    """
        "ProcessorDict": { # Has been changed. New general processor (one threaded) v.1.2.0
            "ActivityList": [ # List of the activities
                # {
                #    "Def":"DefAliasTest", # def link or def alias (look gSettings["Processor"]["AliasDefDict"])
                #    "ArgList":[1,2,3], # Args list
                #    "ArgDict":{"ttt":1,"222":2,"dsd":3}, # Args dictionary
                #    "ArgGSettings": None # Name of GSettings attribute: str (ArgDict) or index (for ArgList)
                #    "ArgLogger": None, # Name of GSettings attribute: str (ArgDict) or index (for ArgList)
                #    "GUIDStr": "sadasd-asdas-d-asdasd", # ActivityItem GUID which identify the Activity
                #    "ThreadBool": False
                # },
            ],
            "AliasDefDict": {}, # Storage for def with Str alias. To use it see pyOpenRPA.Orchestrator.ControlPanel
            "CheckIntervalSecFloat": 1.0 # Interval for check gSettings in ProcessorDict > ActivityList
            "ExecuteBool": True # Flag to execute thread processor
    """
    lL = inGSettings["Logger"]  # Logger alias
    inGSettings["ProcessorDict"]["ThreadIdInt"] = threading.get_ident() # fill Processor thread id
    while inGSettings["ProcessorDict"]["ExecuteBool"]:
        lActivityList = inGSettings["ProcessorDict"]["ActivityList"]  # Alias
        if len(lActivityList)>0:
            if lL: lL.debug(f'Processor ActivityList len: {len(lActivityList)}')
            lActivityItem = inGSettings["ProcessorDict"]["ActivityList"].pop(0) # Extract the first item from processor queue
            lResultList = ActivityListExecute(inGSettings = inGSettings, inActivityList = [lActivityItem]) # execute the activity item
            #Some help code
            if len(lResultList) == 0: lResultList= [None]
            # Send result to Orc if we have GUIDStr
            if "GUIDStr" in lActivityItem:
                # Def to send to Orc
                A2O.ActivityReturnDictSend(inGSettings=inGSettings, inActivityItemGUIDStr=lActivityItem["GUIDStr"],inReturn=lResultList[0])
        else:
            time.sleep(inGSettings["ProcessorDict"]["CheckIntervalSecFloat"]) # Sleep when list is empty

# Run processor Async
def ProcessorRunAsync(inGSettings, inActivityList):
    """
        "inActivityList": [ # List of the activities
            # {
            #    "Def":"DefAliasTest", # def link or def alias (look gSettings["Processor"]["AliasDefDict"])
            #    "ArgList":[1,2,3], # Args list
            #    "ArgDict":{"ttt":1,"222":2,"dsd":3}, # Args dictionary
            #    "ArgGSettings": None # Name of GSettings attribute: str (ArgDict) or index (for ArgList)
            #    "ArgLogger": None, # Name of GSettings attribute: str (ArgDict) or index (for ArgList)
            #    "GUIDStr": "sadasd-asdas-d-asdasd", # ActivityItem GUID which identify the Activity
            #    "ThreadBool": True
            # },
    """
    def __process__(inGSettings, inActivityList):
        for lActivityItem in inActivityList:
            lL = inGSettings["Logger"]  # Logger alias
            if lL: lL.debug(f'ActivityItem in new thread')
            lResultList = ActivityListExecute(inGSettings = inGSettings, inActivityList = [lActivityItem]) # execute the activity item
            #Some help code
            if len(lResultList) == 0: lResultList= [None]
            # Send result to Orc if we have GUIDStr
            if "GUIDStr" in lActivityItem:
                # Def to send to Orc
                A2O.ActivityReturnDictSend(inGSettings=inGSettings, inActivityItemGUIDStr=lActivityItem["GUIDStr"],inReturn=lResultList[0])
    # Start in new thread
    lThread = threading.Thread(target=__process__,kwargs={"inGSettings": inGSettings, "inActivityList": inActivityList})
    lThread.start()

# Execute ActivityItem list
# return the def result
def ActivityListExecute(inGSettings, inActivityList):
    lL = inGSettings["Logger"]  # Logger alias
    lResultList = [] # init the result list
    for lActivityItem in inActivityList:  # Iterate throught the activity list
        lDef = None  # Def variable
        if callable(lActivityItem["Def"]):  # CHeck if def is callable
            lDef = lActivityItem["Def"]  # Get the def
        else:  # Is not callable - check alias
            lDef = inGSettings["ProcessorDict"]["AliasDefDict"].get(lActivityItem["Def"], None)  # get def if def key in Alias def storage
        #gSettings
        lGSettingsDictKey = lActivityItem.pop("ArgGSettings",None)
        # # Prepare arg dict - gSettings
        if type(lGSettingsDictKey) is str: # check if gSetting key is in ArgDict
            lActivityItem["ArgDict"][lGSettingsDictKey] = inGSettings # Set the gSettings in dict
        # # Prepare arg list
        elif type(lGSettingsDictKey) is int: # check if gSetting key is in ArgDict
            lActivityItem["ArgList"].insert(lGSettingsDictKey,inGSettings)# Set the gSettings in list by the index
        #Logger
        lLoggerDictKey = lActivityItem.pop("ArgLogger",None)
        # # Prepare arg dict - gSettings
        if type(lLoggerDictKey) is str: # check if gSetting key is in ArgDict
            lActivityItem["ArgDict"][lLoggerDictKey] = lL # Set the lLogger in dict
        # # Prepare arg list
        elif type(lLoggerDictKey) is int: # check if gSetting key is in ArgDict
            lActivityItem["ArgList"].insert(lLoggerDictKey,lL)# Set the lLogger in list by the index

        try:  # try to run function from Processor.py
            lActivityItemResult = lDef(*lActivityItem["ArgList"], **lActivityItem["ArgDict"])
            lResultList.append(lActivityItemResult) # return the result
        except Exception as e:
            if lL: lL.exception(f"Processor.ActivityListExecute: Exception in def execution - activity will be ignored. Activity item: {lActivityItem}")  # Logging
            lResultList.append(None) # return the generated exception
    return lResultList # return the result list