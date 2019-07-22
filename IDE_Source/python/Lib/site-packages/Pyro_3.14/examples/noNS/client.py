#!/usr/bin/env python

#
#	Client that doesn't use the Name Server. Uses PYROLOC:// URI.
#

import sys
import Pyro.core

Pyro.core.initClient()

objectName = 'QuoteGenerator'
hostname = raw_input('Enter the hostname of the server: ')
port = raw_input('Enter the port of the server, or just enter: ')

print 'Creating proxy for object',objectName,' on ',hostname+':'+port

if port:
	URI='PYROLOC://'+hostname+':'+port+'/'+objectName
else:	
	URI='PYROLOC://'+hostname+'/'+objectName
print 'The URI is',URI

proxy=Pyro.core.getProxyForURI(URI)

print 'Getting some quotes...'
print proxy.quote()
print proxy.quote()

