import curses
import os
import yaml
import sys
import select
import shlex
import signal

import command.command_list
from program.program import Program
from program.program_lst import ProgramLst

progs = []

def execute_command(s, progs):
	if not s.rstrip():
		return
	sp = shlex.split(s)
	for cmd in command.command_list.cmd_list:
		if cmd.is_command(sp):
			cmd.execute(sp, progs)
			return
	print("No command named " + sp[0])


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
		progs = progs + load_one_conf_files(file_name)
	return ProgramLst(progs)

def print_command_prompt():
	sys.stdout.write("taskmaster>>> ")
	sys.stdout.flush()

def signal_handler(signal, frame):
	if type(progs) == ProgramLst:
		execute_command("exit", progs)

if __name__ == '__main__':
	signal.signal(signal.SIGINT, signal_handler)
	progs = load_conf_files()
	progs.launch()

	# Reading the stdin
	print_command_prompt()
	while True:
		ready = select.select([sys.stdin], [], [], 0.1)[0]
		if not ready:
			progs.check()
		else:
			for file in ready:
				line = file.readline()
				if line:
					execute_command(line, progs)
					print_command_prompt()
