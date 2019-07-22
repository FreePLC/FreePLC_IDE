#!/usr/bin/env python
import sys,os

sys.path.insert(0,os.pardir)		# to find testserver.py

import testserver

import Pyro.core
Pyro.config.PYRO_MULTITHREADING=0  

import bench

class benchimpl(Pyro.core.ObjBase, bench.bench):
	def __init__(self):
		Pyro.core.ObjBase.__init__(self)

######## main program

testserver.start(benchimpl, 'benchmark')


