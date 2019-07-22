
class ServerResult(object):
	def __init__(self, name):
		self.name=name
	def method(self):
		print "I am parameter object ",self.name
