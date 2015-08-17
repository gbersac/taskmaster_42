import threading
import cmd
import os
import sys
import select
import shlex
import signal
import readline

from command import exit
from program.program import Program
from program.program_lst import ProgramLst

progs = None
progs_lock = None
interf = None

def signal_handler(signal, frame):
	if interf:
		interf.quit()
	exit.execute(progs)

def thread_check_progs():
	"""
	Function executed in the thread for checking the state of
	all the progs
	"""
	while True:
		progs_lock.acquire(True)
		progs.check()
		progs_lock.release()

class CommandInterface(cmd.Cmd):
	"""Command line argument utilities."""

	prompt = "taskmaster>>> "

	def cmdloop(self):
		return cmd.Cmd.cmdloop(self)

	def do_exit(self, line):
		exit.execute(progs)

	def do_EOF(self, line):
		exit.execute(progs)
		return True

	def postloop(self):
		print

if __name__ == '__main__':
	# create signal handler
	signal.signal(signal.SIGINT, signal_handler)

	# read progs
	progs = ProgramLst()
	progs.launch()
	progs_lock = threading.Lock()

	# launch a thread to test progs
	t = threading.Thread(target = thread_check_progs)
	t.daemon = True
	t.start()

	# command loop
	CommandInterface().cmdloop()
