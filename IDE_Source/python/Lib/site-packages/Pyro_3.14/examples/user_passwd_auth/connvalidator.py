from Pyro.protocol import DefaultConnValidator
import Pyro.constants
import hmac
try:
	import hashlib
	md5=hashlib.md5
except ImportError:
	import md5
	md5=md5.md5


# Example username/password database: (passwords stored in ascii md5 hash)
EXAMPLE_ALLOWED_USERS = {
	"irmen": "5ebe2294ecd0e0f08eab7690d2a6ee69",		# 'secret'
	"guest": "084e0343a0486ff05530df6c705c8bb4",		# 'guest'
	"root": "bbbb2edef660739a6071ab5a4f8a869f",			# 'change_me'
}

#
#	Example login/password validator.
#	Passwords are protected using md5 so they are not stored in plaintext.
#	The actual identification check is done using a hmac-md5 secure hash.
#
class UserLoginConnValidator(DefaultConnValidator):

	def acceptIdentification(self, daemon, connection, token, challenge):
		# extract tuple (login, processed password) from token as returned by createAuthToken
		# processed password is a hmac hash from the server's challenge string and the password itself.
		login, processedpassword = token.split(':', 1)
		knownpasswdhash = EXAMPLE_ALLOWED_USERS.get(login)
		# Check if the username/password is valid.
		if knownpasswdhash:
			# Known passwords are stored as ascii hash, but the auth token contains a binary hash.
			# So we need to convert our ascii hash to binary to be able to validate.
			knownpasswdhash=knownpasswdhash.decode("hex")
			if hmac.new(challenge,knownpasswdhash).digest() == processedpassword:
				print "ALLOWED", login
				connection.authenticated=login  # store for later reference by Pyro object
				return(1,0)
		print "DENIED",login
		return (0,Pyro.constants.DENIED_SECURITY)
		
	def createAuthToken(self, authid, challenge, peeraddr, URI, daemon):
		# authid is what mungeIdent returned, a tuple (login, hash-of-password)
		# we return a secure auth token based on the server challenge string.
		return "%s:%s" % (authid[0], hmac.new(challenge,authid[1]).digest() )

	def mungeIdent(self, ident):
		# ident is tuple (login, password), the client sets this.
		# we don't like to store plaintext passwords so store the md5 hash instead.
		return (ident[0], md5(ident[1]).digest())
		
