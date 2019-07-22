#!/usr/bin/env python

import sys
import Pyro.core

Pyro.core.initClient()

proxy=Pyro.core.getProxyForURI("PYRONAME://:test.chain_A")
print "Result=",proxy.process(["hello"])


