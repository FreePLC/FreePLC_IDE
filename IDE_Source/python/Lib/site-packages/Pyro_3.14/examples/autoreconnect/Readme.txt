This is an example that shows the auto reconnect feature.

Start the server and the client.
You can stop the server while it's running.
The client will report that the connection is lost, and that
it is trying to rebind.
Start the server again. You'll see that the client continues.

The server_no_ns.py and client_no_ns.py show how to do this without
a name server.

NOTES:

1- your server has to be prepared for this feature. It must not rely
   on any transient internal state to function correctly, because
   that state is lost when your server is restarted. You could make
   the state persistent on disk and read it back in at restart.
2- your server MUST register the objects with the new connectPersistent
   method of the PyroDaemon. Otherwise the reconnect feature DOES NOT WORK
   because the client tries to access an invalid URI.
3- the NS does NOT have to be the persistent version on disk, as long as
   it keeps running. All that is needed is that the URI of the objects
   concerned stay available in the NS, so the server can reuse those URIs
   when it gets back up.
4- the client is responsible for detecting a network problem itself.
   It must call the 'hidden' rebindURI() method of the object's
   protocol adapter itself if this is the case.
5- Examine the example code provided here, and Pyro's internal adapter code,
   to see how the rebind feature works.

6- Why isn't this transparent???? Because you HAVE to have control about
   it when a network problem occurs. Furthermore, only YOU can decide
   if your system needs this feature, and if your system can SUPPORT this
   feature (see point 1 and 2 above).

