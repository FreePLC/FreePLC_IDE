#!/usr/bin/env python

import sys
from Pyro.ext import remote
import object

# if you don't like the objects to be registered in the Default namespace
# uncomment the following two lines, and use the 'nsc' tool to create
# the appropriate name group:
# import Pyro
# Pyro.config.PYRO_NS_DEFAULTGROUP=":mygroup"

print 'Providing local object as "quickstart"...'
remote.provide_local_object(object.myObject(), 'quickstart')

print 'Waiting for requests.'
sys.exit(remote.handle_requests(wait_time=2))

