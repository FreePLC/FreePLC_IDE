#!/usr/bin/env python

from __future__ import with_statement
from Pyro.EventService.Clients import Subscriber
from Pyro.errors import NamingError
from threading import Thread
import Pyro.util
import time

class TrafficCounter(Subscriber,Thread):
	def __init__(self,id):
		self.subjPrefix="STRESSTEST.CARS.HEADING."
		Subscriber.__init__(self)
		Thread.__init__(self)
		self.patterns=['north','east','south','west']
		self.currentPattern=None
		self.counter=0
		self.id=id
		self.lock=Pyro.util.getLockObject()
		self.subscribeNextPattern()
	def subscribeNextPattern(self):
		# because this is called from an event,
		# and that may occur in multiple threads concurrently,
		# we need a lock on this.
		# If we don't, it's possible that multiple threads
		# access the same ES proxy concurrently --> HAVOC.
		with self.lock:
			if self.currentPattern:
				self.unsubscribe(self.subjPrefix+self.currentPattern)
			try:
				self.currentPattern=self.patterns.pop()
				print self.id,'I am now watching for cars heading',self.currentPattern
				self.subscribe(self.subjPrefix+self.currentPattern)
			except IndexError:
				print self.id,'I watched all directions. Start over.'
				self.patterns=['north','south','east','west']
				self.currentPattern=self.patterns.pop()
				self.subscribe(self.subjPrefix+self.currentPattern)
	def event(self, event):
		(color,car)=event.msg
		print self.id,'A',color,car,'went',event.subject[len(self.subjPrefix):]
		self.counter+=1
		if self.counter>=4:
			self.counter=0
			print self.id,"There were enough cars in that direction. Let's look somewhere else."
			self.subscribeNextPattern()

	def run(self):
		try:
			print self.id,'Going to count cars.'
			self.listen()
			print self.id,'Stopped counting cars.'
		except NamingError:
			print 'Cannot find service. Is the Event Service running?'


def main():
	threads=[]
	for i in range(20):
		tc=TrafficCounter(i)
		tc.start()
		threads.append(tc)

	try:
		while 1:
			time.sleep(10)
	except KeyboardInterrupt:
		print 'Break-- weating for threads to stop.'
		for tc in threads:
			tc.abort()
		for tc in threads:
			tc.join()

if __name__=='__main__':
	main()

