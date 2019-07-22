#!/usr/bin/env python

import Pyro.naming
import Pyro.core

import connvalidator


class testobject(Pyro.core.ObjBase):
	def __init__(self):
		Pyro.core.ObjBase.__init__(self)
	def method(self,arg):
		caller = self.getLocalStorage().caller   # TCPConnection of the caller
		login = caller.authenticated   # set by the conn.validator
		return "You are '%s' and you were allowed to connect." % login


Pyro.core.initServer()

ns = Pyro.naming.NameServerLocator().getNS()

daemon = Pyro.core.Daemon()
daemon.useNameServer(ns)
daemon.setNewConnectionValidator( connvalidator.UserLoginConnValidator() )

daemon.connect(testobject(),'authentication')

print "---\nfor reference: the following users and passwords are recognised:"
print "user: root     password: change_me"
print "user: irmen    password: secret"
print "user: guest    password: guest"
print "(this table is printed for sake of example; the passwords"
print "  are not stored in plain text but as md5 hashes)"
print

# enter the service loop.
print 'Server started.'
daemon.requestLoop()
