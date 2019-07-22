#!/usr/bin/env python

import time, random
import Pyro.core
import Pyro.naming
from Pyro.errors import *
from threading import Thread

class Listener(Pyro.core.ObjBase):
	def __init__(self):
		Pyro.core.ObjBase.__init__(self)
	def callback(self, message):
		print 'GOT CALLBACK: ',message


abort=0

def shouter(objectURI):
	global abort
	object=objectURI.getProxy()  # we get our own proxy object because we're running in our own thread.
	print 'Shouter thread is running.'
	while not abort:
		print 'Shouting something'
		object.shout('Hello out there!')
		time.sleep(random.random()*3)
	print'Shouter thread is exiting.'	


def main():
	global abort
	Pyro.core.initServer()
	Pyro.core.initClient()
	daemon = Pyro.core.Daemon()
	locator = Pyro.naming.NameServerLocator()
	NS = locator.getNS()
	daemon.useNameServer(NS)
	listener=Listener()
	daemon.connect(listener)
	serverURI=NS.resolve(':test.callback')
	server = serverURI.getProxy()
	server.register(listener.getProxy())

	thread=Thread(target=shouter, args=(serverURI,))
	thread.start()

	while not abort:
		print 'Waiting for notification...'
		try:
			daemon.handleRequests()
		except KeyboardInterrupt:
			abort=1
			thread.join()
	print 'Exiting.'		

if __name__=='__main__':
	main()

