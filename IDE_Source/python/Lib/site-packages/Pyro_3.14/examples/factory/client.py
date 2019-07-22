#!/usr/bin/env python
import sys, os

sys.path.insert(0, os.pardir)	# to find testclient.py

import testclient

fact = testclient.getproxy('factory')

print 'Local Python PID =', os.getpid()

c1=fact.create('Opel')
c2=fact.create('Ford')
c3=fact.create('Honda')

print 'Factory produced three cars (of three different brands).'
print 'Each object\'s PID is printed after its name. The PID'
print 'is different than the local Python PID above: its the PID'
print 'from the server process (the factory) that produced them!'
print '(look in the server window to see what its PID is).'
print c1.name(), 'pid=',c1.pid()
print c2.name(), 'pid=',c2.pid()
print c3.name(), 'pid=',c3.pid()


