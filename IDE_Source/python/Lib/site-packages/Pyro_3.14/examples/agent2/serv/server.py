#!/usr/bin/env python

# This server code is nearly the same as server.py from the agent example.
# except for the path insert because it has to look 1 dir higher,
# the fact that it enables PYRO_MOBILE_CODE,
# and that it sets a codeValidator for our Pyro object.

# NOTE that there is no ShoppingAgent module available here!!!
#      It will be downloaded from the client.


import sys, os
import Pyro.core

sys.path.insert(0,os.path.join(os.pardir,os.pardir))	# to find testserver.py

import testserver
import shop

Pyro.config.PYRO_MOBILE_CODE=1		# Enable mobile code


s1=shop.Shop("Fry's")
s1.setStock( { 'tv':2000, 'computer':3000, 'mouse':10, 'cd': 19 } )
s2=shop.Shop("Fred's groceries")
s2.setStock( { 'apples':5, 'tomatoes':9, 'bananas':4, 'spices': 3 } )
s3=shop.Shop("Rockport store")
s3.setStock( { 'shoes':150, 'boots':190 } )
s4=shop.Shop("Snow world")
s4.setStock( { 'snowboard':400, 'bindings': 150, 'goggles':80, 'wax':12 } )

# start the mall. We cannot start the testserver in delegation mode
# directly because we have to call setCodeValidator from the core.ObjBase!
# So create a subclass from ObjBase and our Mall.

class MallObj(Pyro.core.ObjBase, shop.Mall):
	def __init__(self):
		Pyro.core.ObjBase.__init__(self)
		shop.Mall.__init__(self)

mall=MallObj()
mall.addShop(s1)
mall.addShop(s2)
mall.addShop(s3)
mall.addShop(s4)

def codeValidator(n,m,a):
	# This codevalidator only accepts ShoppingAgent uploads
	# and object.* downloads.
	# As an example, to accept all modules in the agent package:
	# change it to return n.startswith('agent.')
	if m and a:
		return n=='agent.ShoppingAgent'			# client uploads to us
	else:
		return n.startswith("objects.")			# client downloads from us

# set a custom codeValidator because the default validator
# will accept ALL incoming code (HAZARDOUS).
mall.setCodeValidator(codeValidator)

# finally, start the server.
testserver.start(mall,'ShoppingMall')

