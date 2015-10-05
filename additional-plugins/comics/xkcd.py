
import sys, time, os, requests

outputs = []
crontable = []
crontable.append([43200, "xkcd_lookup"])

FILE="plugins/comics/xkcd_count"

def get_number():
	searchfile=open(FILE, 'r')
	count = searchfile.read()
	return count
	searchfile.close()

def make_url(arg):
	base_url = 'https://xkcd.com/%s'
	url = base_url % arg
	return url

def check_site(arg):
	response = requests.get(arg)
	return response.status_code

def make_new_number(arg):
	number = int(arg) + 1
	return number

def append_new_number(arg):
	openfile = open(FILE, 'r+')
	openfile.seek(0)
	openfile.write(str(arg))
	openfile.close()


#this only works with a valid channel number. You can get them from your slack api methods tester
def xkcd_lookup():
	count = get_number()
	url = make_url(count)
	response = check_site(url)
	if response == 200:
		number = make_new_number(count)
		append_new_number(number)
		outputs.append(['<CHANNEL ID>', url])
	elif response == 404:
		outputs.append(['<CHANNEL ID>', 'no new xkcd comic at this time, will check again in 12hrs'])




