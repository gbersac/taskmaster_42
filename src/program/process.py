import subprocess
import os.path

from .auto_restart_enum import AutoRestartEnum

class Process:
	"""
	A process is a running instance of a program

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
		except Exception as e:
			print("Can't launch process {0} because {1}.".
					format(self.name, e))

	def return_code_is_allowed(self, rc, exitcodes):
		if not isinstance(exitcodes, basestring):
			return rc == exitcodes
		for rc in exitcodes:
			if rc == rc:
				return True
		return False

	def relaunch_if_needed(self, autorestart, exitcodes, startretries):
		"""Require that set_execution_vars has already been called"""
		if not self.popen:
			return False
		rc = self.popen.poll()
		if rc:
			if self.nb_start_retries > startretries:
				return
			if autorestart == AutoRestartEnum.unexpected and \
					not self.return_code_is_allowed(rc, exitcodes):
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

	def kill(self):
		if self.popen and not self.popen.poll():
			if Process.check_pid_is_alive(self.popen.pid):
				self.popen.terminate()
				self.popen.kill()
