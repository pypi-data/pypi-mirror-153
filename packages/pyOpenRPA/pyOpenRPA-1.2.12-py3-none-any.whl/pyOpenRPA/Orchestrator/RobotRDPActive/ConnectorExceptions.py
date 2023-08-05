#####################################
# RobotRDPActive Exceptions class
#####################################
class SessionWindowNotExistError(Exception): pass #Error when Window not exists
class SessionWindowNotResponsibleError(Exception): pass # Error when Window not responding to delete
class RUNExistError(Exception): pass # Error when RUN window not identified
class CMDResponsibleError(Exception): pass # Error when command is not return
class HostNoGUIError(Exception): pass # Orchestrator session has no GUI
#try: 
#    raise SessionWindowNotResponsibleError("Test")
#except SessionWindowNotResponsibleError as e:
#    print("Catched")
