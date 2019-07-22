#!/usr/bin/env python
import Pyro.naming
import Pyro.core
import chain
from Pyro.errors import PyroError,NamingError

Pyro.core.initServer()

daemon = Pyro.core.Daemon()
ns = Pyro.naming.NameServerLocator().getNS()
try:
    ns.createGroup(":test")
except NamingError:
    pass
daemon.useNameServer(ns)

objName='A'
nextName='B'

daemon.connect(chain.Chain(objName,nextName),':test.chain_'+objName)

# enter the service loop.
print 'Server started obj',objName
daemon.requestLoop()

