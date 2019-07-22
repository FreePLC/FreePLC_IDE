#!/usr/bin/env python
import sys
import Pyro.naming, Pyro.core, Pyro.util, Pyro.protocol, Pyro.constants
from Pyro.errors import PyroError,NamingError
from Pyro.protocol import getHostname


######## Custom connections validator.
######## This validator asks the user to accept or deny a new connection.
######## Note that the old validator is still called when the user accepts.

class hostCheckingValidator(Pyro.protocol.DefaultConnValidator):
	def __init__(self):
		Pyro.protocol.DefaultConnValidator.__init__(self)
	def acceptHost(self,daemon,conn):
		(ip, port)=conn.addr
		try:
			hostname=getHostname(ip)
		except:
			hostname='<unknown>'
		print '\nNew connection from',ip,hostname
		a=raw_input('Do you want to accept this? y/n: ')
		if a=='y':
			# user accepts, but pass it on to the default validator,
			# which will check the max. number of connections...
			return Pyro.protocol.DefaultConnValidator.acceptHost(self,daemon, conn)
		else:
			Pyro.util.Log.msg('ConnValidator','User denied connection from',ip,hostname)
			return (0,Pyro.constants.DENIED_HOSTBLOCKED)	# not ok


##### test object

class testobject(Pyro.core.ObjBase):
	def method(self,arg):
		print 'method was called with',arg
		return 42


##### main program.

# initialize the server and set the default namespace group
Pyro.core.initServer()
Pyro.config.PYRO_TRACELEVEL=3
Pyro.config.PYRO_NS_DEFAULTGROUP=':test'
Pyro.config.PYRO_LOGFILE='server_log'
print 'Check the logfile for messages: server_log'

# Construct the Pyro Daemon with our own connection validator
daemon = Pyro.core.Daemon()
daemon.setNewConnectionValidator(hostCheckingValidator())   # <-- mind this!!!

# locate the NS
locator = Pyro.naming.NameServerLocator()
print 'searching for Naming Service...'
ns = locator.getNS()

print 'Naming Service found at',ns.URI.address,'('+(Pyro.protocol.getHostname(ns.URI.address) or '??')+') port',ns.URI.port

# make sure our namespace group exists
try: ns.createGroup(':test')
except NamingError: pass

daemon.useNameServer(ns)

# connect a new object implementation (first unregister previous one)
try: ns.unregister('denyhosts')
except NamingError: pass

daemon.connect(testobject(),'denyhosts')

# enter the service loop.
print 'Server object "denyhosts" ready.'
daemon.requestLoop()

