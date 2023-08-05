#Import parent folder to import current / other packages
#########################################################
import sys
lFolderPath = "\\".join(__file__.split("\\")[:-3])
sys.path.insert(0, lFolderPath)
#########################################################
from pyOpenRPA.Studio import Studio