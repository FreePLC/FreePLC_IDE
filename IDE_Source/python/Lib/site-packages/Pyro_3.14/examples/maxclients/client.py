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
    URI=ns.resolve('maxclients')
    print 'URI:',URI
except Pyro.core.PyroError,x:
    print 'Couldn\'t bind object, nameserver says:',x
    raise SystemExit


print '---- trying to create a bunch of proxy objects'
objects=[]
for i in range(20):
	ok=0
	while not ok:
		try:
			print 'creating proxy object',i
			obj=Pyro.core.getProxyForURI(URI)
			# Pyro 1.2+ notice: the following method call
			# actually binds the object. Just creating a proxy
			# doesn't. You can create many, many proxies without
			# a single connection to the server. Try commenting
			# the setname call out and notice that all proxies
			# are created successfully, and a crash occurs only
			# later on. (line 66, where a method call is made and
			# the object is connected).
			obj.setname(i)	# remote name
			obj.__dict__['localname']=i # local (proxy) name
			objects.append(obj)
			ok=1
		except Pyro.errors.ConnectionDeniedError,x:
			# Server denied the new connection.
			# A possible solution is to delete another one we don't need
			# anymore and to try again.
			print 'Error creating proxy object:',x
			print ' -> removing old proxy and trying again...'
			if objects:
				del objects[0]
			

for obj in objects:
	print 'object',id(obj),'is called remotely:',obj.getname(), 'and locally:',obj.__dict__['localname']

