
statictxt = ""

def staticprint(text: str):
	global statictxt
	statictxt = text
	print(statictxt, end='\r')


def cprint(text: str):
	s = ""
	for i in range(max(len(statictxt), len(text))):
		if (i < len(text)): s += text[i]
		else: s += ' '
	print(text)
	if (statictxt != ""): print(statictxt, end='\r')

def cinput(text: str, erase_statictxt=False, estring="") -> str:
	if erase_statictxt:
		s = ""
		for i in range(len(statictxt)):
			if (i < len(estring)): s += estring[i]
			else: s += ' '
		print(s)
	return input(text)