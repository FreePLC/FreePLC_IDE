#!/usr/bin/env python

import time, random
import Pyro.core
import Pyro.naming
from Pyro.errors import *
from threading import Thread
import bouncer2

abort=0

def PyroLoop(daemon):
	global abort
	print 'Pyro daemon loop thread is running.'
	daemon.requestLoop(lambda: not abort) 
	print 'Pyro daemon loop thread is exiting.'


def main():
	global abort
	Pyro.core.initServer()
	Pyro.core.initClient()
	daemon = Pyro.core.Daemon()
	NS = Pyro.naming.NameServerLocator().getNS()
	daemon.useNameServer(NS)

	server = NS.resolve(':test.bouncer2').getProxy()

	bounceObj = bouncer2.Bouncer("Client")
	daemon.connect(bounceObj)  # callback object
	
	# register callback obj on server
	server.register(bounceObj.getProxy())
	# register server as 'callback' on own object
	bounceObj.register(server)

	# create a thread that handles callback requests
	thread=Thread(target=PyroLoop, args=(daemon,))
	thread.start()

	print 'This bounce example will deadlock!'
	print 'Read the manual or Readme.txt for more info why this is the case!'

	print 'Calling server...'
	result = server.process(["hello"])
	print 'Result=',result

	abort=1
	thread.join()
	print 'Exiting.'


if __name__=='__main__':
	main()

