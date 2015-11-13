
import time
import requests
import json

crontable = []
outputs = []

apikey = 'api_key'


def get_pt_data(query):
    base_url = 'https://www.passivetotal.org/api/v1/passive'
    params = {'api_key': apikey, 'query': query}
    response = requests.get(base_url, params=params)
    return response


def make_json(response):
    json_data = json.loads(response.content)
    return json_data


def get_results_from_json(json_data):
    query = json_data['raw_query']
    first_seen = json_data['results']['first_seen']
    last_seen = json_data['results']['last_seen']
    resolved_list = []
    sinkhole_list = []
    for k, v in json_data.iteritems():
        if type(v) == dict:
            for subkey1, subvalue1 in v.iteritems():
                if subkey1 == 'enrichment_map':
                    for subkey2, subvalue2 in subvalue1.iteritems():
                        resolved_list.append(subkey2)
                        if 'sinkhole' in subvalue2:
                            for subkey3, subvalue3 in subvalue2.iteritems():
                                if 'sinkhole' in subkey3:
                                    sinkhole_list.append(subvalue3)
                        else:
                            sinkhole_list.append(' ')
    resolutions_list = []
    length = len(resolved_list)
    for x in range(0, length):
        a = resolved_list[x]
        b = sinkhole_list[x]
        string_vals = "  ----------------------------------------\n  *Resolution:* %s\n  *Sinkhole:* %s" % (a, b)
        resolutions_list.append(string_vals)
    resolvs_string = '\n'.join(resolutions_list)
    pt_results = "*PassiveTotal Results*\n*Query:* %s\n*First Seen:* %s\n*Last Seen:* %s\n*Resolutions:*\n%s" % (query, first_seen, last_seen, resolvs_string)
    return pt_results


def clean_list_for_query(blist):
    if '|' in blist[1]:
        blist = [y for x in blist for y in x.split('|')]
        del blist[1]
    if '>' or '<' in blist[1]:
        x = blist[1].replace('>', "").replace('<', '')
        blist[1] = x
    return blist


def process_message(data):
    channel = data["channel"]
    text = data["text"]
    string = text.lower()
    alist = string.split(' ')
    if alist[0] == '!passivetotal':
        time.sleep(1)
        blist = clean_list_for_query(alist)
        query = blist[1]
        pt_data = get_pt_data(query)
        json_data = make_json(pt_data)
        pt_results = get_results_from_json(json_data)
        outputs.append([channel, pt_results])
