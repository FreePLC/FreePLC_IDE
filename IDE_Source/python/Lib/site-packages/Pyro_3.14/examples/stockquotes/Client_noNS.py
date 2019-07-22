#!/usr/bin/env python

# This client connects to the Event server directly,
# it doesn't use the name server but requires a direct URI.

from Pyro.EventService.Clients import Subscriber
from Server import symbols

class StockSubscriber(Subscriber):
	def __init__(self, symbols, es_URI):
		Subscriber.__init__(self, esURI=es_URI)
		symbols=map(lambda s: 'STOCKQUOTE.'+s, symbols)
		self.subscribe(symbols)
	def event(self, event):
		print event.subject,'=',event.msg

print "Available stock quote symbols:"
for s in symbols:
	print '  ',s,
print 
symbols=raw_input("Enter comma separated stock symbols to listen to: ").split(',')
es_URI = raw_input("enter URI of the Event Server: ")

listener=StockSubscriber(symbols, es_URI)
print 'Listening!'
listener.listen()

