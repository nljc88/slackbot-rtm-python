
import random
import re
import time

from greetings_lists import greeting_list, grumpy_list, insult_list
from user_dict import user_dict

crontable = []
outputs = []


jlist = ['http://gph.is/1kxQxOF',
         'http://gph.is/1umeeuI',
         'http://gph.is/1ytOrRP',
         'http://gph.is/1DotDlN',
         'http://gph.is/XJ4QTb',
         'http://gph.is/1bb1haK',
         'http://gph.is/1haBm6E',
         'http://gph.is/1mbqTtb',
         'http://gph.is/XNdfVJ',
         'http://gph.is/1h8R554',
         'http://gph.is/1WnOD2b',
         'http://gph.is/1gV9DXu',
         'http://gph.is/1ks6iEP'
         ]


def process_message(data):
    # caller
    channel = data["channel"]
    text = data["text"]
    user = data["user"]
    string = text.lower()
    alist = string.split(' ')
    if alist[0] == 'hello' and alist[1] == 'hal':
        time.sleep(1)
        username = user_dict[user]
        x = random.randint(0, 18)
        greeting = greeting_list[x]
        outputs.append([channel, '%s %s' % (greeting, username)])
    elif alist[0] == 'hi' and alist[1] == 'hal':
        time.sleep(1)
        username = user_dict[user]
        x = random.randint(0, 18)
        greeting = greeting_list[x]
        outputs.append([channel, '%s %s' % (greeting, username)])
    elif alist[0] == 'hey' and alist[1] == 'hal':
        time.sleep(1)
        x = random.randint(0, 4)
        grumpy = grumpy_list[x]
        outputs.append([channel, grumpy])
    elif alist[0] == 'sup' and alist[1] == 'hal':
        time.sleep(1)
        x = random.randint(0, 4)
        grumpy = grumpy_list[x]
        outputs.append([channel, grumpy])
    elif re.search('fuck(.*)hal', text):
        time.sleep(1)
        x = random.randint(0, 9)
        insult = insult_list[x]
        outputs.append([channel, insult])
    elif 'jesus' in text:
        time.sleep(1)
        x = random.randint(0, 12)
        the_jesus = jlist[x]
        results = 'You said it man!\n\n%s' % the_jesus
        outputs.append([channel, results])
    elif 'texas' in text:
        time.sleep(1)
        var1 = 'Holy dog shit! Texas? Only steers and queers come from Texas, Private Cowboy, and you dont look much like a steer to me, so that kinda narrows it down. Do you suck dicks?'
        outputs.append([channel, var1])
