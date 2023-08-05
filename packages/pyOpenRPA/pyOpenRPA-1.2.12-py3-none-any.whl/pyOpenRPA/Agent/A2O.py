import requests, time
# A2O - Data flow Agent to Orchestrator

# f"{lProtocolStr}://{lHostStr}:{lPortInt}/pyOpenRPA/Agent/A2O"
# Request BODY:
# { "HostNameUpperStr": "", "UserUpperStr": "", "LogList":[]}
# Response BODY:
# {}

# Send logs to orchestrator
def _A2ODataSend(inGSettings, inDataDict):
    lL = inGSettings["Logger"]
    # Send request to the orchestrator server
    try:
        lProtocolStr= "https" if inGSettings["OrchestratorDict"]["IsHTTPSBool"] else "http"
        lHostStr = inGSettings["OrchestratorDict"]["HostStr"]
        lPortInt = inGSettings["OrchestratorDict"]["PortInt"]
        lURLStr=f"{lProtocolStr}://{lHostStr}:{lPortInt}/pyOpenRPA/Agent/A2O"
        lResponse = requests.post(url= lURLStr, cookies = {"AuthToken":inGSettings["OrchestratorDict"]["SuperTokenStr"]}, json=inDataDict, timeout=inGSettings["A2ODict"]["ConnectionTimeoutSecFloat"])
    except Exception as e:
        if lL: lL.exception(f"A2O Error handler.")


# Send some logs to orchestrator
def LogListSend(inGSettings, inLogList):
    lDataDict = { "HostNameUpperStr": inGSettings["AgentDict"]["HostNameUpperStr"], "UserUpperStr": inGSettings["AgentDict"]["UserUpperStr"], "LogList": inLogList}
    _A2ODataSend(inGSettings=inGSettings, inDataDict=lDataDict)

# Send some def result to the orchestrator by the Activity Item GUID str
def ActivityReturnDictSend(inGSettings, inActivityItemGUIDStr, inReturn):
    lDataDict = {"HostNameUpperStr": inGSettings["AgentDict"]["HostNameUpperStr"],
                 "UserUpperStr": inGSettings["AgentDict"]["UserUpperStr"], "ActivityReturnDict": {inActivityItemGUIDStr:inReturn}}
    _A2ODataSend(inGSettings=inGSettings, inDataDict=lDataDict)