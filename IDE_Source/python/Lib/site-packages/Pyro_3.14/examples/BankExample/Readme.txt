This is a simple electronic banking example.

There are two banks:-

Rabobank and VSBBank (don't ask - I'm from Holland)
Their services are started with BankServer.py.


The client runs some transactions on both banks (if found), like:-
-creating accounts
-deleting accounts
-deposit money
-withdraw money
-inquire balance

The VSBBank will not allow the client to overdraw and have a negative
balance, the RaboBank will.

Currently the only thing lacking that would make this really useful is
persistence: if the bank offices are closed (i.e. the servers are shut
down), all account information is lost.


This is a nice starting point for your own Pyro projects.

See also the Bank2 example which is more advanced,
and has an interactive client to create accounts, 
and to deposit and withdraw money.


