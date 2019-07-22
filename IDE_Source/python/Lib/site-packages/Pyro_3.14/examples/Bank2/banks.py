# Bank and accounts code.
# NOTE that the Account and Bank classes are directly derived
# from the Pyro.core.ObjBase base class. This is required to
# support the 1.2+ attribute access feature.
# Note that an account object is not returned as-is, 
# rather, a PROXY for it is returned.
# Also note that the proxy must support attribute access, so
# we use getAttrProxy().

import Pyro.core

# the bank uses this exception to say there's something wrong:
class BankError(Exception): pass

# Unrestricted account.
class Account(Pyro.core.ObjBase):
	def __init__(self,name,owner):
		Pyro.core.ObjBase.__init__(self)
		self.balance=0.0
		self.name=name
		self.bank=owner
	def _gotReaped(self):
		print 'Account reaped, sorry your cash is lost:',self.name,self.balance 
		self.bank._gotReaped(self)
	def withdraw(self, amount):
		self.balance-=amount
	def deposit(self,amount):
		self.balance+=amount

# Restricted withdrawal account.
class RestrictedAccount(Account):
	def withdraw(s, amount):
		if amount<=s.balance:
			s.balance=s.balance-amount
		else:
			raise BankError('insufficent balance')

# Abstract bank.
class Bank(Pyro.core.ObjBase):
	def __init__(s):
		Pyro.core.ObjBase.__init__(s)
		s.accounts={}
	def createAccount(s, name):
		pass # must override this!
	def _gotReaped(self, account):
		del self.accounts[account.name]
		print 'Bank removed reaped account',account.name
	def deleteAccount(s, name):
		try:
			# find account, disconnect from daemon, delete it
			acc = s.accounts[name]
			s.getDaemon().disconnect(acc)
			del s.accounts[name]
		except KeyError:
			raise BankError('unknown account')
	def findAccount(s, name):
		try:
			# find account, return proxy for it
			return s.accounts[name].getAttrProxy()
		except KeyError:
			raise BankError('unknown account')

	def allAccounts(s):
		# list all accounts, return list of proxies for them
		accs = s.accounts.values()
		proxies = []
		for a in accs:
			proxies.append(a.getAttrProxy())
		return proxies


# Special bank: Rabobank. It has unrestricted accounts.
class Rabobank(Bank):
	def __init__(s):
		Bank.__init__(s)
		s.name = 'Rabobank'
	def createAccount(s,name):
		if s.accounts.has_key(name):
			raise BankError('Account already exists')
		# create account object, connect to daemon, return proxy for it
		acc = Account(name,s)
		acc_URI = s.getDaemon().connect(acc)
		s.accounts[name]=acc
		print 'created account',name
		return acc.getAttrProxy()


# Special bank: VSB. It has restricted accounts.
class VSB(Bank):
	def __init__(s):
		Bank.__init__(s)
		s.name = 'VSB bank'
	def createAccount(s,name):
		if s.accounts.has_key(name):
			raise BankError('Account already exists')
		# create account object, connect to daemon, return proxy for it
		acc = RestrictedAccount(name,s)
		acc_URI = s.getDaemon().connect(acc)
		s.accounts[name]=acc
		print 'created account',name
		return acc.getAttrProxy()

