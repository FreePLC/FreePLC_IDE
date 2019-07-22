#!/usr/bin/env python
import sys, os
import Pyro.util

sys.path.insert(0,os.pardir)	# to find testclient.py

import testclient

# Get a proxy with attrs 
test = testclient.getproxy('attributes',True)

name = raw_input('Enter a name: ')

# new way of doing things:
# direct attribute access!

print 'current sum=',test.sum
print 'last changed by',test.changedby

test.sum = test.sum+1
test.changedby = name

print 'new sum=',test.sum

# creating some new attributes
test.newattr1 = 'new_one'
test.newattr2 = 'new_two'

print 'new attr 1=',test.newattr1
print 'new attr 2=',test.newattr2

print 'Getting nested attribute from person object'
print 'name=',test.person.name
print ' age=',test.person.age
print 'Getting nested attrs using methods from person object'
print 'name=',test.person.getName()
print ' age=',test.person.getAge()

print '(the next attribute access should raise an exception)'
try:
	print 'not existing=',test.notexisting
except Exception,x:
	print "".join(Pyro.util.getPyroTraceback(x))


