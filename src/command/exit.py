import os
import sys
import logger

def execute(progs):
	progs.kill_all()
	logger.log("END TASKMASTER")
	print("end of taskmaster")
	sys.exit(os.EX_OK)
