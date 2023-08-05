from . import Timer # Async thread
import threading # Create in another thread
import datetime # Datetime class
import time # time functions
import importlib # import lib functions
# Scheduler class - init and work by the configuration
# OOP
class Scheduler:
    # Class properties
    mSchedulerDict = None
    mGSettings = None
    #########################
    # Init class
    def __init__(self,inSchedulerDict, inGSettings = None):
        self.Init(inSchedulerDict = inSchedulerDict, inGSettings = inGSettings)
    # Init the class instance
    def Init(self,inSchedulerDict, inGSettings):
        self.mGSettings = inGSettings
        self.mSchedulerDict = inSchedulerDict
        # Init the threads
        lTimerMainThread = threading.Thread(target = self.TimerMainThreadRun)
        lTimerMainThread.start() # Start the Timer main thread
        #print (f"Class instance configuration: {self.mSchedulerDict}, Init has been completed")
    ########################
    # Main timer thread - run when init class instance
    def TimerMainThreadRun(self):
        lDaemonStartDateTime=datetime.datetime.now()
        lDaemonLoopSeconds=self.mSchedulerDict["ActivityTimeCheckLoopSeconds"]
        lDaemonActivityLogDict={} #Словарь отработанных активностей, ключ - кортеж (<activityType>, <datetime>, <processPath || processName>, <processArgs>)
        #Вечный цикл
        while True:
            lCurrentDateTime = datetime.datetime.now()
            #Циклический обход правил
            lFlagSearchActivityType=True
            for lIndex, lItem in enumerate(self.mSchedulerDict["ActivityTimeList"]):
                #Проверка дней недели, в рамках которых можно запускать активность
                lItemWeekdayList=lItem.get("WeekdayList", [0, 1, 2, 3, 4, 5, 6])
                if lCurrentDateTime.weekday() in lItemWeekdayList:
                    if lFlagSearchActivityType:
                        #######################################################################
                        #Branch 1 - if has TimeHH:MM
                        #######################################################################
                        if "TimeHH:MM" in lItem:
                            #Вид активности - запуск процесса
                            #Сформировать временной штамп, относительно которого надо будет проверять время
                            #часовой пояс пока не учитываем
                            lActivityDateTime=datetime.datetime.strptime(lItem["TimeHH:MM"],"%H:%M")
                            lActivityDateTime=lActivityDateTime.replace(year=lCurrentDateTime.year,month=lCurrentDateTime.month,day=lCurrentDateTime.day)
                            #Убедиться в том, что время наступило
                            if (
                                    lActivityDateTime>=lDaemonStartDateTime and
                                    lCurrentDateTime>=lActivityDateTime and
                                    (lIndex,lActivityDateTime) not in lDaemonActivityLogDict):
                                #Выполнить операцию
                                #Запись в массив отработанных активностей
                                lDaemonActivityLogDict[(lIndex,lActivityDateTime)]={"ActivityStartDateTime":lCurrentDateTime}
                                #Запустить процесс - new code
                                #################
                                #Call function from Activity structure
                                ################################################
                                lSubmoduleFunctionName = lItem["Activity"]["DefName"]
                                lFileFullPath = lItem["Activity"]["ModulePath"] # "path\\to\\module.py"
                                lModuleName = (lFileFullPath.split("\\")[-1])[0:-3]
                                lTechSpecification = importlib.util.spec_from_file_location(lModuleName, lFileFullPath)
                                lTechModuleFromSpec = importlib.util.module_from_spec(lTechSpecification)
                                lTechSpecificationModuleLoader = lTechSpecification.loader.exec_module(lTechModuleFromSpec)
                                # Set gSettings in module
                                lTechModuleFromSpec.gSettings = self.mGSettings
                                if lSubmoduleFunctionName in dir(lTechModuleFromSpec):
                                    # Run SettingUpdate function in submodule
                                    #mGlobalDict = getattr(lTechModuleFromSpec, lSubmoduleFunctionName)()
                                    getattr(lTechModuleFromSpec, lSubmoduleFunctionName)(*lItem["Activity"]["ArgList"],**lItem["Activity"]["ArgDict"])
                                #################################################
                        #######################################################################
                        #Branch 2 - if TimeHH:MMStart, TimeHH:MMStop, ActivityIntervalSeconds
                        #######################################################################
                        if "TimeHH:MMStart" in lItem and "TimeHH:MMStop" in lItem and "ActivityIntervalSeconds" in lItem:
                            #Сформировать временной штамп, относительно которого надо будет проверять время
                            #часовой пояс пока не учитываем
                            lActivityDateTime=datetime.datetime.strptime(lItem["TimeHH:MMStart"],"%H:%M")
                            lActivityDateTime=lActivityDateTime.replace(year=lCurrentDateTime.year,month=lCurrentDateTime.month,day=lCurrentDateTime.day)
                            lActivityTimeEndDateTime=datetime.datetime.strptime(lItem["TimeHH:MMStop"],"%H:%M")
                            lActivityTimeEndDateTime=lActivityTimeEndDateTime.replace(year=lCurrentDateTime.year,month=lCurrentDateTime.month,day=lCurrentDateTime.day)
                            #Убедиться в том, что время наступило
                            if (
                                    lCurrentDateTime<lActivityTimeEndDateTime and
                                    lCurrentDateTime>=lActivityDateTime and
                                    (lIndex,lActivityDateTime) not in lDaemonActivityLogDict):
                                #Запись в массив отработанных активностей
                                lDaemonActivityLogDict[(lIndex,lActivityDateTime)]={"ActivityStartDateTime":lCurrentDateTime}
                                #Call function from Activity structure
                                ################################################
                                lSubmoduleFunctionName = lItem["Activity"]["DefName"]
                                lFileFullPath = lItem["Activity"]["ModulePath"] # "path\\to\\module.py"
                                lModuleName = (lFileFullPath.split("\\")[-1])[0:-3]
                                lTechSpecification = importlib.util.spec_from_file_location(lModuleName, lFileFullPath)
                                lTechModuleFromSpec = importlib.util.module_from_spec(lTechSpecification)
                                lTechSpecificationModuleLoader = lTechSpecification.loader.exec_module(lTechModuleFromSpec)
                                # Set gSettings in module
                                lTechModuleFromSpec.gSettings = self.mGSettings
                                if lSubmoduleFunctionName in dir(lTechModuleFromSpec):
                                    # Run SettingUpdate function in submodule
                                    #mGlobalDict = getattr(lTechModuleFromSpec, lSubmoduleFunctionName)()
                                    lDef = getattr(lTechModuleFromSpec, lSubmoduleFunctionName) #(*lItem["Activity"]["ArgList"],**lItem["Activity"]["ArgDict"])
                                    #################################################
                                    #Запуск циклической процедуры
                                    #Timer.activityLoopStart(lItem["ActivityIntervalSeconds"], lActivityTimeEndDateTime, lItem["Activity"])
                                    lTimer = Timer.RepeatedTimer(lItem["ActivityIntervalSeconds"], lActivityTimeEndDateTime, lDef, *lItem["Activity"]["ArgList"], **lItem["Activity"]["ArgDict"]) # it auto-starts, no need of rt.start()
            #Уснуть до следующего прогона
            #print (f"Loop has been completed")
            time.sleep(lDaemonLoopSeconds)