#!/usr/bin/env python
import Pyro.naming
import Pyro.core
from Pyro.errors import NamingError
import bouncer

Pyro.core.initServer()

daemon = Pyro.core.Daemon()
ns = Pyro.naming.NameServerLocator().getNS()
daemon.useNameServer(ns)
try:
	ns.createGroup(':test')
except NamingError:
	pass

daemon.connect(bouncer.Bouncer('Server'),':test.bouncer')

# enter the service loop.
print 'Bouncer started'
daemon.requestLoop()

