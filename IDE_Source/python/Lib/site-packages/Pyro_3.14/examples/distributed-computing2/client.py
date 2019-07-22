#!/usr/bin/env python
import Pyro.core
import Pyro.errors
import Queue
import random
from workitem import Workitem

NUMBER_OF_ITEMS = 40
Pyro.core.initClient()

numbers = {}

def processResult(item):
	print "Got result: %s (from %s)" % (item, item.processedBy)
	numbers[item.data] = item.result


def main():	
	print "\nThis program will calculate Prime Factorials of a bunch of random numbers."
	print "The more workers you will start (on different cpus/cores/machines),"
	print "the faster you will get the complete list of results!\n"
	dispatcher = Pyro.core.getProxyForURI("PYRONAME://:Distributed2.dispatcher")
	print "placing work items into dispatcher queue."
	for i in range(NUMBER_OF_ITEMS):
		number=random.randint(3211, 5000)*random.randint(177,3000)*37
		numbers[number] = None
		item = Workitem(i+1, number)
		dispatcher.putWork(item)
	print "getting results from dispatcher queue."
	resultCount=0
	while resultCount<NUMBER_OF_ITEMS:
		try:
			item = dispatcher.getResult()
			processResult(item)
			resultCount+=1
		except Queue.Empty:
			print "No results available yet. Work queue size:",dispatcher.workQueueSize()
	
	if dispatcher.resultQueueSize()>0:
		print "removing leftover results from the dispatcher"
		while True:
			try:
				item = dispatcher.getResult()
				processResult(item)
			except Queue.Empty:
				break

	print "\nComputed Prime Factorials follow:"
	for (number, factorials) in numbers.items():
		print number,"-->",factorials

if __name__=="__main__":
	main()
