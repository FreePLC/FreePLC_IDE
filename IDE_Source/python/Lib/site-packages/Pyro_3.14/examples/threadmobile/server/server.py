#!/usr/bin/env python

#
#	The server that doesn't use the Name Server.
#

import threading, time
import sys, os
import Pyro.core
from Pyro.errors import PyroError
import outparams

if not Pyro.config.PYRO_MOBILE_CODE:
	raise SystemExit("PYRO_MOBILE_CODE not enabled")
if Pyro.config.PYRO_XML_PICKLE=='gnosis' and Pyro.config.PYRO_GNOSIS_PARANOIA>=0:
	raise SystemExit("Using gnosis xml pickle but PYRO_GNOSIS_PARANOIA needs to be -1")

class Test(Pyro.core.ObjBase):
	def __init__(self):
		Pyro.core.ObjBase.__init__(self)
	def method(self, argument):
		print threading.currentThread().getName(),"got invocation"
		print "some method called on test class, arg=",argument
		time.sleep(0.2)
		print "invoking method on argument object"
		argument.method()
		return outparams.ResultParameter(threading.currentThread().getName())

Pyro.core.initServer()

daemon = Pyro.core.Daemon()
print
print 'The Pyro Deamon is running on ',daemon.hostname+':'+str(daemon.port)
print '(you may need this info for the client to connect to)'
print

objectName='test.threadmobile'

uri=daemon.connect(Test(),objectName)

# enter the service loop.
print 'Server is ready for customers. I am not using the Name Server.'
print 'Object name is:',objectName
print 'The URI is: ',uri

daemon.requestLoop()

