import unittest
from threading import Timer
import sys
lFolderPath = "/".join(__file__.split("\\")[:-3])
sys.path.insert(0, lFolderPath)
from pyOpenRPA.Robot import OrchestratorConnector
from pyOpenRPA.Robot import Utils
class MyTestCase(unittest.TestCase):
    def test_something(self):
        #self.assertEqual(True, False)
        mGlobal={"Storage":{"R01_OrchestratorToRobot":{"Test":"Test2"}}}
        # t=OrchestratorConnector.IntervalDataSendAsync(
        #     Interval=1,
        #     RobotStorage=mGlobal["Storage"],
        #     RobotStorageKey="R01_OrchestratorToRobot",
        #     OrchestratorKeyList=["Storage", "R01_OrchestratorToRobot"],
        #     OrchestratorProtocol="http",
        #     OrchestratorHost="localhost",
        #     OrchestratorPort=8081,
        #     OrchestratorAuthToken="1992-04-03-0643-ru-b4ff-openrpa52zzz"
        # )
        # t=OrchestratorConnector.DataSendSync(
        #     RobotValue="Test",
        #     OrchestratorKeyList=["Storage", "R01_OrchestratorToRobot"],
        #     OrchestratorProtocol="http",
        #     OrchestratorHost="localhost",
        #     OrchestratorPort=8081,
        #     OrchestratorAuthToken="1992-04-03-0643-ru-b4ff-openrpa52zzz"
        # )
        import time
        #def Func(lT,inl):
        #    print(lT)
        #    return True
        #lTimer= Utils.TimerRepeat.TimerRepeat(1, Func, ["dddd"],{"inl":9})
        #lTimer.start()
        OrchestratorConnector.ConfigurationInit({
            "IntervalDataSendResetAsync": [
                {
                    "Interval": 2,
                    "RobotStorage": mGlobal["Storage"],
                    "RobotStorageKey": "R01_OrchestratorToRobot",
                    "RobotResetValue": {"Test": "Test"},
                    "OrchestratorKeyList": ["Storage", "R01_OrchestratorToRobot"],
                    "OrchestratorProtocol": "http",
                    "OrchestratorHost": "localhost",
                    "OrchestratorPort": 8081,
                    "OrchestratorAuthToken": "1992-04-03-0643-ru-b4ff-openrpa52zzz"
                }
            ]
        })
        while True:
            print(mGlobal["Storage"]["R01_OrchestratorToRobot"])
            # t = OrchestratorConnector.DataSendResetAsync(
            #     RobotStorage=mGlobal["Storage"],
            #     RobotStorageKey="R01_OrchestratorToRobot",
            #     RobotResetValue={"Test": "Test"},
            #     OrchestratorKeyList=["Storage", "R01_OrchestratorToRobot"],
            #     OrchestratorProtocol="http",
            #     OrchestratorHost="localhost",
            #     OrchestratorPort=8081,
            #     OrchestratorAuthToken="1992-04-03-0643-ru-b4ff-openrpa52zzz"
            # )
            time.sleep(0.5)
if __name__ == '__main__':
    unittest.main()
