import unittest
from avista_sensors.manager_state import ManagerState


class ManagerStateTest(unittest.TestCase):
    def test_from_str(self):
        oracle = [
            ["IDLE", ManagerState.IDLE],
            ["idle", ManagerState.IDLE],
            ["Idle", ManagerState.IDLE],
            ["STARTING", ManagerState.STARTING],
            ["starting", ManagerState.STARTING],
            ["Starting", ManagerState.STARTING],
            ["INITIALIZING", ManagerState.INITIALIZING],
            ["initializing", ManagerState.INITIALIZING],
            ["Initializing", ManagerState.INITIALIZING],
            ["EXECUTING", ManagerState.EXECUTING],
            ["executing", ManagerState.EXECUTING],
            ["Executing", ManagerState.EXECUTING],
            ["STOPPING", ManagerState.STOPPING],
            ["stopping", ManagerState.STOPPING],
            ["Stopping", ManagerState.STOPPING]
        ]
        for x in range(len(oracle)):
            self.assertEqual(oracle[x][1], ManagerState.from_str(oracle[x][0]))

    def test_invalid_str(self):
        with self.assertRaises(NotImplementedError):
            ManagerState.from_str("Test")

    def test_none(self):
        with self.assertRaises(NotImplementedError):
            ManagerState.from_str(None)

    def test_repr(self):
        self.assertEqual("Manager State: IDLE", ManagerState.IDLE.__repr__(), "repr not same")

    def test_str(self):
        self.assertEqual("IDLE", str(ManagerState.IDLE), "string representation not same")


if __name__ == '__main__':
    unittest.main()
