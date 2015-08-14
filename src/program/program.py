import os
from enum import Enum
import shlex, subprocess

class AutoRestartEnum(Enum):
	def fromstr(s):
		if s == "never":
			return AutoRestartEnum.never
		if s == "unexpected":
			return AutoRestartEnum.unexpected
		if s == "always":
			return AutoRestartEnum.always

	never = 0
	unexpected = 1
	always = 2


class ProgramWithoutCmdError(Exception):
    def __init__(self, _name):
        self.name = _name

    def __str__(self):
        return 'program ' + self.name + ' has no cmd attribute'

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
	starttime = 1
	"""How many times a restart should be attempted before aborting"""
	startretries = 0
	"""Which signal should be used to stop (i.e. exit gracefully) the program"""
	stopsignal = "STOP"
	"""How long to wait after a graceful stop before killing the program"""
	stoptime = 1

	"""The command to use to launch the program"""
	cmd = False
	"""A working directory to set before launching the program"""
	workingdir = False
	"""Options to discard the program’s stdout or to redirect them to files"""
	stdout = None
	"""Options to discard the program’s stderr or to redirect them to files"""
	stderr = None
	""" An umask to set before launching the program"""
	umask = 0o22

	"""
	The processes objects.
	https://docs.python.org/2/library/subprocess.html#popen-objects
	"""
	popen = None

	def open_standard_files(self, file_name):
		if file_name == None:
			return
		try:
			fd = open(file_name, "a")
			return fd
		except Exception as e:
			print("Stantard file for {0} can't be open because {1}.".
					format(self.name, e))
			return None

	def __init__(self, _name, dico):
		"""
		dico parsed from the yaml conf file.
		The first entry is program name : {list of parameters}
		The dico must contain, at least the cmd attribute
		"""
		self.name = _name
		for k, v in dico.items():
			setattr(self, k, v)
		if not self.cmd:
			raise ProgramWithoutCmdError(_name)
			return
		self.cmd = shlex.split(self.cmd)
		self.autorestart = AutoRestartEnum.fromstr(self.autorestart)

	def execute(self):
		try:
			stdoutf = self.open_standard_files(self.stdout)
			stderrf = self.open_standard_files(self.stderr)
			self.popen = subprocess.Popen(self.cmd,
					stdout = stdoutf, stderr = stderrf)
		except Exception as e:
			print("Can't launch program {0} because {1}.".
					format(self.name, e))

	def return_code_is_allowed(self, ec):
		if not isinstance(self.exitcodes, basestring):
			return ec == self.exitcodes
		for rc in exitcodes:
			if ec == rc:
				return True
		return False

	def relaunch(self):
		self.execute()

	def relaunch_if_needed(self):
		if not self.popen:
			return
		rc = self.popen.poll()
		if rc and not self.autorestart == AutoRestartEnum.never:
			if self.autorestart == AutoRestartEnum.unexpected and \
					not self.return_code_is_allowed(rc):
				return
			self.relaunch()

	def kill(self):
		if self.popen:
			self.popen.terminate()
			self.popen.kill()
