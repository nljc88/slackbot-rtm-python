
import sys
import requests
from bs4 import BeautifulSoup
import time
import itertools
import collections

crontable = []
outputs = []


def yt_query(arg1):
	string_arg = str(arg1)
	string_arg = string_arg.replace('[',"").replace(']',"").replace(',',"").replace(' ','+').replace("'","")
	return string_arg
	
def build_url(arg2):
	refined_url = ""
	base_url = "https://www.youtube.com/results?search_query=%s"
	refined_url = base_url % arg2
	return refined_url
	
def get_data(arg3):
	results = ""
	results = requests.get(arg3)
	return results.content

def find_video(arg4):
	soup = BeautifulSoup(arg4, 'html.parser')
	section_data = soup.find('div', {'id': 'results'})
	item_data = section_data.find('ol', {'class': 'item-section'})
	href_link = []
	for hr in item_data.find_all('a', {'class': 'yt-uix-sessionlink yt-uix-tile-link yt-ui-ellipsis yt-ui-ellipsis-2 spf-link '}, href=True, limit=1):
		z = hr['href']
		href_link.append(z.encode("utf-8"))
	href_string = str(href_link)
	video = href_string.replace('/',"https://www.youtube.com/").replace('[',"").replace(']',"").replace("'","") #.replace('u',"")
	return video


def find_video_list(arg5):
	soup = BeautifulSoup(arg5, 'html.parser')
	section_data = soup.find('div', {'id': 'results'})
	item_data = section_data.find('ol', {'class': 'item-section'})
	
	titles = []
	for t in item_data.find_all('a', {'class': 'yt-uix-sessionlink yt-uix-tile-link yt-ui-ellipsis yt-ui-ellipsis-2 spf-link '}, title=True, limit=5):
		y =  t['title']
		titles.append(y)
	
	hrefs = []
	for h in item_data.find_all('a', {'class': 'yt-uix-sessionlink yt-uix-tile-link yt-ui-ellipsis yt-ui-ellipsis-2 spf-link '}, href=True, limit=5):
		x =  h['href']
		hrefs.append(x)
	hstring = str(hrefs)
	new_hstring = hstring.replace('/',"https://www.youtube.com/").replace('[',"").replace(']',"").replace("'","").replace(' ','') #.replace('u',"")
	videos = new_hstring.split(',')
	return titles, videos	
	
	
#caller
def process_message(data):
    channel = data["channel"]
    text = data["text"]
    t_list = text.split(" ")
    if t_list[0] == '!yt':
    	time.sleep(1)
    	string = str(text)
    	alist = string.split(" ")
    	call = alist.index('!yt')
    	del alist[call]
    	query = yt_query(alist)
    	refined_url = build_url(query)
    	results = get_data(refined_url)
    	video = find_video(results)
    	outputs.append([channel, video])
    elif t_list[0] == '!yt-list':
    	time.sleep(1)
    	string = str(text)
    	blist = string.split(" ")
    	call = blist.index('!yt-list')
    	del blist[call]
    	query = yt_query(blist)
    	refined_url = build_url(query)
    	results = get_data(refined_url)
    	vars = find_video_list(results)
    	title = vars[0]
    	videos = vars[1]
    	cdict = collections.OrderedDict(itertools.izip(title,videos))
    	for k,v in cdict.items():
    		outputs.append([channel, "{}: \n{}\n".format(k,v)])

	

