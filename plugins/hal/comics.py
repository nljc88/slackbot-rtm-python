
import time
import requests
from bs4 import BeautifulSoup

outputs = []
crontable = []


def make_url(arg):
    if arg == 'xkcd':
        url = 'https://xkcd.com/'
        return url
    elif arg == 'smbc':
        url = 'http://www.smbc-comics.com/'
        return url
    elif arg == 'cyanide':
        url = 'http://explosm.net/comics/'
        return url


def check_site(arg):
    response = requests.get(arg)
    return response.content


def make_xkcd_soup(arg):
    soup = BeautifulSoup(arg, 'html.parser')
    tag1 = soup.find('div', {'id': 'comic'})
    data = tag1.find('img')['src']
    return data.encode('utf-8')


def make_smbc_soup(arg):
    soup = BeautifulSoup(arg, 'html.parser')
    tag1 = soup.find('div', {'id': 'comicbody'})
    data = tag1.find('img')['src']
    return data.encode('utf-8')


def make_cah_soup(arg):
    soup = BeautifulSoup(arg, 'html.parser')
    tag1 = soup.find('div', {'class': 'row space'})
    data = tag1.find('img')['src']
    return data.encode('utf-8')


def process_message(data):
    channel = data["channel"]
    text = data["text"]
    string = text.lower()
    alist = string.split(' ')
    if alist[0] == 'comics' and alist[1] == 'xkcd':
        time.sleep(1)
        url = make_url(alist[1])
        response = check_site(url)
        data = make_xkcd_soup(response)
        src = 'http:%s' % data
        outputs.append([channel, src])
    elif alist[0] == 'comics' and alist[1] == 'smbc':
        time.sleep(1)
        url = make_url(alist[1])
        response = check_site(url)
        data = make_smbc_soup(response)
        list1 = data.split('/')
        get_query = list1[-1]
        url = 'http://www.smbc-comics.com/comics/%s' % get_query
        outputs.append([channel, url])
    elif alist[0] == 'comics' and alist[1] == 'cyanide':
        time.sleep(1)
        url = make_url(alist[1])
        response = check_site(url)
        data = make_cah_soup(response)
        src = 'http:%s' % data
        outputs.append([channel, src])
