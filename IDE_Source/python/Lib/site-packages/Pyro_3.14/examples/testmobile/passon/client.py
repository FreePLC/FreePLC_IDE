import Pyro.core
import Pyro.util
import params.parameters

obj=Pyro.core.getProxyForURI("PYRONAME://:testmobile_passon_server1")
p = params.parameters.Parameter("Some name")
print "calling remote object: ",obj.method1(p)
