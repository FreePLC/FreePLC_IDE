#!/usr/bin/env python
import sys, os

sys.path.insert(0,os.pardir)		# to find testclient.py

import testclient
import Pyro.util

from excep import MyError

test = testclient.getproxy('exceptions')

print test.div(2.0,9.0)
try:
	print 2/0
except ZeroDivisionError,x:
	print 'DIVIDE BY ZERO',x
try:
	print test.div(2,0)
except ZeroDivisionError,x:
	print 'DIVIDE BY ZERO',x
try:
	result=test.error()
	print repr(result),result
except ValueError,x:
	print 'VALUERROR',x
try:
	result=test.error2()
	print repr(result),result
except ValueError,x:
	print 'VALUERROR',x
try:
	result=test.othererr()
	print repr(result),result
except MyError,x:
	print 'MYERROR',x
try:
	result=test.othererr2()
	print repr(result),result
except MyError,x:
	print 'MYERROR',x

print '*** invoking server method that crashes, catching traceback ***'
try:
	print test.complexerror()
except Exception,x:
	print 'CAUGHT ERROR, printing Pyro traceback >>>>>>',x
	print ''.join(Pyro.util.getPyroTraceback(x))
	print '<<<<<<< end of Pyro traceback'
	
print '*** invoking server method that crashes, not catching anything ***'
print test.complexerror()

