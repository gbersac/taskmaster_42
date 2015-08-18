import logger
from program.program import Program
from program.program_lst import ProgramLst

def execute(old_progs):
	logger.log("taskmaster reloaded")
	new_progs = ProgramLst()
	for oprog in old_progs.lst:
		for nprog in new_progs.lst:
			# only program which we care about processes should be keep
			if oprog.name == nprog.name:
				oprog.keep_running_process(nprog)
				break

	# now all the progs are in new_progs
	new_progs.reload()
	return new_progs

