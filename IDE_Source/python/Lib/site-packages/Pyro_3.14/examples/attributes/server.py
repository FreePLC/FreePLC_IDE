#!/usr/bin/env python
import sys, os
import Pyro.core
from Person import Person

sys.path.insert(0,os.pardir)	# to find testserver.py

import testserver

######## testclass object (subclassed from ObjBase)
class testclass(Pyro.core.ObjBase):
	def __init__(self):
		Pyro.core.ObjBase.__init__(self)
		self.sum=0
		self.changedby=''

		# the following only works because Person is in a separate module
		# that is also available to the client:
		self.person=Person("Irmen de Jong","30")
		

######## testclass object (standalone - delegate approach)
class testclass2(object):
	def __init__(self):
		self.sum=0
		self.changedby=''

		# the following only works because Person is in a separate module
		# that is also available to the client:
		self.person=Person("Irmen de Jong","30")


######## main program

testserver.start(testclass,'attributes')


