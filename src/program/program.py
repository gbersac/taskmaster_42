import os

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
	autorestart = False
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
	stdout = False
	"""Options to discard the program’s stderr or to redirect them to files"""
	stderr = False
	""" An umask to set before launching the program"""
	umask = 0o22

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
