import time
from random import randint
outputs = []

tm = str(time.time())
make = "Cyberdyne Systems"
model = "Series 800 Model 01"
ver = "Version 2.4"
dig = "DIAGNOSTIC:  checking power levels..."
a = randint(10, 99)
aa = randint(8888, 99999)
b = randint(10, 99)
bb = randint(8888, 99999)
c = randint(10, 99)
cc = randint(8888, 99999)
d = randint(10, 99)
dd = randint(8888, 99999)

end = "Initialization Complete.\nOBJECTIVE:     Terminate!"


def canary():
    time.sleep(1)
    #need to insert a legit channel id here
    outputs.append(["channel_ID", 'hal is online'])


canary()
