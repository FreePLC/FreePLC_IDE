#!/usr/bin/env python

import time, random
import Pyro.core
import Pyro.naming
from Pyro.errors import *
from threading import Thread
import bouncer_cberror

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

	bounceObj = bouncer_cberror.Bouncer("Client")
	daemon.connect(bounceObj)  # callback object

	server = NS.resolve(':test.bouncer').getProxy()

	# create a thread that handles callback requests
	thread=Thread(target=PyroLoop, args=(daemon,))
	thread.start()

	print '1.Calling server from main (a single call)...'
	result = server.process(["hello"], bounceObj.getProxy())
	print '1.Result=',result
	print '2.Calling server from main (a single call)...'
	result = server.process(["hello"], bounceObj.getProxy())
	print '2.Result=',result

	abort=1
	thread.join()
	print 'Exiting.'


if __name__=='__main__':
	main()

