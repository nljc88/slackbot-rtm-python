
import sys, random, time

crontable = []
outputs = []

carltons = [
  "http://media.tumblr.com/tumblr_lrzrlymUZA1qbliwr.gif",
  "http://web.archive.org/web/20121119111926/http://3deadmonkeys.com/gallery3/var/albums/random_stuff/Carlton-Dance-GIF.gif",
  "http://gifsoup.com/webroot/animatedgifs/987761_o.gif",
  "http://s2.favim.com/orig/28/carlton-banks-dance-Favim.com-239179.gif",
  "http://gifsoup.com/webroot/animatedgifs/131815_o.gif"
]

def get_carlton():
	x = random.randint(0,4)
	carlton = carltons[x]
	return carlton

def process_message(data):
	channel = data["channel"]
	text = data["text"]
	string = text.lower()
	alist = string.split(' ')
	if alist[0] == 'hal' and alist[1] == 'carlton':
		time.sleep(1)
		carlton = get_carlton()
		outputs.append([channel, carlton])