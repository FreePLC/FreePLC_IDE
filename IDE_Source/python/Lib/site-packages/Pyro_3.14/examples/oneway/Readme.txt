This shows how oneway method calls work.
The client uses a oneway call to the server to start
it. In the meantime, it continues by itself and does some
things. After a short while, it uses regular Pyro calls again
to check on the server until it is ready.

Things to notice:
Not only will the client continue immediately after the oneway
method has been called, the server will also process the method
invocation 'in the background'. Other methods may be called while
the oneway call -which takes a while to complete- is still running.

For more information see the Features chapter in the manual
(callbacks & oneway calls).


PYRO_ONEWAY_THREADED config item:

This server sets PYRO_ONEWAY_THREADED to True, so Pyro will run incoming
oneway method calls in their own thread. This allows for the server to
continue to process other method calls on this object in the meantime!
That is why the client can "poll" for server completion.
(this is the default setting, by the way).

Try setting PYRO_ONEWAY_THREADED to False in the server and see what happens.
The client tries to poll the server for completion, but the method call blocks
until the call to the 'oneway' method finished processing.
