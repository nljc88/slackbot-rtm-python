
import random
import time

crontable = []
outputs = []

sexysaxman = [
        'http://sexysaxmansaxagrams.ytmnd.com/',
        'http://giphy.com/gifs/l41lXXCPM57rFRNqE/html5'
]


def get_sexysaxman():
    x = random.randint(0, 1)
    sexysax = sexysaxman[x]
    return sexysax


def process_message(data):
    channel = data["channel"]
    text = data["text"]
    string = text.lower()
    if 'sex' in string:
        time.sleep(1)
        saxman = get_sexysaxman()
        outputs.append([channel, saxman])
