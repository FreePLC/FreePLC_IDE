#!/usr/bin/env python
import Pyro.core
import Pyro.naming
from Pyro.errors import NamingError
from Queue import Queue

class DispatcherQueue(Pyro.core.ObjBase):
	def __init__(self):
		Pyro.core.ObjBase.__init__(self)
		self.workqueue = Queue()
		self.resultqueue = Queue()
	def putWork(self, item):
		self.workqueue.put(item)
	def getWork(self, timeout=5):
		return self.workqueue.get(block=True, timeout=timeout)
	def putResult(self, item):
		self.resultqueue.put(item)
	def getResult(self, timeout=5):
		return self.resultqueue.get(block=True, timeout=timeout)
	def workQueueSize(self):
		return self.workqueue.qsize()
	def resultQueueSize(self):
		return self.resultqueue.qsize()
		


######## main program

Pyro.core.initServer()
ns=Pyro.naming.NameServerLocator().getNS()
daemon=Pyro.core.Daemon()
daemon.useNameServer(ns)

try:
    ns.createGroup(":Distributed2")
except NamingError:
    pass
try:
	ns.unregister(":Distributed2.dispatcher")
except NamingError:
	pass
uri=daemon.connect(DispatcherQueue(),":Distributed2.dispatcher")

print "Dispatcher is ready."
daemon.requestLoop()
