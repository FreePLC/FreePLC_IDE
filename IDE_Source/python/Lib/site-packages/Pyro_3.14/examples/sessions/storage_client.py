#!/usr/bin/env python
import Pyro.core
import threading, time, sys


def processing(username):
	print "Processing started for user ",username
	time.sleep(0.5)
	data = Pyro.core.getProxyForURI("PYRONAME://:test.datastorage")
	data.init(username)
	for i in range(30):
		sys.stdout.write(username+" ")
		sys.stdout.flush()
		data.addline("line from user "+username)
		time.sleep(0.1)
	print "Stop processing for user "+username
	data.close()



# start a set of threads, 1 per user, which perform requests

users=["peter","nancy","wendy","vince","steve"]

for username in users:
	thread = threading.Thread(target=processing, args=(username, ))
	thread.daemon=False
	thread.start()

print "Wait for threads to finish."
