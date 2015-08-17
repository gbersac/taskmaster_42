from enum import Enum

class AutoRestartEnum(Enum):
	def fromstr(s):
		if type(s) is AutoRestartEnum:
			return s
		if s == "never":
			return AutoRestartEnum.never
		if s == "unexpected":
			return AutoRestartEnum.unexpected
		if s == "always":
			return AutoRestartEnum.always

	never = 0
	unexpected = 1
	always = 2
