import yaml
import sys
from .program import Program

def parse_yaml_file(f, file_name):
	try:
		parse_conf_file = yaml.load(f)
		return parse_conf_file
	except Exception as e:
		print("Can't parse file {0} because :\n{1}"
				.format(file_name, e))

def load_one_conf_files(file_name):
	try:
		f = open(file_name, 'r')
		parse_conf_file = parse_yaml_file(f, file_name)
		if not parse_conf_file:
			return False
		progs = []
		for k, v in parse_conf_file.items():
			try:
				prog = Program(k, v)
				progs.append(prog)
			except Exception as e:
				print("Program error {0}".format(e))
		return progs
	except IOError as e:
		print("Impossible to open file {0} because {1}"
				.format(file_name, e.strerror))
	return False

def load_conf_files():
	args = sys.argv[1:]
	if len(args) < 1:
		print("Usage ./taskmaster conf_file.yaml")
		exit(os.EX_OK)
	progs = []
	for file_name in args:
		nprogs = load_one_conf_files(file_name)
		if nprogs:
			progs = progs + nprogs
	return progs

class NoProgError(Exception):
	"""Error raise when a program is expected and none can be found"""

	def __init__(self, name):
		self.name = name

	def __str__(self):
		return 'the program ' + self.name + ' does not exist'

class ProgramLst:
	"""List of all the programs managed by one taskmaster"""

	lst = []

	def __init__(self):
		self.lst = load_conf_files()

	"""Function to launch all the programs of the list at the beginning."""
	def launch(self):
		for prog in self.lst:
			if prog.autostart:
				prog.execute()

	"""Check the state of all the programs"""
	def check(self):
		for prog in self.lst:
			prog.relaunch_if_needed()

	def kill_all(self):
		for prog in self.lst:
			prog.kill()

	def print_status(self):
		for prog in self.lst:
			print(prog.name, " : ", prog.get_status())
			# "{0}: {1}". format(prog.name, prog.get_status())

	def get_by_name(self, prog_name):
		for prog in self.lst:
			if prog.name == prog_name:
				return prog
		raise NoProgError(prog_name)
