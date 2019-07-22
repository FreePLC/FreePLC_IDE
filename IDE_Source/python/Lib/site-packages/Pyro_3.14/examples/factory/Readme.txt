This example shows the 'factory' feature of Pyro:
it shows how to create new objects on the server and pass them back to
the client (actually, not the objects themselves but proxies are passed
back). 

The example uses PID (process IDs) to show that the produced objects
actually live on the server, not the client.
The server runs single-threaded, this way all pids are the same.
