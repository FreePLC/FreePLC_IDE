#!/usr/bin/env python
import sys, os

from Pyro.errors import *
import Pyro.core
import Pyro.util

sys.path.insert(0,os.pardir)	# to find testclient.py

import testclient

import agent.ShoppingAgent

Pyro.config.PYRO_MOBILE_CODE=1		# Enable mobile code

# Get a proxy with attrs 
mall = testclient.getproxy('Shop1',True)

Harry = agent.ShoppingAgent.ShoppingAgent('Harry')
Joyce = agent.ShoppingAgent.ShoppingAgent('Joyce')

try:
	print 'Harry goes shopping...'
	Harry=mall.goShopping(Harry)		# note that agent returns as result value
	Harry.result()
	print
	print 'Joyce goes shopping...'
	Joyce=mall.goShopping(Joyce)		# note that agent returns as result value
	Joyce.result()
	print
except Exception,x:
	print ''.join(Pyro.util.getPyroTraceback(x))
