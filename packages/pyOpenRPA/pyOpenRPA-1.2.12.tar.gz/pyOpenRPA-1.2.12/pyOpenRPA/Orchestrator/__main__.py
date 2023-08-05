import sys
lFolderPath = "\\".join(__file__.split("\\")[:-3])
sys.path.insert(0, lFolderPath)
from pyOpenRPA.Orchestrator import __Orchestrator__
__Orchestrator__.__deprecated_orchestrator_start__() # Backward compatibility below the v1.2.0. Will be deprecated in 1.3.0