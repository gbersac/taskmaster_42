from .program import Program

class ProgramLst:
	"""List of all the programs managed by one taskmaster"""

	lst = []

	def __init__(self, _lst):
		self.lst = _lst

	"""Function to launch all the programs of the list at the beginning."""
	def launch(self):
		for prog in self.lst:
			if prog.autostart:
				prog.execute()
