import sys
from bs4 import BeautifulSoup
import requests
import time
import itertools
import collections

crontable = []
outputs = []

def playername_statsyear(args):
	if ':' in args:
		x = args.index(":")
		del args[x]
		if len(args) == 2:
			player_name_string = args[0]
			year = args[1]
			return player_name_string, year
		elif len(args) == 3:
			name_a = args[0]
			name_b = args[1]
			year = args[2]
			if name_a[len(name_a)-1] == ",":
				player_name_string = name_a + "%20" + name_b
			else:
				player_name_string = name_b + ",%20" + name_a
			return player_name_string, year
	elif len(args) == 1:
		string_arg = args[0]
		if ':' in string_arg:
			string = string_arg.split(':')
			player_name_string = string[0]
			year = string[1]
			return player_name_string, year
	elif len(args) == 2:
		if ':' in args[-1]:
			string_arg = args.pop()
			string = string_arg.split(':')
		list = args + string
		if len(list) == 3:
			name_a = list[0]
			name_b = list[1]
			year = list[2]
			if name_a[len(name_a)-1] == ",":
				player_name_string = name_a + "%20" + name_b
			else:
				player_name_string = name_b + ",%20" + name_a
			return player_name_string, year
	else:
		print "check name formatting"

#define function to create URL based on what end of url string is needed
def build_url(arg1):
	refined_url = ""
	base_url = "http://www.rotoworld.com/content/playersearch.aspx?searchname=%s&sport=nhl"
	refined_url = base_url % arg1
	return refined_url

#define the process of making the request and returning data
def get_data(arg2):
	results = ""
	results = requests.get(arg2)
	return results.content

def find_statsyear(arg3):
	soup = BeautifulSoup(arg3, 'html.parser')
	bs_data = soup.find_all('table', {'class': 'statstable'})[1]
	return bs_data

#caller
def process_message(data):
    channel = data["channel"]
    text = data["text"]
    if '!statyear' in text:
    	time.sleep(1)
    	string = str(text)
    	alist = string.split(" ")
    	call = alist.index('!statyear')
    	del alist[call]
    	var1 = playername_statsyear(alist)
    	player_name_string = var1[0]
    	year = var1[1]
    	refined_url = build_url(player_name_string)
    	results = get_data(refined_url)
    	if '<h3>Search Results for:' in results:
    		outputs.append([channel, 'DERP!\nplayername spelled incorectly or mutiple players by that name\ntry again'])
    	else:
    		bs_data = find_statsyear(results)
    		header_list = []
    		column_names = bs_data.find('tr', {'class': 'columnnames'}).find_all('td')
    		for cols in column_names:
    			z = cols.get_text()
    			header_list.append(z)
    		table = []
    		trs = bs_data.find_all('tr')
    		for tr in trs:
    			tr_list = []
    			tds = tr.find_all('td')
    			for td in tds:
    				x = td.get_text()
    				tr_list.append(x)
    			table.append(tr_list)
    		for y in table:
    			if year in y:
    				stat_line = y
    		bdict = collections.OrderedDict(itertools.izip(header_list,stat_line))
    		for k,v in bdict.items():
    			outputs.append([channel, "{}: {}".format(k,v)])
