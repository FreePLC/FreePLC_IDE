This test is for showing how you might implement host/IP-based
access control for new connections.

It uses the Pyro feature to set a custom newConnectionValidator.
The validator will ask you to accept or deny any new connections
that occur to the server. Try it out, start the client from
various machines and answer yes or no on the server when it
asks you about the new connections.

Note that even if you accept the connection, the custom validator
then calls the default validator. This one then still checks if
the max. number of connections is not exceeded.

You might want to skip that last step, or re-implement it yourself
(but you'll have to look at the code of the default validator,
Pyro.protocol.DefaultConnValidator) because it accesses some
internal structures of the daemon.

