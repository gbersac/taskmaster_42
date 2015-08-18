import time
import threading
import datetime
import cmd
import os
import sys
import select
import shlex
import signal
import readline

from command import exit, status, start, restart, stop, reload
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
		time.sleep(0.01)

class CommandInterface(cmd.Cmd):
	"""Command line argument utilities."""

	prompt = "taskmaster>>> "

	def do_exit(self, line):
		exit.execute(progs)
		return True

	def do_EOF(self, line):
		exit.execute(progs)
		return True

	def get_prog_name(line):
		sline = shlex.split(line)
		if len(sline) < 1:
			print("*** Usage: cmd prog_name")
			return None
		return sline[0]

	def do_status(self, line):
		progs_lock.acquire(True)
		status.execute(progs)
		progs_lock.release()

	def do_start(self, line):
		progs_lock.acquire(True)
		prog_name = CommandInterface.get_prog_name(line)
		start.execute(progs, prog_name)
		progs_lock.release()

	def do_stop(self, line):
		progs_lock.acquire(True)
		prog_name = CommandInterface.get_prog_name(line)
		stop.execute(progs, prog_name)
		progs_lock.release()

	def do_restart(self, line):
		progs_lock.acquire(True)
		prog_name = CommandInterface.get_prog_name(line)
		restart.execute(progs, prog_name)
		progs_lock.release()

	def do_reload(self, line):
		global progs
		progs_lock.acquire(True)
		progs = reload.execute(progs)
		progs_lock.release()

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
