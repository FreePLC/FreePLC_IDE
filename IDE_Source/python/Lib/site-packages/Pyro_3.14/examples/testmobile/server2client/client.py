import Pyro.core
import Pyro.util

if not Pyro.config.PYRO_MOBILE_CODE:
	print "\nWARNING: PYRO_MOBILE_CODE not enabled\n"
if Pyro.config.PYRO_XML_PICKLE=='gnosis' and Pyro.config.PYRO_GNOSIS_PARANOIA>=0:
	print "\nWARNING: Using gnosis xml pickle but PYRO_GNOSIS_PARANOIA needs to be -1\n"


HOST="localhost"
URI = "PYROLOC://%s/testmobile.server2client"

HOST=raw_input("server host (empty for %s): " % HOST) or HOST	
obj=Pyro.core.getProxyForURI(URI % HOST)
result=obj.method("some name")   # this will be an 'unknown' object type !
print "result of calling remote object: ",result
print "name was: ",result.name

