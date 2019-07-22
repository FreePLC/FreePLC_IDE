#!/usr/bin/env python

#
#    Bank client.
#
#    The client searches the two banks and performs a set of operations.
#    (the banks are searched simply by listing the :banks namespace!)
#

import sys
import Pyro.naming, Pyro.core

from banks import BankError

group = ':banks'  # the default namespace group

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

banks={}    # banks (proxies)


print
for name in banknames:
    print 'Found a bank: ',name
    try:
        URI=ns.resolve(name)
    except Pyro.core.PyroError,x:
        print 'Bank can\'t be found:',x
        raise SystemExit

    # create a proxy for the bank object
    banks[name] = Pyro.core.getAttrProxyForURI(URI)

def selectBank():
    i = 1
    banknames=banks.keys()
    for b in banknames:
        print i," ",b
        i=i+1
    b = input("Select a bank: ")
    return banks[banknames[b-1]]
    
def createAccount():
    print "\nCreate Account."
    bank = selectBank()
    name = raw_input("Enter name: ")
    a = bank.createAccount(name)
    amount = input("Initial deposit: ")
    a.deposit(amount)
    print "Balance:", a.balance
    

def removeAccount():
    print "\nRemove Account."
    bank = selectBank()
    name = raw_input("Enter name: ")
    bank.deleteAccount(name)

def viewBalance():
    print "\nView Balance."
    bank = selectBank()
    name = raw_input("Enter name: ")
    ac = bank.findAccount(name)
    print ac.balance

def deposit():
    print "\nDeposit."
    bank = selectBank()
    name = raw_input("Enter name: ")
    ac = bank.findAccount(name)
    amount = input("Amount: ")
    ac.deposit(amount)
    print "New balance:", ac.balance

def withdraw():
    print "\nWithdraw."
    bank = selectBank()
    name = raw_input("Enter name: ")
    ac = bank.findAccount(name)
    amount = input("Amount: ")
    ac.withdraw(amount)
    print "New balance:", ac.balance

def listAll():
    print "\nList all accounts."
    for (bankname,bank) in banks.items():
        print bank.name
        accs = bank.allAccounts()
        if not accs:
            print "   No accounts."
        for a in accs:
            print "  ",a.name, a.balance

going = 1

while going:
    print "\n---- menu ----"
    print "1: create account"
    print "2: remove account"
    print "3: view balance"
    print "4: list all accounts"
    print "5: deposit money"
    print "6: withdraw money"
    print "0: exit"
    print
    try:
        choice = input("Choice: ")
        if choice==0:    going=0
        elif choice==1:    createAccount()
        elif choice==2:    removeAccount()
        elif choice==3:    viewBalance()
        elif choice==4:    listAll()
        elif choice==5:    deposit()
        elif choice==6:    withdraw()
    except SyntaxError,x:
        print "Input problem:",x
    except BankError,x:
        print 'Problem:',x
    except StandardError,x:
        print 'Try again (input incorrect?)'
        raise

        
