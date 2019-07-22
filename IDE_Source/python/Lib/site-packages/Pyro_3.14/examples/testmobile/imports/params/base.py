
class ParameterBase(object):
	def __init__(self, basename):
		self.basename=basename
	def basemethod(self):
		print "I am parameterbase object ",self.basename
