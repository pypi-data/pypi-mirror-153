import time
import os
from .. import __Orchestrator__
from . import Process
import threading
from typing import List
from typing import Tuple

from pyOpenRPA import Orchestrator

class Git():

    mAgentHostNameStr = None
    mAgentUserNameStr = None
    mAbsPathStr = None
    mProcessList: List[Tuple] = [] # List of the key turples of the Process instance

    def __init__(self, inAgentHostNameStr=None, inAgentUserNameStr=None, inGitPathStr=""):
        """
        Init the Git repo instance. It helps to detect new changes in repo and auto restart services

        :param inAgentHostNameStr: Agent hostname in any case. Required to identify Process. If None - works with Orc session
        :param inAgentUserNameStr: Agent user name in any case. Required to identify Process. If None - works with Orc session
        :param inGitPathStr: Relative (from the orchestrator working directory) or absolute. If "" - work with Orc repo
        :return:
        """
        lAbsPathStr = os.path.abspath(inGitPathStr)
        lAbsPathUpperStr = lAbsPathStr.upper()
        lGS = __Orchestrator__.GSettingsGet()
        # Check if Process is not exists in GSettings
        if (inAgentHostNameStr.upper(), inAgentUserNameStr.upper(), lAbsPathUpperStr) not in lGS["ManagersGitDict"]:
            self.mAbsPathStr = lAbsPathStr
            self.mAbsPathUpperStr = lAbsPathUpperStr
            self.mAgentHostNameStr = inAgentHostNameStr
            self.mAgentUserNameStr = inAgentUserNameStr
            lGS["ManagersGitDict"][(inAgentHostNameStr.upper(), inAgentUserNameStr.upper(), lAbsPathUpperStr)]=self
        else: raise Exception(f"Managers.Git ({inAgentHostNameStr}, {inAgentUserNameStr}, {lAbsPathUpperStr}): Can't init the Git instance because it already inited in early")

    def ProcessConnect(self, inProcess: Process):
        """
        Connect process to the Git instance. It will apply to stop safe process when upgrade the repo and than start it

        :param inProcess: Process instance
        :type inProcess: Process
        """
        lProcessTurple = inProcess.KeyTurpleGet()
        if lProcessTurple not in self.mProcessList:
            self.mProcessList.append(lProcessTurple)
        else:
            raise Exception(f"Process with current key is already exists in Git process list.")

    def ProcessListSaveStopSafe(self):
        """
        Save the state and do the stop safe for the all processes
        Will send safe stop in parallel mode but wait to the end of the safestop for the all processes. After that will continue
        """
        lIntervalScheckSecFloat = 5.0
        lThreadList:List[threading.Thread] = []
        for lProcessItemTuple in self.mProcessList:
            lProcessItem = Orchestrator.Managers.ProcessGet(*lProcessItemTuple)
            lProcessItem.StatusSave()
            lThread = threading.Thread(target=lProcessItem.StopSafe)
            lThread.start()
            lThreadList.append(lThread)
        # Wait for all process will be safe stopped
        lAllThreadStoppedBool = False
        while not lAllThreadStoppedBool:
            lAllThreadStoppedBool = True
            for lThread in lThreadList:
                if lThread.is_alive() == True:
                    lAllThreadStoppedBool = False
                    break
            time.sleep(lIntervalScheckSecFloat)

    def ProcessListRestore(self):
        """
        Restore the process state for the all processes
        """
        for lProcessItem in self.mProcessList:
            lProcessItem.StatusRestore()

    def __OSCMDShell__(self, inCMDStr):
        """
        Detect the way of use and send the cmd. Wait for command execution!

        :return: None is not exists
        """
        if self.mAgentUserNameStr is not None and self.mAgentHostNameStr is not None: # Check if Agent specified
            lActivityItemGUIDStr = __Orchestrator__.AgentOSCMD(inHostNameStr=self.mAgentHostNameStr,inUserStr=self.mAgentUserNameStr,inCMDStr=inCMDStr,inRunAsyncBool=False,inSendOutputToOrchestratorLogsBool=False)
            lCMDResultStr = __Orchestrator__.AgentActivityItemReturnGet(inGUIDStr=lActivityItemGUIDStr)
        else:
            lCMDResultStr = __Orchestrator__.OSCMD(inCMDStr=inCMDStr, inRunAsyncBool=False)
        return lCMDResultStr

    def BranchRevGet(self, inBranchNameStr="HEAD"):
        """
        Get the specified branch revision. Default return the current branch revision

        .. code-block:: python
            lGit.BranchRevGet(inBranchNameStr="dev") # Get revision of the local dev branch
            lGit.BranchRevGet(inBranchNameStr="remotes/origin/dev") # Get revision of the remotes dev branch
            lGit.BranchRevGet(inBranchNameStr="HEAD") # Get revision of the current HEAD branch
            lGit.BranchRevGet() # Equal to the call inBranchNameStr="HEAD"

        :param inBranchNameStr: The branch name where to get revision guid
        :return: revision GUID
        """
        lCMDStr = f"cd \"{self.mAbsPathUpperStr}\" && git rev-parse {inBranchNameStr}"
        lCMDResultStr = self.__OSCMDShell__(inCMDStr=lCMDStr)
        return lCMDResultStr

    def BranchRevIsLast(self, inBranchLocalStr: str, inBranchRemoteStr: str) -> bool:
        """Get fetch and check if local branch revision is last (if check with remote)

        :param inBranchLocalStr: _description_
        :type inBranchLocalStr: str
        :param inBranchRemoteStr: example: origin/prd
        :type inBranchRemoteStr: str
        :return: _description_
        :rtype: bool
        """
        lIsLastBool = False
        self.Fetch()
        lLocalBranchRevStr = self.BranchRevGet(inBranchNameStr=inBranchLocalStr)
        lRemoteBranchRevStr = self.BranchRevGet(inBranchNameStr=inBranchRemoteStr)
        if lLocalBranchRevStr == lRemoteBranchRevStr:
            lIsLastBool = True
        return lIsLastBool


    def BranchRevLastGetInterval(self, inBranchLocalStr: str, inBranchRemoteStr: str, inPreviousBranchRestoreBool: bool = True, inIntervalSecFloat: float = 60.0):
        """Periodically check if revision is last

        :param inBranchLocalStr: _description_
        :type inBranchLocalStr: str
        :param inBranchRemoteStr: example: origin/prd
        :type inBranchRemoteStr: str
        :param inPreviousBranchRestoreBool: _description_, defaults to True
        :type inPreviousBranchRestoreBool: bool, optional
        :param inIntervalSecFloat: _description_, defaults to 60.0
        :type inIntervalSecFloat: float, optional
        """    
        #self.BranchRevLastGet(inBranchLocalStr, inBranchRemoteStr, inPreviousBranchRestoreBool)    
        Orchestrator.OrchestratorScheduleGet().every(inIntervalSecFloat).seconds.do(self.BranchRevLastGet, inBranchLocalStr, inBranchRemoteStr, inPreviousBranchRestoreBool)

    def BranchRevLastGet(self, inBranchLocalStr: str, inBranchRemoteStr: str, inPreviousBranchRestoreBool: bool = True):
        """Do some action to get the last revision

        :param inBranchLocalStr: [description]
        :type inBranchLocalStr: str
        :param inBranchRemoteStr: [description]
        :type inBranchRemoteStr: str
        """
        Orchestrator.OrchestratorLoggerGet().debug(f"Managers.Git ({self.mAbsPathStr}): self.BranchRevLastGet has been init")
        # check if the correct revision
        lCMDResultStr = None
        if self.BranchRevIsLast(inBranchLocalStr=inBranchLocalStr, inBranchRemoteStr=inBranchRemoteStr) == False:
            Orchestrator.OrchestratorLoggerGet().info(f"Managers.Git ({self.mAbsPathStr}): self.BranchRevLastGet, new rev (branch: {inBranchLocalStr}) has been detected - merge (branch: {inBranchRemoteStr})")
            # Do the stop safe for the connected process
            self.ProcessListSaveStopSafe()
            lBranchNameCurrentStr = self.BranchNameGet()
            # reset all changes in local folder
            self.Clear()
            # checkout
            self.BranchCheckout(inBranchNameStr=inBranchLocalStr)
            # merge
            lCMDStr = f"cd \"{self.mAbsPathUpperStr}\" && git merge {inBranchRemoteStr}"
            lCMDResultStr = self.__OSCMDShell__(inCMDStr=lCMDStr)
            if inPreviousBranchRestoreBool == True:
                # checkout to the source branch which was
                self.BranchCheckout(inBranchNameStr=lBranchNameCurrentStr)
            # do the orc restart
            Orchestrator.OrchestratorLoggerGet().info(f"Managers.Git ({self.mAbsPathStr}): self.BranchRevLastGet, merge done, restart orc")
            Orchestrator.OrchestratorRestart()
        return lCMDResultStr

    def BranchNameGet(self) -> str:
        """Get the current local branch name

        :return: current local branch name
        """
        #"git rev-parse --abbrev-ref HEAD"
        lCMDStr = f"cd \"{self.mAbsPathUpperStr}\" && git rev-parse --abbrev-ref HEAD"
        lCMDResultStr = self.__OSCMDShell__(inCMDStr=lCMDStr)
        return lCMDResultStr

    def BranchCheckout(self, inBranchNameStr):
        self.Clear()
        lCMDStr = f"cd \"{self.mAbsPathUpperStr}\" && git checkout {inBranchNameStr}"
        lCMDResultStr = self.__OSCMDShell__(inCMDStr=lCMDStr)
        return lCMDResultStr

    def Clear(self):
        """Clear the all changes in the local folder. Get up to the current revision
        """
        # f"git clean -f -d" # Очистить от лишних файлов
        lCMDStr = f"cd \"{self.mAbsPathUpperStr}\" && git clean -f -d"
        lCMDResultStr = self.__OSCMDShell__(inCMDStr=lCMDStr)
        # f"git reset --hard" # Откатить файлы, которые отслеживаются Git и которые были изменены
        lCMDStr = f"cd \"{self.mAbsPathUpperStr}\" && git reset --hard"
        lCMDResultStr = self.__OSCMDShell__(inCMDStr=lCMDStr)
        return lCMDResultStr

    def Fetch(self):
        """
        Get updates from the git server.

        .. code-block:: python
            lGit.Fetch() # get updates from the server

        :return: None
        """
        lCMDStr = f"cd \"{self.mAbsPathUpperStr}\" && git fetch"
        lCMDResultStr = self.__OSCMDShell__(inCMDStr=lCMDStr)
        return lCMDResultStr

def GitExists(inAgentHostNameStr: str, inAgentUserNameStr: str, inGitPathStr: str) -> bool:
    """
    Check if the Git instance is exists in GSettings by the (inAgentHostNameStr: str, inAgentUserNameStr: str, inGitPathStr: str)

    :param inAgentHostNameStr: Agent hostname in any case. Required to identify Process
    :param inAgentUserNameStr: Agent user name in any case. Required to identify Process
    :param inGitPathStr: Relative (from the orchestrator working directory) or absolute. If "" - work with Orc repo
    :return: True - process exists in gsettings; False - else
    """
    return (inAgentHostNameStr.upper(), inAgentUserNameStr.upper(), inGitPathStr.upper()) in __Orchestrator__.GSettingsGet()["ManagersGitDict"]


def GitGet(inAgentHostNameStr: str, inAgentUserNameStr: str, inGitPathStr: str) -> Git:
    """
    Return the Git instance by the (inAgentHostNameStr: str, inAgentUserNameStr: str, inGitPathStr: str)

    :param inAgentHostNameStr: Agent hostname in any case. Required to identify Process
    :param inAgentUserNameStr: Agent user name in any case. Required to identify Process
    :param inGitPathStr: Relative (from the orchestrator working directory) or absolute. If "" - work with Orc repo
    :return: Git instance (if exists) Else None
    """
    lAbsPathUpperStr = os.path.abspath(inGitPathStr).upper()
    return __Orchestrator__.GSettingsGet()["ManagersGitDict"].get((inAgentHostNameStr.upper(), inAgentUserNameStr.upper(), lAbsPathUpperStr),None)


def GitBranchRevGet(inAgentHostNameStr: str, inAgentUserNameStr: str, inGitPathStr: str, inBranchNameStr: str="HEAD") -> str:
    lGit = GitGet(inAgentHostNameStr = inAgentHostNameStr, inAgentUserNameStr = inAgentUserNameStr, inGitPathStr=inGitPathStr)
    if lGit is not None: return lGit.BranchRevGet(inBranchNameStr=inBranchNameStr)

def GitFetch(inAgentHostNameStr: str, inAgentUserNameStr: str, inGitPathStr: str) -> None:
    lGit = GitGet(inAgentHostNameStr=inAgentHostNameStr, inAgentUserNameStr=inAgentUserNameStr,
                  inGitPathStr=inGitPathStr)
    if lGit is not None: lGit.Fetch()