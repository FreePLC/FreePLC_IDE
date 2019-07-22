import tasks.task

import array, time
try:
	import hashlib
	md5=hashlib.md5
except ImportError:
	import md5
	md5=md5.md5

# Determine how fast your cpu is (est.)
# this is used to create a reasonable progress update rate.
start=time.time()
print "(benchmarking...)"
CPU_SPEED=0
while time.time()-start < 1:
    void=md5("benchmark").digest()
    CPU_SPEED+=1
CPU_SPEED /= 2


#
# The 'main' task of cracking (guessing) a MD5 hash.
# It partitions the work in a way where each subtask
# processes a small set of the possible search space.
# (it is a brute-force search).
#
class CrackTask(tasks.task.PartitionableTask):
            
    def __init__(self, sourceText):
        tasks.task.PartitionableTask.__init__(self,"md5 guesser")
        self.source=sourceText                      # we will guess this
        self.md5hash=md5(self.source).digest()   # we will crack this
        self.result=None
    def split(self, numPiecesHint):
        pieces=numPiecesHint*3 # number of pieces
        step=26.0/pieces  # chunks from the alphabet
        begin=ord('a')   # start with a
        taskparts=[]
        for i in range(1,pieces+1):
            end= ord('a')+int(i*step)
            taskparts.append(CrackTaskPartition(self.md5hash, begin, end, len(self.source)))
            begin=end
        return taskparts
    def join(self,task):
        if not self.result and task.result:
            # we found the solution!
            self.result=task.result
            return True
        return False
    def getResult(self):
        return self.result



# generator to cycle trough all possible strings (letter combinations)
def allStrings(size, begin, end):
    data=array.array('b')
    data.fromstring( chr(begin)+'a'*(size-1) )    # 'xaaaaaa...'
    def nextletter(pos):   
        data[pos]+=1
        if data[pos]>122:   # ord('z')
            if pos==0:
                data[0]+=1
                return
            data[pos]=97 # ord('a')
            nextletter(pos-1)
    while data[0]<=end:
        yield data.tostring()
        # increase letters
        nextletter(size-1)

#
# The subtask responsible for brute-forcing a certain part
# of the search space (a limited range based on the first letter)
#
class CrackTaskPartition(tasks.task.TaskPartition):
    def __init__(self, md5hash, begin, end, size):
        tasks.task.TaskPartition.__init__(self,"md5  %s - %s" % (chr(begin),chr(end-1)) )
        self.md5hash=md5hash
        self.begin=begin
        self.end=end
        self.amount=(self.end-self.begin) * 26.0**(size-1)
        self.size=size
        self.abort=False
    def work(self):
        strings=allStrings(self.size, self.begin, self.end)
        self.result=None
        counter=0
        try:
            while not self.result and not self.abort:
                for i in range(CPU_SPEED):
                    s = strings.next()
                    if md5(s).digest() == self.md5hash:
                        self.result=s # FOUND IT!!
                        return
                counter+=CPU_SPEED
                yield counter
        except StopIteration:
            pass   # we've processed all strings, no result.
            
    def progress(self, pos):
        return pos/self.amount



#
# The 'user interface' for the md5 task.
#
class UserInterface(object):
	def begin(self):
		print "MD5 'cracking'."
		code=raw_input("Enter a short word (4-5 lowercase letters; a-z) that is the key: ")
		return code
	def info(self, task):
		print "The md5 hash of your word is ",task.md5hash.encode("hex")
		print "Cracking the md5 hash with code length %d..." % len(task.source)
	def result(self,taskresult):
		if taskresult:
			print "\nI cracked the code! It was: '%s'" % taskresult
			print "(that string produces the same md5 hash as your original code word)"
		else:
			print "\nCode could not be cracked."
