#!/usr/bin/env python

from Pyro.EventService.Clients import Subscriber
from Pyro.errors import NamingError

class TrafficCounter(Subscriber):
	def __init__(self):
		self.subjPrefix="CARS.HEADING."
		Subscriber.__init__(self)
		self.patterns=['north','south','east','west']
		self.currentPattern=None
		self.counter=0
		self.subscribeNextPattern()
	def subscribeNextPattern(self):
		if self.currentPattern:
			self.unsubscribe(self.subjPrefix+self.currentPattern)
		try:
			self.currentPattern=self.patterns.pop()
			print 'I am now watching for cars heading',self.currentPattern
			self.subscribe(self.subjPrefix+self.currentPattern)
		except IndexError:
			print 'I watched all directions.'
			self.abort() # break from the event loop
	def event(self, event):
		(color,car)=event.msg
		print 'A',color,car,'went',event.subject[len(self.subjPrefix):]
		self.counter+=1
		if self.counter>=4:
			self.counter=0
			print "There were enough cars in that direction. Let's look somewhere else."
			self.subscribeNextPattern()

try:
	counter=TrafficCounter()
	print 'Going to count cars.'
	counter.listen()
	print 'Stopped counting cars.'
except NamingError:
	print 'Cannot find service. Is the Event Service running?'

