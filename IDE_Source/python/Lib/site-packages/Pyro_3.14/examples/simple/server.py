#!/usr/bin/env python
import Pyro.core
import Pyro.naming
from Pyro.errors import NamingError
import tst

# The testclass object.
# make a Pyro object from our regular class.
# (note that this can also be done using delegation)

class testclass(Pyro.core.ObjBase, tst.testclass):
	def __init__(self):
		Pyro.core.ObjBase.__init__(self)

######## main program

Pyro.core.initServer()

ns=Pyro.naming.NameServerLocator().getNS()

daemon=Pyro.core.Daemon()
daemon.useNameServer(ns)

try:
    ns.createGroup(":test")
except NamingError:
    pass
uri=daemon.connect(testclass(),":test.simple")

print "Server is ready."
daemon.requestLoop()
