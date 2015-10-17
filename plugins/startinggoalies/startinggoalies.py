
import sys, requests, time, re
from bs4 import BeautifulSoup

crontable = []
outputs = []

def get_data():
	url = 'http://www2.dailyfaceoff.com/starting-goalies/'
	response = requests.get(url)
	if 'There are no games scheduled for today.' in response.content:
		return 'error1'
	else:
		return response.content

def make_soup_date(arg):
	soup = BeautifulSoup(arg, 'html.parser')
	container_tag = soup.find('div', {'id': 'matchups_container'})
	date = container_tag.find('h2').get_text()
	return date.encode("utf-8")

def make_soup_goalies(arg):
	soup = BeautifulSoup(arg, 'html.parser')
	matchup_tag = soup.find('div', {'id': 'matchups'})
	confirmed_list1 = []
	likely_list1 = []
	unconfirmed_list1 = []
	for child in matchup_tag.descendants:
		if 'Confirmed' in child:
			c = child.parent.parent
			string1 = str(c)
			confirmed_list1.append(string1)
		if 'Likely' in child:
			l = child.parent.parent
			string1 = str(l)
			likely_list1.append(string1)
		if 'Unconfirmed' in child:
			un = child
			string1 = str(un)
			unconfirmed_list1.append(string1)
	confirmed_list = []
	if confirmed_list1:
		conf_name_list = []
		conf_team_list = []
		for item1 in confirmed_list1:
			if 'alt' in item1:
				names = re.search('alt=(.*?)" ', item1)
				conf_name_list.append(names.group().encode('utf-8'))
				teams = re.search('title=(.*?)">', item1)
				conf_team_list.append(teams.group().encode('utf-8'))
		conf_name_list1 = []
		for item in conf_name_list:
			x = item.replace('alt="',"").replace('" ','')
			conf_name_list1.append(x)
		conf_name_list2 = []
		for item in conf_name_list1:
			string = str(item).replace(',','')
			sublist = string.split(' ')
			string2 = '%s %s' %(sublist[1],sublist[0])
			conf_name_list2.append(string2)
		cts = ' '.join(conf_team_list).replace('title="',"").replace('">',',')
		conf_team_list2 = cts.split(', ')
		for item in conf_team_list2:
			if "," in item:
				z = item.replace(',','')
				conf_team_list2.remove(item)
				conf_team_list2.append(z)
		length1 = len(conf_name_list2)
		for x in range(0, length1):
			a = conf_team_list2[x]
			b = conf_name_list2[x]
			conf_string = "%s: %s" %(a,b)
			confirmed_list.append(conf_string)
	likely_list = []
	if likely_list1:
		likely_name_list = []
		likely_team_list = []
		for item in likely_list1:
			if 'alt' in item:
				names = re.search('alt=(.*?)" ', item)
				likely_name_list.append(names.group().encode('utf-8'))
				teams = re.search('title=(.*?)">', item)
				likely_team_list.append(teams.group().encode('utf-8'))
		likely_name_list1 = []
		for item in likely_name_list:
			x = item.replace('alt="',"").replace('" ','')
			likely_name_list1.append(x)
		likely_name_list2 = []
		for item in likely_name_list1:
			string = str(item).replace(',','')
			sublist = string.split(' ')
			string2 = '%s %s' %(sublist[1],sublist[0])
			likely_name_list2.append(string2)
		lts = ' '.join(likely_team_list).replace('title="',"").replace('">',',')
		likely_team_list2 = lts.split(', ')
		for item2 in likely_team_list2:
			if "," in item2:
				y = item2.replace(',', '')
				likely_team_list2.remove(item2)
				likely_team_list2.append(y)
		length2 = len(likely_name_list2)
		for x in range(0, length2):
			a = likely_team_list2[x]
			b = likely_name_list2[x]
			likely_string = "%s: %s" %(a,b)
			likely_list.append(likely_string)
	unconfirmed_list = []
	unconf_name_list = []
	unconf_team_list = []
	for item1 in unconfirmed_list1:
		if 'alt' in item1:
			names = re.search('alt=(.*?)" ', item1)
			unconf_name_list.append(names.group().encode('utf-8'))
			teams = re.search('title=(.*?)">', item1)
			unconf_team_list.append(teams.group().encode('utf-8'))
	unconf_name_list1 = []
	for item in unconf_name_list:
		x = item.replace('alt=\\"',"").replace('\\" ','')
		unconf_name_list1.append(x)
	unconf_team_list1 = []
	for item in unconf_team_list:
		x = item.replace('title=\\"',"").replace('\\">','')
		unconf_team_list1.append(x)
	length3 = len(unconf_name_list1)
	for x in range(0, length3):
		a = unconf_team_list1[x]
		b = unconf_name_list1[x]
		unconf_string = "%s: %s" %(a,b)
		unconfirmed_list.append(unconf_string)
	if confirmed_list1:
		for z in conf_team_list2:
			for item in unconfirmed_list:
				if z in item:
					unconfirmed_list.remove(item)
	if likely_list1:
		for y in likely_team_list2:
			for item in unconfirmed_list:
				if y in item:
					unconfirmed_list.remove(item)
	if likely_list:
		return confirmed_list, likely_list, unconfirmed_list
	else:
		return confirmed_list, unconfirmed_list


def process_message(data):
	channel = data["channel"]
	text = data["text"]
	string = text.lower()
	alist = string.split(' ')
	if alist[0] == '!starting' or alist[0] == 'starting' and alist[1] == 'goalies':
		time.sleep(1)
		response = get_data()
		if response == 'error1':
			outputs.append([channel, 'There are no games scheduled for today.'])
		else:
			date = make_soup_date(response)
			data = make_soup_goalies(response)	
			if len(data) == 2:
				confirmed_list = data[0]
				unconfirmed_list = data[-1]
				conf_string1 = '\n'.join(confirmed_list)
				unconf_string1 = '\n'.join(unconfirmed_list)
				outputs.append([channel, "%s\n\nConfirmed Starting Goaltenders:\n%s \n\nUnconfirmed Goaltenders:\n%s" %(date,conf_string1, unconf_string1)])
			if len(data) == 3:
				confirmed_list = data[0]
				likely = data[1]
				unconfirmed_list = data[-1]
				conf_string1 = '\n'.join(confirmed_list)
				likely_string1 = '\n'.join(likely)
				unconf_string1 = '\n'.join(unconfirmed_list)
				outputs.append([channel, "%s\n\nConfirmed Starting Goaltenders:\n%s \n\nLikely Goaltenders:\n%s \n\nUnconfirmed Goaltenders:\n%s" %(date,conf_string1, likely_string1, unconf_string1)])

