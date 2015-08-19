#!/nfs/zfs-student-3/users/2013/gbersac/.brew/bin/python3

import signal

def signal_handler(sig, frame):
	if sig == signal.SIGINT:
		print("SIGINT")
	if sig == signal.SIGUSR1:
		print("SIGUSR1")
	if sig == signal.SIGQUIT:
		print("SIGQUIT")

if __name__ == '__main__':
	signal.signal(signal.SIGINT, signal_handler)
	signal.signal(signal.SIGQUIT, signal_handler)

	while True:
		pass
