
import time
import requests
import json

crontable = []
outputs = []


def check_query(arg):
    if len(arg) == 40:
        return arg
    elif len(arg) == 32:
        return arg
    else:
        return 'error1'


def get_shadow_data(query):
    base_url = 'http://innocuous.shadowserver.org/api/?query=%s'
    refined_url = base_url % query
    response = requests.get(refined_url)
    return response


def make_json(response):
    if '! No match found for' in response:
        return response
    else:
        list1 = response.split('\n')
        file_info1 = list1[0]
        file_info_list = file_info1.split(',')
        file_info = "*md5:* %s\n*sha1:* %s\n*First Seen:* %s\n*Last Seen:* %s\n*FileType:* %s\n*ssdeep:* %s\n" % (file_info_list[0], file_info_list[1], file_info_list[2], file_info_list[3], file_info_list[4], file_info_list[-1])
        json_string = list1[1]
        json_data = json.loads(json_string.encode('utf-8'))
        av_engine_list = []
        signature_list = []
        for k, v in json_data.iteritems():
            av_engine_list.append(k)
            signature_list.append(v)
        av_list = []
        length = len(av_engine_list)
        for x in range(0, length):
            a = av_engine_list[x]
            b = signature_list[x]
            string_vals = "%s: %s\n" % (a, b)
            av_list.append(string_vals)
        av_string = ''.join(av_list)
        shadow_results = "%s\n----------------------------------------\n*AV Hits:*\n%s" % (file_info, av_string)
        return shadow_results


def process_message(data):
    channel = data["channel"]
    text = data["text"]
    string = text.lower()
    alist = string.split(' ')
    if alist[0] == '!shadow':
        time.sleep(1)
        hash1 = alist[1]
        query1 = check_query(hash1)
        if query1 == 'error1':
            outputs.append([channel, 'please submit md5 or sha1'])
        else:
            response = get_shadow_data(query1)
            shadow_results = make_json(response.content)
            outputs.append([channel, shadow_results])
