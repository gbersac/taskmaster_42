from program.process_status_enum import ProcessStatusEnum

def execute(progs, prog_name):
	if progs == None or prog_name == None:
		return
	try:
		prog = progs.get_by_name(prog_name)
		if prog.nb_proc_status(ProcessStatusEnum.RUNNING) == 0:
			print("This program is not running.")
			return
		prog.kill()
	except Exception as e:
		print("Can't stop program : ", e)
