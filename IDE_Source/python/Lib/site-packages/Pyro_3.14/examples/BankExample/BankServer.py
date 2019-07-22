#!/usr/bin/env python

#
#	The banks server
#

import sys
import Pyro.naming
import Pyro.core
from Pyro.errors import PyroError,NamingError
import banks

group = ':banks1'   # the namespace group for all test servers

# avoid network port trouble with the VSB bank server
Pyro.config.PYRO_PORT=Pyro.config.PYRO_PORT+1

# initialize the server and set the default namespace group
Pyro.core.initServer()
Pyro.config.PYRO_NS_DEFAULTGROUP=group


# locate the NS
print 'Searching Naming Service...'
daemon = Pyro.core.Daemon()
locator = Pyro.naming.NameServerLocator()
ns = locator.getNS()


# make sure our namespace group exists
try:
	ns.createGroup(group)
except NamingError:
	pass

daemon.useNameServer(ns)

# connect a new object implementation (first unregister previous one)
try:
	ns.unregister('Rabobank')
	ns.unregister('VSB')
except NamingError:
	pass

# use Delegation approach for object implementation
obj1=Pyro.core.ObjBase()
obj1.delegateTo(banks.Rabobank())
daemon.connect(obj1,'Rabobank')
obj2=Pyro.core.ObjBase()
obj2.delegateTo(banks.VSB())
daemon.connect(obj2,'VSB')

# enter the service loop.
print 'Banks are ready for customers.'
daemon.requestLoop()

