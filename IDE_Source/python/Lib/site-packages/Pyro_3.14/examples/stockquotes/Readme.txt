This simple stock quote server shows the use of the Event Service.
Clients subscribe to certain stock quotes.
Stock markets publish certain stock quotes at random intervals.
The interested clients receive the quotes.

MAKE SURE THAT THE EVENT SERVICE (es) HAS BEEN STARTED IN ADVANCE.

You may want to start multiple clients in different windows that
listen to different (or the same!) stock symbols.
If you start a second or third server, stock quotes will 
be generated faster because there are multiple publishers!

Publishers don't know the interested parties and the listeners
don't know where the quotes come from.

The MClient program uses a pattern match for subscribing.


See also the countingcars example.


Note: the Server_noNS and Client_noNS show the use of the event server
without using the name server. You can start the Event server itself with the -N
parameter. This way you don't need to have a name server running.
