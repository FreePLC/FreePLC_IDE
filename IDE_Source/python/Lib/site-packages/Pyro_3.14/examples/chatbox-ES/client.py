#!/usr/bin/env python

from Pyro.EventService.Clients import Publisher, Subscriber
from server import CHAT_SERVER_NAME
from threading import Thread
import Pyro.core
from Pyro.errors import NamingError, ConnectionClosedError

# Chat client.
# Uses main thread for printing incoming event server messages
# (the chat messages!)
# and another to read user input and publish this on the chat channel.
# Logon/logoff is performed using the Chat server, which gives us a chat channel
# event server topic. The actual chatting is done fully trough
# this channel (the ES), the chat server is not needed for this!
class Chatter(Publisher, Subscriber):
	def __init__(self):
		Publisher.__init__(self)
		Subscriber.__init__(self)
		self.chatbox = Pyro.core.getProxyForURI('PYRONAME://'+CHAT_SERVER_NAME)
	def event(self, event):
		(nick,line)=event.msg
		if nick!=self.nick:
			print '['+nick+'] '+line
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
		(self.eventTopic, people)=self.chatbox.join(self.channel,self.nick)
		self.subscribe(self.eventTopic)
		print 'Joined channel',self.channel,'as',self.nick
		print 'People on this channel:',', '.join(people)
		self.inputThread=Thread(target=self.handleInput)
		self.inputThread.start()
		try:
			self.listen()
		except KeyboardInterrupt:
			print 'Shutting down... (press enter)'
			self.abort()
			self.inputThread.join()
	def handleInput(self):
		print 'Ready for input! Type /quit to quit'
		try:
			try:
				while not self.abortListen:
					line=raw_input('> ')
					if line=='/quit':
						break
					if line:
						self.publish(self.eventTopic,(self.nick,line))
			except EOFError:
				pass
		finally:
			# need to get new chatbox proxy because we're in a different thread
			chatbox = Pyro.core.getProxyForURI('PYRONAME://'+CHAT_SERVER_NAME)
			chatbox.leave(self.channel, self.nick)
			self.abort()
			print 'Bye!'


def main():
	chatter=Chatter()
	chatter.chooseChannel()

	
if __name__=="__main__":
	main()
