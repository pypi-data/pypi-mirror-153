import sys
lFolderPath = "\\".join(__file__.split("\\")[:-3])
sys.path.insert(0, lFolderPath)
from pyOpenRPA.Tools.RobotDB import RobotDB