import Pyro.core
import Pyro.util
import params.parameters

HOST="localhost"
URI = "PYROLOC://%s/testmobile.client2server"

HOST=raw_input("server host (empty for %s): " % HOST) or HOST	
obj=Pyro.core.getProxyForURI(URI % HOST)
p = params.parameters.Parameter("Some name")
print "calling remote object: ",obj.method(p)
