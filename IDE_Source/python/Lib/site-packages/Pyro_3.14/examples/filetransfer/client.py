#!/usr/bin/env python

#
#	Client for the extremely simple 'file-server' using Pyro.
#
#	NOTE: this is just an example to show how you _could_ send
#	large streams of data with Pyro (by transferring it in chunks).
#	THIS CODE CAN NOT COPE WITH MULTIPLE TRANSFERS AT THE SAME TIME!
#	(because the file server is statefull and only knows about
#	a single file transfer that is in progress). Also, no measures
#	are taken to protect the file transfer from other clients that
#	connect to the server and 'hijack' the download by calling
#	retrieveNextChunk.
#

import Pyro.core
import sys,time

class FileClient(object):
	def __init__(self):
		self.fileserver = Pyro.core.getProxyForURI("PYRONAME://fileserver")
	def menu(self):
		print "\nls : list directory"
		print "r <file> : retrieve file at once"
		print "c <file> : retrieve file in chunks"
		print "q : quit"
	def cli(self):
		while True:
			self.menu()
			cmd=raw_input("?>")
			if cmd=="ls":
				self.ls()
			elif cmd.startswith("r "):
				self.retrieveAtOnce(cmd[2:])
			elif cmd.startswith("c "):
				self.retrieveChunks(cmd[2:])
			elif cmd=="q":
				return
			else:
				print "invalid command"
	def ls(self):
		files = self.fileserver.listdir()
		files.sort()
		#for d in dirs:
		#	print "  %s [DIRECTORY]" % d
		for f in files:
			print f

	def retrieveAtOnce(self,file):
		print "Retrieving",file,"..."
		starttime=time.time()
		try:
			data=self.fileserver.retrieveAtOnce(file)
		except IOError,x:
			print "error: ",x
		else:
			duration=time.time()-starttime
			print len(data),"bytes received in",int(duration),"seconds",
			if duration>0:
				print "=",int(len(data)/duration/1024.0),"kb/sec"
			open(file,"wb").write(data)
			print "saved to",file
			
	def retrieveChunks(self,file):
		print "Retrieving",file,"..."
		starttime=time.time()
		try:
			size = self.fileserver.openFile(file)
		except IOError,x:
			print "error: ",x
		else:
			print "Filesize=",size
			total=0
			file=open(file,"wb")
			while True:
				chunk=self.fileserver.retrieveNextChunk()
				sys.stdout.write(".")
				sys.stdout.flush()
				if chunk:
					file.write(chunk)
					total+=len(chunk)
				else:
					break
			self.fileserver.closeFile()
			file.close()
			duration=time.time()-starttime
			print total,"bytes received in",int(duration),"seconds",
			if duration>0:
				print "=",int(total/duration/1024.0),"kb/sec"
		

def main(args):
	Pyro.core.initClient()
	client=FileClient()
	client.cli()

if __name__=="__main__":
	main(sys.argv)
