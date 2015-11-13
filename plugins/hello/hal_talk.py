

import time
from user_dict import user_dict
from rave_channel_dict import channel_dict

crontable = []
outputs = []


def get_info(arg):
    user_id = []
    channelid = []
    dm_list = []
    text_list = []
    dm_list = []
    for item in arg:
        if 'user:' in item:
            u = arg.index('user:')
            user_id.append(arg[u+1])
        if 'channel:' in item:
            c = arg.index('channel:')
            channelid.append(arg[c+1])
        if 'text:' in item:
            t = arg.index('text:')
            x = t+1
            y = ' '.join(arg[x:])
            text_list.append(y)
        if 'dm:' in item:
            dm_list.append(item)
    user_string = ' '.join(user_id)
    channel_string = ' '.join(channelid)
    message_string = ' '.join(text_list)
    return user_string, channel_string, message_string, dm_list


def get_channel(channel):
    for k, v in channel_dict.items():
        if v == channel:
            return k


def process_message(data):
    channel = data["channel"]
    text = data["text"]
    user = data["user"]
    string = text.lower().encode('ascii', 'ignore').decode('ascii')
    alist = string.split(' ')
    if alist[0] == 'haltalk':
        time.sleep(1)
        alist = alist[1:]
        info = get_info(alist)
        username = info[0]
        channel_name = info[1]
        message_sending = info[2]
        dm_list = info[3]
        channel_id = channel_dict[channel_name]
        message_user = "@%s %s" % (username, message_sending.encode('ascii', 'ignore').decode('ascii'))
        message = message_sending.encode('ascii', 'ignore').decode('ascii')
        if dm_list:
            pass
        elif username:
            outputs.append([channel_id, message_user])
        else:
            outputs.append([channel_id, message])
    elif 'hal' in string and alist[0] != 'haltalk' and alist[0] != 'hi' and alist[0] != 'hello' and alist[0] != 'hey' and alist[0] != 'sup' and alist[1] != 'abstract' and alist[1] != 'carlton' and alist[1] != 'chuck' and alist[1] != 'catfacts' and alist[1] != 'commands' and alist[1] != 'google' and alist[1] != 'meme' and alist[1] != 'sexysaxman' and alist[1] != 'wiki' and alist[2] != 'obama':
            time.sleep(1)
            username = user_dict[user]
            channel_name = get_channel(channel)
            #the channel is your own dm with the bot
            outputs.append(['DM_with_bot_channel', "user: %s\nchannel name: %s\nchannelID: %s\nmessage: %s" % (username, channel_name, channel, string)])
