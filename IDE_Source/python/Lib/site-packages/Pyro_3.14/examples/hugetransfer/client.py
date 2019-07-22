#!/usr/bin/env python
import sys, os

sys.path.insert(0,os.pardir)	# to find testclient.py

import testclient

obj = testclient.getproxy('hugetransfer')
#if os.name!="java":
#	object._setTimeout(4)

import time

basesize = 500000

data='A'*basesize

totalsize=0
begin=time.time()
for i in range(1,15):
	print 'transferring',basesize*i,'bytes'
	size=obj.transfer(data*i)
	# print " reply=",size
	totalsize=totalsize+basesize*i
duration=time.time()-begin

print 'It took',duration,'seconds to transfer',totalsize/1024,'kilobyte.'
print 'That is',totalsize/1024/duration,'k/sec. = ',totalsize/1024/1024/duration,'mb/sec.'

