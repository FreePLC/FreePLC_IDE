#!/usr/bin/env python

import time
import Pyro.core
import Pyro.naming
from Pyro.errors import *


def main():
	Pyro.core.initClient()
	locator = Pyro.naming.NameServerLocator()
	NS = locator.getNS()
	server = Pyro.core.getProxyForURI(NS.resolve(':test.callback'))
	print 'Shouting something'
	server.shout('somebody there?')

if __name__=='__main__':
	main()
