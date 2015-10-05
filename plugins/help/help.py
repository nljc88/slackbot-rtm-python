import time
import itertools
from collections import OrderedDict

crontable = []
outputs = []

title = 'You can use the following commands in any channel HAL is in:'
commands = 'Or try "hal commands" for a list of my commands'
end = 'enjoy!'

hlist = [
  '!playernews  <playername>',
  '!playerstats  <playername>',
  '!statyear  <playername> : <year>',
  '!yt  <keyword>',
  '!yt-list  <keyword>',
  '!weather  <city>',
  '!weather-current  <city>',
  '!weather-forecast	 <city>',
  '!weather-10day  <city>'
  ]

def process_message(data):
	channel = data["channel"]
	text = data["text"]
	string = text.lower()
	alist = string.split(' ')
	if alist[0] == '!help':
		time.sleep(1)
		string = '\n'.join(hlist)
		outputs.append([channel, "%s \n\n%s \n\n%s \n%s" % (title, string, commands, end)])