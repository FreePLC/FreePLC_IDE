from __future__ import with_statement
import Pyro.core
import Pyro.util

# a message bouncer. Passes messages back to the callback
# object, until a certain limit is reached.

class Bouncer(Pyro.core.CallbackObjBase):
	def __init__(self, name):
		Pyro.core.ObjBase.__init__(self)
		self.name=name
		self.count=0
		self.callbackMutex=Pyro.util.getLockObject()
	def register(self, callback):
		self.callback=callback
	def process(self,message):
		print 'in process',self.name
		if len(message)>=3:
			print "Back in",self.name,", message is large enough... stopping!"
			return ["complete at "+self.name+':'+str(self.count)]

		print "I'm",self.name,", bouncing back..."
		message.append(self.name)
		with self.callbackMutex:
			result=self.callback.process(message)
		self.count+=1
		result.insert(0,"passed on from "+self.name+':'+str(self.count))
		print 'returned from callback'
		return result
		
		
