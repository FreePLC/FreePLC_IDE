import params.base

class Parameter(params.base.ParameterBase):
	def __init__(self, name):
		params.base.ParameterBase.__init__(self, "name of base")
		self.name=name
	def method(self):
		print "I am parameter object ",self.name
