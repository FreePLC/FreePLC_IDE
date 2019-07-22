#!/usr/bin/env python

#
#	The server that doesn't use the Name Server.
#

import sys, os
import Pyro.core
from Pyro.errors import PyroError

class QuoteGen(Pyro.core.ObjBase):
	def __init__(self):
		Pyro.core.ObjBase.__init__(self)
	def quote(self):
		try:
			quote=os.popen('fortune').read()
			if len(quote)>0:
				return quote
			return "This system cannot provide you a good fortune, install it"	
		except:		
			return "I know only this quote... but it came from the server!"
		
		
		
Pyro.core.initServer()

daemon = Pyro.core.Daemon()
print
print 'The Pyro Deamon is running on ',daemon.hostname+':'+str(daemon.port)
print '(you may need this info for the client to connect to)'
print

objectName='QuoteGenerator'

uri=daemon.connect(QuoteGen(),objectName)

# enter the service loop.
print 'QuoteGen is ready for customers. I am not using the Name Server.'
print 'Object name is:',objectName
print 'The URI is: ',uri

daemon.requestLoop()

