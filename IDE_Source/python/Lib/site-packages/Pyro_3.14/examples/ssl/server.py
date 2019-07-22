#!/usr/bin/env python
import sys
import Pyro.naming, Pyro.core, Pyro.util, Pyro.protocol
from Pyro.errors import PyroError,NamingError
from Pyro.protocol import getHostname



######## Custom connections validator.

class printCertValidator(Pyro.protocol.BasicSSLValidator):
	def checkCertificate(self,cert):
		if cert is None:
			return (0,3)
		print "Cert issuer: %s" % cert.get_issuer()
		print "Cert subject: %s" % cert.get_subject()
		print "Cert valid not before: %s" % cert.get_not_before()
		print "Cert valid not after: %s" % cert.get_not_after()
		return (1,0)


##### test object

class testclass(Pyro.core.ObjBase):
	def passSecretMessage(self,arg):
		print 'I got a secret message: ',arg
		return "Elvis Presley isn't dead, he just went home"


##### main program.

Pyro.config.PYROSSL_CERT="server.pem"
# Pyro.config.PYROSSL_KEY="server.key"
Pyro.config.PYRO_DNS_URI=True
Pyro.config.PYRO_TRACELEVEL=3
Pyro.config.PYRO_NS_DEFAULTGROUP=':test'
Pyro.config.PYRO_LOGFILE='server_log'
print 'Check the logfile for messages: server_log'

# Construct the Pyro Daemon with our own connection validator, using SSL
daemon = Pyro.core.Daemon(prtcol='PYROSSL')
daemon.setNewConnectionValidator(printCertValidator())		### <<--- !!!

# locate the NS
locator = Pyro.naming.NameServerLocator()
print 'searching for Naming Service...'
ns = locator.getNS()

print 'Naming Service found at',ns.URI.address,'('+(Pyro.protocol.getHostname(ns.URI.address) or '??')+') port',ns.URI.port

# make sure our namespace group exists
try: ns.createGroup(Pyro.config.PYRO_NS_DEFAULTGROUP)
except NamingError: pass

daemon.useNameServer(ns)

# connect a new object implementation (first unregister previous one)
try: ns.unregister('ssl')
except NamingError: pass

uri=daemon.connect(testclass(),'ssl')
print "server uri=",uri

# enter the service loop.
print 'Server object "ssl" ready.'
daemon.requestLoop()

