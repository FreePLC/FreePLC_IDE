import Pyro.core
import Pyro.util
import clientparams.parameters

if not Pyro.config.PYRO_MOBILE_CODE:
	print "\nWARNING: PYRO_MOBILE_CODE not enabled\n"
if Pyro.config.PYRO_XML_PICKLE=='gnosis' and Pyro.config.PYRO_GNOSIS_PARANOIA>=0:
	print "\nWARNING: Using gnosis xml pickle but PYRO_GNOSIS_PARANOIA needs to be -1\n"

HOST="localhost"
URI = "PYROLOC://%s/testmobile.bothways"

HOST=raw_input("server host (empty for %s): " % HOST) or HOST	
obj=Pyro.core.getProxyForURI(URI % HOST)
# create a parameter of a class that the serve doesn't know about.
# Pyro's mobile code feature will supply the code to the server.
param = clientparams.parameters.ClientParameter("some name")
result=obj.method(param)
# the restut will be an 'unknown' object type !
# Pyro's mobile code feature will make the server supply the code to us as well.
print "result of calling remote object: ",result
print "name was: ",result.name
