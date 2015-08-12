class Command:
	"""The is the parent class of every command supported by this program"""

	name = "cmd"
	help_strg = "No help"

	def __init__(self):
		pass

	"""
	This function return true if the string correspond to this command.

	strg: the splitted command line.
	"""
	def is_command(self, strg):
		if strg[0] != self.name:
			return False
		return True

	"""
	Execute the command.

	strg: the splitted command line.
	"""
	def execute(self, sp):
		raise NotImplementedError("Subclass must implement abstract method")

	def print_help(self):
		print(self.name + ": " + self.help_strg)

