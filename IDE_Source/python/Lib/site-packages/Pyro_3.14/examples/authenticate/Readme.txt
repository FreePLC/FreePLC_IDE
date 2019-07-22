Example of connection Authentication.


FIRST: Starting the NS with authentication enabled

You need to use authentication on the Name Server too:--

Either start 'ns' with a custom authentication ID option ("s3cr3t"),
or use a custom security plugin (supplied).

To use the security plugin, which prints the authentication process,
make sure the current directory ('.') is part of your PYTHONPATH,
because otherwise the security module cannot be loaded from this
directory (this is correct -safe- behavior of Python).

Start the nameserver with:
	"ns -v -s NSSecEx"

It will show you that it's using your security plugins.
(If you don't use the -v flag, you won't see this on the console)

Using a custom connection validator enables you to have more
control over the authentication process, and to specify
multiple allowed authentication IDs.



Running the server and client:

The server tells Pyro that it wants to use a limited set of
allowed authentication IDs. Pyro will now refuse any new
client connection that does not supply one of the allowed IDs.

The client asks for the ID. You can deliberately enter a wrong
ID to see what happens.
(first id is for connecting to the Name Server, second is for
connecting to the test server).
