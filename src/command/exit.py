import os
import sys
from .command import Command

class CmdExit(Command):
	name = "exit"
	help_strg = "Exit the main program"

	"""This is the exit command to quit the main program"""
	def __init__(self):
		super(CmdExit, self).__init__()

	def execute(self, sp, progs):
		print("end of program")
		progs.kill_all()
		sys.exit(os.EX_OK)
