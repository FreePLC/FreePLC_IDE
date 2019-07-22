#!/usr/bin/env python
import sys, os

sys.path.insert(0,os.pardir)	# to find testclient.py

import testclient

test = testclient.getproxy('inheritance')

print "base1.meth1? -->",test.meth1()		# should be base1.meth1
print "Fsub.meth2?  -->",test.meth2()		# should be Fsub.meth2
print "base2.meth3? -->",test.meth3()		# should be base2.meth3
print "Fsub.meth4?  -->",test.meth4()		# should be Fsub.meth4

