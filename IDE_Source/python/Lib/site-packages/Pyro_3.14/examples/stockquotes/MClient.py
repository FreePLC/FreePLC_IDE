#!/usr/bin/env python

from Pyro.EventService.Clients import Subscriber
from Server import symbols
from Pyro.errors import NamingError

class MatchStockSubscriber(Subscriber):
	def __init__(self, pattern):
		Subscriber.__init__(self)
		self.subscribeMatch(pattern)
	def event(self, event):
		print event.subject,'=',event.msg

pattern = '^STOCKQUOTE\\.S.*$'

try:
	listener=MatchStockSubscriber(pattern)
	print 'Listening on pattern',pattern
	listener.listen()
except NamingError:
	print 'Cannot find service. Is the Event Service running?'

