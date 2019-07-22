#!/usr/bin/env python

import Pyro.core
import Pyro.naming
import os,sys

CHUNK_SIZE = 500000

#
#	File server.
#	Serves files only from a single directory.
#	Supports two transfer methods:
#	- read and send whole file in once call (uses much memory!, but is fastest)
#	- read and send file in chunks (uses only <chunksize> bytes of memory, is slightly slower.)
#
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

class FileServer(Pyro.core.ObjBase):
	def __init__(self, rootdir):
		Pyro.core.ObjBase.__init__(self)
		self.rootdir=os.path.abspath(rootdir)
		print "File server serving from",self.rootdir
		
	def listdir(self):
		dirs=[]
		files=[]
		for a in os.listdir(self.rootdir):
			if os.path.isdir(os.path.join(self.rootdir,a)):
				dirs.append(a)
			else:
				files.append(a)
		return files    # forget about the directories.
	
	def retrieveAtOnce(self, file):
		return open(os.path.join(self.rootdir,file),'rb').read()
		
	def openFile(self,file):
		if hasattr(self.getLocalStorage(), "openfile"):
			raise IOError("can only read one file at a time, close previous file first")
		file=os.path.join(self.rootdir,file)
		self.getLocalStorage().openfile=open(file,'rb')
		return os.path.getsize(file)
	def retrieveNextChunk(self):
		chunk= self.getLocalStorage().openfile.read(CHUNK_SIZE)
		if chunk:
			return chunk
		self.getLocalStorage().openfile.close()
		return ''
	def closeFile(self):
		self.getLocalStorage().openfile.close()
		del self.getLocalStorage().openfile



def main(args):
	Pyro.core.initServer()
	daemon=Pyro.core.Daemon()
	daemon.useNameServer(Pyro.naming.NameServerLocator().getNS())
	uri=daemon.connect(FileServer(args[1]), "fileserver")
	print "File server is running."
	daemon.requestLoop()


if __name__=="__main__":
	if len(sys.argv)!=2:
		print "Please give the file server root path as an argument to this script."
	else:
		main(sys.argv)
