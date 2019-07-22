#!/usr/bin/env python
import sys, os

sys.path.insert(0,os.pardir)	# to find testserver.py

import testserver

import Pyro.core
import factory


###### For educational purposes, disable threads

Pyro.config.PYRO_MULTITHREADED=0

######## main program

print 'Server PID=', os.getpid()

testserver.start(factory.CarFactory,'factory')


