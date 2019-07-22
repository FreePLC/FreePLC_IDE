# Autoreconnect server
# doesn't use the Name Server

import time, Pyro.core

class testobject(Pyro.core.ObjBase):
	def method(self,arg):
		print 'You can now try to stop this server with ctrl-C'
		time.sleep(1)

daemon = Pyro.core.Daemon()
object=testobject()
fixed_guid="a9fe57de0a3862c9b31b925b97a98d8a" # use some fixed random GUID
object.setGUID(fixed_guid)
daemon.connect(object,':test.autoreconnect')
print 'Fixed object guid =',fixed_guid
print 'Server started.'
daemon.requestLoop()
