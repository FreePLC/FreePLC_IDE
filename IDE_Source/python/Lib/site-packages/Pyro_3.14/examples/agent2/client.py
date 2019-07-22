#!/usr/bin/env python
import sys, os

from Pyro.errors import *
import Pyro.core

sys.path.insert(0,os.pardir)	# to find testclient.py
Pyro.config.PYRO_MOBILE_CODE=1		# Enable mobile code

import testclient
import agent.ShoppingAgent


# Get a proxy with attrs
mall = testclient.getproxy('ShoppingMall',True)

import sys, os, string
import Pyro.core

try:
	# just to show what happens: try to supply some bogus code
	print 'Supplying bogus code to server... see what happens:'
	mall.remote_supply_code('crash','this is no python code',333)
	print 'Server ACCEPTED!!! You should not see this!!!'
except PyroError,x:
	print 'remote_supply_code failed:',x

print


Harry = agent.ShoppingAgent.ShoppingAgent('Harry')
Harry.cashLimit(500)
Harry.shoppingList(['tv', 'mouse', 'bananas', 'boots', 'snowboard', 'goggles'])

Joyce = agent.ShoppingAgent.ShoppingAgent('Joyce')
Joyce.cashLimit(3200)
Joyce.shoppingList(['bananas','mouse','computer','cd','spices','apples','boots'])

try:
	print 'Harry goes shopping...'
	Harry=mall.goShopping(Harry)		# note that agent returns as result value
	Harry.result()
	Harry.describeObjects()
	print
	print 'Joyce goes shopping...'
	Joyce=mall.goShopping(Joyce)		# note that agent returns as result value
	Joyce.result()
	Joyce.describeObjects()
	print
except Exception,x:
	import Pyro.util
	print ''.join(Pyro.util.getPyroTraceback(x))
