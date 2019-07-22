import Pyro.core

Pyro.config.PYRO_MOBILE_CODE=1		# Enable mobile code

import clientmodule3
mobileobject=clientmodule3.MyClass()

print "sending object to server"
server = Pyro.core.getProxyForURI("PYROLOC://localhost:12233/MobileHierarchy")
result=server.process(mobileobject)
print "done, got result, method call:",result.method()


	
