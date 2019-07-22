This example contains:

- a stress test for the Naming Server (naming.py)

This test creates a bunch of threads that connect to the NS
and create/delete groups and object registrations randomly, very fast.


- a stress test for the Event Server (producer.py and consumer.py)

The producer starts a bunch of threads that all publish events very fast
on the same channel. The consumer creates a bunch of consumers that
all listen on that channel.


No other stress tests seem necessary because the two above exercise
most of Pyro's features.

You should keep an eye on the CPU load and the memory usage. Both
should be stable.

