import datetime

LOG_PATH = "./log.txt"

def log(s):
	f = open(LOG_PATH, "a")
	f.write("[" + str(datetime.datetime.now()) + "] " + s + "\n")
	f.close()
