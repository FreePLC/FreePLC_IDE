#!/usr/bin/env python

import sys, os
import Pyro.core
from Pyro.errors import PyroError
import Pyro.naming

if not Pyro.config.PYRO_MOBILE_CODE:
	print "\nWARNING: PYRO_MOBILE_CODE not enabled\n"
if Pyro.config.PYRO_XML_PICKLE=='gnosis' and Pyro.config.PYRO_GNOSIS_PARANOIA>=0:
	print "\nWARNING: Using gnosis xml pickle but PYRO_GNOSIS_PARANOIA needs to be -1\n"

class Test(Pyro.core.ObjBase):
	def __init__(self):
		Pyro.core.ObjBase.__init__(self)
	def method2(self, argument):
		print "method2 called on test class, arg=",argument
		return "Server2 answer"

Pyro.core.initServer()
daemon = Pyro.core.Daemon()
ns=Pyro.naming.NameServerLocator().getNS()
daemon.useNameServer(ns)
objectName=':testmobile_passon_server2'
uri=daemon.connect(Test(),objectName)

# enter the service loop.
print 'Server2 is ready for customers.'
daemon.requestLoop()

