#!/usr/bin/env python

#
#	Bank client.
#
#	The client searches the two banks and performs a set of operations.
#	(the banks are searched simply by listing the :banks namespace!)
#

import sys
import Pyro.naming, Pyro.core

from banks import BankError

group = ':banks1'  # the default namespace group

# A bank client.
class client(object):
	def __init__(self,name):
		self.name=name
	def doBusiness(self, bank):
		print
		print '***',self.name,'is doing business with',bank.name(),':'

		print 'Creating account'
		try:
			bank.createAccount(self.name)
		except BankError,x:
			print 'Failed:',x
			print 'Removing account and trying again'
			bank.deleteAccount(self.name)
			bank.createAccount(self.name)

		print 'Deposit money'
		bank.deposit(self.name, 200.00)
		print 'Deposit money'
		bank.deposit(self.name, 500.75)
		print 'Balance=', bank.balance(self.name)
		print 'Withdraw money'
		bank.withdraw(self.name, 400.00)
		print 'Withdraw money (red)'
		try:
			bank.withdraw(self.name, 400.00)
		except BankError,x:
			print 'Failed:',x
		print 'End balance=', bank.balance(self.name)

		print 'Withdraw money from non-existing account'
		try:
			bank.withdraw('GOD',2222.22)
			print '!!! Succeeded?!? That is an error'
		except BankError,x:
			print 'Failed, as expected:',x

		print 'Deleting non-existing account'
		try:
			bank.deleteAccount('GOD')
			print '!!! Succeeded?!? That is an error'
		except BankError,x:
			print 'Failed, as expected:',x



# initialize the client and set the default namespace group
Pyro.core.initClient()
Pyro.config.PYRO_NS_DEFAULTGROUP=group

# locate the NS
locator = Pyro.naming.NameServerLocator()
print 'Searching Naming Service...',
ns = locator.getNS()

print 'Naming Service found at',ns.URI.address,'('+(Pyro.protocol.getHostname(ns.URI.address) or '??')+') port',ns.URI.port

# List the banks.
# This is done by simply looking in the :banks namespace, to see what
# banks have registered. The filter is for removing any groups that could
# be in the namespace (the type of real names is 1).
banknames = filter(lambda x: x[1]==1, ns.list(group))
banknames = map(lambda (x,y): x, banknames) # keep only the object name
if not banknames:
	raise RuntimeError('There are no banks to do business with!')

banks=[]	# list of banks (proxies)
print
for name in banknames:
	print 'Found a bank: ',name
	try:
		URI=ns.resolve(name)
	except Pyro.core.PyroError,x:
		print 'Bank can\'t be found:',x
		raise SystemExit

	# create a proxy for the bank object
	bank = Pyro.core.getProxyForURI(URI)
	banks.append(bank)

# Different clients
irmen = client('Irmen')
suzy = client('Suzy')

# Try the different banks
for bank in banks:
	irmen.doBusiness(bank)
	suzy.doBusiness(bank)

# List all accounts
print
for bank in banks:
	print 'The accounts in the',bank.name(),':'
	accounts = bank.allAccounts()
	for name in accounts.keys():
		print '  ',name,':',accounts[name]

# Pedantic cleanup
del irmen
del suzy
del banks
del ns

