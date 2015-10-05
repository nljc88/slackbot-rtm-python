
import time

crontable = []
outputs = []


def process_message(data):
    channel = data["channel"]
    text = data["text"]
    if '!data' in text:
    	string = str(data)
    	time.sleep(1)
    	outputs.append([channel, string])