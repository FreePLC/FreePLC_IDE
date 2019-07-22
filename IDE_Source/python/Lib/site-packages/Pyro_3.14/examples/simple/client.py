#!/usr/bin/env python

import Pyro.util
import Pyro.core

Pyro.core.initClient()

test = Pyro.core.getProxyForURI("PYRONAME://:test.simple")

print test.mul(111,9)
print test.add(100,222)
print test.sub(222,100)
print test.div(2.0,9.0)
print test.mul('.',10)
print test.add('String1','String2')

print '*** invoking server method that crashes ***'
try:
	print test.error()
except Exception,x:
	print "".join(Pyro.util.getPyroTraceback(x))

