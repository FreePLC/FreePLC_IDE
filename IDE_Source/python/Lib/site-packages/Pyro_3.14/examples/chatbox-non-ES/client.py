#!/usr/bin/env python

from server import CHAT_SERVER_NAME
from threading import Thread
import Pyro.core
from Pyro.errors import NamingError, ConnectionClosedError

# Chat client.
# Uses main thread for printing incoming event server messages (the chat messages!)
# and another to read user input and publish this on the chat channel.
class Chatter(Pyro.core.ObjBase):
	def __init__(self):
		Pyro.core.ObjBase.__init__(self)
		self.chatbox = Pyro.core.getProxyForURI('PYRONAME://'+CHAT_SERVER_NAME)
		self.abort=0
	def message(self, nick, msg):
		if nick!=self.nick:
			print '['+nick+'] '+msg
	def chooseChannel(self):
		nicks=self.chatbox.getNicks()
		if nicks:
			print 'The following people are on the server: ',', '.join(nicks)
		channels=self.chatbox.getChannels()
		channels.sort()
		if channels:
			print 'The following channels already exist: ',', '.join(channels)
			print
			self.channel=raw_input('Choose a channel or create a new one: ')
		else:
			print 'The server has no active channels.'
			self.channel=raw_input('Name for new channel: ')
		self.nick=raw_input('Choose a nickname: ')
		people=self.chatbox.join(self.channel,self.nick,self.getProxy())
		print 'Joined channel',self.channel,'as',self.nick
		print 'People on this channel:',', '.join(people)
		self.inputThread=Thread(target=self.handleInput)
		self.inputThread.start()
	def handleInput(self):
		print 'Ready for input! Type /quit to quit'
		# we need to get a new chatbox proxy because we're running in a different thread
		chatbox = Pyro.core.getProxyForURI('PYRONAME://'+CHAT_SERVER_NAME)
		try:
			try:
				while not self.abort:
					line=raw_input('> ')
					if line=='/quit':
						break
					if line:
						chatbox.publish(self.channel,self.nick,line)
			except EOFError:
				pass
		finally:
			chatbox.leave(self.channel, self.nick)
			self.abort=1
			print 'Bye! (from input thread)'


def main():
	Pyro.core.initServer()
	Pyro.core.initClient()
	daemon = Pyro.core.Daemon()
	ns = Pyro.naming.NameServerLocator().getNS()
	daemon.useNameServer(ns)
	
	chatter=Chatter()
	daemon.connect(chatter)
	chatter.chooseChannel()
	try:
		daemon.requestLoop(lambda: not chatter.abort)
	except KeyboardInterrupt:
		print 'Shutting down chatter... (press enter)'
		chatter.abort=1
		chatter.inputThread.join()
	print 'Exiting.'	

	
if __name__=="__main__":
	main()
