#!/usr/bin/env python

import time
import Pyro.core

serv = Pyro.core.getProxyForURI("PYRONAME://oneway")

print "starting server using a oneway call"
serv._setOneway("start")
serv.start()
print "doing some stuff..."
time.sleep(4)
print "now contacting the server to see if it's done."
print "we are faster, so you should see a few attempts,"
print "until the server is finished."
while True:
    print "server done?"
    if serv.ready():
        print "yes!"
        break
    else:
        print "no, trying again"
        time.sleep(1)

print "getting the result from the server:",serv.result()
