import win32clipboard
import keyboard # keyboard functions
import time # Some operations need wait
import random # random number for test
gWaitTextInClipboardSec = 1 # Second for wait text will be set in clipboard (for get operations)
# set clipboard data
def TextSet(inTextStr):
    win32clipboard.OpenClipboard()
    win32clipboard.EmptyClipboard()
    win32clipboard.SetClipboardText(inTextStr)
    win32clipboard.CloseClipboard()
# get clipboard data
def TextGet(inWaitTextInClipboardSec = gWaitTextInClipboardSec):
    time.sleep(inWaitTextInClipboardSec) # Wait for clipboard will save
    win32clipboard.OpenClipboard()
    data = win32clipboard.GetClipboardData()
    win32clipboard.CloseClipboard()
    return data
# Test in has text cursor and ready to apply
def InputIsFocused():
    keyboard.press_and_release("ctrl+a")
    keyboard.press_and_release("backspace") # remove old text
    lTextForTest = str(random.randrange(100,99999))
    keyboard.write(lTextForTest)
    keyboard.press_and_release("ctrl+a")
    keyboard.press_and_release("ctrl+c")
    time.sleep(2)
    keyboard.press_and_release("backspace")  # remove old text
    lClipboardText = TextGet()
    lResult = lClipboardText == lTextForTest
    return lResult
# Check if cmd is opened
def CMDIsOpen():
    lTextForTest = str(random.randrange(100,99999))
    keyboard.write(lTextForTest+" |clip")
    keyboard.press_and_release("enter")
    time.sleep(2)
    lClipboardText = TextGet()
    lResult = lClipboardText == lTextForTest
    return lResult