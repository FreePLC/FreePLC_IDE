#!/usr/bin/env python

#  this is exactly the same server code as "bounce_server.py"
#  but this one uses "bouncer2" as Pyro object.

import Pyro.naming
import Pyro.core
from Pyro.errors import NamingError
import bouncer2 as bouncer

Pyro.core.initServer()

daemon = Pyro.core.Daemon()
ns = Pyro.naming.NameServerLocator().getNS()
daemon.useNameServer(ns)
try:
	ns.createGroup(':test')
except NamingError:
	pass

daemon.connect(bouncer.Bouncer('Server'),':test.bouncer2')

# enter the service loop.
print 'This bounce example will deadlock!'
print 'Read the manual or Readme.txt for more info why this is the case!'
print 'Bouncer started'
daemon.requestLoop()

