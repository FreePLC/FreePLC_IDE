#!/usr/bin/env python

from Pyro.EventService.Clients import Publisher
from Pyro.errors import NamingError

import random, time

from threading import Thread


mustStop=0

class VehicleProducer(Publisher, Thread):
	directions = ('north','east','south','west')
	cars = ('Ford','Toyota','Chrysler','Vauxhall','Honda','BMW')
	colors = ('red','green','white','black','blue','yellow')

	def __init__(self,id):
		Publisher.__init__(self)
		Thread.__init__(self)
		self.id=id
	def nextVehicle(self):
		direction=random.choice(self.directions)
		car=random.choice(self.cars)
		color=random.choice(self.colors)
		self.publish('STRESSTEST.CARS.HEADING.'+direction, (color,car))
		print self.id,'published'

	def run(self):	
		print 'Producer running.'
		try:
			global mustStop
			while not mustStop:
				time.sleep(random.random()/10)
				self.nextVehicle()
			print 'Producer stopped.'
		except NamingError:
			print 'Cannot find service. Is the Event Service running?'

def main():
	threads=[]
	for i in range(10):
		vp=VehicleProducer(i)
		vp.start()
		threads.append(vp)

	try:
		while 1:
			time.sleep(10)
	except KeyboardInterrupt:
		global mustStop
		mustStop=1

	print 'Break-- waiting for threads to stop.'
	for vp in threads:
		vp.join()

if __name__=='__main__':
	main()

