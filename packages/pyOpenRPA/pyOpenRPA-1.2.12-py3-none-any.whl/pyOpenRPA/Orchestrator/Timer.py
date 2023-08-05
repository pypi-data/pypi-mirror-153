from threading import Timer
import datetime
import subprocess
import importlib
import logging
from . import Processor

global gSettingsDict

class RepeatedTimer(object):
    def __init__(self, interval, function, *args, **kwargs):
        self._timer     = None
        self.interval   = interval
        self.function   = function
        self.args       = args
        self.kwargs     = kwargs
        self.is_running = False
        self.start()
    def _run(self):
        self.is_running = False
        lResult = self.function(*self.args, **self.kwargs)
        if lResult is not None:
            if lResult:
                self.start()
    def start(self):
        if not self.is_running:
            self._timer = Timer(self.interval, self._run)
            self._timer.start()
            self.is_running = True

    def stop(self):
        self._timer.cancel()
        self.is_running = False

############################################################
####Техническая функция обработки таймера - потока
############################################################
def activityLoopExecution(inLoopTimeEndDateTime, inActivity):
    lResultGoLoop=True
    lCurrentDateTime=datetime.datetime.now()
    #Запустить актитвость через процессор (orchestratorProcessor)
    Processor.ActivityListOrDict(inActivity)
    #Выключить таймер, если время наступило
    if lCurrentDateTime>=inLoopTimeEndDateTime:
        lResultGoLoop=False
    #Вернуть результат
    return lResultGoLoop
############################################################
####Функция запуска таймера - потока
############################################################
def activityLoopStart(inActivityLoopSeconds, inLoopTimeEndDateTime, inActivity):
    lTimer = RepeatedTimer(inActivityLoopSeconds, activityLoopExecution, inLoopTimeEndDateTime, inActivity) # it auto-starts, no need of rt.start()
    lTimer.start()
