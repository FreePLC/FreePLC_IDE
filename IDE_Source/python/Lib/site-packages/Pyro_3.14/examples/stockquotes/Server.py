#!/usr/bin/env python

from Pyro.EventService.Clients import Publisher
from Pyro.errors import NamingError

import random, time

symbols = ('SUN','MICROSOFT','IBM','ORACLE','SAP','NOVELL')

class StockMarket(Publisher):
	def __init__(self, symbols):
		Publisher.__init__(self)
		self.symbols=symbols
	def publishQuote(self):
		symbol=random.choice(self.symbols)
		quote =round(random.random()*100+50,2)
		print symbol,'=',quote
		self.publish('STOCKQUOTE.'+symbol, quote)

def main():
	try:
		market1 = StockMarket(symbols[:3])
		market2 = StockMarket(symbols[3:])

		print 'Publishing quotes.'
		while 1:
			time.sleep(random.random())
			market = random.choice( (market1, market2) )
			market.publishQuote()
	except NamingError:
		print 'Cannot find service. Is the Event Service running?'

if __name__=='__main__':
	main()

