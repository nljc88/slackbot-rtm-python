
import sys, time, os, requests

outputs = []
crontable = []

FILE1="plugins/comics/xkcd_count"
FILE2="plugins/comics/smbc_count"
FILE3="plugins/comics/cah_count"

def get_xkcd_number():
	searchfile=open(FILE1, 'r')
	count = searchfile.read()
	return count
	searchfile.close()

def get_smbc_number():
	searchfile=open(FILE2, 'r')
	count = searchfile.read()
	return count
	searchfile.close()

def get_cah_number():
	searchfile=open(FILE3, 'r')
	count = searchfile.read()
	return count
	searchfile.close()

def process_message(data):
	channel = data["channel"]
	text = data["text"]
	string = text.lower()
	alist = string.split(' ')
	if alist[0] == 'xkcd' and alist[1] == 'count':
		time.sleep(1)
		count = get_xkcd_number()
		outputs.append([channel, 'Count is: %s' % count])
	elif alist[0] == 'smbc' and alist[1] == 'count':
		time.sleep(1)
		count = get_smbc_number()
		outputs.append([channel, 'Count is: %s' % count])
	elif alist[0] == 'cyanide' and alist[1] == 'count':
		time.sleep(1)
		count = get_cah_number()
		outputs.append([channel, 'Count is: %s' % count])