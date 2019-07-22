import Pyro.core
import Pyro.naming
import Pyro.errors
import itertools
import sys,os,time,copy
import sets

Pyro.config.PYRO_MOBILE_CODE=1		# Enable mobile code (for the tasks)


#
# The task dispatcher.
# It receives a single computation Task, searches in the Pyro Namespace
# for available cell Processors, and divides and distributes the Task
# among the processors.
# It lets them run (in parallel!) and gathers the result from each.
# As soon as one found the 'solution' to the Task, the others are
# signalled to abort their computation, and the result is returned
# to the client program.
#
# NOTE2: notice that this module doesn't import or use
# the actual task code implementation. It relies on Pyro's
# mobile code feature to obtain the actual task data!
# (which it then sends to the cell processor(s) to run).
#
class Dispatcher(Pyro.core.ObjBase):
    def __init__(self, nameServer):
        Pyro.config.PYRO_NS_DEFAULTGROUP = ":Distributed.Cells"
        Pyro.core.ObjBase.__init__(self)
        self.NSBase=nameServer
        # make sure that the Event Server is active:
        self.NSBase.resolve(Pyro.constants.EVENTSERVER_NAME)
    def process(self,task):
        print "received task:",task
        NS=copy.copy(self.NSBase)   # copy proxy because of thread issue
        try:
            cells=NS.list(None)  # search the namespace for processors
            print "cells:",cells
            cells = [ NS.resolve(name).getAttrProxy() for name,otype in cells ]
            if cells:
                print "splitting task"
                taskparts = task.split(len(cells))
                print "-->",len(taskparts),"tasks"
                celliter = itertools.cycle(cells)   # just loop over all processors
                print "dispatching"
                busy=sets.Set()
                # While there are still subtasks to compute, and the
                # solution has not been found, dispatch the next subtask
                # to an available cell.
                while taskparts and not task.getResult():
                    cell = celliter.next()
                    if cell in busy:
                        time.sleep(0.2)
                        if cell.finished:
                            # okay... a cell has become available again.
                            # process its result and remove it from the busy-set
                            task.join(cell.task)
                            busy.remove(cell)
                        else:
                            continue
                    # found an idle cell, give it a task to do
                    busy.add(cell)
                    subtask = taskparts.pop()
                    # NOTE: we first submit the task to the cell using a normal
                    # Pyro invocation. This is needed because of the mobile code feature:
                    # the server cannot request code over a oneway invocation.
                    # Only after the server has received the computation task,
                    # we invoke a oneway method to actually start the cell processor.
                    # Because is is oneway, we can continue, while the cell is running.
                    cell._setOneway("process")
                    cell.receivetask(subtask)
                    cell.process()
                    print "dispatched %s, %d remain" % (str(subtask), len(taskparts))

                print "Task fully dispatched!"
                print "Gathering results..."

                # wait for and retreive the result from each cell
                while busy and not task.getResult():
                    for cell in sets.Set(busy):
                        if cell.finished:
                            print "got result, %d remain" % len(busy)
                            busy.remove(cell)
                            task.join(cell.task)
                            if task.getResult():
                                break
                    time.sleep(0.2)

                print "all done for task",task
                if task.getResult() and busy:
                    print "There are still %d running tasks" % len(busy)
                    for cell in busy:
                        cell._setOneway("abort")   # so that we can continue
                        cell.abort()
                    
                print "Returning final result!"
                return task.getResult()                    
            else:
                print "no cells in ns"
                raise RuntimeError("no computing cells found")
        except Pyro.errors.NamingError,x:
            print "No cells registered on the network",x
            raise RuntimeError("no computing cells found")
    
    
Pyro.core.initServer()
ns=Pyro.naming.NameServerLocator().getNS()
try:
    ns.createGroup(":Distributed")
except Pyro.errors.NamingError:
    pass
try:
    ns.unregister(":Distributed.Dispatcher")
except Pyro.errors.NamingError:
    pass
daemon=Pyro.core.Daemon()
daemon.useNameServer(ns)
uri=daemon.connect(Dispatcher(ns),":Distributed.Dispatcher")

print "Dispatcher ready."
daemon.requestLoop()
