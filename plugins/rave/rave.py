
import time
from raveatcloseofday import poem

crontable = []
outputs = []


def process_message(data):
    channel = data["channel"]
    text = data["text"]
    text = text.lower()
    if 'rave' in text:
        time.sleep(1)
        outputs.append([channel, poem])
