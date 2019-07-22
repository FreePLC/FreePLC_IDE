#!/usr/bin/env python

import Pyro.core
import connvalidator
import getpass

login = raw_input('Enter user name: ')
password = getpass.getpass('Enter password: ')
ident = "%s:%s" % (login,password)

Pyro.core.initClient()
obj = Pyro.core.getProxyForURI("PYRONAME://authentication")
obj._setNewConnectionValidator( connvalidator.UserLoginConnValidator() )
obj._setIdentification( (login,password) )

# Try to call the method.
# If you supplied correct username/password, it will succeed.
result=obj.method('foo bar')
print "Result from method call: ",result

