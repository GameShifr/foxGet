import requests
import os
from Console import cprint, staticprint, cinput

# href lesson [vst/ast] [n] ps
href = "https://apps.foxford.ru/webinar-foxford/storage/api/v2/backends/yandex/sets/hls.webinar.foxford.ru::"
lesson = cinput("Lesson: ")
vst = "/objects/long.video.720p."
ast = "/objects/long.audio.32kbps."
ps = cinput("pstfix: ")
ps = f".{ps}.ts"

bearer = ""
code = None
r = None

try: os.mkdir(lesson)
except FileExistsError:
	cprint("Dir is already existed. Recreating")
	m = os.listdir(lesson)
	for i in range(len(m)):
		os.remove(lesson+"/"+m[i])
		cprint(f"{m[i]} deleted!")

st = ast
mvi = '?'

for tp in ["audio", "video"]:
	vi = 0
	if (tp == 'video'):
		st = vst
	while True:
		vi += 1
		staticprint(f"{vi}/{mvi}")
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
					cprint("    Error: loss some data. Trying again...")
					continue
				else: cprint("    N: data mismatch in non-200 code")
			break

		if (code == 404):
			cprint("    404 status code. Finishing the loop...")
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

with open(f"{lesson}/script.bat", "w") as f:
	f.writelines(["ffmpeg -f concat -i video.txt -c copy video.ts\n",
							 "ffmpeg -f concat -i audio.txt -c copy audio.ts\n",
							 "ffmpeg -i video.ts -i audio.ts -c:v copy -c:a copy _output.mp4\n",
							 "del video.ts\n",
							 "del audio.ts"])
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
