import sys, os
import Pyro.core

sys.path.insert(0,os.path.join(os.pardir,os.pardir))    # to find testserver.py

import testserver

Pyro.config.PYRO_MOBILE_CODE=1      # Enable mobile code


class MallObj(Pyro.core.ObjBase):
    def __init__(self):
        Pyro.core.ObjBase.__init__(self)
    def goShopping(self, shopper):
        print "shop3 goshopping:",shopper
        shopper.visit("Shop 3")
        return shopper
    def __call__(self):
        return self             # hack for testserver's delegation init

mall=MallObj()

# finally, start the server.
testserver.start(mall,'Shop3')

