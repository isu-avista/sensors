import unittest
from avista_sensors.sweep_state import SweepState


class ManagerStateTest(unittest.TestCase):
    def test_from_str(self):
        oracle = [
            ["IDLE", SweepState.IDLE],
            ["idle", SweepState.IDLE],
            ["Idle", SweepState.IDLE],
            ["STARTING", SweepState.STARTING],
            ["starting", SweepState.STARTING],
            ["Starting", SweepState.STARTING],
            ["INITIALIZING", SweepState.INITIALIZING],
            ["initializing", SweepState.INITIALIZING],
            ["Initializing", SweepState.INITIALIZING],
            ["EXECUTING", SweepState.EXECUTING],
            ["executing", SweepState.EXECUTING],
            ["Executing", SweepState.EXECUTING],
            ["STOPPING", SweepState.STOPPING],
            ["stopping", SweepState.STOPPING],
            ["Stopping", SweepState.STOPPING]
        ]
        for x in range(len(oracle)):
            self.assertEqual(oracle[x][1], SweepState.from_str(oracle[x][0]))

    def test_invalid_str(self):
        with self.assertRaises(NotImplementedError):
            SweepState.from_str("Test")

    def test_none(self):
        with self.assertRaises(NotImplementedError):
            SweepState.from_str(None)

    def test_repr(self):
        self.assertEqual("Manager State: IDLE", SweepState.IDLE.__repr__(), "repr not same")

    def test_str(self):
        self.assertEqual("IDLE", str(SweepState.IDLE), "string representation not same")


if __name__ == '__main__':
    unittest.main()
