#!/usr/bin/env python

from Pyro.EventService.Clients import Publisher
from Pyro.errors import NamingError

import random, time


class VehicleProducer(Publisher):
	directions = ('north','east','south','west')
	cars = ('Ford','Toyota','Chrysler','Vauxhall','Honda','BMW')
	colors = ('red','green','white','black','blue','yellow')

	def nextVehicle(self):
		direction=random.choice(self.directions)
		car=random.choice(self.cars)
		color=random.choice(self.colors)
		print color,car,'heading',direction
		self.publish('CARS.HEADING.'+direction, (color,car))

def main():
	try:
		producer=VehicleProducer()

		print 'Starting traffic.'
		while 1:
			time.sleep(random.random())
			producer.nextVehicle()
	except NamingError:
		print 'Cannot find service. Is the Event Service running?'

if __name__=='__main__':
	main()

