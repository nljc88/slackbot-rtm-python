import time

crontable = []
outputs = []

title = 'Here is a list of my programmed functions:'
beer = 'or type "*beer commands*" for a list of my beer commands'
fantasy = 'or type "*fantasy commands*" for a list of my sports commands'
security = 'you can also try "*security commands*" for a list of my tools'
end = 'cheers!'

command_list = [
  'hal google <searchterms>',
  'hal abstract <topic>',
  'hal wiki summary <keywords>',
  'hal wiki search <keywords>',
  'hal wiki <page> url',
  'hal wiki <page> references',
  'hal wiki random',
  'hal comics (xkcd|smbc|cyanide)',
  'hal meme',
  'hal meme random',
  'hal meme <meme name>',
  'hal meme random <meme name>',
  'hal chuck norris',
  'hal carlton',
  'hal catfacts',
  'hal thanks obama'
 ]


def process_message(data):
    channel = data["channel"]
    text = data["text"]
    string = text.lower()
    alist = string.split(' ')
    if alist[0] == 'hal' and alist[1] == 'commands':
        time.sleep(1)
        string = '\n'.join(command_list)
        outputs.append([channel, "%s \n\n%s\n\n%s\n%s\n%s\n\n%s" % (title, string, beer, fantasy, security, end)])
