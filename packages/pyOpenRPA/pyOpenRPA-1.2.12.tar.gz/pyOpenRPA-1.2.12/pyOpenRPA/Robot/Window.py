import ctypes
####################################
#Info: Window module of the Robot app (OpenRPA - Robot)
####################################
# WIndow Module - Show information dialog messages to user by the modal windows

################
###DialogYesNo
################
#return 1 - Yes; 2 - No
def DialogYesNo(inTitle,inBody):
    lResult = ctypes.windll.user32.MessageBoxW(0, inBody, inTitle, 1)
    return lResult