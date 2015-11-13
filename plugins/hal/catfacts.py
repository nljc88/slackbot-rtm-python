
import requests
import json
import time

crontable = []
outputs = []


def get_data():
    response = ''
    response = requests.get('http://catfacts-api.appspot.com/api/facts?number=1')
    return response.content


def make_json(arg):
    json_data = json.loads(arg)
    return json_data


def get_catfact(arg):
    catfact = arg['facts']
    return catfact[0]


def process_message(data):
    channel = data["channel"]
    text = data["text"]
    string = text.lower()
    alist = string.split(' ')
    if alist[0] == 'hal' and alist[1] == 'catfacts':
        time.sleep(1)
        response = get_data()
        json_data = make_json(response)
        catfact = get_catfact(json_data)
        if not catfact:
            outputs.append([channel, 'did not find any cat facts'])
        else:
            outputs.append([channel, catfact])
