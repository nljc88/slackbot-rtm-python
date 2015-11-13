
import requests
import time
import random
from bs4 import BeautifulSoup

crontable = []
outputs = []


def build_url():
    base_url = 'http://thanks-obama.tumblr.com/?page=%s'
    page = random.randint(1, 9)
    refined_url = base_url % page
    return refined_url


def get_data(arg):
    results = ""
    results = requests.get(arg)
    return results.content


def find_random_obama(arg):
    soup = BeautifulSoup(arg, 'html.parser')
    section = soup.find('section', {'id': 'container'})
    ul_tag = section.find('ul', {'id': 'posts'})
    x = random.randint(1, 9)
    bs_resultset = ul_tag.find_all('li', {'class': 'post group'})[x]
    resultset2 = bs_resultset.find_all('div', {'class': 'cont group'})
    string2 = str(resultset2)
    list1 = string2.split('"')
    src_string = [s for s in list1 if 'http' in s]
    src = src_string[0]
    return src


def process_message(data):
    channel = data["channel"]
    text = data["text"]
    string = text.lower()
    alist = string.split(' ')
    if alist[0] == 'hal' and alist[1] == 'thanks' and alist[2] == 'obama':
        time.sleep(1)
        url = build_url()
        results = get_data(url)
        src = find_random_obama(results)
        outputs.append([channel, src])
