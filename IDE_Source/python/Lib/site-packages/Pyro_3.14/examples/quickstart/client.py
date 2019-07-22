#!/usr/bin/env python

from Pyro.ext import remote

print 'getting remote object "quickstart"...'
test = remote.get_remote_object('quickstart')

print test.method1("Johnny")
print test.method2(42)

