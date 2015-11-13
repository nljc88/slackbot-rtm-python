import time

crontable = []
outputs = []

title = 'The following is a list of *fantasy sports commands*:'
format1 = 'format your requests like so:\n<sport> <request> <playername>'
end = 'enjoy!'


hlist = [
  'baseball  news <playername>',
  'football stats  <playername>',
  'hockey statyear  <playername> <year>',
  '!starting goalies    (iphone: starting goalies)',
  ' ',
  'request = (news|stats|statyear)',
  ' ',
  'the following is a list of sports:',
  'hockey',
  'football',
  'baseball (no statyear)',
  'basketball',
  'golf (no statyear)',
  'nascar (news only)',
  ]


def process_message(data):
    channel = data["channel"]
    text = data["text"]
    string = text.lower()
    alist = string.split(' ')
    if alist[0] == 'fantasy' and alist[1] == 'commands':
        time.sleep(1)
        string = '\n'.join(hlist)
        message = "%s\n\n%s\n\n%s\n\n%s" % (title, format1, string, end)
        outputs.append([channel, message])
