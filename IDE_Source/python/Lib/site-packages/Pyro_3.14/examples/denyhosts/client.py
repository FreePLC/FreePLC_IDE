#!/usr/bin/env python

#
#	Notice: this client doesn't use the base testclient.py code
#	because this one has to do special tests with creating proxies.
#

import Pyro.naming, Pyro.core
import Pyro.errors
from Pyro.protocol import getHostname

Pyro.core.initClient()
Pyro.config.PYRO_NS_DEFAULTGROUP=':test'	# default namespace group
Pyro.config.PYRO_TRACELEVEL=3
Pyro.config.PYRO_LOGFILE='client_log'
print 'Check the logfile: client_log'

locator = Pyro.naming.NameServerLocator()
print 'Searching Naming Service...',
ns = locator.getNS()

print 'Naming Service found at',ns.URI.address,'('+(Pyro.protocol.getHostname(ns.URI.address) or '??')+') port',ns.URI.port

print 'binding to object'
try:
    URI=ns.resolve('denyhosts')
    print 'URI:',URI
except Pyro.core.PyroError,x:
    print 'Couldn\'t bind object, nameserver says:',x
    raise SystemExit


try:
	print 'Trying to create proxy object'
	obj=Pyro.core.getProxyForURI(URI)
	print 'Calling method 5 times'
	print 'Result1=',obj.method('Hi there 1')
	print 'Result2=',obj.method('Hi there 2')
	print 'Result3=',obj.method('Hi there 3')
	print 'Result4=',obj.method('Hi there 4')
	print 'Result5=',obj.method('Hi there 5')
except Pyro.errors.ConnectionDeniedError,x:
	# Server denied the new connection.
	print 'ConnectionDeniedError occured:',x

