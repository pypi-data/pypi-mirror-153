import os
import threading
import pdb
import time

"""Module wait file "init_debug" in working directory
"""
    
gKWARGS = None

def LiveDebugCheckLoop():
    while True:
        if os.path.exists("init_debug"):
            pdb.set_trace()
        time.sleep(30.0)

def LiveDebugCheckThread(**inKWARGS):
    """Create thread to wait file appear "init_debug" in the working directory. 
    """
    global gKWARGS
    gKWARGS = inKWARGS
    lThread = threading.Thread(target=LiveDebugCheckLoop)
    lThread.start()