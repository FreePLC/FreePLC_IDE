#!/usr/bin/env python
#
# This application creates a Name Server, Event Server,
# Pyro server, and clients, and uses a custom event loop to keep them
# all running in parallel.
# The custom loop runs in its own server thread otherwise we
# can't run client invocations, obviously.
# The main loop calls Pyro objects to set some artificial
# properties. Those objects publish those events on a ES channel,
# on which an event listener is subscribed. That listener prints
# the events that it receives.
#

import time
import random
import string
import Pyro.naming
import Pyro.EventService.Server
from Pyro.EventService.Clients import Publisher, Subscriber
from Pyro.errors import *
import Pyro.util

import select
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

	

################ Multi-purpose monolithic server. #####################
# handles all socket events from NS, ES, Pyro daemon.
class Server(Thread):
	def __init__(self):
		Thread.__init__(self)
		self.setDaemon(1)
		self.ns_starter=None
		self.ns_sockets=[]
		self.es_starter=None
		self.es_sockets=[]
		self.pdaemon=None
		# daemon sockets are dynamic...
		self.listener=None
		self.listener_sockets=[]
	def setNameServerStarter(self, starter):
		starter.waitUntilStarted()
		self.ns_starter=starter
		self.ns_sockets=starter.getServerSockets()
	def setEventServerStarter(self, starter):
		starter.waitUntilStarted()
		self.es_starter=starter
		self.es_sockets=starter.getServerSockets()
	def setPyroDaemon(self, pdaemon):
		self.pdaemon=pdaemon
	def setEventListener(self, listener):
		self.listener=listener
		self.listener_sockets=listener.getDaemon().getServerSockets()
	def run(self):
		Pyro.core.initServer()
		while 1:
			all_sockets = self.ns_sockets + self.es_sockets + self.listener_sockets
			daemon_sockets=[]
			if self.pdaemon:
				# daemon sockets are dynamic.
				daemon_sockets = self.pdaemon.getServerSockets()
				all_sockets.extend(daemon_sockets)

			################### CUSTOM EVENT LOOP ####################

			if all_sockets:
				ins,outs,exs=select.select(all_sockets,[],[],1)
			else:
				# windows doesn't like empty select. Just wait a while.
				time.sleep(1)
				continue

			##########################################################

			# check for Name Server sockets...
			for ns_sock in self.ns_sockets:
				if ns_sock in ins:
					self.ns_starter.handleRequests(timeout=0)
					break
			# check for Event Server sockets....
			for es_sock in self.es_sockets:
				if es_sock in ins:
					self.es_starter.handleRequests(timeout=0)
					break
			# check for Daemon Server sockets....
			for d_sock in daemon_sockets:
				if d_sock in ins:
					self.pdaemon.handleRequests(timeout=0)
					break
			# check for Event listener sockets...
			for l_sock in self.listener_sockets:
				if l_sock in ins:
					self.listener.getDaemon().handleRequests(timeout=0)
					break


############################# MAIN LOOP #############################
	
def main():

	if not Pyro.config.PYRO_MULTITHREADED:
		print "Sorry, this example requires multithreading."
		print "Either your Python doesn't support it or it has been disabled in the config."
		return

	Pyro.core.initClient()
	server = Server()
	server.start()

	# We are starting the different servers in a separate thread (here),
	# otherwise the custom server thread cannot handle the concurrent
	# invocations (for instance, the ES needs the NS when it starts...)
	print "STARTING NAME SERVER"
	starter = Pyro.naming.NameServerStarter()  # no special identification
	starter.initialize()
	server.setNameServerStarter(starter)
	print "NAME SERVER STARTED ON PORT",starter.daemon.port
	
	print "STARTING EVENT SERVER"
	starter = Pyro.EventService.Server.EventServiceStarter()  # no special identification
	# use port autoselect
	es_port=0
	starter.initialize(port=es_port, norange=(es_port==0))
	server.setEventServerStarter(starter)
	print "EVENT SERVER STARTED ON PORT",starter.daemon.port

	print "CREATING PYRO SERVER OBJECTS AND PYRO DAEMON"
	# use port autoselect
	port=0
	daemon = Pyro.core.Daemon(port=port, norange=(port==0))
	daemon.useNameServer(Pyro.naming.NameServerLocator().getNS())
	daemon.connect(PropertyChangePublisher("publisher1"), "publisher1")
	daemon.connect(PropertyChangePublisher("publisher2"), "publisher2")
	daemon.connect(PropertyChangePublisher("publisher3"), "publisher3")
	server.setPyroDaemon(daemon)
	print "PYRO SERVER ACTIVATED ON PORT",daemon.port

	listener = PropertyChangeListener()
	listener.subscribeMatch("^publisher.\\..*$")
	server.setEventListener(listener)
	print "EVENT LISTENER ACTIVATED"

	print "ALL SERVERS WERE STARTED!"
	time.sleep(1)
	p1 = Pyro.core.getProxyForURI("PYRONAME://publisher1")
	p2 = Pyro.core.getProxyForURI("PYRONAME://publisher2")
	p3 = Pyro.core.getProxyForURI("PYRONAME://publisher3")
	try:
		while True:
			print "MAIN LOOP CHANGES PROPERTIES..."
			p1.setProperty(random.choice(string.uppercase), random.randint(0,1000))
			p2.setProperty(random.choice(string.uppercase), random.randint(0,1000))
			p3.setProperty(random.choice(string.uppercase), random.randint(0,1000))
			time.sleep(1)
	except Exception,x:
		print "".join(Pyro.util.getPyroTraceback(x))

if __name__=="__main__":
	main()
