import threading

# Check if current execution is in Processor thread
def IsProcessorThread(inGSettings):
    return inGSettings["ProcessorDict"]["ThreadIdInt"] == threading.get_ident()

def IsOrchestratorInitialized(inGSettings) -> bool:
    """
    Check if Orchestrator will be successfully initialized

    :param inGSettings: global settings (singleton)
    :return:
    """
    # Check if gSettings has flag "HiddenOrchestratorInitBool"
    return inGSettings.get("HiddenIsOrchestratorInitializedBool", False)