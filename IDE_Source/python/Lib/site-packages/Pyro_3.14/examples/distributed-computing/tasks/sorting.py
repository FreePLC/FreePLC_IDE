from tasks.task import PartitionableTask, TaskPartition

import time
import random
import string

#
# The 'main' task of sorting a big list of random numbers.
# It partitions the work in a way where each subtask
# sorts a chunk of the original huge list, and after that,
# all sorted chunks are merged using a single merge pass of O(n).
#
class SortTask(PartitionableTask):
			
	def __init__(self, listSize):
		PartitionableTask.__init__(self,"data sorter")
		self.size=listSize
		self.chunks=[]
		self.numchunks=0
		self.result=[]
	def split(self, numPiecesHint):
		lst=[random.choice(string.lowercase) for i in range(self.size)]
		pieces=numPiecesHint*3 # number of pieces
		chunksize=self.size/pieces
		taskparts=[]
		for i in range(pieces+1):
			chunk = lst[0:chunksize]
			del lst[0:chunksize]
			if chunk:
				taskparts.append(SortTaskPartition(chunk, i+1))
			else:
				break
		self.numchunks=len(taskparts)
		return taskparts
	def join(self,task):
		self.chunks.append(task.result)
		return False  # not done yet, also join all other tasks
	def getResult(self):
		if len(self.chunks)!=self.numchunks:
			return None  # not yet enough chunks received
		if self.result:
			return self.result
		assert sum([len(x) for x in self.chunks])==self.size, "length of combined chunks is incorrect"
		# use a single pass of the generic merge sort O(n) to get the final sorted list.
		# we sort in reverse order because removing elements from the end of a list is O(1)
		result=[]
		starttime=time.time()
		while len(result)<self.size:
			for chunk in self.chunks:
				if chunk:
					largest_chunk=chunk
					largest_elt=chunk[-1]
					break
			for chunk in self.chunks[1:]:
				if chunk and chunk[-1]>largest_elt:
					largest_elt=chunk[-1]
					largest_chunk=chunk
			result.append(largest_elt)
			del largest_chunk[-1]
		result.reverse()
		self.result=result
		print "Chunks merged in %.03f seconds." % (time.time()-starttime)
		return self.result
				


#
# The subtask responsible for sorting a certain part of the full list
#
class SortTaskPartition(TaskPartition):
	def __init__(self, unsortedList, chunknumber):
		TaskPartition.__init__(self,"sort chunk %d" % chunknumber )
		self.lst = unsortedList
		self.result=None
		self.size=len(self.lst)
	def work(self):
		prevprogress=time.time()
		result=[]
		while self.lst:
			elt=self.lst.pop()
			i=0
			while i<len(result):
				if result[i]>=elt:
					break
				i+=1
			result.insert(i, elt)
			if (time.time()-prevprogress)>0.3:
				yield len(result)
				prevprogress=time.time()
		self.result=result
			
	def progress(self, pos):
		return pos/float(self.size)



#
# The 'user interface' for the sort task.
#
class UserInterface(object):
	def begin(self):
		print "Big data array sorting."
		size=input("Enter the size of the data array (>100): ")
		return size
	def info(self, task):
		print "Sorting the data array of length %d..." % task.size
	def result(self,taskresult):
		filename="sorted.txt"
		print "\nWriting the sorted data array to",filename
		out=open(filename,"w")
		while taskresult:
			print >>out, "".join(taskresult[:70])
			del taskresult[:70]
		out.close()
