#!/usr/bin/env python

# This server connects to the Event server directly,
# it doesn't use the name server but requires a direct URI.

from Pyro.EventService.Clients import Publisher

import random, time

symbols = ('SUN','MICROSOFT','IBM','ORACLE','SAP','NOVELL')

class StockMarket(Publisher):
	def __init__(self, symbols, es_URI):
		Publisher.__init__(self, esURI=es_URI)
		self.symbols=symbols
	def publishQuote(self):
		symbol=random.choice(self.symbols)
		quote =round(random.random()*100+50,2)
		print symbol,'=',quote
		self.publish('STOCKQUOTE.'+symbol, quote)

def main():
	es_URI = raw_input("enter URI of the Event Server: ")
	market1 = StockMarket(symbols[:3], es_URI)
	market2 = StockMarket(symbols[3:], es_URI)

	print 'Publishing quotes.'
	while 1:
		time.sleep(random.random())
		market = random.choice( (market1, market2) )
		market.publishQuote()

if __name__=='__main__':
	main()

