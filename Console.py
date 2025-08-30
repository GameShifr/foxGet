C = False
try: 
	from colorama import Fore
	C = True

except: print("Warning: colorama didn't installed")

statictxt = ""

def staticprint(text: str):
	global statictxt
	statictxt = text
	print("\r"+statictxt, end='\r')


def cprint(text: str, style: str| None=""):
	"""w - yellow | e - red"""
	c = ""
	s = ""
	for i in range(max(len(statictxt), len(text))):
		if (i < len(text)):
			if (text[i] == '\t'): s += "    "
			else: s += text[i]
		else: s += ' '
	if (style == "w"): c = Fore.YELLOW
	elif (style == "e"): c = Fore.RED
	print(c+text+Fore.RESET)
	if (statictxt != ""): print(statictxt, end='\r')

def cinput(text: str, erase_statictxt=False, estring="") -> str:
	if erase_statictxt:
		s = ""
		for i in range(len(statictxt)):
			if (i < len(estring)): s += estring[i]
			else: s += ' '
		print(s)
	return input(text)