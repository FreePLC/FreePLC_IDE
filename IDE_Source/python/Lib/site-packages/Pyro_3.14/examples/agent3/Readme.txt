This test shows another mobile 'agent' system, where the
agent travels from server to server (three, in this example).
The anwser in the end travels back from 3 to 2 to 1 and 
is then returned to the client.
("true" agent travel, where the answer would be returned
from the final destination of the agent directly back to
the calling client, is not yet available in Pyro).

This test shows that Pyro can send along the agent's module
bytecode. It used to load it from the module's source file,
but that is not possible if you're passing the agent on
to other servers (the dynamically loaded bytecode no longer
has a file associated). 

Also see 'agent2' for a more thorough mobile code example and
explanation.

** running this example **
1. cd into the serv/ directory
2. start the three servers (separate processes)
3. cd back into the main directory
4. start the client program and observe the result.

