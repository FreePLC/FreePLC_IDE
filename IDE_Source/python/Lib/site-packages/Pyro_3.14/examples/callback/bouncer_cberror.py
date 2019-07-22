import Pyro.core

# a message bouncer. Raises an error in the callback function!

# it is subclassed form CallbackObjBase, 
# so the error is also thrown on the client.

# If you change this to the regular ObjBase,
# you'll see that the error is silently passed back
# to the server, and the client never knows about it.

class Bouncer(Pyro.core.CallbackObjBase):
	def __init__(self, name):
		Pyro.core.ObjBase.__init__(self)
		self.name=name
		self.count=0
	def process(self,message,callback):
		print 'This is',self.name
		print 'I\'ll throw an exception...'
		raise ValueError("Some error in the callback function")
		
		
