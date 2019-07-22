#!/usr/bin/env python
import sys, os

sys.path.insert(0,os.pardir)	# to find testserver.py

import testserver
import Pyro.core

######## testclass object

class testclass(object):
	def setname(self,name):
		self.name=name
	def getname(self):
		return self.name

######## main program

Pyro.core.initServer()
Pyro.config.PYRO_TRACELEVEL=3
Pyro.config.PYRO_LOGFILE='server_log'
Pyro.config.PYRO_MAXCONNECTIONS = 10
print 'Reduced max number of simultaneous connections to 10'
print 'Check the logfile for messages: server_log'

testserver.start(testclass, 'maxclients', delegate=1)

