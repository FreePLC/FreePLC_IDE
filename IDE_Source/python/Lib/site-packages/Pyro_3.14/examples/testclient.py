#
#	Test client utility startup code
#	Kind of verbose; all this could be done much simpler
#	by using PYRONAME:// or something, but it shows what is happening.
#

import sys
import Pyro.naming, Pyro.core, Pyro.protocol

group = ':test'  # the default namespace group for the tests

# objname = the name of the object which is used in the NS
# withAttrs = use a DynamicProxyWithAttrs or a regular DynamicProxy?
def getproxy(objName, withAttrs=0):
	# initialize the client and set the default namespace group
	Pyro.core.initClient()
	Pyro.config.PYRO_NS_DEFAULTGROUP=group

	# locate the NS
	locator = Pyro.naming.NameServerLocator()
	print 'Searching Naming Service...',
	ns = locator.getNS()
	print 'Naming Service found at',ns.URI.address,'('+(Pyro.protocol.getHostname(ns.URI.address) or '??')+') port',ns.URI.port

	# resolve the Pyro object
	print 'asking for object'
	try:
		URI=ns.resolve(objName)
		print 'URI:',URI
	except Pyro.core.PyroError,x:
		print 'Couldn\'t locate object, nameserver says:',x
		raise SystemExit

	# create a proxy for the Pyro object, and return that
	if withAttrs:
		return Pyro.core.getAttrProxyForURI(URI)
	else:
		return Pyro.core.getProxyForURI(URI)

