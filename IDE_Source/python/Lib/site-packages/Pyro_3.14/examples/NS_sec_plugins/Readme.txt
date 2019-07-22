Example of Name Server security plugins.
This shows possible implementations of a NS BC request validator
(the one here denies all shutdown requests)
and a NS new connection validator (the one here prints
some info of the client wanting a Pyro connection, and
requires a special identification passphrase to connect. Use
the -i option with nsc).

Make sure the current directory ('.') is part of your PYTHONPATH,
because otherwise the security module cannot be loaded from this
directory (this is correct -safe- behavior of Python).

Start the nameserver with:
	"pyro-ns -v -s NSSecEx"
or	"python -m Pyro.naming -v -s NSSecEx"

It will show you that it's using your security plugins.
Then try to use the commands from the "nsc" or "xnsc" tool and
see what happens and what is printed on your screen.

