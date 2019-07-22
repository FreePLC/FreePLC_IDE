import Pyro.core

# a message bouncer. Passes messages back to the callback
# object, until a certain limit is reached.

class Bouncer(Pyro.core.CallbackObjBase):
	def __init__(self, name):
		Pyro.core.ObjBase.__init__(self)
		self.name=name
		self.count=0
	def process(self,message,callback):
		if len(message)>=100:
			print "Back in",self.name,", message is large enough... stopping!"
			return ["complete at "+self.name+':'+str(self.count)]

		print "I'm",self.name,", bouncing back..."
		message.append(self.name)
		try:
			# note that we can use the callback proxy directly because it has
			# been passed in as a parameter to this method. That means that
			# Pyro has already taken care of transfering control to the current thread.
			result=callback.process(message, self.getProxy())
			self.count+=1
			result.insert(0,"passed on from "+self.name+':'+str(self.count))
			return result
		except Exception,x:
			print "Error occurred in callback object:",x
		
		
