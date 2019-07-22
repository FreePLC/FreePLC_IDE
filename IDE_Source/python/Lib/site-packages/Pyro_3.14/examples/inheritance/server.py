#!/usr/bin/env python
import sys, os

sys.path.insert(0,os.pardir)	# to find testserver.py

import testserver

import Pyro.core
import inherit

######## testclass object

class testclass(Pyro.core.ObjBase, inherit.Fsub):
	def __init__(self):
		Pyro.core.ObjBase.__init__(self)

######## main program

testserver.start(testclass, 'inheritance')

