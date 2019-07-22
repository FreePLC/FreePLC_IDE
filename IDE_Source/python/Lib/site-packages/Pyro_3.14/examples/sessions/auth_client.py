#!/usr/bin/env python
import Pyro.core, Pyro.protocol
import threading, time, sys, copy

# worker thread code

def processing(username, proxy):
	print "Processing started for user ",username
	time.sleep(0.5)
	proxy.init()
	for i in range(30):
		sys.stdout.write(username+" ")
		sys.stdout.flush()
		proxy.addline("little text line")
		time.sleep(0.1)
	print "Stop processing for user "+username
	proxy.close()



# the Connection Validator, client side
# This is only an example, don't use it like this in your own code!
class SimpleClientsideConnValidator(Pyro.protocol.DefaultConnValidator):
	def createAuthToken(self, authid, challenge, peeraddr, URI, daemon):
		# make a single string out of the ident tuple
		return "%s:%s" % (authid[0], authid[1])
	def mungeIdent(self, ident):
		# for simplicity's sake we just return the ident verbatim (username, password)
		return (ident[0], ident[1])


# start a set of threads, 1 per user, which perform requests

users=["peter","nancy","wendy","vince","steve"]
password = "secretpassw0rd"

storageProxy = Pyro.core.getProxyForURI("PYRONAME://:test.datastorage_auth")
storageProxy._setNewConnectionValidator( SimpleClientsideConnValidator() )

for username in users:
	# every thread needs its own user identification!
	# so make a copy of the proxy and set the identification token.
	proxy = copy.copy(storageProxy)
	proxy._setIdentification( (username, password) )
	thread = threading.Thread(target=processing, args=(username, proxy))
	thread.daemon=False
	thread.start()

print "Wait for threads to finish."
