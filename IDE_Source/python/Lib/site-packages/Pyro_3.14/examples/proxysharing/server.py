#!/usr/bin/env python
import Pyro.core
import Pyro.naming
from Pyro.errors import NamingError

class RemoteObject(Pyro.core.ObjBase):
	def __init__(self):
		Pyro.core.ObjBase.__init__(self)
	def method(self, arg):
		return " ~~this is the remote result~~ "
	
ns=Pyro.naming.NameServerLocator().getNS()
daemon=Pyro.core.Daemon()
daemon.useNameServer(ns)

try:
    ns.createGroup(":test")
except NamingError:
    pass
uri=daemon.connect(RemoteObject(),":test.proxysharing")

print "Server is ready."
daemon.requestLoop()
