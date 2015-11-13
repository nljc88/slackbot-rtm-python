import time

crontable = []
outputs = []

title = 'You can use the following commands in any channel HAL is in:'
hal = 'Try "*hal commands*" for a list of my commands'
beer = 'Type "*beer commands*" for a list of my beer options'
fantasy = 'Type "*fantasy commands*" for a list of commands'
security = 'Use "*security commands*" for a list of my security tools'
end = 'enjoy!'

hlist = [
  'youtube  <keyword>',
  'youtube list  <keyword>',
  '!weather  <city>',
  '!weather-current  <city>',
  '!weather-forecast     <city> (returns hourly)',
  '!weather forecast #day <city> (if no day, default is 10)',
  'comics (xkcd|smbc|cyanide)'
  ]


def process_message(data):
    channel = data["channel"]
    text = data["text"]
    string = text.lower()
    alist = string.split(' ')
    if alist[0] == 'hal' and alist[1] == 'help!':
        time.sleep(1)
        string = '\n'.join(hlist)
        outputs.append([channel, "%s\n\n%s\n\n%s\n%s\n%s\n%s\n\n%s" % (title, string, hal, beer, fantasy, security, end)])
