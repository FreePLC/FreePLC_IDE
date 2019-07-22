#!/usr/bin/env python

from threading import Thread
from Pyro.errors import NamingError
import Pyro.core, Pyro.naming, Pyro.util
import sys

CHAT_SERVER_GROUP = ":ChatBox"
CHAT_SERVER_NAME = CHAT_SERVER_GROUP+".Server"


# Chat box administration server.
# Handles logins, logouts, channels and nicknames, and the chatting.
class ChatBox(Pyro.core.ObjBase):
	def __init__(self):
		Pyro.core.ObjBase.__init__(self)
		self.channels={}		# registered channels { channel --> (nick, client callback) list }
		self.nicks=[]			# all registered nicks on this server
	def getChannels(self):
		return self.channels.keys()
	def getNicks(self):
		return self.nicks
	def join(self, channel, nick, callback):
		if nick in self.nicks:
			raise ValueError,'this nick is already in use'
		if not self.channels.has_key(channel):
			print 'CREATING NEW CHANNEL',channel
			self.channels[channel]=[]
		self.channels[channel].append((nick,callback))
		self.nicks.append(nick)
		callback._setOneway('message')	# don't wait for results for this method
		print nick,'JOINED',channel
		self.publish(channel,'SERVER','** '+nick+' joined **')
		nicks=[]
		for (n,c) in self.channels[channel]:
			nicks.append(n)
		return nicks
	def leave(self,channel,nick):
		if not self.channels.has_key(channel):
			print 'IGNORED UNKNOWN CHANNEL',channel
			return
		for (n,c) in self.channels[channel]:
			if n==nick:
				self.channels[channel].remove((n,c))
				break
		self.publish(channel,'SERVER','** '+nick+' left **')
		if len(self.channels[channel])<1:
			del self.channels[channel]
			print 'REMOVED CHANNEL',channel
		self.nicks.remove(nick)
		print nick,'LEFT',channel
	def publish(self, channel, nick, msg):
		# This must be performed in its own thread otherwise a thread deadlock may occur
		# when the publish is performed from within a call of a subscriber!
		Thread(target=self._do_publish, args=(channel, nick ,msg)).start()
	def _do_publish(self, channel, nick, msg):
		if not self.channels.has_key(channel):
			print 'IGNORED UNKNOWN CHANNEL',channel
			return
		for (n,c) in self.channels[channel][:]:		# use a copy of the list
			try:
				c.message(nick,msg)	# oneway call
			except Pyro.errors.ConnectionClosedError,x:
				# connection dropped, remove the listener if it's still there
				# check for existence because other thread may have killed it already
				if (n,c) in self.channels[channel]:
					self.channels[channel].remove((n,c))
					print 'Removed dead listener',n,c


def main():
	Pyro.core.initServer()
	daemon = Pyro.core.Daemon()
	ns = Pyro.naming.NameServerLocator().getNS()
	daemon.useNameServer(ns)

	# make sure our namespace group exists, and that our object name doesn't
	try:
		ns.createGroup(CHAT_SERVER_GROUP)
	except NamingError:
		pass
	try:
		ns.unregister(CHAT_SERVER_NAME)
	except NamingError:
		pass

	uri=daemon.connect(ChatBox(),CHAT_SERVER_NAME)

	# enter the service loop.
	print 'Chatbox open.'
	daemon.requestLoop()


if __name__=='__main__':
	main()

