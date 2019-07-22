#!/usr/bin/env python

#
#	Client that doesn't use the Name Server. Uses URI directly.
#

import sys
import Pyro.core

Pyro.core.initClient()

uri = raw_input('Enter the URI of the quote object: ')

print 'Creating proxy'

proxy=Pyro.core.getProxyForURI(uri)

print 'Getting some quotes...'
print proxy.quote()
print proxy.quote()

