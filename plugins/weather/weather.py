
import sys
import requests
import json
import time
import datetime
import itertools
from collections import OrderedDict

APIKEY = '<insert api key if needed>'

crontable = []
outputs = []

FILE="plugins/weather/city_id"

def get_city(arg1):
	strcity = ' '.join(arg1)
	city = strcity.lower()
	return city

def get_cityID(arg2):
	searchfile = open(FILE, 'r')
	cities = []
	for line in searchfile:
		line = line.replace('[',"").replace(']',"").replace('\n','').replace("u'",'').replace("'","")
		newline = line.split(', ,')
		if arg2 == newline[0]:
			id = newline[1]
			return id
		elif arg2 in newline[0]:
			x = newline[0]
			cities.append(x)
	return cities
	searchfile.close()


def build_url(arg3, arg4, *arg5):
	base_url = "http://api.openweathermap.org/data/2.5/%s?id=%s"
	if arg3 == 'weather':
		refined_url = base_url % (arg3, arg4) + '&units=imperial'
		return refined_url
	elif arg3 == 'forecast' and len(arg5) != 1:
		refined_url = base_url % (arg3, arg4) + '&units=imperial&cnt=17'
		return refined_url
	elif arg3 == 'forecast' and len(arg5) == 1:
		base_url2 = "http://api.openweathermap.org/data/2.5/%s/daily?id=%s"
		refined_url = base_url2 %(arg3, arg4)  + '&units=imperial' + '&cnt=%s' % arg5
		return refined_url

def get_data(arg6):
	results = ""
	results = requests.get(arg6)
	return results #.content

def find_weather(arg7):
	data = json.loads(arg7.content)
	return data

def weather_current(arg8):
	name = arg8['name']
	dt = arg8['dt']
	tmp = arg8['main']['temp']
	min_tmp = arg8['main']['temp_min']
	max_tmp = arg8['main']['temp_max']
	humidity = arg8['main']['humidity']
	wind = arg8['wind']['speed']
	weather = arg8['weather']
	desc = [x['description'] for x in weather]
	description = str(desc[0])
	date = datetime.datetime.strptime(time.ctime(dt), "%a %b %d %H:%M:%S %Y")
	return name,date,tmp,min_tmp,max_tmp,humidity,wind,description

def weather_forecast(arg):
	dt_list = []
	temp_list = []
	humidity_list = []
	description_list = []
	for d in arg['list']:
		dt_list.append(d['dt'])
		temp_list.append(d['main']['temp'])
		humidity_list.append(d['main']['humidity'])
		description_list.append(d['weather'][0]['description'])
	date = dt_time(dt_list)
	temp = tempF(temp_list)
	humidity = humidity_percent(humidity_list)
	description = desc_func(description_list)
	length = len(temp)
	list3 = []
	for x in range(0, length):
		a = temp[x]
		b = description[x]
		string_val = "%s %s" %(a,b)
		list3.append(string_val)
	mdict = OrderedDict(itertools.izip(date, list3))
	return mdict


def weather_numDay(arg):
	dt_list = []
	min_temp_list = []
	max_temp_list = []
	humidity_list = []
	description_list = []
	for d in arg['list']:
		dt_list.append(d['dt'])
		min_temp_list.append(d['temp']['min'])
		max_temp_list.append(d['temp']['max'])
		humidity_list.append(d['humidity'])
		description_list.append(d['weather'][0]['description'])
	date = dt_time(dt_list)
	min_temp = tempMin(min_temp_list)
	max_temp = tempMax(max_temp_list)
	humidity = humidity_percent(humidity_list)
	description = desc_func(description_list)
	length = len(min_temp)
	list3 = []
	for x in range(0, length):
		a = min_temp[x]
		b = max_temp[x]
		c = humidity[x]
		d = description[x]
		string_val = "%s %s %s %s" %(a,b,c,d)
		list3.append(string_val)
	mdict = OrderedDict(itertools.izip(date, list3))
	return mdict
	
		
		
def dt_time(arg):
	date = []
	for item in arg:
		x = datetime.datetime.strptime(time.ctime(item), "%a %b %d %H:%M:%S %Y")
		y = str(x)
		date.append(y)
	return date

def tempF(arg):
	temp = []
	for item in arg:
		t = "%s F" % item
		temp.append(t)
	return temp

def tempMin(arg):
	temp = []
	for item in arg:
		t = "Min: %s F" % item
		temp.append(t)
	return temp
	
def tempMax(arg):
	temp = []
	for item in arg:
		t = "Max: %s F" % item
		temp.append(t)
	return temp

def humidity_percent(arg):
	humidity = []
	for item in arg:
		h = "%s%%" % item
		humidity.append(h)
	return humidity

def desc_func(arg):
	desc = []
	for item in arg:
		desc.append(item.encode("utf-8"))
	return desc


#caller
def process_message(data):
	channel = data["channel"]
	text = data["text"]
	w_list = text.split(" ")
	if w_list[0] == '!weather':
		time.sleep(1)
		string = str(text)
		alist = string.split(" ")
		call1 = alist.index('!weather')
		del alist[call1]
		city = get_city(alist)
		var2 = get_cityID(city)
		if type(var2) is list and len(var2) > 0:
			string = '\n'.join(var2)
			outputs.append([channel, "Which city are you looking for?\n%s" % string])
		elif not var2:
			outputs.append([channel, "try that again, this time with correct spelling"])
		elif type(var2) is str:
			wvar = 'weather'
			refined_url = build_url(wvar,var2)
			results = get_data(refined_url)
			data = find_weather(results)
			var1 = weather_current(data)
			name = var1[0]
			date = var1[1]
			tmp = var1[2]
			min_tmp = var1[3]
			max_tmp = var1[4]
			humidity = var1[5]
			wind = var1[6]
			description = var1[7]
			outputs.append([channel, "city: %s \ndate: %s \ntemp: %s F \nmin_temp: %s F \nmax_temp: %s F \nhumidity: %s%% \nwind: %s mph \ndescription: %s" % (name,date,tmp,min_tmp,max_tmp,humidity,wind,description)])
	elif w_list[0] == '!weather-current':
		time.sleep(1)
		string = str(text)
		alist = string.split(" ")
		call1 = alist.index('!weather-current')
		del alist[call1]
		city = get_city(alist)
		var2 = get_cityID(city)
		if type(var2) is list and len(var2) > 0:
			string = '\n'.join(var2)
			outputs.append([channel, "Which city are you looking for?\n%s" % string])
		elif not var2:
			outputs.append([channel, "Derp! check spelling of your city"])
		elif type(var2) is str:
			wvar = 'weather'
			refined_url = build_url(wvar,var2)
			results = get_data(refined_url)
			data = find_weather(results)
			var1 = weather_current(data)
			name = var1[0]
			date = var1[1]
			tmp = var1[2]
			min_tmp = var1[3]
			max_tmp = var1[4]
			humidity = var1[5]
			wind = var1[6]
			description = var1[7]
			outputs.append([channel, "city: %s \ndate: %s \ntemp: %s F \nmin_temp: %s F \nmax_temp: %s F \nhumidity: %s%% \nwind: %s mph \ndescription: %s" % (name,date,tmp,min_tmp,max_tmp,humidity,wind,description)])
	elif w_list[0] == '!weather-forecast':
		time.sleep(1)
		string = str(text)
		alist = string.split(" ")
		call1 = alist.index('!weather-forecast')
		del alist[call1]
		city = get_city(alist)
		var2 = get_cityID(city)
		if type(var2) is list and len(var2) > 0:
			string = '\n'.join(var2)
			outputs.append([channel, "Which city are you looking for?\n%s" % string])
		elif not var2:
			outputs.append([channel, "check your map and spell the city correctly"])
		elif type(var2) is str:
			fvar = 'forecast'
			refined_url = build_url(fvar,var2)
			results = get_data(refined_url)
			data = find_weather(results)
			mdict = weather_forecast(data)
			for k,v in mdict.items():
				outputs.append([channel, "{}: {}".format(k,v)])
	elif w_list[0] == '!weather-10day':
		time.sleep(1)
		string = str(text)
		alist = string.split(" ")
		call1 = alist.index('!weather-10day')
		del alist[call1]
		city = get_city(alist)
		var2 = get_cityID(city)
		if type(var2) is list and len(var2) > 0:
			string = '\n'.join(var2)
			outputs.append([channel, "Which city are you looking for?\n%s" % string])
		elif not var2:
			outputs.append([channel, "where did you learn to spell. try your city again"])
		elif type(var2) is str:
			fvar = 'forecast'
			cnt = 10
			refined_url = build_url(fvar,var2,cnt)
			results = get_data(refined_url)
			data = find_weather(results)
			mdict = weather_numDay(data)
			for k,v in mdict.items():
				outputs.append([channel, "{}: {}".format(k,v)])