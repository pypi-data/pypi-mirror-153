"""
# How to use
# from pyOpenRPA.Tools import StopSafe
# StopSafe.Init(inLogger=None)
# StopSafe.IsSafeStop() # True - WM_CLOSE SIGNAL has come. taskkill /im someprocess.exe
"""


import win32con
import win32gui
import os
gIsSignalCloseBool = False
gLogger = None
gWindowTitleStr = "PythonTerminator" # Title of the phantom window
gWindowDescriptionStr = "pyOpenRPA library for safe turn off the program (by send the WM_CLOSE signal from task kill)" # Description of the phantom window

def Init(inLogger=None):
    """
    Init the StopSafe module. After that you can use def IsStopSafe() to check if close signal has come.

    :param inLogger: Logger to log messages about StopSafe
    :return:
    """
    global gLogger
    global gIsSignalCloseBool
    gIsSignalCloseBool = False # Init default
    gLogger = inLogger
    import threading
    if gLogger: gLogger.info(f"StopSafe: Init termination catch thread")
    shutdown_thread = threading.Thread(target=_shutdown_monitor)
    shutdown_thread.start()
    #shutdown_thread.join()
    #shutdown_monitor()
    

def IsStopSafe():
    """
    Check if stop signal has come.

    :return:
    """
    global gIsSignalCloseBool # Init the global variable
    return gIsSignalCloseBool # Return the result

def _shutdown_monitor():
    global gIsSignalCloseBool # Init the global variable
    global gLogger
    def wndproc(hwnd, msg, wparam, lparam):
        if msg == win32con.WM_CLOSE:
            win32gui.DestroyWindow(hwnd)
            return 0
        elif msg == win32con.WM_DESTROY:
            win32gui.PostQuitMessage(0)
            return 0
        return win32gui.DefWindowProc(hwnd, msg, wparam, lparam)
    wc = win32gui.WNDCLASS()
    wc.lpszClassName = gWindowTitleStr
    wc.lpfnWndProc = wndproc
    win32gui.RegisterClass(wc)
    hwnd = win32gui.CreateWindow(gWindowTitleStr, gWindowDescriptionStr,
                0, 0, 0, 0, 0, 0, 0, 0, None)
    win32gui.PumpMessages()
    gIsSignalCloseBool = True # WM_CLOSE message has come
    if gLogger:
        gLogger.info(f"StopSafe: Program has catch VM_CLOSE signal - do safe exit")
    
