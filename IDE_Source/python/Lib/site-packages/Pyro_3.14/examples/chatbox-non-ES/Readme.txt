Chat box example without using Event Server


This chat box example is constructed as follows:

- a Chat Server (Pyro object) handles the login/logoff process
  and keeps track of all chat channels and clients that are
  subscribed to each channel
- The Chat Server itself implements the chatting and distributing
  of chat messages to all subscribers. It uses Pyro's oneway calls
  to improve performance and to avoid blocking.

The chat client uses two threads, one for incoming chat messages,
and one for reading and publishing the user's input.

See also the 'callbacks' example. Many of the details shown there
also apply here (oneway callback method, handling of killed
callback clients, threading issues).

[Your conclusion should be: unless you want more flexibility,
use the Event Server if it can do the job!]
