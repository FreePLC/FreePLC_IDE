import threading
import time
import Pyro.core
import Pyro.util
import params.parameters

HOST="localhost"
URI = "PYROLOC://%s/test.threadmobile"
NUM_THREADS=10

if not Pyro.config.PYRO_MOBILE_CODE:
	raise SystemExit("PYRO_MOBILE_CODE not enabled")
if Pyro.config.PYRO_XML_PICKLE=='gnosis' and Pyro.config.PYRO_GNOSIS_PARANOIA>=0:
	raise SystemExit("Using gnosis xml pickle but PYRO_GNOSIS_PARANOIA needs to be -1")


startEvent = threading.Event()

def worker():
	obj=Pyro.core.getProxyForURI(URI % HOST)
	startEvent.wait()
	name = threading.currentThread().getName()
	print "worker", name
	p = params.parameters.Parameter(name)
	try:
		result=obj.method(p)
		print "result=",result,"calling method on it..."
		result.method()
	except Exception,x:
		print "".join(Pyro.util.getPyroTraceback(x))
	time.sleep(1)
	print "exit"


HOST=raw_input("server host (empty for %s): " % HOST) or HOST	

workers=[]
for i in range(NUM_THREADS):
	w=threading.Thread(target=worker)
	workers.append(w)
	w.start()
	time.sleep(0.1)

time.sleep(1)
print "starting!"
startEvent.set()

print "running"	

for w in workers:
	w.join()

print "done!"
