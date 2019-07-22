#!/usr/bin/env python
import sys, os, random

import time
import threading

sys.path.insert(0,os.pardir)	# to find testclient.py

import testclient

count = int(raw_input('Number of parallel clients: '))


test = testclient.getproxy('multithread')

testObjects=[test]

for i in range(count-1):
	testObjects.append(test.__copy__())

processtime = 1.0

def processing(index, proxy):
	thread=threading.currentThread()
	name=thread.getName()
	time.sleep(random.randint(1,5))
	print 'Processing started',name
	while threading.currentThread().running:
		t1 = time.time()
		print name, "CALLING...."
		print name, proxy.process(name,processtime),
		span = time.time() - t1
		print 'It took %.2f sec' % span
	print "exiting thread",name


# start a set of threads which perform requests

print
print 'I will create a set of threads which run concurrently.'
print 'Each thread invokes the remote object with a process time of',processtime,'seconds.'
print 'The remote object will wait that long before completion.'
print 'If the remote server is singlethreaded, each invocation is processed sequentially and has to wait for the previous one to complete. This will result in processing times longer than the specified amount!'
print 'If the remote server is multithreaded, all remote invocations are processed in parallel and will complete exactly after the specified process time.'

threads=[]
for i in range(count):
	thread = threading.Thread(target=processing, args=(i, testObjects[i]))
	threads.append(thread)
	thread.running=True
	thread.start()

void=raw_input('\nPress enter to stop...\n\n')
for p in threads:
	p.running=False
for p in threads:
	p.join()
	print 'stopped',p.getName()

print 'Graceful exit.'

