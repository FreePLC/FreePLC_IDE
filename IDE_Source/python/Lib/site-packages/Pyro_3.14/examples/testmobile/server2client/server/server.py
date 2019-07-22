#!/usr/bin/env python

#
#	The server that doesn't use the Name Server.
#

import sys, os
import Pyro.core
from Pyro.errors import PyroError
import params.parameters

if not Pyro.config.PYRO_MOBILE_CODE:
	print "\nWARNING: PYRO_MOBILE_CODE not enabled\n"
if Pyro.config.PYRO_XML_PICKLE=='gnosis' and Pyro.config.PYRO_GNOSIS_PARANOIA>=0:
	print "\nWARNING: Using gnosis xml pickle but PYRO_GNOSIS_PARANOIA needs to be -1\n"

class Test(Pyro.core.ObjBase):
	def __init__(self):
		Pyro.core.ObjBase.__init__(self)
	def method(self, argument):
		print "some method called on test class, arg=",argument
		# create object of a type that that client does not know about,
		# so Pyro's mobile code featuer will also pass the (module)code
		# back to the client.
		return params.parameters.Parameter(argument)

Pyro.core.initServer()
daemon = Pyro.core.Daemon()
objectName='testmobile.server2client'
uri=daemon.connect(Test(),objectName)

# enter the service loop.
print 'Server is ready for customers. I am not using the Name Server.'
print 'Object name is:',objectName
print 'The URI is: ',uri

daemon.requestLoop()

