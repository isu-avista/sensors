from enum import Enum


class ManagerState(Enum):
    """Enum representing the various states of the processor manager"""

    IDLE = 0
    STARTING = 1
    INITIALIZING = 2
    EXECUTING = 3
    STOPPING = 4

    def __repr__(self):
        """An unambiguous representation of ManagerState"""
        return f"Manager State: {self.name}"

    def __str__(self):
        """A readable representation of ManagerState"""
        return f"{self.name}"

    @staticmethod
    def from_str(label):
        """Provides an instance of the Role for the given string.

        Args:
            label (str): String representation of ManagerState literal

        Returns:
            ManagerState: literal of ManagerSTate

        Raises:
            NotImplementedError: If value is not a defined enum literal of ManagerState
        """
        if label in ('IDLE', 'idle', 'Idle'):
            return ManagerState.IDLE
        elif label in ('STARTING', 'starting', 'Starting'):
            return ManagerState.STARTING
        elif label in ('INITIALIZING', 'initializing', 'Initializing'):
            return ManagerState.INITIALIZING
        elif label in ('EXECUTING', 'executing', 'Executing'):
            return ManagerState.EXECUTING
        elif label in ('STOPPING', 'stopping', 'Stopping'):
            return ManagerState.STOPPING
        else:
            raise NotImplementedError
