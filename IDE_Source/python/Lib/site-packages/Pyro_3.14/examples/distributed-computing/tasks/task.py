import sys
import Pyro.EventService.Clients
import Pyro.constants

#
# The 'main' Task abstract baseclass.
#
class PartitionableTask(object):
	def __init__(self, name):
		self.name=name
	def split(self, numPiecesHint): 
		pass  # implement in subclass
	def join(self, task):
		pass  # implement in subclass, return True to stop the whole task.
	def getResult(self):
		pass  # implement in subclass
	def __str__(self):
		return "<Task '%s'>" % self.name

#
# The subtask baseclass. The main task is split into these
# subtasks, which are distributed over the processors.
# The progress of each subtask can be monitored on the ES
# channels Distributed.cell.*  (*=subtask name)
# (use the monitor.py for this)
#
class TaskPartition(Pyro.EventService.Clients.Publisher):
	def __init__(self, name):
		Pyro.EventService.Clients.Publisher.__init__(self)
		self.name=name
	def run(self):
		self.publish("Distributed.cell."+self.name, "START")
		for pos in self.work():
			self.publish("Distributed.cell."+self.name, self.progress(pos))
		self.publish("Distributed.cell."+self.name, "FINISHED")
	def progress(self,pos):
		return 100.0*pos/100.0	# override in subclass
	def work(self):
		yield 100 	# override this generator in subclass, here the actual work is done
	def __str__(self):
		return "<TaskPartition '%s'>" % self.name
