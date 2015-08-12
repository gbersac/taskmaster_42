from .command import Command
import command.command_list

class CmdHelp(Command):
	name = "help"
	help_strg = "Describe all the commands of the file."

	"""The help command display a description of all the commands"""
	def __init__(self):
		super(CmdHelp, self).__init__()

	def execute(self, sp):
		for cmd in command.command_list.cmd_list:
			cmd.print_help()
