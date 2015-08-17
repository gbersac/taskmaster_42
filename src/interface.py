import curses
import os
from os import system

COMMAND_PROMPT = "taskmaster>>> "

class Interface:
	"""This is the interface between the user and the program in curses"""
	has_changed = True
	history = []
	"""Id of the history on which the user is working"""
	cmd_id = -1

	def __init__(self):
		self.screen = curses.initscr()
		curses.echo()

	def user_input(self):
		while True:
			c = self.screen.getch()
			if c == -1:
				break
			if c == curses.KEY_UP:
				cmd_id -= 1
			if c == curses.KEY_DOWN:
				cmd_id += 1

	def get_prompt(self):
		if history[cmd_id] != None:
			return COMMAND_PROMPT + history[cmd_id]
		return COMMAND_PROMPT

	def refresh(self):
		# if True:
		self.user_input()
		if self.has_changed:
			(self.height, self.width) = self.screen.getmaxyx()
			self.screen.border(0)
			self.screen.clear()
			print(get_prompt)
			self.screen.addstr(self.height - 2, 2, get_prompt())
			self.screen.refresh()
			self.has_changed = False

	def quit(self):
		curses.endwin()
