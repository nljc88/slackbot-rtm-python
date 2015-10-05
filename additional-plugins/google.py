#
# Instructions for setting up google dev for your custom search API
# http://scriptsonscripts.blogspot.com/2015/02/python-google-search-api-requests.html
#
# python code you can reference for your plugin
# https://code.google.com/p/google-api-python-client/source/browse/#hg%2Fsamples%2Fcustomsearch

import json, sys, time, itertools
from apiclient.discovery import build
from collections import OrderedDict

crontable = []
outputs = []

search_engine_id = '<your search engine ID>'
api_key = '<your API key>'

def build_keyword_search(arg):
	keywords = ' '.join(arg)
	return keywords

def build_service():
	service = build("customsearch", "v1", developerKey=api_key)
	return service

# ar1 = service, arg2 is user keywords to search
def get_data(arg1, arg2):
	results = arg1.cse().list(
		q=arg2,
		num=5,
      	cx=search_engine_id,).execute()
	return results #cant .content because its  a dict(json), not a string or html

def make_json(arg3):
	json_data = json.dumps(arg3, sort_keys=True, indent=2) #.content)
	return json_data

def filter_json(arg4):
	title_list = []
	snippet_list = []
	link_list = []
	for d in arg4['items']:
		title_list.append(d['title'])
		snippet_list.append(d['snippet'])
		link_list.append(d['link'])
	length = len(title_list)
	newlist = []
	for x in range(0, length):
		a = snippet_list[x]
		b = link_list[x]
		string_val = "%s %s" %(a,b)
		newlist.append(string_val.encode('ascii', 'ignore').decode('ascii')) #that fixed it#encode("utf-8"))
	gdict = OrderedDict(itertools.izip(title_list, newlist))
	return gdict

#caller
def process_message(data):
	channel = data["channel"]
	text = data["text"]
	text = text.lower()
	w_list = text.split(" ")
	if w_list[0] == 'hal' and w_list[1] == 'google':
		time.sleep(1)
		string = str(text)
		alist = string.split(" ")
		call1 = alist.index('hal')
		del alist[call1]
		call2 = alist.index('google')
		del alist[call2]
		keywords = build_keyword_search(alist)
		service = build_service()
		results = get_data(service, keywords)
		gdict = filter_json(results)
		for k,v in gdict.items():
			outputs.append([channel, "{}: {}".format(k,v)])


