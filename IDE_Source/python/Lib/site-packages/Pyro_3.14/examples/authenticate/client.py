#!/usr/bin/env python

import Pyro.naming, Pyro.core
import Pyro.errors

Pyro.core.initClient()
ident = raw_input('Enter authentication ID for NS ("s3cr3t"): ')

locator = Pyro.naming.NameServerLocator(identification=ident)  # note the ID
print 'Searching Naming Service...',
ns = locator.getNS()

print 'Naming Service found at',ns.URI.address,'port',ns.URI.port


print 'binding to object'
try:
    URI=ns.resolve(':test.authentication')
    print 'URI:',URI
except Pyro.core.PyroError,x:
    print 'Couldn\'t bind object, nameserver says:',x
    raise SystemExit

ident = raw_input('Enter authentication ID for Server ("s3cr3t"): ')
obj=Pyro.core.getProxyForURI(URI)
obj._setIdentification(ident)
result=obj.method('foo bar')
print "Result from method call: ",result

