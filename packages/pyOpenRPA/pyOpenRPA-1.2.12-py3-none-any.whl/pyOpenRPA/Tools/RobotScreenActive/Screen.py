from PIL import ImageGrab
import os # to execute cmd commands
#Check if screen is exists
def Exists():
    #Try to get 1 px from screen
    try:
        #Take 1 px
        ImageGrab.grab(bbox=(0,0,1,1))
        #Screen is exists - return True
        return True
    #Catch exception
    except Exception:
        #Screen does not exists - return false
        return False
#Make console session
def ConsoleScreenBase():
    #Get script folder path
    lFolderPath = "/".join(__file__.split("\\")[:-1])
    #Send command to cmd
    os.system(os.path.join(lFolderPath,"ConsoleStart.bat"))