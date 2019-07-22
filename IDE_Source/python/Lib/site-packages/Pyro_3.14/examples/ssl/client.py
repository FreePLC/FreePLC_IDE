#!/usr/bin/env python
import Pyro.core

Pyro.config.PYRO_DNS_URI=True
Pyro.config.PYROSSL_CERT="client.pem"
# Pyro.config.PYROSSL_KEY="client.key"

def sendMsg(obj):
	message="Irmen de Jong is a space alien"
	print
	print 'Sending secret message ('+message+')...'
	reply=obj.passSecretMessage(message)
	print 'I got a secret reply: ',reply
	print

print "First, connect using the Name Server (PYRONAME://)"
test = Pyro.core.getProxyForURI("PYRONAME://:test.ssl")
sendMsg(test)

print "Next, connect without using the Name Server (PYROLOCSSL://)"
host=raw_input("Enter the hostname where the SSL server is running: ")
test = Pyro.core.getProxyForURI("PYROLOCSSL://"+host+"/ssl")
sendMsg(test)

