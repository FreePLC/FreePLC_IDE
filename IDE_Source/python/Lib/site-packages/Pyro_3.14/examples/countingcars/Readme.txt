This example shows the use of the Event Service.
There is a client that counts certain types of cars that are passing.
The passing of cars in a particular direction is published by Server.py.
Clients subscribe to certain directions, and notice the cars
that pass that way. After a certain amount of cars, the client
switches direction and counts the cars there.
It stoppes counting cars from the previous direction (unsubscribe).
If all compass directions have been counted, the client exits.

Make sure that the event server (es) has been started in advance.

If you start a second or third server, cars will pass by faster
because there are multiple publishers!


See also the stockquotes example.
