import win32clipboard
####################################
#Info: Clipboard module of the Robot app (OpenRPA - Robot)
####################################
# GUI Module - interaction with Windows clipboard

################
###ClipboardGet
################
def ClipboardGet():
    win32clipboard.OpenClipboard()
    lResult = win32clipboard.GetClipboardData(win32clipboard.CF_UNICODETEXT)
    win32clipboard.CloseClipboard()
    return lResult
################
###ClipboardSet
################
def ClipboardSet(inText):
    win32clipboard.OpenClipboard()
    win32clipboard.EmptyClipboard()
    win32clipboard.SetClipboardData(win32clipboard.CF_UNICODETEXT,inText)
    win32clipboard.CloseClipboard()
