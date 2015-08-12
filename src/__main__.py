import yaml
import sys

import command.command_list

def execute_command(s):
	sp = s.split(' ')
	for cmd in command.command_list.cmd_list:
		if cmd.is_command(sp):
			cmd.execute(sp)
			return
	print("No command named " + sp[0])


if __name__ == '__main__':
	while True:
	    s = input("taskmaster>>> ")
	    execute_command(s)
	    sys.stdout.flush()
