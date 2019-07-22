#!/usr/bin/env python

#
#	Naming example. Shows basic name server handling.
#

import Pyro.naming

from Pyro.errors import PyroError,NamingError
from Pyro.protocol import getHostname

group = ':test'   # the namespace group for all test servers


#------------------------------------------------- subroutines --------------

# join: join 2 name components to form one name
def join(part1,part2):
	if part2[0]==':':
		return part2
	elif part1==':':
		return part1+part2
	else:
		return part1+'.'+part2
	
# dumpNamespace: print a flat dump of all object names in the namespace
def dumpNamespace(ns):
	print '--- namespace flat dump ---'
	flat = ns.flatlist()
	for (name, value) in flat:
		print '  ',name,'-->',value
	print '-------'

# _listsub: recursive helper for listNamespace
def _listsub(ns, parent,name,level):
	newgroup = join(parent,name)
	list = ns.list(newgroup)
	print '    '*level+'['+name+']'
	for (subname,type) in list:
		if type==0:		# group
			_listsub(ns,newgroup,subname,level+1)
		elif type==1:	# object name
			print '    '*(1+level)+subname

# listNamespace: print the namespace in a recursive tree format
def listNamespace(ns):
	print '--- namespace tree listing ---'
	_listsub(ns,'',':',0)
	print '-------'


#------------------------------------------------- main program --------------

# initialize the server and set the default namespace group
Pyro.core.initServer()
Pyro.config.PYRO_NS_DEFAULTGROUP=group
print 'Default group changed to',group

# locate the NS
locator = Pyro.naming.NameServerLocator()
print 'searching for Naming Service...'
ns = locator.getNS()

print 'Naming Service found at',ns.URI.address,'('+(Pyro.protocol.getHostname(ns.URI.address) or '??')+') port',ns.URI.port

# make sure our namespace group exists
try:
	ns.deleteGroup(group)	# delete it and all stuff that's still in it
except NamingError:
	pass
ns.createGroup(group)	# create it again

print 'Created name group',group
print 'Creating some subgroups...'
ns.createGroup('group1')
ns.createGroup('group2')
ns.createGroup('group3')
ns.createGroup(join('group3','group3a'))		# subgroup
ns.createGroup(join('group3','group3b'))		# subgroup
ns.createGroup(join('group3',join('group3b','deeplynested')))		# subgroup
ns.createGroup('group3/notasubgroup')	# / is not a name separator, so this is not a subgroup
raw_input("Created some groups. Press enter to see them.")
dumpNamespace(ns)
listNamespace(ns)
raw_input("That were the groups. Press enter to register some objects.")

print 'Registering some objects...'
URI='PYRO://localhost/12345678-12345678-12345678-12345678'
ns.register('def_obj1',URI)
ns.register('def_obj2',URI)
ns.register('def_obj3',URI)
ns.register(join('group1','def_obj1a'),URI)
ns.register(join('group1','def_obj1b'),URI)
ns.register(join('group2','def_obj2a'),URI)
ns.register(join('group2','def_obj2b'),URI)
ns.register(join('group3',join('group3a','someobject')),URI)
ns.register(join('group3',join('group3b',join('deeplynested','deepobject'))),URI)
raw_input("Registered some objects. Press enter to see them.")

dumpNamespace(ns)
listNamespace(ns)
raw_input("That were the objects. Press enter to continue.")

name = join('group3',join('group3b',join('deeplynested','deepobject')))
print 'Full name of',name,'is:',ns.fullName(name)
grp = ns.fullName(join('group3',join('group3b','deeplynested')))
Pyro.config.PYRO_NS_DEFAULTGROUP = grp
print 'Default group changed to',grp
name = 'deepobject'
print 'Full name of',name,'is:',ns.fullName(name)
Pyro.config.PYRO_NS_DEFAULTGROUP = group
print 'Default group changed back to',group

raw_input("Press enter to clean up.")
print 'Cleaning up...'
ns.deleteGroup('group1')
ns.deleteGroup('group2')
ns.deleteGroup('group3')
ns.deleteGroup('group3/notasubgroup')
ns.unregister('def_obj1')
ns.unregister('def_obj2')
ns.unregister('def_obj3')
ns.deleteGroup(group)

print "done!"
