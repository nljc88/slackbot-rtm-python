
import sys
import requests
import random
import time
from bs4 import BeautifulSoup

crontable = []
outputs = []

def build_keyword(arg):
	if not arg:
		keywords = 'random'
		return keywords
	else:
		keywords = ' '.join(arg)
		return keywords

def build_url(arg):
	base_url = "http://9gag.com/%s"
	refined_url = base_url % arg
	return refined_url

def get_data(arg2):
	results = ""
	results = requests.get(arg2)
	return results.content

def find_random_meme(arg3):
	soup = BeautifulSoup(arg3, 'html.parser')
	section = soup.find('section', {'id': 'individual-post'})
	badge = section.find('div', {'class': 'badge-post-container badge-entry-content post-container '})
	list1 = badge.contents
	string1 = str(list1)
	if 'javascript' in string1:
		meme_unicode = badge.find('img', {'class': 'badge-item-img'}).get('src')
		meme = meme_unicode.encode("utf-8")
		return meme
	elif 'badge-animated-cover badge-track badge-track-no-follow' in string1:
		meme_unicode = badge.find('div', {'class': 'badge-animated-container-animated post-view'}).get('data-image')
		meme = meme_unicode.encode("utf-8")
		return meme
	elif 'badge-nsfw-entry-cover' in string1:
		href_unicode = badge.find('a', {'class': 'badge-nsfw-entry-cover'}).get('href')
		href = href_unicode.encode("utf-8")
		return href

def find_link_to_meme(arg4):
	soup = BeautifulSoup(arg4, 'html.parser')
	section_tag = soup.find('section', {'id': 'search-result'})
	list2 = section_tag.contents
	string2 = str(list2)
	if 'Sorry! No results were found' in string2:
		return 'error1'
	else:
		ul_tag = section_tag.find('ul', {'class': 'overview-list badge-entry-collection'})
		x = random.randint(1, 17)
		bs_resultset_url = ul_tag.find_all('li')[x].get('data-entry-url')
		return bs_resultset_url

def find_meme2(arg5):
	soup = BeautifulSoup(arg5, 'html.parser')
	section = soup.find('section', {'id': 'individual-post'})
	badge = section.find('div', {'class': 'badge-post-container badge-entry-content post-container '})
	list1 = badge.contents
	string1 = str(list1)
	if 'javascript' in string1:
		meme_unicode = badge.find('img', {'class': 'badge-item-img'}).get('src')
		meme = meme_unicode.encode("utf-8")
		return meme
	elif 'badge-animated-cover badge-track badge-track-no-follow' in string1:
		meme_unicode = badge.find('div', {'class': 'badge-animated-container-animated post-view'}).get('data-image')
		meme = meme_unicode.encode("utf-8")
		return meme
	elif 'badge-nsfw-entry-cover' in string1:
		href_unicode = badge.find('a', {'class': 'badge-nsfw-entry-cover'}).get('href')
		href = href_unicode.encode("utf-8")
		return href


#caller
def process_message(data):
	channel = data["channel"]
	text = data["text"]
	text = text.lower()
	alist = text.split(' ')
	if alist[0] == 'hal' and alist[1] == 'meme':
		time.sleep(1)
		del alist[0]
		del alist[0]
		keywords = build_keyword(alist)
		if 'random' in keywords:
			refined_url = build_url(keywords)
			results = get_data(refined_url)
			meme = find_random_meme(results)
			outputs.append([channel, meme])
		else:
			keywords = keywords.replace(' ', '+')
			search_query = 'search?query=%s' % keywords
			refined_url = build_url(search_query)
			results = get_data(refined_url)
			bs_resultset_url = find_link_to_meme(results)
			if 'error1' in bs_resultset_url:
				outputs.append([channel, 'Sorry! No results were found'])
			else:
				base_url = "http://9gag.com%s"
				meme_link1 = base_url % bs_resultset_url
				results2 = get_data(meme_link1)
				meme = find_meme2(results2)
				outputs.append([channel, meme])

