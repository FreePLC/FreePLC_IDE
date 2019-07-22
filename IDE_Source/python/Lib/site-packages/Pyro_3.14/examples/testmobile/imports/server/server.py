#!/usr/bin/env python

#
#	The server that doesn't use the Name Server.
#

import sys, os
import Pyro.core
from Pyro.errors import PyroError

import answers.answer

if not Pyro.config.PYRO_MOBILE_CODE:
	print "\nWARNING: PYRO_MOBILE_CODE not enabled\n"
if Pyro.config.PYRO_XML_PICKLE=='gnosis' and Pyro.config.PYRO_GNOSIS_PARANOIA>=0:
	print "\nWARNING: Using gnosis xml pickle but PYRO_GNOSIS_PARANOIA needs to be -1\n"

class Test(Pyro.core.ObjBase):
	def __init__(self):
		Pyro.core.ObjBase.__init__(self)
	def method(self, argument):
		print "some method called on test class, arg=",argument
		# returning an answer object
		result=answers.answer.Answer("some answer")
		print "returning",result
		return result

Pyro.core.initServer()
daemon = Pyro.core.Daemon()
objectName='testmobile.imports'
uri=daemon.connect(Test(),objectName)

# enter the service loop.
print 'Server is ready for customers. I am not using the Name Server.'
print 'Object name is:',objectName
print 'The URI is: ',uri

daemon.requestLoop()

