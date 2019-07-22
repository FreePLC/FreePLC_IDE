#!/usr/bin/env python

import Pyro.naming
import random, time
from threading import Thread
import random
from Pyro.errors import NamingError
import binascii

mustStop=0

def name():
	return str(random.random())[-3:]

def nameG():
	if random.random()>0.3:
		return 'trasher.G'+name()+'.'+name()
	else:
		return 'trasher.'+name()
	

class NamingTrasher(Thread):
	def __init__(self,number):
		Thread.__init__(self)
		self.number=number

	def flatlist(self):
		if random.random()>0.8:
			try:
				a=len(self.ns.flatlist())
			except NamingError,x:
				pass
	def register(self):
		for i in range(4):
			try:
				self.ns.register(nameG(),'PYRO://localhost/111111111')
			except NamingError,x:
				pass
	def remove(self):
		try:
			self.ns.unregister(nameG())
		except NamingError,x:
			pass
	def resolve(self):
		try:
			uri=self.ns.resolve(nameG())
		except NamingError,x:
			pass
	def creategrp(self):
		for i in range(3):
			try:
				self.ns.createGroup('trasher.G'+name())
			except NamingError,x:
				pass
	def delgrp(self):
		if random.random()>0.8:
			try:
				self.ns.deleteGroup('trasher.G'+name())
			except NamingError,x:
				pass

	def run(self):	
		self.ns = Pyro.naming.NameServerLocator().getNS()
		print 'Name Server trasher running.'
		while not mustStop:
			random.choice((self.flatlist, self.register, self.remove, self.resolve, self.creategrp, self.delgrp)) ()
			print self.number,'called'
			time.sleep(random.random()/10)
		print 'Trasher exiting.'	

def main():
	Pyro.core.initClient()
	threads=[]
	ns = Pyro.naming.NameServerLocator().getNS()
	ns.createGroup('trasher')
	for i in range(10):
		nt=NamingTrasher(i)
		nt.start()
		threads.append(nt)

	try:
		while 1:
			time.sleep(10)
	except KeyboardInterrupt:
		global mustStop
		mustStop=1

	print 'Break-- waiting for threads to stop.'
	for nt in threads:
		nt.join()
	ns.deleteGroup('trasher')

if __name__=='__main__':
	main()

