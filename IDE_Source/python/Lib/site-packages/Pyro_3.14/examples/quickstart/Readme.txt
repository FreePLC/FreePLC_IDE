This is a Pyro Quickstart example.
Using the supplied "remote.py" module, it becomes extremely
easy to set up a distributed object system using Pyro.
(The module is in the extensions package: Pyro.ext.remote)

But, using the "pyrorun" script, it is even easier to provide
Python objects as remote Pyro objects; you don't have to write
a single line of server code. Great for testing.
Type
$ pyrorun
to see a short help text, and Type
$ pyrorun --verbose object
to load the object.py module and to start a Pyro server for
the "quickstart" object (myObject). This is exactly the same object
as server.py uses. In both cases, client.py is the client
that accesses this remote object.



The remote.py module was kindly provided by John Wiegley.
It requires the "signal" module, which is not available on certain systems.

To create a server, and remote an object from it, use this snippet:
    import sys
	from Pyro.ext import remote
    
    remote.daemon_port = port
    remote.verbose = verbose
    
    remote.provide_local_object(MyObject(), 'my_object')
    
    sys.exit(remote.handle_requests())

This will look for a nameserver by broadcast.  Optionally, the keyword
argument 'nameserver' can be passed to 'provide_local_object'.

To get a proxy for 'my_object' from a client package:

    from Pyro.ext import remote
    my_object = remote.get_remote_object('my_object')


[note: remote.py will first unregister any previous occurence of a name
 in the NameServer, and then register the new name. Existing bindings
 will be silently overwritten. ]



See also the quickstart-noNS example, which doesn't use the Name Server at
all.
