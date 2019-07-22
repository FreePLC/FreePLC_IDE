#!/usr/bin/env python

from Pyro.EventService.Clients import Publisher
from Pyro.errors import NamingError
import Pyro.core
import sys

CHAT_SERVER_GROUP = ":ChatBox-ES"
CHAT_SERVER_NAME = CHAT_SERVER_GROUP+".Server"


# Chat box administration server.
# Handles logins, logouts, channels and nicknames.
# The actual chat is fully performed by the Event Server!
# (Yes, this also means that if this Chatbox server dies, the people
#  currently chatting can continue to do so without problems!)
class ChatBox(Pyro.core.ObjBase, Publisher):
	def __init__(self):
		Pyro.core.ObjBase.__init__(self)
		Publisher.__init__(self)
		self.channels={}		# registered channels { eventTopic->nick list }
		self.nicks=[]			# all registered nicks on this server
	def getChannels(self):
		return self.channels.keys()
	def getNicks(self):
		return self.nicks
	def join(self, channel, nick):
		if nick in self.nicks:
			raise ValueError,'this nick is already in use'
		if not self.channels.has_key(channel):
			print 'CREATING NEW CHANNEL',channel
			self.channels[channel]=('ChatBox.Channel.'+channel,[])
		self.channels[channel][1].append(nick)
		self.nicks.append(nick)
		print nick,'JOINED',channel
		self.publish(self.channels[channel][0],('SERVER','** '+nick+' joined **'))
		return self.channels[channel]  # return the eventTopic for this channel
	def leave(self, channel, nick):
		if not self.channels.has_key(channel):
			print 'IGNORED UNKNOWN CHANNEL',channel
			return
		self.channels[channel][1].remove(nick)
		self.publish(self.channels[channel][0],('SERVER','** '+nick+' left **'))
		if len(self.channels[channel][1])<1:
			del self.channels[channel]
			print 'REMOVED CHANNEL',channel
		self.nicks.remove(nick)
		print nick,'LEFT',channel
		

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

