import Pyro.core
import Pyro.naming
import Pyro.errors
import sys,os

Pyro.config.PYRO_MOBILE_CODE=1		# Enable mobile code (for the tasks)


#
# The cell processor.
# It processes tasks that it receives.
# NOTE: it is not particularly intelligent about
# what tasks to run and when!! It depends on the
# dispatcher to do this in the correct way!
#
# NOTE2: notice that this module doesn't import or use
# the actual task code implementation. It relies on Pyro's
# mobile code feature to obtain the task data and code to run!
#
class Cell(Pyro.core.ObjBase):
    def __init__(self):
        Pyro.core.ObjBase.__init__(self)
        self.finished=False
    def receivetask(self,task):
        self.finished=False
        self.task=task
        print "received task: "+str(task)
    def process(self):  
        print "running task..."
        self.task.run()
        print "task finished."
        self.finished=True
    def abort(self):
        print "ABORT!"
        self.task.abort=True
 
#
# Initialize the environment
#   
Pyro.core.initServer()
ns=Pyro.naming.NameServerLocator().getNS()
try:
    ns.createGroup(":Distributed")
except Pyro.errors.NamingError:
    pass
try:
    ns.createGroup(":Distributed.Cells")
except Pyro.errors.NamingError:
    pass
daemon=Pyro.core.Daemon()
daemon.useNameServer(ns)
Pyro.config.PYRO_NS_DEFAULTGROUP = ":Distributed.Cells"


#
# Find the next available object name that we can use
# to register this cell processor.
# The dispatcher looks in the Pyro namespace to find
# us and the other available cells.
#
i=1
object = Cell()
while True:
    try:
        name="processor%d" % i
        uri=daemon.connect( object ,name)
        print "Connected",ns.fullName(name)
        print "Cell ready."
        try:
            daemon.requestLoop()
        except Exception:
            daemon.shutdown()
            print "clean shutdown."
            try:
                ns.unregister(name)
            except Pyro.errors.NamingError:
                pass
            break
    except Pyro.errors.NamingError,x:
        i+=1
