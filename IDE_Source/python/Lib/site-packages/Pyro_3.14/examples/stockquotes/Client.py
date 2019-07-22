#!/usr/bin/env python

from Pyro.EventService.Clients import Subscriber
from Server import symbols
from Pyro.errors import NamingError

class StockSubscriber(Subscriber):
	def __init__(self, symbols):
		Subscriber.__init__(self)
		symbols=map(lambda s: 'STOCKQUOTE.'+s, symbols)
		self.subscribe(symbols)
	def event(self, event):
		print event.subject,'=',event.msg

print "Available stock quote symbols:"
for s in symbols:
	print '  ',s,
print 
symbols=raw_input("Enter comma separated stock symbols to listen to: ").split(',')

try:
	listener=StockSubscriber(symbols)
	print 'Listening!'
	listener.listen()
except NamingError:
	print 'Cannot find service. Is the Event Service running?'

