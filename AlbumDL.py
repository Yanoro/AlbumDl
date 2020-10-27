from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import sys,time,re,os


if (len(sys.argv) != 3):
	print("[*] {} URL PlaylistName".format(sys.argv[0]))
	sys.exit(1)

url = sys.argv[1]
playlist = sys.argv[2]

driver = webdriver.Firefox()
driver.get(url)
forms = driver.find_elements_by_tag_name("paper-button")

for form in forms:
	if (form.get_attribute("id") == "more"):
		form.click()


time.sleep(13) #Fix Ads blocking getting the last timestamp later
#The script still doens't click on the play button automaticly
LastStamp = driver.find_element_by_class_name("ytp-time-duration").text
description = driver.find_element_by_id("description").text
artist = driver.find_element_by_id("channel-name").find_element_by_tag_name("a").text


entrys = re.findall(r'\d{0,2}:?\d{1,2}:\d{2} .*', description)
entrys.append(LastStamp)

driver.quit()

for i in range(0, len(entrys) - 1):
		entrys[i] = entrys[i].split(' ', 1)

		entrys[i].insert(1, entrys[i + 1].split(' ', 1)[0]) 

		entrys[i] = ' '.join(entrys[i])
		print(entrys[i])

del entrys[-1]

MusicPath = "/home/egoist/Music/"
AlbumPath = MusicPath + playlist + "/AlbumFile"
PlaylistPath = "/home/egoist/.mpd/playlists/"
ext = ".opus"
PlaylistFile = PlaylistPath + playlist + ".m3u"

os.system('mkdir {}'.format(MusicPath + playlist))
os.system('touch {}'.format(PlaylistFile))
os.system('youtube-dl -x -o "{}.opus" -f bestaudio/best "{}"'.format(AlbumPath, url))

for entry in entrys:
	Start = entry.split(' ', 1)[0]
	End = entry.split(' ', 2)[1]
	Song = entry.split(' ', 2)[2]
	print("[*] Song: {} - {}  {}".format(Start, End, Song))
	os.system('ffmpeg -i "{}.opus" -metadata "Title"="{}" -metadata "Artist"="{}" -acodec copy -ss "{}" -to "{}" "{}"'.format(AlbumPath, Song, artist, Start, End, MusicPath + playlist + "/" + Song + ext))
	os.system('echo "{}/{}{}" >> "{}"'.format(playlist, Song, ext, PlaylistFile))
