

import json
import time
from apiclient.discovery import build
import itertools
import collections

crontable = []
outputs = []

search_engine_id = 'search_engine_id'
api_key = 'api_key'


def build_keyword_search(arg):
    keywords = ' '.join(arg)
    return keywords


def build_service():
    service = build("customsearch", "v1", developerKey=api_key)
    return service


def get_data(arg1, arg2):
    results = arg1.cse().list(
        q=arg2,
        num=5,
        cx=search_engine_id,).execute()
    return results


def make_json(arg3):
    json_data = json.dumps(arg3, sort_keys=True, indent=2)
    return json_data


def filter_json(arg4):
    title_list = []
    snippet_list = []
    link_list = []
    for d in arg4['items']:
        title_list.append(d['title'].encode('ascii', 'ignore').decode('ascii'))
        snippet_list.append(d['snippet'])
        link_list.append(d['link'])
    gdict = collections.OrderedDict(itertools.izip(title_list, link_list))
    return gdict


def process_message(data):
    channel = data["channel"]
    text = data["text"]
    string = text.lower()
    alist = string.split(' ')
    if alist[0] == 'hal' and alist[1] == 'google':
        time.sleep(1)
        alist = alist[2:]
        keywords = build_keyword_search(alist)
        service = build_service()
        results = get_data(service, keywords)
        gdict = filter_json(results)
        for k, v in gdict.items():
            outputs.append([channel, "{}: {}".format(k, v)])
