import types
import subprocess
import os.path
import signal
import datetime

from .auto_restart_enum import AutoRestartEnum
from .process_status_enum import ProcessStatusEnum

class Process:
	"""
	A process is an instance of a program.

	This is a wrapper over a python popen object :
	https://docs.python.org/2/library/subprocess.html#popen-objects
	"""
	popen = None

	def __init__(self, name, cmd):
		self.cmd = cmd
		self.name = name
		self.nb_start_retries = 0

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

	def set_execution_vars(self, stdout, stderr, nenv, workingdir, umask):
		self.stdout = stdout
		self.stderr = stderr
		self.env = nenv
		self.workingdir = workingdir
		self.umask = umask

	def execute(self):
		"""Require that set_execution_vars has already been called"""
		self.nb_start_retries += 1
		try:
			stdoutf = self.open_standard_files(self.stdout)
			stderrf = self.open_standard_files(self.stderr)
			self.cmd = self.umask + self.cmd
			self.popen = subprocess.Popen(self.cmd,
					stdout = stdoutf, stderr = stderrf,
					env = self.env, shell = True, cwd = self.workingdir)
			self.starttime = datetime.datetime.now()
			self.closetime = None
		except Exception as e:
			print("Can't launch process {0} because {1}.".
					format(self.name, e))

	def return_code_is_allowed(self, rc, exitcodes):
		# if exitcodes is only one code
		if not type(exitcodes) is list:
			return rc == exitcodes
		# if exitcodes is a list of exitcode
		for rc in exitcodes:
			if rc == rc:
				return True
		return False

	def lived_enough(self, starttime):
		"""Return true if the progs lifetime was too short."""
		# The program wasn't started/killed at all
		if not hasattr(self, "starttime") or not hasattr(self, "closetime") \
 				or not starttime:
			return False
		# Test program lifetime
		td = datetime.timedelta(seconds = starttime)
		if (self.closetime - self.starttime) >= td:
			return True
		return False

	def relaunch_if_needed(self, autorestart, exitcodes, startretries, starttime):
		"""Require that set_execution_vars has already been called"""
		if not self.popen:
			return False
		# if program returned
		if self.popen.poll() != None:
			if not hasattr(self, "closetime") or not self.closetime:
				self.closetime = datetime.datetime.now()
			if self.nb_start_retries > startretries:
				return False
			if autorestart == AutoRestartEnum.unexpected and \
					self.return_code_is_allowed(self.popen.poll(), exitcodes) and \
					self.lived_enough(starttime):
				return False
			self.execute()
			return True
		return False

	def check_pid_is_alive(pid):
		try:
			os.kill(pid, 0)
		except OSError:
			return False
		else:
			return True

	def print_signal(stopsignal):
		if stopsignal == signal.SIGINT:
			return "SIGINT"
		if stopsignal == signal.SIGUSR1:
			return "SIGUSR1"
		if stopsignal == signal.SIGQUIT:
			return "SIGQUIT"

	def kill(self, stopsignal):
		if self.popen and not self.popen.poll():
			if Process.check_pid_is_alive(self.popen.pid):
				# print("signal ", Process.print_signal(stopsignal))
				os.kill(self.popen.pid, stopsignal)
				if not Process.check_pid_is_alive(self.popen.pid):
					self.closetime = datetime.datetime.now()

	def get_status(self, exitcodes):
		if not self.popen:
			return ProcessStatusEnum.NOT_LAUNCH
		if self.popen.poll() == None:
			return ProcessStatusEnum.RUNNING
		if self.return_code_is_allowed(self.popen.poll(), exitcodes):
			return ProcessStatusEnum.STOP_OK
		else:
			return ProcessStatusEnum.STOP_KO
