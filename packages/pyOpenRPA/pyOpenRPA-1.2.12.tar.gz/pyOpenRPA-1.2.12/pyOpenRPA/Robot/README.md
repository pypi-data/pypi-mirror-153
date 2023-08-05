# OpenRPA
First open source RPA platform for business is released!

# How to run
Studio
Double click to Studio\StudioRun_32.cmd or Studio\StudioRun_64.cmd

# Robot how to debug
Robot\PythonDebug_64.cmd
import Robot
Robot.ActivityRun(
	{
	   ModuleName: <"GUI"|..., str>,
	   ActivityName: <Function or procedure name in module, str>,
	   ArgumentList: [<Argument 1, any type>, ...] - optional,
	   ArgumentDict: {<Argument 1 name, str>:<Argument 1 value, any type>, ...} - optional
	}
)

# Robot example script:
Robot\Examples\GetFolderList\Python_32_Script_Run.cmd

# Python 32 bit
Resources\WPy32-3720\python-3.7.2\python.exe

# Python 64 bit
Resources\WPy64-3720\python-3.7.2.amd64\python.exe

# Module GUI activity List:
############################
Новая версия
############################
Получить список элементов, который удовлетворяет условиям через расширенный движок поиска
[
   {
       "index":<Позиция элемента в родительском объекте>,
       "depth_start" - глубина, с которой начинается поиск (по умолчанию 1)
       "depth_end" - глубина, до которой ведется поиск (по умолчанию 1)
       "class_name" - наименование класса, который требуется искать
       "title" - наименование заголовка
       "rich_text" - наименование rich_text
   }
]


# Open RPA Wiki
- [Home](https://gitlab.com/UnicodeLabs/OpenRPA/wikis/home)
- [04. Desktop app access (win32 & ui automation)](https://gitlab.com/UnicodeLabs/OpenRPA/wikis/04.-Desktop-app-access-(win32-&-ui-automation))

#Dependencies
*  Python 3 x32 [psutil, pywinauto, wmi, PIL, keyboard, pyautogui, win32api (pywin32), selenium, openCV, tesseract, requests, lxml, PyMuPDF]
*  Python 3 x64 [psutil, pywinauto, wmi, PIL, keyboard, pyautogui, win32api (pywin32), selenium, openCV, tesseract, requests, lxml, PyMuPDF]
*  pywinauto (Windows GUI automation)
*  Semantic UI CSS framework
*  JsRender by https://www.jsviews.com (switch to Handlebars)
*  Handlebars

Created by Unicode Labs (Ivan Maslov)