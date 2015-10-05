import sys
from bs4 import BeautifulSoup
import requests
import time

crontable = []
outputs = []



# create format for playername to append to url
def player_name(arguments):
	player_name_string = ""
	if len(arguments) == 2:
		player_name_string = arguments[1]
		return player_name_string
	else:
		name_a = arguments[1]
		name_b = arguments[2]
		if name_a[len(name_a)-1] == ",":
			player_name_string = name_a + "%20" + name_b
		else:
			player_name_string = name_b + ",%20" + name_a
		return player_name_string

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

#format returned data and search for latest news
def find_news(arg3):
	soup = BeautifulSoup(arg3, 'html.parser')
	news = soup.find('div', {'class': 'playernews'})
	return news


def process_message(data):
    channel = data["channel"]
    text = data["text"]
    if '!playernews' in text:
    	time.sleep(1)
    	string = str(text)
    	args = string.split(" ")
    	player_name_string = player_name(args)
    	refined_url = build_url(player_name_string)
    	results = get_data(refined_url)
    	if '<h3>Search Results for:' in results:
    		outputs.append([channel, 'DERP!\nplayername spelled incorectly or mutiple players by that name\ntry again'])
    	else:
    		news = find_news(results)
    		outputs.append([channel, news.text])
        
