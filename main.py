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
		staticprint(f'{i+1}/{len(m)} files deleted')
		os.remove(lesson+"/"+m[i])
		cprint(f"{m[i]} deleted!")
	staticprint("")

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
		while True:
			headers = {'authorization': f'Bearer {bearer}'}
			r = requests.get(url, headers=headers)
			code = r.status_code
			if (code != 401): break
			bearer = cinput("Bearer? ", True)

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
