# Autoreconnect client
# uses the Name Server

import time
import Pyro.naming, Pyro.core

locator = Pyro.naming.NameServerLocator()
print 'Searching Naming Service...',
ns = locator.getNS()
URI=ns.resolve(':test.autoreconnect')
obj = Pyro.core.getAttrProxyForURI(URI)

while True:
	print 'call...'
	try:
		obj.method(42)
		print 'Sleeping 1 second'
		time.sleep(1)
		#obj._release() # experiment with this
		#print 'released'
		#time.sleep(2)
	except Pyro.errors.ConnectionClosedError,x:     # or possibly even ProtocolError
		print 'Connection lost. REBINDING...'
		print '(restart the server now)'
		obj.adapter.rebindURI()
