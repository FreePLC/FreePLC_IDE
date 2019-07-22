Chat box example using the Event Server


This chat box example is constructed as follows:

- a Chat Server (Pyro object) handles the login/logoff process
  and hands out Event Server topics for the desired channels
- the Event Server is used to do the chatting itself.

If the chat server dies, all people currently chatting can continue
to do so because the chatting relies only on the Event Server.

The chat client uses two threads, one for incoming chat messages,
and one for reading and publishing the user's input.

You'll have to start the Event Server ofcourse before running
this example.
