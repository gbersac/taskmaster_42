from enum import Enum

class ProcessStatusEnum(Enum):
	NOT_LAUNCH = 0
	RUNNING = 1
	STOP_OK = 2
	STOP_KO = 3
