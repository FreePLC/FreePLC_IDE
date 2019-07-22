#!/usr/bin/env python
import sys,os,time
import Pyro.protocol

sys.path.insert(0,os.pardir)		# to find testclient.py

import testclient
import bench

object = testclient.getproxy('benchmark')
object._setOneway('oneway')

def f1(): void=object.length('Irmen de Jong')
def f2(): void=object.timestwo(21)
def f3(): void=object.bigreply()
def f4(): void=object.manyargs(1,2,3,4,5,6,7,8,9,10,11,12,13,14,15)
def f5(): void=object.noreply(99993333)
def f6(): void=object.varargs('een',2,(3,),[4])
def f7(): void=object.keywords(arg1='zork')
def f8(): void=object.echo('een',2,(3,),[4])
def f9(): void=object.meth1('stringetje')
def fa(): void=object.meth2('stringetje')
def fb(): void=object.meth3('stringetje')
def fc(): void=object.meth4('stringetje')
def fd(): void=object.bigarg('Argument'*50)
def fe(): void=object.oneway('stringetje',432423434)
def ff(): void=object.mapping( {"aap":42, "noot": 99, "mies": 987654} )

funcs = (f1,f2,f3,f4,f5,f6,f7,f8,f9,fa,fb,fc,fd,fe,ff)

print '-------- BENCHMARK REMOTE OBJECT ---------'
print 'Pay attention to the "fe" test -- this is a Oneway call and is *fast*'
print '(if you are running the server and client on different machines)'
begin = time.time()
iters = 1000
for f in funcs:
	print iters,'times',f.__name__,
	sys.stdout.flush()
	voor = time.time()
	for i in range(iters):
		f()
	print '%.4f' % (time.time()-voor)
duration = time.time()-begin
print 'total time %.4f seconds' % duration
amount=len(funcs)*iters
print 'total method calls',amount
avg_pyro_msec = 1000.0*duration/amount
print 'avg. time per method call: %.4f msec (%d/sec)' % (avg_pyro_msec,amount/duration)

print '-------- BENCHMARK LOCAL OBJECT ---------'
object=bench.bench()
begin = time.time()
iters = 200000
for f in funcs:
	print iters,'times',f.__name__,
	voor = time.time()
	for i in range(iters):
		f()
	print '%.4f' % (time.time()-voor)
duration = time.time()-begin
print 'total time %.4f seconds' % duration
amount=len(funcs)*iters
print 'total method calls',amount
avg_normal_msec = 1000.0*duration/amount
print 'avg. time per method call: %.4f msec (%d/sec)' % (avg_normal_msec,amount/duration)
print 'Normal method call is %.4f times faster than Pyro method call.'%(avg_pyro_msec/avg_normal_msec)

