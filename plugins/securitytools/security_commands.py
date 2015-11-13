import time

crontable = []
outputs = []

title = 'Here is a list of my *security commands*:'
end = 'Happy Hunting!'

command_list = [
  '!vt (hash|url|url-scan|ip|domain) <searchitem>',
  '!shadow (md5|sha1)',
  '!threatcrowd (domain|ip|email|md5) <searchitem>',
  '!passivetotal (ip|domain)',
  '!phish search <url>',
  ' ',
  'totalhash analysis <sha1>',
  'totalhash usage',
  'totalhash search <searchtype> <searchitem> (optional page=#)',
  'searchtypes include:',
  '(dns|email|filename|hash|ip|url|av|mutex|pdb|registry|useragent|version)',
  ' ',
  'censys (view|search) (ipv4|websites|certficiates) (ip|domain|sha256)',
  ' ',
  'tools whois (domain|ip)',
  'tools dnslookup (IP|MX|NS) <domain>',
  'tools reversedns <ip>',
  'tools geolocate <ip>'
 ]


def process_message(data):
    channel = data["channel"]
    text = data["text"]
    string = text.lower()
    alist = string.split(' ')
    if alist[0] == 'security' and alist[1] == 'commands':
        time.sleep(1)
        string = '\n'.join(command_list)
        outputs.append([channel, "%s \n\n%s \n\n%s" % (title, string, end)])
