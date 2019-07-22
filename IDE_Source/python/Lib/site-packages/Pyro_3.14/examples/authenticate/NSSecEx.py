#!/usr/bin/env python

#  Name Server security plugins.


ACCEPTED_ID = 's3cr3t'

#----- required global funcs that return validator objects ------
def BCGuard():
	return None		# no special broadcast server guard

def NSGuard():
	v=NSnewConnValidator()
	v.setAllowedIdentifications([ACCEPTED_ID])
	return v


#----- validator object implementation --------

import Pyro.protocol

# NS Pyro Daemon newConnValidator
class NSnewConnValidator(Pyro.protocol.DefaultConnValidator):
	def acceptIdentification(self, tcpserver, conn, hash, challenge):
		print conn.addr[0],'SENDS IDENTIFICATION...'
		(ok,reason)=Pyro.protocol.DefaultConnValidator.acceptIdentification(self, tcpserver, conn, hash, challenge)
		if not ok:
			print 'Connection denied!  Make sure the identification is "'+ACCEPTED_ID+'"'
		return (ok,reason)

