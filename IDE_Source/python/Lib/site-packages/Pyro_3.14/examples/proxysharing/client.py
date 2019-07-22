#!/usr/bin/env python

import Pyro.core, Pyro.naming
import threading
import time

stop=False

def myThread(nsproxy, proxy):
	global stop
	name=threading.currentThread().getName()
	try:
		while not stop:
			result=nsproxy.list(":test")
			result=proxy.method("the quick brown fox jumps over the lazy dog")
	except Exception,x:
		print "**** Exception in thread %s: {%s} %s" % (name, type(x), x)
	print "done in thread %s." % name

nsproxy = Pyro.naming.NameServerLocator().getNS()
proxy = Pyro.core.getAttrProxyForURI("PYRONAME://:test.proxysharing")

# now create a handful of threads and give each of them the same two proxy objects
threads = []
for i in range(20):
	thread=threading.Thread(target=myThread, args=(nsproxy, proxy) )
	# thread.setDaemon(True)
	threads.append(thread)

print "Starting all threads and running them for 5 seconds."
print "They're hammering the name server and the test server using the same proxy objects."
print "You should not see any exceptions."
for t in threads:
	t.start()

time.sleep(5)
print "END!"
stop=True
