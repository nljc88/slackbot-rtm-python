
import sys, random, time, re

crontable = []
outputs = []

zombie_list = [
  "http://24.media.tumblr.com/tumblr_m35jnyjTco1qikhvso1_100.gif",
  "http://www.netanimations.net/head2.gif",
  "http://www.netanimations.net/Animated-Zombie-Reverse.gif",
  "http://www.freewebs.com/echoeyy/zombie%20getting%20shot.gif",
  "https://i.chzbgr.com/maxW500/6360720640/h487AE90F/",
  "https://i.chzbgr.com/maxW500/5912815872/h8AB29CB2/",
  "https://i.chzbgr.com/maxW500/5299680512/h5120FD0B/"
  ]

def get_zombie():
	x = random.randint(0,6)
	zombie = zombie_list[x]
	return zombie


def process_message(data):
	channel = data["channel"]
	text = data["text"]
	string = text.lower()
	if re.search('zombi(es|e)', text):
		time.sleep(1)
		zombie = get_zombie()
		outputs.append([channel, zombie])