
import sys, random, time

crontable = []
outputs = []

sexysaxman = 'http://sexysaxmansaxagrams.ytmnd.com/'

def process_message(data):
	channel = data["channel"]
	text = data["text"]
	string = text.lower()
	alist = string.split(' ')
	if alist[0] == 'hal' and alist[1] == 'sexysaxman':
		time.sleep(1)
		outputs.append([channel, sexysaxman])