This is a simple electronic banking example.

It looks a lot like the other banking example (BankExample) but
it has some important differences:

1. It uses the Pyro 1.2+ feature to directly access object attributes;
2. It uses the Pyro 1.2+ feature to create new objects on the server
   and to pass proxies to those objects back to the client.
   The creation of accounts is realised this way. Clients get a real
   account object on which they can call deposit and withdraw methods.
3. The client is interactive.
4. It uses the Pyro 3.0 'transient object timeout reaping' feature.

There are two banks:-

Rabobank and VSBBank (don't ask - I'm from Holland)
Their services are started with BankServer.py.


The client starts an interactive loop in which you can
-create accounts
-delete accounts
-deposit money
-withdraw money
-inquire balance

The VSBBank will not allow you to overdraw and have a negative
balance, the RaboBank will.


The bank has a maximum account inactivity time (say 20 seconds).
If an account has not been accessed for that time, it will be
reaped on the server. The transient account object will be deleted
after it has notified the bank that it must be removed.
See the server console for messages indicating that this took place.


Currently the only thing lacking that would make this really useful is
persistence: if the bank offices are closed (i.e. the servers are shut
down), all account information is lost.


This is a nice starting point for your own Pyro projects.

