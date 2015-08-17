import os
import sys

def execute(progs):
	print("end of taskmaster")
	progs.kill_all()
	sys.exit(os.EX_OK)
