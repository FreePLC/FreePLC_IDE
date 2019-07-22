####### Special object

class Person(object):
	def __init__(self, name, age):
		self.name=name
		self.age=age

	def getName(self):
		return 'My name is '+self.name
	def getAge(self):
		return self.age
