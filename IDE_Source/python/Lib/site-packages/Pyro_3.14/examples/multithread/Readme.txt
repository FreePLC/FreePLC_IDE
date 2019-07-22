This example shows the need of multithreading in the Pyro server.
The client spawns serveral concurrent loops which access the same
remote object. If the Pyro server is single threading, each remote
invocation has to wait for the previous one to complete.
If the Pyro server is multithreading, each remote invocation is
processed simultaneously.


If your server is I/O bound, you may successfully run several
requests at the same time without noticable delay (because the
I/O gets executed in parallel).

If your sever is CPU bound, you may notice that the multithreading
has no effect, because the CPU is busy 100%. If you are lucky and
have multiple CPUs, you may experience speedup after all. But
no more than the number of cpus you have.


Thread Local Storage (TLS): the server access Pyro's TLS feature.
If you're running in single-threaded mode you'll see that the
counter is shared among all invocations (because there is only
one thread) and that it increases with each invocation.
If running multithreaded, you'll see that each caller/thread
has its own TLS and that the counters are increased independently.
The server also takes care of correct initialization of the TLS
by setting a custom initTLS function in the Daemon.

