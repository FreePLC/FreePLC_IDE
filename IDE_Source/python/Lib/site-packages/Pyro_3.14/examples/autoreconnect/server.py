# Autoreconnect server
# uses the Name Server

import time
import Pyro.naming
import Pyro.core
from Pyro.errors import NamingError

class testobject(Pyro.core.ObjBase):
	def __init__(self):
		Pyro.core.ObjBase.__init__(self)
	def method(self,arg):
		print 'Method called with',arg
		print 'You can now try to stop this server with ctrl-C'
		time.sleep(1)


print 'Searching Naming Service...'
daemon = Pyro.core.Daemon()
locator = Pyro.naming.NameServerLocator()
ns = locator.getNS()

try:
	ns.createGroup(":test")
except NamingError:
	pass

daemon.useNameServer(ns)

# connect new instance, but using persistent mode
daemon.connectPersistent(testobject(),':test.autoreconnect')

# enter the service loop.
print 'Server started.'
daemon.requestLoop()
