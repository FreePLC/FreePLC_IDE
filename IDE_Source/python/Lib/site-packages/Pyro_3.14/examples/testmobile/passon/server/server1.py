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
	def method1(self, argument):
		print "method1 called on test class, arg=",argument
		try:
			obj=Pyro.core.getProxyForURI("PYRONAME://:testmobile_passon_server2")
			print "calling method on server2, passing on argument"
			result="Server1 result;"
			result+=obj.method2(argument)
		except PyroError,x:
			print "Some error occured!",x
			result="there was an error in server1, see the console over there"	
		print "returning result:",result
		return result

Pyro.core.initServer()
Pyro.core.initClient()
ns=Pyro.naming.NameServerLocator().getNS()
daemon = Pyro.core.Daemon()
daemon.useNameServer(ns)
objectName=':testmobile_passon_server1'
uri=daemon.connect(Test(),objectName)

# enter the service loop.
print 'Server1 is ready for customers.'
daemon.requestLoop()

