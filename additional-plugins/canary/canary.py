#this plugin just lets me know the bot booted back up. you can customize it to say whatever you want. i stuck with a terminator bootup

import time
from random import randint
outputs = []

tm = str(time.time())
make = "Cyberdyne Systems"
model = "Series 800 Model 01"
ver = "Version 2.4"
dig = "DIAGNOSTIC:	checking power levels..."
a = randint(10,99)
aa = randint(8888,99999)
b = randint(10,99)
bb = randint(8888,99999)
c = randint(10,99)
cc = randint(8888,99999)
d = randint(10,99)
dd = randint(8888,99999)

end = "Initialization Complete.\nOBJECTIVE:		Terminate!"


#this only works with a valid channel number. You can get them from your slack api methods tester
def canary():
	time.sleep(1)
	outputs.append(["<CHANNEL>", "Initialization Sequence: %s \n%s \n%s \n%s \n%s \n%s		%s \n%s		%s \n%s		%s \n%s		%s \n%s" %(tm, make, model, ver, dig, a, aa, b, bb, c, cc, d, dd, end)])

canary()
