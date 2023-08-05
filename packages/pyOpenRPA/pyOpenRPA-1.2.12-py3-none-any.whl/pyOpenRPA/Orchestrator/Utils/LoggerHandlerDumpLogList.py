from logging import StreamHandler

class LoggerHandlerDumpLogList(StreamHandler):
    def __init__(self, inDict, inKeyStr, inHashKeyStr, inRowCountInt):
        StreamHandler.__init__(self)
        self.Dict = inDict
        self.KeyStr = inKeyStr
        self.HashKeyStr = inHashKeyStr
        self.RowCountInt = inRowCountInt
        self.Dict[self.HashKeyStr]="0"
    def emit(self, inRecord):
        inMessageStr = self.format(inRecord)
        self.Dict[self.KeyStr].append(inMessageStr)
        self.Dict[self.HashKeyStr]=str(int(self.Dict[self.HashKeyStr])+1)
        if len(self.Dict[self.KeyStr])>self.RowCountInt:
            self.Dict[self.KeyStr].pop(0)