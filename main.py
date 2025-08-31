import requests
import os
from Console import cprint, staticprint, cinput
import argparse

parser = argparse.ArgumentParser(description="Загрузить видео из вебинара foxford")
parser.add_argument("-d", "--del_all", action="store_true", help="delete all files except the output file")
parser.add_argument("-s", "--save", action="store_true", help="save existed files in dir")
parser.add_argument("lesson", type=str, help="The lesson code")
parser.add_argument("pstfix", type=str, help="Postfix string in file name")
args = parser.parse_args()

# href lesson [vst/ast] [n] ps
href = "https://apps.foxford.ru/webinar-foxford/storage/api/v2/backends/yandex/sets/hls.webinar.foxford.ru::"
lesson = args.lesson
vst = "/objects/long.video.720p."
ast = "/objects/long.audio.32kbps."
ps = args.pstfix
ps = f".{ps}.ts"

bearer = ""
code = None
r = None
exfiles = []

try: os.mkdir(lesson)
except FileExistsError:
	exfiles = os.listdir(lesson)
	if not(args.save):
		cprint("Dir is already existed. Recreating", style="w")
		for i in range(len(exfiles)):
			os.remove(lesson+"/"+exfiles[i])
			cprint(f"{exfiles[i]} deleted!")
		exfiles = []
	else: cprint("Dir is already existed.", style="w")

st = ast
mvi = '?'

for tp in ["audio", "video"]:
	vi = 0
	if (tp == 'video'):
		st = vst
	while True:
		vi += 1
		staticprint(f"{vi}/{mvi}")
		if (args.save) and (len(exfiles) < 3) and (len(exfiles) > 0): #fs
			cprint("Deleting last ex-files in dir...")
			for i in range(len(exfiles)):
				os.remove(lesson+"/"+exfiles[i])
				cprint(f"    {exfiles[i]} deleted!")
			exfiles = []
		if (args.save) and (f"{tp}.{vi}.ts" in exfiles):
			cprint(f"file {tp}.{vi}.ts already existed. Continuing...")
			exfiles.remove(f"{tp}.{vi}.ts")
			continue

		url = href+lesson+st+str(vi)+ps
		cprint(f"requesting {url}")
		ec = 0
		while True:
			headers = {'authorization': f'Bearer {bearer}'}
			r0 = requests.get(url, headers=headers) #try
			code0 = r0.status_code
			r1 = requests.get(url, headers=headers)
			code1 = r1.status_code
			r = requests.get(url, headers=headers)
			code = r.status_code

			if not(code == code0 == code1) or (code == 401):
				bearer = cinput("Bearer? ", True)
				continue
			elif not(r0.content == r1.content == r.content):
				if (code == 200):
					cprint("    Error: loss some data. Trying again...", style="w")
					continue
				else: cprint("    N: data mismatch in non-200 code", style="w")
			break

		if (code == 404):
			cprint("    404 status code. Finishing the loop...", style="w")
			break
		if (code != 200): 
			cinput("", True, f"    Error with code {code}")
			exit()

		cprint("    -response received successfully!")

		with open(f"{lesson}/{tp}.{vi}.ts", 'wb') as f:
			f.write(r.content)
		cprint(f'    -file "{tp}.{vi}.ts" is written!')

	staticprint("")
	with open(f"{lesson}/{tp}.txt", 'w') as f:
		for i in range(1, vi):
			f.write(f"file '{tp}.{i}.ts'\n")
	cprint(f"list of {tp} files has been created! Total:{vi-1}")
	mvi = str(vi-1)

t = []
if (args.del_all):
	t = ["del audio.txt\n", "del video.txt\n"]
	for i in ["video", "audio"]:
		for j in range(1, vi):
			t.append(f"del {i}.{j}.ts\n")
with open(f"{lesson}/script.bat", "w") as f:
	f.writelines(["ffmpeg -f concat -i video.txt -c copy video.ts\n",
							 "ffmpeg -f concat -i audio.txt -c copy audio.ts\n",
							 "ffmpeg -i video.ts -i audio.ts -c:v copy -c:a copy _output.mp4\n",
							 "del video.ts\n",
							 "del audio.ts\n"]+t)
cprint("Bat file has been created!")
t = ""
while (t != 'y') and (t != 'n'):
	t = cinput("Bat autostart? [y/n] ")
if (t == 'y'):
	cprint("Bat output:")
	os.chdir(lesson)
	os.system("script.bat")

cprint("done!")
cinput("Press Enter key...")
