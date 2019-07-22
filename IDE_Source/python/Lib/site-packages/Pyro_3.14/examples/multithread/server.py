#!/usr/bin/env python
import sys, os, time

sys.path.insert(0,os.pardir)	# to find testserver.py

import testserver
import time
import Pyro.naming
import Pyro.core
from Pyro.errors import NamingError
from threading import currentThread

_timeval=0

def _cpu_delay():
	# try to do a 100% cpu time delay loop without using python bytecode
	try:
		import cPickle
		x=cPickle.dumps(range(100))
	except:
		import hmac
		x=hmac.new("somerandomthingie",str(range(100))).digest()

def determinePeriod():
	global _timeval
	print 'Determining how long to busy wait for 1 seconds'
	begin = time.time()
	i=0
	while (time.time()-begin) < 1.0:
		_cpu_delay()
		i+=1
	print 'That is',i
	_timeval=i
	return _timeval


######## testclass objects

class IOtestclass_delegate(object):
	def process(self, name, period):
		print 'called by',name
		print 'thread=',currentThread().getName()
		try:
			currentThread().localStorage.counter+=1
			print 'TLS.counter=',currentThread().localStorage.counter
		except AttributeError:
			print "No TLS available!"
		time.sleep(period)
		return 'READY!'

class CPUtestclass_delegate(object):
	def process(self,name, period):
		global _timeval
		print 'called by',name
		try:
			currentThread().localStorage.counter+=1
			print 'TLS.counter=',currentThread().localStorage.counter
		except AttributeError:
			print "No TLS available!"
		begin = time.time()
		print 'begin=',begin
		for i in range(period*_timeval):
			x=time.time()
			_cpu_delay()
		z=time.time()-begin	
		print 'ready in ',z,'sec  ',name



######## TLS INIT

def initTLS(tls):
	print "INIT TLS! TLS=",tls
	print "Setting counter for this TLS to 0."
	tls.counter=0


######## main program

def main():
	Pyro.config.PYRO_NS_DEFAULTGROUP=":test"
	if raw_input('multithreaded? y/n: ')=='y':
		Pyro.config.PYRO_MULTITHREADED = 1
		print 'Using multithreaded server.'
	else:
		Pyro.config.PYRO_MULTITHREADED = 0
		print 'Using singlethreaded server.'
	if raw_input('IO bound or CPU bound? io/cpu: ')=='io':
		testclass = IOtestclass_delegate
		print 'Using IO bound server.'
	else:
		testclass = CPUtestclass_delegate
		print 'Using CPU bound server.'
		determinePeriod()	

	print "Class used for server object:", testclass

	Pyro.core.initServer()

	daemon = Pyro.core.Daemon()
	ns = Pyro.naming.NameServerLocator().getNS()
	daemon.useNameServer(ns)

	# set TLS init func
	daemon.setInitTLS(initTLS)

	# make sure our namespace group exists
	try: ns.createGroup(":test")
	except NamingError: pass
	
	try: ns.unregister(":test.multithread")
	except NamingError: pass

	object=Pyro.core.ObjBase()  # delegate approach
	object.delegateTo(testclass())

	daemon.connect(object,"multithread")

	# enter the service loop.
	print "Server started"
	daemon.requestLoop()

if __name__=="__main__":
	main()



