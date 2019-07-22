#!/usr/bin/env python
#
# This application creates a Name Server, Event Server,
# Pyro server, and clients, and uses threads to keep them
# all running in parallel.
# The main loop calls Pyro objects to set some artificial
# properties. Those objects publish those events on a ES channel,
# on which an event listener is subscribed. That listener prints
# the events that it receives.
#
# Thread 1: Pyro Name Server
# Thread 2: Pyro Event Server
# Thread 3: our own Pyro Daemon
# Thread 4: our own Event listener loop
# Thread 5: Main Loop, calling our Pyro object to set properties.
#

import time
import random
import string
import Pyro.naming
import Pyro.EventService.Server
from Pyro.EventService.Clients import Publisher, Subscriber
from Pyro.errors import *
import Pyro.util

from threading import Thread


####################### EVENT SERVER LISTENER & PUBLISHER #################

class PropertyChangePublisher(Pyro.core.ObjBase, Publisher):
	def __init__(self, name):
		Pyro.core.ObjBase.__init__(self)
		Publisher.__init__(self)
		self.name=name
	def setProperty(self, property, value):
		print self.name,"sets",property,"to",value
		self.publish(self.name+"."+property, value)

class PropertyChangeListener(Subscriber):
	def __init__(self):
		Subscriber.__init__(self)
	def event(self,event):
		# event.msg, subject, time
		print "Listener got Event: %s=%s"%(event.subject, event.msg)

	
####################### NS, ES, DAEMON, EVENT LISTENER THREADS ############

class NameServer(Thread):
	def __init__(self):
		Thread.__init__(self)
		self.setDaemon(1)
		self.starter = Pyro.naming.NameServerStarter()  # no special identification
	def run(self):
		print "Launching Pyro Name Server"
		self.starter.start()
	def waitUntilStarted(self):
		return self.starter.waitUntilStarted()
		
class EventServer(Thread):
	def __init__(self):
		Thread.__init__(self)
		self.setDaemon(1)
		self.starter = Pyro.EventService.Server.EventServiceStarter()  # no special identification
	def run(self):
		print "Launching Pyro Event Server"
		# we're using the OS's automatic port allocation
		es_port=0 
		self.starter.start(port=es_port, norange=(es_port==0))
	def waitUntilStarted(self):
		return self.starter.waitUntilStarted()

class PyroServer(Thread):
	def __init__(self):
		Thread.__init__(self)
		self.setDaemon(1)
		self.ready=0
	def run(self):
		Pyro.core.initServer()
		print "Creating Pyro server objects and Pyro Daemon"
		# we're using the OS's automatic port allocation
		port=0
		daemon = Pyro.core.Daemon(port=port, norange=(port==0))
		daemon.useNameServer(Pyro.naming.NameServerLocator().getNS())
		daemon.connect(PropertyChangePublisher("publisher1"), "publisher1")
		daemon.connect(PropertyChangePublisher("publisher2"), "publisher2")
		daemon.connect(PropertyChangePublisher("publisher3"), "publisher3")
		self.ready=1
		daemon.requestLoop()

class EventListener(Thread):
	def __init__(self):
		Thread.__init__(self)
		self.setDaemon(1)
	def run(self):
		Pyro.core.initServer()
		listener = PropertyChangeListener()
		listener.subscribeMatch("^publisher.\\..*$")
		print "EVENT LISTENER ACTIVATED"
		listener.listen()


############################# MAIN LOOP #############################
	
def main():
	if not Pyro.config.PYRO_MULTITHREADED:
		print "Sorry, this example requires multithreading."
		print "Either your Python doesn't support it or it has been disabled in the config."
		return

	nss=NameServer()
	nss.start()
	nss.waitUntilStarted()		# wait until the NS has fully started.
	ess=EventServer()
	ess.start()
	ess.waitUntilStarted()		# wait until the ES has fully started.
	
	EventListener().start()

	server=PyroServer()
	server.start()
	while not server.ready:
		time.sleep(1)

	p1 = Pyro.core.getProxyForURI("PYRONAME://publisher1")
	p2 = Pyro.core.getProxyForURI("PYRONAME://publisher2")
	p3 = Pyro.core.getProxyForURI("PYRONAME://publisher3")
	try:
		while 1:
			print "MAIN LOOP CHANGES PROPERTIES..."
			p1.setProperty(random.choice(string.uppercase), random.randint(0,1000))
			p2.setProperty(random.choice(string.uppercase), random.randint(0,1000))
			p3.setProperty(random.choice(string.uppercase), random.randint(0,1000))
			time.sleep(1)
	except Exception,x:
		print "".join(Pyro.util.getPyroTraceback(x))

if __name__=="__main__":
	main()


