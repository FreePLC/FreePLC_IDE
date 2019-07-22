#!/usr/bin/env python
import sys, os
sys.path.insert(0,os.pardir)	# to find testserver.py

import testserver

import Pyro.core, Pyro.util

######## object that does the callbacks

class CallbackThing(Pyro.core.ObjBase):
	def __init__(self):
		Pyro.core.ObjBase.__init__(self)
		self.clients=[]
	def register(self, client):
		print 'REGISTER',client
		self.clients.append(client)
		#client._setOneway('callback') # don't wait for results for this method
	def shout(self, message):	
		print 'Got shout:',message
		# let it know to all clients!
		for c in self.clients[:]:		# use a copy of the list
			try:
				c.callback('Somebody shouted: '+message) # oneway call
			except Pyro.errors.ConnectionClosedError,x:
				# connection dropped, remove the listener if it's still there
				# check for existence because other thread may have killed it already
				if c in self.clients:
					self.clients.remove(c)
					print 'Removed dead listener',c


######## main program

testserver.start(CallbackThing,'callback')

