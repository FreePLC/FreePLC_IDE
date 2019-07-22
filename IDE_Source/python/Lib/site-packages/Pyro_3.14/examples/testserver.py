#
#	Test server base implementation, used by a lot of the tests,
#	to avoid having to repeat this boilerplate code time after time.
#

import sys
import Pyro.naming
import Pyro.core
from Pyro.protocol import getHostname
from Pyro.errors import PyroError,NamingError

group = ':test'   # the namespace group for all test servers


######## main program

# objClass = the class of the Pyro implementation object
# objName = the name for the object to register in the Name Server
# delegate = whether to use the delegate approach or the regular
#            objBase subclassing approach

def start(objClass, objName, delegate=0):
	# initialize the server and set the default namespace group
	Pyro.core.initServer()
	Pyro.config.PYRO_NS_DEFAULTGROUP=group

	# locate the NS
	daemon = Pyro.core.Daemon()
	locator = Pyro.naming.NameServerLocator()
	print 'searching for Naming Service...'
	ns = locator.getNS()
	print 'Naming Service found at',ns.URI.address,'('+(Pyro.protocol.getHostname(ns.URI.address) or '??')+') port',ns.URI.port

	# make sure our namespace group exists
	try:
		ns.createGroup(group)
	except NamingError:
		pass

	daemon.useNameServer(ns)

	# connect a new object implementation (first unregister previous one)
	try:
		ns.unregister(objName)
	except NamingError:
		pass

	if delegate:
		print 'Delegation...'
		# use Deletation approach
		obj=Pyro.core.ObjBase()
		obj.delegateTo(objClass())
		daemon.connect(obj,objName)
	else:
		# use regular ObjBase subclassing approach
		obj=objClass()
		daemon.connect(obj,objName)

	# enter the service loop.
	print 'Server object "'+objName+'" ready.'
	try:
		# daemon.setTimeout(5)
		daemon.requestLoop()
	except KeyboardInterrupt:
		print 'shutting down gracefully.'
	daemon.disconnect(obj)
	daemon.shutdown()
	print 'Exiting.'


