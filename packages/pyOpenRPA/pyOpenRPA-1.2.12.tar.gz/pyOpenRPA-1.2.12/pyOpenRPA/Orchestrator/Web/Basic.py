import json, copy
from .. import __Orchestrator__
from .. import Processor
# Escape JS to the safe JS for the inline JS in HTML tags ATTENTION! Use it only if want to paste JS into HTML tag - not in <script>
# USAGE: JSEscapeForHTMLInline(inJSStr="lTest=\"Hello World\"; alert(\"lTest\")")
def JSEscapeForHTMLInline(inJSStr):
    lResult = inJSStr.replace("\"","&quot;")
    return lResult

def JSProcessorActivityListAdd(inActivityList, inGUIDRemoveBool = True):
    """
        # Create JS for send activity list/ activity to the processor
        # USAGE: Orchestrator.Web.Basic.JSProcessorActivityListAdd(inActivityList)

    :param inActivityList: List of the activities (See __Orchestrator__.ProcessorActivityItemCreate)
    :param inGUIDRemoveBool: True - remove GUID before generate JS (if GUID is not important)
    :return: JavaScript string for the front end
    """
    Processor.__ActivityListVerify__(inActivityList=inActivityList)  # DO VERIFICATION FOR THE inActivityList
    inActivityList = copy.deepcopy(inActivityList)
    # Check if no def function is here - if exist - replace to alias
    for lActivityItem in inActivityList:
        if "GUIDStr" in lActivityItem and inGUIDRemoveBool == True: del lActivityItem["GUIDStr"] # Remove GUID from activity items if exists
        lDef = lActivityItem["Def"]
        if callable(lDef): raise Exception(f"pyOpenRPA Exception: You can't send ActivityList with def to JS. Use Def Alias (see Orchestrator.ProcessorAliasDefUpdate)")
    lJSStr = f"""mGlobal.pyOpenRPA.ProcessorQueueAdd({json.dumps(inActivityList)});"""
    return lJSStr


def JSActivityListExecute(inActivityList, inGUIDRemoveBool = True):
    """
        Create JS for execute activity list/ activity permanent
        USAGE: Orchestrator.Web.Basic.JSActivityListExecute(inActivityList, inGUIDRemoveBool = True)

    :param inActivityList: List of the activities (See __Orchestrator__.ProcessorActivityItemCreate)
    :param inGUIDRemoveBool: True - remove GUID before generate JS (if GUID is not important)
    :return: JavaScript string for the front end
    """
    Processor.__ActivityListVerify__(inActivityList=inActivityList)  # DO VERIFICATION FOR THE inActivityList
    inActivityList = copy.deepcopy(inActivityList)
    # Check if no def function is here - if exist - replace to alias
    for lActivityItem in inActivityList:
        if "GUIDStr" in lActivityItem and inGUIDRemoveBool == True: del lActivityItem["GUIDStr"] # Remove GUID from activity items if exists
        lDef = lActivityItem["Def"]
        if callable(lDef): raise Exception(f"pyOpenRPA Exception: You can't send ActivityList with def to JS. Use Def Alias (see Orchestrator.ProcessorAliasDefUpdate)")
    lJSStr = f"""mGlobal.pyOpenRPA.ActivityListExecute({json.dumps(inActivityList)});"""
    return lJSStr

# Generate HTML code of the simple URL link by the URL
# USAGE: Orchestrator.Web.Basic.HTMLLinkURL(inURLStr="test",inColorStr="orange")
# USAGE: Basic.HTMLLinkURL(inURLStr="test",inColorStr="orange")
def HTMLLinkURL(inURLStr, inTitleStr=None, inColorStr=None):
    lCSSStyleStr = ""
    if not inTitleStr: inTitleStr = inURLStr
    if inColorStr: lCSSStyleStr=f"style=\"color:{inColorStr}\""
    lResult=f"<a {lCSSStyleStr} href=\"{inURLStr}\">{inTitleStr}</a>"
    return lResult

# Generate HTML code of the simple URL link by the JS when onclick
# USAGE: Orchestrator.Web.Basic.HTMLLinkJSOnClick(inJSOnClickStr="",inColorStr="orange")
# USAGE: Basic.HTMLLinkJSOnClick(inJSOnClickStr="test",inColorStr="orange")
def HTMLLinkJSOnClick(inJSOnClickStr, inTitleStr, inColorStr=None):
    lCSSStyleStr = ""
    if inColorStr: lCSSStyleStr=f"style=\"color:{inColorStr}\""
    inJSOnClickStr= JSEscapeForHTMLInline(inJSStr=inJSOnClickStr) # Escape some symbols for the inline JS
    lResult=f"<a {lCSSStyleStr} onclick=\"{inJSOnClickStr}\">{inTitleStr}</a>"
    return lResult

# Create HTMLLink by the def, argdict, arglist, gsettingsStr, logger Str titleStr, color, (add in processor queue)
def HTMLLinkDefProcessor(inGSettings, inDef, inArgDict=None, inArgList=None, inArgGSettingsStr=None, inArgLoggerStr=None, inLinkTitleStr=None, inLinkColorStr=""):
    lDefAliasStr = inDef
    if callable(inDef):
        lDefAliasStr = str(inDef)
        lDefAliasStr = __Orchestrator__.ProcessorAliasDefUpdate(inGSettings=inGSettings, inDef=inDef, inAliasStr=lDefAliasStr)
    if inLinkTitleStr is None: inLinkTitleStr = lDefAliasStr
    lActivityList = [__Orchestrator__.ProcessorActivityItemCreate(inDef=lDefAliasStr,inArgList=inArgList,inArgDict=inArgDict,inArgGSettingsStr=inArgGSettingsStr,inArgLoggerStr=inArgLoggerStr)]
    lJSStr = JSProcessorActivityListAdd(lActivityList)
    lHTMLStr = HTMLLinkJSOnClick(inJSOnClickStr=lJSStr,inTitleStr=inLinkTitleStr, inColorStr=inLinkColorStr)
    return lHTMLStr

# Create HTMLLink by the def, argdict, arglist, gsettingsStr, logger Str titleStr, color, (execute permanently)
def HTMLLinkDefExecute(inGSettings, inDef, inArgDict=None, inArgList=None, inArgGSettingsStr=None, inArgLoggerStr=None, inLinkTitleStr=None, inLinkColorStr=""):
    lDefAliasStr = inDef
    if callable(inDef):
        lDefAliasStr = str(inDef)
        lDefAliasStr = __Orchestrator__.ProcessorAliasDefUpdate(inGSettings=inGSettings, inDef=inDef, inAliasStr=lDefAliasStr)
    if inLinkTitleStr is None: inLinkTitleStr = lDefAliasStr
    lActivityList = [__Orchestrator__.ProcessorActivityItemCreate(inDef=lDefAliasStr,inArgList=inArgList,inArgDict=inArgDict,inArgGSettingsStr=inArgGSettingsStr,inArgLoggerStr=inArgLoggerStr)]
    lJSStr = JSActivityListExecute(lActivityList)
    lHTMLStr = HTMLLinkJSOnClick(inJSOnClickStr=lJSStr,inTitleStr=inLinkTitleStr, inColorStr=inLinkColorStr)
    return lHTMLStr

# HTML Generator for the CP up to v.1.2.0
def HTMLControlPanelBC(inCPDict):
    # FooterButtonX2List generation
    lFooterButtonX2Str = ""
    for lItem in inCPDict["FooterButtonX2List"]:
        lFooterButtonX2Str+=f'<div class="ui basic {lItem.get("Color","")} button" onclick="{JSEscapeForHTMLInline(lItem.get("OnClick",""))}">{lItem.get("Text","")}</div>'
    # FooterButtonX1List generation
    lFooterButtonX1Str = ""
    for lItem in inCPDict["FooterButtonX1List"]:
        lFooterButtonX1Str+=f'<div class="ui basic {lItem.get("Color","")} button" onclick="{JSEscapeForHTMLInline(lItem.get("OnClick",""))}">{lItem.get("Text","")}</div>'
    # BodyKeyValue generation
    lBodyKeyValueStr = ""
    for lItem in inCPDict["BodyKeyValueList"]:
        lBodyKeyValueStr+=f"<li>{lItem['Key']}: {lItem['Value']}</li>"
    # Generate consolidated string
    lResultHTMLStr = f"""
    <div class="card">
        <div class="content">
            <div class="right floated mini ui ">
                {inCPDict['HeaderRightText']}
            </div>
            <div class="header">
                {inCPDict['HeaderLeftText']}

            </div>
            <div class="meta">
                {inCPDict['SubheaderText']}
            </div>
            <div class="description">
                <ul style="padding-inline-start:16px;margin:0px">
                    {lBodyKeyValueStr}
                </ul>
            </div>
        </div>
        <div class="extra content">
            {inCPDict['FooterText']}
        </div>
        <div class="extra content">
            <div class="ui two buttons">
            {lFooterButtonX2Str}
            </div>
            <div class="ui horizontal divider">Add. controls</div>
            <div class="ui one buttons">
            {lFooterButtonX1Str}
            </div>
        </div>
    </div>
    """

    return lResultHTMLStr
