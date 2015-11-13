
import time
import json
import urllib
import urllib2
import base64

crontable = []
outputs = []

apikey = 'apikey'


def clean_list_for_query(arg):
    blist = arg
    if '|' in blist[0]:
        blist = [y for x in blist for y in x.split('|')]
        del blist[0]
    if '>' or '<' in blist[0]:
        x = blist[0].replace('>', "").replace('<', '')
        blist[0] = x
    return blist


def get_encoded_url(arg):
    url = base64.encodestring(arg)
    return url


def make_params(arg):
    params = urllib.urlencode(
        {'url': arg,
         'format': 'json',
         'app_key': apikey,
         })
    return params


def get_data(arg):
    base_url = 'http://checkurl.phishtank.com/checkurl/'
    req = urllib2.Request(base_url, arg)
    response = urllib2.urlopen(req)
    json_data = json.loads(response.read())
    return json_data


def get_phish_results(arg):
    try:
        if arg['results']['in_database'] == False:
            searched_url = arg['results']['url'].encode('utf-8')
            phish_results = "Searched URL: %s\nNot In Database" % (searched_url)
            return phish_results
        elif arg['results']['in_database'] == True:
            searched_url = arg['results']['url'].encode('utf-8')
            in_database = arg['results']['in_database']
            verified = arg['results']['verified']
            verified_date = arg['results']['verified_at'].encode('utf-8')
            phishtank_page = arg['results']['phish_detail_page'].encode('utf-8')
            phish_results = "Searched URL: %s\nIn PhishTank DB: %s\nVerified: %s\nVerified Date: %s\nPhishtank: %s" % (searched_url, in_database, verified, verified_date, phishtank_page)
            return phish_results
    except KeyError:
        if arg['errortext']:
            phish_results = arg['errortext'].encode('utf-8')
            return phish_results
        else:
            phish_results = 'idk, something wront with api probably, it sucks'
            return phish_results


def process_message(data):
    channel = data["channel"]
    text = data["text"]
    string = text.lower()
    alist = string.split(' ')
    if alist[0] == '!phish' and alist[1] == 'search':
        time.sleep(1)
        alist = alist[2:]
        blist = clean_list_for_query(alist)
        encoded_url = get_encoded_url(blist[0])
        params = make_params(encoded_url)
        json_data = get_data(params)
        phish_results = get_phish_results(json_data)
        outputs.append([channel, phish_results])
