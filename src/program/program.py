import os
import shlex
import subprocess
import signal

from .process import Process
from .auto_restart_enum import AutoRestartEnum

class ProgramWithoutCmdError(Exception):
    def __init__(self, _name):
        self.name = _name

    def __str__(self):
        return 'program ' + self.name + ' has no cmd attribute'

class UnknowSignalError(Exception):
    def __init__(self, _name):
        self.name = _name

    def __str__(self):
        return 'unknow signal ' + self.name

class Program:
	"""
	A Program to be launch by the taskmaster

	This is all of the options supported by this class :
	cmd, numprocs, autostart, autorestart, exitcodes, starttime,
	startretries, stopsignal, stoptime, stdout, env, directory, umask.
	"""

	"""The number of processes to start and keep running"""
	numprocs = 1
	"""Whether to start this program at launch or not"""
	autostart = True
	"""Whether the program should be restarted always, never, or on unexpected exits only"""
	autorestart = AutoRestartEnum.unexpected
	"""Which return codes represent an "expected" exit status"""
	exitcodes = os.EX_OK
	"""How long the program should be running after it’s started for it to be considered successfully started"""
	starttime = None
	"""How many times a restart should be attempted before aborting"""
	startretries = 0
	"""Which signal should be used to stop (i.e. exit gracefully) the program"""
	stopsignal = signal.SIGTERM
	"""How long to wait after a graceful stop before killing the program"""
	stoptime = None
	"""The command to use to launch the program"""
	cmd = False
	"""A working directory to set before launching the program"""
	workingdir = None
	"""Options to discard the program’s stdout or to redirect them to files"""
	stdout = None
	"""Options to discard the program’s stderr or to redirect them to files"""
	stderr = None
	""" An umask to set before launching the program"""
	umask = 22

	"""List of all the processes associated with this program."""
	processes = []

	def signal_from_str(s):
		s = s.upper()
		if s == "TERM":
			return signal.SIGTERM
		if s == "HUP":
			return signal.SIGHUP
		if s == "INT":
			return signal.SIGINT
		if s == "QUIT":
			return signal.SIGQUIT
		if s == "KILL":
			return signal.SIGKILL
		if s == "USR1":
			return signal.SIGUSR1
		if s == "USR2":
			return signal.SIGUSR2
		raise UnknowSignalError()

	def __init__(self, _name, dico):
		"""
		dico:	parsed from the yaml conf file.
		The first entry is {program name : {list of parameters}}
		The dico must contain at least the cmd attribute
		"""
		self.name = _name
		for k, v in dico.items():
			setattr(self, k, v)
		if not self.cmd:
			raise ProgramWithoutCmdError(_name)
			return
		self.autorestart = AutoRestartEnum.fromstr(self.autorestart)
		self.processes = []
		if type(self.stopsignal) == str:
			self.stopsignal = Program.signal_from_str(self.stopsignal)
		for i in range(0, self.numprocs):
			self.processes.append(Process(self.name, self.cmd))

	def get_expanded_env(self):
		new_env = os.environ
		if not hasattr(self, "env"):
			return new_env
		for k, v in self.env.items():
			new_env[k] = str(v)
		return new_env

	def execute(self):
		new_env = self.get_expanded_env()
		for proc in self.processes:
			proc. set_execution_vars(self.stdout, self.stderr, new_env, \
					self.workingdir, "umask {:03d};".format(self.umask))
			proc.execute()

	def relaunch(self):
		self.execute()

	def relaunch_if_needed(self):
		# print("relaunch_if_needed")
		if self.autorestart == AutoRestartEnum.never or self.startretries < 1:
			return
		for proc in self.processes:
			proc.relaunch_if_needed(self.autorestart, self.exitcodes,
					self.startretries, self.starttime)

	def kill(self):
		for proc in self.processes:
			proc.kill(self.stopsignal)
