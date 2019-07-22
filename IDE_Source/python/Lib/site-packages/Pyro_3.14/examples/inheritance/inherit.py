from ftplib import FTP
import Pyro.core

class base1(object):
	def meth1(self):
		return 'base1.meth1'
	def meth2(self):
		return 'base1.meth2'

class base2(object):
	def meth2(self):
		return 'base2.meth2'
	def meth3(self):
		return 'base2.meth3'

class sub(base1,base2):
	def meth2(self):
		return 'sub.meth2 (overridden)'
	def meth4(self):
		return 'sub.meth4'

class Fsub(base1,base2,FTP):
	def meth2(self):
		return 'Fsub.meth2 (overridden)'
	def meth4(self):
		return 'Fsub.meth4'

class Gsub(base1, Pyro.core.ObjBase):
	def ding(self):
		pass
