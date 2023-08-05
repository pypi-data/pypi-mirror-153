from enum import Enum


class SherpaJobBeanStatus(str, Enum):
    STARTED = "STARTED"
    PAUSED = "PAUSED"
    CANCELLED = "CANCELLED"
    FAILED = "FAILED"
    COMPLETED = "COMPLETED"

    def __str__(self) -> str:
        return str(self.value)
