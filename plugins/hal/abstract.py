
import sys, time, requests, json

crontable = []
outputs = []

def build_query(arg):
	query = ' '.join(arg)
	return query

def build_url(arg):
	base_url = 'http://api.duckduckgo.com/?q=%s&format=json'
	refined_url = base_url % arg
	return refined_url

def get_data(arg):
	response = ''
	response = requests.get(arg)
	return response.content

def make_json(arg):
	json_data = json.loads(arg)
	return json_data

def get_abstract(arg):
	abstract = arg['Abstract']
	return abstract


def process_message(data):
	channel = data["channel"]
	text = data["text"]
	string = text.lower()
	alist = string.split(' ')
	if alist[0] == 'hal' and alist[1] == 'abstract':
		time.sleep(1)
		call1 = alist.index('hal')
		del alist[call1]
		call2 = alist.index('abstract')
		del alist[call2]
		query = build_query(alist)
		url = build_url(query)
		response = get_data(url)
		json_data = make_json(response)
		abstract = get_abstract(json_data)
		if not abstract:
			outputs.append([channel, 'no results found'])
		else:
			outputs.append([channel, abstract])
