#!/usr/bin/env python
import sys, os

sys.path.insert(0,os.pardir)	# to find testserver.py

import testserver

import Pyro.core

######## testclass object

class testclass(object):
	def transfer(self,data):
		print 'received',len(data),'bytes'
		return len(data)

######## main program

testserver.start(testclass, 'hugetransfer', delegate=1)


