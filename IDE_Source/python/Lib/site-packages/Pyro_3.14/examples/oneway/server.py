#!/usr/bin/env python
import Pyro.core
import Pyro.naming
import time

class server(Pyro.core.ObjBase):
    def __init__(self):
        Pyro.core.ObjBase.__init__(self)
        self.busy=False
    def start(self):
        print "start request received. Starting work..."
        self.busy=True
        for i in range(10):
            time.sleep(1)
            print 10-i
        print "work is done!"
        self.busy=False
    def ready(self):
        print "ready status requested (%r)" % (not self.busy)
        return not self.busy
    def result(self):
        return "The result :)"
      

######## main program

Pyro.config.PYRO_ONEWAY_THREADED = True			# try setting this to False and see what happens in the client

Pyro.core.initServer()

ns=Pyro.naming.NameServerLocator().getNS()

daemon=Pyro.core.Daemon()
daemon.useNameServer(ns)

uri=daemon.connect(server(),"oneway")

print "Server is ready."
daemon.requestLoop()
