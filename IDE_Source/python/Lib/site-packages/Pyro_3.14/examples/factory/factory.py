import os
import Pyro.core

class Opel(Pyro.core.ObjBase):
	def name(s): return "Opel Astra coupe"
	def pid(s): return os.getpid()

class Honda(Pyro.core.ObjBase):
	def name(s): return "Honda S2000"
	def pid(s): return os.getpid()

class Ford(Pyro.core.ObjBase):
	def name(s): return "Ford Mustang"
	def pid(s): return os.getpid()
	
class CarFactory(Pyro.core.ObjBase):
	def pid(s): return os.getpid()
	def create(s, brand):
		if brand=='Ford':
			car = Ford()
		elif brand=='Honda':
			car = Honda()
		elif brand=='Opel':
			car = Opel()
		else:
			raise ValueError('unknown brand')
		s.getDaemon().connect(car)
		return car.getProxy()
		
