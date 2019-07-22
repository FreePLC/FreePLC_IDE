#!/usr/bin/env python
import Pyro.core
import threading, time

NUMTHREADS=5

test = Pyro.core.getProxyForURI("PYRONAME://:test.threadstorage")

print "Will reuse the proxy in all threads."
print "Observe in the server console that the TLS counter is the same counter for all calls. "

def processing(index, proxy):
	print 'Processing started',index
	while threading.currentThread().running:
		t1 = time.time()
		print index, "CALLING...."
		proxy.process("thread_"+str(index))
		time.sleep(NUMTHREADS+1)
	print "exiting thread",index


# start a set of threads which perform requests

threads=[]
for i in range(NUMTHREADS):
	thread = threading.Thread(target=processing, args=(i, test))
	threads.append(thread)
	thread.running=True
	time.sleep(0.5)
	thread.start()

void=raw_input('\nPress enter to stop...\n\n')
print "Stopping threads."
for p in threads:
	p.running=False
for p in threads:
	p.join()
	print 'stopped',p.getName()

print 'Graceful exit.'
