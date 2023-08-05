import json
from . import ExcelCom
import os
import sqlite3
import win32com.client
import time
import pythoncom
#Insert in DB
def SQLInsert(inRequest,inGlobalDict):
    inResponseDict = inRequest.OpenRPAResponseDict
    # Create result JSON
    lResultJSON = {"Status": "OK", "ErrorMessage":"", "Result":[]}
    #Set status code 200
    inResponseDict["StatusCode"] = 200
    try:
        #Read the body
        #ReadRequest
        lInputJSON={}
        if inRequest.headers.get('Content-Length') is not None:
            lInputByteArrayLength = int(inRequest.headers.get('Content-Length'))
            lInputByteArray=inRequest.rfile.read(lInputByteArrayLength)
            #print(lInputByteArray.decode('utf8'))
            #Превращение массива байт в объект
            lInputJSON=json.loads(lInputByteArray.decode('utf8'))
        ########################################
        conn = sqlite3.connect(inGlobalDict["SQLite"]["DBPath"])
        c = conn.cursor()
        # Loop for rows
        for lRowItem in lInputJSON:
            lRowResult={"Status": "OK", "ErrorMessage":""}
            try:
                my_dict = lRowItem["RowDict"]
                # Insert a row of data
                columns = ', '.join(my_dict.keys())
                placeholders = ':'+', :'.join(my_dict.keys())
                query = f'INSERT INTO {lRowItem["TableName"]} (%s) VALUES (%s)' % (columns, placeholders)
                c.execute(query, my_dict)
            except Exception as e:
                lRowResult["Status"]="ERROR"
                lRowResult["ErrorMessage"]=str(e)
            finally:
                lResultJSON["Result"].append(lRowResult)
        # Save (commit) the changes
        conn.commit()
        # We can also close the connection if we are done with it.
        # Just be sure any changes have been committed or they will be lost.
        conn.close()
    except Exception as e:
        lResultJSON["Status"]="ERROR"
        lResultJSON["ErrorMessage"]=str(e)
    finally:
        ########################################
        # Send message back to client
        message = json.dumps(lResultJSON)
        print(message)
        # Write content as utf-8 data
        inResponseDict["Body"] = bytes(message, "utf8")
################################################
#Export SQLite to Excel
def SQLExportXLS(inRequest,inGlobalDict):
    #Step 1 - read SQLite
    conn = sqlite3.connect(inGlobalDict["SQLite"]["DBPath"])
    c = conn.cursor()
    # Loop for rows
#    for lRowItem in lInputJSON:
#        my_dict = lRowItem["RowDict"]
#        # Insert a row of data
#        columns = ', '.join(my_dict.keys())
#        placeholders = ':'+', :'.join(my_dict.keys())
    query = f'select * from Test'
    #create data array
    #row = range(0,10)
    i = 0
    data_array = []
    for row in c.execute(query):
        # use the cursor as an iterable
        data_array.append(row)
        i += 1
    # We can also close the connection if we are done with it.
    # Just be sure any changes have been committed or they will be lost.
    conn.close()
    #step 2 - insert in XLS
    pythoncom.CoInitialize()
    #write the array to an excel file
    #excel = win32com.client.Dispatch("Excel.Application")
    excel = win32com.client.gencache.EnsureDispatch('Excel.Application')
    excel.Visible = True
    excel.DisplayAlerts = False
    #excel.ScreenUpdating = False
    #book = excel.Workbooks.Add()
    #sheet = book.Worksheets(1)
    #Read input JSON
    lInputJSON={}
    if inRequest.headers.get('Content-Length') is not None:
        lInputByteArrayLength = int(inRequest.headers.get('Content-Length'))
        lInputByteArray=inRequest.rfile.read(lInputByteArrayLength)
        #print(lInputByteArray.decode('utf8'))
        #Превращение массива байт в объект
        lInputJSON=json.loads(lInputByteArray.decode('utf8'))
        #Config
        lOffsetRow = lInputJSON["OffsetRow"]
        lOffsetCol = lInputJSON["OffsetCol"]
        lXLSTemplatePath = lInputJSON["XLSTemplatePath"]
        lXLSSheetName = lInputJSON["XLSSheetName"]
        lXLSResultPath = lInputJSON["XLSResultPath"]
        lXLSResultFlagSendInResponse = lInputJSON["XLSResultFlagSendInResponse"]
        lXLSResultFlagDeleteAfterSend = lInputJSON["XLSResultFlagDeleteAfterSend"]
        try:
            #excel = win32com.client.gencache.EnsureDispatch('Excel.Application')
            book = ExcelCom.OpenWorkbook(excel, lXLSTemplatePath)
            sheet = book.Worksheets(lXLSSheetName) 
            excel.Visible = True
            #single loop, writing a row to a range
            #Logic
            start = time.time()
            row = 0
            for line in data_array:
                row += 1
                sheet.Range(sheet.Cells(row+lOffsetRow,1+lOffsetCol), sheet.Cells(row+lOffsetRow, len(line)+lOffsetCol)).Value = line
            if lXLSResultPath:
                book.SaveAs(Filename = lXLSResultPath)
            #excel.ScreenUpdating = True
        except Exception as e:
            print(e)
        finally:
            # RELEASES RESOURCES
            sheet = None
            book = None
            excel.DisplayAlerts = True
            excel.Quit()
            excel = None
            pythoncom.CoUninitialize()
        #####################
        #Step 3 - Send file content to client
        #####################
        if lXLSResultFlagSendInResponse and lXLSResultPath:
            lFileObject = open(lXLSResultPath, "rb")
            # Write content as utf-8 data
            inRequest.OpenRPAResponseDict["Body"] = lFileObject.read()
            # Закрыть файловый объект
            lFileObject.close()
        #####################
        #Step 4 - Delete after send
        #####################
        if lXLSResultFlagDeleteAfterSend and lXLSResultPath:
            if os.path.exists(lXLSResultPath):
                os.remove(lXLSResultPath)
def SettingsUpdate(inGlobalConfiguration):
    import os
    import pyOpenRPA.Orchestrator
    lOrchestratorFolder = "\\".join(pyOpenRPA.Orchestrator.__file__.split("\\")[:-1])
    lURLList = \
        [ #List of available URLs with the orchestrator server
            #{
            #    "Method":"GET|POST",
            #    "URL": "/index", #URL of the request
            #    "MatchType": "", #"BeginWith|Contains|Equal|EqualCase",
            #    "ResponseFilePath": "", #Absolute or relative path
            #    "ResponseFolderPath": "", #Absolute or relative path
            #    "ResponseContentType": "", #HTTP Content-type
            #    "ResponseDefRequestGlobal": None #Function with str result
            #}
            #Orchestrator basic dependencies
            {"Method":"POST", "URL": "/SQLInsert", "MatchType": "EqualCase", "ResponseDefRequestGlobal": SQLInsert, "ResponseContentType": "application/json"},
            {"Method":"POST", "URL": "/SQLExportXLS.xlsx", "MatchType": "EqualCase", "ResponseDefRequestGlobal": SQLExportXLS, "ResponseContentType": "application/octet-stream"}
        ]
    inGlobalConfiguration["Server"]["URLList"]=inGlobalConfiguration["Server"]["URLList"]+lURLList
    return inGlobalConfiguration