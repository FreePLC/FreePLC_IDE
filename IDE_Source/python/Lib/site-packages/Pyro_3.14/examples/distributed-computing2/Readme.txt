A bit easier distributed computing example as the first.
This one uses a "pull" model instead of a "push" model:
there is a single central work dispatcher/gatherer that is contacted
by every worker you create. The worker asks the dispatcher for a chunk
of work data and returns the results when it is done, ad infinitum.

For simplicity sake, there is no mobile code involved in this example.
There is no real-time monitor as well.
For a more generic system that allows for different worker tasks,
and with realtime monitoring, see the first distributed-computing example.


*** Starting up ***
- start the Name Server
- start the Dispatcher (dispatcher.py)
- start one or more workers (worker.py). For best results,
  start one of these on every machine/CPU in your network
- finally, give the system a task to solve: start the client.py program.



WHAT DOES THIS THING DO ANYWAY???

It computes Prime Factorials of a bunch of random numbers.
The client program generates a list of random numbers and sends
each number as a single work item to the dispatcher.
One or more workers pick work items from the dispatcher and go
to factorize the number. They place their result back into the
dispacher.
The client collects all results and prints a nice table afterwards.

The dispatcher is really not more than 2 threadsafe queues wrapped
in a Pyro object.

The more workers you will start (one per cpu/core/machine) the faster
the list of results will be produced, because every worker will do
the factorization of its current work item in parallel to the others.
