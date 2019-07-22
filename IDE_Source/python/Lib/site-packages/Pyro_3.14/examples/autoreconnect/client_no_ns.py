# Autoreconnect client
# doesn't use the Name Server

import time
import Pyro.core
import Pyro.errors

obj = Pyro.core.getProxyForURI("PYROLOC://localhost/:test.autoreconnect")

while True:
	print 'call...'
	try:
		obj.method(42)
		print 'Sleeping 1 second'
		time.sleep(1)
	except Pyro.errors.ConnectionClosedError,x:
		print 'Connection lost. REBINDING...'
		print '(restart the server now)'
		obj.adapter.rebindURI()

