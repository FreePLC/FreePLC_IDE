#!/usr/bin/env python

#
#	The bank server.
#

import sys
import Pyro.naming
import Pyro.core
from Pyro.errors import PyroError,NamingError
import banks

group = ':banks'   # the namespace group for all test servers

# initialize the server and set the default namespace group
Pyro.core.initServer()
Pyro.config.PYRO_NS_DEFAULTGROUP=group

# locate the NS
print 'Searching Naming Service...'
locator = Pyro.naming.NameServerLocator()
ns = locator.getNS()

# make sure our namespace group exists
try:
	ns.createGroup(group)
except NamingError:
	pass

daemon = Pyro.core.Daemon()
daemon.useNameServer(ns)
cleanupAge=20
daemon.setTransientsCleanupAge(cleanupAge)
print '>>>The maximum account inactivity age is',cleanupAge,'seconds<<<'

# connect a new object implementation (first unregister previous one)
try:
	ns.unregister('Rabobank')
	ns.unregister('VSB')
except NamingError:
	pass

# bank class is direct subclass of Pyro.core.ObjBase
daemon.connect(banks.Rabobank(),'Rabobank')
daemon.connect(banks.VSB(),'VSB')

# enter the service loop.
print 'Banks are ready for customers.'
daemon.requestLoop()


