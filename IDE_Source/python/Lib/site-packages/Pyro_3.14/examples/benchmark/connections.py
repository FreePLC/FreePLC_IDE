import Pyro.core
import Pyro.naming
import time

ns_uri=Pyro.naming.NameServerLocator().getNS().URI
print "Name server location:",repr(ns_uri)

print "Timing raw connect speed (no method call)..."
p=Pyro.core.DynamicProxy(ns_uri)
p.ping()
begin=time.time()
ITERATIONS=2000
for loop in xrange(ITERATIONS):
    if loop%500==0:
        print loop
    p._release()
    p.adapter.rebindURI()
duration=time.time()-begin
print "%d connections in %s sec = %f conn/sec" % (ITERATIONS, duration, ITERATIONS/duration)
del p

print "Timing proxy creation+connect+methodcall speed..."
ITERATIONS=2000
begin=time.time()
for loop in xrange(ITERATIONS):
    if loop%500==0:
        print loop
    p=Pyro.core.DynamicProxy(ns_uri)
    p.ping()
duration=time.time()-begin
print "%d new proxy calls in %s sec = %f calls/sec" % (ITERATIONS, duration, ITERATIONS/duration)

print("Timing proxy methodcall speed...")
p=Pyro.core.DynamicProxy(ns_uri)
p.ping()
ITERATIONS=10000
begin=time.time()
for loop in range(ITERATIONS):
    if loop%1000==0:
        print(loop)
    p.ping()
duration=time.time()-begin
print("%d calls in %s sec = %.2f calls/sec" % (ITERATIONS, duration, ITERATIONS/duration))
