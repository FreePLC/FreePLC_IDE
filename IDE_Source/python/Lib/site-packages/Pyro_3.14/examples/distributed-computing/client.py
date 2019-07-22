import Pyro.core
import Pyro.errors
import Pyro.util
import tasks.md5crack
import tasks.sorting
import time


Pyro.config.PYRO_MOBILE_CODE=1		# Enable mobile code (for the tasks)

Pyro.core.initClient()

selected_task = raw_input("What task do you want to run (md5 or sorting; m/s): ")

if selected_task in ('m','md5'):
	UIClass = tasks.md5crack.UserInterface
	TaskClass = tasks.md5crack.CrackTask
elif selected_task in ('s','sorting'):
	UIClass = tasks.sorting.UserInterface
	TaskClass = tasks.sorting.SortTask
else:
	raise ValueError("invalid task chosen")
		
ui=UIClass()
arguments = ui.begin()
task = TaskClass(arguments)
ui.info(task)
	
choice=input("Do you want sequential/normal (1) or distributed processing (2) ? ")
if choice==1:
	print "(using normal sequential local processing)"
	start=time.time()
	tasks=task.split(3)        # just for the fun of it
	
	while tasks:
		t=tasks.pop()
		print "(local) running task",t
		t.run()
		if task.join(t):
			break
	print "(local) gathering result"
	result=task.getResult()
	duration=time.time()-start

elif choice==2:
	print "(using distributed parallel processing)"
	dispatcher = Pyro.core.getProxyForURI("PYRONAME://:Distributed.Dispatcher")
	start=time.time()
	try:
		result=dispatcher.process(task)        # the interesting stuff happens here :)
	except Exception,x:
		print "".join(Pyro.util.getPyroTraceback(x))
	duration=time.time()-start
		
ui.result(result)
print "It took %.3f seconds." % duration
