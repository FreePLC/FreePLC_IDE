
This directory contains 4 callback examples:
Shout, Bouncing, Bouncing2 and BounceError.


SHOUT CALLBACK EXAMPLE
----------------------

This example shows how to use callbacks from server to client.
It also makes use of the oneway call that was introduced in Pyro 2.4.
The callback call is made oneway. This way the server can't be
blocked by slow or buggy clients that fail to process the
callback quickly.

As you will see, you have to create your client not only as
a client, but also as a Pyro server, because it will have to
receive incoming Pyro calls.

Also have a close look at the server. You need to take several
things into account when dealing with subscribed callback objects.
They may raise exceptions, they may get killed (no connection anymore)
and many other things.

This example may have some race conditions in the server because
the 'shout' method may be called concurrently from different threads.
You should use a thread lock on the list of subscribers.

Server: shout_server.py
Client: shout_client.py
separate shouter: shout.py



BOUNCING CALLBACK EXAMPLE
-------------------------

This example shows how multiple Pyro objects could call back
to each other, effectively bouncing a message around.
(up to a certain limit, in this example: 100 invocations).
This is sometimes called a conversation between objects.

The client calls the server, which calls back to the client,
which calls back to the server, which calls back to the client....

The server is just a regular Pyro server that serves a single
"bouncer" object. The client also serves its own "bouncer" object,
but has to run a separate thread to process the Pyro daemon loop.

Because both client and server pass a new callback proxy at each
method call, a new socket connection and thread is used for
the callback. This makes sure that all calls get processed,
and that no deadlock occurs.

Server: bounce_server.py
Client: bounce_client.py
bouncer object: bounce.py


BOUNCER2: broken code that triggers deadlock
---------------------------------------------
The (broken!) bouncer2 code triggers a deadlock problem that is
present in Pyro: a conversation between objects using a *single*
registered callback proxy deadlocks because Pyro is still waiting
for the other process to answer the callback invocation, instead
of invoking the object again!
Server: b2_server.py
Client: b2_client.py


BOUNCE_ERROR
------------
Server: bounce_server.py
Client: cberror_client.py
This callback example shows the use of CallbackObjBase as a base
class for your callback objects, instead of ObjBase.
The callback function throws an error and you'll see that it
is not only returned to the server (who called the callback object),
but it is also rethrown on the client, because the client usually
is most interested in errors that occur in its own callback objects.

