#!/usr/bin/env python

import Pyro.core

Pyro.config.PYRO_MOBILE_CODE=1		# Enable mobile code 

import servermodule3

class PyroServer(Pyro.core.ObjBase):
	def __init__(self):
		Pyro.core.ObjBase.__init__(self)
	def process(self, obj):
		print "Got call, invoking method, result=", obj.method()
		print "Returning response object."
		return servermodule3.ResponseClass()

daemon = Pyro.core.Daemon(host='localhost', port=12233)
print
print 'The Pyro Deamon is running on ',daemon.hostname+':'+str(daemon.port)

uri=daemon.connect(PyroServer(),'MobileHierarchy')

# enter the service loop.
print 'waiting for calls.'
daemon.requestLoop()
