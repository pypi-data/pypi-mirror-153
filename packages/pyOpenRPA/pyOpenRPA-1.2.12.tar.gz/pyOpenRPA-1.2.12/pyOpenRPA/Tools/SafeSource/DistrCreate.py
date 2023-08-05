import pyautogui # Enter password window
import hashlib # Create hash of the key
import tkinter #tkinter
from tkinter import filedialog
from . import Crypter
import shutil # Copy folder
import os # rm dir, listdir
import glob # list files
import datetime #Get current datetime
from Crypto.Cipher import AES
# Settings
gInUncryptedExtension = "py" # cry for filename.cry
gOutCryptedExtension = "cry" # cry for filename.cry
gFileMaskToDelete = "pyc" #Remove all .pyc files
# Create process run
def Run():
    print(f"{str(datetime.datetime.now())}: Start to create crypted distr")
    ############# Step 1 - select folder to copy 
    lStep_1_TkinterRoot = tkinter.Tk()
    lStep_1_TkinterRoot.withdraw()
    lStep_1_FolderPath = filedialog.askdirectory(parent=lStep_1_TkinterRoot,title='Please select a source code directory to crypt')
    ############# Step 2 - Select folder to save
    lStep_2_FolderPath = filedialog.askdirectory(parent=lStep_1_TkinterRoot,title='Please select a folder to save the crypted result')	
    # Before delete the folder check if directory is empty - else ask user to confirm the deletion
    if len(os.listdir(lStep_2_FolderPath)) != 0:
        lStep_2_ConfirmDelete = pyautogui.confirm('The destination folder contains some files/folders. The are will be removed. Continue?', buttons=['Yes', 'No'])
        if lStep_2_ConfirmDelete=="No":
            raise Exception("Stop program - user suggestion. Don't want to clear destination folder")
    shutil.rmtree(lStep_2_FolderPath, ignore_errors=False, onerror=None)
    ############# Step 3 - Copy folder
    shutil.copytree(lStep_1_FolderPath, lStep_2_FolderPath)
    ############# Step 3.1 - Remove files to delete 
    lPyFilesToDeleteList = [f for f in glob.glob(os.path.join(lStep_2_FolderPath,f"**/*.{gFileMaskToDelete}"), recursive=True)]
    for lFileItem in lPyFilesToDeleteList:
        #Create right \\ splashes
        lFileItem = os.path.abspath(lFileItem)
        #Remove old file
        os.remove(lFileItem)
    ############# Step 4 - Get file list with extension .py
    lPyFileList = [f for f in glob.glob(os.path.join(lStep_2_FolderPath,f"**/*.{gInUncryptedExtension}"), recursive=True)]
    ############# Step 5 - Ask and confirm the secret word
    lKeyHashStr_1 = hashlib.sha256(pyautogui.password('Please enter the key to protect source code').encode("utf-8")).digest()
    lKeyHashStr_2 = hashlib.sha256(pyautogui.password('Please repeat the key to protect source code').encode("utf-8")).digest()
    if lKeyHashStr_1 == lKeyHashStr_2:
        for lFileItem in lPyFileList:
            #Hotfix - dont encrypt __main__.py to __main__.cry - python dont see it
            if True:#"__main__.py" not in lFileItem:
                #Create right \\ splashes
                lFileItem = os.path.abspath(lFileItem)
                Crypter.encrypt_file(lKeyHashStr_1, lFileItem, f"{lFileItem[0:-2]}{gOutCryptedExtension}")
                #Remove old file
                os.remove(lFileItem)
    else:
        raise Exception("User set different secret key 1 and key 2")
    ############ Step 6 - Final stage
    print(f"{str(datetime.datetime.now())}: Crypted distr is created!")