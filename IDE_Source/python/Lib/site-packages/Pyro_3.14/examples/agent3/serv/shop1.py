import sys, os
import Pyro.core

sys.path.insert(0,os.path.join(os.pardir,os.pardir))    # to find testserver.py

import testserver

Pyro.config.PYRO_MOBILE_CODE=1      # Enable mobile code


class MallObj(Pyro.core.ObjBase):
    def __init__(self):
        Pyro.core.ObjBase.__init__(self)
    def goShopping(self, shopper):
        print "shop1 goshopping:",shopper
        shopper.visit("Shop 1")
        try:
            shop2=Pyro.core.getProxyForURI("PYRONAME://Shop2")
        except Exception,x:
            print "ERROR FINDING SHOP 2!!",x
        else:
            shopper=shop2.goShopping(shopper) # hop to next shop
        return shopper
    def __call__(self):
        return self             # hack for testserver's delegation init

mall=MallObj()

# finally, start the server.
testserver.start(mall,'Shop1')

