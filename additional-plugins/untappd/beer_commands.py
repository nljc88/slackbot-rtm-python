import time

crontable = []
outputs = []

title = 'Here is a list of my *beer commands*:'
end = 'bottoms-up!'

command_list = [
  'beer search <beer name>',
  'beer info <beer name>',
  'beer reviews <beer name>',
  'brewery search <brewery name>',
  'brewery info <brewery name>',
  'brewery beerlist <brewery name>',
  'local search <address>'
 ]


def process_message(data):
    channel = data["channel"]
    text = data["text"]
    string = text.lower()
    alist = string.split(' ')
    if alist[0] == 'beer' and alist[1] == 'commands':
        time.sleep(1)
        string = '\n'.join(command_list)
        outputs.append([channel, "%s \n\n%s \n\n%s" % (title, string, end)])
