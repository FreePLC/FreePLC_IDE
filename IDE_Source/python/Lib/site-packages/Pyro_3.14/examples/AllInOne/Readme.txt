The purpose of this example is to show how to build a single application
that starts up everything it nees from Pyro itself (NS, ES, what not).

The application creates a Name Server, Event Server,
Pyro server with event publisher, and an event listener.

The main loop calls Pyro objects to set some artificial
properties. Those objects publish those events on a ES channel,
on which an event listener is subscribed. That listener prints
the events that it receives.


allinone_threads.py: uses THREADS to run everything concurrently.
allinone_ownloop.py: uses a CUSTOM EVENT LOOP for everything.


NOTE: no Name Server must be running.

NOTE2: this example doesn't show what a good solution might be to
run everything in a monolithic application!!! 
For instance, if you want publish-subscribe notifications inside
your own application, and it is not distributed, why even use
Pyro's Event Server? Just build your own 'event' dispatch object
as a regular Python class and everything will be much easier.
You only *need* Pyro's ES if you want it to be distributed...
