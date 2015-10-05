
import sys, requests, json, time

crontable = []
outputs = []


def build_url(arg):
	if not arg:
		base_url = 'http://api.icndb.com/jokes/random'
		return base_url
	elif len(arg) == 1:
		base_url = 'http://api.icndb.com/jokes/random?firstName=%s'
		refined_url = base_url % arg
		return refined_url
	elif len(arg) == 2:
		base_url = 'http://api.icndb.com/jokes/random?firstName=%s&amp;lastName=%s'
		firstname = arg[0]
		lastname = arg[1]
		refined_url = base_url % (firstname, lastname)
		return refined_url


def get_data(arg):
	response = ''
	response = requests.get(arg)
	return response.content

def make_json(arg):
	json_data = json.loads(arg)
	return json_data

def get_joke(arg):
	joke = arg['value']['joke']
	return joke

def process_message(data):
	channel = data["channel"]
	text = data["text"]
	string = text.lower()
	alist = string.split(' ')
	if alist[0] == 'hal' and alist[1] == 'chuck' and alist[2] == 'norris':
		time.sleep(1)
		call1 = alist.index('hal')
		del alist[call1]
		call2 = alist.index('chuck')
		del alist[call2]
		call3 = alist.index('norris')
		del alist[call3]
		if not alist:
			url = build_url(alist)
			response = get_data(url)
			json_data = make_json(response)
			joke = get_joke(json_data)
			outputs.append([channel, joke])
		else:
			url = build_url(alist)
			print url
			response = get_data(url)
			json_data = make_json(response)
			joke = get_joke(json_data)
			outputs.append([channel, joke])
