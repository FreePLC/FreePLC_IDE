Cell-based- or distributed computing: md5 'cracking' and sorting.
An MIMD (multiple instruction-multiple data) parallel system.
Uses Pyro's mobile code feature to transfer the tasks to
the cell processors, so it's also very easy to feed them
new, other kinds of tasks.

*** Starting up ***
- start the Name Server
- start the Event Server
- cd into the cell/ directory
- start the Dispatcher (dispatcher.py)
- start a Monitor (monitor.py) to monitor the progress
- start one or more processing 'cells' (processor.py). For best results,
  start one of these on every machine/CPU in your network
- finally, give the system a task to solve: start the client.py program.
  Choose what you like to do: md5 cracking or sorting a huge list of 
  random letters.

  MD5: "frogs" is a nice string for it to solve.
  Sorting: a list size of 20000 (twenty thousand) is nice for starters.

- Select '1' to see how your system works when it solves the task
  'locally' (in a single Python process),
  select '2' to have fun and observe how the distributed system does it.
  On my 2 computers at home it guesses "frogs" in about 30 seconds
  (on a single computer it takes 60 seconds);
  it sorts a 50000-element list in 20 seconds (on a single computer
  the same task takes 40 seconds).

- while the system solves the task, observe the monitor program to see
  how the different tasks are progessing.
  
  The effect will be better the more computers participating, ofcourse,
  but having 2 or 3 is usually enough already for interesting results.

** NOTE: starting/removing cells after the dispatcher has run will not work **


*** What the heck is this, anyway? ***

This is a distributed task processor, with two specific tasks implemented:
the 'cracking' or 'guessing' of strings that make up a given secure
MD5 hash code. It does this by brute-force search: simply try all strings
from aaaaa to zzzzz (example) and see if the MD5 hash is the same.
Words longer than 5 letters take a long time to guess...
The other task is distributed sorting of a huge list of random letters.
The sorting algorithm is a dumb, slow one that works similar to
insertion sort with a final single merge sort pass at the end.

You enter the string to guess, a MD5 hashcode is generated from it,
or with the sorting task, a long list of random letters is generated,
and then the task is divided over the available cell processors.
They each work trough a part of the search space in parallel, thus
greatly improving computation power. The more computers you add in the
network (and start a cell processor on), the faster it finds your
"secret" string or sorts the list!


- The Pyro Namespace is used to register and discover the
  set of available processing cells. The task dispatcher just
  asks the NS for a list of registered processors, to see
  where it can send the tasks to.
  The cells are called:
   :Distributed.Cells.processor1
   :Distributed.Cells.processor2
   :Distributed.Cells.processor3  and so on.

- The Event Server is used to channel the processor's progress reports.
  Every cell processor emits progress reports during the calculation
  that it performs and the monitor script listens for these reports.
  It displays them in nice bar graphs.

- The task implementation that is used here for the md5 cracker can be
  aborted. This is used to signal all processors to stop as soon as
  one of them has found the solution.
 
- The way the Task and TaskPartition classes are designed should make
  it very easy to add your own specific task implementation that you
  would like to use in this system. Distributed PI computation,
  image processing, whatever. Any task that can be partitioned.
  It is NOT required that every partition is of equal size, and it
  is also NOT required to exactly have N partitions where N=number
  of cells. The dispatcher takes care of it all.
  Many smaller partitions are better than a few large ones though,
  because response time will be better.

- Because the mobile code feature is used to transfer the tasks,
  the cell processors need not have the code for the computation
  task available. You can feed them any task you like :-)
  (as long as it uses the Task/TaskPartition API)
 
- Because of a bug in Pyro 3.4 and older you can only run this example
  correctly on Pyro 3.5+ (older versions didn't process oneway method
  calls in the way that was intended, and froze on subsequent calls).

