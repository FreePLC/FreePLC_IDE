import Pyro.core
import Pyro.util
import params.parameters

if not Pyro.config.PYRO_MOBILE_CODE:
	print "\nWARNING: PYRO_MOBILE_CODE not enabled\n"
if Pyro.config.PYRO_XML_PICKLE=='gnosis' and Pyro.config.PYRO_GNOSIS_PARANOIA>=0:
	print "\nWARNING: Using gnosis xml pickle but PYRO_GNOSIS_PARANOIA needs to be -1\n"


HOST="localhost"
URI = "PYROLOC://%s/testmobile.imports"

HOST=raw_input("server host (empty for %s): " % HOST) or HOST	
obj=Pyro.core.getProxyForURI(URI % HOST)
p = params.parameters.Parameter("Some name")
try:
	result=obj.method(p)
	print "calling remote object: ",result
	print "calling result method:", result.getAnswer()
except Exception,x:
	print "".join(Pyro.util.getPyroTraceback(x))
