from threading import Timer
import datetime
class RepeatedTimer(object):
    def __init__(self, interval, inDateTimeEnd, function, *args, **kwargs):
        self._timer     = None
        self.interval   = interval
        self.function   = function
        self.args       = args
        self.kwargs     = kwargs
        self.is_running = False
        self.mDateTimeEnd = inDateTimeEnd # DateTime when stop
        self.start()
    def _run(self):
        self.is_running = False
        lResultGoLoop=True
        lCurrentDateTime=datetime.datetime.now()
        self.function(*self.args, **self.kwargs)
        if lCurrentDateTime>=self.mDateTimeEnd:
            lResultGoLoop=False    
        if lResultGoLoop is not None:
            if lResultGoLoop:
                self.start()
    def start(self):
        if not self.is_running:
            self._timer = Timer(self.interval, self._run)
            self._timer.start()
            self.is_running = True

    def stop(self):
        self._timer.cancel()
        self.is_running = False