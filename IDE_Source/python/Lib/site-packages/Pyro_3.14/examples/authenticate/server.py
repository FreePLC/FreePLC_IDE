#!/usr/bin/env python
import sys
import Pyro.naming
import Pyro.core
from Pyro.errors import PyroError,NamingError

class testobject(Pyro.core.ObjBase):
	def __init__(self):
		Pyro.core.ObjBase.__init__(self)
	def method(self,arg):
		print 'Method called with',arg
		return 'An interesting result'


# initialize the server
Pyro.core.initServer()

# locate the NS
print 'Searching Naming Service...'
locator = Pyro.naming.NameServerLocator(identification='s3cr3t') # note the ident string
ns = locator.getNS()

try:
    ns.createGroup(":test")
except NamingError:
    pass

daemon = Pyro.core.Daemon()
daemon.useNameServer(ns)
daemon.setAllowedIdentifications(['s3cr3t'])

# connect new instance, but using persistent mode
daemon.connectPersistent(testobject(),':test.authentication')

# enter the service loop.
print 'Server started.'
daemon.requestLoop()
