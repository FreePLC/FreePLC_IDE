This test is for checking how Pyro handles the maximum number of
client connections. It shows a possible way to deal with the
event that the Pyro server is fully occupied with connections.

Also it uses the Delegate Pattern on the server side instead of
subclassing the Pyro.core.ObjBase.
