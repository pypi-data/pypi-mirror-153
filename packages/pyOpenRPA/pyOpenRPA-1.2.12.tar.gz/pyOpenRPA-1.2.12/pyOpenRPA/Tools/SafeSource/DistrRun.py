#coding=utf-8

import os
import sys
import imp
import base64
from . import Crypter # Crypto functions
import datetime #Datetime
import hashlib #Get hash of the word
import pyautogui
import os
import glob # list files
EXT = '.cry'
gExtensionName = "cry"
# How to run
# sys.meta_path.append(Base64Importer(root_pkg_path))

# Init cryptographer
def CryptographerInit(inFolderPathList, inKey):
    #sys.meta_path.append(Base64Importer(inFolderPath))
    # Flag add subfolder, which contains extension files
    #path = 'c:\\projects\\hc2\\'
    #folders = []
    # Recursive walk throught the tree
    # r=root, d=directories, f = files
    #import pdb
    #pdb.set_trace()
    for lItem in inFolderPathList:
        sys.meta_path.append(Base64Importer(os.path.abspath(lItem), inKey=inKey))
        #for r, d, f in os.walk(lItem):
        #    for folder in d:
                #folders.append(os.path.join(r, folder))
                #sys.meta_path.append(Base64Importer(os.path.join(r, folder), inKey=inKey))
        #        pass
        #for f in folders:
        #    print(f)
#===============================================================================
class Base64Importer(object):
    """Служит для поиска и импорта python-модулей, кодированных в base64
    Класс реализует Import Protocol (PEP 302) для возможности импортирования
    модулей, зашифрованных в base64 из указанного пакета.
    """
    #---------------------------------------------------------------------------
    def __init__(self, root_package_path, inKey):
        self.mKeyStr = inKey
        self.__modules_info = self.__collect_modules_info(root_package_path)
        # Create list of cry files when run
        #for lItem in root_package_path_list:
        #    lCryptedFileList = [f for f in glob.glob(os.path.join(lItem,f"**/*.{EXT}"), recursive=True)]
    #---------------------------------------------------------------------------
    def find_module(self, fullname, path=None):
        """Метод будет вызван при импорте модулей
        Если модуль с именем fullname является base64 и находится в заданной
        папке, данный метод вернёт экземпляр импортёра (finder), либо None, если
        модуль не является base64.
        """
        #print(f"find_module:: Fullname: {fullname}, path: {path}")
        #print(f"modules info: {self.__modules_info}")
        if fullname in self.__modules_info:
            return self
        return None
    #---------------------------------------------------------------------------
    def load_module(self, fullname):
        """Метод загружает base64 модуль
        Если модуль с именем fullname является base64, то метод попытается его
        загрузить. Возбуждает исключение ImportError в случае любой ошибки.
        """
        #print(f"load_module:: Fullname: {fullname}")
        if not fullname in self.__modules_info:
            raise ImportError(fullname)
        # Для потокобезопасности
        imp.acquire_lock()
        try:
            mod = sys.modules.setdefault(fullname, imp.new_module(fullname))
            mod.__file__ = "<{}>".format(self.__class__.__name__)
            mod.__file__ = self.__modules_info[fullname]['filename'] #Hotfix
            #print(f"MODFILE::{mod.__file__}")
            mod.__loader__ = self
            if self.is_package(fullname):
                mod.__path__ = []
                mod.__package__ = fullname
            else:
                mod.__package__ = fullname.rpartition('.')[0]
            src = self.get_source(fullname)
            try:
                #__name__ = "pyPackage"
                #print(f"MODNAME:: {mod.__name__}")
                #exec(src) in mod.__dict__
                exec(src,mod.__dict__)
            except:
                del sys.modules[fullname]
                raise ImportError(fullname)
        finally:
            imp.release_lock()
        return mod
    #---------------------------------------------------------------------------
    def is_package(self, fullname):
        """Возвращает True если fullname является пакетом
        """
        return self.__modules_info[fullname]['ispackage']

    #---------------------------------------------------------------------------
    def get_source(self, fullname):
        """Возвращает исходный код модуля fullname в виде строки

        Метод декодирует исходные коды из base64
        """
        filename = self.__modules_info[fullname]['filename']

        try:
            src = Crypter.decrypt_file_bytes(key = self.mKeyStr, in_filename = filename).decode("utf-8")
            #with open(filename, 'r') as ifile:
            #    src = base64.decodestring(ifile.read())
        except IOError:
            src = ''

        return src
    # for __main__
    def get_code(self, inModName):
        return self.get_source(inModName)
    #---------------------------------------------------------------------------
    def __collect_modules_info(self, root_package_path):
        """Собирает информацию о модулях из указанного пакета
        """
        modules = {}
        """
        p = os.path.abspath(root_package_path)
        dir_name = os.path.dirname(p) + os.sep
        #dir_name = "" # Hotfix 2020 03 19
        #print(f"__collect_modules_info:: root_package_path: {root_package_path}")
        for root, _, files in os.walk(p):
            # Информация о текущем пакете
            filename = os.path.join(root, '__init__' + EXT)
            p_fullname = root.rpartition(dir_name)[2].replace(os.sep, '.')
            modules[p_fullname] = {
                'filename': filename,
                'ispackage': True
            }
            # Информация о модулях в текущем пакете
            for f in files:
                if not f.endswith(EXT):
                    continue
                filename = os.path.join(root, f)
                fullname = '.'.join([p_fullname, os.path.splitext(f)[0]])
                fullname = os.path.splitext(f)[0]
                modules[fullname] = {
                    'filename': filename,
                    'ispackage': False
                }
        """
        # # # # # # # # # # #
        # New way of collection
        lRootAbsPath = os.path.abspath(root_package_path)
        #print(lRootAbsPath)
        lNewPathIndex = len(lRootAbsPath)+len(os.sep) # Len of the root path + len sep
        lCryptedFileList = [f for f in glob.glob(os.path.join(lRootAbsPath,f"**/*.{gExtensionName}"), recursive=True)]
        #print(lCryptedFileList)
        for lCryptedItemFullPath in lCryptedFileList:
            # Get Module name
            lModuleName = lCryptedItemFullPath[lNewPathIndex:-(1+len(gExtensionName))].replace(os.sep, '.')
            # Check if file is not __init__.{EXT} - This is package
            if f"__init__.{EXT}" in lCryptedItemFullPath:
                # Add package
                lModuleName = lModuleName.replace(f"{os.sep}__init__.{gExtensionName}","")
                modules[lModuleName] = {
                    'filename': lCryptedItemFullPath,
                    'ispackage': True
                }
            else:
                # Add item 
                modules[lModuleName] = {
                    'filename': lCryptedItemFullPath,
                    'ispackage': False
                }
        return modules
# Settings
gInUncryptedExtension = "py" # cry for filename.cry
gOutCryptedExtension = "cry" # cry for filename.cry
gFileMaskToDelete = "pyc" #Remove all .pyc files

#Settings to run crypted module
gSettings = {
    #runpy
    "run_module": {
        "mod_name": "TestPackage", #"TestPackage",
        "init_globals": None,
        "run_name": None,
        "alter_sys": True
    }
}

# Settings
gInUncryptedExtension = "py" # cry for filename.cry
gOutCryptedExtension = "cry" # cry for filename.cry
gFileMaskToDelete = "pyc" #Remove all .pyc files
print(f"{str(datetime.datetime.now())}: Run decryptography")
############# Step 5 - Ask and confirm the secret word
lKeyHashStr_1 = hashlib.sha256(pyautogui.password('Please enter the key to protect source code').encode("utf-8")).digest()
lKeyHashStr_2 = hashlib.sha256(pyautogui.password('Please repeat the key to protect source code').encode("utf-8")).digest()
if lKeyHashStr_1 == lKeyHashStr_2:
    #sys.meta_path.append(Base64Importer("TestPackage",inKey = lKeyHashStr_1))
    CryptographerInit(sys.argv[1:], inKey = lKeyHashStr_1)
    print(f"{str(datetime.datetime.now())}: Cryprography module has been successfully initialized")
    if __name__ == "__main__":
        #import runpy
        #runpy.run_module(**gSettings["run_module"])
        #runpy.run_path("pyPackage_Settings", init_globals=None, run_name=None)
        # Here is the execution code...
        #############
        ###########
        #######
else:
    raise Exception("User set different secret key 1 and key 2")