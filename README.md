slackbot-rtm-python
=============
A Slack bot written in python that connects via the RTM API. Hosted at Heroku. 

This is my project to learn python. Im sure there are better ways to do much of the code, so input is appreciated. I have named the bot HAL, so many of the plugin commands use hal in the calling arguments. You can change this to whatever name you would like. Its a good idea to use whatever you name your bot in the plugin calls.

the worker for this bot is the slackhq/python-rtmbot. I had a lot of growing pains getting it to work with Heroku. So the detailed instructions below should streamline its setup with heroku. 

slackbot-rtm-python is a callback based bot engine. The plugins architecture should be familiar to anyone with knowledge to the [Slack API](https://api.slack.com) and Python. The configuration file format is YAML.  

Installation
-----------

I did this on a MAC, so some of the instructions pertain to OSX users.

1. Download the slackbot-rtm-python code

        git clone # to be set
        cd slackbot-rtm-python

2. Setup Heroku Account and install its Dependencies
	
	https://www.heroku.com/
	
	Under 'Getting Started with Heroku', click Python
	
	You should be on the 'Getting Started with python on Heroku' page
	
	Install python if you have not already
	
	Install setuptools and pip ($ easy_install setuptools) & ($ easy_install pip)
	
	Install Virtualenv ($ pip install virtualenv)
	
	Install Postgres ($ brew install postgresql) - this is to run the worker locally when testing new plugins. Its more efficient than pushing to heroku every time.

	
	You will most likely need to alter permissions on a file to complete postgres install
	
	$ sudo chown -R `whoami` /usr/local/lib/pkgconfig
	
	$ brew link postgresql


3. Finish Heroku Setup
	
	In Heroku, click 'Im ready to start'
	
	Download and install Heroku Toolbelt
	
	$ heroku login
	
	Install worker dependencies
	
	$ pip install -r requirements.txt
	
	NOTE: Anytime you add a plugin that uses a library not currently installed, you will need to add that library to the requirements.txt
	
4. Configure rtmbot (https://api.slack.com/bot-users). Create your bot in slack, insert its slack token into the rtmbot.conf file
        
        vi rtmbot.conf (or use pico ;) )
          SLACK_TOKEN: "xoxb-11111111111-222222222222222"


5. Deploy the worker to Heroku

	$ heroku create
	
	You will need to alter the .gitignore file, for when you push to heroku it will ignore some critical files
	
	$ cat .gitignore
	
	pico or vim and remove the ignored files you want to push
	- It will most likely ignore the Procfile, rtmbot.conf files, and plugin/ folders
	- delete these from the .gitignore file, maybe add .DS_Store
	
	You may need to add the files previously ignored
	
	$ git add Procfile
	
	$ git add rtmbot.conf
	
	$ git commit -m "<insert your notes>"

	another common issue is that the Procfile should not have an extension. if it does, create a new one. It only needs to have the following in it:
	
	worker: python rtmbot.py
	
	Push worker to heroku
	
	$ git push heroku master

	Turn on the worker
	
	$ heroku ps:scale worker=1

6. Additional Heroku commands to know
	
	check status of worker
	
	$ heroku ps

	check logs
	
	$ heroku logs

	turn off the worker
	
	$ heroku ps:stop worker

	run worker locally (best for testing plugins)
	
	$ heroku local worker



Add Plugins
-------

Plugins can be installed as .py files in the ```plugins/``` directory OR as a .py file in any first level subdirectory. If your plugin uses multiple source files and libraries, it is recommended that you create a directory. You can install as many plugins as you like, and each will handle every event received by the bot independently.


    mkdir plugins/<plugin name>
 

Create Plugins
--------

####Incoming data
Plugins are callback based and respond to any event sent via the rtm websocket. To act on an event, create a function definition called process_(api_method) that accepts a single arg. For example, to handle incoming messages:

    def process_message(data):
        print data

This will print the incoming message json (dict) to the screen where the bot is running.

Plugins having a method defined as ```catch_all(data)``` will receive ALL events from the websocket. This is useful for learning the names of events and debugging.

####Outgoing data
Plugins can send messages back to any channel, including direct messages. This is done by appending a two item array to the outputs global array. The first item in the array is the channel ID and the second is the message text. Example that writes "hello world" when the plugin is started:

    outputs = []
    outputs.append(["C12345667", "hello world"])
        
*Note*: you should always create the outputs array at the start of your program, i.e. ```outputs = []```

####Timed jobs
Plugins can also run methods on a schedule. This allows a plugin to poll for updates or perform housekeeping during its lifetime. This is done by appending a two item array to the crontable array. The first item is the interval in seconds and the second item is the method to run. For example, this will print "hello world" every 10 seconds.

    outputs = []
    crontable = []
    crontable.append([10, "say_hello"])
    def say_hello():
        outputs.append(["C12345667", "hello world"])

####Plugin misc
The data within a plugin persists for the life of the rtmbot process. If you need persistent data, you should use something like sqlite or the python pickle libraries.

All of the default plugins should load. There are plugins in the 'additional-plugins' folder. These plugins are easily implemented, but they may require something like your API key.


!data

in any channel, the bot will post the json blob that was sent to the worker


!help 

returns a list of plugins your bot can currently do.

if you add a plugin, you will have to manually add it to the help list


hal commands

returns a list of commands the bot can do

these are in addition to the !help 


Current Plugins
--------

try !help or 'hal commands' for syntax needed for each plugin

!data
\n#returns json passed to worker back to a channel

!help
\n#list of functions called by '!'

commands
\n#list of bot commands initiated by bot name 'hal' 

abstract		#returns short abstract about a subject

carlton		#dancing carltons

catfacts		#random catfacts

chucknorris	#random Chuck Norris awesomeness

meme		#returns random or specific meme

sexysaxman	#link to sexysaxman site

thanks_obama	#returns thanks obama meme

wiki		#search wiki for summary, list of articles, links, references

zombie		#random zombies

!playernews	#recent news on a nhl player

!playerstats	#current season stats on nhl player

!statyear	#stats for a specific season for nhl player

!weather		#current weather, forecast, and 10day

!yt		#youtube vide or list of yt video's


####Plugins that need configured

canary		#lets you know your bot has started, you will need to add a valid channelID

comics		#pulls a few comics into a channel, you will need to add a valid channelID

google		#does google search, you will need to use your own search_engine_id and API key. see plugin for links to instructions on setting it up








