import logger

def execute(progs, prog_name):
	if progs == None or prog_name == None:
		return
	try:
		prog = progs.get_by_name(prog_name)
		prog.kill()
		prog.execute()
		logger.log("restart prog " + prog_name)
	except Exception as e:
		print("Can't start program : ", e)
