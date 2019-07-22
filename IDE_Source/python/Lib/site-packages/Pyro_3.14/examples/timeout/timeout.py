import time
import Pyro.core
import Pyro.naming
from Pyro.errors import NamingError
from threading import Thread

class MySimpleServer(Thread):
    def __init__(self, daemon):
        super(MySimpleServer, self).__init__()
        self.__oDaemon = daemon
        self.__tIsRuning = False
        self.__tIsStopped = False
        self.setDaemon(True)

    def run(self):
        self.__tIsRunning = True
        while self.__tIsRunning:
            time.sleep(.1)
            self.__oDaemon.handleRequests(3)
        self.__oDaemon.shutdown()
        self.__tIsStopped = True
        print "server stopped."

    def stop(self):
        self.__tIsRunning = False

    def isStopped(self):
        return self.__tIsStopped


class MyObject(Pyro.core.ObjBase):
    def test(self):
        print 'test called'

Pyro.core.initServer()

oNs = Pyro.naming.NameServerLocator().getNS()
oDaemon = Pyro.core.Daemon()
oDaemon.useNameServer(oNs)


strTag = 'timeout_example'
try:
    oNs.unregister(strTag)
except NamingError:
    pass

oObj = MyObject()
strUri = oDaemon.connect(oObj, strTag)

oServer = MySimpleServer(oDaemon)
oServer.start()

oProxy = Pyro.core.getProxyForURI(strUri)
oProxy._setTimeout(4)

print 'calling remote method on live proxy.'
oProxy.test()
print 'success.'

print "stopping server..."
oServer.stop()
while not oServer.isStopped():
    time.sleep(.1)

print
print 'calling remote method on stale proxy.'
print 'because we specified a timeout, Pyro should take notice of this and throw a TimeoutException after a short while.'
oProxy = Pyro.core.getProxyForURI(strUri)
oProxy._setTimeout(4)
oProxy.test()
print 'This should not be shown!!! You should have seen a TimeoutException'
