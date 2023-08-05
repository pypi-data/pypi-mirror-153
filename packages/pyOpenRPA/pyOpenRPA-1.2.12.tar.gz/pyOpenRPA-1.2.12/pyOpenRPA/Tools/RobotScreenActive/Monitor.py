import time #lib to create delay
from . import Screen # module to detect screen exists
#Check screen every 1 second
def CheckScreen(inIntervalSeconds=1):
    while True:
        #Check if screen exist
        if not Screen.Exists():
            #Send os command to create console version (base screen)
            Screen.ConsoleScreenBase()
            #Delay to create console screen
            time.sleep(2)
        #Delay
        time.sleep(inIntervalSeconds)
    return None