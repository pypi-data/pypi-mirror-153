import logging
import datetime
#Robot settings
def Settings():
    import os
    mDict = {
        "Logger": logging.getLogger("Robot"),
        "Storage": {
            "Robot_R01_help": "Robot data storage in orchestrator env",
            "Robot_R01": {}
        },
        "ProcessBitness": {
            "Python32FullPath": None, #Set from user: "..\\Resources\\WPy32-3720\\python-3.7.2\\OpenRPARobotGUIx32.exe"
            "Python64FullPath": None, #Set from user
            "Python32ProcessName": "OpenRPAUIDesktopX32.exe", #Config set once
            "Python64ProcessName": "OpenRPAUIDesktopX64.exe" #Config set once
        }
    }
    #Создать файл логирования
    # add filemode="w" to overwrite
    if not os.path.exists("Reports"):
        os.makedirs("Reports")
    ##########################
    #Подготовка логгера Robot
    #########################
    mRobotLogger=mDict["Logger"]
    mRobotLogger.setLevel(logging.INFO)
    # create the logging file handler
    mRobotLoggerFH = logging.FileHandler("Reports\ReportRobot_"+datetime.datetime.now().strftime("%Y_%m_%d")+".log")
    mRobotLoggerFormatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    mRobotLoggerFH.setFormatter(mRobotLoggerFormatter)
    # add handler to logger object
    mRobotLogger.addHandler(mRobotLoggerFH)
    ############################################