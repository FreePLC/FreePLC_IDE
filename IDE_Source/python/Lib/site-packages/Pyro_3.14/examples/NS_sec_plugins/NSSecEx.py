#!/usr/bin/env python

# 
#  Example of Name Server security plugins.
#
#  This shows possible implementations of a NS BC request validator
#  and a NS new connection validator.
#
#  See the Readme.txt for more information.
#


ACCEPTED_ID = 'p4ssphr4se'

#----- required global funcs that return validator objects ------
def BCGuard():
	return BCReqValidator()

def NSGuard():
	v=NSnewConnValidator()
	v.setAllowedIdentifications([ACCEPTED_ID])
	return v


#----- validator object implementation --------

import Pyro.naming
import Pyro.protocol

# NS Broadcast Request Validator
# Must inherit from the base class as shown,
# because dispatcher code is in there.
class BCReqValidator(Pyro.naming.BCReqValidator):
	# we have:
	# self.addr = address of client (ip, port)
	# self.sock = reply socket (used by self.reply method)
	def acceptLocationCmd(self):
		print self.addr[0],'WANTS TO KNOW OUR LOCATION. Ok...'
		return 1
	def acceptShutdownCmd(self):
		print self.addr[0],'WANTS US TO SHUT DOWN, Pfff!'
		self.reply('denied!')  # send this back to client
		return 0

		
# NS Pyro Daemon newConnValidator
class NSnewConnValidator(Pyro.protocol.DefaultConnValidator):
	def acceptHost(self, tcpserver, conn):
		print conn.addr[0],'WANTS CONNECTION...'
		return Pyro.protocol.DefaultConnValidator.acceptHost(self, tcpserver, conn)
	def acceptIdentification(self, tcpserver, conn, token, challenge):
		print conn.addr[0],'SENDS IDENTIFICATION...'
		(ok,reason)=Pyro.protocol.DefaultConnValidator.acceptIdentification(self, tcpserver, conn, token, challenge)
		if not ok:
			print 'Connection denied!  Make sure the identification is "'+ACCEPTED_ID+'"'
		return (ok,reason)

